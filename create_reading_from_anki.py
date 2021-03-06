#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description of script
"""

import sys
import argparse
import ankipandas
import logging
import random
import jieba
import hanziconv
import pandas as pd

LOGGER = logging.getLogger(__name__)


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
    cards = col.cards.merge_notes()
    reading_cards = cards[cards["cdeck"] == "1a_myChinese\x1fReading"]
    currently_learning_cards = reading_cards[
        (reading_cards["cqueue"] == "learning")
        | (reading_cards["cqueue"] == "in learning")
    ]
    trad_chars = currently_learning_cards.apply(lambda row: row["nflds"][1], axis=1).tolist()
    
    learning_sentences=[]
    sentence_df = pd.read_csv("data/graded_sentences.csv")
    sentence_df["char_list"] = sentence_df.apply(lambda row: list(jieba.cut(row["hanzi"])),axis=1)
    for char in trad_chars:
        tmp=sentence_df[pd.DataFrame(sentence_df.char_list.tolist()).isin([char]).any(1).values]
        tmp=tmp[:3]
        for index, row in tmp.iterrows():
            learning_sentences.append(row["hanzi"])

    random.shuffle(learning_sentences)
    with open("../../Dropbox/scr/learning_sentences.txt","w") as ff:
        for sen in learning_sentences:
            trad_sen=hanziconv.HanziConv.toTraditional(sen)
            ff.write(trad_sen+"\n")




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
