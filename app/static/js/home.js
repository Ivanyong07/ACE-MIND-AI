let currentPage = 1;
    const rowsPerPage = 5;

    function updateTable() {
    const tableBody = document.getElementById("tableBody");
    const rows = tableBody.getElementsByTagName("tr");
    const totalRows = rows.length;
    const totalPages = Math.ceil(totalRows / rowsPerPage);

    // Loop through rows and show/hide based on current page
    for (let i = 0; i < totalRows; i++) {
        const start = (currentPage - 1) * rowsPerPage;
        const end = currentPage * rowsPerPage;

        if (i >= start && i < end) {
        rows[i].style.display = "";
        } else {
        rows[i].style.display = "none";
        }
    

        const table_array = rows[i].getElementsByTagName("td")
        const status = table_array[3];

        if (status) {
            const statusText = status.textContent.trim().toLowerCase();

            status.classList.remove("text-pass", "text-fail");

            if (statusText === "pass") {
                status.style.color = "#4ade80";
            } else if (statusText === "fail") {
                status.style.color = "#f87171";
            }
        }
    }

    // Update indicators and buttons
    document.getElementById("pageIndicator").textContent =
        `Page ${currentPage} of ${totalPages}`;
    document.getElementById("prevBtn").disabled = currentPage === 1;
    document.getElementById("nextBtn").disabled =
        currentPage === totalPages;
    }

    function changePage(direction) {
    currentPage += direction;
    updateTable();
    }

    // Initialize table on load
    document.addEventListener("DOMContentLoaded", updateTable);