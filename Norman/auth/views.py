# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request
from Norman.models import Hospital
from mongoengine.errors import DoesNotExist

blueprint = Blueprint('auth', __name__, url_prefix='/auth', static_folder='../static')


@blueprint.route('/', methods=['GET'])
def auth():
    return redirect(url_for('auth.register'))


@blueprint.route('/hospital/register', methods=['GET'])
def register():
    action, verification_id = request.args.get('action'), request.args.get('verID')
    if action:
        if action == "verify":
            return redirect(url_for('auth.verify', action=action, verID=verification_id))
    return render_template('dashboard/admin/register.html')


@blueprint.route('/hospital/register/plans', methods=['GET'])
def plan():
    return render_template('dashboard/admin/plans.html')


@blueprint.route('/hospital/verify', methods=['GET'])
def verify():
    verification_id = request.args.get('verID')
    try:
        hospital = Hospital.objects.get(ver_id=verification_id)
        return render_template('dashboard/admin/verify.html', hospital=hospital)
    except DoesNotExist as error:
        return redirect(url_for('auth.login'))
