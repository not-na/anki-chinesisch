#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.model import AnkiDeck, AnkiNote


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
            f"Duplicating pinyin: {', '.join(extract_pinyin(n) for n in matches)}"
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
            f"Duplicating pinyin: {', '.join(extract_pinyin(n) for n in matches)}"
        )
