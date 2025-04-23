function updatePagination(response) {
    let paginationContainer = $(".pagination");
    paginationContainer.empty(); // Clear existing pagination

    if (response.total_pages > 1) {
        let paginationHtml = '<div class="pagination-links">';

        if (response.has_previous) {
            paginationHtml += `<button class="pagination-link" data-page="1">« First</button>`;
            paginationHtml += `<button class="pagination-link" data-page="${response.current_page - 1}">Previous</button>`;
        }

        paginationHtml += `<span> Page ${response.current_page} of ${response.total_pages} </span>`;

        if (response.has_next) {
            paginationHtml += `<button class="pagination-link" data-page="${response.current_page + 1}">Next</button>`;
            paginationHtml += `<button class="pagination-link" data-page="${response.total_pages}">Last »</button>`;
        }

        paginationHtml += '</div>';
        paginationContainer.append(paginationHtml);
    }
}
