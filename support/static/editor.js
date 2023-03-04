let editor = null
let addEditor = null

const editModal = document.getElementById('editModal')

editModal.addEventListener('show.bs.modal', event => {
  const button = event.relatedTarget
  console.log(button)
  let title = button.getAttribute('data-bs-title')
  let text = button.getAttribute('data-bs-text')
  let idFaq = button.getAttribute('data-bs-id')
  let parentId = button.getAttribute('data-bs-parentId')
  console.log(parentId)
  const modalTitle = editModal.querySelector('#title')
  modalTitle.value = title
  editModal.querySelector('#idFaq').value = idFaq
  editModal.querySelector('#parentId').value = parentId
  if (!editor) {
    console.log("ADSad")
    editor = new FroalaEditor('#example', {
      requestHeaders: {
    
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    
      },
      imageUploadParam: 'in_file',
    
      imageUploadURL: '/upload_image/',
    
      imageUploadMethod: 'POST',
    
      imageMaxSize: 5 * 1024 * 1024,
    
      imageAllowedTypes: ['jpeg', 'jpg', 'png'],
       	

      toolbarButtons: {

        'moreText': {
      
          'buttons': ['bold', 'italic', 'underline','strikeThrough'],
          'buttonsVisible': 6
      
        },
        'moreRich': {
      
          'buttons': ['insertLink', 'insertImage']
      
        },
      },
      enter: FroalaEditor.ENTER_DIV,
      quickInsertTags: null,
      shortcutsEnabled: ['bold', 'italic']
      }, () => {
        editor.html.set(text);
      });  
  } else {
    editor.html.set(text);
  }
})

editModal.addEventListener('hidden.bs.modal', event => {
  if (editor) {
    editor.destroy()
    editor = null
  }
})

const addModal = document.getElementById('addModal')

addModal.addEventListener('show.bs.modal', event => {
  const button = event.relatedTarget
  let parentId = button.getAttribute('data-bs-parentId')
  addModal.querySelector('#parentAdd').value = parentId
  if (!addEditor) {
    addEditor = new FroalaEditor('#addEditor', {
      requestHeaders: {
      
      "Authorization": `Bearer ${localStorage.getItem("token")}`
      
      },
      imageUploadParam: 'in_file',
    
      imageUploadURL: '/upload_image/',
    
      imageUploadMethod: 'POST',
    
      imageMaxSize: 5 * 1024 * 1024,
    
      imageAllowedTypes: ['jpeg', 'jpg', 'png'],
      toolbarButtons: {

        'moreText': {
      
          'buttons': ['bold', 'italic', 'underline','strikeThrough'],
          'buttonsVisible': 6
      
        },
        'moreRich': {
      
          'buttons': ['insertLink', 'insertImage']
      
        },
      },
      quickInsertTags: null,
      enter: FroalaEditor.ENTER_DIV,
      shortcutsEnabled: ['bold', 'italic']
    }); 
  } 
})

addModal.addEventListener('hidden.bs.modal', event => {
  if (addEditor) {
    addEditor.destroy()
    addEditor = null
  }
})
