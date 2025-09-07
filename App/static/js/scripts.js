document.addEventListener("DOMContentLoaded", () => {
  const ctx = document.getElementById("gastosChart");
  if (ctx) {
    new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["Alimentación", "Transporte", "Hogar", "Ocio", "Otros"],
        datasets: [
          {
            label: "Gastos",
            data: [400, 150, 200, 100, 50],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "bottom" },
        },
      },
    });
  }
});
