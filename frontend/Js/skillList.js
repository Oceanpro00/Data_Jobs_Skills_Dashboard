function renderSkillList(allSkills, checkedSkills, updateFilteredSkills) {
    const listContainer = d3.select("#skillRankingList").html("");

    allSkills.slice(0, 10).forEach(skill => {
        const listItem = listContainer.append("li");
        listItem.append("input")
            .attr("type", "checkbox")
            .attr("value", skill.skill)
            .property("checked", checkedSkills.has(skill.skill))
            .on("change", updateFilteredSkills);
        listItem.append("span").text(` ${skill.skill} (${skill.count})`);
    });
}
