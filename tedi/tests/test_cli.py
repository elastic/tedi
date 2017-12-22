import os
import shutil

from pathlib import Path
from uuid import uuid4
from click.testing import CliRunner
from ..tedi import cli
from ..constants import render_dir


def invoke(command):
    return CliRunner().invoke(cli, command.split())


def output_of(command):
    return invoke(command).output


def test_render_command_prints_a_message():
    assert output_of('render') == 'Consider them rendered.\n'


def test_render_command_has_valid_help_text():
    assert 'Render' in output_of('render --help')


def test_clean_command_removes_files_from_the_render_directory():
    if os.path.isdir(render_dir):
        shutil.rmtree(render_dir)
        os.mkdir(render_dir)
    canary = os.path.join(render_dir, 'test-canary-%s' % uuid4())
    Path(canary).touch()
    invoke('clean')
    assert not os.path.exists(canary)
