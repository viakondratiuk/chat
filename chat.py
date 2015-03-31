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

'''
------ Registration ------
'''


# Login page used as start page
@view_config(route_name='login', renderer='login.mako')
def login_view(request):
    if request.method == 'POST' and request.POST.get('name') and request.POST.get('password'):
        name = request.POST.get('name')
        password = md5.md5(request.POST.get('password')).hexdigest()
        if not get_user(request, name, password):
            request.session.flash('User %s not found!' % name)
            return HTTPFound(location=request.route_url('login'))

        return HTTPFound(location=request.route_url('room_list'))
    return {}


def get_user(request, name, password):
    rs = request.db.execute("select * from user where name = ? and password = ?", (name, password)).fetchone()
    if rs is not None:
        request.session['user'] = dict(id=rs[0], name=rs[1])
        return True

    return None


# Registration page
@view_config(route_name='register', renderer='register.mako')
def register_view(request):
    if request.method == 'POST' and request.POST.get('name') and request.POST.get('password1'):
        name = request.POST.get('name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if user_exists(request, name):
            request.session.flash('Specified name: %s already exists.' % name)
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


def user_exists(request, name):
    return request.db.execute("select * from user where name = ?", (name, )).fetchone()


def add_user(request, name, password):
    request.db.execute("insert into user (name, password) values (?, ?)", (name, password))
    request.db.commit()


# Logout
@view_config(route_name='logout')
def logout_view(request):
    clear_session(request)
    return HTTPFound(location=request.route_url('login'))


# Clear user session
def clear_session(request):
    add_left_message(request)
    request.session.invalidate()


'''
------ Rooms ------
'''


# Show all available chat rooms
@view_config(route_name='room_list', renderer='room_list.mako')
def room_list_view(request):
    if 'user' not in request.session:
        return HTTPFound(location=request.route_url('login'))
    if 'room' in request.session:
        add_left_message(request)

    return {'rooms': get_room_list(request)}


# Add left message of chat member
def add_left_message(request):
    message = '%s left a room' % request.session['user']['name']
    add_message(request, request.session['user']['id'], request.session['room']['id'], 'system', message)
    del request.session['room']


# Get all available rooms
def get_room_list(request):
    rs = request.db.execute("select id, name from room order by id desc")
    return [dict(room_id=row[0], name=row[1]) for row in rs.fetchall()]


# Add new room
@view_config(route_name='add_room', renderer='add_room.mako')
def add_room_view(request):
    if 'user' not in request.session:
        return HTTPFound(location=request.route_url('login'))

    if request.method == 'POST' and request.POST.get('room'):
        room = request.POST.get('room')
        request.db.execute("insert into room (name) values (?)", (room, ))
        request.db.commit()

        return HTTPFound(location=request.route_url('room_list'))
    return {}


# Delete room
@view_config(route_name='delete_room')
def delete_room_view(request):
    if 'user' not in request.session:
        return HTTPFound(location=request.route_url('login'))

    room_id = int(request.matchdict['id'])
    request.db.execute("delete from room where id = ?", (room_id, ))
    request.db.commit()
    return HTTPFound(location=request.route_url('room_list'))


# Join selected room
@view_config(route_name='room', renderer='room.mako')
def room_view(request):
    if 'user' not in request.session:
        return HTTPFound(location=request.route_url('login'))

    room_id = int(request.matchdict['id'])
    room = get_room(request, room_id)
    if not room:
        request.session.flash('Room with id %s doesn\'t exist.' % room_id)
        return HTTPFound(location=request.route_url('room_list'))

    add_joined_message(request, room_id)
    request.session['room'] = room
    request.session['room']['last_id'] = get_room_last_msg_id(request, room_id)
    return {'history': get_room_history(request, room_id)}


def get_room(request, room_id):
    rs = request.db.execute("select * from room where id = ?", (room_id, )).fetchone()
    return dict(id=rs[0], name=rs[1]) if rs is not None else None


def add_joined_message(request, room_id):
    if 'room' not in request.session or request.session['room']['id'] != room_id:
        message = '%s joined a room' % request.session['user']['name']
        add_message(request, request.session['user']['id'], room_id, 'system', message)


def get_room_last_msg_id(request, room_id):
    rs = request.db.execute(
        "select id from message where room_id = ? order by id desc limit 1;", (room_id, )
    ).fetchone()

    return rs[0] if rs is not None else None


# Take last 10 messages from room history
def get_room_history(request, room_id):
    q = (
        "select * "
        "from "
        "(select message.id, user.name, message.type, message.message, message.datetime "
        "from message "
        "inner join user on message.user_id = user.id "
        "where message.room_id = ? order by message.id desc limit 10) "
        "as t "
        "order by id"
    )
    rs = request.db.execute(q, (room_id, ))
    return [dict(id=row[0], name=row[1], type=row[2], message=row[3], datetime=row[4]) for row in rs.fetchall()]


# Process user message
chat_commands = ['/search', '/sum', '/product', '/mean']
@view_config(route_name='process_message', renderer='json')
def process_message_view(request):
    if 'user' not in request.session:
        return HTTPFound(location=request.route_url('login'))

    if request.method == 'POST' and request.POST.get('message') and request.POST.get('id'):
        message = request.POST.get('message')
        room_id = request.POST.get('id')
        message = ' '.join(message.split())
        if message.split(' ')[0] in chat_commands:
            return {'messages': execute_command(request, message, room_id)}
        else:
            add_message(request, request.session['user']['id'], room_id, 'message', message)

    return {}


# Add message with specified type into db
def add_message(request, user_id, room_id, m_type, message):
    request.db.execute(
        "insert into message (user_id, room_id, type, message) values (?, ?, ?, ?)", (user_id, room_id, m_type, message)
    )
    request.db.commit()


# Executes one of the commands from chat_commands list
def execute_command(request, message, room_id):
    spl = message.split(' ')
    name = 'Result of %s (%s)' % (spl[0], ', '.join(spl[1:]))
    if spl[0] == '/search':
        res = [dict(name=name, type='command', message='')]
        res.extend(find_message(request, spl[1:], room_id))
        return res
    elif spl[0] == '/sum':
        res = sum(int(y) for y in spl[1:] if y.isdigit())
    elif spl[0] == '/product':
        res = reduce(lambda x, y: x * int(y) if y.isdigit() else 1, spl[1:], 1)
    elif spl[0] == '/mean':
        res = sum(int(y) for y in spl[1:] if y.isdigit())/float(len(spl[1:]))

    return [dict(name=name, type='command', message=res)]


# Search for messages in db
def find_message(request, message, room_id):
    rs = request.db.execute(
        "select * from "
        "(select message.id,  user.name, 'search', message, datetime "
        "from message "
        "inner join user on message.user_id = user.id "
        "where message like ? and room_id = ? and type='message'"
        "order by message.id desc limit 5) "
        "as t order by id", ('%'+' '.join(message)+'%', room_id)
    )
    return [dict(name=row[1], type=row[2], message=row[3], datetime=row[4]) for row in rs.fetchall()]


# Router which send responses on AJAX calls to refresh chat messages
@view_config(route_name='refresh', renderer='json')
def refresh_view(request):
    if 'user' not in request.session:
        return {}

    return {'messages': get_new_message_list(request)}


# Collect all new messages from db
def get_new_message_list(request):
    room_id = request.session['room']['id']
    last_id = request.session['room']['last_id']
    q = (
        "select message.id, user.name, message.type, message.message, message.datetime "
        "from message "
        "inner join user on message.user_id = user.id "
        "where message.room_id = ? and message.id > ?"
    )
    rs = request.db.execute(q, (room_id, last_id))
    request.session['room']['last_id'] = get_room_last_msg_id(request, room_id)
    return [dict(id=row[0], name=row[1], type=row[2], message=row[3], datetime=row[4]) for row in rs.fetchall()]


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
    config.add_route('logout', '/logout')
    config.add_route('register', '/register')
    config.add_route('room_list', '/room_list')
    config.add_route('add_room', '/add_room')
    config.add_route('delete_room', '/delete_room/{id}')
    config.add_route('room', '/room/{id}')
    config.add_route('refresh', '/refresh')
    config.add_route('process_message', '/process_message')
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