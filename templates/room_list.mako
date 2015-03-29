# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>
<h1>Join Room</h1>
<div id="join">
% if rooms:
    % for room in rooms:
        <div class="fieldcontainer">
            <p class="alighleft"><a href="/room/${room['room_id']}">${room['name']}</a></p>
            <p class="alighright"><a href="/delete_room/${room['room_id']}">x</a></p>
        </div>
    % endfor
% else:
  <div>There are no rooms. Create new one. Be the first.</div>
% endif
</div>

<h1>Or Add New One</h1>
<form class="inline" action="${request.route_url('add_room')}" method="post">
    <div class="fieldcontainer">
        <div class="label"><label form="room">Room</label></div>
        <div class="field"><input type="text" id="room" name="room" /></div>
        <div class="field"><input type="submit" value="Add" /></div>
    </div>
</form>

