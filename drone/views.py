from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from api.views import NestedSerializerMixin, NestedGenericMixin
from drone.serializers import *


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
    parser_classes = (MultiPartParser, )


class EntityView(NestedSerializerMixin):
    queryset = Entity.objects.all()
    serializer_class = EntityCreateSerializer
    read_serializer_class = EntityReadSerializer
    permission_classes = (IsAuthenticated,)


class DeliveryView(NestedGenericMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    read_serializer_class = DeliveryReadSerializer
    permission_classes = (IsAuthenticated,)


class ShippingView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Shipping.objects.all()
    serializer_class = ShippingReadSerializer
    permission_classes = (IsAuthenticated,)
