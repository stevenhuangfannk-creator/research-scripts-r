"""Run input-contract tests and save actual text, JSON and JUnit evidence."""
import contextlib
import io
import json
import time
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def startTest(self, test):
        super().startTest(test)
        self.started = time.monotonic()

    def stopTest(self, test):
        self.records.append((test.id(), time.monotonic() - self.started))
        super().stopTest(test)


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    output = folder / "validation_logs"
    output.mkdir(exist_ok=True)
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(folder), pattern="test_input_contracts.py")
    with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
        runner = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=RecordedResult)
        result = runner.run(suite)
    (output / "input_contracts.log").write_text(stream.getvalue(), encoding="utf-8")
    failed = {test.id(): message for test, message in result.failures}
    errors = {test.id(): message for test, message in result.errors}
    xml = ET.Element("testsuite", name="RegVeloInputContracts", tests=str(result.testsRun),
                     failures=str(len(result.failures)), errors=str(len(result.errors)))
    for name, elapsed in result.records:
        case = ET.SubElement(xml, "testcase", name=name, time=f"{elapsed:.3f}")
        for tag, outcomes in (("failure", failed), ("error", errors)):
            if name in outcomes:
                ET.SubElement(case, tag).text = outcomes[name]
    ET.ElementTree(xml).write(output / "junit.xml", encoding="utf-8", xml_declaration=True)
    summary = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
               "failures": len(result.failures), "errors": len(result.errors),
               "scope": "Software fixtures: rejection, named GRN orientation, config paths and real CLI audit; not model validation",
               "log": "tests/validation_logs/input_contracts.log", "junit": "tests/validation_logs/junit.xml"}
    (output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(stream.getvalue())
    print(json.dumps(summary, indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)
