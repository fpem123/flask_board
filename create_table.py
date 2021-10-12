import sqlite3

conn = sqlite3.connect("test.db")

CREATE_USER_TABLE = """
    create table if not exists user(
        uid char(10) not null primary key,
        pwd char(10) not null,
        nickname char(10) not null
    );
"""

CREATE_ARTICLE_TABLE = """
    create table if not exists article(
        aid integer not null primary key autoincrement,
        board char(10) not null,
        uid char(10) not null,
        pwd char(10) not null,
        title char(20) not null,
        date_time TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')) not null,
        content blob not null,
        CONSTRAINT uid_fk FOREIGN KEY(uid) REFERENCES user(uid)
    );
"""

conn.execute(CREATE_USER_TABLE)
conn.execute(CREATE_ARTICLE_TABLE)

conn.commit()
conn.close()
