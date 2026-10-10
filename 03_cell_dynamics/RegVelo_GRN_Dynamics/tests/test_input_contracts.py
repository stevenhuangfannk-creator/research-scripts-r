"""Software fixtures verify safety contracts; they are not research datasets."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse

MODULE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE / "src"))
from regvelo_workflow.cli import load_config
from regvelo_workflow.core import audit_adata, validate_grn


def software_fixture():
    counts = sparse.csr_matrix([[3, 0, 2], [1, 4, 0]], dtype=float)
    data = ad.AnnData(counts, obs=pd.DataFrame({"cell_type": ["fixture_a", "fixture_b"]}, index=["cell_1", "cell_2"]),
                      var=pd.DataFrame(index=["TF1", "target1", "target2"]))
    data.layers["spliced"] = counts.copy()
    data.layers["unspliced"] = sparse.csr_matrix([[1, 0, 1], [0, 2, 0]], dtype=float)
    return data


class InputAuditContracts(unittest.TestCase):
    def test_missing_splice_layer_is_rejected(self):
        for key in ("spliced", "unspliced"):
            with self.subTest(key=key):
                data = software_fixture()
                del data.layers[key]
                with self.assertRaisesRegex(ValueError, key):
                    audit_adata(data)

    def test_invalid_spliced_values_are_rejected(self):
        for value in (-1.0, np.nan, np.inf):
            with self.subTest(value=value):
                data = software_fixture()
                data.layers["spliced"].data[0] = value
                with self.assertRaisesRegex(ValueError, "Invalid spliced"):
                    audit_adata(data)

    def test_duplicate_identifiers_are_not_silently_renamed(self):
        for axis in ("obs_names", "var_names"):
            with self.subTest(axis=axis):
                data = software_fixture()
                names = list(getattr(data, axis))
                names[-1] = names[0]
                setattr(data, axis, names)
                with self.assertRaisesRegex(ValueError, "unique"):
                    audit_adata(data)
                self.assertEqual(list(getattr(data, axis)), names)

    def test_splice_presence_does_not_certify_raw_count_origin(self):
        result = audit_adata(software_fixture(), "cell_type")
        self.assertEqual((result["n_cells"], result["n_genes"]), (2, 3))
        self.assertIn("CONDITIONAL", result["readiness"])
        self.assertIn("UNKNOWN", result["raw_counts_provenance"])


class NamedGrnContracts(unittest.TestCase):
    def setUp(self):
        self.genes = ["TF1", "target1", "target2"]
        self.regulator_rows = pd.DataFrame([[2.0, -1.0]], index=["TF1"], columns=["target2", "target1"])

    def test_orientation_preserves_the_named_edge(self):
        target_rows = validate_grn(self.regulator_rows, self.genes, "regulator_by_target", ["TF1"])
        self.assertEqual(target_rows.loc["target2", "TF1"], 2.0)
        self.assertEqual(target_rows.loc["target1", "TF1"], -1.0)
        pd.testing.assert_frame_equal(target_rows, self.regulator_rows.T)
        pd.testing.assert_frame_equal(validate_grn(target_rows, self.genes, "target_by_regulator", ["TF1"]), target_rows)

    def test_auto_only_uses_unambiguous_regulator_names(self):
        target_rows = validate_grn(self.regulator_rows, self.genes, "auto", ["TF1"])
        pd.testing.assert_frame_equal(target_rows, self.regulator_rows.T)
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            validate_grn(self.regulator_rows, self.genes, "auto")

    def test_square_matrix_direction_cannot_be_guessed(self):
        square = pd.DataFrame([[0, 2], [-3, 0]], index=["TF1", "target1"], columns=["TF1", "target1"])
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            validate_grn(square, self.genes, "auto", ["TF1"])
        explicit = validate_grn(square, self.genes, "regulator_by_target", ["TF1"])
        self.assertEqual(explicit.loc["target1", "TF1"], 2)

    def test_duplicates_nonfinite_empty_edges_and_wrong_ids_are_rejected(self):
        duplicate = self.regulator_rows.copy()
        duplicate.columns = ["target1", "target1"]
        nonfinite = self.regulator_rows.copy()
        nonfinite.iloc[0, 0] = np.nan
        empty = self.regulator_rows * 0
        wrong = self.regulator_rows.rename(index={"TF1": "different_species_tf"})
        for frame, reason in ((duplicate, "duplicate"), (nonfinite, "non-finite"), (empty, "no effective"), (wrong, "No regulator/target")):
            with self.subTest(reason=reason), self.assertRaisesRegex(ValueError, reason):
                validate_grn(frame, self.genes, "regulator_by_target", ["TF1"])


class ConfigurationContracts(unittest.TestCase):
    def test_paths_are_relative_to_config_not_process_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            nested = base / "configs"
            nested.mkdir()
            path = nested / "job.json"
            path.write_text(json.dumps({"input": "../data/a.h5ad", "grn": "../data/grn.csv", "output": "../derived"}), encoding="utf-8")
            result = load_config(path)
            self.assertEqual(Path(result["input"]), base / "data" / "a.h5ad")
            self.assertEqual(Path(result["grn"]), base / "data" / "grn.csv")
            self.assertEqual(Path(result["output"]), base / "derived")

    def test_missing_keys_variables_and_source_overwrite_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "job.json"
            cases = [({"input": "a", "grn": "b"}, "Missing configuration key"),
                     ({"input": "$REGVELO_TEST_MISSING/input.h5ad", "grn": "b", "output": "out"}, "Unresolved"),
                     ({"input": "a.h5ad", "grn": "b.csv", "output": "a.h5ad"}, "separate")]
            previous = os.environ.pop("REGVELO_TEST_MISSING", None)
            try:
                for config, reason in cases:
                    with self.subTest(reason=reason):
                        path.write_text(json.dumps(config), encoding="utf-8")
                        with self.assertRaisesRegex(ValueError, reason):
                            load_config(path)
            finally:
                if previous is not None:
                    os.environ["REGVELO_TEST_MISSING"] = previous


class CliAuditContracts(unittest.TestCase):
    def invoke(self, config):
        return subprocess.run([sys.executable, str(MODULE / "scripts" / "regvelo.py"), "audit", "--config", str(config)],
                              capture_output=True, text=True, encoding="utf-8", timeout=60)

    def test_missing_input_records_real_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            config = base / "missing.json"
            config.write_text(json.dumps({"input": "missing.h5ad", "grn": "missing.csv", "output": "failure", "grn_orientation": "regulator_by_target"}), encoding="utf-8")
            process = self.invoke(config)
            self.assertEqual(process.returncode, 1, process.stderr)
            state = json.loads((base / "failure" / "run_state.json").read_text(encoding="utf-8"))
            record = state["stages"]["audit"]
            self.assertEqual(record["status"], "FAIL")
            self.assertTrue(Path(record["error_log"]).is_file())
            self.assertIn("missing.h5ad", Path(record["error_log"]).read_text(encoding="utf-8"))

    def test_audit_creates_outputs_without_modifying_input(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            data_path = base / "source.h5ad"
            grn_path = base / "prior.csv"
            software_fixture().write_h5ad(data_path)
            pd.DataFrame([[2, -1]], index=["TF1"], columns=["target2", "target1"]).to_csv(grn_path)
            before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in (data_path, grn_path)}
            config = base / "job.json"
            config.write_text(json.dumps({"input": "source.h5ad", "grn": "prior.csv", "output": "derived", "group_key": "cell_type", "grn_orientation": "regulator_by_target"}), encoding="utf-8")
            process = self.invoke(config)
            self.assertEqual(process.returncode, 0, process.stderr)
            for path, digest in before.items():
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)
            result = json.loads((base / "derived" / "INPUT_AUDIT.json").read_text(encoding="utf-8"))
            self.assertEqual(result["grn"]["edges"], 2)
            state = json.loads((base / "derived" / "run_state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["stages"]["audit"]["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
