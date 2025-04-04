$(document).ready(function () {
    // Function to fetch sources based on search input
    function fetchSources() {
        $.ajax({
            url: sourceListUrl,  // Ensure this variable is correctly set in your template
            data: {
                q: $("#search-source").val().trim()
            },
            dataType: "json",
            success: function (data) {
                let sourceTableBody = $("#source-table tbody");
                sourceTableBody.empty(); // Clear previous content

                if (!data.sources || data.sources.length === 0) {
                    sourceTableBody.append("<tr><td colspan='4'>No results found.</td></tr>");
                    return;
                }

                data.sources.forEach(source => {
                    let companies = Array.isArray(source.tagged_companies)
                        ? source.tagged_companies.join(", ")
                        : "N/A";

                    sourceTableBody.append(`
                        <tr class="source-row">
                            <td class="source-name">${source.name}</td>
                            <td><a href="${source.url}" target="_blank">${source.url}</a></td>
                            <td>${companies}</td>
                            <td>
                                <a href="/source/edit/${source.id}/" class="edit-btn">Edit</a>
                                <form action="/source/delete/${source.id}/" method="post" class="delete-form">
                                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                    <button type="submit" class="delete-btn"
                                            onclick="return confirm('Are you sure?');">Delete</button>
                                </form>
                                <button class="fetch-story-btn" data-source-id="${source.id}">Fetch Story</button>
                            </td>
                        </tr>`);
                });

                // Reattach fetchStories event after updating the table
                $(".fetch-story-btn").off("click").on("click", fetchStories);
            }
        });
    }

    // Function to fetch stories when the "Fetch Story" button is clicked
    function fetchStories() {
        var sourceId = $(this).data("source-id");  // Get the source ID from button
        var finalUrl = fetchStoriesUrl + sourceId + "/";  // Append source ID dynamically

        $.ajax({
            url: finalUrl,  // Use dynamically constructed URL
            method: "POST",
            headers: { "X-CSRFToken": csrfToken },  // Ensure CSRF token is included
            success: function (response) {
                $("#fetch-message").text(response.message).show().delay(3000).fadeOut();
            },
            error: function (xhr, status, error) {
                console.error("Error:", xhr.responseText);
                alert("Failed to fetch story. Please try again.");
            }
        });
    }

    // Fetch sources on page load
    fetchSources();

    // Fetch sources when search input changes
    $("#search-source").on("input", fetchSources);

    // Attach event handler for fetch story button clicks
    $(document).on("click", ".fetch-story-btn", fetchStories);
});
