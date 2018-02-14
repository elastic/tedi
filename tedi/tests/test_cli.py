import os

from uuid import uuid4
from click.testing import CliRunner
from ..cli import cli
from ..paths import make_render_path
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


def assert_in_test_file(string, test_file='Dockerfile'):
    invoke_render()
    assert string in Path(render_path, test_file).open().read()


def assert_command_does_cleaning(command):
    """Given a TEDI subcommand name, assert that it cleans up the rendered output"""
    canary = Path(render_path, 'test-canary-%s' % uuid4())
    render_path.mkdir(exist_ok=True)
    canary.touch()
    invoke_clean()
    assert not canary.exists()


def test_render_command_has_valid_help_text():
    assert 'Render' in output_of('render --help')


def test_clean_command_removes_files_from_the_render_directory():
    assert_command_does_cleaning('clean')


def test_render_command_cleans_extraneous_files():
    assert_command_does_cleaning('render')


def test_render_command_produces_one_output_file_per_input_file():
    invoke_render()

    # Collect a list of every file in the template directory.
    for root, subdirs, files in os.walk(str(template_path)):
        input_files = [Path(os.path.join(root, f)) for f in files]
        assert len(input_files) > 0

    # Collect a similar list of every file in the output (render) directory.
    for root, subdirs, files in os.walk(str(render_path)):
        output_files = [Path(os.path.join(root, f)) for f in files]

    # Now make sure that we have a one to one mapping.
    for input_file in input_files:
        assert make_render_path(input_file) in output_files


def test_render_expands_jinja_template_tags():
    assert_in_test_file('two_plus_two=4')


def test_render_expands_our_custom_facts():
    invoke_render()
    assert_in_test_file('Cats can be right-pawed or left-pawed.')
