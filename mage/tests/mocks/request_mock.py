import json
from .spells_mock import get_spell_index_mock, get_spells_mock, get_spells_for_batch_mock


class SpellsBatchMock:
    @staticmethod
    def json():
        return json.loads(get_spells_for_batch_mock())


class SpellIndexMock:
    @staticmethod
    def json():
        return json.loads(get_spell_index_mock())


class GetSpellsMock:
    @staticmethod
    def json():
        return json.loads(get_spells_mock())


def mock_get_spell_index(*args, **kwargs):
    return SpellIndexMock()


def mock_get_spells(*args, **kwargs):
    return GetSpellsMock()


def mock_get_spells_batch(*args, **kwargs):
    return SpellsBatchMock()
