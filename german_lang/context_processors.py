from django.conf import settings
from django_jwt_utils import user_to_dictionary, user_dictionary_to_jwt
from utils import url_manifest

def jwt_token_processor(request):
    if request.user.is_authenticated:
        ud = user_to_dictionary(request.user)
        jwt = user_dictionary_to_jwt(ud, settings.JWT_KEY)
        return {'jwt_token': jwt}
    return {}

def url_manifest_processor(request):
    return {
        'urls' : url_manifest()
    }
