#!/usr/bin/env python3
"""Run one command with a hard process-group timeout."""

from __future__ import annotations

import os
import signal
import subprocess
import sys


def stop_process_group(process: subprocess.Popen[bytes]) -> None:
    os.killpg(process.pid, signal.SIGTERM)
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()


def run(timeout: float, command: list[str]) -> int:
    process = subprocess.Popen(command, start_new_session=True)
    try:
        return process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        print(
            f"TIMEOUT after {timeout:g}s: {' '.join(command)}",
            file=sys.stderr,
        )
        stop_process_group(process)
        return 124
    except KeyboardInterrupt:
        stop_process_group(process)
        return 130


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: run-with-timeout.py SECONDS COMMAND [ARG ...]", file=sys.stderr)
        return 2
    return run(float(argv[1]), argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
