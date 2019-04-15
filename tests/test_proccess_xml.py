import pytest
from pytest_mock import mocker
from ..proccess_xml import proccess_xml


class TestProccessXml:
    def test_call_function_without_exceptions(self, mocker):
        mocker.patch("builtins.open", mocker.mock_open(read_data="<root></root>"))
        with open("data.xml") as file:
            proccess_xml(file)
        assert True