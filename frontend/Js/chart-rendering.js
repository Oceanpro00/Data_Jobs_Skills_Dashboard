// Color Id by Title id Function
function getColorByTitleId(titleId) {
    const entryLevel = ["6", "13", "5"];
    const midLevel = ["9", "12", "3"];
    const seniorLevel = ["4", "7", "14", "2"];
    const advancedLevel = ["1", "8", "10", "11"];

    if (entryLevel.includes(titleId)) return "#90CAF9"; // Light Blue (Entry)
    if (midLevel.includes(titleId)) return "#80CBC4";   // Teal (Mid)
    if (seniorLevel.includes(titleId)) return "#FFCC80"; // Amber (Senior)
    if (advancedLevel.includes(titleId)) return "#EF9A9A"; // Red (Advanced)

    return "#ff9800"; // Default Orange (if title_id doesn't match any group)
}

function updatePercentageColor(titleId) {
    titleId = String(titleId);

    const entryLevel = ["6", "13", "5"];
    const midLevel = ["9", "12", "3"];
    const seniorLevel = ["4", "7", "14", "2"];
    const advancedLevel = ["1", "8", "10", "11"];

    let textColor = "#FF6F00"; // Default Dark Orange

    if (entryLevel.includes(titleId)) {
        textColor = "#1976D2"; // Dark Blue (Entry)
    } else if (midLevel.includes(titleId)) {
        textColor = "#00796B"; // Dark Teal (Mid)
    } else if (seniorLevel.includes(titleId)) {
        textColor = "#FF8F00"; // Dark Amber (Senior)
    } else if (advancedLevel.includes(titleId)) {
        textColor = "#D32F2F"; // Dark Red (Advanced)
    }
    
    document.querySelectorAll(".highlight-percentage, .metric-card p").forEach(element => {
        element.style.color = textColor;
    });
}


// Get title ID from URL
const params = new URLSearchParams(window.location.search);
const titleId = params.get("title_id") || "1"; // Default to 1 if missing

// Set colorPicker based on titleId
let colorPicker = getColorByTitleId(titleId);

// Bar Chart Rendering
function renderChart(allSkills, checkedSkills) {
    const uncheckedSkills = allSkills
        .filter(skill => !checkedSkills.has(skill.skill))
        .slice(0, 10);

    const skillNames = uncheckedSkills.map(skill => skill.skill);
    const skillCounts = uncheckedSkills.map(skill => skill.count);

    const trace = {
        y: skillNames,
        x: skillCounts,
        type: "bar",
        orientation: "h",
        marker: { color: colorPicker },
        text: skillCounts.map((count, i) => `${skillNames[i]}: ${count} jobs`),
        hoverinfo: "text",
        hovertemplate: "<b>%{y}</b><br>Mentions: %{x} jobs"
    };

    const layout = {
        title: "Filtered Top Skills",
        xaxis: { title: "Count" },
        yaxis: { automargin: true, autorange: "reversed", tickvals: skillNames, ticktext: skillNames },
        margin: { t: 30, b: 40, l: 180, r: 20 },
        responsive: true,
    };

    Plotly.newPlot("skillsBarChart", [trace], layout, { responsive: true });
}


// Pie Chart Rendering
function renderPieCharts(degreeCounts, totalJobs) {
    const degreeIdMap = {
        "master's degree": "mastersdegreeChart",
        "phd": "phdChart",
        "bachelor's degree": "bachelorsdegreeChart"
    };

    Object.entries(degreeCounts).forEach(([degree, count]) => {
        const percentage = totalJobs > 0 ? ((count / totalJobs) * 100).toFixed(1) : 0;
        const formattedDegree = degree.charAt(0).toUpperCase() + degree.slice(1);
        const chartTitle = `<span class="highlight-percentage">${percentage}%</span> of jobs mention a ${formattedDegree}`;

        const titleIdMap = {
            "master's degree": "MastersDegreeChartTitle",
            "phd": "PhDChartTitle",
            "bachelor's degree": "BachelorsDegreeChartTitle"
        };

        // Update chart titles / color before rendering
        const titleElement = document.getElementById(titleIdMap[degree]);
        if (titleElement) titleElement.innerHTML = chartTitle;

        updatePercentageColor(titleId);

        Plotly.newPlot(degreeIdMap[degree], [{
            values: [count, totalJobs - count],
            labels: [`${count} Jobs`, `Other Jobs (${totalJobs - count})`],
            type: "pie",
            hoverinfo: "label+percent", 
            hovertemplate: "<b>%{label}</b><br>Mentions: %{value} jobs (%{percent})<extra></extra>",  
            textinfo: "label+percent",
            marker: { colors: [colorPicker, "#f0f0f0"] }
        }], {
            showlegend: false,
            hovermode: "closest",
            margin: { t: 0, b: 0, l: 0, r: 0 },
            height: 320,
            width: 320
        }, {
            responsive: true,
            displayModeBar: false,
            staticPlot: false
        });
    });
}
