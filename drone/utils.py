from drone.stats import stats_dm
import json
from drone.models import *
from typing import List
from datetime import timedelta, datetime
import pytz
utc = pytz.UTC


def get_shippings(drone: Drone) -> List[Shipping] | None:
    ships: List[Shipping] = list(drone.shipping_set.filter(
        end_date__gt=utc.localize(datetime.now())))
    if len(ships) > 0:
        return ships
    return None


def calc_can_do_distance(drone: Drone, distance) -> bool:
    battery = drone.battery
    stats = stats_dm[drone.model]
    if battery >= 2*distance*stats['battery_loss']:
        return True
    return False


def get_entity_drones_can_dispatch(entity: Entity, distance) -> List[Drone] | None:
    drones: List[Drone] = list(entity.drones.all())
    inactive: List[Drone] = []
    for drone in drones:
        if get_shippings(drone) is None:
            if drone.battery > 25 and calc_can_do_distance(drone, distance):
                inactive.append(drone)
    if len(inactive):
        return inactive
    return None


def get_entity(pk) -> Entity | None:
    entity = Entity.objects.get(pk=pk)
    return entity


def calc_duration_task(drone: Drone, distance: float):
    stats = stats_dm[drone.model]
    if distance > 0:
        seconds = distance*1000/stats["speed"]
        return seconds
    return 0


def create_shipping(
        drones: List[Drone],
        medications: List[Medication],
        distance: float,
        delivery: Delivery):
    print("====CREATE SHIPPING====")
    print("Drones -> ", drones)
    print("medications -> ", medications)
    print("distance -> ", distance)
    print("delivery -> ", delivery)
    print("==END CREATE SHIPPING==")
    duration_task = calc_duration_task(drones[0], distance)
    start_loading = utc.localize(datetime.now())
    end_loading = start_loading+timedelta(seconds=60)
    start_delivering = end_loading
    end_delivering = start_delivering+timedelta(seconds=duration_task)
    start_returning = end_delivering
    end_returning = end_delivering+timedelta(seconds=duration_task)
    help_mode = len(drones) > 1

    t1 = Shipping.objects.create(
        state="Loading",
        help_mode=help_mode,
        start_date=start_loading,
        end_date=end_loading
    )
    t1.drones.add(*drones)
    t1.medications.add(*medications)
    t1.save()
    t2 = Shipping.objects.create(
        state="Delivering",
        help_mode=help_mode,
        start_date=start_delivering,
        end_date=end_delivering
    )
    t2.drones.add(*drones)
    t2.medications.add(*medications)
    t2.save()
    t3 = Shipping.objects.create(
        state="Returning",
        help_mode=help_mode,
        start_date=start_returning,
        end_date=end_returning
    )
    t3.drones.add(*drones)
    t3.save()
    print(t1, t2, t3)
    delivery.shippings.add(t1)
    delivery.shippings.add(t2)
    delivery.shippings.add(t3)
    print(delivery.shippings.all())


def make_ship_drone(drones: List[Drone], medications: List[Medication],
                    delivery: Delivery, distance: float):
    medications_heavy: List[Medication] = []
    medications_light: List[Medication] = []
    while len(medications) > 0:
        medication: Medication = medications.pop()
        if medication.weight > 500:
            medications_heavy.append(medication)
        else:
            medications_light.append(medication)

    medications_light.sort(key=lambda x: x.weight, reverse=True)
    medications_heavy.sort(key=lambda x: x.weight, reverse=True)
    print('medications_light -> ', medications_light)
    print('medications_heavy -> ', medications_heavy)
    if len(drones) > 0:
        capacidad = 0
        if len(medications_heavy) > 0:
            for drone in drones:
                capacidad += drone.weight
            print('capacidad - >', capacidad)
            medication_heavy_delete: List[Medication] = []
            for i in range(len(medications_heavy)):
                medication_h = medications_heavy[i]
                medications_to_drone = []
                print('medication_h - >', medication_h)
                print('medications_to_drone - >', medication_h)
                if capacidad == medication_h.weight:
                    medications_to_drone.append(medication_h)
                    medication_heavy_delete.append(medication_h)
                    create_shipping(
                        drones, medications_to_drone, distance, delivery)
                    drones = []
                    i = len(medications_heavy)
                elif capacidad > medication_h.weight:
                    medications_to_drone.append(medication_h)
                    medication_heavy_delete.append(medication_h)
                    drones.sort(key=lambda x: (x.weight))
                    rellena_capacidad = 0
                    list_drones: List[Drone] = []
                    while rellena_capacidad < medication_h.weight:
                        print('rellena_capacidad - >', rellena_capacidad)
                        print('list_drones - >', list_drones)
                        drone = drones.pop()
                        list_drones.append(drone)
                        rellena_capacidad += drone.weight
                    sobrante = rellena_capacidad - medication_h.weight
                    print('sobrante - >', sobrante)
                    medication_light_delete: List[Medication] = []
                    for i in range(len(medications_light)):
                        print('medications_to_drone - >', medications_to_drone)
                        weight = medications_light[i].weight
                        if sobrante > weight:
                            sobrante -= weight
                            medications_to_drone.append(medications_light[i])
                            medication_light_delete.append(
                                medications_light[i])
                    if len(medication_light_delete) > 0:
                        for med in medication_light_delete:
                            medications_light.remove(med)
                    create_shipping(
                        list_drones, medications_to_drone, distance, delivery)
                else:
                    i = len(medications_heavy)
            if len(medication_heavy_delete) > 0:
                for med in medication_heavy_delete:
                    medications_heavy.remove(med)
            print('medications_light -> ', medications_light)
            print('medications_heavy -> ', medications_heavy)
            print('drones -> ', drones)
            if len(drones) > 0 and len(medications_light) > 0:
                print('Continue with medications')
                while len(drones) > 0 and len(medications_light) > 0:
                    drone = drones.pop()
                    capacity = drone.weight
                    medications_to_drone: List[Medication] = []
                    medication_light_delete = []
                    for i in range(len(medications_light)):
                        weight = medications_light[i].weight
                        print('capacity -> ', capacity)
                        print('weight -> ', weight)
                        if capacity > weight:
                            capacity -= weight
                            medications_to_drone.append(medications_light[i])
                            medication_light_delete.append(
                                medications_light[i])
                    if len(medication_light_delete) > 0:
                        for med in medication_light_delete:
                            medications_light.remove(med)
                        print("Send Create Tasks")
                        create_shipping(
                            [drone], medications_to_drone, distance, delivery)

        else:
            while len(drones) > 0 and len(medications_light) > 0:
                drone = drones.pop()
                capacity = drone.weight
                medications_to_drone: List[Medication] = []
                for i in range(len(medications_light)):
                    weight = medications_light[i].weight
                    if capacity > weight:
                        capacity -= weight
                        medications_to_drone.append(medications_light[i])
                if len(medications_to_drone) > 0:
                    for med in medications_to_drone:
                        medications_light.remove(med)

                    print("Send Create Tasks")
                    create_shipping(
                        [drone], medications_to_drone, distance, delivery)


def get_distance(z1, z2):
    data_json_file = open('zip_distance.json')
    data = json.load(data_json_file)
    return data[str(z1)+","+str(z2)]


def processing_entity_delivery(entity: Entity):
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
        print('medications_to_processed ', medications_to_processed)
        for ship in shippings:
            meds = list(ship.medications.all())
            for m in meds:
                medications_to_processed.remove(m)
        if len(medications_to_processed) > 0:
            inactives = get_entity_drones_can_dispatch(entity, distance)
            make_ship_drone(inactives, medications_to_processed,
                            delivery, distance)
        else:
            if delivery.state == 'Processing':
                delivery.state = 'Processed'
                delivery.save()
            else:
                print('Delivery', delivery.shippings.all())
                shipping = delivery.shippings.filter(
                    state='Returning', end_date__gt=utc.localize(datetime.now())).order_by('end_date').last()
                if shipping is not None:
                    print(shipping)
                    delivery.state = 'Processed'
                    delivery.end_date = shipping.end_date
                    delivery.save()
                else:
                    delivery.state = 'Complete'
                    delivery.save()
            print(delivery.state)
