document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const titleId = params.get("title_id") || "1";
    const apiUrl = `http://127.0.0.1:5000/title_id/${titleId}`;

    let allSkills = [];
    let checkedSkills = new Set();

    const excludedSkills = ["master's degree", "phd", "bachelor's degree"];
    let totalJobs = 0;
    let degreeCounts = { "master's degree": 0, "phd": 0, "bachelor's degree": 0 };

    d3.json(apiUrl).then(data => {
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

        renderSkillList();
        renderChart();
        renderPieCharts();
    }).catch(error => {
        console.error("Error fetching data:", error);
        document.getElementById("job-classification").textContent = "Failed to load data.";
    });

    function renderSkillList() {
        const listContainer = d3.select("#skillRankingList").html("");

        const topSkills = allSkills.slice(0, 10);
        topSkills.forEach(skill => {
            const listItem = listContainer.append("li");
            listItem.append("input")
                .attr("type", "checkbox")
                .attr("value", skill.skill)
                .property("checked", checkedSkills.has(skill.skill))
                .on("change", updateFilteredSkills);
            listItem.append("span").text(` ${skill.skill} (${skill.count})`);
        });
    }

    function updateFilteredSkills() {
        checkedSkills = new Set(
            d3.selectAll("#skillRankingList input:checked")
                .nodes()
                .map(input => input.value)
        );
        renderChart();
    }

    function renderChart() {
        const uncheckedSkills = allSkills
            .filter(skill => !checkedSkills.has(skill.skill))
            .slice(0, 10); // Ensure top 10 always show
    
        const skillNames = uncheckedSkills.map(skill => skill.skill);
        const skillCounts = uncheckedSkills.map(skill => skill.count);
    
        const trace = {
            y: skillNames,
            x: skillCounts,
            type: "bar",
            orientation: "h",
            marker: { color: "#ff9800" },
            text: skillNames, 
            textposition: "inside", 
        };
    
        const layout = {
            title: "Filtered Top Skills",
            xaxis: { title: "Count" },
            yaxis: {
                automargin: true, 
                autorange: "reversed",
                tickmode: "array",
                tickvals: skillNames,
                ticktext: skillNames, 
            },
            margin: { t: 30, b: 40, l: 180, r: 20 }, 
            responsive: true, 
        };
    
        Plotly.newPlot("skillsBarChart", [trace], layout, { responsive: true });
    }
    

    function renderPieCharts() {
        Object.entries(degreeCounts).forEach(([degree, count]) => {
            const percentage = totalJobs > 0 ? ((count / totalJobs) * 100).toFixed(1) : 0;
            const formattedDegree = degree.charAt(0).toUpperCase() + degree.slice(1);
            const chartTitle = `<span class="highlight-percentage">${percentage}%</span> of jobs mention a ${formattedDegree}`;
    
            // Directly set the title in the corresponding div
            const degreeIdMap = {
                "master's degree": "MastersDegreeChartTitle",
                "phd": "PhDChartTitle",
                "bachelor's degree": "BachelorsDegreeChartTitle"
            };
            
            const titleElement = document.getElementById(degreeIdMap[degree]);

            if (titleElement) {
                titleElement.innerHTML = chartTitle;
            }
    
            // Render the pie chart into the correct div
            Plotly.newPlot(`${degree.replace(/[' ]/g, "")}Chart`, [{
                values: [count, totalJobs - count],
                labels: ["Degree Holders", "Others"],
                type: "pie",
                hoverinfo: "none",
                textinfo: "none",
                marker: { colors: ["#ff9800", "#f0f0f0"] }
            }], {
                showlegend: false,
                hovermode: false,
                staticPlot: true,
                margin: { t: 0, b: 0, l: 0, r: 0 },
                height: 320,
                width: 320
            });
        });
    }
});
