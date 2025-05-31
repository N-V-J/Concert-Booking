# middleware.py
from django.utils.deprecation import MiddlewareMixin

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # HTTP 1.1.
        response['Pragma'] = 'no-cache'  # HTTP 1.0.
        response['Expires'] = '0'  # Proxies.
        return response