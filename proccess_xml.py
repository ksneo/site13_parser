import xml.etree.ElementTree as ET

ROOT_FOLDER = '00000000-0000-0000-0000-000000000000'

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


def get_offer(el, product_id, tree):
    offer = {}
    offer["product_id"] = product_id
    product_ref = get_text(tree.find("./Номенклатура"))
    product_el = tree.find(f".//CatalogObject.Номенклатура[Ref={product_ref}]")
    offer["article"] = get_text(product_el.find("./Артикул"), '')
    return offer


def read_product(el, tree):
    product = {}
    product["name"] = get_descr(el)
    product["product_id"] = get_text(el.find("./КодТовараНаСайте"))
    offer_elems = el.findall("./ТорговыеПредложения/Row")
    product["offers"] = [get_offer(offer_elem, product["product_id"], tree) for offer_elem in offer_elems]
    return product


def read_tree(el, tree):
    parent_id = el.find("./Ref")
    if parent_id and is_folder(el):
        find_path = f".//CatalogObject.ТоварыНаСайте13[Parent='{parent_id}']"
        children = tree.findall(find_path)
        if len(children) == 0:
            return {get_descr(el): {}}
        for child in children:
            return {get_descr(el): read_tree(child, tree)}
    else:
        return read_product(el, tree)


def proccess_xml(file):
    result = {'sites': {}}
    xmlTree = ET.fromstring(file.read())
    root_xpath = f".//CatalogObject.ТоварыНаСайте13[Parent='{ROOT_FOLDER}']"
    root_elements = xmlTree.findall(root_xpath)

    for el in root_elements:
        result["sites"][get_descr(el)] = read_tree(el, xmlTree)
    return result