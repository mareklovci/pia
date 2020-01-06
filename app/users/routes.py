from typing import List

from faker import Faker
from faker.providers import barcode, internet, phone_number, credit_card
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import bcrypt, db
from app.models import Role, Roles, User
from app.users.forms import (LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm,
                             UpdateUserForm)
from app.users.utils import save_picture, send_reset_email
from app.utils import roles_required

from random import randint

users = Blueprint('users', __name__)

fake = Faker()
fake.add_provider(barcode)
fake.add_provider(internet)
fake.add_provider(phone_number)
fake.add_provider(credit_card)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token!', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route('/user')
@login_required
@roles_required([Roles.ADMIN.value])
def list_users():
    users: List = User.query.order_by(User.username.asc()).all()
    users.remove(current_user)  # remove current user from the list
    return render_template('list_users.html', users=users)


# noinspection PyArgumentList
@users.route('/user/create', methods=['GET', 'POST'])
@login_required
@roles_required([Roles.ADMIN.value])
def create_user():
    form = RegistrationForm()

    if request.method == 'GET':
        # push random values into the form
        form.name.data = fake.name()
        form.birth_number.data = fake.ean(length=13)
        form.address.data = fake.address()
        form.username.data = 'User' + str(randint(1000, 9999))
        form.email.data = form.username.data + '@' + fake.free_email_domain()
        form.phone.data = fake.phone_number()
        form.card_number.data = fake.credit_card_number(card_type=None)
        form.account_number.data = fake.ean(length=13)
        form.password.data = str(randint(1000, 9999))

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_role = Role.query.filter_by(name=form.role.data).first()
        user = User(name=form.name.data,
                    birth_number=form.birth_number.data,
                    address=form.address.data,
                    username=form.username.data,
                    email=form.email.data,
                    phone=form.phone.data,
                    card_number=form.card_number.data,
                    account_number=form.account_number.data,
                    password=hashed_password,
                    role_id=user_role.id)
        db.session.add(user)
        db.session.commit()
        flash(f'The account has been created! User is now able to log in.', 'success')
        return redirect(url_for('users.list_users'))
    return render_template('create_user.html', title='Register', form=form)


@users.route('/user/<int:user_id>/update', methods=['GET', 'POST'])
@login_required
@roles_required([Roles.ADMIN.value])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UpdateUserForm()
    form.id.data = user.id  # we need to push user id into the form to validate user uniqueness
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash(f'The account of user {user.username} has been updated!', 'success')
        return redirect(url_for('users.update_user', user_id=user.id))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('update_user.html', title='User', image_file=image_file, form=form, user=user)


@users.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@roles_required([Roles.ADMIN.value])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('users.list_users'))
