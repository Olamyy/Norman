# -*- coding: utf-8 -*-
"""User views."""

from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint('hospital', __name__, url_prefix='/hospital', static_folder='../static')


@blueprint.route('/', methods=['GET'])
def hospital():
    return render_template('auth/login.html')
