# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>
<h1>Room</h1>
% if history:
    <table class="info" align="center">
        <tr>
            <td>Name</td>
            <td>Message</td>
        </tr>
    % for m in history:
        <tr>
            <td><b>${m['name']}</b></td>
            <td>${m['message']}</td>
        </tr>
    % endfor
    </table>
% else:
  <p>Chat history is empty.</p>
% endif

<h1>Add Message</h1>
<form action="${request.route_url('add_message')}" method="post">
    <label form="message">Name:</label>
    <input type="text" id="message" name="message" />

    <input type="submit" value="Go" />
</form>

