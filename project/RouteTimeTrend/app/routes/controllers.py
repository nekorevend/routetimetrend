__author__ = 'vchang'
from flask import Blueprint, request, render_template, redirect, url_for

routes = Blueprint('routes', __name__, url_prefix='/routes')

# from run import app

import re
import urllib
import time
import datetime
from subprocess import check_output, TimeoutExpired
from bs4 import BeautifulSoup
from retry import retry

from app.routes.models import Route, RouteTime
from app.routes.forms import AddRouteForm

from app import db

@routes.route('/')
def index():
    hours_test = 'https://www.google.com/maps/dir/Los+Angeles,+CA/Sydney,+NS,+Canada/@39.6024415,-106.8817656,4z/data=!3m1!4b1!4m14!4m13!1m5!1m1!1s0x80c2c75ddc27da13:0xe22fdf6f254608f4!2m2!1d-118.2436849!2d34.0522342!1m5!1m1!1s0x4b67fb367e723415:0xa783539b7b308087!2m2!1d-60.194224!2d46.1367899!3e0'
    hours_minutes_test = 'https://www.google.com/maps/dir/Los+Angeles,+CA/San+Francisco,+CA/@35.8599167,-124.7220576,6z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x80c2c75ddc27da13:0xe22fdf6f254608f4!2m2!1d-118.2436849!2d34.0522342!1m5!1m1!1s0x80859a6d00690021:0x4a501367f076adff!2m2!1d-122.4194155!2d37.7749295'
    minutes_test = 'https://www.google.com/maps/dir/Santa+Monica,+CA/Beverly+Hills,+CA/@34.0309858,-118.3222016,12z/data=!3m1!4b1!4m14!4m13!1m5!1m1!1s0x80c2a4cec2910019:0xb4170ab5ff23f5ab!2m2!1d-118.4911912!2d34.0194543!1m5!1m1!1s0x80c2bc04d6d147ab:0xd6c7c379fd081ed1!2m2!1d-118.4003563!2d34.0736204!3e0'

    start_time = time.time()
    output = 'Hours only: '
    output += str(get_duration(hours_test))
    output += '<br/>Hours and minutes: '
    output += str(get_duration(hours_minutes_test))
    output += '<br/>Minutes only: '
    output += str(get_duration(minutes_test))
    processing_time = (time.time() - start_time)
    output += '<br/>Results grabbed in: ' + str(processing_time) + ' seconds'
    return output

@routes.route('/list')
def route_list():
    routes = Route.query.all()

    return render_template('routes.html', title='Route List', routes=routes)


@routes.route('/add', methods=['GET', 'POST'])
def add_route():
    form = AddRouteForm(request.form)
    print(form.errors)
    if form.validate_on_submit():
        route = Route()
        route.name = form.name.data
        route.url = form.url.data
        db.session.add(route)
        db.session.commit()
        return redirect(url_for('routes.add_route'))

    return render_template('add_route.html', title='Add Route', form=form)


@routes.route('/<int:route_id>/check_now')
def manual_route_poll(route_id):
    save_duration(route_id)
    return redirect(url_for('routes.route_list'))

def save_duration(route_id):
    route = Route.query.get(route_id)
    if route:
        route_time = RouteTime()
        route_time.route_id = route.id
        file = open('/out/route'+str(route.id)+'.html', 'w+')
        route_time.duration = get_duration(route.url, file)
        file.close()
        if route_time.duration:
            print('Saving for route', route_id, ":", route.name)
            db.session.add(route_time)
            db.session.commit()
        else:
            print('Failed to get duration for route', route_id)

@retry(tries=2)
def get_duration(url, file):
    print('Attempting to get duration for', url)
    result = ''
    html_source = ''
    html_source = check_output('chromium-browser --headless --disable-gpu --dump-dom --no-sandbox --disable-software-rasterizer --disable-dev-shm-usage --virtual-time-budget=20000 ' + url, encoding='UTF-8', shell=True)

    file.write(html_source)

    soup = BeautifulSoup(html_source, features='html.parser')
    result = soup.find('img', src=re.compile('directions_car'), attrs={'aria-label': 'Driving'})

    matches = None
    while result.parent and not matches:
        result = result.parent
        matches = re.search('((?:(?:\d+ h(?:our[s]?)? ?)|(?:\d+ min[s]? ?))+)', str(result))
        if matches:
            return parse_duration(matches.group(1))
    raise Exception('No time match found!')

def parse_duration(duration_str):
    hours = 0
    minutes = 0
    match = re.search(r'(\d+) h', duration_str)
    if match:
        hours = match.group(1)
    match = re.search(r'(\d+) min', duration_str)
    if match:
        minutes = match.group(1)
    return datetime.timedelta(hours=int(hours), minutes=int(minutes))
