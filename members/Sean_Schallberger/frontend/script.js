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

    animateBars();
});