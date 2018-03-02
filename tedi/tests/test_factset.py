from ..factset import Factset
from pytest import fixture, raises


@fixture
def facts():
    return Factset(sky_color='blue')


def test_can_test_membership(facts):
    assert 'sky_color' in facts


def test_elastic_version_is_present(facts):
    assert 'elastic_version' in facts


def test_can_override_elastic_version_in_constructor():
    facts = Factset(elastic_version='future')
    assert facts['elastic_version'] == 'future'


def test_can_set_facts_like_a_dictionary(facts):
    facts['key_canary'] = 'bird'
    assert facts['key_canary'] == 'bird'


def test_can_set_facts_via_contructor_keywords(facts):
    assert facts['sky_color'] == 'blue'


def test_can_delete_facts(facts):
    del(facts['sky_color'])
    assert 'sky_color' not in facts


def test_setting_a_fact_to_none_deletes_it(facts):
    facts['sky_color'] = None
    assert 'sky_color' not in facts


def test_setting_a_new_key_to_none_does_nothing(facts):
    facts['point'] = None
    assert 'point' not in facts


def test_setting_non_string_facts_is_an_error(facts):
    for value in (True, False, 5, object()):
        with raises(ValueError):
            facts['test'] = value


def test_using_non_string_keys_is_an_error(facts):
    for value in (True, False, 5, object()):
        with raises(ValueError):
            facts[value] = 'test'


def test_to_dict_returns_a_dictionary(facts):
    assert isinstance(facts.to_dict(), dict)
    assert 'sky_color' in facts.to_dict()


def test_update_updates_facts_from_a_dict(facts):
    facts.update({'sky_color': 'black'})
    assert facts['sky_color'] == 'black'


def test_update_updates_facts_from_keywords(facts):
    facts.update(sky_color='pink')
    assert facts['sky_color'] == 'pink'
