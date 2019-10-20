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
| User0003 | 0003     | secretary     |
| User0004 | 0004     | secretary     |

## Invoices

Two invoices for each user.

## Create secret key

```python
import secrets

secrets.token_hex(16)
```