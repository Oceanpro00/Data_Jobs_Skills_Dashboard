// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
    // Get all title containers
    const seniorityBars = document.querySelectorAll('.seniority-level');

    // function to check if an element is in the viewport
    const isInViewport = (element) => {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 && 
            rect.left >= 0 && 
            rect.bottom <= 
            (window.innerHeight || document.documentElement.clientHeight) && 
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    };

    // function to animate the bars
    const animateBars = () => {
        seniorityBars.forEach(bar => {
            if (isInViewport(bar)) {
                // get percentage from data-percent attribute
                const percent = bar.getAttribute('data-percent');
                // animate the bar to the percentage
                bar.style.setProperty('--percent', `${percent}%`);
                // add animation class
                bar.classList.add('animate');
                setTimeout(() => {
                    bar.style.width(`${percent}%`);
                }, 1000);
            }
        });
    };

    // run function on page load
    animateBars();

    // run function on scroll and resize
    window.addEventListener('scroll', animateBars);
    window.addEventListener('resize', animateBars);

    // Define the base path for job detail pages
    const basePath = "dashboard.html";

    // Job title to URL mapping
    const jobTitleToUrl = {
        "Machine Learning Engineer": "1",
        "Software & Platform Engineering": "2",
        "Data Modeling & Warehousing": "3",
        "Data Engineer": "4",
        "Risk & Compliance Analytics": "5",
        "Data Analyst": "6",
        "MLOps Engineer": "7",
        "Data Governance & Security": "8",
        "Database Engineer / Administrator": "9",
        "Data Scientist": "10",
        "Data Architect": "11",
        "Data Operations & Management": "12",
        "Data Specialist": "13",
        "Cloud & Infrastructure Engineering": "14"
    };

    // Select all job title divs
    const jobDivs = document.querySelectorAll('.title-container');

    // Add click event to each div
    jobDivs.forEach(div => {
        div.addEventListener('click', () => {
            const title = div.getAttribute('data-title'); // Get job title
            const url = jobTitleToUrl[title]; // Get corresponding URL

            if (url) {
                window.location.href = `${basePath}?title_id=${url}`; // Redirect
            } else {
                console.error(`No title_id found for title: ${title}`);
            }
        });
    });
});
