# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/', methods=['GET'])
def home():
    return render_template('landingpage/indexed.html')


@blueprint.route('/privacy', methods=['GET'])
def privacy():
    return render_template('landingpage/privacy.html')


@blueprint.route('/services', methods=['GET'])
def services():
    return render_template('landingpage/services.html')


@blueprint.route('/service', methods=['GET'])
def service():
    return render_template('landingpage/single-service.html')


@blueprint.route('/hospital', methods=['GET'])
def hospital():
    return render_template('landingpage/single-hospital.html')
