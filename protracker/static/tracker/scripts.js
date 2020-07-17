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
};


