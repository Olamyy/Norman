# -*- coding: utf-8 -*-
"""User views."""

from flask import Blueprint, render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import login_user
from flask import request
from Norman.hospital.models import Hospital
from Norman.hospital.forms import RegisterForm
from Norman.utils import flash_errors

blueprint = Blueprint('auth', __name__, url_prefix='/auth', static_folder='../static')


@blueprint.route('/login', methods=['GET'])
def login():
    form = RegisterForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('auth/login.html', form=form)


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        Hospital(name=form.name.data, email=form.email.data, password=form.password.data, confirm=form.confirm.data, active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        print('Noe')
        flash_errors(form)
    return render_template('auth/register.html', form=form)

