const app = document.getElementById("app");

function renderLoginPage() {
    app.innerHTML = `
        <section class="row justify-content-center align-items-center login-shell">
            <div class="col-12 col-md-8 col-lg-5 col-xl-4">
                <div class="portal-card p-4">
                    <div class="mb-4">
                        <p class="small-muted mb-1">Smart City Citizen Portal</p>
                        <h1 class="h3 fw-bold mb-2">Login Citizen</h1>
                        <p class="small-muted mb-0">Masuk menggunakan akun yang sudah terdaftar pada backend Smart City.</p>
                    </div>
                    <div id="loginAlert"></div>
                    <form id="loginForm">
                        <div class="mb-3">
                            <label for="username" class="form-label">Username</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="bi bi-person"></i></span>
                                <input type="text" class="form-control" id="username" placeholder="Masukkan username" required>
                            </div>
                        </div>
                        <div class="mb-4">
                            <label for="password" class="form-label">Password</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="bi bi-lock"></i></span>
                                <input type="password" class="form-control" id="password" placeholder="Masukkan password" required>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">
                            <i class="bi bi-box-arrow-in-right me-2"></i>Login
                        </button>
                    </form>
                </div>
            </div>
        </section>
    `;

    setupLoginForm();
}

function reportStatusBadge(status) {
    const badgeMap = {
        DRAFT: "secondary",
        REPORTED: "primary",
        VERIFIED: "info",
        IN_PROGRESS: "warning",
        RESOLVED: "success",
    };

    return badgeMap[status] || "secondary";
}

async function renderDashboardPage() {
    app.innerHTML = `
        <section class="mb-4">
            <div class="d-flex flex-column flex-lg-row justify-content-between gap-3">
                <div>
                    <p class="small-muted mb-1">Dashboard Citizen</p>
                    <h1 class="h3 fw-bold mb-1">Smart City Citizen Portal</h1>
                    <p class="small-muted mb-0">Pantau ringkasan laporan dan status layanan kota secara ringkas.</p>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <span class="status-dot"></span>
                    <span class="small-muted">Terhubung ke backend Django</span>
                </div>
            </div>
        </section>

        <section class="row g-3">
            <aside class="col-12 col-lg-3">
                <div class="dashboard-panel p-3 h-100">
                    <h2 class="h6 fw-bold mb-3">Akun</h2>
                    <div class="d-flex align-items-center gap-3 mb-3">
                        <div class="rounded-circle bg-primary-subtle text-primary d-flex align-items-center justify-content-center" style="width: 44px; height: 44px;">
                            <i class="bi bi-person-check"></i>
                        </div>
                        <div>
                            <p class="mb-0 fw-semibold">Citizen User</p>
                            <p class="small-muted mb-0">JWT authenticated</p>
                        </div>
                    </div>
                    <button class="btn btn-outline-danger w-100" type="button" id="dashboardLogoutButton">
                        <i class="bi bi-box-arrow-right me-2"></i>Logout
                    </button>
                </div>
            </aside>

            <main class="col-12 col-lg-6">
                <div class="dashboard-panel p-3 mb-3">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div>
                            <h2 class="h6 fw-bold mb-1">Ringkasan Laporan</h2>
                            <p class="small-muted mb-0">Data diambil dari endpoint protected.</p>
                        </div>
                        <i class="bi bi-clipboard-data text-primary fs-4"></i>
                    </div>
                    <div class="row g-3" id="dashboardMetrics">
                        <div class="col-12 col-md-4">
                            <div class="surface-muted p-3 rounded border">
                                <p class="small-muted mb-1">Total</p>
                                <p class="metric-value mb-0" id="totalReports">-</p>
                            </div>
                        </div>
                        <div class="col-12 col-md-4">
                            <div class="surface-muted p-3 rounded border">
                                <p class="small-muted mb-1">Draft</p>
                                <p class="metric-value mb-0" id="draftReports">-</p>
                            </div>
                        </div>
                        <div class="col-12 col-md-4">
                            <div class="surface-muted p-3 rounded border">
                                <p class="small-muted mb-1">Selesai</p>
                                <p class="metric-value mb-0" id="resolvedReports">-</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="dashboard-panel p-3">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h2 class="h6 fw-bold mb-0">Laporan Terbaru</h2>
                        <span class="badge text-bg-light border">Live API</span>
                    </div>
                    <div id="reportList">
                        <div class="text-center py-4 small-muted">
                            <div class="spinner-border spinner-border-sm me-2"></div>Memuat data laporan
                        </div>
                    </div>
                </div>
            </main>

            <aside class="col-12 col-lg-3">
                <div class="dashboard-panel p-3 h-100">
                    <h2 class="h6 fw-bold mb-3">Status Sistem</h2>
                    <div class="list-group list-group-flush">
                        <div class="list-group-item px-0 d-flex justify-content-between">
                            <span class="small-muted">API</span>
                            <span class="text-success fw-semibold">Online</span>
                        </div>
                        <div class="list-group-item px-0 d-flex justify-content-between">
                            <span class="small-muted">Auth</span>
                            <span class="text-success fw-semibold">JWT</span>
                        </div>
                        <div class="list-group-item px-0 d-flex justify-content-between">
                            <span class="small-muted">Layout</span>
                            <span class="fw-semibold">Responsive</span>
                        </div>
                    </div>
                </div>
            </aside>
        </section>
    `;

    document.getElementById("dashboardLogoutButton").addEventListener("click", logout);
    await loadDashboardReports();
}

async function loadDashboardReports() {
    const reportList = document.getElementById("reportList");

    try {
        const reports = await requestAPI("/api/reports/", "GET");
        const reportArray = Array.isArray(reports) ? reports : [];
        const latestReports = reportArray.slice(0, 5);

        document.getElementById("totalReports").textContent = reportArray.length;
        document.getElementById("draftReports").textContent = reportArray.filter((report) => report.status === "DRAFT").length;
        document.getElementById("resolvedReports").textContent = reportArray.filter((report) => report.status === "RESOLVED").length;

        if (!latestReports.length) {
            reportList.innerHTML = '<p class="small-muted mb-0">Belum ada data laporan.</p>';
            return;
        }

        reportList.innerHTML = latestReports.map((report) => `
            <div class="border-top py-3">
                <div class="d-flex justify-content-between gap-3">
                    <div>
                        <p class="fw-semibold mb-1">${report.title}</p>
                        <p class="small-muted mb-0">${report.location}</p>
                    </div>
                    <span class="badge text-bg-${reportStatusBadge(report.status)} align-self-start">${report.status}</span>
                </div>
            </div>
        `).join("");
    } catch (error) {
        reportList.innerHTML = `
            <div class="alert alert-warning mb-0" role="alert">
                Data laporan belum bisa dimuat. Pastikan backend berjalan dan token masih valid.
            </div>
        `;
    }
}

document.getElementById("logoutButton").addEventListener("click", logout);
