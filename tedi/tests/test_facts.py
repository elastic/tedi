from ..facts import Facts


def test_set_method_creates_new_facts():
    facts = Facts()
    canary = 'princely_camel'
    assert canary not in facts.get_all()
    facts.set(canary, True)
    assert canary in facts.get_all()


def test_elastic_version_is_present():
    assert 'elastic_version' in Facts().get_all()
