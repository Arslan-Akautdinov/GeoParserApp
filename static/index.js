if (window.location == "")
{
    window.location.replace("./");
}

var upload = function (files)
{
    var file = files[0];
    document.getElementById("title").textContent = file.name
    document.getElementById("send_btn").style.display = "block"
}