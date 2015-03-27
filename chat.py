# -*- encoding: utf-8 -*-
import os
import logging
import sqlite3
import md5

from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated
from pyramid.httpexceptions import HTTPFound
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.view import view_config

from wsgiref.simple_server import make_server

logging.basicConfig()
log = logging.getLogger(__file__)

here = os.path.dirname(os.path.abspath(__file__))

# Start page where we can login
@view_config(route_name='login', renderer='login.mako')
def login_view(request):
    if request.method == 'POST' and request.POST.get('name') and request.POST.get('password'):
        name = request.POST.get('name')
        password = md5.md5(request.POST.get('password')).hexdigest()
        if not user_exists(request, name, password):
            request.session.flash('User not found!')
            return HTTPFound(location=request.route_url('login'))
        return HTTPFound(location=request.route_url('chat_rooms'))
    return {}

# Registration page
@view_config(route_name='register', renderer='register.mako')
def register_view(request):
    if request.method == 'POST' and request.POST.get('name') and request.POST.get('password1'):
        name = request.POST.get('name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if name_exists(request, name):
            request.session.flash('Specified name: %s already exists' % name)
            return HTTPFound(location=request.route_url('register'))
        if password1 != password2:
            request.session.flash('Password mismatch! Please check your password.')
            return HTTPFound(location=request.route_url('register'))
        if len(password1) < 5:
            request.session.flash('The password cannot be shorter than 5 symbols.')
            return HTTPFound(location=request.route_url('register'))

        password = md5.md5(password1).hexdigest()
        add_user(request, name, password)
        return HTTPFound(location=request.route_url('login'))
    return {}

# Show all available chat rooms
@view_config(route_name='chat_rooms', renderer='chat_rooms.mako')
def chat_rooms_view(request):
    return {}

# subscribers
@subscriber(NewRequest)
def new_request_subscriber(event):
    request = event.request
    settings = request.registry.settings
    request.db = sqlite3.connect(settings['db'])
    request.add_finished_callback(close_db_connection)

def close_db_connection(request):
    request.db.close()

@subscriber(ApplicationCreated)
def application_created_subscriber(event):
    with open(os.path.join(here, 'schema.sql')) as f:
        stmt = f.read()
        settings = event.app.registry.settings
        db = sqlite3.connect(settings['db'])
        db.executescript(stmt)
        db.commit()

#custom
def user_exists(request, name, password):
    return request.db.execute("select * from users where name = ? and password = ?", (name, password)).fetchone()

def name_exists(request, name):
    return request.db.execute("select * from users where name = ?", (name,)).fetchone()

def add_user(request, name, password):
    request.db.execute(
        "insert into users (name, password) values (?, ?)", (name, password)
    )
    request.db.commit()

if __name__ == '__main__':
    # configuration settings
    settings = {}
    settings['reload_all'] = True
    settings['debug_all'] = True
    settings['mako.directories'] = os.path.join(here, 'templates')
    settings['db'] = os.path.join(here, 'chat.db')
    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    # configuration setup
    config = Configurator(settings=settings, session_factory=session_factory)
    # add mako templating
    config.include('pyramid_mako')
    # routes setup
    config.add_route('login', '/')
    config.add_route('register', '/register')
    config.add_route('chat_rooms', '/chat-rooms')
    config.add_route('message', '/message')
    config.add_route('error', '/error')
    # static view setup
    config.add_static_view('static', os.path.join(here, 'static'))
    # scan for @view_config and @subscriber decorators
    config.scan()
    # serve app
    app = config.make_wsgi_app()
    port = int(os.environ.get('PORT', '5000'))
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()