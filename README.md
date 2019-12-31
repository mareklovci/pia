# pia
KIV/PIA

## Pre-filled data

## Users

Administrator and 2 users from each role

| Title         | email                | password   |
|---------------|----------------------|------------|
| Administrator | mareklovci@gmail.com | admin      |
| TestUser1     | testuser1@gmail.com  | testing321 |
| TestUser2     | TestUser2            | testing987 |

| Login    | password | Role          |
|----------|----------|---------------|
| Admin001 | 1234     | administrator |
| User0001 | 0001     | accountant    |
| User0002 | 0002     | accountant    |

## Invoices

Two invoices for each user.

## CSS

https://coolors.co/27187e-758bfd-aeb8fe-f1f2f6-ff8600

## Create secret key

```python
import secrets

secrets.token_hex(16)
```

## Docker

Remove Docker images: `docker rm -f $(docker ps -aq)`.

```shell script
$ docker build -f Dockerfile -t pia-flask:latest .
$ docker run -p 5000:5000 --rm -e LC_ALL=C.UTF-8 -e LANG=C.UTF-8 -e FLASK_ENV=development -e FLASK_DEBUG=1 -e FLASK_APP=app.py pia-flask
```

Endpoint: `http://192.168.99.100:5000/`.
