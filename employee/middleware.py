#class CustomMiddleware:

#    def __init__(self, get_response):
#        self.get_response = get_response

#    def __call__(self, request):
#        response = self.get_response(request)
#        response["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
#        response["Pragma"] = "no-cache" # HTTP 1.0.
#        response["Expires"] = "0" # Proxies.
#        return response
