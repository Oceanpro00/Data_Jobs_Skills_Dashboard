document.addEventListener("DOMContentLoaded", async function () {
    const params = new URLSearchParams(window.location.search);
    const titleId = params.get("title_id") || "1";
    const apiUrl = `http://127.0.0.1:5000/title_id/${titleId}`;

    let allSkills = [];
    let checkedSkills = new Set();
    const excludedSkills = ["master's degree", "phd", "bachelor's degree"];
    let totalJobs = 0;
    let degreeCounts = { "master's degree": 0, "phd": 0, "bachelor's degree": 0 };

    const data = await fetchJobData(apiUrl);
    if (!data) return;

    document.getElementById("job-classification").textContent = data.job_classification;
    totalJobs = data.total_count;
    document.getElementById("job-count").textContent = totalJobs;

    allSkills = [];
    data.top_skills.forEach(skill => {
        if (excludedSkills.includes(skill.skill)) {
            degreeCounts[skill.skill] = skill.count;
        } else {
            allSkills.push(skill);
        }
    });

    function updateFilteredSkills() {
        checkedSkills = new Set(
            d3.selectAll("#skillRankingList input:checked")
                .nodes()
                .map(input => input.value)
        );
        renderChart(allSkills, checkedSkills);
    }

    renderSkillList(allSkills, checkedSkills, updateFilteredSkills);
    renderChart(allSkills, checkedSkills);
    renderPieCharts(degreeCounts, totalJobs);
});
