// script.js

document.addEventListener("DOMContentLoaded", function () {
    // Navigation for signup and login buttons
    const signInBtn = document.querySelector(".sign-in");
    const createAccountBtn = document.querySelector(".create-account");
    const loginBtn = document.getElementById("loginBtn");
    const uploadForm = document.querySelector("form");
    const downloadBtn = document.getElementById("download-btn");

    if (signInBtn) {
        signInBtn.addEventListener("click", function () {
            window.location.href = "signup.html";
        });
    }

    if (createAccountBtn) {
        createAccountBtn.addEventListener("click", function () {
            window.location.href = "signup.html";
        });
    }

    if (loginBtn) {
        loginBtn.addEventListener("click", function () {
            window.location.href = "upload.html";
        });
    }

    if (uploadForm) {
        uploadForm.addEventListener("submit", function (event) {
            event.preventDefault();
            alert("Processing your file... Please wait.");
            setTimeout(() => {
                if (downloadBtn) {
                    downloadBtn.classList.remove("hidden");
                }
            }, 3000);
        });
    }

    if (downloadBtn) {
        downloadBtn.addEventListener("click", function () {
            alert("Your cleaned file is ready for download!");
        });
    }
});
