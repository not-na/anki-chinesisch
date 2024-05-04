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

