import random
from celery import shared_task
from drone.utils import *
from drone.serializers import *
from rest_framework.response import Response


@shared_task(name="processing_entity_delivery")
def processing_entity_delivery():
    entity = Entity.objects.all().first()
    if entity is not None:
        query_delivery = Delivery.objects.filter(
            entity=entity, end_date=None).order_by('start_date')
        if query_delivery.count() > 0:
            delivery: Delivery = query_delivery.first()
            z1 = entity.zip_code
            z2 = delivery.customer.zip_code
            distance = get_distance(z1, z2)
            medications_to_processed: List[Medication] = list(
                delivery.medications.all())
            shippings = list(delivery.shippings.filter(state='Loading'))
            #print('medications_to_processed ', medications_to_processed)
            for ship in shippings:
                meds = list(ship.medications.all())
                for m in meds:
                    medications_to_processed.remove(m)
            if len(medications_to_processed) > 0:
                inactives = get_entity_drones_can_dispatch(entity, distance)
                if inactives is not None:
                    make_ship_drone(inactives, medications_to_processed,
                                    delivery, distance)
            else:
                if delivery.state == 'Processing':
                    delivery.state = 'Processed'
                    delivery.save()
                else:
                    #print('Delivery', delivery.shippings.all())
                    shipping = delivery.shippings.filter(
                        state='Returning',
                        end_date__gt=timezone.now()).order_by('end_date').last()
                    if shipping is not None:
                        # print(shipping)
                        delivery.state = 'Processed'
                        delivery.end_date = shipping.end_date
                        delivery.save()
                    else:
                        delivery.state = 'Finish'
                        delivery.save()
                # print(delivery.state)
            serializer = DeliveryReadSerializer(delivery)
            return serializer.data
        return {"detail": "Nothing to processing"}
    return {"detail": "No have entity"}


@shared_task(name="change_state")
def change_states_drone_delivery_entity():
    entity: Entity = Entity.objects.all().first()
    if entity is not None:
        drones: List[Drone] = list(entity.drones.all())
        deliverys: List[Delivery] = list(
            Delivery.objects.filter(entity=entity))
        for drone in drones:
            change_drone_state(drone)
        for delivery in deliverys:
            change_delivery_state(delivery)
        serializer_drones = DroneSerializer(entity.drones, many=True)
        serializer_deliverys = DeliveryReadSerializer(
            Delivery.objects.filter(entity=entity), many=True)
        return {"drones": serializer_drones.data, "deliverys": serializer_deliverys.data}
    return {"detail": "No have entity"}


@shared_task(name="update_battery_entity")
def update_battery_entity():
    time_now = timezone.now()
    time_prev = time_now - timedelta(seconds=10)
    print('n:', time_now, 'p:', time_prev)
    entity = Entity.objects.all().first()
    if entity is not None:
        drones: List[Drone] = list(entity.drones.all())
        for drone in drones:
            drone_set_charge(drone, time_prev, time_now)
        serializer_drones = DroneSerializer(entity.drones, many=True)
        return {"drones": serializer_drones.data}
    return {"detail": "No have entity"}
