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

* 글에 미디어 파일 첨부 가능

* 익명 게시판

* 댓글 쓰기, 삭제 (수정은 불가능)

* 회원가입, 로그인, 로그아웃, 정보수정, 탈퇴

* 아이디, 비밀번호 규칙 설정 (특정 특수문자, 영어, 숫자만)

* 닉네임 규칙 설정 (특정 특수문자 및 공백 불가)

* 비밀번호 저장시 암호화

* html script들 모아서 하나의 javascript 로 만들기

---

## WORKING

* 중복 html코드들 frame화

* 리펙토링

* 글에 수정시 미디어 파일 바꿀 수 있게

* 글 꾸미기 기능 -> ckeditor5 사용

---

## TO-DO

* 추천, 댓글 작성시 조회수가 올라가는 문제 -> JS로 data를 보낸 뒤 성공했을 때 새로고침 말고 바로 바뀌게 해야할듯

---

## Maybe

* 댓글 답글?

* 비회원 게시판

