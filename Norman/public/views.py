# -*- coding: utf-8 -*-

from flask import Blueprint,render_template

blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/', methods=['GET'])
def home():
    return render_template('landingpage/index.html')


@blueprint.route('/privacy', methods=['GET'])
def privacy():
    return render_template('landingpage/privacy.html')


@blueprint.route('/help', methods=['GET'])
def help():
    return render_template('landingpage/privacy.html')


@blueprint.route('/features', methods=['GET'])
def features():
    return render_template('landingpage/features.html')


@blueprint.route('/promo-video', methods=['GET'])
def youtube():
    return render_template('landingpage/features.html')


@blueprint.route('/about', methods=['GET'])
def pricing():
    return render_template('landingpage/pricing.html')


@blueprint.route('/pricing', methods=['GET'])
def about():
    return render_template('landingpage/pricing.html')