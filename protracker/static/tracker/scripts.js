window.onload = function() {
    
    if (document.body.contains(document.getElementById("admin-login-button"))) {
        document.getElementById("admin-login-button").onclick = function () {
            window.location.href = "//localhost:8000/admin";
        };    
    }

    if (document.body.contains(document.getElementById("user-login-button"))) {
        document.getElementById("user-login-button").onclick = function () {
            window.location.href = "//localhost:8000/tracker/login";
        };    
    }

    if (document.body.contains(document.getElementById("user-logout-button"))) {
        document.getElementById("user-logout-button").onclick = function () {
            window.location.href = "//localhost:8000/tracker/logout";
        };
    }

    if (document.body.contains(document.getElementById("dashboard-button"))) {
        document.getElementById("dashboard-button").onclick = function () {
            window.location.href = "//localhost:8000/tracker/dashboard/";
        };
    }



    // TEST MODAL CODE
    // Get the modal
    var modal = document.getElementById("edit-record-modal");

    // Get the button that opens the modal
    var btn = document.getElementById("edit-record-button");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close-modal")[0];

    // When the user clicks on the button, open the modal
    btn.onclick = function() {
    modal.style.display = "block";
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
    modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
    }
};


