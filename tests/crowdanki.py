#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from pathlib import Path
from uuid import UUID

from tests.model import *


def load_deck_from_file(filename: Path) -> AnkiDeck:
    assert filename.exists() and filename.is_file()

    data = json.loads(filename.read_text())

    # Create basic deck info
    deck = AnkiDeck(
        name=data['name'],
        notes=[],
        media_files=data['media_files'],
        notemodels={},
        base_dir=filename.parent,
    )

    # Load all note models
    for nmodeldat in data['note_models']:
        ctype = CardType(UUID(nmodeldat['crowdanki_uuid']))
        nmodel = AnkiNoteModel(
            name=nmodeldat['name'],
            uuid=UUID(nmodeldat['crowdanki_uuid']),
            ctype=ctype,
            fields=[fdat["name"] for fdat in nmodeldat['flds']],
        )
        deck.notemodels[nmodel.uuid] = nmodel

    # Load notes themselves
    for ndat in data['notes']:
        assert UUID(ndat["note_model_uuid"]) in deck.notemodels, f"Unknown note model {ndat['note_model_uuid']} for card {ndat['guid']}"
        nmodel = deck.notemodels[UUID(ndat["note_model_uuid"])]

        note = AnkiNote(
            guid=ndat["guid"],
            cardtype_uuid=UUID(ndat["note_model_uuid"]),
            cardtype=nmodel.ctype,
            tags=ndat["tags"],
            fields={
                nmodel.fields[i]: v for i, v in enumerate(ndat["fields"])
            },
        )

        assert len(note.fields) == len(nmodel.fields)

        deck.notes.append(note)

    return deck

