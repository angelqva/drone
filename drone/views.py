from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from api.views import NestedSerializerMixin
from drone.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action


class DroneView(viewsets.ModelViewSet):
    serializer_class = DroneSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Drone.objects.all()

    @action(detail=True, methods=["get"])
    def check_cargo(self, request, **kwargs):
        drone: Drone = self.get_object()
        time_now = timezone.now()
        ship: Shipping = drone.shipping_set.filter(
            end_date__gte=time_now, start_date__lte=time_now).first()
        result = {
            "drone": (DroneSerializer(drone)).data,
            "medications": False,
            "helping to charge": False
        }
        if ship is not None:
            if ship.drones.count() > 1:
                result["drones"] = (DroneSerializer(
                    ship.drones.all(), many=True)).data
                result["medications"] = (MedicationSerializer(
                    ship.medications.all(), many=True)).data
                result["helping to charge"] = True
            else:
                result["medications"] = (MedicationSerializer(
                    ship.medications.all(), many=True)).data
                result["helping to charge"] = False

        return Response(result, status=status.HTTP_200_OK)


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
