# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>
<a href="/room_list">Room List</a>
<a href="/logout">Logout</a>
<h1>Room: <u>${room['name']}</u></h1>

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
    <input type="hidden" name="id" value="${room['id']}"/>
    <div class="fieldcontainer">
        <div class="label"><label form="message"><b>${request.session['user']['name']}</b></label></div>
        <div class="field"><input type="text" id="message" name="message" value="" autofocus /></div>
        <div class="field"><input type="button" value="Add" onclick="addMessage()"/></div>
    </div>
</form>

