import datetime
from django.conf import settings
from django_jwt_utils import user_to_dictionary, user_dictionary_to_jwt

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response = self.process_response(request, response)
        return response

    def process_response(self, request, response):
        if not request.COOKIES.get('authentication_token', None):
            if request.user.is_authenticated:
                ud = user_to_dictionary(request.user)
                jwt = user_dictionary_to_jwt(ud, settings.JWT_KEY)
            
                max_age = 365 * 24 * 60 * 60  # 10 years
                expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
                response.set_cookie('authentication_token', jwt, expires=expires)

        return response
