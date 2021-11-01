# Flask, SQLite3 를 이용하여 만든 간단한 게시판입니다.

## 사용법

* 호스팅 : [pythonanywhere](http://hoseop.pythonanywhere.com/)

* 사용한 오픈소스 : [CKEditor5](https://ckeditor.com/ckeditor-5/download/)

* requirements : Flask, sqlite3, bs4

* create_table.py 먼저 실행하고 server.py 실행하기

* 프로토타입 : [OVEN](https://ovenapp.io/view/6xyc7AHTnkoAuw75yHj5af5yY7xJylTH/)

* 기본 프로필 사진 : [pixabay](https://pixabay.com/ko/vectors/%eb%b9%88-%ed%94%84%eb%a1%9c%ed%95%84-%ec%82%ac%ec%a7%84-%eb%af%b8%ec%8a%a4%ed%84%b0%eb%a6%ac-%eb%a7%a8-973460/)


---

## DONE

* 호스팅

* 게시판 검색

* 에러 페이지

* 글 쓰기, 보기, 수정, 삭제, 추천, 도배 방지 쿨타임 20초

* 글 꾸미기 및 미디어 파일 첨부 -> ckeditor5 로 구현

* 게시물 페이지에선 ckeditor5을 읽기 전용으로 만들어 XSS 공격 방어

* 익명 게시판

* 댓글 쓰기, 삭제 (수정은 불가능), 도배 방지 쿨타임 3초

* 회원가입, 로그인, 로그아웃, 정보수정, 탈퇴

* 아이디, 비밀번호 규칙 설정 (특정 특수문자, 영어, 숫자만)

* 닉네임 규칙 설정 (특정 특수문자 및 공백 불가)

* 비밀번호 저장시 암호화

* CSS

---

## WORKING

* 중복 html코드들 frame화

* 리펙토링

---

## TO-DO

---

## Maybe

* 댓글 답글?

* 비회원 게시판

* 모바일 페이지
