function followup(button, event) {
    document.getElementById('loading').style.display='flex';
    event.preventDefault();
    button.disabled = true;
    setTimeout(function() {
        document.getElementById('myform').submit();
    }, 100);
}