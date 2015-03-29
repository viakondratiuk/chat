# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>
<h1>Register</h1>
<form class="standard" action="${request.route_url('register')}" onsubmit="return comparePasswords('password1', 'password2');" method="post">
    <div class="fieldcontainer">
        <div class="label"><label form="name">Name</label></div>
        <div class="field"><input type="text" id="name" name="name" /></div>
    </div>

    <div class="fieldcontainer">
        <div class="label"><label form="password1">Password 1</label></div>
        <div class="field"><input type="password" id="password1" name="password1" /></div>
    </div>

    <div class="fieldcontainer">
        <div class="label"><label form="password2">Password 2</label></div>
        <div class="field"><input type="password" id="password2" name="password2" /></div>
    </div>
    <br />
    <br />
    <input type="submit" value="Register" /> or <a href="/">Login</a>
</form>

