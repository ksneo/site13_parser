import pytest
from pytest_mock import mocker
import xml.etree.ElementTree as ET
from ..proccess_xml import proccess_xml, is_folder, get_descr
from .fixtures.data_fixtures import category, root_folders

class TestProccessXml:
    def test_call_function_without_exceptions(self, mocker):
        mocker.patch("builtins.open", mocker.mock_open(read_data="<root></root>"))
        with open("data.xml") as file:
            proccess_xml(file)
        assert True

    def test_real_file_open(self):
        with open(".\\data\\data.xml", mode="r", encoding="utf-8") as file:
            result = proccess_xml(file)
        assert '' == result

    def test_isfolder(self, category):
        el = ET.fromstring(category)
        assert is_folder(el) == True

    def test_proccess_xml_with_root(self, mocker, root_folders):
        mocker.patch("builtins.open", mocker.mock_open(read_data=root_folders))
        with open("data.xml") as file:
            result = proccess_xml(file)
        assert result == ''

    def test_get_descr(self):
        xml_str = "<root><Description>test</Description></root>"
        el = ET.fromstring(xml_str)
        assert get_descr(el) == 'test'