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