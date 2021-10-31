import sqlite3

conn = sqlite3.connect("flask_board.db")


#   user_id : pk, 유저 id
#   password : 유저 비밀번호
#   nickname : 유저 닉네임
#   is_admin : 어드민 여부
CREATE_USER_TABLE = """
    create table if not exists user(
        user_id     char(16) not null primary key,
        password    char(64) not null,
        nickname    char(10) UNIQUE not null,
	    is_admin    INTEGER NOT NULL DEFAULT 0
    );
"""

#   article_id : pk, 글 번호
#   board : 글이 있는 게시판
#   user_id : fk, 작성자
#   title : 글 제목
#   article_time : 글 작성시간
#   content : 글 내용
#   view : 조회수
#   hit : 추천 수
CREATE_ARTICLE_TABLE = """
    create table if not exists article(
        article_id integer not null primary key autoincrement,
        board char(10) not null,
        user_id char(16),
        title char(20) not null,
        article_time TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')) not null,
        content blob not null,
        view unsigned int default 0 not null,
        hit unsigend int default 0 not null,
        CONSTRAINT user_id_fk FOREIGN KEY(user_id) REFERENCES user(user_id)
         ON UPDATE CASCADE ON DELETE SET NULL
    );
"""

#   comment_id : pk, 댓글 id
#   user_id : fk, 댓글 작성자 id
#   article_id : fk, 댓글 작성된 게시물 id
#   comment : 댓글 내용
#   comment_time : 댓글 작성시간
CREATE_COMMENT_TABLE = """
    create table if not exists comment(
        comment_id integer not null primary key autoincrement,
        article_id int not null,
        user_id char(16),
        comment char(100) not null,
        comment_time TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')) not null,
        CONSTRAINT user_fk FOREIGN KEY(user_id) REFERENCES user(user_id)
         ON UPDATE CASCADE ON DELETE SET NULL,
        CONSTRAINT article_fk FOREIGN KEY(article_id) REFERENCES article(article_id)
         ON UPDATE CASCADE ON DELETE CASCADE 
    );
"""

#   hit_id : pk, 추천기록 id
#   user_id : fk, 추천한 사람 id
#   article_id : fk, 추천된 게시물 id
#   hit_time : 댓글 작성시간
CREATE_ARTICLE_HIT_HISTORY_TABLE = """
    create table if not exists hit_history(
        hit_id integer not null primary key autoincrement,
        article_id int,
        user_id char(16),
        hit_time TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')) not null,
        CONSTRAINT user_fk FOREIGN KEY(user_id) REFERENCES user(user_id)
         ON UPDATE CASCADE ON DELETE SET NULL,
        CONSTRAINT article_fk FOREIGN KEY(article_id) REFERENCES article(article_id)
         ON UPDATE CASCADE ON DELETE CASCADE 
    );
"""

#   file_id : pk, 파일 id
#   file_name : 업로드 당시 서버가 받았던 파일 이름
#   file_type : 파일 타입
#   upload_time : 파일이 업로드된 시간
CREATE_IMAGE_FILE_TABLE = """
    create table if not exists image_files(
        file_id integer not null primary key autoincrement,
        file_name char(50),
        file_type char(10) not null,
        upload_time TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')) not null
    );
"""

conn.execute(CREATE_USER_TABLE)
conn.execute(CREATE_ARTICLE_TABLE)
conn.execute(CREATE_COMMENT_TABLE)
conn.execute(CREATE_ARTICLE_HIT_HISTORY_TABLE)
conn.execute(CREATE_IMAGE_FILE_TABLE)

#### TO-DO 비 회원 게시판 전용 테이블 ####



conn.commit()
conn.close()
