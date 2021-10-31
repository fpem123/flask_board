import sqlite3

class SquliteClass():
    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute('PRAGMA foreign_keys=ON;')
        cursor.close
        self.conn.commit()


    def insertQuery(self, query, data):
        """
            ### db에 데이터 추가

            * 입력

                query : 쿼리
                data : 추가할 데이터

            * 출력

                추가된 데이터의 id
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, data)
            result = cursor.lastrowid
            cursor.close()
            self.conn.commit()

            return result
        except Exception as e:
            cursor.close()
            self.conn.rollback()
            raise e


    def selectQuery(self, query, data):
        """
            ### db에 데이터 추가

            * 입력

                query : 쿼리
                data : 검색할 조건 데이터
                
            * 출력

                select 결과
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, data)
            result = cursor.fetchall()
            cursor.close()
            self.conn.commit()

            return result
        except Exception as e:
            print(e)
            cursor.close()
            raise e


    def updateQuery(self, query, data):
        """
            ### db에 데이터 추가

            * 입력

                query : 쿼리
                data : 수정할 데이터
                
            * 출력

                bool 성공여부
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, data)
            result = cursor.fetchall()
            cursor.close()
            self.conn.commit()

            return True
        except Exception as e:
            cursor.close()
            self.conn.rollback()
            raise e


    def deleteQuery(self, query, data):
        """
            ### db에 데이터 추가

            * 입력

                query : 쿼리
                data : 제거할 타겟 데이터

            * 출력

            bool 성공여부
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, data)
            result = cursor.fetchall()
            cursor.close()
            self.conn.commit()

            return True
        except Exception as e:
            cursor.close()
            self.conn.rollback()
            raise e
