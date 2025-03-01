#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from pathlib import Path
from typing import List

from tests.model import AnkiDeck, AnkiNote


def get_audiofile_from_note(note: AnkiNote) -> str:
    match = re.match(r".*\[sound:(hypertts-[0-9a-f]{56}\.mp3)]", note.fields["Audio"])
    assert match is not None, f"Pronunciation not found in note {note}"
    audiofile = match.group(1)

    return audiofile


def test_basic(deck: AnkiDeck):
    assert deck.name.startswith("Chinesisch")
    assert " " not in deck.name
    assert len(deck.notes) != 0
    assert len(deck.notemodels) != 0


def test_pronunciation(note: AnkiNote):
    audiofile = get_audiofile_from_note(note)

    assert audiofile in note.deck.media_files
    assert (note.deck.base_dir / "media" / audiofile).exists()


def test_unneeded_audio(decks: List[AnkiDeck], notes: List[AnkiNote]):
    basedir = decks[0].base_dir / "media"
    all_media = set((basedir / f).absolute() for f in basedir.glob("*.mp3"))

    for deck in decks:
        assert deck.base_dir / "media" == basedir

    for note in notes:
        audiofile = get_audiofile_from_note(note)
        all_media.discard(
            (note.deck.base_dir / "media" / audiofile).absolute()
        )  # Don't care if audio is missing, may be used more than once

    assert (
        len(all_media) == 0
    ), f"{len(all_media)} unneeded audio files ({len(notes)} notes)"


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
