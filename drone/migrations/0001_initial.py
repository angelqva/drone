# Generated by Django 3.2.9 on 2022-05-28 03:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import drone.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='Date Start Delivery', null=True)),
                ('end_date', models.DateTimeField(blank=True, help_text='Date End Delivery', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(help_text='Serial Number', max_length=100, unique=True)),
                ('model', models.CharField(choices=[('Lightweight', 'Lightweight'), ('Middleweight', 'Middleweight'), ('Cruiserweight', 'Cruiserweight'), ('Heavyweight', 'Heavyweight')], default='Lightweight', help_text="Dron Model Choices default='Lightweight'", max_length=13)),
                ('weight', models.IntegerField(help_text='Weight max value 500', validators=[django.core.validators.MaxValueValidator(500)])),
                ('battery', models.FloatField(default=100, help_text='Dron Battery percentage 0-100', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('state', models.CharField(choices=[('Idle', 'Idle'), ('Loading', 'Loading'), ('Delivering', 'Delivering'), ('Returning', 'Returning')], default='Idle', help_text="Dron State Choices default='Idle'", max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Only allowed letters, numbers, ‘-‘, ‘_’', max_length=255, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9_-]*$', 'Only allowed letters, numbers, ‘-‘, ‘_’')])),
                ('weight', models.IntegerField(help_text='More than 1gr', validators=[django.core.validators.MinValueValidator(1)])),
                ('code', models.CharField(help_text='Only allowed upper case letters, underscore and numbers', max_length=255, unique=True, validators=[django.core.validators.RegexValidator('^[A-Z0-9_]*$', 'Only allowed upper case letters, underscore and numbers')])),
                ('image', models.ImageField(help_text='Image of Medication', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('Loading', 'Loading'), ('Delivering', 'Delivering'), ('Returning', 'Returning')], default='Lightweight', help_text='Drones state', max_length=13)),
                ('start_date', models.DateTimeField(help_text='Date Start Shipping')),
                ('end_date', models.DateTimeField(help_text='Date End Shipping')),
                ('drones', models.ForeignKey(blank=True, help_text='one to many Drone', null=True, on_delete=django.db.models.deletion.CASCADE, to='drone.drone')),
                ('medications', models.ForeignKey(blank=True, help_text='one to many Medications', null=True, on_delete=django.db.models.deletion.CASCADE, to='drone.medication')),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Entity Name', max_length=255)),
                ('zip_code', models.CharField(help_text='Only zip codes of US', max_length=5, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Only allowed digits'), drone.validators.zipusa])),
                ('deliverys', models.ForeignKey(blank=True, help_text='one to many Medications', null=True, on_delete=django.db.models.deletion.CASCADE, to='drone.delivery')),
                ('drones', models.ForeignKey(blank=True, help_text='one to many Medications', null=True, on_delete=django.db.models.deletion.CASCADE, to='drone.drone')),
                ('medications', models.ForeignKey(blank=True, help_text='one to many Medications', null=True, on_delete=django.db.models.deletion.CASCADE, to='drone.medication')),
            ],
        ),
        migrations.AddField(
            model_name='delivery',
            name='medications',
            field=models.ForeignKey(blank=True, help_text='one to many Medications', null=True, on_delete=django.db.models.deletion.CASCADE, to='drone.medication'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='shippings',
            field=models.ForeignKey(blank=True, help_text='one to many Shipping', null=True, on_delete=django.db.models.deletion.CASCADE, to='drone.shipping'),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(help_text='Enter your fullname', max_length=255)),
                ('email', models.EmailField(help_text='Enter your email:example@domain.com', max_length=254, unique=True)),
                ('zip_code', models.CharField(help_text='Only zip codes of Miami Dade run zipcodes in api', max_length=5, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Only allowed 33186, 33015, 33157, 33033, 33142, 33125, 33177 check zipcode in validators'), drone.validators.zipusa])),
                ('deliverys', models.ForeignKey(blank=True, help_text='one to many', null=True, on_delete=django.db.models.deletion.CASCADE, to='drone.delivery')),
            ],
        ),
    ]