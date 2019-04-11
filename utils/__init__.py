from django.core.urlresolvers import get_resolver
from typing import Dict


def url_manifest() -> Dict:
    return {k: "/{}".format(v[0][0][0]) for k, v in get_resolver(None).reverse_dict.items() if type(k) == str}
