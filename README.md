# Django JWT Rest Template

You can fork this project as a starting point for your Django-based JSON Web Token REST API.


## Included

- `jwt_key_gen` script to generate JSON Web Token keys on the command line.
- `django-jwt-auth`, a custom Django backend that works with microservices and the Django REST Framework.
- `djangorestframework`
- `djangorestframework-jsonapi`
- `docker`-ized for your convenience
- `Postgres` integration through docker


## Installation

- install `Docker`
- fork the repo
- check for `TODO TEMPLATE-USER:` in the codebase, and modify the code accordingly
- `docker-compose up --build`


## Usage

- implement a REST API (ie: models, views, routes, etc...)

## TODO

- instructions for deploying to Heroku
- instructions for deploying to AWS
- instructions for integration into Kubernetes
- integrate `django-kube-wrapper` to read secrets into the settings file
- configure logging
- documentation on how to bash, psql