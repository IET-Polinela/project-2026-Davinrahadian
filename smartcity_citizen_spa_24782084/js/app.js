const app = document.getElementById("app");

let currentTab = "my_reports";
let currentPage = 1;
let currentReports = [];
let editingReportId = null;
let clickedSubmitStatus = "DRAFT";

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderLoginPage() {
    app.innerHTML = `
        <section class="row justify-content-center align-items-center login-shell page-enter">
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

function reportStatusProgress(status) {
    const progressMap = {
        DRAFT: 20,
        REPORTED: 40,
        VERIFIED: 60,
        IN_PROGRESS: 80,
        RESOLVED: 100,
    };

    return progressMap[status] || 20;
}

function getPaginationItems(data) {
    const items = Array.isArray(data) ? data : data.results || [];
    const total = Array.isArray(data) ? data.length : data.count || items.length;

    return { items, total, next: data.next, previous: data.previous };
}

async function renderDashboardPage() {
    currentTab = "my_reports";
    currentPage = 1;

    app.innerHTML = `
        <section class="mb-4 page-enter">
            <div class="d-flex flex-column flex-lg-row justify-content-between gap-3">
                <div>
                    <p class="small-muted mb-1">Dashboard Citizen</p>
                    <h1 class="h3 fw-bold mb-1">Smart City Citizen Portal</h1>
                    <p class="small-muted mb-0">Kelola laporan kota, pantau status, dan simpan draft sebelum diajukan.</p>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <span class="status-dot"></span>
                    <span class="small-muted">Terhubung ke backend Django</span>
                </div>
            </div>
        </section>

        <section class="row g-3 page-enter page-enter-delay">
            <aside class="col-12 col-lg-3">
                <div class="dashboard-panel motion-card p-3 h-100">
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
                    <button class="btn btn-primary w-100 mb-2" type="button" id="addReportButton">
                        <i class="bi bi-plus-circle me-2"></i>Tambah Laporan Baru
                    </button>
                    <button class="btn btn-outline-danger w-100" type="button" id="dashboardLogoutButton">
                        <i class="bi bi-box-arrow-right me-2"></i>Logout
                    </button>
                    <hr>
                    <h2 class="h6 fw-bold mb-3">Rekap Status</h2>
                    <div class="list-group list-group-flush">
                        <div class="list-group-item px-0 d-flex justify-content-between">
                            <span class="small-muted">Draft</span>
                            <span class="fw-bold" id="sidebarDraftReports">-</span>
                        </div>
                        <div class="list-group-item px-0 d-flex justify-content-between">
                            <span class="small-muted">Diproses</span>
                            <span class="fw-bold" id="sidebarProgressReports">-</span>
                        </div>
                        <div class="list-group-item px-0 d-flex justify-content-between">
                            <span class="small-muted">Selesai</span>
                            <span class="fw-bold" id="sidebarResolvedReports">-</span>
                        </div>
                    </div>
                </div>
            </aside>

            <main class="col-12 col-lg-6">
                <div class="dashboard-panel motion-card p-3 mb-3">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div>
                            <h2 class="h6 fw-bold mb-1">Ringkasan Laporan Saya</h2>
                            <p class="small-muted mb-0">Rekap dihitung dari endpoint protected dengan page_size besar.</p>
                        </div>
                        <i class="bi bi-clipboard-data text-primary fs-4"></i>
                    </div>
                    <div class="row g-3" id="dashboardMetrics">
                        <div class="col-12 col-md-4">
                            <div class="surface-muted p-3 rounded border">
                                <p class="small-muted mb-1">Draft</p>
                                <p class="metric-value mb-0" id="draftReports">-</p>
                            </div>
                        </div>
                        <div class="col-12 col-md-4">
                            <div class="surface-muted p-3 rounded border">
                                <p class="small-muted mb-1">Diproses</p>
                                <p class="metric-value mb-0" id="progressReports">-</p>
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

                <div class="dashboard-panel motion-card p-3">
                    <div class="d-flex flex-column flex-sm-row justify-content-between align-items-sm-center gap-2 mb-3">
                        <h2 class="h6 fw-bold mb-0">Daftar Laporan</h2>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-primary active" type="button" data-tab="my_reports">Laporan Saya</button>
                            <button class="btn btn-outline-primary" type="button" data-tab="feed">Feed Kota</button>
                        </div>
                    </div>
                    <div id="reportList">
                        <div class="text-center py-4 small-muted">
                            <div class="spinner-border spinner-border-sm me-2"></div>Memuat data laporan
                        </div>
                    </div>
                    <div id="paginationControls" class="d-flex justify-content-between align-items-center mt-3"></div>
                </div>
            </main>

            <aside class="col-12 col-lg-3">
                <div class="dashboard-panel motion-card p-3 h-100">
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
                            <span class="small-muted">Pagination</span>
                            <span class="fw-semibold">Aktif</span>
                        </div>
                        <div class="list-group-item px-0 d-flex justify-content-between">
                            <span class="small-muted">Filter</span>
                            <span class="fw-semibold">Server-side</span>
                        </div>
                    </div>
                </div>
            </aside>
        </section>
    `;

    document.getElementById("dashboardLogoutButton").addEventListener("click", logout);
    document.getElementById("addReportButton").addEventListener("click", openCreateReportModal);
    document.querySelectorAll("[data-tab]").forEach((button) => {
        button.addEventListener("click", () => changeTab(button.dataset.tab));
    });

    setupReportForm();
    await loadDashboardData();
}

function setupReportForm() {
    const reportForm = document.getElementById("reportForm");

    reportForm.querySelectorAll("[data-submit-status]").forEach((button) => {
        button.onclick = () => {
            clickedSubmitStatus = button.dataset.submitStatus;
            submitReportForm(clickedSubmitStatus);
        };
    });

    reportForm.onsubmit = (event) => event.preventDefault();
}

async function changeTab(tab) {
    currentTab = tab;
    currentPage = 1;

    document.querySelectorAll("[data-tab]").forEach((button) => {
        button.classList.toggle("active", button.dataset.tab === tab);
    });

    await loadDashboardData();
}

async function loadDashboardData() {
    await Promise.all([loadSummaryStats(), loadReportList()]);
}

async function loadSummaryStats() {
    try {
        const data = await requestAPI("/api/reports/?tab=my_reports&page_size=1000", "GET");
        const { items } = getPaginationItems(data);

        const draftCount = items.filter((report) => report.status === "DRAFT").length;
        const progressCount = items.filter((report) => ["REPORTED", "VERIFIED", "IN_PROGRESS"].includes(report.status)).length;
        const resolvedCount = items.filter((report) => report.status === "RESOLVED").length;

        document.getElementById("draftReports").textContent = draftCount;
        document.getElementById("progressReports").textContent = progressCount;
        document.getElementById("resolvedReports").textContent = resolvedCount;
        document.getElementById("sidebarDraftReports").textContent = draftCount;
        document.getElementById("sidebarProgressReports").textContent = progressCount;
        document.getElementById("sidebarResolvedReports").textContent = resolvedCount;
    } catch (error) {
        document.getElementById("draftReports").textContent = "-";
        document.getElementById("progressReports").textContent = "-";
        document.getElementById("resolvedReports").textContent = "-";
        document.getElementById("sidebarDraftReports").textContent = "-";
        document.getElementById("sidebarProgressReports").textContent = "-";
        document.getElementById("sidebarResolvedReports").textContent = "-";
    }
}

async function loadReportList() {
    const reportList = document.getElementById("reportList");
    const paginationControls = document.getElementById("paginationControls");

    reportList.innerHTML = `
        <div class="text-center py-4 small-muted">
            <div class="spinner-border spinner-border-sm me-2"></div>Memuat data laporan
        </div>
    `;

    try {
        const data = await requestAPI(`/api/reports/?tab=${currentTab}&page=${currentPage}&page_size=5`, "GET");
        const { items, total, next, previous } = getPaginationItems(data);
        currentReports = items;

        if (!items.length) {
            reportList.innerHTML = '<p class="small-muted mb-0">Belum ada data laporan pada tab ini.</p>';
            paginationControls.innerHTML = "";
            return;
        }

        reportList.innerHTML = items.map(renderReportCard).join("");
        renderPagination(total, next, previous);
        bindReportActions();
    } catch (error) {
        reportList.innerHTML = `
            <div class="alert alert-warning mb-0" role="alert">
                Data laporan belum bisa dimuat. ${escapeHtml(error.message)}
            </div>
        `;
        paginationControls.innerHTML = "";
    }
}

function renderReportCard(report) {
    const canManageDraft = report.is_owner && report.status === "DRAFT";
    const progress = reportStatusProgress(report.status);
    const actions = canManageDraft ? `
        <div class="d-flex flex-column gap-2 report-card-action">
            <button class="btn btn-sm btn-outline-primary" type="button" data-edit-id="${report.id}">
                <i class="bi bi-pencil-square me-1"></i>Edit
            </button>
            <button class="btn btn-sm btn-success" type="button" data-submit-draft-id="${report.id}">
                <i class="bi bi-send me-1"></i>Ajukan
            </button>
            <button class="btn btn-sm btn-outline-danger" type="button" data-delete-id="${report.id}">
                <i class="bi bi-trash me-1"></i>Hapus
            </button>
        </div>
    ` : "";

    return `
        <article class="report-item border-top py-3">
            <div class="d-flex flex-column flex-md-row justify-content-between gap-3">
                <div>
                    <div class="d-flex flex-wrap align-items-center gap-2 mb-1">
                        <p class="fw-semibold mb-0">${escapeHtml(report.title)}</p>
                        <span class="badge text-bg-${reportStatusBadge(report.status)}">${escapeHtml(report.status)}</span>
                        ${report.is_owner ? '<span class="badge text-bg-light border">Milik saya</span>' : ""}
                    </div>
                    <p class="small-muted mb-1">Pelapor: ${escapeHtml(report.reporter)}</p>
                    <p class="small-muted mb-1">${escapeHtml(report.location)}</p>
                    <p class="small-muted mb-2">${escapeHtml(report.description)}</p>
                    <div class="progress" style="height: 8px;" aria-label="Progress status laporan">
                        <div class="progress-bar bg-${reportStatusBadge(report.status)}" style="width: ${progress}%"></div>
                    </div>
                </div>
                ${actions}
            </div>
        </article>
    `;
}

function renderPagination(total, next, previous) {
    document.getElementById("paginationControls").innerHTML = `
        <span class="small-muted">Total data: ${total}</span>
        <div class="btn-group btn-group-sm">
            <button class="btn btn-outline-secondary" type="button" id="prevPageButton" ${previous ? "" : "disabled"}>
                Sebelumnya
            </button>
            <button class="btn btn-outline-secondary" type="button" disabled>Halaman ${currentPage}</button>
            <button class="btn btn-outline-secondary" type="button" id="nextPageButton" ${next ? "" : "disabled"}>
                Berikutnya
            </button>
        </div>
    `;

    document.getElementById("prevPageButton").addEventListener("click", async () => {
        currentPage -= 1;
        await loadReportList();
    });

    document.getElementById("nextPageButton").addEventListener("click", async () => {
        currentPage += 1;
        await loadReportList();
    });
}

function bindReportActions() {
    document.querySelectorAll("[data-edit-id]").forEach((button) => {
        button.addEventListener("click", () => editDraft(Number(button.dataset.editId)));
    });

    document.querySelectorAll("[data-submit-draft-id]").forEach((button) => {
        button.addEventListener("click", () => submitDraft(Number(button.dataset.submitDraftId)));
    });

    document.querySelectorAll("[data-delete-id]").forEach((button) => {
        button.addEventListener("click", () => deleteDraft(Number(button.dataset.deleteId)));
    });
}

function getReportPayload(status) {
    return {
        title: document.getElementById("reportTitle").value.trim(),
        category: document.getElementById("reportCategory").value,
        location: document.getElementById("reportLocation").value.trim(),
        description: document.getElementById("reportDescription").value.trim(),
        status,
    };
}

function openCreateReportModal() {
    editingReportId = null;
    clickedSubmitStatus = "DRAFT";
    document.getElementById("reportModalTitle").textContent = "Tambah Laporan Baru";
    document.getElementById("reportFormAlert").innerHTML = "";
    document.getElementById("reportForm").reset();

    bootstrap.Modal.getOrCreateInstance(document.getElementById("reportModal")).show();
}

function editDraft(id) {
    const report = currentReports.find((item) => item.id === id);
    if (!report) {
        return;
    }

    editingReportId = id;
    clickedSubmitStatus = report.status;
    document.getElementById("reportModalTitle").textContent = "Edit Draft Laporan";
    document.getElementById("reportFormAlert").innerHTML = "";
    document.getElementById("reportTitle").value = report.title;
    document.getElementById("reportCategory").value = report.category;
    document.getElementById("reportLocation").value = report.location;
    document.getElementById("reportDescription").value = report.description;

    bootstrap.Modal.getOrCreateInstance(document.getElementById("reportModal")).show();
}

async function submitReportForm(status) {
    const reportForm = document.getElementById("reportForm");
    if (!reportForm.reportValidity()) {
        reportForm.reportValidity();
        return;
    }

    const method = editingReportId === null ? "POST" : "PUT";
    const endpoint = editingReportId === null ? "/api/reports/" : `/api/reports/${editingReportId}/`;
    const payload = getReportPayload(status);

    try {
        await requestAPI(endpoint, method, payload);
        bootstrap.Modal.getOrCreateInstance(document.getElementById("reportModal")).hide();
        reportForm.reset();
        editingReportId = null;
        currentTab = "my_reports";
        currentPage = 1;
        await loadDashboardData();
    } catch (error) {
        document.getElementById("reportFormAlert").innerHTML = `
            <div class="alert alert-danger" role="alert">${escapeHtml(error.message)}</div>
        `;
    }
}

async function submitDraft(id) {
    const report = currentReports.find((item) => item.id === id);
    if (!report) {
        return;
    }

    const payload = {
        title: report.title,
        category: report.category,
        location: report.location,
        description: report.description,
        status: "REPORTED",
    };

    try {
        await requestAPI(`/api/reports/${id}/`, "PUT", payload);
        await loadDashboardData();
    } catch (error) {
        alert(`Gagal mengajukan draft: ${error.message}`);
    }
}

async function deleteDraft(id) {
    const confirmed = confirm("Hapus draft laporan ini?");
    if (!confirmed) {
        return;
    }

    try {
        await requestAPI(`/api/reports/${id}/`, "DELETE");
        await loadDashboardData();
    } catch (error) {
        alert(`Gagal menghapus draft: ${error.message}`);
    }
}

document.getElementById("logoutButton").addEventListener("click", logout);
