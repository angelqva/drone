from rest_framework import serializers
from drone.models import *
from django.core.exceptions import ValidationError
from typing import *


class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'


class MedicationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Medication
        fields = '__all__'


class EntityCreateSerializer(serializers.ModelSerializer):
    medications = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Medication.objects.all(
    ), many=True, help_text='List of Primary keys of LOTE [1,2,3]')
    drones = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Drone.objects.all(
    ), many=True, help_text='List of Primary keys of DRONE [1,2,3]')

    class Meta:
        model = Entity
        fields = '__all__'

    def create(self, validated_data):
        max_weigth = 0
        for drone in validated_data['drones']:
            drone: Drone = drone
            max_weigth += drone.weight
        for medication in validated_data['medications']:
            medication: Medication = medication
            if medication.weight > max_weigth:
                detail = "Medication:"+medication.name + \
                    " entity can't Delivery please add more drones to support that weight"
                raise serializers.ValidationError(detail=detail)
        return super().create(validated_data)


class EntityReadSerializer(serializers.ModelSerializer):
    medications = MedicationSerializer(many=True)
    drones = DroneSerializer(many=True)

    class Meta:
        model = Entity
        fields = '__all__'
        depth = 1


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ShippingReadSerializer(serializers.ModelSerializer):
    drones = DroneSerializer(many=True)
    medications = MedicationSerializer(many=True)

    class Meta:
        model = Shipping
        fields = '__all__'
        depth = 1


class DeliverySerializer(serializers.ModelSerializer):
    entity = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Entity.objects.all(
    ), help_text='Primary key of Entity')
    customer = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Customer.objects.all(
    ), help_text='Primary key of Entity')
    medications = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Medication.objects.all(
    ), many=True, help_text='List of Primary keys of Medication [1,2,3]')

    class Meta:
        model = Delivery
        fields = ('entity', 'customer', 'medications')
        depth = 1

    def create(self, validated_data):
        medications_delivery: List[Medication] = validated_data['medications']
        entity: Entity = validated_data['entity']
        medications_entity: List[Medication] = list(entity.medications.all())
        medications_cant_dispatch: List[str] = []
        for medication in medications_delivery:
            medication: Medication = medication
            if medication not in medications_entity:
                medications_cant_dispatch.append(medication.name)
        if len(medications_cant_dispatch) > 0:
            detail = "Entity no have this medication(" + \
                ', '.join(medications_cant_dispatch)+") to dispatch"
            raise serializers.ValidationError(detail=detail)
        else:
            medications_removed: List[Medication] = []
            try:
                for med in medications_delivery:
                    entity.medications.remove(med)
                    medications_removed.append(med)
            except:
                detail = "Cant delivery this medications"
                entity.medications.add(*medications_removed)
                raise serializers.ValidationError(detail=detail)
        return super().create(validated_data)


class DeliveryReadSerializer(serializers.ModelSerializer):
    entity = EntityReadSerializer()
    customer = CustomerSerializer()
    medications = MedicationSerializer(many=True)
    shippings = ShippingReadSerializer(many=True)

    class Meta:
        model = Delivery
        fields = '__all__'
        depth = 1
