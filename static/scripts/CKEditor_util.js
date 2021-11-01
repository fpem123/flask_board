let ckEditor;

function setCkeditor(board){
    ClassicEditor
    .create( document.querySelector( '#editor' ), {
        language: { ui: 'ko', content: 'ko'},
    })
    .then(editor => {
        ckEditor = editor;
        editor.on();
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
    .then(editor => {
        ckEditor = editor;
        editor.isReadOnly = true;
    })
    .catch( error => {
        console.error(error);
    })
}

