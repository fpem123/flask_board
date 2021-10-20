# Flask, SQLite3 를 이용하여 만든 간단한 게시판입니다.

## 사용법

* 사용한 오픈소스 : [CKEditor5](https://ckeditor.com/ckeditor-5/download/)

* requirements : Flask, sqlite3

* create_table.py 먼저 실행하고 server.py 실행하기


---

## DONE

* 게시판 검색

* 에러 페이지

* 글 쓰기, 보기, 수정, 삭제, 추천

* 글 꾸미기 및 미디어 파일 첨부 -> ckeditor5 로 구현

* 게시물 페이지에선 ckeditor5을 읽기 전용으로 만들어 XSS 공격 방어

* 익명 게시판

* 댓글 쓰기, 삭제 (수정은 불가능)

* 회원가입, 로그인, 로그아웃, 정보수정, 탈퇴

* 아이디, 비밀번호 규칙 설정 (특정 특수문자, 영어, 숫자만)

* 닉네임 규칙 설정 (특정 특수문자 및 공백 불가)

* 비밀번호 저장시 암호화

---

## WORKING

* 중복 html코드들 frame화

* 리펙토링

* 웹에서 서버로 정보를 보낼 때 암호화 해서 보내도록

* 입력 길이 검사

---

## TO-DO

* CSS로 꾸미기

* 호스팅

---

## Maybe

* 댓글 답글?

* 비회원 게시판
