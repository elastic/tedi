from unittest.mock import patch
from .. import process


def test_fail_exits():
    with patch('sys.exit') as exit:
        process.fail()
        assert exit.called
