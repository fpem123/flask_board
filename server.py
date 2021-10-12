from flask import (Flask, request, render_template, 
                redirect, url_for, flash, jsonify)
import math
import sqlite3

app = Flask(__name__)

BOARD_DICT = {'etc':'기타', 
    'game' : '게임'
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


##############
## 댓글 작성 요청
## return : 실패시 alert, 성공시 새로고침
##############
@app.route('/comment/write_submit',  methods=['POST'])
def commentCreateCall():
    try:
        # TO-DO : 전부 SQL 인젝션, 스크립트 공격 방어해야함
        aid = request.form['aid']
        uid = request.form['uid']
        pwd = request.form['pwd']
        comment = request.form['comment']
    except Exception as e:
        return {'result': False}, 400

    try:
        COMMENT_INSERT = """
            INSERT INTO comment (
                aid,
                uid,
                pwd,
                comment
            ) VALUES (
                ?,
                ?,
                ?,
                ?
            )
        """
        cursor.execute(COMMENT_INSERT, (aid, uid, pwd, comment))
        res = cursor.fetchall()
        conn.commit()
    except Exception as e:
        return {'result': False}, 500
    
    return {'result': True}, 200


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

    # 글 작성 페이지
    return render_template('article_write.html', board=board, board_name=BOARD_DICT[board]), 200


##############
## 글 작성 요청
## return : 결과 json
##############
@app.route('/board/write_submit',  methods=['POST'])
def articleCreateCall():
    try:
        board = request.form['board']
        title = request.form['title']
        content = request.form['content']
        uid = request.form['uid']
        pwd = request.form['pwd']
        # media_files = request.form['media_files']
    except:
        return errorPage(2)

    try:
        ARTICLE_INSERT = """
            INSERT INTO article (
                uid,
                pwd,
                board,
                title,
                content
            ) VALUES (
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """
        cursor.execute(ARTICLE_INSERT, (uid, pwd, board, title, content))
        res = cursor.fetchall()
        conn.commit()

    except Exception as e:
        return errorPage(1)
    
    return redirect(url_for('board', board=board))


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
        VIEW_UP = f"""
            UPDATE  article
            SET     view = view + 1
            WHERE   aid={aid};
        """
        cursor.execute(VIEW_UP)
        conn.commit()

        ARTICLE_SELECT = f"""
            SELECT  article.uid, article.date_time, title, content, view, hit, count()
            FROM    article left join comment
                    on article.aid = comment.aid
            WHERE   article.aid={aid};
        """
        cursor.execute(ARTICLE_SELECT)
        article = cursor.fetchall()[0]

        COMMENT_SELECT = f"""
            SELECT  cid, uid, comment, date_time
            FROM    comment
            WHERE   aid={aid}
            ORDER BY cid ASC;
        """
        cursor.execute(COMMENT_SELECT)
        comments = cursor.fetchall()
        conn.commit()
    except Exception as e:
        return errorPage(1)

    # 글 보기
    return render_template('article_page.html', board=board, board_name=BOARD_DICT[board],
     uid=article[0], date=article[1], title=article[2], content=article[3], view=article[4], hit=article[5], 
     num_comment=article[6], comments=comments, aid=aid), 200


##############
## 유저 체크 페이지
##############
@app.route('/board/check')
def userChect():
    try:
        board = request.args.get('board', type=str)
        uid = request.args.get('uid', type=str)
        aid = request.args.get('aid', type=int)
        check_type = request.args.get('check_type', type=str)
    except Exception as e:
        return errorPage(2)

    return render_template('user_check.html', board=board, board_name=BOARD_DICT[board], 
    uid=uid, aid=aid, check_type=check_type), 200


##############
## 글 수정 페이지
##############
@app.route('/board/update', methods=["POST"])
def acrticleUpdate():
    try:
        board = request.args.get('board', type=str)

        aid = request.form['aid']
        uid = request.form['uid']
        pwd = request.form['pwd']
    except Exception as e:
        return errorPage(2)

    if isNotAllowBoard(board):
        return errorPage(0)

    try:
        PWD_GET = f"""
            SELECT  pwd, title, content
            FROM    article
            WHERE   aid = {aid}
        """
        cursor.execute(PWD_GET)
        res = cursor.fetchall()[0]

        if pwd == res[0]:
            return render_template('article_update.html', board=board, board_name=BOARD_DICT[board], 
            uid=uid, pwd=pwd, aid=aid, title=res[1], content=res[2]), 200
        else:
            return "block"
    except Exception as e:
        return errorPage(1)


##############
## 글의 비밀번호와 같은지 확인
##############
def isCollectPWD(pwd, aid):
    try:
        PWD_GET = f"""
            SELECT  pwd
            FROM    article
            WHERE   aid = {aid}
        """
        cursor.execute(PWD_GET)

        return pwd == cursor.fetchall()[0][0]
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

        uid = request.form['uid']
        pwd = request.form['pwd']
        npwd = request.form['npwd']
        aid = request.form['aid']
        title = request.form['title']
        content = request.form['content']
    except:
        return errorPage(2)

    if isNotAllowBoard(board):
        return errorPage(0)

    if not isCollectPWD(pwd, aid):
        # TO-DO : alert 메시지 전송
        return "block"

    try:
        ARTICLE_UPDATE = f"""
            UPDATE article
            SET uid = '{uid}',
                pwd = '{npwd}',
                title = '{title}',
                content = '{content}'
            WHERE aid = '{aid}'
        """
        cursor.execute(ARTICLE_UPDATE)
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

        aid = request.form['aid']
        pwd = request.form['pwd']
    except Exception as e:
        return errorPage(2)

    if isNotAllowBoard(board):
        return errorPage(0)

    if not isCollectPWD(pwd, aid):
        # TO-DO : alert 메시지 전송
        return "block"

    # 글 삭제
    try:

        ARTIECLE_DELTE = f"""
            DELETE
            FROM article
            WHERE aid = {aid};
        """

        cursor.execute(ARTIECLE_DELTE)
        res = cursor.fetchall()
        conn.commit()
    except Exception as e:
        return errorPage(1)

    return redirect(url_for('articleDaleteDone', board=board))


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

    # TO-DO : 삭제 완료 페이지(meta 태그로 구현)
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
        
    except Exception as e:
        res = False

    # 게시판 페이지, db에서 가져온 정보
    return render_template(f'board_page.html', board=board, board_name=BOARD_DICT[board], 
    articles=res, page=page, start=start, end=end, isSearch=isSearch), 200


##############
## 게시판 페이지에 사용할 SQL 쿼리
##############
def boardQueryBuilder(board, option, keyword)->str:
    query = f"""
        SELECT  aid, title, uid, date_time, view, hit
        FROM    article
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
        uid like '%{keyword}%' ESCAPE '$'
        """
    
    query += """
    ORDER BY aid DESC;
    """

    return query


##############
## 메인 페이지
##############
@app.route('/')
def main():
    return render_template('main.html', boards=BOARD_DICT), 200


##############
## 에러 페이지
##############
@app.errorhandler(404)
def errorPage(signal=-1):
    #   0 = 잘못된 게시판
    #   1 = DB 에러
    #   2 = request 에러
    if signal == 0:
        return render_template('error_page.html', errMsg="존재하지 않는 게시판입니다.")
    elif signal == 1:
        return render_template('error_page.html', errMsg="DB 확인 중 문제가 발생했습니다.")
    elif signal == 2:
        return render_template('error_page.html', errMsg="잘못된 요청입니다.")
    else:
        return render_template('error_page.html', errMsg="잘못된 페이지 입니다.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
