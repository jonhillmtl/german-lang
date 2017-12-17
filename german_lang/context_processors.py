from utils import url_manifest

def url_manifest_processor(request):
    return {
        'urls' : url_manifest()
    }
