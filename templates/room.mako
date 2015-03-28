# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>
<h1>Room: <u>${room['name']}</u></h1>
<a href="/room_list">Room List</a>
<a href="/logout">Logout</a>
<div id="chat">
% if history:
    % for m in history:
        <div><span>[${m['datetime']}]</span> <b>${m['name']}:</b> <span>${m['message']}</span></div>
    % endfor
% else:
  <div>Chat history is empty.</div>
% endif
</div>

<form class="inline" action="${request.route_url('add_message')}" method="post">
    <input type="hidden" name="id" value="${room['id']}"/>
    <div class="fieldcontainer">
        <div class="field"><input type="text" id="message" name="message" autocomplete="off"/></div>
        <div class="field"><input type="submit" value="Add" /></div>
    </div>
</form>

