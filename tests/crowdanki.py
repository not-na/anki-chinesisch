#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from pathlib import Path
from typing import List
from uuid import UUID

from tests.model import *


def load_deck_from_file(filename: Path) -> AnkiDeck:
    return load_decks_from_file(filename)[0]


def load_decks_from_file(filename: Path) -> List[AnkiDeck]:
    assert filename.exists() and filename.is_file()

    data = json.loads(filename.read_text())

    return load_decks(data, filename)


def load_decks(
    data: dict, fname: Path, name_prefix="", note_models=None
) -> List[AnkiDeck]:
    decks = []

    # Create basic deck info
    deck = AnkiDeck(
        name=name_prefix + data["name"],
        notes=[],
        media_files=data["media_files"],
        notemodels={},
        base_dir=fname.parent,
    )

    # Load all note models
    if note_models is not None:
        deck.notemodels = note_models
    else:
        for nmodeldat in data["note_models"]:
            ctype = CardType(UUID(nmodeldat["crowdanki_uuid"]))
            nmodel = AnkiNoteModel(
                name=nmodeldat["name"],
                uuid=UUID(nmodeldat["crowdanki_uuid"]),
                ctype=ctype,
                fields=[fdat["name"] for fdat in nmodeldat["flds"]],
            )
            deck.notemodels[nmodel.uuid] = nmodel

    # Load notes themselves
    for ndat in data["notes"]:
        assert (
            UUID(ndat["note_model_uuid"]) in deck.notemodels
        ), f"Unknown note model {ndat['note_model_uuid']} for card {ndat['guid']}"
        nmodel = deck.notemodels[UUID(ndat["note_model_uuid"])]

        note = AnkiNote(
            guid=ndat["guid"],
            cardtype_uuid=UUID(ndat["note_model_uuid"]),
            cardtype=nmodel.ctype,
            tags=ndat["tags"],
            fields={nmodel.fields[i]: v for i, v in enumerate(ndat["fields"])},
            deck=deck,
        )

        assert len(note.fields) == len(nmodel.fields)

        deck.notes.append(note)

    decks.append(deck)

    for child in data["children"]:
        decks.extend(
            load_decks(child, fname, data["name"] + "::", note_models=deck.notemodels)
        )

    return decks
