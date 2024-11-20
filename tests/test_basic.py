#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from tests.model import AnkiDeck, AnkiNote


def test_basic(deck: AnkiDeck):
    assert deck.name == "Chinesisch"
    assert len(deck.notes) != 0
    assert len(deck.notemodels) != 0


def test_pronunciation(deck: AnkiDeck, note: AnkiNote):
    match = re.match(r".*\[sound:(hypertts-[0-9a-f]{56}\.mp3)]", note.fields["Pinyin"])
    assert match is not None, f"Pronunciation not found in note {note}"
    audiofile = match.group(1)

    assert audiofile in deck.media_files
    assert (deck.base_dir / "media" / audiofile).exists()


def test_fields(deck: AnkiDeck, note: AnkiNote):
    # Fields not empty
    assert note.fields["Pinyin"].strip() != ""
    assert note.fields["Hanzi"].strip() != ""
    assert note.fields["Deutsch"].strip() != ""

    # No trailing/leading whitespace
    assert note.fields["Pinyin"] == note.fields["Pinyin"].strip()
    assert note.fields["Hanzi"] == note.fields["Hanzi"].strip()
    assert note.fields["Deutsch"] == note.fields["Deutsch"].strip()

    assert note.fields["MitHanzi"] == note.fields["MitHanzi"].strip()
    assert note.fields["MitPinyin"] == note.fields["MitPinyin"].strip()
    assert note.fields["MitDeutsch"] == note.fields["MitDeutsch"].strip()

    # Flag fields only one character
    assert len(note.fields["MitHanzi"]) in [0, 1]
    assert len(note.fields["MitPinyin"]) in [0, 1]
    assert len(note.fields["MitDeutsch"]) in [0, 1]

    # No leech tag in export
    assert "leech" not in note.tags, "Leech tag should be removed prior to exporting"
