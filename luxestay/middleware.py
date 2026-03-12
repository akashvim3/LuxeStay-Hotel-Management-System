from django.utils import translation
from django.conf import settings

class PreferenceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Handle Language
        language = request.session.get('language')
        if request.user.is_authenticated:
            language = request.user.preferred_language
        
        if language:
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()

        # 2. Handle Currency
        # Currency logic usually involves a context processor for display
        # but we can set it in session here if not present
        if 'currency' not in request.session:
            if request.user.is_authenticated:
                request.session['currency'] = request.user.preferred_currency
            else:
                request.session['currency'] = 'INR'

        response = self.get_response(request)
        return response
