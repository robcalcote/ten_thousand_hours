window.onload = function() {
    document.getElementById("admin-login").onclick = function () {
        window.location.href = "//localhost:8000/admin";
    };

    if (document.body.contains(document.getElementById("user-login"))) {
        document.getElementById("user-login").onclick = function () {
            window.location.href = "//localhost:8000/tracker/login";
        };    
    }

    if (document.body.contains(document.getElementById("user-logout"))) {
        document.getElementById("user-logout").onclick = function () {
            window.location.href = "//localhost:8000/tracker/logout";
        };
    }
};


