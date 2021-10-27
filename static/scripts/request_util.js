let UID = undefined;
const ALLOW_RESPONSE_STATUS = [200, 400, 500];

// 유저 아이디 반환
function setUID(uid){
    UID = uid;
}

function isUIDEmpty(){
    if (UID == undefined)
        return true;
    else
        return false;
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
    })
    .then(result => {
        if (result['result']){
            const hits = document.getElementsByName( "hit" );
            for (let hit of hits)
                hit.innerText = result['data'];
        }
        else if (signal){
            signal = false;
            alert(result['msg']);
        }
    })
    .catch(err => {
        if (signal){
            signal = false;
            alert("추천 실패");
        }
    });
}


// 댓글 상태 업데이트
function commentBuilder(comments, uid, aid, board) {
    document.getElementById( "num-comments" ).innerText = comments.length;
    let table = document.getElementById( "comments" );
    table.removeChild(table.getElementsByTagName("tbody")[0]);

    for (let comment of comments) {
        const row = table.insertRow();
        const comment_nickname_cell = row.insertCell(0);
        const comment_content_cell = row.insertCell(1);
        const comment_date_cell = row.insertCell(2);
        const comment_btn_cell = row.insertCell(3);
        
        row.align = "center";
        comment_nickname_cell.innerText = comment[1];

        comment_content_cell.align = "left";
        comment_content_cell.innerText = comment[2];

        comment_date_cell.align = "right";
        comment_date_cell.innerText = comment[3]

        comment_btn_cell.align = "center";

        if (comment[4]){
            const del_form = document.createElement('form');
            del_form.setAttribute("onsubmit", "return sendDeleteComment(this)");
            del_form.innerHTML = `
            <input type="hidden" name="uid" value=${uid}>
            <input type="hidden" name="aid" value=${aid}>
            <input type="hidden" name="board" value=${board}>
            <input type="hidden" name="cid" value=${comment[0]}>
            <button class="del-btn comment-btn" type="submit">X</button>
            `
            comment_btn_cell.appendChild(del_form);
        }
        else
            comment_btn_cell.innerHTML = '&nbsp;';
    }
}


// 댓글 작성 리퀘스트
function sendInsertComment(form) {
    try{
        const uid_element = form.uid;
        const comment_element = form.input_comment;

        if (uid_element.value === undefined){
            alert("로그인이 필요한 작업입니다.");

            return false;
        }

        if (comment_element.value.length === 0)
        {
            alert("댓글을 작성해 주세요");
            comment_element.focus();

            return false;
        }

        const formData = new FormData(form);
        const url = '/comment/write';
        let signal = true;

        fetch (url, { method: 'POST', body: formData })
        .then(response=>{
            if (ALLOW_RESPONSE_STATUS.includes(response.status))
                return response.json()
            else{
                signal = false;
                alert("댓글 등록 실패");
            }
        })
        .then(result => {
            if (result['result']){
                commentBuilder(result['data'], uid_element.value, form.aid.value, form.board.value);
                document.getElementById( 'input-comment' ).value = "";
            }
            else if (signal){
                signal = false;
                alert(result['msg']);
                comment_element.focus();
            }
        })
        .catch(err => {
            if (signal){
                signal = false;
                alert("댓글 등록 실패");
            }
        });

        return false;
    }
    catch(err){
        console.log(err);
        alert("에러가 발생했습니다.");
        return false;
    }
}

// 댓글 삭제 리퀘스트
function sendDeleteComment(form){
    try{
        const uid = form.uid.value
        
        if (uid === undefined){
            alert("로그인이 필요한 작업입니다.");
    
            return false;
        }
        
        const formData = new FormData(form);
        const url = '/comment/delete';
        let signal = true;

        fetch (url, { method: 'POST', body: formData })
        .then(response=>{
            if (ALLOW_RESPONSE_STATUS.includes(response.status))
                return response.json()
            else{
                signal = false;
                alert("삭제 실패");
            }
        })
        .then(result => {
            if (result['result']){
                alert(result['msg']);
                commentBuilder(result['data'], uid, form.aid.value, form.board.value);
            }
            else if (signal){
                signal = false;
                alert(result['msg']);
            }
        })
        .catch(err => {
            console.log(err);
            if (signal){
                signal = false;
                alert("삭제 실패");
            }
        });
        return false;
    }
    catch(err){
        console.log(err)
        alert("에러가 발생했습니다.");
        return false;
    }
}

// 회원 가입 리퀘스트
function sendInsertUser(form) {
    if (!isUIDEmpty()){
        alert("이미 로그인 된 상태입니다.");

        return false;
    }
    try{
        let new_uid_element = form.new_uid;
        let new_pwd_element = form.new_pwd;
        let new_nickname_element = form.new_nickname;

        if (new_uid_element.value.length === 0){
            alert("아이디를 입력해 주세요");
            new_uid_element.focus();

            return false;
        }
        else if (new_pwd_element.value.length === 0){
            alert("비밀번호를 입력해 주세요");
            new_pwd_element.focus();
            return false;
        }
        else if (new_nickname_element.value.length === 0){
            alert("닉네임을 입력해 주세요");
            new_nickname_element.focus();
            return false;
        }

        const formData = new FormData(form);
        const url = '/member/join/request';
        let signal = true;
        
        formData.set('new_uid', btoa(new_uid_element.value));
        formData.set('new_pwd', btoa(new_pwd_element.value));

        fetch (url, { method: 'POST', body: formData })
        .then(response=>{
            if (ALLOW_RESPONSE_STATUS.includes(response.status))
                return response.json()
            else {
                signal = false;
                alert("에러가 발생했습니다.");
            }
        })
        .then(result => {
            if (result['result']){
                alert(result['msg']);
                location.href="/";
            }
            else if (signal){
                signal = false;
                alert(result['msg']);

                switch(result['data']){
                    case 0:
                        new_uid_element.focus();
                        break;
                    case 1:
                        new_pwd_element.focus();
                        break;
                    case 2:
                        new_nickname_element.focus();
                        break;
                }
            }
        })
        .catch(err => {
            if (signal){
                signal = false;
                console.log(err);
                alert("에러가 발생했습니다.");
            }
        });

        return false;
    }
    catch(err){
        console.log(err);
        alert("에러가 발생했습니다.");
        return false;
    }
}

// 로그인 리퀘스트
function sendLoginUser(form) {
    if (!isUIDEmpty()){
        alert("이미 로그인 된 상태입니다.");

        return false;
    }
    
    try{
        let uid_element = form.request_uid;
        let pwd_element = form.request_pwd;
        
        if (uid_element.value.length === 0){
            alert("아이디를 입력해 주세요");
            uid_element.focus();
            return false;
        }
        else if (uid_element.value.length === 0){
            alert("비밀번호를 입력해 주세요");
            pwd_element.focus();
            return false;
        }

        const formData = new FormData(form);
        const url = '/member/login/request';
        let signal = true;

        formData.set('request_uid', btoa(uid_element.value));
        formData.set('request_pwd', btoa(pwd_element.value));

        fetch (url, { method: 'POST', body: formData })
        .then(response=>{
            if (ALLOW_RESPONSE_STATUS.includes(response.status))
                return response.json()
            else {
                signal = false;
                alert("에러가 발생했습니다.");
            }
        })
        .then(result => {
            if (result['result']){
                alert(result['msg']);
                window.location.reload(true);
            }
            else if (signal){
                signal = false;
                alert(result["msg"]);
                
                switch(result["data"]){
                    case 0:
                        uid_element.focus();
                        break;
                    case 1:
                        pwd_element.focus();
                        break;
                }
            }
        })
        .catch(err => {
            if (signal){
                signal = false;
                alert("에러가 발생했습니다.");
            }
        });

        return false;
    }
    catch(err){
        console.log(err);
        alert("에러가 발생했습니다.");
        return false;
    }
}

// 로그아웃 리퀘스트
function sendLogoutUser(button) {
    const uid = button.value;

    if (uid === undefined){
        alert("로그인이 필요한 작업입니다.");

        return;
    }

    const formData = new FormData();
    const url = '/member/logout/request';
    let signal = true;

    formData.append('uid', btoa(uid));

    fetch (url, { method: 'POST', body: formData })
    .then(response=>{
        if (ALLOW_RESPONSE_STATUS.includes(response.status))
            return response.json()
        else {
            signal = false;
            alert("에러가 발생했습니다.");
        }
    })
    .then(result => {
        if (result['result'])
            window.location.reload(true);
        else if (signal){
            signal = false;
            alert(result['msg']);
        }
    })
    .catch(err => {
        if (signal){
            signal = false;
            alert("에러가 발생했습니다.");
        }
    });
}

// 회원 정보 수정 리퀘스트
function sendUpdateUser(form) {
    if (form.uid === undefined){
        alert("로그인이 필요한 작업입니다.");

        return false;
    }
    
    try{
        let old_pwd_element = form.old_pwd;
        let new_pwd_element = form.new_pwd;
        let new_nickname_element = form.new_nickname;

        if (old_pwd_element.value === '') {
            alert('비밀번호를 입력하세요.');
            old_pwd_element.focus();
            return false;
        }
        else if (new_pwd_element.value === '' && new_nickname_element.value ===''){
            alert('변경할 값을 적어도 1개 입력하세요.');
            new_pwd_element.focus();
            return false;
        }

        const formData = new FormData(form);
        const url = '/member/update/request';
        let signal = true;
        
        formData.set('uid', btoa(form.uid.value));
        formData.set('old_pwd', btoa(old_pwd_element.value));
        formData.set('new_pwd', btoa(new_pwd_element.value));
        
        fetch (url, { method: 'POST', body: formData })
        .then(response=>{
            if (ALLOW_RESPONSE_STATUS.includes(response.status))
                return response.json()
            else{
                signal = false;
                alert("변경 실패");
            }
        })
        .then(result => {
            if (result['result']){
                alert(result['msg']);
                location.href="/";
            }
            else if (signal){
                alert(result['msg']);
                
                switch(result['data']) {
                    case 0:
                        old_pwd_element.focus();
                        break;
                    case 1:
                        new_pwd_element.focus();
                        break;
                    case 2:
                        new_nickname_element.focus();
                        break;
                }
            }
        })
        .catch(err => {
            if (signal){
                signal = false;
                alert("변경 실패");
            }
        });

        return false;
    }
    catch(err){
        console.log(err);
        alert("에러가 발생했습니다.");
        return false;
    }
}

// 회원 탈퇴 리퀘스트
function sendDeleteUser(form) {
    if (form.uid === undefined){
        alert("로그인이 필요한 작업입니다.");

        return false;
    }

    try{
        let pwd_element = form.pwd;
        let confirm_element = form.confirm;

        if (pwd_element.value.length === 0){
            alert("비밀번호를 입력하세요.");
            pwd_element.focus()
            return false;
        }
        else if (confirm_element.value !== '탈퇴합니다'){
            alert("탈퇴를 원한다면 탈퇴합니다를 입력해주세요.");
            confirm_element.focus();
            return false;
        }

        const formData = new FormData(form);
        const url = '/member/delete/request';
        let signal = true;

        formData.set('uid', btoa(form.uid.value));
        formData.set('pwd', btoa(pwd_element.value));

        fetch (url, { method: 'POST', body: formData })
        .then(response=>{
            if (ALLOW_RESPONSE_STATUS.includes(response.status))
                return response.json()
            else{
                signal = false;
                alert("탈퇴 실패");
            }
        })
        .then(result => {
            if (result['result']){
                alert(result['msg']);
                location.href="/";
            }
            else if (signal){
                alert(result['msg']);
                pwd_element.focus();
            }
        })
        .catch(err => {
            if (signal){
                signal = false;
                alert("탈퇴 실패");
            }
        });

        return false;
    }
    catch(err){
        console.log(err);
        alert("에러가 발생했습니다.");
        return false;
    }
}
