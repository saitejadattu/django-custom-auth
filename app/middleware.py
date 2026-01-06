class SimpleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        print("Middleware Initialized")

    def __call__(self, request):
        print(request.headers)
        print("Before View.............................................")

        response = self.get_response(request)

        print("After View...................................................")
        print(response._container)
        return response
