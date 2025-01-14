#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

import pytest

from tests.model import AnkiDeck, AnkiNote

import pypinyin

SOUND_TAG = "[sound:hypertts-"
DISAMBIGUATE_TAG = "【"


def extract_pinyin(note: AnkiNote) -> str:
    pinyin = note.fields["Pinyin"].strip().replace(" ", "")
    return pinyin.split(SOUND_TAG)[0].strip()


def test_pinyin_duplicate(note: AnkiNote, deck: AnkiDeck):
    if note.fields["MitPinyin"] != "":
        # Find all notes with the same pinyin
        # Can be disabled by adding a tag with the hanzi to disambiguate
        matches = list(
            filter(
                lambda n: n.fields["MitPinyin"] != ""
                and extract_pinyin(n) == extract_pinyin(note),
                deck.notes,
            )
        )

        assert len(matches) == 1, (
            f"Duplicate note with same pinyin: {extract_pinyin(note)} (Hanzi: {note.fields['Hanzi']})\n"
            f"Duplicating hanzi: {', '.join(n.fields['Hanzi'] for n in matches)}\n"
            f"Duplicating pinyin: {', '.join(extract_pinyin(n) for n in matches)}\n"
            f"Duplicating DE: {', '.join(n.fields['Deutsch'] for n in matches)}"
        )

        # Check that all notes with pinyin and with the disambiguation tag removed still do not match us
        # Note that we check against the own pinyin with the disambiguation tag
        matches = list(
            filter(
                lambda n: n.fields["MitPinyin"] != ""
                and extract_pinyin(n).split(DISAMBIGUATE_TAG)[0].strip()
                == extract_pinyin(note),
                deck.notes,
            )
        )

        assert len(matches) <= 1, (
            f"Duplicate note with same pinyin and no disambiguation tag: {extract_pinyin(note)} (Hanzi: {note.fields['Hanzi']})\n"
            f"Duplicating hanzi: {', '.join(n.fields['Hanzi'] for n in matches)}\n"
            f"Duplicating pinyin: {', '.join(extract_pinyin(n) for n in matches)}\n"
            f"Duplicating DE: {', '.join(n.fields['Deutsch'] for n in matches)}"
        )


def _check_match(target: str, heteronyms: List[List[str]], prefix="") -> bool:
    our_syllable = heteronyms[0]

    next_syllables = heteronyms[1:]
    for candidate in our_syllable:
        if prefix + candidate == target:
            return True
        elif len(next_syllables) == 0:
            return False
        elif _check_match(target, next_syllables, prefix + candidate):
            return True

    return False


@pytest.mark.skip
def test_pinyin_hanzi_match(note: AnkiNote, deck: AnkiDeck):
    hanzi = note.fields["Hanzi"].split("[")[0].split(DISAMBIGUATE_TAG)[0].strip()
    pinyin = note.fields["Pinyin"].split("[")[0].split(DISAMBIGUATE_TAG)[0].strip()
    if "/" in hanzi:
        words_hanzi = hanzi.split("/")
        words_pinyin = pinyin.split("/")
        assert len(words_hanzi) == len(words_pinyin)
    else:
        words_hanzi = [hanzi]
        words_pinyin = [pinyin]

    for hanzi, pinyin in zip(words_hanzi, words_pinyin):
        BLACKLIST = " .!?-\n"
        hanzi = "".join(list(filter(lambda c: ord(c) >= 0x2E80, hanzi.strip())))
        pinyin = "".join(
            list(filter(lambda c: c not in BLACKLIST, pinyin.strip()))
        ).lower()

        conv_pinyin = pypinyin.pinyin(hanzi, heteronym=True)

        # Check if we can build the pinyin using at least one valid heteronym combination
        assert _check_match(
            pinyin, conv_pinyin
        ), f"Hanzi {hanzi} does not match pinyin {pinyin}. Possible pinyin: {conv_pinyin}"
