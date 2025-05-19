document.getElementById("fileInput").addEventListener("change", function (e) {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function (event) {
    const csv = event.target.result;
    const data = parseCSV(csv);
    displayTable(data);
    renderChart(data);
  };
  reader.readAsText(file);
});

function parseCSV(csv) {
  const rows = csv.split("\n").filter(Boolean);
  const headers = rows[0].split(",");
  const data = [];

  for (let i = 1; i < rows.length; i++) {
    const values = rows[i].split(",");
    const entry = {};
    headers.forEach((header, index) => {
      entry[header.trim()] = values[index].trim();
    });
    data.push(entry);
  }
  return data;
}

function displayTable(data) {
  const container = document.getElementById("tableContainer");
  let html = "<table><tr>";

  const headers = Object.keys(data[0]);
  headers.forEach(header => {
    html += `<th>${header}</th>`;
  });
  html += "</tr>";

  data.forEach(row => {
    html += "<tr>";
    headers.forEach(header => {
      html += `<td>${row[header]}</td>`;
    });
    html += "</tr>";
  });

  html += "</table>";
  container.innerHTML = html;
}

function renderChart(data) {
  const ctx = document.getElementById("expenseChart").getContext("2d");

  const categories = {};
  data.forEach(row => {
    const category = row.Category || "Uncategorized";
    const amount = parseFloat(row.Amount || "0");
    categories[category] = (categories[category] || 0) + amount;
  });

  const labels = Object.keys(categories);
  const amounts = Object.values(categories);

  new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Expenses by Category",
        data: amounts,
        backgroundColor: "rgba(75, 192, 192, 0.6)"
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}
