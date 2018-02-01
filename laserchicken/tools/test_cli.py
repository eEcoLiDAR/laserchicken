import pytest
from click.testing import CliRunner
from . import cli


@pytest.fixture
def runner():
    return CliRunner()


# def test_cli(runner):
#     result = runner.invoke(cli.main)
#     assert result.exit_code == 0
#     assert not result.exception
#     assert result.output.strip() == 'Hello.'
#
#
# def test_cli_with_option(runner):
#     result = runner.invoke(cli.main, ['--', './testdata/AHN2.las'])
#     assert not result.exception
#     assert result.exit_code == 0
#     assert result.output.strip() == ''
#
#
# def test_cli_with_arg(runner):
#     result = runner.invoke(cli.main, ['Chicken'])
#     assert result.exit_code == 0
#     assert not result.exception
#     assert result.output.strip() == ''
