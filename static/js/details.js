var modal = document.getElementById('my_modal');
var closeBtn = document.getElementsByClassName("close")[0];


window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

closeBtn.onclick = function() {
	modal.style.display = "none";
}