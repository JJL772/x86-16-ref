
function doSearch() {
	const input = document.getElementById("SearchBar");
	const table = document.getElementById("Table");
	const entry = table.getElementsByTagName("tr");
	const filterText = input.value.toUpperCase();
	
	for(i = 0; i < entry.length; i++) {
		const text = entry[i].getElementsByTagName("td")[0]?.innerText;
		if (!text) continue;
		if (text.toUpperCase().indexOf(filterText) > -1) // Check if the text has the stuffs
			entry[i].style.display = "";
		else
			entry[i].style.display = "none";
	}
}