import sqlite3

conn = sqlite3.connect("test.db")


#   uid : pk, 유저 id
#   pwd : 유저 비밀번호
#   nickname : 유저 닉네임
CREATE_USER_TABLE = """
    create table if not exists user(
        uid char(10) not null primary key,
        pwd char(64) not null,
        nickname char(10) UNIQUE not null
    );
"""

#   aid : pk, 글 번호
#   board : 글이 있는 게시판
#   uid : fk, 작성자
#   title : 글 제목
#   date_time : 글 작성시간
#   content : 글 내용
#   view : 조회수
#   hit : 추천 수
CREATE_ARTICLE_TABLE = """
    create table if not exists article(
        aid integer not null primary key autoincrement,
        board char(10) not null,
        uid char(10) not null,
        title char(20) not null,
        date_time TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')) not null,
        content blob not null,
        view unsigned int default 0 not null,
        hit unsigend int default 0 not null,
        CONSTRAINT uid_fk FOREIGN KEY(uid) REFERENCES user(uid)
         ON UPDATE CASCADE ON DELETE SET NULL
    );
"""

#   cid : pk, 댓글 id
#   uid : fk, 댓글 작성자 id
#   aid : fk, 댓글 작성된 게시물 id
#   comment : 댓글 내용
#   date_time : 댓글 작성시간
CREATE_COMMENT_TABLE = """
    create table if not exists comment(
        cid integer not null primary key autoincrement,
        aid char(10) not null,
        uid char(10),
        comment char(100) not null,
        date_time TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')) not null,
        CONSTRAINT uid_fk FOREIGN KEY(uid) REFERENCES user(uid)
         ON UPDATE CASCADE ON DELETE SET NULL,
        CONSTRAINT aid_fk FOREIGN KEY(aid) REFERENCES article(aid)
         ON UPDATE CASCADE ON DELETE CASCADE 
    );
"""

#   hid : pk, 추천기록 id
#   uid : fk, 추천한 사람 id
#   aid : fk, 추천된 게시물 id
#   date_time : 댓글 작성시간
CREATE_ARTICLE_HIT_HISTORY_TABLE = """
    create table if not exists hit_history(
        hid integer not null primary key autoincrement,
        aid char(10),
        uid char(10),
        date_time TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')) not null,
        CONSTRAINT uid_fk FOREIGN KEY(uid) REFERENCES user(uid)
         ON UPDATE CASCADE ON DELETE SET NULL,
        CONSTRAINT aid_fk FOREIGN KEY(aid) REFERENCES article(aid)
         ON UPDATE CASCADE ON DELETE CASCADE 
    );
"""

conn.execute(CREATE_USER_TABLE)
conn.execute(CREATE_ARTICLE_TABLE)
conn.execute(CREATE_COMMENT_TABLE)
conn.execute(CREATE_ARTICLE_HIT_HISTORY_TABLE)

#### TO-DO 비 회원 게시판 전용 테이블 ####



conn.commit()
conn.close()
