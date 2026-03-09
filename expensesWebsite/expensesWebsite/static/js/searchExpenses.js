const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");

tableOutput.style.display = "none";


searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value.trim();

    if (searchValue.length > 0) {

        paginationContainer.style.display = "none";
        tbody.innerHTML = "";

        fetch("/search-expenses", {
            method: "POST",
            body: JSON.stringify({ searchText: searchValue }),
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then((res) => res.json())
        .then((data) => {

            console.log("data received:", data);

            appTable.style.display = "none";
            tableOutput.style.display = "block";

            if (data.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="4" style="text-align:center;">
                            No results found
                        </td>
                    </tr>
                `;
            } else {

                let rows = "";

                data.forEach((item) => {
                    rows += `
                        <tr>
                            <td>${item.amount}</td>
                            <td>${item.category}</td>
                            <td>${item.description}</td>
                            <td>${item.date}</td>
                        </tr>
                    `;
                });

                tbody.innerHTML = rows;
            }

        })
        .catch((error) => {
            console.error("Search error:", error);
        });

    } else {

        // restore original table
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
        tableOutput.style.display = "none";
    }
});