# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>
<h1>Register</h1>
<form action="${request.route_url('register')}" onsubmit="return comparePasswords('password1', 'password2');" method="post">
    <label form="name">Name:</label>
    <input type="text" id="name" name="name" />

    <label form="password1">Password:</label>
    <input type="password" id="password1" name="password1" />

    <label form="password2">Retype password:</label>
    <input type="password" id="password2" name="password2" />

    <input type="submit" value="Register" />
</form>
<div class="center" ><a href="/">Login</a></div>

