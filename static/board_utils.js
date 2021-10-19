let UID = undefined;
const ALLOW_RESPONSE_STATUS = [200, 400, 500];

// 유저 아이디 반환
function setUID(){
    UID =  document.getElementById( 'uid' ).value;
}

function isUIDEmpty(){
    if (UID == undefined){
        return true;
    }
    else
        return false;
}


function setCkeditor(board){
    ClassicEditor
    .create( document.querySelector( '#editor' ), {
        language: { ui: 'ko', content: 'ko'},
        ckfinder : {uploadUrl: `/board/${board}/image-upload`}
    })
    .catch( error => {
        console.error(error);
    });
}


function setCkeditorReadOnly(){
    ClassicEditor
    .create( document.querySelector( '#content' ), {
        language: { ui: 'ko', content: 'ko'},
        toolbar: []
    })
    .catch( error => {
        console.error(error);
    })
    .then(editor => {
        editor.isReadOnly = true;
    })
    .catch( error => {
        console.error(error);
    })
}


// 엔터키 전송 방지
function onKeydownEnter(){
    if(event.keyCode==13) 
        return false
}

// textarea tap키 처리
function onKeydownTap(textarea){
    if (event.keyCode==9) {
        textarea.focus();
        space = "    ";
        textarea.selection = document.selection.createRange();
        textarea.selection.text = space;
        event.returnValue = false;
        return false;
    }
}

// 추천 리퀘스트
function sendHit(){
    if (isUIDEmpty()){
        alert("로그인이 필요한 작업입니다.");
        return;
    }

    let aid = document.getElementById( 'aid' ).value;

    const formData = new FormData();
    const url = '/article/hit';
    let signal = true;

    formData.append('aid', aid);
    formData.append('uid', UID);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if (ALLOW_RESPONSE_STATUS.includes(response.status))
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
        if (result['result']){
            hits = document.getElementsByName( "hit" );
            for (let hit of hits){
                console.log(hit);
                hit.innerText = result['data'];
            }
        }
        else if (signal){
            signal = false;
            alert(result['msg']);
        }
    });
}


// 댓글 보여주기
function commentBuilder(comments) {
    document.getElementById( "num-comments" ).innerText = comments.length;
    table = document.getElementById( "comments" );

    while (table.hasChildNodes()){
        table.removeChild(table.lastChild);
    }

    for (let comment of comments) {
        const row = table.insertRow();
        const comment_nickname_cell = row.insertCell(0);
        const comment_content_cell = row.insertCell(1);
        const comment_date_cell = row.insertCell(2);
        const comment_btn_cell = row.insertCell(3);
        const comment_uid = comment[1];
        
        row.align = "center";

        comment_nickname_cell.style.width = "10%";
        comment_nickname_cell.innerText = comment[2];

        comment_content_cell.align = "left";
        comment_content_cell.style.width = "65%";
        comment_content_cell.innerText = comment[3];

        comment_date_cell.align = "right";
        comment_date_cell.style.width = "20%";
        comment_date_cell.innerText = comment[4]

        comment_btn_cell.style.width = "5%";
        comment_btn_cell.align = "right";

        if (comment_uid === UID){
            const del_btn = document.createElement('button');
            del_btn.value = comment[0];
            del_btn.innerText = 'X';
            del_btn.setAttribute("onClick", "return sendDeleteComment(this)");
            comment_btn_cell.appendChild(del_btn);
        }
        else {
            comment_btn_cell.innerText = '&nbsp;';
        }
    }
}


// 댓글 작성 리퀘스트
function sendInsertComment() {
    if (isUIDEmpty()){
        alert("로그인이 필요한 작업입니다.");

        return;
    }

    let aid = document.getElementById( 'aid' ).value;
    let comment = document.getElementById( 'input-comment' ).value;

    const formData = new FormData();
    const url = '/comment/write';
    let signal = true;

    formData.append('aid', aid);
    formData.append('uid', UID);
    formData.append('comment', comment);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if (ALLOW_RESPONSE_STATUS.includes(response.status))
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
        if (result['result']){
            commentBuilder(result['data']);
            document.getElementById( 'input-comment' ).value = "";
        }
        else if (signal){
            signal = false;
            alert(result['msg']);
        }
    });
}

// 댓글 삭제 리퀘스트
function sendDeleteComment(button){
    if (isUIDEmpty()){
        alert("로그인이 필요한 작업입니다.");

        return;
    }
    let cid = button.value;
    let aid = document.getElementById( 'aid' ).value;

    const formData = new FormData();
    const url = '/comment/delete';
    let signal = true;

    formData.append('uid', UID);
    formData.append('cid', cid);
    formData.append('aid', aid);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if (ALLOW_RESPONSE_STATUS.includes(response.status))
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
        if (result['result']){
            alert(result['msg']);
            commentBuilder(result['data']);
        }
        else if (signal){
            signal = false;
            alert(result['msg']);
        }
    });
}

// 회원 가입 리퀘스트
function sendInsertUser() {
    if (!isUIDEmpty()){
        alert("이미 로그인 된 상태입니다.");

        return;
    }

    let new_uid = document.getElementById( 'new_uid' ).value;
    let new_pwd = document.getElementById( 'new_pwd' ).value;
    let new_nickname = document.getElementById( 'new_nickname' ).value;

    const formData = new FormData();
    const url = '/member/join/request';
    let signal = true;

    formData.append('uid', new_uid);
    formData.append('pwd', new_pwd);
    formData.append('nickname', new_nickname);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if (ALLOW_RESPONSE_STATUS.includes(response.status))
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
    if (!isUIDEmpty()){
        alert("이미 로그인 된 상태입니다.");

        return;
    }

    let uid = document.getElementById( 'request_uid' ).value;
    let pwd = document.getElementById( 'request_pwd' ).value;

    const formData = new FormData();
    const url = '/member/login/request';
    let signal = true;

    formData.append('uid', uid);
    formData.append('pwd', pwd);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if (ALLOW_RESPONSE_STATUS.includes(response.status))
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
    if (isUIDEmpty()){
        alert("로그인이 필요한 작업입니다.");

        return;
    }
    const formData = new FormData();
    const url = '/member/logout/request';
    let signal = true;

    formData.append('uid', UID);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if (ALLOW_RESPONSE_STATUS.includes(response.status))
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
    if (isUIDEmpty()){
        alert("로그인이 필요한 작업입니다.");

        return;
    }
    let old_pwd = document.getElementById( 'old_pwd' ).value;
    let new_pwd = document.getElementById( 'new_pwd' ).value;
    let new_nickname = document.getElementById( 'new_nickname' ).value;

    const formData = new FormData();
    const url = '/member/update/request';
    let signal = true;

    if (old_pwd === '') {
        alert('비밀번호를 입력하세요.');
        return ;
    }
    else if (new_pwd === '' && new_nickname ===''){
        alert('변경할 값을 적어도 1개 입력하세요.');
        return ;
    }
    
    formData.append('uid', UID);
    formData.append('pwd', old_pwd);

    if (new_pwd !== ''){
        formData.append('new_pwd', new_pwd);
    }
    if (new_nickname !== ''){
        formData.append('new_nickname', new_nickname);
    }

    
    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if (ALLOW_RESPONSE_STATUS.includes(response.status))
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
    if (isUIDEmpty()){
        alert("로그인이 필요한 작업입니다.");

        return;
    }

    let pwd = document.getElementById( 'pwd' ).value;
    let confirm = document.getElementById( 'confirm' ).value;

    if (confirm !== '탈퇴합니다'){
        alert("탈퇴를 원한다면 탈퇴합니다를 입력해주세요.");
        return
    }

    const formData = new FormData();
    const url = '/member/delete/request';
    let signal = true;

    formData.append('uid', UID);
    formData.append('pwd', pwd);

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if (ALLOW_RESPONSE_STATUS.includes(response.status))
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