// 게시글 삭제 요청
function sendDeleteArticleForAdmin(form){
    try{
        const uid_element = form.uid;
        const board = form.board.value;

        if (uid_element.value === undefined){
            alert("로그인이 필요한 작업입니다.");
    
            return false;
        }
        
        const formData = new FormData(form);
        const url = `/delete/article?board=${board}`;

        fetch (url, { method: 'POST', body: formData })
        .then(response=>{
            if (response.status === 200)
                return response.json()
        })
        .then(result => {
            console.log(result);
            alert('삭제 성공');
            window.location.reload();
        })
        .catch(err => {
            alert('삭제 실패');
            console.log(err);
        });
    }
    catch(err){
        console.log(err)
        alert("에러가 발생했습니다.");
    }
    return false;
}

// 페이징을 위한 li 생성
function mkPagingLiForAdmin(page, current_page, query, char){
    const paging_li = document.createElement( "li" );
    const paging_anchor = document.createElement( "a" );

    paging_li.className = "page";

    if (page != current_page)
        paging_anchor.href = "/admin/board" + query + `&page=${page}`;
    paging_anchor.innerText = char;
    paging_li.appendChild(paging_anchor);

    return paging_li
}

// 글 목록 상태 업데이트
function boardBuilderForAdmin(data, search_data) {
    const table = document.getElementById( "board-table" );
    const msg_block = document.getElementById( "board-msg" );
    table.removeChild(table.getElementsByTagName("tbody")[0]);
    table.appendChild(document.createElement('tbody'))
    msg_block.style.display = "none";

    for (let board_check of document.getElementsByClassName( "need-board-check" ))
        board_check.style.display = "none";

    if (data['articles'].length === 0){
        msg_block.style.display = "block";
        msg_block.innerText = "작성된 글이 없습니다.";
    }

    for (let article of data['articles']) {
        const row = table.getElementsByTagName('tbody')[0].insertRow();
        const article_id_cell = row.insertCell(0);
        const article_title_cell = row.insertCell(1);
        const article_writer_cell = row.insertCell(2);
        const article_date_cell = row.insertCell(3);
        const article_view_cell = row.insertCell(4);
        const article_hit_cell = row.insertCell(5);
        const article_del_btn_cell = row.insertCell(6);
        
        row.align = "center";

        article_id_cell.innerText = article[0];
        article_writer_cell.innerText = article[1]
        
        article_title_cell.align = "left";
        const article_anchor = document.createElement('a');
        if (search_data["aid"] != article[0])
            article_anchor.href = `/board/view?board=${article[7]}&aid=${article[0]}`;
        article_anchor.className = "to-article";
        article_anchor.innerHTML = `<label class="origin-board">[${article[7]}]</label>
        ${article[2]}<label class="num-comment">
        [${article[6]}]</label>`;
        article_title_cell.appendChild(article_anchor);

        article_date_cell.innerText = article[3];
        article_view_cell.innerText = article[4];
        article_hit_cell.innerText = article[5];
        
        const del_form = document.createElement('form');
        del_form.setAttribute("onsubmit", "return sendDeleteArticleForAdmin(this)");
        del_form.innerHTML = `
            <input type="hidden" name="uid" value=${uid}>
            <input type="hidden" name="aid" value=${article[0]}>
            <input type="hidden" name="board" value=${article[7]}>
            <button class="del-btn article-del-btn" type="submit">X</button>
        `;
        article_del_btn_cell.appendChild(del_form);
    }

    // 페이징 상태 업데이트
    const paging_ui = document.getElementById( "paging-ui" );

    if (data['start'] > 10) {
        const paging_li = mkPagingLiForAdmin(data['start'] - 1, search_data["page"], search_data['query'], "◀");
        paging_ui.appendChild(paging_li);
    }

    for (let page = data['start']; page < data['end']; page++) {
        const paging_li = mkPagingLiForAdmin(page, search_data["page"], search_data['query'], page);
        paging_ui.appendChild(paging_li);
    }

    if (data['end'] < data['last_page']) {
        const paging_li = mkPagingLiForAdmin(data['end'], search_data["page"], search_data['query'], "▶");
        paging_ui.appendChild(paging_li);
    }
}

// 글 목록 가져오기
function getArticlesForAdmin(board, aid=undefined, page=undefined, art_per_page=undefined, option=undefined, keyword=undefined) {
    let query = `?board=${board}`;

    if (art_per_page)
        query += `&art_per_page=${art_per_page}`;
    if (option)
        query += `&option=${option}`;
    if (keyword)
        query += `&keyword=${keyword}`;

    let url = "/articles/get" + query;

    if (page)
        url += `&page=${page}`;

    const search_data = { "query": query, "aid": aid, "page": page, "art_per_page": art_per_page, "option": option, "keyword": keyword };
    
    fetch (url)
    .then(response=>{
        if (response.status === 200)
            return response.json();
    })
    .then(result => {
        if (result['result'])
            boardBuilderForAdmin(result['data'], search_data);
    })
    .catch(err => {
        console.log(err);
    });
}


// 유저 목록 상태 업데이트
function userBuilderForAdmin(data) {
    const table = document.getElementById( "board-table" );
    const msg_block = document.getElementById( "board-msg" );
    table.removeChild(table.getElementsByTagName("tbody")[0]);
    table.appendChild(document.createElement('tbody'))
    msg_block.style.display = "none";

    if (data['user_infos'].length === 0){
        msg_block.style.display = "block";
        msg_block.innerText = "검색된 유저가 없습니다.";
    }

    for (const userinfo of data['user_infos']) {
        const row = table.getElementsByTagName('tbody')[0].insertRow();
        const user_id_cell = row.insertCell(0);
        const user_nickname_cell = row.insertCell(1);
        const user_grade_cell = row.insertCell(2);
        const user_state_cell = row.insertCell(3);
        const user_nickname_change_cell = row.insertCell(4);
        const user_ban_btn_cell = row.insertCell(5);
        
        row.align = "center";

        user_id_cell.innerText = userinfo[0];
        user_nickname_cell.innerText = userinfo[1]
        
        if (userinfo[2] == 0) {
            user_grade_cell.innerText = "일반"
            user_state_cell.innerText = userinfo[3]

            
            const nickname_change_form = document.createElement('form');
            nickname_change_form.setAttribute("onsubmit", "return userNicknameChange(this)");
            nickname_change_form.innerHTML = `
                <input type="hidden" name="uid" value=${userinfo[0]}>
                <input type="text" name="new_nickname" maxlength=10 value=${userinfo[1]}>
                <button class="admin-submit" type="submit">변경</button>
            `;
            user_nickname_change_cell.appendChild(nickname_change_form);

            const ban_form = document.createElement('form');
            if (userinfo[3]){
                ban_form.setAttribute("onsubmit", "return userUnban(this)");
                ban_form.innerHTML = `
                    <input type="hidden" name="uid" value=${userinfo[0]}>
                    <button class="admin-submit" type="submit">해제</button>
                `;
            }
            else {
                ban_form.setAttribute("onsubmit", "return userBan(this)");
                ban_form.innerHTML = `
                    <input type="hidden" name="uid" value=${userinfo[0]}>
                    <select class="ban-option" name="ban-option">
                        <option value=1>1일</option>
                        <option value=7>7일</option>
                        <option value=30>30일</option>
                        <option value=365>365일</option>
                    </select>
                    <button class="admin-submit" type="submit">확인</button>
                `;

            }
            user_ban_btn_cell.appendChild(ban_form);
        }
        else if  (userinfo[2] == 1) {
            user_grade_cell.innerText = "어드민"
            user_state_cell.innerText = "해당 없음"
            user_nickname_change_cell.innerText = "불가능";
            user_ban_btn_cell.innerText = "불가능";
        }
    }

    /*
    // 페이징 상태 업데이트
    const paging_ui = document.getElementById( "paging-ui" );

    if (data['start'] > 10) {
        const paging_li = mkPagingLiForAdmin(data['start'] - 1, search_data["page"], search_data['query'], "◀");
        paging_ui.appendChild(paging_li);
    }

    for (let page = data['start']; page < data['end']; page++) {
        const paging_li = mkPagingLiForAdmin(page, search_data["page"], search_data['query'], page);
        paging_ui.appendChild(paging_li);
    }

    if (data['end'] < data['last_page']) {
        const paging_li = mkPagingLiForAdmin(data['end'], search_data["page"], search_data['query'], "▶");
        paging_ui.appendChild(paging_li);
    }
    */
}


// 유저 목록 가져오기
function getUsersForAdmin(page=undefined, art_per_page=undefined, option=undefined, keyword=undefined) {
    let query = `?art_per_page=${art_per_page}`;

    if (option)
        query += `&option=${option}`;
    if (keyword)
        query += `&keyword=${keyword}`;

    let url = "/userinfos/get" + query;

    if (page)
        url += `&page=${page}`;

    fetch (url)
    .then(response=>{
        if (response.status === 200)
            return response.json();
    })
    .then(result => {
        if (result['result'])
            userBuilderForAdmin(result["data"]);
    })
    .catch(err => {
        console.log(err);
    });
}

// 유저 닉네임 강제 변경
function userNicknameChange(form) {
    try{
        const formData = new FormData(form);
        const url = '/user/set_nickname';

        fetch (url, { method: 'POST', body: formData })
        .then(response=>{
            if (ALLOW_RESPONSE_STATUS.includes(response.status))
                return response.json()
        })
        .then(result => {
            alert(result['msg']);
            window.location.reload();
        })
        .catch(err => {
            alert('변경 실패');
            console.log(err);
        });
    }
    catch(err) {
        console.log(err);
        alert("에러가 발생했습니다.");
    }

    return false;
}

// 유저 밴
function userBan(form) {
    try{
        const formData = new FormData(form);
        const url = '/user/ban';

        fetch (url, { method: 'POST', body: formData })
        .then(response=>{
            if (ALLOW_RESPONSE_STATUS.includes(response.status))
                return response.json()
        })
        .then(result => {
            alert(result['msg']);
            window.location.reload();
        })
        .catch(err => {
            alert('밴 실패');
            console.log(err);
        });
    }
    catch(err) {
        console.log(err);
        alert("에러가 발생했습니다.");
    }

    return false;
}

// 유저 밴 해제
function userUnban(form) {
    try{
        const formData = new FormData(form);
        const url = '/user/unban';

        fetch (url, { method: 'POST', body: formData })
        .then(response=>{
            if (ALLOW_RESPONSE_STATUS.includes(response.status))
                return response.json()
        })
        .then(result => {
            alert(result['msg']);
            window.location.reload();
        })
        .catch(err => {
            alert('밴 해제 실패');
            console.log(err);
        });
    }
    catch(err) {
        console.log(err);
        alert("에러가 발생했습니다.");
    }

    return false;
}
