"""Engineering AnnData fixtures only; no model or scientific validation."""
import ast
import copy
import importlib.util
import io
import json
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

import numpy as np
import pandas as pd

# AnnData 0.11 eagerly probes its optional PyTorch loader; this test needs only CPU arrays.
find_spec = importlib.util.find_spec
with patch("importlib.util.find_spec", side_effect=lambda name, package=None:
           None if name == "torch" else find_spec(name, package)):
    import anndata as ad


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_perturbation.py"
LEGACY_ERRORS = []


def cleanup_code(legacy=False):
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    compute, = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "compute"]
    start = next(i for i, node in enumerate(compute.body)
                 if isinstance(node, ast.Expr) and ast.unparse(node.value).startswith("result.layers.pop("))
    stop = next(i for i, node in enumerate(compute.body)
                if isinstance(node, ast.Assign) and ast.unparse(node.targets[0]) == "result.obs['latent_time']")
    nodes = copy.deepcopy(compute.body[start:stop + 1])
    if legacy:
        loop, = [node for node in nodes if isinstance(node, ast.For)
                 and ast.literal_eval(node.iter) == ("velocity_self_transition", "latent_time_posterior_mean")]
        loop.body = ast.parse("result.obs.pop(key, None)").body
    return compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])), str(SCRIPT), "exec")


def fixture(inherited=True, constant_time=False):
    result = ad.AnnData(np.array([[1., 0.], [2., 1.], [0., 3.]]),
                        obs=pd.DataFrame({"sample": ["a", "a", "b"], "latent_time": [8., 9., 10.]},
                                         index=["cell_1", "cell_2", "cell_3"]),
                        var=pd.DataFrame(index=["TF1", "target1"]))
    result.layers["velocity"] = np.array([[-.2, .4], [.1, -.3], [.5, .2]])
    result.layers["fit_t"] = (np.full((3, 2), 4.) if constant_time
                              else np.array([[0., 2.], [2., 4.], [4., 6.]]))
    result.obsm["lineages_fwd"] = np.array([[.8, .2], [.4, .6], [.1, .9]])
    result.uns["fate_metadata"] = {"lineages": ["fixture_A", "fixture_B"]}
    if inherited:
        result.layers["velocity_std"] = np.ones((3, 2))
        result.obsm["velocity_umap"] = np.ones((3, 2))
        for key in ("velocity_graph", "velocity_graph_neg", "velocity_uncertainty"):
            result.uns[key] = "inherited"
        result.obs["velocity_self_transition"] = [.1, .2, .3]
        result.obs["latent_time_posterior_mean"] = [7., 8., 9.]
    return result


class SensitivityCleanupRegression(unittest.TestCase):
    def test_legacy_dataframe_pop_failure_is_reproduced(self):
        for inherited in (True, False):
            with self.subTest(inherited=inherited):
                with self.assertRaisesRegex(TypeError, "positional arguments") as caught:
                    exec(cleanup_code(legacy=True), {"result": fixture(inherited), "np": np})
                LEGACY_ERRORS.append(str(caught.exception))

    def check_cleanup(self, inherited, constant_time=False):
        result = fixture(inherited, constant_time)
        before = result.copy()
        exec(cleanup_code(), {"result": result, "np": np})
        self.assertNotIn("velocity_std", result.layers)
        self.assertNotIn("velocity_umap", result.obsm)
        for key in ("velocity_graph", "velocity_graph_neg", "velocity_uncertainty"):
            self.assertNotIn(key, result.uns)
        for key in ("velocity_self_transition", "latent_time_posterior_mean"):
            self.assertNotIn(key, result.obs)
        np.testing.assert_array_equal(result.obs["latent_time"], [0., 0., 0.] if constant_time else [0., .5, 1.])
        np.testing.assert_array_equal(result.layers["velocity"], before.layers["velocity"])
        np.testing.assert_array_equal(result.layers["fit_t"], before.layers["fit_t"])
        np.testing.assert_array_equal(result.obsm["lineages_fwd"], before.obsm["lineages_fwd"])
        np.testing.assert_array_equal(result.X, before.X)
        pd.testing.assert_series_equal(result.obs["sample"], before.obs["sample"])
        pd.testing.assert_index_equal(result.obs_names, before.obs_names)
        pd.testing.assert_frame_equal(result.var, before.var)
        self.assertEqual(result.uns["fate_metadata"], before.uns["fate_metadata"])

    def test_current_cleanup_with_inherited_fields_present_or_absent(self):
        for inherited in (True, False):
            with self.subTest(inherited=inherited):
                self.check_cleanup(inherited)

    def test_constant_fit_t_produces_finite_zero_latent_time(self):
        self.check_cleanup(True, constant_time=True)


if __name__ == "__main__":
    output = Path(__file__).resolve().parent / "validation_logs"
    output.mkdir(exist_ok=True)
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SensitivityCleanupRegression)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    heavy_imports = [name for name in ("torch", "scvi", "regvelo", "cellrank") if name in sys.modules]
    summary = {"status": "PASS" if result.wasSuccessful() and not heavy_imports else "FAIL",
               "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
               "legacy_failure_reproduced": len(LEGACY_ERRORS) == 2, "legacy_errors": LEGACY_ERRORS,
               "model_stack_imports": heavy_imports,
               "anndata_optional_torch_import_disabled": True,
               "scope": "AST-extracted actual cleanup block on engineering AnnData fixtures; no model or scientific validation"}
    (output / "sensitivity_cleanup.log").write_text(stream.getvalue() + "\n" + json.dumps(summary, indent=2), encoding="utf-8")
    (output / "sensitivity_cleanup_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(stream.getvalue())
    print(json.dumps(summary, indent=2))
    raise SystemExit(0 if summary["status"] == "PASS" else 1)
