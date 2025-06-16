
const openFileBtn = document.getElementById('openFileBtn');
const fileInput = document.getElementById('fileInput');
const output = document.getElementById('output')
const selectFileBtn = document.getElementById('selectFileBtn')

//seleccionamos el archivo
selectFileBtn.addEventListener('click', () =>{
    fileInput.click();
})

//mostrar el nombre del archivo
fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0){
        alert('archivo seleccionado: '+fileInput.files[0].name);
    }
})

//subir el archivo
openFileBtn.addEventListener('click', () => {
    const file = fileInput.files[0];
    if (!file){
        alert('por favor seleccione un archivo');
        return;
    }
    const formData = new FormData()
    formData.append('file', file);

    fetch('/upload',{
        method : 'POST',
        body : formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error){
            alert('error: '+data.error);
        }
        else {
            //mostrar el contenido json en el text area
            output.value = JSON.stringify(data, null, 2);


        }
    })
    .catch(error => {
        alert('error al subir el archivo');
        console.error(error);
    });
});

fileInput.addEventListener('change', () => {

    if (fileInput.files.length > 0) {
        alert('archivo seleccionado: ' + fileInput.files[0].name);
    }
});