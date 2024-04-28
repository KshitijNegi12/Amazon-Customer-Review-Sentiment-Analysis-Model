function toggleInput() {
    var inputType = document.getElementById("inputType").value;
    var textInput = document.getElementById("textInput");
    var linkInput = document.getElementById("linkInput");
    if (inputType === "text") {
        textInput.style.display = "flex";
        linkInput.style.display = "none";
        linkInput.querySelector('textarea').removeAttribute('id');
        textInput.querySelector('textarea').setAttribute('id', 'textarea');
    } else {
        textInput.style.display = "none";
        linkInput.style.display = "flex";
        textInput.querySelector('textarea').removeAttribute('id');
        linkInput.querySelector('textarea').setAttribute('id', 'textarea');
    }
}

function autoResizeTextarea() {
    const textInput = document.getElementById('textarea');
    const lines = textInput.value.split('\n').length;
    textInput.rows = Math.min(lines, 3);
}

document.getElementById('textarea').addEventListener('input', autoResizeTextarea);

function followup(button, event) {
    document.getElementById('loading').style.display='block';
    event.preventDefault();
    button.disabled = true;
    setTimeout(function() {
        document.getElementById('myform').submit();
    }, 100);
}


// function rightpage(){
//     var textInput = document.getElementById("textInput");
//     var linkInput = document.getElementById("linkInput");
//     document.getElementById('result')
//     textInput.style.display = "none";
//     linkInput.style.display = "flex";
//     textInput.querySelector('textarea').removeAttribute('id');
//     linkInput.querySelector('textarea').setAttribute('id', 'textarea');
// }