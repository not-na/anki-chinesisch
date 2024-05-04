from pathlib import Path

import pytest

from tests.crowdanki import load_deck_from_file


DECK_PATH = Path(__file__).parent.parent / 'decks' / "Chinesisch" / "deck.json"

_deck = load_deck_from_file(DECK_PATH)


@pytest.fixture(scope='session')
def deck():
    return _deck


def pytest_generate_tests(metafunc):
    if "note" in metafunc.fixturenames:
        metafunc.parametrize("note", _deck.notes)
