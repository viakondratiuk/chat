# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>
<h1>Room {room_name}</h1>
<div id="chat" style="width: 273px; height: 200px; overflow: auto; margin: 0 auto;">
% if history:
    % for m in history:
        <div><b>${m['name']}:</b> <span>${m['message']}</span></div>
    % endfor
% else:
  <div>Chat history is empty.</div>
% endif
</div>
<input type="button" name="refresh" id="refresh" value="Refresh" />
<script type="text/javascript">
    document.getElementById('chat').scrollTop = 9999999;
</script>
<form class="inline" action="${request.route_url('add_message')}" method="post">
    <input type="hidden" name="id" value="18"/>
    <div class="fieldcontainer">
        <div class="label"><label form="message">Message</label></div>
        <div class="field"><input type="text" id="message" name="message" /></div>
        <div class="field"><input type="submit" value="Add" /></div>
    </div>
</form>

