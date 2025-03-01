from pathlib import Path

import pytest

from tests.crowdanki import load_decks_from_file

DECK_PATH = Path(__file__).parent.parent / "decks" / "Chinesisch" / "deck.json"

_decks = load_decks_from_file(DECK_PATH)

_notes = []
for deck in _decks:
    _notes.extend(deck.notes)


@pytest.fixture(scope="session")
def decks():
    return _decks


@pytest.fixture(scope="session")
def notes():
    return _notes


def pytest_generate_tests(metafunc):
    if "note" in metafunc.fixturenames:
        metafunc.parametrize("note", _notes)

    if "deck" in metafunc.fixturenames:
        metafunc.parametrize("deck", _decks)
