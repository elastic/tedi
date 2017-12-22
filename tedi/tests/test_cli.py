import os
import shutil

from uuid import uuid4
from click.testing import CliRunner
from ..tedi import cli
from ..paths import render_path
from pathlib import Path


def invoke(command):
    return CliRunner().invoke(cli, command.split())


def output_of(command):
    return invoke(command).output


def test_render_command_prints_a_message():
    assert output_of('render') == 'Consider them rendered.\n'


def test_render_command_has_valid_help_text():
    assert 'Render' in output_of('render --help')


def test_clean_command_removes_files_from_the_render_directory():
    canary = Path(render_path, 'test-canary-%s' % uuid4())
    render_path.mkdir(exist_ok=True)
    canary.touch()
    invoke('clean')
    assert not canary.exists()
