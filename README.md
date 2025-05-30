# Django Liberty 🗽

Easy decoupled Django projects with OIDC Auth.

## TL;DR

Recommended
```python
uvx cookiecutter && cookiecutter https://github.com/roicort/django-liberty.git
```
Or
```python
pip install cookiecutter && cookiecutter https://github.com/roicort/django-liberty.git
```

### What?

Django Liberty is a cookiecutter template for Decoupled Django projects. It is a full-stack template that includes both backend and frontend. The backend part is based on Django and the frontend is based on Nuxt or Next.js (your choice).
Cookiecutter handles the project creation and configuration, secrets, and environment variables. The project is ready to run with Docker Compose and pre-configured with OIDC Auth, Unfold admin theme, and custom user model.

### Why?

The main problem I encountered while decoupling Django was the authentication, while some boilerplates provide JWT Auth, I wanted to use OpenID Connect (OIDC) for authentication. As I spent a lot of time setting this, I decided to create a cookiecutter template that includes all the necessary packages and configurations to start a new project quickly.

### Current Status

- [x] Cookiecutter template
  - [x] Docker Compose
  - [x] Postgenerate hooks
  - [x] Frontend choice
- [x] Django backend
  - [x] Dockerfile
  - [x] Custom user model with email as username (Account)
  - [x] OIDC Provider Config
  - [x] Unfold Admin
  - [x] OpenAPI
  - [x] Claims
  - [ ] OIDC Templates
- [ ] Next frontend
  - [x] Dockerfile
  - [x] Auth.js
- [ ] Nuxt frontend
  - [ ] Dockerfile
  - [ ] Auth.js

### Features

- **Cookiecutter**: Start a new project by just running `cookiecutter https://github.com/roicort/django-liberty.git`
- **Docker Compose**: start both front end and backend by just running `docker-compose up --build`
- **Django backend**: Custom django backend with Unfold Admin
- **Custom user model**: extended default Django user model to include additional fields
- **Decoupled frontend**: Nuxt and Next available (WIP)
- **OIDC Auth**: Pre-configured OIDC Auth with Django as Provider and Frontend-[Nuxt/Next] as RP (Client)
- **Admin Theme**: Unfold admin theme with user & group management

![](https://github.com/user-attachments/assets/2ff0d3ff-dfdf-4dab-ad54-c9e6131e9788)

## Quickstart

To start using django-liberty, it is needed to create a cookiecutter project from the template. After the project is created, it is possible to start the project by running docker-compose command.

```
cookiecutter https://github.com/roicort/django-liberty.git
```

- Set {{cookiecutter.project_slug}}
- Select {{cookiecutter.frontend}} [Nuxt or Next]

### Running docker-compose

```bash
cd {{cookiecutter.project_slug}}
docker compose up -d --build
```

Then, open the browser and navigate to `http://localhost:3000` to see the front end part of the application. To access Django admin, navigate to `http://localhost:8000/admin/`.

### Backend dependencies

For dependency management in Django application we are using UV. When starting the project through the docker-compose command, it is checked for new dependencies as well. In the case they are not installed, docker will install them before running development server.

- **[djangorestframework](https://github.com/encode/django-rest-framework)** - REST API support
- **[django-oidc-provider]()** - OIDC Provider
- **[drf-spectacular](https://github.com/tfranzel/drf-spectacular)** - OpenAPI schema generator
- **[django-unfold](https://github.com/unfoldadmin/django-unfold)** - Admin theme for Django admin panel

Below, you can find a command to install new dependency into backend project.

```bash
docker compose exec backend uv add djangorestframework
```

For initializing the backend first run init.sh within the container (No longer needed)

```bash
docker compose exec backend bash
```

```bash
bash init.sh
```

And create a superuser (No longer needed, can be done through env)

```bash
uv run manage.py createsuperuser
```

## ⚠️ Hosts config ⚠️

In the case you want to locally try the OIDC login, you may add the backend to the hosts file. Its necessary to have two separate hosts for the frontend and backend.

```bash
sudo [vi/nano] /etc/hosts
```

    ##
    # Host Database
    #
    # localhost is used to configure the loopback interface
    # when the system is booting.  Do not change this entry.
    ##
    127.0.0.1       localhost
    255.255.255.255 broadcasthost
    ::1             localhost
    127.0.0.1       backend          <--- add this line

After that, when your frontend redirects you to the login page, you be able to see `http://backend:8000/oidc/etc..`

## Authentication

For the authentication, Django Liberty uses **django-oidc-provider** and **auth.js** package to provide Open ID Connect authentication. All configuration and secrets are generated by cookiecutter and set in envs.

### User accounts on the backend

There are two ways how to create new user account in the backend. First option is to run managed command responsible for creating superuser. It is more or less required, if you want to have an access to the Django admin. After running the command below, it will be possible to log in on the front end part of the application.

```bash
docker compose exec backend uv run manage.py createsuperuser
```

The second option how to create new user account is to register it on the front end. The Django admin provides simple registration form in account/signup/ endpoint. After the registration, the user account will be created in the backend.

### OpenAPI

By default, Django Liberty includes and endpoint for OpenAPI schema which is available in Swagger `http://localhost:8000/api/schema/swagger-ui/` or ReDOC in `http://localhost:8000/api/schema/redoc/`

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

## ⭐️ Support

Give a ⭐️ if you liked this project

## License

The MIT License

## Shoutout

### This project aims to be an extention of the idea by [Turbo](https://github.com/unfoldadmin/turbo)
