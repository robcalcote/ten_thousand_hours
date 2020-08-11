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

    // try/catches for each modal load in the event that modals aren't included in pages
    try {
        var goalAddModal = document.getElementById("goal-add-modal");
        var goalAddButton = document.getElementById("goal-add-button");
        var goalAddClose = document.getElementById("goal-add-close");
        goalAddButton.onclick = function() {
            goalAddModal.style.display = "block";
        }
        goalAddClose.onclick = function() {
            goalAddModal.style.display = "none";
        }
    } catch {}
    try {
        var goalEditModal = document.getElementById("goal-edit-modal");
        var goalEditButton = document.getElementById("goal-edit-button");
        var goalEditClose = document.getElementById("goal-edit-close");
        goalEditButton.onclick = function() {
            goalEditModal.style.display = "block";
        }
        goalEditClose.onclick = function() {
            goalEditModal.style.display = "none";
        }
    } catch {}
    try {
        var milestoneAddModal = document.getElementById("milestone-add-modal");
        var milestoneAddButton = document.getElementById("milestone-add-button");
        var milestoneAddClose = document.getElementById("milestone-add-close");
        milestoneAddButton.onclick = function() {
            milestoneAddModal.style.display = "block";
        }
        milestoneAddClose.onclick = function() {
            milestoneAddModal.style.display = "none";
        }
    } catch {}
    try {
        var milestoneEditModal = document.getElementById("milestone-edit-modal");
        var milestoneEditButton = document.getElementById("milestone-edit-button");
        var milestoneEditClose = document.getElementById("milestone-edit-close");
        milestoneEditButton.onclick = function() {
            milestoneEditModal.style.display = "block";
        }
        milestoneEditClose.onclick = function() {
            milestoneEditModal.style.display = "none";
        }
    } catch{}
    try {
        var rewardAddModal = document.getElementById("reward-add-modal");
        var rewardAddButton = document.getElementById("reward-add-button");
        var rewardAddClose = document.getElementById("reward-add-close");
        rewardAddButton.onclick = function() {
            rewardAddModal.style.display = "block";
        }
        rewardAddClose.onclick = function() {
            rewardAddModal.style.display = "none";
        }
    } catch{}
    try {
        var rewardEditModal = document.getElementById("reward-edit-modal");
        var rewardEditButton = document.getElementById("reward-edit-button");
        var rewardEditClose = document.getElementById("reward-edit-close");
        rewardEditButton.onclick = function() {
            rewardEditModal.style.display = "block";
        }
        rewardEditClose.onclick = function() {
            rewardEditModal.style.display = "none";
        }
    } catch{}
    try {
        var sessionAddModal = document.getElementById("session-add-modal");
        var sessionAddButton = document.getElementById("session-add-button");
        var sessionAddClose = document.getElementById("session-add-close");
        sessionAddButton.onclick = function() {
            sessionAddModal.style.display = "block";
        }
        sessionAddClose.onclick = function() {
            sessionAddModal.style.display = "none";
        }
    } catch{}
    try {
        var sessionEditModal = document.getElementById("session-edit-modal");
        var sessionEditButton = document.getElementById("session-edit-button");
        var sessionEditClose = document.getElementById("session-edit-close");
        sessionEditButton.onclick = function() {
            sessionEditModal.style.display = "block";
        }
        sessionEditClose.onclick = function() {
            sessionEditModal.style.display = "none";
        }
    } catch{}
    
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

