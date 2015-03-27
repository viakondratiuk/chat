# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>
<h1>Available Rooms</h1>
% if rooms:
    <table class="info" align="center">
        <tr>
            <td>Name</td>
        </tr>
    % for room in rooms:
        <tr>
            <td><a href="/join_room?id=${room['room_id']}">${room['name']}</a></td>
        </tr>
    % endfor
    </table>
% else:
  <p>There are no rooms. Create new one. Be the first.</p>
% endif

<h1>Add Room</h1>
<form action="${request.route_url('add_room')}" method="post">
    <label form="room">Name:</label>
    <input type="text" id="room" name="room" />

    <input type="submit" value="Go" />
</form>

