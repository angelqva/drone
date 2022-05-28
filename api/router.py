from rest_framework.routers import DefaultRouter
from user.views import *
from drone.views import *

router = DefaultRouter()
router.register(prefix='users', basename='users', viewset=UserView)
router.register(prefix='logout-token', basename='logout', viewset=LogoutView)
router.register(prefix='drones', basename='drones', viewset=DroneView)
router.register(prefix='customers', basename='customers', viewset=CustomerView)
router.register(prefix='medications', basename='medications',
                viewset=MedicationView)
router.register(prefix='entitys', basename='entitys', viewset=EntityView)
router.register(prefix='deliverys', basename='deliverys', viewset=DeliveryView)
router.register(prefix='shippings', basename='shippings',
                viewset=ShippingView)


# GROUPS AND PERMISSIONS
# router.register(prefix='groups', basename='groups', viewset=GroupView)
# router.register(
#     prefix='permissions',
#     basename='permissions',
#     viewset=PermissionView
# )
