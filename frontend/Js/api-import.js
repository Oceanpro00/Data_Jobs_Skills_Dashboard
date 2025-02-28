async function fetchJobData(apiUrl) {
    try {
        console.log(`Fetching data from: ${apiUrl}`); // Debug log

        const data = await d3.json(apiUrl);
        console.log("Fetched Data:", data); // Debug log
        return data;
    } catch (error) {
        console.error("Error fetching data:", error);
        document.getElementById("job-classification").textContent = "Failed to load data.";
        return null;
    }
}