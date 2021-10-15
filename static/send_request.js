// 엔터키 전송 방지
function onKeydownEnter(){
    if(event.keyCode==13) 

    return false
}

// 추천 리퀘스트
function sendHit(){
    let aid = document.getElementById( 'aid' ).value;
    let uid = document.getElementById( 'uid' ).value;

    if (uid === ''){
        alert("추천은 로그인한 유저만 가능합니다.");

        return;
    }

    const formData = new FormData();
    const url = '/article/hit';
    let signal = true;

    formData.append('aid', aid);
    formData.append('uid', uid);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if ([200, 400, 500].includes(response.status))
            return response.json()
        else{
            signal = false;
            alert("추천 실패");
        }
    }).catch(err => {
        if (signal){
            signal = false;
            alert("추천 실패");
        }
    }).then(result => {
        if (result['result'])
            window.location.reload(true);
        else if (signal){
            signal = false;
            alert(result['msg']);
        }
    });
}

// 댓글 작성 리퀘스트
function sendInsertComment() {
    let aid = document.getElementById( 'aid' ).value;
    let uid = document.getElementById( 'uid' ).value;
    let comment = document.getElementById( 'comment' ).value;

    const formData = new FormData();
    const url = '/comment/write';
    let signal = true;

    formData.append('aid', aid);
    formData.append('uid', uid);
    formData.append('comment', comment);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if ([200, 400, 500].includes(response.status))
            return response.json()
        else{
            signal = false;
            alert("댓글 등록 실패");
        }
    }).catch(err => {
        if (signal){
            signal = false;
            alert("댓글 등록 실패");
        }
    }).then(result => {
        if (result['result'])
            window.location.reload(true);
        else if (signal){
            signal = false;
            alert(result['msg']);
        }
    });
}

// 댓글 삭제 리퀘스트
function sendDeleteComment(cid){
    let uid = document.getElementById( 'uid' ).value;

    if (uid === ''){
        alert("삭제 권한이 없습니다.");

        return
    }

    const formData = new FormData();
    const url = '/comment/delete';
    let signal = true;

    formData.append('uid', uid);
    formData.append('cid', cid);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if (response.status === 200)
            return response.json()
        else{
            signal = false;
            alert("삭제 실패");
        }
    }).catch(err => {
        if (signal){
            signal = false;
            alert("삭제 실패");
        }
    }).then(result => {
        if (result['result'])
            window.location.reload(true);
        else if (signal){
            signal = false;
            alert("삭제 실패");
        }
    }).catch(err => {
        if (signal)
            alert("삭제 실패");
    });
}

// 회원 가입 리퀘스트
function sendInsertUser() {
    let uid = document.getElementById( 'uid' ).value;
    let pwd = document.getElementById( 'pwd' ).value;
    let nickname = document.getElementById( 'nickname' ).value;

    const formData = new FormData();
    const url = '/member/join/request';
    let signal = true;

    formData.append('uid', uid);
    formData.append('pwd', pwd);
    formData.append('nickname', nickname);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if ([200, 400, 500].includes(response.status))
            return response.json()
        else {
            signal = false;
            alert("에러가 발생했습니다.");
        }
    }).catch(err => {
        if (signal){
            signal = false;
            alert("에러가 발생했습니다.");
        }
    }).then(result => {
        if (result['result']){
            alert(result['msg']);
            location.href="/";
        }
        else if (signal){
            signal = false;
            alert(result['msg']);
        }
    });
};

// 로그인 리퀘스트
function sendLoginUser() {
    let uid = document.getElementById( 'uid' ).value;
    let pwd = document.getElementById( 'pwd' ).value;

    const formData = new FormData();
    const url = '/member/login/request';
    let signal = true;

    formData.append('uid', uid);
    formData.append('pwd', pwd);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if ([200, 400, 500].includes(response.status))
            return response.json()
        else {
            signal = false;
            alert("에러가 발생했습니다.");
        }
    }).catch(err => {
        if (signal){
            signal = false;
            alert("에러가 발생했습니다.");
        }
    }).then(result => {
        if (result['result']){
            alert(result['msg']);
            window.location.reload(true);
        }
        else if (signal){
            signal = false;
            alert(result["msg"]);
        }
    });
};

// 로그아웃 리퀘스트
function sendLogoutUser() {
    let uid = document.getElementById( 'uid' ).value;
    let nickname = document.getElementById( 'nickname' ).value;

    const formData = new FormData();
    const url = '/member/logout/request';
    let signal = true;

    formData.append('uid', uid);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if ([200, 400, 500].includes(response.status))
            return response.json()
        else {
            signal = false;
            alert("에러가 발생했습니다.");
        }
    }).catch(err => {
        if (signal){
            signal = false;
            alert("에러가 발생했습니다.");
        }
    }).then(result => {
        if (result['result']){
            window.location.reload(true);
        }
        else if (signal){
            signal = false;
            alert(result['msg']);
        }
    });
};

// 회원 정보 수정 리퀘스트
function sendUpdateUser() {
    let uid = document.getElementById( 'uid' ).value;
    let pwd = document.getElementById( 'pwd' ).value;
    let new_pwd = document.getElementById( 'new_pwd' ).value;
    let new_nickname = document.getElementById( 'new_nickname' ).value;

    const formData = new FormData();
    const url = '/member/update/request';
    let signal = true;

    formData.append('uid', uid);
    formData.append('pwd', pwd);

    if (pwd === '') {
        alert('비밀번호를 입력하세요.');
        return ;
    }
    else if (new_pwd === '' && new_nickname ===''){
        alert('변경할 값을 적어도 1개 입력하세요.');
        return ;
    }
    
    if (new_pwd !== ''){
        formData.append('new_pwd', new_pwd);
    }
    if (new_nickname !== ''){
        formData.append('new_nickname', new_nickname);
    }

    
    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if ([200, 400, 500].includes(response.status))
            return response.json()
        else{
            signal = false;
            alert("변경 실패");
        }
    }).catch(err => {
        if (signal){
            signal = false;
            alert("변경 실패");
        }
    }).then(result => {
        if (result['result']){
            alert(result['msg']);
            location.href="/";
        }
        else if (signal){
            alert(result['msg']);
        }
    });
}

// 회원 탈퇴 리퀘스트
function sendDeleteUser() {
    let uid = document.getElementById( 'uid' ).value;
    let pwd = document.getElementById( 'pwd' ).value;
    let confirm = document.getElementById( 'confirm' ).value;

    if (confirm !== '탈퇴합니다'){
        alert("탈퇴를 원한다면 탈퇴합니다를 입력해주세요.");
        return
    }

    const formData = new FormData();
    const url = '/member/delete/request';
    let signal = true;

    formData.append('uid', uid);
    formData.append('pwd', pwd);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if ([200, 400, 500].includes(response.status))
            return response.json()
        else{
            signal = false;
            alert("탈퇴 실패");
        }
    }).catch(err => {
        if (signal){
            signal = false;
            alert("탈퇴 실패");
        }
    }).then(result => {
        if (result['result']){
            alert(result['msg']);
            location.href="/";
        }
        else if (signal){
            alert(result['msg']);
        }
    });
}