from pathlib import Path
from pytest import fixture
from ..factset import Factset
from ..jinja_renderer import JinjaRenderer


@fixture
def renderer():
    facts = Factset(color='yellow')
    return JinjaRenderer(facts)


@fixture
def template():
    return Path('tedi/tests/fixtures/template/simple.j2')


def test_facts_is_a_factset(renderer):
    assert isinstance(renderer.facts, Factset)


def test_render_expands_facts_in_the_template(renderer, template):
    rendered = renderer.render(template)
    assert rendered == 'The canary is a yellow bird.'
