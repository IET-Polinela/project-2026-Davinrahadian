const routes = {
    "#login": renderLoginPage,
    "#dashboard": renderDashboardPage,
};

function router() {
    const hash = window.location.hash || "#login";
    const protectedRoutes = ["#dashboard"];

    if (protectedRoutes.includes(hash) && !isAuthenticated()) {
        window.location.hash = "#login";
        return;
    }

    const render = routes[hash] || renderLoginPage;
    render();
}

window.addEventListener("hashchange", router);
window.addEventListener("load", router);
