from .utils import create_spell_response
import requests
import tests.mocks.request_mock as request_mock
import mage.spells.transform.batch as transform_batch
import mage.spells.transform.base as base
import mage.spells.transform.description as description
import mage.spells.transform.components as components
import mage.spells.transform.range as range
import mage.spells.transform.damage as damage


def test_transformer(monkeypatch):
    monkeypatch.setattr(requests, "get", request_mock.mock_get_spell_index)

    spells = create_spell_response()
    batches = transform_batch.turn_into_batches(spells)

    solved = []
    for batch in batches:
        new_batch = base.Transformer(batch=batch['spells']) \
            .apply(description.transform_description) \
            .apply(components.transform_components) \
            .apply(range.transform_range) \
            .apply(damage.transform_damage)
        solved += new_batch.batch

    should_description_be_transformed(solved[0])
    should_range_be_transformed(solved[0])
    should_components_be_transformed(solved[0])
    should_damage_be_transformed(solved[0])


def should_description_be_transformed(batch):
    assert batch['description'] == "A simple description\nMore description"
    assert batch['higher_level_description'] == "Higher level description\nMore description"


def should_range_be_transformed(batch):
    assert batch['squares'] == 18


def should_components_be_transformed(batch):
    assert batch['components'] == "V, S, M"


def should_damage_be_transformed(batch):
    assert batch['damage'] == '4d4 of Acid damage'
    assert batch['total_damage_scale'] == [
        16, 20, 24, 28, 32, 36, 40, 44
    ]
