$(document).ready(function () {
    function fetchStories() {
        $.ajax({
            url: storyListUrl,
            data: {
                q: $("#search-title").val().trim(),
                date: $("#filter-date").val()
            },
            dataType: "json",
            success: function (data) {
                let storiesList = $("#stories-list");
                storiesList.empty(); // Clear previous content

                if (data.stories.length === 0) {
                    storiesList.append("<p>No results found.</p>");
                    return;
                }

                data.stories.forEach(story => {
                    storiesList.append(`
                        <div class="story-card">
                            <h3 class="story-title">
                                <a href="${story.article_url}" target="_blank">${story.title}</a>
                            </h3>
                            <p class="story-date"><strong>Published Date:</strong> ${story.published_date}</p>
                            <p class="story-body">${story.body_text}</p>
                            <p class="story-companies"><strong>Tagged Companies:</strong> ${story.tagged_companies.join(", ")}</p>
                            <div class="story-actions">
                                <a href="/story/edit/${story.id}/" class="btn edit-btn">Edit</a>
                                <a href="/story/delete/${story.id}/" class="btn delete-btn" onclick="return confirm('Are you sure?');">Delete</a>
                            </div>
                        </div>`);
                });
            }
        });
    }

    // Fetch stories on page load
    fetchStories();

    // Fetch stories when search input changes or date filter changes
    $("#search-title, #filter-date").on("input change", fetchStories);
});
