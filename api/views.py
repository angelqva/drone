from rest_framework import viewsets


class NestedSerializerMixin(viewsets.ModelViewSet):
    read_serializer_class = None

    def get_serializer_class(self):
        if self.request.method.lower() == "get":
            return self.read_serializer_class
        return self.serializer_class
