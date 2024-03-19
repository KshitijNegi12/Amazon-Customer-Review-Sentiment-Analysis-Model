function toggleInput() {
    var inputType = document.getElementById("inputType").value;
    var textInput = document.getElementById("textInput");
    var linkInput = document.getElementById("linkInput");

    if (inputType === "text") {
        textInput.style.display = "block";
        linkInput.style.display = "none";
    } else {
        textInput.style.display = "none";
        linkInput.style.display = "block";
    }
}

