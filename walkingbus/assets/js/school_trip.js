function checkTripState() {
    return new Promise(function (resolve) {
        var xhr = new XMLHttpRequest();
        xhr.onload = function () {
            var responseJson = JSON.parse(xhr.responseText);
            var _progress = responseJson.progress;
            resolve(_progress);
        };
        xhr.open('GET', '/api/progress');
        xhr.send();
    });
}

async function refresh(lastProgress) {
    if (await checkTripState() !== lastProgress)
        document.location.reload();
}

function updateParticipants() {
    var form = document.getElementById('participants');
    var formData = new FormData(form);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', window.location.href);
    xhr.send(formData);
}

function updatePassengers() {
    return new Promise(function (resolve) {
        var form = document.getElementById('passengers');
        var formData = new FormData(form);
        var xhr = new XMLHttpRequest();
        xhr.onload = resolve;
        xhr.open('POST', window.location.href);
        xhr.send(formData);
    });
}
