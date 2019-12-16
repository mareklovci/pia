import os
import secrets

from PIL import Image
from flask import current_app, url_for
from flask_mail import Message
from wtforms.validators import ValidationError

from app import mail


def save_picture(form_picture, output_size=(125, 125), nbytes=8):
    random_hex = secrets.token_hex(nbytes)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password visit following link:
    {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)


class Unique(object):
    """Validator checking field uniqueness"""

    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = 'The element already exists. Please choose a different one.'
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        object_id = form.id.data if 'id' in form else None
        if check and (object_id is None or object_id != check.id):
            raise ValidationError(self.message)
