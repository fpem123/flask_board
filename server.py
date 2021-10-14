from os import SEEK_CUR
from flask import Flask
from flask import session, request
from flask import render_template, redirect, url_for, escape, flash
import math
import sqlite3

app = Flask(__name__)
app.secret_key = "1q2w3e4r!"

BOARD_DICT = {'etc':'기타', 
    'game' : '게임',
    'anonymous' : '익명',
    'no-member' : '비회원'
    }

conn = sqlite3.connect("test.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys=ON;')
conn.commit()


##############
## 허용되지 않은 게시판인지 확인
## return : boolean
##############
def isNotAllowBoard(board):
    return board not in BOARD_DICT


def isCollectArticlePWD(pwd: str, aid: int):
    """
    ### 글의 비밀번호와 입력된 비밀번호가 같은지 확인
    비회원 게시판 전용
    """
    try:
        # 게시물 비밀번호 획득
        SELECT_PWD = f"""
            SELECT  pwd
            FROM    article
            WHERE   aid = {aid}
        """
        cursor.execute(SELECT_PWD)

        return pwd == cursor.fetchall()[0][0]
    except Exception as e:
        raise Exception('DB 확인 에러!')


def isExistUser(uid: str, nickname: str = None):
    """
    ### 존재하는 회원 id인지 확인
    회원 전용
    """
    try:
        # uid에 해당하는 유저가 있는지
        SELECT_USER = f"""
            SELECT  *
            FROM    user
            WHERE   uid = '{uid}'
        """
        if not nickname is None:
            # uid에 해당하는 유저가 있는지
            SELECT_USER += f" or nickname = '{nickname}'"
        cursor.execute(SELECT_USER)
        return cursor.fetchall()
    except Exception as e:
        return False


def isCollectPWD(uid: str, pwd: int):
    """
    ### 회원 비밀번호와 입력된 비밀번호가 같은지 확인
    회원 전용
    """
    try:
        # 유저 비밀번호 획득
        SELECT_PWD = f"""
            SELECT  pwd
            FROM    user
            WHERE   uid = '{uid}'
        """
        cursor.execute(SELECT_PWD)

        return pwd == cursor.fetchall()[0][0]
    except Exception as e:
        raise Exception('DB 확인 에러!')


def isLogin():
    return session.get('uid')


def getNickname(uid: str):
    """
    ### 회원의 닉네임을 가져옴
    회원 전용
    """
    try:
        # 유저 비밀번호 획득
        SELECT_NICKNAME = f"""
            SELECT  nickname
            FROM    user
            WHERE   uid = '{uid}'
        """
        cursor.execute(SELECT_NICKNAME)

        return escape(cursor.fetchall()[0][0])
    except Exception as e:
        raise Exception('DB 확인 에러!')


@app.route('/clear')
def masterClear():
    session.clear()
    return 'Clear'


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
        print(request.form)
    except Exception as e:
        return {'result': False}, 400

    if isExistUser(request_uid, request_nickname):
        return {'result': False}, 200

    if isLogin():
        return {'result': False}, 400

    try:
        INSERT_USER = """
            INSERT INTO user (
                uid,
                pwd,
                nickname
            ) VALUES (
                ?,
                ?,
                ?
            )
        """
        cursor.execute(INSERT_USER, (request_uid, request_pwd, request_nickname))
        conn.commit()
        res = cursor.fetchall()
        print("회원가입완료")
        return {'result': True}, 200
    except Exception as e:
        return {'result': False}, 500


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
        return {'result': False}, 400

    # 존재하는 않는 유저
    if not isExistUser(request_uid):
        return {'result': False}, 200

    if isLogin():
        return {'result': False}, 400

    try:

        # 비밀번호가 일치하는지
        if isCollectPWD(request_uid, request_pwd):
            SELECT_USER_NICKNAME = f"""
                SELECT  nickname
                FROM    user
                WHERE   uid = '{request_uid}';
            """
            cursor.execute(SELECT_USER_NICKNAME)
            res = cursor.fetchall()[0][0]

            # 세션에 유저 추가
            session['uid'] = request_uid
            session['nickname'] = getNickname(request_uid)

            return {'result': True, 'nickname': res}, 200
        else:
            return {'result': False}, 200
    except Exception as e:
        return  {'result': False}, 500


##############
## 로그아웃 페이지
##############
@app.route('/member/logout/request', methods=["POST"])
def memberLogout():
    if not isLogin():
        return {'reuslt': False}, 400
    
    try:
        # 세션 나가기
        session.pop("uid", None)
        session.pop("nickname", None)
        return {'result': True}, 200
    except Exception as e:
        return {'result': False}, 500


##############
## 회원 정보 수정 페이지
##############
@app.route('/member/update')
def memberUpdate():
    # TO-DO : 비밀번호 검문 필요
    return render_template('member_update.html'), 200


##############
## 회원 탈퇴 요청
##############
@app.route('/member/secession')
def memberSecessione():
    # TO-DO : 비밀번호 검문 필요
    return {'result': True}, 200


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
        return {'result': False}, 400
    
    if not isExistUser(uid) or not isLogin():
        return {'result': False}, 400

    try:
        # 추천했던 유저인지 확인
        READ_HIT_HISTORY = f"""
            SELECT  *
            FROM    hit_history
            WHERE   aid={aid} and uid='{uid}';
        """
        cursor.execute(READ_HIT_HISTORY)
        res = cursor.fetchall()

        if res:
            return {'result': False}, 200

        # 추천 기록 추가
        INSERT_HIT_USER = """
            INSERT INTO hit_history (
                aid,
                uid
            ) VALUES (
                ?,
                ?
            )
        """
        cursor.execute(INSERT_HIT_USER, (aid, uid))
        res = cursor.fetchall()

        # 추천수 증가
        ARTICLE_HIT_UP = f"""
            UPDATE  article
            SET     hit = hit + 1
            WHERE   aid={aid};
        """
        cursor.execute(ARTICLE_HIT_UP)
        res = cursor.fetchall()
        conn.commit()

        # 추천수 반환
        READ_ARTICLE_HIT = f"""
            SELECT  hit
            FROM    article
            WHERE   aid={aid};
        """
        cursor.execute(READ_ARTICLE_HIT)
        res = cursor.fetchall()[0][0]

        return {'result': True, 'hit': res}, 200
    except Exception as e:
        return {'result': False}, 500


##############
## 댓글 작성 요청
##############
@app.route('/comment/write', methods=['POST'])
def commentCreateCall():
    try:
        # TO-DO : 전부 SQL 인젝션, 스크립트 공격 방어해야함
        aid = request.form['aid']
        request_uid = request.form['uid']
        comment = request.form['comment']
    except Exception as e:
        return {'result': False}, 400

    if not isLogin() or not isExistUser(request_uid):
        return {'result': False}, 400

    try:
        # 댓글 정보 추가
        INSERT_COMMENT = """
            INSERT INTO comment (
                aid,
                uid,
                comment
            ) VALUES (
                ?,
                ?,
                ?
            )
        """
        cursor.execute(INSERT_COMMENT, (aid, request_uid, comment))
        res = cursor.fetchall()
        conn.commit()

        return {'result': True}, 200
    except Exception as e:
        return {'result': False}, 500
    

##############
## 댓글 삭제 요청
##############
@app.route('/comment/delete', methods=['POST'])
def commentDeleteCall():
    try:
        # TO-DO : 전부 SQL 인젝션, 스크립트 공격 방어해야함
        cid = request.form['cid']
        request_uid = request.form['uid']
    except Exception as e:
        return {'result': False}, 400

    if not isLogin() or not isExistUser(request_uid):
        return {'result': False}, 400

    try:
        # 댓글 작성자 가져오기
        SELECT_COMMENT_WRITER = f"""
            SELECT  uid
            FROM    comment
            WHERE   cid={cid}
        """
        cursor.execute(SELECT_COMMENT_WRITER)
        writer = cursor.fetchall()[0][0]

        if writer != request_uid:
            return {'result': False}, 400

        # 댓글 삭제
        DELETE_COMMENT = f"""
            DELETE   
            FROM    comment
            WHERE   cid={cid}
        """
        cursor.execute(DELETE_COMMENT)
        res = cursor.fetchall()
        conn.commit()

        return {'result': True}, 200
    except Exception as e:
        return {'result': False}, 500


##############
## 글 작성 페이지
## return : 글 작성 페이지
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
## 글 작성 요청
## return : 결과 json
##############
@app.route('/board/write_submit',  methods=['POST'])
def articleCreateCall():
    try:
        uid = request.form['uid']
        board = request.form['board']
        title = request.form['title']
        content = request.form['content']
        #pwd = request.form['pwd']   # 비회원 게시판일 때만 사용하도록
        # media_files = request.form['media_files']
    except Exception as e:
        return errorPage(2)

    if not isExistUser(uid):
        return errorPage(2)

    if not isLogin():
        return errorPage(4)

    try:
        ARTICLE_INSERT = """
            INSERT INTO article (
                uid,
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
        cursor.execute(ARTICLE_INSERT, (uid, board, title, content))
        res = cursor.fetchall()
        conn.commit()

        return redirect(url_for('board', board=board))
    except Exception as e:
        return errorPage(1)
    

##############
## 글 페이지
##############
@app.route('/board/view', methods=['GET'])
def acrticlePage():
    try:
        board = request.args.get('board', type=str)
        aid = request.args.get('aid', type=int)
    except Exception as e:
        return errorPage(2)

    if isNotAllowBoard(board):
        return errorPage(0)

    try:
        # 조회수 증가
        VIEW_UP = f"""
            UPDATE  article
            SET     view = view + 1
            WHERE   aid={aid};
        """
        cursor.execute(VIEW_UP)
        conn.commit()

        # 게시물 정보 반환
        ARTICLE_SELECT = f"""
            SELECT  article.uid, article.date_time, title, content, view, hit
            FROM    article left join comment
                    on article.aid = comment.aid
            WHERE   article.aid={aid};
        """
        cursor.execute(ARTICLE_SELECT)
        article = cursor.fetchall()[0]

        # 댓글 정보 반환
        COMMENT_SELECT = f"""
            SELECT  cid, uid, comment, date_time
            FROM    comment
            WHERE   aid={aid}
            ORDER BY cid ASC;
        """
        cursor.execute(COMMENT_SELECT)
        comments = cursor.fetchall()
        conn.commit()

        # 글 보기
        return render_template('article_page.html', board=board, board_name=BOARD_DICT[board],
        aid=aid, article_uid=article[0], article_date=article[1], article_title=article[2], 
        article_content=article[3], article_view=article[4], article_hit=article[5], comments=comments), 200
    except Exception as e:
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

    if not isExistUser(request_uid):
        return errorPage(2)

    if not isLogin():
        return errorPage(3)

    try:
        # 게시물 정보 획득 획득
        SELECT_ARTICLE_INFO = f"""
            SELECT  title, content, uid
            FROM    article
            WHERE   aid = {aid};
        """
        cursor.execute(SELECT_ARTICLE_INFO)
        res = cursor.fetchall()[0]

        if res[2] != request_uid:
            return errorPage(3)

        return render_template('article_update.html', board=board, board_name=BOARD_DICT[board], 
        aid=aid, title=res[0], content=res[1]), 200
    except Exception as e:
        return errorPage(1)


##############
## 글 수정
##############
@app.route('/board/update_submit', methods=['POST'])
def acrticleUpdateCall():
    # 글 수정
    try:
        # TO-DO : 전부 SQL 인젝션, 스크립트 공격 방어해야함
        board = request.args.get('board', type=str)
        request_uid = request.form['uid']
        #pwd = request.form['pwd']
        #npwd = request.form['npwd']
        aid = request.form['aid']
        title = request.form['title']
        content = request.form['content']
    except:
        return errorPage(2)

    if isNotAllowBoard(board):
        return errorPage(0)

    if not isExistUser(request_uid):
        return errorPage(2)

    if not isLogin():
        return errorPage(3)

    try:
        # 회원은 아이디만으로도 글을 수정할 수 있다.
        SELECT_ARTICLE_WRITER = f"""
            SELECT  uid
            FROM    article
            WHERE   aid = {aid};
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
            WHERE aid = '{aid}'
            """

        cursor.execute(UPDATE_ARTICLE)
        res = cursor.fetchall()
        conn.commit()

        return redirect(url_for('board', board=board))
    except Exception as e:
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
        #pwd = request.form['pwd']
    except Exception as e:
        return errorPage(2)

    if isNotAllowBoard(board):
        return errorPage(0)

    if not isExistUser(request_uid):
        return errorPage(2)

    if not isLogin():
        return errorPage(4)

    # 글 삭제
    try:
        GET_ARTICLE_WRITER = f"""
            SELECT  uid
            FROM    article
            WHERE   aid = {aid};
        """
        cursor.execute(GET_ARTICLE_WRITER)
        writer = cursor.fetchall()[0][0]

        if writer != request_uid:
            # TO-DO : json을 보내도록 수정
            return errorPage(2)

        ARTIECLE_DELTE = f"""
            DELETE
            FROM article
            WHERE aid = {aid};
        """

        cursor.execute(ARTIECLE_DELTE)
        res = cursor.fetchall()
        conn.commit()

        return redirect(url_for('articleDaleteDone', board=board))
    except Exception as e:
        print(e)
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

    isSearch = option != 'all'

    try:
        BOARD_COUNT = f"""
            SELECT  count(aid)
            FROM    article
            WHERE   board='{board}';
        """
        cursor.execute(BOARD_COUNT)
        a_cnt = cursor.fetchall()[0][0]         # 글의 수
        p_cnt = math.ceil(a_cnt / art_per_page)  # 전체 페이지 개수

        ARTICLE_SELECT = boardQueryBuilder(board, option, keyword)
        cursor.execute(ARTICLE_SELECT)
        res = cursor.fetchall()

        tmp = (page - 1) * art_per_page
        res = res[tmp:min(tmp + art_per_page, a_cnt)]
        start = (page // 10) * 10 + 1
        end = min((page // 10 + 1) * 10, p_cnt) + 1
        conn.commit()

        # 게시판 페이지, db에서 가져온 정보
        return render_template(f'board_page.html', board=board, board_name=BOARD_DICT[board], 
        articles=res, page=page, start=start, end=end, isSearch=isSearch), 200
    except Exception as e:
        res = False



##############
## 게시판 페이지에 사용할 SQL 쿼리
##############
def boardQueryBuilder(board, option, keyword)->str:
    query = f"""
        SELECT  article.aid, article.uid, title, article.date_time, view, hit, count(cid)
        FROM    article left join comment
                on article.aid = comment.aid
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
    elif option == 'uid':
        query += f""" and
        article.uid like '%{keyword}%' ESCAPE '$'
        """
    
    query += """
    GROUP BY article.aid
    ORDER BY article.aid DESC;
    """

    return query


##############
## 메인 페이지
##############
@app.route('/')
def main():
    return render_template('main.html', boards=BOARD_DICT), 200



@app.errorhandler(404)
def errorPage(signal: int = -1) -> str:
    """
        ### 에러 페이지 함수
        
        ### In
        * signal (type: int, default: -1):
            0 = 존재하지 않는 게시판

            1 = DB 에러

            2 = request 에러

            3 = 아이디가 다름

            3 = 비회원 불가 작업

            other = 잘못된 페이지

        ### Out
        * render_template('error_page.html', errMsg: 에러메시지)
    """
    if signal == 0:
        return render_template('error_page.html', errMsg="존재하지 않는 게시판입니다.")
    elif signal == 1:
        return render_template('error_page.html', errMsg="DB 확인 중 문제가 발생했습니다.")
    elif signal == 2:
        return render_template('error_page.html', errMsg="잘못된 요청입니다.")
    elif signal == 3:
        return render_template('error_page.html', errMsg="작성자와 다른 유저입니다.")
    elif signal == 4:
        return render_template('error_page.html', errMsg="비회원은 할 수 없는 작업입니다.")
    else:
        return render_template('error_page.html', errMsg="잘못된 페이지 입니다.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
