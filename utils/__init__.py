from django.core.urlresolvers import get_resolver

def url_manifest():
    return {k: "/{}".format(v[0][0][0]) for k, v in get_resolver(None).reverse_dict.items() if type(k) == str}
