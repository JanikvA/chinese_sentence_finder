#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description of script
"""

import sys
import argparse
import logging
LOGGER = logging.getLogger(__name__)
import ankipandas


# fmt: off
def comandline_argument_parser(parser=None):
    if not parser:
        parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    if __name__ == "__main__":
        parser.add_argument("--loggers", nargs="*", default=[__name__], help="Changes the logging level of all the given loggers. 'root' is the global logger and __name__  is logger of this script")
        parser.add_argument("--logging-level", default="warning", choices=["notset", "debug", "info", "warning", "error", "critical"], help="Logging level")
        parser.add_argument("--logging-file", help="Logging file name")
    return parser
# fmt: on


def main(args):
    col = ankipandas.Collection()
    # note = col.notes["nflds"][501]
    # selection = col.notes["nflds"][501]
    selection = col.notes[col.notes['nmodel']=="Simple Model linedict"]
    selection["nflds"] = selection.apply(lambda row: row["nflds"],axis=1)
    # note[-1]="test"
    # print(note[-1])
    # col.notes.update(note)
    col.notes.update(selection)
    col.summarize_changes()
    # col.write(modify=True)




if __name__ == "__main__":
    parser = comandline_argument_parser()
    command_line_arguments = parser.parse_args()
    logging.basicConfig(
        filename=command_line_arguments.logging_file,
        format="%(levelname)s [%(filename)s:%(lineno)s - %(funcName)s() ]: %(message)s",
    )
    logLevel = getattr(logging, command_line_arguments.logging_level.upper())
    for logger in command_line_arguments.loggers:
        if logger == "root":
            tmpLOGGER = logging.getLogger()
        else:
            tmpLOGGER = logging.getLogger(logger)
        tmpLOGGER.setLevel(logLevel)
    LOGGER.info(command_line_arguments)
    sys.exit(main(command_line_arguments))
