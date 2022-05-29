# DRONES APIREST

APIREST for solve Drones problem

## Installation

Clone this repository

```bash
git clone git@github.com:angelqva/drone.git
```

copy .env configuration on terminal

```bash
copy .env.sample .env
```

Build and Up Docker container

```bash
docker-compose -f docker-compose.yml up -d --build
```

Open python console on container

```bash
docker exec -it drones_v1_django_app bash
```

Create SuperUser

```bash
python manage.py createsuperuser
```

## Enter Data for example

Username: usuario

Email: user@email.com

Password: Password\*2022

Password (again): Password\*2022

## Execute example.py and copy token for enpoints

```bash
python example.py
```

![alt text](https://github.com/angelqva/drone/blob/main/media/dash-02.jpg?raw=true)

## License

[MIT](https://choosealicense.com/licenses/mit/)
