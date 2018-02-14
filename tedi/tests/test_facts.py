from ..facts import Facts


def test_fact_elastic_version():
    assert 'elastic_version' in Facts().get_all()
