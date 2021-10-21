function article_check(form){
    try{
        const reg = /(<([^>]+)>)/gi;
        let title = form.title.value;
        // CKEditor는 getData를 통해 값을 가져온다.
        let content = ckEditor.getData();
        content = content.replace(reg, "");

        if (title.length < 1){
            form.title.focus();
            alert("제목을 작성해주세요.");
            
            return false;
        }
        else if (content.length < 1){
            form.content.focus();
            alert("내용을 작성해주세요.");
            
            return false;
        }
    }
    catch(err){
        alert("에러 발생으로 인한 전송 실패");
        return false;
    }
}