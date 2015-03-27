create table if not exists users (
    id integer primary key autoincrement,
    name char(32) not null unique,
    password char(32) not null
);

create table if not exists chat_chanells (
    id integer primary key autoincrement,
    name char(32) not null unique
);

create table if not exists chat_messages (
    id integer primary key autoincrement,
    user_id integer not null,
    channel_id integer not null,
    datetime datetime default (datetime('now', 'localtime')),
    message text not null
);
