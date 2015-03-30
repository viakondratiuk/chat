# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>
<a href="/room_list">Room List</a>
<a href="/logout">Logout</a>
<h1>Room: <u>${request.session['room']['name']}</u></h1>

<div id="chat">
% if history:
    % for m in history:
        <div><span>[${m['datetime']}]</span> <b>${m['name']}:</b> <span>${m['message']}</span></div>
    % endfor
% else:
  <div>Chat history is empty.</div>
% endif
</div>

<form id="add_message" class="inline" action="${request.route_url('add_message')}" method="post">
    <input type="hidden" name="id" value="${request.session['room']['id']}"/>
    <div class="field_container">
        <div class="label">
            <label form="message"><b>${request.session['user']['name']}</b></label>
        </div>
        <div class="field">
            <input type="text" id="message" name="message" autofocus />
        </div>
        <div class="field">
            <input type="submit" value="Add" />
        </div>
    </div>
</form>

