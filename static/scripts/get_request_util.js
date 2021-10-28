// 댓글 상태 업데이트
function commentBuilder(comments, uid, aid, board) {
    document.getElementById( "num-comments" ).innerText = comments.length;
    let table = document.getElementById( "comments" );
    table.removeChild(table.getElementsByTagName( "tbody" )[0]);
    table.appendChild(document.createElement( "tbody" ));

    for (let comment of comments) {
        const row = table.getElementsByTagName('tbody')[0].insertRow();
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


// 댓글 가져오기
function getComments(aid, board, uid=undefined) {
    const url = `/comments/get?aid=${aid}&board=${board}&uid=${uid}`;

    fetch (url)
    .then(response=>{
        if (response.status === 200)
            return response.json()
    })
    .then(result => {
        if (result['result'])
            commentBuilder(result['data'], uid, aid, board);
    })
    .catch(err => {
        console.log(err);
    });
}


// 글 정보 업데이트
function articleReadBuilder(article, aid, board) {
    document.getElementById( "article-title" ).innerText = article["title"];
    document.getElementById( "article-nickname" ).innerText = article["nickname"];
    document.getElementById( "article-id" ).innerText = aid;
    document.getElementById( "article-date" ).innerText = article["article_time"];
    document.getElementById( "article-view" ).innerText = article["view"];
    ckEditor.data.set(article["content"]);
    for (let hit of document.getElementsByName( "hit" ))
        hit.innerText = article["hit"];
    if (article["flag"])
        for (let flag_need of document.getElementsByClassName( "flag-need" ))
            flag_need.style.display = "block";
    if (board == 'all')
        for (let board_check of document.getElementsByClassName( "need-board-check" ))
            board_check.style.display = "none";
}


// 글 가져오기 for article_read
function getArticleForReadPage(aid, board) {
    const url = `/article/get?aid=${aid}&board=${board}`;

    fetch (url)
    .then(response=>{
        if (response.status === 200)
            return response.json()
    })
    .then(result => {
        if (result['result'])
            articleReadBuilder(result['data'], aid, board);
    })
    .catch(err => {
        console.log(err);
    });
}


// 글 정보 업데이트
function articleUpdateBuilder(article) {
    document.getElementById( "title" ).value = article["title"];
    ckEditor.data.set(article["content"]);
}


// 글 가져오기 for article_update
function getArticleForUpdatePage(aid, board) {
    const url = `/article/get?aid=${aid}&board=${board}`;

    fetch (url)
    .then(response=>{
        if (response.status === 200)
            return response.json()
    })
    .then(result => {
        if (result['result'])
            articleUpdateBuilder(result['data']);
    })
    .catch(err => {
        console.log(err);
    });
}


// 페이징을 위한 li 생성
function mkPagingLi(page, current_page, query, char){
    const paging_li = document.createElement( "li" );
    const paging_anchor = document.createElement( "a" );
    paging_li.className = "page";
    if (page != current_page)
        paging_anchor.href = "/board/articles" + query + `&page=${page}`;
    paging_anchor.innerText = char;
    paging_li.appendChild(paging_anchor);

    return paging_li
}


// 글 목록 상태 업데이트
function boardBuilder(data, board, search_data) {
    const table = document.getElementById( "board-table" );
    const msg_block = document.getElementById( "board-msg" );
    table.removeChild(table.getElementsByTagName("tbody")[0]);
    table.appendChild(document.createElement('tbody'))
    msg_block.style.display = "none";

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
        
        row.align = "center";

        article_id_cell.innerText = article[0];
        article_writer_cell.innerText = article[1]
        
        article_title_cell.align = "left";
        const article_anchor = document.createElement('a');
        if (search_data["aid"] != article[0])
            article_anchor.href = `/board/view` + search_data['query'] + `&aid=${article[0]}&page=${search_data['page']}`;
        article_anchor.className = "to-article";
        if (board == "all")
            article_anchor.innerHTML = `<label class="origin-board">[${article[7]}]</label>
            ${article[2]}<label class="num-comment">
            [${article[6]}]</label>`;
        else
            article_anchor.innerHTML = `${article[2]}<label class="num-comment">[${article[6]}]</label>`;
        article_title_cell.appendChild(article_anchor);

        article_date_cell.innerText = article[3];
        article_view_cell.innerText = article[4];
        article_hit_cell.innerText = article[5];
    }

    // 페이징 상태 업데이트
    const paging_ui = document.getElementById( "paging-ui" );

    if (data['start'] > 10) {
        const paging_li = mkPagingLi(data['start'] - 1, search_data["page"], search_data['query'], "◀");
        paging_ui.appendChild(paging_li);
    }

    for (let page = data['start']; page < data['end']; page++) {
        const paging_li = mkPagingLi(page, search_data["page"], search_data['query'], page);
        paging_ui.appendChild(paging_li);
    }

    if (data['end'] < data['last_page']) {
        const paging_li = mkPagingLi(data['end'], search_data["page"], search_data['query'], "▶");
        paging_ui.appendChild(paging_li);
    }
}


// 글 목록 가져오기
function getArticles(board, aid=undefined, page=undefined, art_per_page=undefined, option=undefined, keyword=undefined) {
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
            boardBuilder(result['data'], board, search_data);
    })
    .catch(err => {
        console.log(err);
    });
}

