// Function to fetch state-level job data and render the choropleth map
function renderStateMap(apiUrl) {
    d3.json(apiUrl).then(jobData => {
        if (!Array.isArray(jobData)) {
            console.error("Unexpected API response:", jobData);
            return;
        }

        // Get the selected job ID from the URL parameters
        const params = new URLSearchParams(window.location.search);
        const selectedJobId = params.get("title_id") || "1"; // Default to job ID 1 if none provided

        console.log("Selected Job ID:", selectedJobId);

        // Group job postings by state for the selected job ID
        const jobCountsByState = {};

        jobData.forEach(({ State, job_id }) => {
            // Convert job_id to string for comparison (URL params are strings)
            if (String(job_id) === selectedJobId) {
                jobCountsByState[State] = (jobCountsByState[State] || 0) + 1;
            }
        });

        // Extract data for Plotly
        const states = Object.keys(jobCountsByState);
        const counts = Object.values(jobCountsByState);

        console.log("Total Jobs Mapped to States:", counts.reduce((sum, count) => sum + count, 0));
        console.log("States Represented:", states);

        var data = [{
            type: "choropleth",
            locationmode: "USA-states",
            locations: states,
            z: counts,
            colorscale: [
                [0, "#FFF3E0"],  // Very Light Orange
                [0.3, "#FFCC80"], // Light Orange
                [0.6, "#FF9800"], // Main Orange (Your Preferred Color)
                [0.8, "#F57C00"], // Deeper Orange
                [1, "#E65100"]   // Dark Burnt Orange
            ],
            colorbar: { title: "Job Postings" }
        }];

        var layout = {
            title: `Job Distribution for Job ID: ${selectedJobId}`,
            geo: {
                scope: "usa",
                showlakes: true,
                lakecolor: "rgb(255,255,255)"
            },
            margin: { t: 30, b: 20, l: 10, r: 10 },
            responsive: true
        };

        Plotly.newPlot("stateMap", data, layout, { responsive: true });

        // Resize map on window resize
        window.addEventListener("resize", function() {
            Plotly.relayout("stateMap", { "autosize": true });
        });

    }).catch(error => {
        console.error("Error fetching state-level job data:", error);
    });
}
