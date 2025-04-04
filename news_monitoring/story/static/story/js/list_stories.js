//
//$(document).ready(function () {
//
//    // Fetch stories on page load
//    fetchStories();
//
//    // Fetch stories when search input changes or date filter changes
//    $("#search-title, #filter-date").on("input change", fetchStories);
//});
//
//function fetchStories() {
//        $.ajax({
//            url: storyListUrl,
//            data: {
//                q: $("#search-title").val().trim(),
//                date: $("#filter-date").val()
//            },
//            dataType: "json",
//            success: function (response) {
//                console.log(response);
//                let storiesList = $("#stories-list");
//                storiesList.empty(); // Clear previous content
//
//                if (response.stories.length === 0) {
//                    console.log("Zero")
//                    storiesList.append("<p>No results found.</p>");
//                    return;
//                }
//
//                response.stories.forEach(story => {
//                    console.log("Loop",response)
//                    storiesList.append(`
//                        <div class="story-card">
//                            <h3 class="story-title">
//                                <a href="${story.article_url}" target="_blank">${story.title}</a>
//                            </h3>
//                            <p class="story-date"><strong>Published Date:</strong> ${story.published_date}</p>
//                            <p class="story-body">${story.body_text}</p>
//                            <p class="story-companies"><strong>Tagged Companies:</strong> ${story.tagged_companies.join(", ")}</p>
//                            <div class="story-actions">
//                                <a href="/story/edit/${story.id}/" class="btn edit-btn">Edit</a>
//                                <a href="/story/delete/${story.id}/" class="btn delete-btn" onclick="return confirm('Are you sure?');">Delete</a>
//                            </div>
//                        </div>`);
//                });
//            }
//        });
//    }
$(document).ready(function () {
    fetchStories(1);  // Load the first page on initial page load

    // Search and filter event
    $("#search-title, #filter-date").on("input change", function () {
        fetchStories(1);  // Reset to first page on new search
    });

    // Pagination event handlers (will be dynamically added later)
    $(document).on("click", ".pagination-link", function (e) {
        e.preventDefault();
        let page = $(this).data("page");  // Get the page number from button
        fetchStories(page);
    });
});

function fetchStories(page = 1) {
    $.ajax({
        url: storyListUrl,
        data: {
            q: $("#search-title").val().trim(),
            date: $("#filter-date").val(),
            page: page  // Pass the selected page number
        },
        dataType: "json",
        success: function (response) {
            let storiesList = $("#stories-list");
            storiesList.empty(); // Clear previous content

            if (!response.stories || response.stories.length === 0) {
                storiesList.append("<p>No results found.</p>");
                return;
            }

            response.stories.forEach(story => {
                let companies = story.tagged_companies.length
                    ? story.tagged_companies.join(", ")
                    : "No companies tagged";

                storiesList.append(`
                    <div class="story-card">
                        <h3 class="story-title">
                            <a href="${story.article_url}" target="_blank">${story.title}</a>
                        </h3>
                        <p class="story-date"><strong>Published Date:</strong> ${story.published_date || "N/A"}</p>
                        <p class="story-body">${story.body_text}</p>
                        <p class="story-companies"><strong>Tagged Companies:</strong> ${companies}</p>
                        <div class="story-actions">
                            <a href="/story/edit/${story.id}/" class="btn edit-btn">Edit</a>
                            <a href="/story/delete/${story.id}/" class="btn delete-btn" onclick="return confirm('Are you sure?');">Delete</a>
                        </div>
                    </div>`);
            });

            // Update pagination controls
            updatePagination(response);
        },
        error: function (xhr) {
            console.error("AJAX Error:", xhr.responseText);
            alert("Failed to load stories. Please try again.");
        }
    });
}

// Update pagination buttons dynamically
function updatePagination(response) {
    let paginationContainer = $(".pagination");
    console.log("Pagination Container Found:", paginationContainer.length);
    paginationContainer.empty(); // Clear existing pagination
    console.log("Hi Sameer")
    console.log(response)

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
        console.log("Page - Updated")
    }
}
