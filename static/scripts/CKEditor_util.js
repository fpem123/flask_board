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
