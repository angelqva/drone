from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from api.views import NestedSerializerMixin
from drone.serializers import *
from rest_framework.response import Response


class DroneView(viewsets.ModelViewSet):
    serializer_class = DroneSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Drone.objects.all()


class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()


class MedicationView(viewsets.ModelViewSet):
    serializer_class = MedicationSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Medication.objects.all()
    parser_classes = (MultiPartParser, FormParser, )

    def create(self, request, format=None, *args, **kwargs):
        return super().create(request, format=None, *args, **kwargs)


class EntityView(NestedSerializerMixin):
    queryset = Entity.objects.all()
    serializer_class = EntityCreateSerializer
    read_serializer_class = EntityReadSerializer
    permission_classes = (IsAuthenticated,)


class DeliveryView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = DeliveryReadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = DeliveryReadSerializer(queryset, many=True)
        return Response(serializer.data)


class ShippingView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Shipping.objects.all()
    serializer_class = ShippingReadSerializer
    permission_classes = (IsAuthenticated,)
