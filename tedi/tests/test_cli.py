from uuid import uuid4
from click.testing import CliRunner
from ..cli import cli
from pathlib import Path

template_path = Path('tedi/tests/fixtures/templates')
render_path = Path('renders.test.tmp')


def invoke(command):
    return CliRunner().invoke(cli, command.split())


def invoke_clean():
    invoke('clean --render-path=%s' % render_path)


def invoke_render():
    invoke('render --template-path=%s --render-path=%s' % (template_path, render_path))


def output_of(command):
    return invoke(command).output


def assert_in_test_file(string, test_file='image01/Dockerfile'):
    invoke_render()
    assert string in Path(render_path, test_file).open().read()


def assert_command_does_cleaning(command):
    """Given a TEDI subcommand name, assert that it cleans up rendered files"""
    canary = Path(render_path, 'test-canary-%s' % uuid4())
    render_path.mkdir(exist_ok=True)
    canary.touch()
    invoke_clean()
    assert canary.exists() is False


def test_render_command_has_valid_help_text():
    assert 'Render' in output_of('render --help')


def test_clean_command_removes_files():
    assert_command_does_cleaning('clean')


def test_render_command_removes_files():
    assert_command_does_cleaning('render')


def test_render_expands_jinja_template_tags():
    assert_in_test_file('two_plus_two=4')


def test_render_expands_our_custom_facts():
    invoke_render()
    assert_in_test_file('Cats can be right-pawed or left-pawed.')
