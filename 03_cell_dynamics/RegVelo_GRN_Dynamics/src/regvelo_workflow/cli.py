"""Unified CLI with explicit state, failure logs, and config-relative paths."""
import argparse
import hashlib
import json
import logging
import os
import sys
import time
import traceback
from pathlib import Path

STAGES = ("audit", "prepare", "fit", "velocity", "fate", "grn", "perturb", "visualize", "report")


def load_config(path):
    path = Path(path).resolve()
    config = json.loads(path.read_text(encoding="utf-8-sig"))
    for key in ("input", "grn", "output"):
        if key not in config:
            raise ValueError(f"Missing configuration key: {key}")
        value = os.path.expandvars(config[key])
        if "$" in value or "%" in value:
            raise ValueError(f"Unresolved environment variable in {key}: {value}")
        target = Path(value).expanduser()
        config[key] = str(target.resolve() if target.is_absolute() else (path.parent / target).resolve())
    if Path(config["input"]).resolve() == Path(config["output"]).resolve():
        raise ValueError("Output must be a separate directory, not the source input.")
    return config


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    temp.replace(path)


def main(argv=None):
    parser = argparse.ArgumentParser(description="RegVelo: official GRN-aware RNA dynamics / 官方模型流程")
    parser.add_argument("stage", choices=(*STAGES, "all"))
    parser.add_argument("--config", required=True, help="JSON config; paths resolve relative to its directory")
    parser.add_argument("--tf", nargs="+", help="Override perturb.tfs; gene identifiers are case-sensitive")
    parser.add_argument("--resume", action="store_true", help="Skip completed stages with the same config and existing artifacts")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        if args.tf:
            config.setdefault("perturb", {})["tfs"] = args.tf
        output = Path(config["output"])
        output.mkdir(parents=True, exist_ok=True)
        (output / "logs").mkdir(exist_ok=True)
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.FileHandler(output / "logs" / "workflow.log", encoding="utf-8"), logging.StreamHandler()])
    digest = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
    state_path = output / "run_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"stages": {}}
    write_json(output / "resolved_config.json", config)
    stages = STAGES if args.stage == "all" else [args.stage]
    for stage in stages:
        previous = state["stages"].get(stage, {})
        if (args.resume and previous.get("status") == "PASS" and previous.get("config_hash") == digest
                and previous.get("artifacts") and all(Path(p).exists() for p in previous["artifacts"])):
            logging.info("Resuming: %s already completed", stage)
            continue
        record = {"status": "RUNNING", "config_hash": digest, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        state["stages"][stage] = record
        write_json(state_path, state)
        start = time.monotonic()
        try:
            if stage in ("prepare", "fit", "velocity", "fate", "perturb"):
                from . import dynamics
                result = getattr(dynamics, f"run_{stage}")(config, output)
            elif stage in ("audit", "grn", "report"):
                from . import core
                result = getattr(core, f"run_{stage}")(config, output)
            else:
                from .plots import run_visualize
                result = run_visualize(config, output)
            record.update(result or {})
            record.setdefault("artifacts", [])
            record["status"] = record.get("status", "RUNNING") if record.get("status") != "RUNNING" else "PASS"
        except Exception as error:
            error_path = output / "logs" / f"{stage}_error.log"
            error_path.write_text(traceback.format_exc(), encoding="utf-8")
            record.update(status="FAIL", error=f"{type(error).__name__}: {error}", error_log=str(error_path))
            logging.exception("Stage %s failed", stage)
            record["elapsed_seconds"] = round(time.monotonic() - start, 3)
            write_json(state_path, state)
            return 1
        record["elapsed_seconds"] = round(time.monotonic() - start, 3)
        record["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        write_json(state_path, state)
        if stage == "report":
            # Refresh after its final status is persisted; avoid publishing RUNNING in a completed report.
            core.run_report(config, output)
        logging.info("%s: %s (%.1fs)", stage, record["status"], record["elapsed_seconds"])
        if record["status"] == "FAIL":
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
