import sys
import os
from pathlib import Path

import typer
from loguru import logger

from customercounter import run_program


def main(interface: str, logs_out: Path = "./out/logs.txt"):
    sys.stderr = os.devnull

    logger.remove()
    logger.add(logs_out, diagnose=False, backtrace=False)

    run_program(interface)



if __name__ == "__main__":
    typer.run(main)
