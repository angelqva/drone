# DRONES APIREST

APIREST for solve Drones problem

## Installation

# Clone this repository

```bash
git clone git@github.com:angelqva/drone.git
```

# Build and Up Docker container

```bash
docker-compose up -d
```

![alt text](https://github.com/angelqva/drone/blob/main/media/containers.png?raw=true)

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

![alt text](https://github.com/angelqva/drone/blob/main/media/token.png?raw=true)

## Open browser

Navigate into this url to see all api endpoints to test and docs

```bash
http://localhost:8000/
```

![alt text](https://github.com/angelqva/drone/blob/main/media/docs.png?raw=true)

## Login with simple jwt

After copy token you can auth in:

![alt text](https://github.com/angelqva/drone/blob/main/media/auth_token.png?raw=true)

Or in endpoint login-token/ yo can put user and password before and get acces token
add first JWT tkoen_access or Bearrer token_access

Navigate into this url to see all tasks running and tracking

```bash
http://localhost:5555/
```

![alt text](https://github.com/angelqva/drone/blob/main/media/task-dashboard.png?raw=true)

Thanks and Greetings!

## License

[BSD](https://choosealicense.com/licenses/bsd/)
