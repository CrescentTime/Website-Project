function min_max_filter() {
    let min_input = document.getElementById("min_price");
    min_input = parseFloat(min_input.value);
    let max_input = document.getElementById("max_price");
    max_input = parseFloat(max_input.value);
    let table = document.getElementById("rec_table");
    let tr = table.getElementsByTagName("tr");
    let td_value, td, i;
    for (i = 0; i <tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[2];
        if (td) {
            td_value = parseFloat(td.textContent || td.innerText);
            if ((!isNaN(min_input) && td_value < min_input) ||
                (!isNaN(max_input) && td_value > max_input)) {
                tr[i].style.display = "none";
            }
            else {
                tr[i].style.display = "";
            }
        }
    }

}