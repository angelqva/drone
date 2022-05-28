from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from drone.validators import zipusa
from datetime import timedelta, datetime
import pytz
utc = pytz.UTC


class Drone(models.Model):
    DRONE_MODEL_CHOICES = (
        ('Lightweight', 'Lightweight'),
        ('Middleweight', 'Middleweight'),
        ('Cruiserweight', 'Cruiserweight'),
        ('Heavyweight', 'Heavyweight')
    )
    DRONE_STATE_CHOICES = (
        ('Idle', 'Idle'),
        ('Loading', 'Loading'),
        ('Delivering', 'Delivering'),
        ('Returning', 'Returning')
    )
    serial_number = models.CharField(
        max_length=100,
        help_text="Serial Number",
        unique=True
    )
    model = models.CharField(
        max_length=13,
        choices=DRONE_MODEL_CHOICES,
        default='Lightweight',
        help_text="Dron Model Choices default='Lightweight'"
    )
    weight = models.IntegerField(
        validators=[MaxValueValidator(500)],
        help_text="Weight max value 500"
    )
    battery = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        default=100,
        help_text="Dron Battery percentage 0-100"
    )
    state = models.CharField(
        max_length=13,
        choices=DRONE_STATE_CHOICES,
        default='Idle',
        help_text="Dron State Choices default='Idle'"
    )

    def __str__(self) -> str:
        return "Drone->id({id})-w({w})-b({b})-s({st})".format(
            id=self.pk,
            w=self.weight,
            b=self.battery,
            st=self.state
        )


class Medication(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                r"^[a-zA-Z0-9_-]*$", "Only allowed letters, numbers, ‘-‘, ‘_’"
            )
        ],
        help_text="Only allowed letters, numbers, ‘-‘, ‘_’"
    )
    weight = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="More than 1gr"
    )
    code = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                r"^[A-Z0-9_]*$", "Only allowed upper case letters, underscore and numbers"
            )
        ],
        unique=True,
        help_text="Only allowed upper case letters, underscore and numbers"
    )
    image = models.ImageField(
        help_text="Image of Medication"
    )

    def __str__(self) -> str:
        return "Medication -> id({id})-w({w})".format(
            id=self.pk,
            w=self.weight
        )


class Customer(models.Model):
    fullname = models.CharField(
        max_length=255,
        help_text="Enter your fullname"
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        help_text="Enter your email:example@domain.com"
    )
    zip_code = models.CharField(
        max_length=5,
        validators=[
            RegexValidator(
                r"^[0-9]*$", "Only allowed digits and zips like 33186, 33015, " +
                "33157, 33033, 33142, 33125, 33177 check zipcode in validators"
            ),
            zipusa
        ],
        help_text="Only zip codes of Miami Dade run zipcodes in api 33186, 33015, " +
        "33157, 33033, 33142, 33125, 33177"
    )


class Entity(models.Model):
    name = models.CharField(
        max_length=255,
        help_text="Entity Name"
    )
    zip_code = models.CharField(
        max_length=5,
        validators=[
            RegexValidator(
                r"^[0-9]*$", "Only allowed digits"
            ),
            zipusa
        ],
        help_text="Only zip codes of US"
    )
    medications = models.ManyToManyField(Medication)
    drones = models.ManyToManyField(Drone)

    def __str__(self) -> str:
        return "id({id})-zipcode({z})".format(
            id=self.pk,
            z=self.zip_code
        )


class Shipping(models.Model):
    DRONE_STATE_CHOICES = (
        ('Loading', 'Loading'),
        ('Delivering', 'Delivering'),
        ('Returning', 'Returning')
    )
    medications = models.ManyToManyField(Medication)
    drones = models.ManyToManyField(Drone)
    state = models.CharField(
        max_length=13,
        choices=DRONE_STATE_CHOICES,
        default='Loading',
        help_text="Drones state"
    )
    help_mode = models.BooleanField(
        default=False,
        help_text="If load medication to heavy"
    )
    start_date = models.DateTimeField(
        help_text="Date Start Shipping"
    )
    end_date = models.DateTimeField(
        help_text="Date End Shipping"
    )


class Delivery(models.Model):
    DELIVERY_STATE_CHOICES = (
        ('Processing', 'Processing'),
        ('Processed', 'Processed'),
        ('Delivered', 'Delivered'),
        ('Complete', 'Complete')
    )
    entity = models.OneToOneField(
        Entity, on_delete=models.CASCADE, help_text="Entity to belong")
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, help_text="Customer to belong")
    medications = models.ManyToManyField(Medication)
    shippings = models.ManyToManyField(Shipping)
    state = models.CharField(
        max_length=13,
        choices=DELIVERY_STATE_CHOICES,
        default='Processing',
        help_text="Delivery State Choices default='Processing'"
    )
    start_date = models.DateTimeField(
        default=utc.localize(datetime.now()),
        help_text="Date Start Delivery",
        blank=True,
        null=True
    )
    end_date = models.DateTimeField(
        help_text="Date End Delivery",
        blank=True,
        null=True
    )
