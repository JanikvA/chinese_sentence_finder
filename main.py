#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
short script to find sentences containing a certain chinese word
"""

import sys
import argparse
import logging
LOGGER = logging.getLogger(__name__)
import sqlite3


# fmt: off
def comandline_argument_parser(parser=None):
    if not parser:
        parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    if __name__ == "__main__":
        parser.add_argument("--loggers", nargs="*", default=[__name__], help="Changes the logging level of all the given loggers. 'root' is the global logger and __name__  is logger of this script")
        parser.add_argument("--logging-level", default="warning", choices=["notset", "debug", "info", "warning", "error", "critical"], help="Logging level")
        parser.add_argument("--logging-file", help="Logging file name")
    parser.add_argument("-w", "--word", help="word you are looking for in sentences")
    return parser
# fmt: on


def main(args):
    connection = sqlite3.connect("data/chinese_sentences.db")
    cursor = connection.cursor()
    sql=f"SELECT * FROM chinese_sentences WHERE chinese LIKE '%{args.word}%'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows[:10]:
        print(row)
    connection.close()



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
