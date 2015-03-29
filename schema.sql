create table if not exists user (
    id integer primary key autoincrement,
    name char(32) not null unique,
    password char(32) not null
);

create table if not exists room (
    id integer primary key autoincrement,
    name char(32) not null unique
);

create table if not exists message (
    id integer primary key autoincrement,
    user_id integer not null,
    room_id integer not null,
    datetime datetime default (datetime('now', 'localtime')),
    message text not null,
    FOREIGN KEY(room_id) REFERENCES room(id) ON DELETE CASCADE
);
