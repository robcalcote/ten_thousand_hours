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

    // Get the modal
    var goalEditModal = document.getElementById("goal-edit-modal");
    var goalEditButton = document.getElementById("goal-edit-button");
    var goalEditClose = document.getElementById("goal-edit-close");
    var goalAddModal = document.getElementById("goal-add-modal");
    var goalAddButton = document.getElementById("goal-add-button");
    var goalAddClose = document.getElementById("goal-add-close");

    // When the user clicks on the button, open the corresponding modal
    goalEditButton.onclick = function() {
        goalEditModal.style.display = "block";
    }
    goalAddButton.onclick = function() {
        goalAddModal.style.display = "block";
    }

    // When the user clicks on <span> (x), close current modal
    goalEditClose.onclick = function() {
        goalEditModal.style.display = "none";
    }
    goalAddClose.onclick = function() {
        goalAddModal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == goalEditModal) {goalEditModal.style.display = "none";}
        if (event.target == goalAddModal) {goalAddModal.style.display = "none";}
    }
};


