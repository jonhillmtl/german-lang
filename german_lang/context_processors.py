from utils import url_manifest
import json
from typing import Dict


def url_manifest_processor(request: Dict) -> Dict:
    return {
        'urls' : url_manifest()
    }


def menu_item_processor(request: Dict) -> Dict:
    with open("./apps/config/menu_items.json") as f:
        menu_items = json.loads(f.read())
        return {
            'menu_items' : menu_items
        }
