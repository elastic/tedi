from click.testing import CliRunner
from ..tedi import cli


def invoke(command):
    return CliRunner().invoke(cli, command.split())

def output_of(command):
    return invoke(command).output


def test_render_command_prints_a_message():
    assert output_of('render') == 'Consider them rendered.\n'


def test_render_command_has_valid_help_text():
    assert 'Render' in output_of('render --help')









