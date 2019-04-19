import pytest

@pytest.fixture()
def category():
    return """
        <CatalogObject.ТоварыНаСайте13>
			<Ref>3a8f9ee5-1db9-11e9-88ba-00155d003f0a</Ref>
			<IsFolder>true</IsFolder>
			<DeletionMark>false</DeletionMark>
			<Parent>3c8f6a2e-1db8-11e9-88ba-00155d003f0a</Parent>
			<Code>000000225</Code>
			<Description>Масла и воски серии Legno</Description>
			<ТипЦен>00000000-0000-0000-0000-000000000000</ТипЦен>
			<Склад>00000000-0000-0000-0000-000000000000</Склад>
			<ТорговыеПредложения/>
		</CatalogObject.ТоварыНаСайте13>
    """

def adler():
    return """
        <CatalogObject.ТоварыНаСайте13>
			<Ref>3c8f6a2e-1db8-11e9-88ba-00155d003f0a</Ref>
			<IsFolder>true</IsFolder>
			<DeletionMark>false</DeletionMark>
			<Parent>00000000-0000-0000-0000-000000000000</Parent>
			<Code>000000224</Code>
			<Description>adler</Description>
			<ТипЦен>33dbe622-1478-11da-99a0-505054503030</ТипЦен>
			<Склад>00000000-0000-0000-0000-000000000000</Склад>
			<ТорговыеПредложения/>
		</CatalogObject.ТоварыНаСайте13>

    """


@pytest.fixture()
def root_folders():
    start = """<?xml version="1.0" encoding="UTF-8"?>
        <V8Exch:_1CV8DtUD xmlns:V8Exch="http://www.1c.ru/V8/1CV8DtUD/" xmlns:v8="http://v8.1c.ru/data" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
	        <V8Exch:Data>"""
    end = """</V8Exch:Data>
        </V8Exch:_1CV8DtUD>"""
    return f"{start}{adler()}{end}"

