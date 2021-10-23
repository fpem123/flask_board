from flask import Flask
from flask import session, request
from flask import render_template, redirect, url_for, escape, flash
from datetime import timedelta

import sqlite3
import pathlib
import hashlib
import math
import re


app = Flask(__name__)
app.secret_key = b"1q2w3e4r!"
#app.permanent_session_lifetime = timedelta(minutes=10)  # 세션 시간 10분으로 설정


BOARD_DICT = {'etc':'기타', 
    'game' : '게임',
    'anonymous' : '익명',
    'no-member' : '비회원'
    }

conn = sqlite3.connect("test.db", check_same_thread=False)
conn.commit()


##############
## 허용되지 않은 게시판인지 확인
## return : boolean
##############
def isNotAllowBoard(board: str) -> bool:
    """
    ### 허용된 게시판인지 확인
    """
    return board not in BOARD_DICT


def isCorrectArticlePWD(pwd: str, aid: int):
    """
    ### 글의 비밀번호와 입력된 비밀번호가 같은지 확인
    비회원 게시판 전용
    """
    try:
        cursor = conn.cursor()

        # 게시물 비밀번호 획득
        SELECT_PWD = f"""
            SELECT  password
            FROM    article
            WHERE   article_id = {aid}
        """
        cursor.execute(SELECT_PWD)
        article_pwd = cursor.fetchall()[0][0]
        cursor.close()

        return pwd == article_pwd
    except Exception as e:
        cursor.close()

        return False


def isExistUser(uid: str=None, nickname: str=None):
    """
    ### 존재하는 회원 id인지 확인
    회원 전용
    """
    try:
        cursor = conn.cursor()

        # uid 또는 nickname에 해당하는 유저가 있는지
        SELECT_USER = f"""
            SELECT  *
            FROM    user
            WHERE   """

        if not uid is None and not nickname is None:
            # uid과 nickname에 해당하는 유저가 있는지
            SELECT_USER += f"user_id = '{uid}' or nickname = '{nickname}'"
        elif not uid is None:
            # uid에 해당하는 유저가 있는지
            SELECT_USER += f"user_id = '{uid}'"
        elif not nickname is None:
            # nickname에 해당하는 유저가 있는지
            SELECT_USER += f"nickname = '{nickname}'"
        cursor.execute(SELECT_USER)
        res = cursor.fetchall()
        cursor.close()

        if res:
            return True
        else:
            return False

    except Exception as e:
        cursor.close()

        return False


def isCorrectPWD(uid: str, pwd: int) -> bool:
    """
    ### 회원 비밀번호와 입력된 비밀번호가 같은지 확인
    회원 전용
    """
    try:
        cursor = conn.cursor()

        # 유저 비밀번호 획득
        SELECT_USER_PWD = f"""
            SELECT  password
            FROM    user
            WHERE   user_id = '{uid}'
        """
        cursor.execute(SELECT_USER_PWD)
        user_pwd = cursor.fetchall()[0][0]
        cursor.close()

        return pwd == user_pwd
    except Exception as e:
        cursor.close()

        raise False


def isSessionUser(uid: str) -> bool:
    """
    ### 요청한 유저가 세션 유저와 동일한 유저인지
    회원 전용
    """
    return session.get('uid') == uid


def isLogin() -> bool:
    """
    ### 로그인 된 상태인지
    회원 전용
    """
    return session.get('uid')


def isCorrectPWDForm(pwd: str) -> bool:
    """
    ### 올바른 비밀번호 형식인지 확인

    * 5 글자 이상, 16 글자 이하
    * 영어와 숫자, 일부 특수문자만 가능
    * 허용된 특수문자 = ['!', '@', '#', '$', '%', '^', '&']
    * 공백 불가
    """
    # 길이 검사
    if len(pwd) < 5 or len(pwd) > 16:
        return False
    
    # 영어, 숫자, 특문, 공백 검사
    if not re.match('^[\w!@#$%^&*]+$', pwd):
        return False
    
    return True


def isCorrectUidForm(uid: str) -> bool:
    """
    ### 올바른 아이디 형식인지 확인
    
    * 5 글자 이상, 16 글자 이하
    * 영어와 숫자만 가능
    * 특수문자 불가능
    * 공백 불가
    """
    # 길이 검사
    if len(uid) < 5 or len(uid) > 16:
        return False
    
    # 영어, 숫자, 특문, 공백 검사
    if not uid.isalnum:
        return False

    return True


def isCorrectNicknameForm(nickname) -> bool:
    """
    ### 올바른 닉네임 형식인지 확인
    * 2 글자 이상, 10 글자 이하
    * 영어와 숫자만 가능
    * 공백 불가
    * ', " 사용 볼가
    """
    # 길이 검사
    if len(nickname) < 2 or len(nickname) > 16:
        return False
    
    # 공백, 특수문자 검사
    if re.findall('[\s\'\"]+', nickname):
        return False
    
    return True


def getNickname(uid: str) -> bool:
    """
    ### 회원의 닉네임을 가져옴
    회원 전용
    """
    try:
        cursor = conn.cursor()

        # 유저 비밀번호 획득
        SELECT_USER_NICKNAME = f"""
            SELECT  nickname
            FROM    user
            WHERE   user_id = '{uid}'
        """
        cursor.execute(SELECT_USER_NICKNAME)
        nickname = escape(cursor.fetchall()[0][0])
        cursor.close()

        return nickname
    except Exception as e:
        cursor.close()

        raise Exception('DB 확인 에러!')


def getSHA256(item: str) -> str:
    """
    ### SHA256 암호화
    """
    return hashlib.sha256(item.encode()).hexdigest()


def makeReturnDict(result: bool, msg: str, data=None) -> dict:
    """
    ### json 통신을 위한 dict 만듬
    """
    if not data is None:
        return {"result": result, "msg": msg, "data": data}
    else:
        return {"result": result, "msg": msg}


##############
## 회원 가입 페이지
##############
@app.route('/member/join')
def memberJoin():
    return render_template('member_join.html'), 200


##############
## 회원 가입 요청
##############
@app.route('/member/join/request', methods=['POST'])
def memberJoinRequest():
    try:
        request_uid = request.form['uid']
        request_pwd = request.form['pwd']
        request_nickname = request.form['nickname']
    except Exception as e:
        return makeReturnDict(False, '잘못된 리퀘스트입니다.'), 400

    if isExistUser(uid=request_uid):
        return makeReturnDict(False, '이미 존재하는 아이디입니다.', 0), 200

    if isExistUser(nickname=request_nickname):
        return makeReturnDict(False, '이미 존재하는 닉네임입니다.', 2), 200

    if isLogin():
        return makeReturnDict(False, '로그인한 유저는 할 수 없는 작업입니다.'), 400

    if not isCorrectUidForm(request_uid):
        return makeReturnDict(False, '올바르지 않은 아이디 형식입니다.', 0), 400
    
    if not isCorrectPWDForm(request_pwd):
        return makeReturnDict(False, '올바르지 않은 비밀번호 형식입니다.', 1), 400

    if not isCorrectNicknameForm(request_nickname):
        return makeReturnDict(False, '올바르지 않은 닉네임 형식입니다.', 2), 400

    request_pwd = getSHA256(request_pwd)

    try:
        cursor = conn.cursor()

        INSERT_USER = """
            INSERT INTO user (
                user_id,
                password,
                nickname
            ) VALUES (
                ?,
                ?,
                ?
            )
        """
        cursor.execute(INSERT_USER, (request_uid, request_pwd, request_nickname))
        cursor.close()
        conn.commit()

        return makeReturnDict(True, '회원가입 성공'), 200
    except Exception as e:
        cursor.close()
        conn.rollback()

        return makeReturnDict(False, '서버에서 에러가 발생했습니다.'), 500


##############
## 로그인 페이지
##############
@app.route('/member/login')
def memberLogin():
    return render_template('member_login.html'), 200


##############
## 로그인 요청
##############
@app.route('/member/login/request', methods=['POST'])
def memberLoginRequest():
    try:
        request_uid = request.form['uid']
        request_pwd = request.form['pwd']
    except Exception as e:
        return makeReturnDict(False, '잘못된 리퀘스트입니다.'), 400

    # 존재하는 않는 유저
    if not isExistUser(request_uid):
        return makeReturnDict(False, '존재하지 않는 유저입니다.', 0), 200

    if isLogin():
        return makeReturnDict(False, '로그인 된 유저는 할 수 없는 작업입니다.'), 400

    request_pwd = getSHA256(request_pwd)

    # 비밀번호가 일치하는지
    if isCorrectPWD(request_uid, request_pwd):
        # 세션에 유저 추가
        session['uid'] = request_uid
        session['nickname'] = getNickname(request_uid)

        return makeReturnDict(True, f"{session.get('nickname')}님 반갑습니다."), 200
    else:
        return makeReturnDict(False, '비밀번호가 일치하지 않습니다.', 1), 200


##############
## 로그아웃 페이지
##############
@app.route('/member/logout/request', methods=["POST"])
def memberLogout():
    if not isLogin():
        return makeReturnDict(False, '잘못된 리퀘스트입니다.'), 400
    
    try:
        # 세션 나가기
        session.pop("uid", None)
        session.pop("nickname", None)
        return makeReturnDict(True, '로그아웃 성공'), 200
    except Exception as e:
        return makeReturnDict(False, '서버에서 에러가 발생했습니다.'), 500


##############
## 회원 정보 수정 페이지
##############
@app.route('/member/update')
def memberUpdate():
    return render_template('member_update.html'), 200


##############
## 회원 정보 수정 요청
##############
@app.route('/member/update/request', methods=["POST"])
def memberUpdateRequest():
    try:
        request_uid = request.form['uid']
        request_pwd = request.form['pwd']
        request_new_pwd = request.form.get('new_pwd', default=False)
        request_new_nickname = request.form.get('new_nickname', default=False)
    except Exception as e:
        return makeReturnDict(False, '잘못된 리퀘스트입니다.'), 400

    if not isLogin():
        return makeReturnDict(False, '로그인이 필요한 작업입니다'), 400

    if not isSessionUser(request_uid):
        return makeReturnDict(False, '세션과 정보가 동일하지 않습니다.'),400

    if not isExistUser(request_uid):
        return makeReturnDict(False, '존재하지 않는 유저입니다.'), 400

    if isExistUser(nickname=request_new_nickname):
        return makeReturnDict(False, '이미 존재하는 닉네임입니다.', 2), 400

    if request_new_pwd:
        if not isCorrectPWDForm(request_new_pwd):
            return makeReturnDict(False, '올바르지 않은 비밀번호 형식입니다.', 1), 400

    if request_new_nickname:
        if not isCorrectNicknameForm(request_new_nickname):
            return makeReturnDict(False, '올바르지 않은 닉네임 형식입니다.', 2), 400

    request_pwd = getSHA256(request_pwd)

    # 비밀번호 확인
    if not isCorrectPWD(request_uid, request_pwd):
        return makeReturnDict(False, '비밀번호가 일치하지 않습니다.', 0), 400

    try:
        cursor = conn.cursor()

        if request_new_pwd and request_new_nickname:
            request_new_pwd = getSHA256(request_new_pwd)
            set_query = f"password='{request_new_pwd}', nickname='{request_new_nickname}'"
        elif request_new_pwd:
            request_new_pwd = getSHA256(request_new_pwd)
            set_query = f"password='{request_new_pwd}'"
        elif request_new_nickname:
            set_query = f"nickname='{request_new_nickname}'"
        else:
            return makeReturnDict(False, '변경할 값을 전달받지 못했습니다.'), 500

        # 유저 정보 업데이트
        UPDATE_USER = f"""
            UPDATE  user
            SET     {set_query}
            WHERE   user_id='{request_uid}'
        """
        cursor.execute(UPDATE_USER)
        cursor.close()
        conn.commit()

        if request_new_nickname:
            session['nickname'] = getNickname(request_uid)

        return makeReturnDict(True, "정보수정 완료"), 200
    except Exception as e:
        cursor.close()
        conn.rollback()

        return makeReturnDict(False, "서버에서 에러가 발생했습니다."), 500


##############
## 회원 탈퇴 페이지
##############
@app.route('/member/delete')
def memberDelete():
    return render_template('member_delete.html'), 200


##############
## 회원 탈퇴 요청
##############
@app.route('/member/delete/request', methods=["POST"])
def memberDeleteeRequest():
    try:
        request_uid = request.form['uid']
        request_pwd = request.form['pwd']
        request_confirm = request.form['confirm']
    except Exception as e:
        return makeReturnDict(False, '잘못된 리퀘스트입니다.'), 400

    if request_confirm != '탈퇴합니다':
        return makeReturnDict(False, '확인 메시지가 잘 못 되었습니다.'), 400

    if not isLogin():
        return makeReturnDict(False, '로그인된 유저만 할 수 있는 작업입니다.'), 400

    if not isExistUser(request_uid):
        return makeReturnDict(False, '존재하지 않는 유저입니다.'), 400

    if not isSessionUser(request_uid):
        return makeReturnDict(False, '세션과 정보가 동일하지 않습니다.'),400
    
    # 비밀번호 확인
    if isCorrectPWD(request_uid, request_pwd):
        return makeReturnDict(False, '비밀번호가 일치하지 않습니다.'), 400

    try:
        cursor = conn.cursor()

        DELETE_USER = f"""
            DELETE  
            FROM    user
            WHERE   user_id='{request_uid}'
        """
        cursor.execute(DELETE_USER)
        cursor.close()
        conn.commit()

        memberLogout()

        return makeReturnDict(True, "탈퇴 성공"), 200
    except Exception as e:
        cursor.close()
        conn.rollback()

        return makeReturnDict(False, "서버에서 에러가 발생했습니다."), 500


##############
## 게시글 추천 요청
## return : dict
##############
@app.route('/article/hit',  methods=['POST'])
def articleHit():
    try:
        uid = request.form['uid']
        aid = request.form['aid']
    except Exception as e:
        return makeReturnDict(False, '잘못된 리퀘스트입니다.'), 400
    
    if not isLogin():
        return makeReturnDict(False, '로그인이 필요한 작업입니다.'),400

    if not isSessionUser(uid):
        return makeReturnDict(False, '세션과 정보가 동일하지 않습니다.'),400

    if not isExistUser(uid):
        return makeReturnDict(False, '존재하지 않는 유저입니다.'), 400

    try:
        cursor = conn.cursor()

        # 추천했던 유저인지 확인
        SELECT_HIT_HISTORY = f"""
            SELECT  *
            FROM    hit_history
            WHERE   article_id={aid} and user_id='{uid}';
        """
        cursor.execute(SELECT_HIT_HISTORY)
        res = cursor.fetchall()

        if res:
            return makeReturnDict(False, '추천은 게시물당 1번만 할 수 있습니다.'), 200

        # 추천 기록 추가
        INSERT_HIT_USER = """
            INSERT INTO hit_history (
                article_id,
                user_id
            ) VALUES (
                ?,
                ?
            )
        """
        cursor.execute(INSERT_HIT_USER, (aid, uid))

        # 추천수 증가
        UPDATE_ARTICLE_HIT = f"""
            UPDATE  article
            SET     hit = hit + 1
            WHERE   article_id={aid};
        """
        cursor.execute(UPDATE_ARTICLE_HIT)

        # 추천수 반환
        SELECT_ARTICLE_HIT = f"""
            SELECT  hit
            FROM    article
            WHERE   article_id={aid};
        """
        cursor.execute(SELECT_ARTICLE_HIT)
        hit = cursor.fetchall()[0][0]
        cursor.close()
        conn.commit()

        return makeReturnDict(True, '추천 성공', hit), 200
    except Exception as e:
        cursor.close()
        conn.rollback()

        return makeReturnDict(False, '서버에서 에러가 발생했습니다.'), 500


##############
## aid에 해당하는 댓글 정보 반환
##############
def selectComment(cursor, aid, uid, board):
    try:
        SELECT_ARTICLE_WRITER = f"""
            SELECT  user_id
            FROM    article
            WHERE   article_id={aid}
        """
        cursor.execute(SELECT_ARTICLE_WRITER)
        writer = cursor.fetchall()[0][0]

        # 댓글 정보 반환
        SELECT_COMMENTS = f"""
            SELECT  comment_id, nickname, comment, comment_time, user.user_id
            FROM    comment left join user
                    on comment.user_id = user.user_id
            WHERE   article_id={aid}
            ORDER BY comment_id ASC;
        """
        cursor.execute(SELECT_COMMENTS)
        comments = cursor.fetchall()

        if board == 'anonymous':
            for idx, comment in enumerate(comments):
                comment = list(comment)
                if writer == comment[4]:
                    comment[1] = "작성자"
                else:
                    comment[1] = "익명"
                comments[idx] = tuple(comment)
        
        for idx, comment in enumerate(comments):
            comment = list(comment)
            if uid == comment[4]:
                comment[4] = True
            else:
                comment[4] = False
            comments[idx] = tuple(comment)

        return comments
    except Exception as e:
        raise e


##############
## 댓글 작성 요청
##############
@app.route('/comment/write', methods=['POST'])
def commentCreateCall():
    try:
        print(request.form)
        aid = request.form['aid']
        request_uid = request.form['uid']
        comment = request.form['input_comment']
        board = request.form['board']
    except Exception as e:
        return makeReturnDict(False, '잘못된 리퀘스트입니다.'), 400
    
    if len(comment) == 0:
        return makeReturnDict(False, '댓글을 작성해 주세요.'), 400 

    if not isLogin():
        return makeReturnDict(False, '로그인이 필요한 작업입니다.'), 400

    if not isSessionUser(request_uid):
        return makeReturnDict(False, '세션과 정보가 동일하지 않습니다.'),400

    if not isExistUser(request_uid):
        return makeReturnDict(False, '존재하지 않는 유저입니다.'), 400

    try:
        cursor = conn.cursor()

        # 댓글 정보 추가
        INSERT_COMMENT = """
            INSERT INTO comment (
                article_id,
                user_id,
                comment
            ) VALUES (
                ?,
                ?,
                ?
            )
        """
        cursor.execute(INSERT_COMMENT, (aid, request_uid, comment))

        comments = selectComment(cursor, aid, request_uid, board)

        cursor.close()
        conn.commit()

        return makeReturnDict(True, '댓글작성 성공.', comments), 200
    except Exception as e:
        cursor.close()
        conn.rollback()

        return makeReturnDict(False, '서버에서 에러가 발생했습니다.'), 500
    

##############
## 댓글 삭제 요청
##############
@app.route('/comment/delete', methods=['POST'])
def commentDeleteCall():
    try:
        print(request.form)
        cid = request.form['cid']
        aid = request.form['aid']
        request_uid = request.form['uid']
        board = request.form['board']
    except Exception as e:
        return makeReturnDict(False, '잘못된 리퀘스트입니다.'), 400

    if not isLogin():
        return makeReturnDict(False, '로그인이 필요한 작업입니다.'), 400

    if not isSessionUser(request_uid):
        return makeReturnDict(False, '세션과 정보가 동일하지 않습니다.'),400

    if not isExistUser(request_uid):
        return makeReturnDict(False, '존재하지 않는 유저입니다.'), 400

    try:
        cursor = conn.cursor()
        
        # 댓글 작성자 가져오기
        SELECT_COMMENT_WRITER = f"""
            SELECT  user_id
            FROM    comment
            WHERE   comment_id={cid}
        """
        cursor.execute(SELECT_COMMENT_WRITER)
        writer = cursor.fetchall()[0][0]

        if writer != request_uid:
            return makeReturnDict(False, '작성자와 일치하지 않습니다.'), 400

        # 댓글 삭제
        DELETE_COMMENT = f"""
            DELETE   
            FROM    comment
            WHERE   comment_id={cid}
        """
        cursor.execute(DELETE_COMMENT)

        comments = selectComment(cursor, aid, request_uid, board)

        cursor.close()
        conn.commit()

        return makeReturnDict(True, '댓글삭제 성공.', comments), 200
    except Exception as e:
        cursor.close()
        conn.rollback()

        return makeReturnDict(False, '서버에서 에러가 발생했습니다.'), 500


##############
## 글 작성 페이지
##############
@app.route('/board/write')
def articleCreate():
    try:
        board = request.args.get('board', type=str)
    except Exception as e:
        return errorPage(2)

    if isNotAllowBoard(board):
        return errorPage(0)

    if not isLogin():
        return errorPage(4)

    # 글 작성 페이지
    return render_template('article_write.html', board=board, board_name=BOARD_DICT[board]), 200


##############
## 이미지 업로드 처리
##############
@app.route('/board/<board>/image-upload',  methods=['POST'])
def imageUploadCall(board):
    try:
        image = request.files['upload']
    except Exception as e:
        return {"uploaded": False, "url": False}, 400

    if isNotAllowBoard(board):
        return {"uploaded": False, "url": False}, 400

    try:
        cursor = conn.cursor()

        image_file_name = pathlib.Path(image.filename).name
        extension = pathlib.Path(image_file_name).suffix

        INSERT_IMAGE_FILE = """
            INSERT INTO image_files (
                file_name,
                file_type
            ) VALUES (
                ?,
                ?
            )
        """
        cursor.execute(INSERT_IMAGE_FILE, (image_file_name, extension))
        image_id = cursor.lastrowid
        SAVE_PATH = f"static/image/{board}/{board}-{image_id}{extension}"
        image.save(SAVE_PATH)

        cursor.close()
        conn.commit()

        return {"uploaded": True, "url": "/" + SAVE_PATH}, 200
    except Exception as e:
        cursor.close()
        conn.rollback()
        return {"uploaded": False, "url": False}, 400


##############
## 글 작성 요청
##############
@app.route('/board/write_submit',  methods=['POST'])
def articleCreateCall():
    try:
        uid = request.form['uid']
        board = request.form['board']
        title = request.form['title']
        content = request.form['content']
    except Exception as e:
        return errorPage(2)

    if len(title) == 0:
        return errorPage(msg="제목을 전달받지 못했습니다.")
    
    if len(content) == 0:
        return errorPage(msg="내용을 전달받지 못했습니다.")

    if not isLogin():
        return errorPage(4)
    
    if not isSessionUser(uid):
        return errorPage(5)

    if not isExistUser(uid):
        return errorPage(2)

    try:
        cursor = conn.cursor()

        INSERT_ARTICLE = """
            INSERT INTO article (
                user_id,
                board,
                title,
                content
            ) VALUES (
                ?,
                ?,
                ?,
                ?
            )
        """
        cursor.execute(INSERT_ARTICLE, (uid, board, title, content))

        cursor.close()
        conn.commit()

        return redirect(url_for('board', board=board))
    except Exception as e:
        cursor.close()
        conn.rollback()

        return errorPage(1)
    

##############
## 글 목록 가져오기
##############
def getArticles(cursor, board, page, art_per_page, option, keyword):
    try:
        SELECT_BOARD_COUNT = f"""
            SELECT  count(article_id)
            FROM    article
            WHERE   board='{board}';
        """
        cursor.execute(SELECT_BOARD_COUNT)
        a_cnt = cursor.fetchall()[0][0]         # 글의 수
        p_cnt = math.ceil(a_cnt / art_per_page)  # 전체 페이지 개수

        SELECT_ARTICLE = boardQueryBuilder(board, option, keyword)
        cursor.execute(SELECT_ARTICLE)
        articles = cursor.fetchall()

        tmp = (page - 1) * art_per_page
        articles = articles[tmp:min(tmp + art_per_page, a_cnt)]
        start = (page // 10) * 10 + 1
        end = min((page // 10 + 1) * 10, p_cnt) + 1

        return articles, start, end

    except Exception as e:
        raise Exception('요청 처리 중 에러가 발생했습니다.')


##############
## 글 페이지
##############
@app.route('/board/view', methods=['GET'])
def acrticlePage():
    try:
        board = request.args.get('board', type=str)
        aid = request.args.get('aid', type=int)
        page = request.args.get('page', type=int, default=1)          # 현재 페이지
        art_per_page = request.args.get('art_per_page', type=int, default=30)     # 페이지 당 글 개수
        option = request.args.get('option', type=str, default='all')
        keyword = request.args.get('keyword', type=str, default='')
    except Exception as e:
        return errorPage(2)

    if isNotAllowBoard(board):
        return errorPage(0)

    try:
        cursor = conn.cursor()

        # 조회수 증가
        UPDATE_ARTICLE_VIEW = f"""
            UPDATE  article
            SET     view = view + 1
            WHERE   article_id={aid};
        """
        cursor.execute(UPDATE_ARTICLE_VIEW)

        # 게시물 정보 반환
        SELECT_ARTICLE= f"""
            SELECT  distinct article.user_id, nickname, article_time, title, content, view, hit
            FROM    article left join comment
                    on article.article_id = comment.article_id
                    left join user
                    on article.user_id = user.user_id
            WHERE   article.article_id = {aid};
        """
        cursor.execute(SELECT_ARTICLE)
        article = cursor.fetchall()[0]

        # 댓글 정보 반환
        comments = selectComment(cursor, aid, session.get('uid'), board)

        articles, start, end = getArticles(cursor, board, page, art_per_page, option, keyword)
        isSearch = option != 'all'
        
        cursor.close()
        conn.commit()

        # 글 보기
        return render_template('article_page.html', board=board, board_name=BOARD_DICT[board],
        aid=aid, article=article, comments=comments, articles=articles, medias=False,
        page=page, start=start, end=end, isSearch=isSearch, option=option, keyword=keyword), 200
    except Exception as e:
        cursor.close()
        conn.rollback()

        return errorPage(1)


##############
## 유저 체크 페이지
## 비회원 게시판 전용 비밀번호 검문 페이지
##############
@app.route('/board/anonymous_check')
def anonymousCheck():
    try:
        board = request.args.get('board', type=str)
        uid = request.args.get('uid', type=str)
        aid = request.args.get('aid', type=int)
        check_type = request.args.get('check_type', type=str)

        return render_template('anonymous_check.html', board=board, board_name=BOARD_DICT[board], 
        uid=uid, aid=aid, check_type=check_type), 200
    except Exception as e:
        return errorPage(2)


##############
## 글 수정 페이지
##############
@app.route('/board/update', methods=['POST'])
def acrticleUpdate():
    try:
        board = request.args.get('board', type=str)

        request_uid = request.form['uid']
        aid = request.form['aid']
    except Exception as e:
        return errorPage(2)

    if isNotAllowBoard(board):
        return errorPage(0)

    if not isLogin():
        return errorPage(3)

    if not isSessionUser(request_uid):
        return errorPage()

    if not isExistUser(request_uid):
        return errorPage(2)

    try:
        cursor = conn.cursor()

        # 게시물 정보 획득 획득
        SELECT_ARTICLE_INFO = f"""
            SELECT  title, content, user_id
            FROM    article
            WHERE   article_id = {aid};
        """
        cursor.execute(SELECT_ARTICLE_INFO)
        title, content, user_id = cursor.fetchall()[0]

        if user_id != request_uid:
            return errorPage(3)

        cursor.close()

        return render_template('article_update.html', board=board, board_name=BOARD_DICT[board], 
        aid=aid, title=title, content=content), 200
    except Exception as e:
        cursor.close()

        return errorPage(1)


##############
## 글 수정 요청
##############
@app.route('/board/update_submit', methods=['POST'])
def acrticleUpdateCall():
    # 글 수정
    try:
        board = request.args.get('board', type=str)

        request_uid = request.form['uid']
        aid = request.form['aid']
        title = request.form['title']
        content = request.form['content']
    except:
        return errorPage(2)

    if len(title) == 0:
        return errorPage(msg="제목을 전달받지 못했습니다.")
    
    if len(content) == 0:
        return errorPage(msg="내용을 전달받지 못했습니다.")

    if isNotAllowBoard(board):
        return errorPage(0)

    if not isLogin():
        return errorPage(3)

    if not isSessionUser(request_uid):
        return errorPage(5)

    if not isExistUser(request_uid):
        return errorPage(2)
    
    try:
        cursor = conn.cursor()

        # 회원은 아이디만으로도 글을 수정할 수 있다.
        SELECT_ARTICLE_WRITER = f"""
            SELECT  user_id
            FROM    article
            WHERE   article_id = {aid};
        """
        cursor.execute(SELECT_ARTICLE_WRITER)
        writer = cursor.fetchall()[0][0]

        if writer != request_uid:
            return errorPage(2)

        # 회원용 게시물 수정
        UPDATE_ARTICLE = f"""
            UPDATE article
            SET title = '{title}',
                content = '{content}'
            WHERE article_id = '{aid}'
            """

        cursor.execute(UPDATE_ARTICLE)
        cursor.close()
        conn.commit()

        return redirect(url_for('board', board=board))
    except Exception as e:
        cursor.close()
        conn.rollback()

        return errorPage(1)


##############
## 글 삭제 페이지
##############
@app.route('/board/delete', methods=['POST'])
def articleDalete():
    try:
        board = request.args.get('board', type=str)
        
        request_uid = request.form['uid']     # 삭제 요청자
        aid = request.form['aid']
    except Exception as e:
        return errorPage(2)

    if isNotAllowBoard(board):
        return errorPage(0)

    if not isLogin():
        return errorPage(4)

    if not isSessionUser(request_uid):
        return errorPage(5)

    if not isExistUser(request_uid):
        return errorPage(2)

    # 글 삭제
    try:
        cursor = conn.cursor()

        SELECT_ARTICLE_WRITER = f"""
            SELECT  user_id
            FROM    article
            WHERE   article_id = {aid};
        """
        cursor.execute(SELECT_ARTICLE_WRITER)
        writer = cursor.fetchall()[0][0]

        if writer != request_uid:
            return errorPage(2)

        DELETE_ARTIECLE = f"""
            DELETE
            FROM article
            WHERE article_id = {aid};
        """

        cursor.execute(DELETE_ARTIECLE)
        cursor.close()
        conn.commit()

        return redirect(url_for('articleDaleteDone', board=board))
    except Exception as e:
        cursor.close()
        conn.rollback()

        return errorPage(1)


##############
## 글 삭제 완료 페이지
##############
@app.route('/board/delete_submit')
def articleDaleteDone():
    try:
        board = request.args.get('board', type=str)
    except Exception as e:
        return errorPage(2)

    if isNotAllowBoard(board):
        return errorPage(0)

    # 삭제 완료 페이지, 2 초후 게시판으로 이동함
    return render_template(f'article_delete.html', board=board, board_name=BOARD_DICT[board]), 200


##############
## 게시판 페이지
##############
@app.route('/board/articles', methods=["GET"])
def board():
    try:
        board = request.args.get('board', type=str)
        page = request.args.get('page', type=int, default=1)          # 현재 페이지
        art_per_page = request.args.get('art_per_page', type=int, default=30)     # 페이지 당 글 개수
        option = request.args.get('option', type=str, default='all')
        keyword = request.args.get('keyword', type=str, default='')
    except Exception as e:
        return errorPage(2)

    if isNotAllowBoard(board):
        return errorPage(0)

    try:
        cursor = conn.cursor()
        articles, start, end = getArticles(cursor, board, page, art_per_page, option, keyword)
        isSearch = option != 'all'
        cursor.close()

        # 게시판 페이지, db에서 가져온 정보
        return render_template(f'board_page.html', board=board, board_name=BOARD_DICT[board], 
        aid=False, articles=articles, page=page, start=start, end=end, isSearch=isSearch,
        option=option, keyword=keyword), 200
    except Exception as e:
        cursor.close()

        return errorPage(1)



##############
## 게시판 페이지에 사용할 SQL 쿼리
##############
def boardQueryBuilder(board, option, keyword)->str:
    try:
        query = f"""
            SELECT  article.article_id, nickname, title, article_time, view, hit, count(comment_id)
            FROM    article left join comment
                    on article.article_id = comment.article_id
                    left join user
                    on article.user_id = user.user_id
            WHERE   board='{board}'"""

        if option == 'title, content':
            query += f""" and (
            title like '%{keyword}%' ESCAPE '$' or
            content like '%{keyword}%' ESCAPE '$') """
        elif option == 'title':
            query += f""" and
            title like '%{keyword}%' ESCAPE '$'
            """
        elif option == 'content':
            query += f""" and
            content like '%{keyword}%' ESCAPE '$'
            """
        elif option == 'user':
            query += f""" and
            nickname like '%{keyword}%' ESCAPE '$'
            """
        
        query += """
        GROUP BY article.article_id
        ORDER BY article.article_id DESC;
        """

        return query
    except Exception as e:
        raise Exception("DB 확인 중 에러가 발생했습니다.")

##############
## 메인 페이지
##############
@app.route('/')
def main():
    return render_template('main.html', boards=BOARD_DICT), 200


@app.errorhandler(404)
def errorPage(signal: int=-1, msg=None) -> str:
    """
        ### 에러 페이지 함수
        
        ### In
        * signal (type: int, default: -1):
            0 = 존재하지 않는 게시판

            1 = DB 에러

            2 = request 에러

            3 = 아이디가 다름

            4 = 비회원 불가 작업

            5 = 세션 정보 불일치

            other = 잘못된 페이지

        ### Out
        * render_template('error_page.html', errMsg: 에러메시지)
    """
    if not msg is None:
        return render_template('error_page.html', errMsg=msg)
    elif signal == 0:
        return render_template('error_page.html', errMsg="존재하지 않는 게시판입니다.")
    elif signal == 1:
        return render_template('error_page.html', errMsg="DB 확인 중 문제가 발생했습니다.")
    elif signal == 2:
        return render_template('error_page.html', errMsg="잘못된 요청입니다.")
    elif signal == 3:
        return render_template('error_page.html', errMsg="작성자와 다른 유저입니다.")
    elif signal == 4:
        return render_template('error_page.html', errMsg="비회원은 할 수 없는 작업입니다.")
    elif signal == 5:
        return render_template('error_page.html', errMsg="세션과 정보가 동일하지 않습니다.")
    else:
        return render_template('error_page.html', errMsg="잘못된 페이지 입니다.")


def init():
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    cursor.close

if __name__ == '__main__':
    init()
    app.run(host='0.0.0.0', port=80, debug=True)
