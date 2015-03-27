# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>
<h1>Login</h1>
<form action="${request.route_url('login')}" method="post">
    <label form="name">Name:</label>
    <input type="text" id="name" name="name" />
    <label form="password">Password:</label>
    <input type="password" id="password" name="password" />
    <input type="submit" value="Login" />
</form>
<div class="center" ><a href="/register">Register</a></div>

