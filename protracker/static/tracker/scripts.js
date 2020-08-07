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
    try {
        var goalEditModal = document.getElementById("goal-edit-modal");
        var goalEditButton = document.getElementById("goal-edit-button");
        var goalEditClose = document.getElementById("goal-edit-close");
        var goalAddModal = document.getElementById("goal-add-modal");
        var goalAddButton = document.getElementById("goal-add-button");
        var goalAddClose = document.getElementById("goal-add-close");
    } catch {}
    try {
        var milestoneEditModal = document.getElementById("milestone-edit-modal");
        var milestoneEditButton = document.getElementById("milestone-edit-button");
        var milestoneEditClose = document.getElementById("milestone-edit-close");
        var milestoneAddModal = document.getElementById("milestone-add-modal");
        var milestoneAddButton = document.getElementById("milestone-add-button");
        var milestoneAddClose = document.getElementById("milestone-add-close");
    } catch{}
    try {
        var rewardEditModal = document.getElementById("reward-edit-modal");
        var rewardEditButton = document.getElementById("reward-edit-button");
        var rewardEditClose = document.getElementById("reward-edit-close");
        var rewardAddModal = document.getElementById("reward-add-modal");
        var rewardAddButton = document.getElementById("reward-add-button");
        var rewardAddClose = document.getElementById("reward-add-close");
    } catch{}
    try {
        var sessionEditModal = document.getElementById("session-edit-modal");
        var sessionEditButton = document.getElementById("session-edit-button");
        var sessionEditClose = document.getElementById("session-edit-close");
        var sessionAddModal = document.getElementById("session-add-modal");
        var sessionAddButton = document.getElementById("session-add-button");
        var sessionAddClose = document.getElementById("session-add-close");
    } catch{}



    // When the user clicks on the button, open the corresponding modal
    goalEditButton.onclick = function() {
        goalEditModal.style.display = "block";
    }
    goalAddButton.onclick = function() {
        goalAddModal.style.display = "block";
    }
    milestoneEditButton.onclick = function() {
        milestoneEditModal.style.display = "block";
    }
    milestoneAddButton.onclick = function() {
        milestoneAddModal.style.display = "block";
    }
    rewardEditButton.onclick = function() {
        rewardEditModal.style.display = "block";
    }
    rewardAddButton.onclick = function() {
        rewardAddModal.style.display = "block";
    }
    sessionEditButton.onclick = function() {
        sessionEditModal.style.display = "block";
    }
    sessionAddButton.onclick = function() {
        sessionAddModal.style.display = "block";
    }

    // When the user clicks on <span> (x), close current modal
    goalEditClose.onclick = function() {
        goalEditModal.style.display = "none";
    }
    goalAddClose.onclick = function() {
        goalAddModal.style.display = "none";
    }
    milestoneEditClose.onclick = function() {
        milestoneEditModal.style.display = "none";
    }
    milestoneAddClose.onclick = function() {
        milestoneAddModal.style.display = "none";
    }
    rewardEditClose.onclick = function() {
        rewardEditModal.style.display = "none";
    }
    rewardAddClose.onclick = function() {
        rewardAddModal.style.display = "none";
    }
    sessionEditClose.onclick = function() {
        sessionEditModal.style.display = "none";
    }
    sessionAddClose.onclick = function() {
        sessionAddModal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.addEventListener("click", function(event) {
        if (event.target == goalEditModal) {goalEditModal.style.display = "none";}
        if (event.target == goalAddModal) {goalAddModal.style.display = "none";}
        if (event.target == milestoneEditModal) {milestoneEditModal.style.display = "none";}
        if (event.target == milestoneAddModal) {milestoneAddModal.style.display = "none";}
        if (event.target == rewardEditModal) {rewardEditModal.style.display = "none";}
        if (event.target == rewardAddModal) {rewardAddModal.style.display = "none";}
        if (event.target == sessionEditModal) {sessionEditModal.style.display = "none";}
        if (event.target == sessionAddModal) {sessionAddModal.style.display = "none";}
    });
};


