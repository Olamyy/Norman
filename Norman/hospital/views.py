# -*- coding: utf-8 -*-
"""User views."""

from flask import Blueprint, render_template


blueprint = Blueprint('hospital', __name__, url_prefix='/hospital', static_folder='../static')

