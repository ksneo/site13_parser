import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger()

EMPTY_UUID = '00000000-0000-0000-0000-000000000000'
ROOT_FOLDER = EMPTY_UUID

def get_text(el, default=None):
    if not el is None:
        return el.text

    return default


def get_descr(el):
    return get_text(el.find("./Description"), '')


def is_folder(el):
    isfolder = get_text(el.find("./IsFolder"))
    if isfolder and isfolder == "true":
        return True

    return False

def get_volume(el, tree):
    result = ""
    result_name = ""
    try:
        volume_ref = get_text(el.find("./ЕдиницаХраненияОстатков"))
        volume_el = tree.find(f".//CatalogObject.ЕдиницыИзмерения[Ref='{volume_ref}']")
        result = get_text(volume_el.find("./Объем"),"")
        volume_name_ref = get_text(volume_el.find("./ЕдиницаПоКлассификатору"), "")
        volume_name_el = tree.find(f".//CatalogObject.КлассификаторЕдиницИзмерения[Ref='{volume_name_ref}']")
        result_name = get_text(volume_name_el.find("./Description"))
    except Exception as e:
        logger.error(f"Ошибка получения единицы измерения {e}")

    return (result, result_name)


def get_offer(el, product_id, tree):
    offer = {}
    offer["product_id"] = product_id
    product_ref = get_text(el.find("./Номенклатура"))
    product_el = tree.find(f".//CatalogObject.Номенклатура[Ref='{product_ref}']")
    product_colour = get_text(el.find("./ХарактеристикаНоменклатуры"), "")
    volume, volume_name = get_volume(product_el, tree)
    extension_ref = get_text(el.find("./ДополнительнаяНоменклатура"))
    extension_el = None

    if not extension_ref == EMPTY_UUID:
        extension_el = tree.find(f".//CatalogObject.Номенклатура[Ref='{extension_ref}']")

    offer["article"] = "" if not product_el else get_text(product_el.find("./Артикул"), "")
    offer["extension"] = "" if not extension_el else (get_text(product_el.find("./Code"), "")).strip()
    offer["colour"] = get_text(el.find("./ХарактеристикаДополнительнойНоменклатуры"), "")
    offer["colour"] = product_colour if not offer["colour"] else offer["colour"]
    offer["volume"] = volume
    offer["volume_name"] = volume_name
    return offer


def read_product(el, tree):
    product = {}
    product["type"] = "product"
    product["name"] = get_descr(el)
    product["product_id"] = get_text(el.find("./КодТовараНаСайте"))
    offer_elems = el.findall("./ТорговыеПредложения/Row")
    offers = []
    for offer_elem in offer_elems:
        offers.append(get_offer(offer_elem, product["product_id"], tree))
    product["offers"] = offers
    return product


def read_tree(el, tree):
    parent_id = get_text(el.find("./Ref"))
    if parent_id and is_folder(el):
        find_path = f".//CatalogObject.ТоварыНаСайте13[Parent='{parent_id}']"
        children = tree.findall(find_path)

        if len(children) == 0:
            return {"type": "folder", "name": get_descr(el), "children": []}

        children_elems = []
        for child in children:
            children_elems.append(read_tree(child, tree))
        return {"type": "folder", "name": get_descr(el), "children": children_elems}
    else:
        return read_product(el, tree)


def proccess_xml(file):
    result = {"sites": []}
    xmlTree = ET.fromstring(file.read())
    root_xpath = f".//CatalogObject.ТоварыНаСайте13[Parent='{ROOT_FOLDER}']"
    root_elements = xmlTree.findall(root_xpath)

    for el in root_elements:
        result["sites"].append(read_tree(el, xmlTree))
    return result