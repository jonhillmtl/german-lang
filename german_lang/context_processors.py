from utils import url_manifest
import json


def url_manifest_processor(request):
    return {
        'urls' : url_manifest()
    }

def menu_item_processor(request):
    with open("./apps/config/menu_items.json") as f:
        menu_items = json.loads(f.read())
        return {
            'menu_items' : menu_items
        }
