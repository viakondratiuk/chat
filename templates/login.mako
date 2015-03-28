# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>
<h1>Login</h1>
<form class="standard" action="${request.route_url('login')}" method="post">
    <div class="fieldcontainer">
        <div class="label"><label form="name">Name</label></div>
        <div class="field"><input type="text" id="name" name="name" /></div>
    </div>

    <div class="fieldcontainer">
        <div class="label"><label form="password">Password</label></div>
        <div class="field"><input type="password" id="password" name="password" /></div>
    </div>
    <br />
    <br />
    <input type="submit" value="Login" /> or <a href="/register">Register</a>
</form>

