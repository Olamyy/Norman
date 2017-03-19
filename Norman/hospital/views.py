# -*- coding: utf-8 -*-
"""User views."""

from flask import Blueprint, render_template

blueprint = Blueprint('hospital', __name__, url_prefix='/hospital', static_folder='../static')


@blueprint.route('/', methods=['GET'])
def hospital():
    return render_template('auth/login.html')

