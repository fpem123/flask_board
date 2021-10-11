from flask import (Flask, request, render_template, 
                redirect, url_for, flash)
import math
import sqlite3

app = Flask(__name__)

BOARD_DICT = {'etc':'기타', 
    'game' : '게임'
    }

conn = sqlite3.connect("test.db", check_same_thread=False)
cursor = conn.cursor()


##############
## 허용되지 않은 게시판인지 확인
## return : boolean
##############
def isNotAllowBoard(board):
    return board not in BOARD_DICT


##############
## 글 작성 페이지
## return : 글 작성 페이지
##############
@app.route('/board/write')
def articleCreate():
    try:
        board = request.args.get('board', type=str)
    except Exception as e:
        print(e)

    if isNotAllowBoard(board):
        pass

    # 글 작성 페이지
    return render_template('article_write.html', board=board, board_name=BOARD_DICT[board]), 200


##############
## 글 작성 요청
## return : 결과 json
##############
@app.route('/board/write_submit',  methods=['POST'])
def articleCreateCall():
    try:
        # TO-DO : 전부 SQL 인젝션, 스크립트 공격 방어해야함
        board = request.form['board']
        title = request.form['title']
        content = request.form['content']
        uid = request.form['uid']
        pwd = request.form['pwd']
        # media_files = request.form['media_files']
    except:
        pass

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
        print(e)
    
    return redirect(url_for('board', board=board))


##############
## 글 검색 페이지
##############
@app.route('/board/<board>/search', methods=['GET'])
def articleSearch(board):
    if isNotAllowBoard(board):
        return 'none'
    
    print(request.args)

    # TO-DO : 글 검색 페이지
    return render_template(f'search_page.html', board=board), 200


##############
## 글 페이지
##############
@app.route('/board/view', methods=['GET'])
def acrticlePage():
    try:
        board = request.args.get('board', type=str)
        aid = request.args.get('aid', type=int)
    except Exception as e:
        print(e)

    if isNotAllowBoard(board):
        pass

    try:
        ARTICLE_SELECT = f"""
            SELECT  uid, date_time, title, content
            FROM    article
            WHERE   aid={aid};
        """
        cursor.execute(ARTICLE_SELECT)
        res = cursor.fetchall()[0]

    except Exception as e:
        print(e)

    # 글 보기
    return render_template('article_page.html', board=board, board_name=BOARD_DICT[board],
     uid=res[0], date=res[1], title=res[2], content=res[3], aid=aid), 200


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
        return 

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
        print(e)

    if isNotAllowBoard(board):
        pass

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
        return ""
    # TO-DO : 글 수정 페이지


##############
## 글 수정
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
        return False


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
        pass

    if isNotAllowBoard(board):
        pass

    if not isCollectPWD(pwd, aid):
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
        print(e)

        return 'error'


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
        print(e)

    if isNotAllowBoard(board):
        pass

    if not isCollectPWD(pwd, aid):
        return "block"

    # 글 삭제
    try:

        ARTIECLE_DELTE = f"""
            DELETE
            FROM article
            WHERE aid = {aid}
        """

        cursor.execute(ARTIECLE_DELTE)
        res = cursor.fetchall()
        print(res)
        conn.commit()
    except Exception as e:
        print(e)

    return redirect(url_for('articleDaleteDone', board=board))


##############
## 글 삭제 완료 페이지
##############
@app.route('/board/delete_submit')
def articleDaleteDone():
    try:
        board = request.args.get('board', type=str)
    except Exception as e:
        print(e)

    if isNotAllowBoard(board):
        # TO-DO : 없는 게시판 페이지
        return render_template('board_missing.html'), 200

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
    except Exception as e:
        print(e)

    if isNotAllowBoard(board):
        # TO-DO : 없는 게시판 페이지
        return render_template('board_missing.html'), 200

    try:
        BOARD_COUNT = f"""
            SELECT  count(aid)
            FROM    article
            WHERE   board='{board}';
        """
        cursor.execute(BOARD_COUNT)
        a_cnt = cursor.fetchall()[0][0]         # 글의 수
        p_cnt = math.ceil(a_cnt / art_per_page)  # 전체 페이지 개수
        print(p_cnt)

        ARTICLE_SELECT = f"""
            SELECT  aid, title, uid, date_time
            FROM    article
            WHERE   board='{board}'
            ORDER BY aid DESC;
        """
        cursor.execute(ARTICLE_SELECT)
        res = cursor.fetchall()
        tmp = (page - 1) * art_per_page
        res = res[tmp:min(tmp + art_per_page, a_cnt)]
        start = (page // 10) * 10 + 1
        end = min((page // 10 + 1) * 10, p_cnt) + 1

    except Exception as e:
        print(e)
        res = False

    # 게시판 페이지, db에서 가져온 정보
    return render_template(f'board_page.html', board=board, board_name=BOARD_DICT[board], 
    articles=res, page=page, start=start, end=end), 200


##############
## 메인 페이지
##############
@app.route('/')
def main():
    return render_template('main.html', boards=BOARD_DICT), 200


@app.errorhandler(404)
def errorPage():
    return render_template('not_found.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
