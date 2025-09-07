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

document.addEventListener("DOMContentLoaded", () => {
  // ----------------------------
  // Modal de error de login
  // ----------------------------
  const body = document.querySelector("body");
  const error = body.dataset.error;

  if (error) {
    const modalEl = document.getElementById('errorModal');
    const modalBody = modalEl.querySelector('.modal-body');
    modalBody.textContent = error; // llenar el mensaje de error

    const modal = new bootstrap.Modal(modalEl);
    modal.show();
  }
});
