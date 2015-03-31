# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>
<a href="/room_list">Room List</a>
<a href="/logout">Logout</a>
<h1>Room: <u>${request.session['room']['name']}</u></h1>

<div id="chat">
% if history:
    % for m in history:
        % if m['type'] == 'message':
            <div id="m${m['id']}"><span>[${m['datetime']}]</span> <b>${m['name']}:</b> <span>${m['message']}</span></div>
        % elif m['type'] == 'system':
            <div id="m${m['id']}"><b>${m['message']}</b></div>
        % elif m['type'] == 'news':
            <div><i>${m['message']}</i></div>
        % endif
    % endfor
% else:
  <div>Chat history is empty.</div>
% endif
</div>

<form class="inline" id="process_message" action="${request.route_url('process_message')}" method="post">
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

<div class="center">
    <a class="toggle" href="#" onclick="toggleVisibility('commands'); return false;" title="Available commands">Available commands</a>
</div>
<div id="commands" style="display: none">
    <ul>
        <li>/clear - clears chat window</li>
        <li>/search search terms - search for search string, can be delimited by spaces</li>
        <li>/sum 1 2 3 4 5 - finds sum of elements delimited by spaces</li>
        <li>/product 1 2 3 4 5 - finds product of elements delimited by spaces</li>
        <li>/mean 1 2 3 4 5 6 - finds mean of elements delimited by spaces</li>
    </ul>
</div>


