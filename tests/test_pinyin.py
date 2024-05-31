#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.model import AnkiDeck, AnkiNote


def extract_pinyin(note: AnkiNote) -> str:
    pinyin = note.fields["Pinyin"].strip().replace(" ", "")
    return pinyin.split("[sound:hypertts-")[0]


def test_pinyin_duplicate(note: AnkiNote, deck: AnkiDeck):
    if note.fields["MitPinyin"] != "":
        matches = list(
            filter(
                lambda n: n.fields["MitPinyin"] != ""
                and extract_pinyin(n) == extract_pinyin(note),
                deck.notes,
            )
        )

        assert len(matches) == 1, (
            f"Duplicate note with same pinyin: {extract_pinyin(note)} (Hanzi: {note.fields['Hanzi']})\n"
            f"Duplicating hanzi: {', '.join(n.fields['Hanzi'] for n in matches)}"
        )
