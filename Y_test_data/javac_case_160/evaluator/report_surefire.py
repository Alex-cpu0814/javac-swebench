#!/usr/bin/env python3
"""Emit Maven Surefire XML results in the evaluator's stable line format."""

import pathlib
import sys
import xml.etree.ElementTree as ET


def main():
    report_dir = pathlib.Path(sys.argv[1])
    found = 0
    for path in sorted(report_dir.glob("TEST-*.xml")):
        root = ET.parse(path).getroot()
        for case in root.iter("testcase"):
            class_name = case.get("classname", "unknown")
            method = case.get("name", "unknown")
            if case.find("failure") is not None:
                status = "FAIL"
            elif case.find("error") is not None:
                status = "ERROR"
            elif case.find("skipped") is not None:
                status = "skipped"
            else:
                status = "ok"
            print(f"{method} ({class_name}) ... {status}")
            found += 1
    if found == 0:
        print("No Surefire test results found", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
