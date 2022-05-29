# DRONES APIREST

APIREST for solve Drones problem

## Installation

# Clone this repository

```bash
git clone git@github.com:angelqva/drone.git
```

# Necessary files

Create Folder with name logs

add file celery.log

copy .env configuration on terminal

```bash
copy .env.sample .env
```

# Build and Up Docker container

```bash
docker-compose -f docker-compose.yml up -d --build
```

# Create User and data sample

Open python console on container

```bash
docker exec -it drones bash
```

Create SuperUser

```bash
python manage.py createsuperuser
```

Enter this data

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

[BSD](https://choosealicense.com/licenses/bsd/)
