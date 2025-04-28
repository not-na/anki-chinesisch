#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = [
    "CardType",
    "AnkiNoteModel",
    "AnkiNote",
    "AnkiDeck",
]

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict
from uuid import UUID


class CardType(Enum):
    UNKNOWN = UUID("00000000-0000-0000-0000-000000000000")
    CH_Tripel = UUID("9878c924-bf79-11ee-82ca-cdae705cc9c0")


@dataclass
class AnkiNoteModel:
    uuid: UUID
    name: str
    ctype: CardType

    fields: List[str]


@dataclass
class AnkiNote:
    guid: str

    fields: Dict[str, str]

    cardtype_uuid: UUID
    cardtype: CardType
    tags: List[str]

    deck: "AnkiDeck"


@dataclass
class AnkiDeck:
    base_dir: Path

    name: str
    notes: List[AnkiNote]
    media_files: List[str]

    notemodels: Dict[UUID, AnkiNoteModel]
