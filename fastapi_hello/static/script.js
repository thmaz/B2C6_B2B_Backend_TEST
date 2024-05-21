function getMessage() {
    var xhr = new XMLHttpRequest;
    xhr.open("GET", "http://0.0.0.0:8000/data", true);
    xhr.onreadystatechange = function() {
        console.log(xhr.responseText);
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            document.getElementById("message").innerHTML = response.message;
        }
    }
    xhr.send();
}

window.onload = function() {
    getMessage();
}