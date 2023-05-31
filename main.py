from pathlib import Path

import typer
from loguru import logger

from customercounter import start_probe_requests_listener


def main(interface: str, logs_out: Path = "./out/logs.txt"):
    logger.add(logs_out, diagnose=False, backtrace=False)
    start_probe_requests_listener(interface)


if __name__ == "__main__":
    typer.run(main)
