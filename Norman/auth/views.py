# -*- coding: utf-8 -*-


from flask import Blueprint, render_template, redirect, url_for, request

blueprint = Blueprint('auth', __name__, url_prefix='/auth', static_folder='../static')


@blueprint.route('/', methods=['GET'])
def auth():
    return redirect(url_for('auth.register'))


@blueprint.route('/login', methods=['GET'])
def login():
    return render_template('dashboard/admin/login.html')


@blueprint.route('/register', methods=['GET'])
def register():
    action = request.args.get('action')
    if action:
        if action == "verify":
            return verify()
    return render_template('dashboard/admin/register.html')


# FOR SELECTION OF PLAN ID AFTER REGISTRATION
@blueprint.route('/register/plans', methods=['GET'])
def plan():
    return render_template('dashboard/admin/plans.html')


def verify():
    return render_template('dashboard/admin/verify.html')

