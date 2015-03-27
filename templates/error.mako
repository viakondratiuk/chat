# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>
% if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        <p class="error">${message}</p>
    % endfor
% endif
<input type="button" value="Back" onclick="history.back();" />