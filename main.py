#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO mine more sentences
# TODO make beter HSKaverage. Maybe ratio=HSKaverage + Sum (HSK_word_i - HSKaverage)**2 / words_in_sentence

"""
short script to find sentences containing a certain chinese word
"""

import sys
import argparse
import logging

LOGGER = logging.getLogger(__name__)
import sqlite3
import json
import jieba
import pandas as pd
import wordfreq


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

freq_dict = {1: 0.005, 2: 0.0008, 3: 0.0004, 4: 0.0002, 5: 0.00007, 6: 0.000001, 7: 0}
with open("data/hsk.json") as f:
    HSK_dict = json.load(f)


def get_HSK(char) -> int:
    for entry in HSK_dict:
        if entry["hanzi"] == char:
            return entry["HSK"]
    word_freq = wordfreq.word_frequency(char, "zh")
    if word_freq == 0:
        print(
            f"WARNING Can't identify frequency for {char}! It's probably a special character so will return HSK level 0"
        )
        return 0
    else:
        for hsk_level, freq_threshold in freq_dict.items():
            if word_freq > freq_threshold:
                return hsk_level


def get_complexity(chinese_sentence):
    list_of_chars = [
        char
        for char in jieba.cut(chinese_sentence)
        if char
        not in [
            "。",
            "？",
            "！",
            "，",
            "；",
            ".",
            "   ",
            ",",
            ":",
            '"',
            "?",
            "[",
            "]",
            "、",
            "｀",
        ]
    ]
    complexity = 0
    for char in list_of_chars:
        complexity += get_HSK(char) ** 2
    return complexity


def use_SQL(args):
    connection = sqlite3.connect("data/chinese_sentences.db")
    cursor = connection.cursor()
    sql = f"SELECT * FROM chinese_sentences WHERE chinese LIKE '%{args.word}%'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows[:10]:
        print(row, get_complexity(row[0]))
    connection.close()


def create_new_csv():

    sentence_df = pd.read_csv(
        "data/sentences.tsv",
        sep="\t",
        header=0,
        names=["hanzi", "pinyin", "english", "HSK_average", "custom"],
    )
    sentence_df = sentence_df.drop(["custom"], axis=1)
    sentence_df = sentence_df.drop(["HSK_average"], axis=1)
    sentence_df["complexity"] = sentence_df.apply(
        lambda row: get_complexity(row.hanzi), axis=1
    )
    all_senteces = sentence_df

    # sentence_df2 = pd.read_csv(
    #     "data/HSKsentences.tsv",
    #     sep="\t",
    #     header=0,
    #     names=["hanzi", "pinyin", "english"],
    # )
    # sentence_df2["complexity"] = sentence_df2.apply(
    #     lambda row: get_complexity(row.hanzi), axis=1
    # )
    # all_senteces = pd.concat([sentence_df, sentence_df2])

    all_senteces = all_senteces.drop_duplicates(subset=["hanzi"])
    all_senteces = all_senteces.sort_values(by=["complexity"])
    all_senteces.to_csv("data/graded_sentences.csv", index=False)


def main(args):

    # create_new_csv(args)

    sentence_df = pd.read_csv("data/graded_sentences.csv")
    sentence_df["char_list"] = sentence_df.apply(
        lambda row: list(jieba.cut(row["hanzi"])), axis=1
    )
    while True:
        word = input("####### Input word: ")
        tmp = sentence_df[
            pd.DataFrame(sentence_df.char_list.tolist()).isin([word]).any(1).values
        ]
        tmp = tmp[:6]
        print("--------------------")
        for index, row in tmp.iterrows():
            print(row["hanzi"])
            print(row["pinyin"])
            print(row["english"])
            print("--------------------")
        print()


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
