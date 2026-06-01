function isAuthenticated() {
    return Boolean(localStorage.getItem("access_token"));
}

function setupLoginForm() {
    const form = document.getElementById("loginForm");
    if (!form) {
        return;
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;
        const alertBox = document.getElementById("loginAlert");
        const submitButton = form.querySelector("button[type='submit']");

        alertBox.innerHTML = "";
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Memproses';

        try {
            const result = await requestAPI("/api/token/", "POST", { username, password });

            localStorage.setItem("access_token", result.access);
            localStorage.setItem("refresh_token", result.refresh);

            alertBox.innerHTML = `
                <div class="alert alert-success mb-3" role="alert">
                    Login berhasil. Anda akan diarahkan ke dashboard.
                </div>
            `;

            window.location.hash = "#dashboard";
        } catch (error) {
            alertBox.innerHTML = `
                <div class="alert alert-danger mb-3" role="alert">
                    Login gagal. ${error.message}
                </div>
            `;
        } finally {
            submitButton.disabled = false;
            submitButton.innerHTML = '<i class="bi bi-box-arrow-in-right me-2"></i>Login';
        }
    });
}

function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.hash = "#login";
}
