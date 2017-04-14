# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/', methods=['GET'])
def home():

    return render_template('landingpage/indexed.html')


@blueprint.route('/privacy', methods=['GET'])
def privacy():
    return render_template('landingpage/privacy.html')

