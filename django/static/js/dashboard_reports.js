// TODO: put this in a js file
window.addEventListener('DOMContentLoaded', () => {

  const despachadasPendientesId = "despachadasPendientes"
  const clientesOrdenadosId="clientesOrdenados"

  const facturasVigentesId="facturasVigentes"
  const pieLabelsStyles={
      color: "#ffffff",
      font: {
        size: 20,
      }
  }
  const chartDespachadasPendientes = new Chart(
    document.getElementById(despachadasPendientesId),
    {
      type: 'pie',
      data: {
        labels: [
          'Solicitudes Pendientes',
          'Solicitudes Despachadas',
        ],
        datasets: [{
          data: [2, 10], // TOOD: grab default data from somewhere else
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
          ],
        }],
      },
      options: {
        aspectRatio: 1,
        plugins: {
          legend: {
            labels: pieLabelsStyles,
          },
        }
      }
    }
  );
  const chartClientesOrdenados = new Chart(
    document.getElementById(clientesOrdenadosId),
    {
      type: "bar",
      data: {
        labels: [
          "gshoes",
          "jjclothes",
        ],
        datasets: [{
          data: [2,10],
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 159, 64, 0.2)',
          ],
        }],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    }
  );
  const chartFacturasVigentes = new Chart(
    document.getElementById(facturasVigentesId),
    {
      type: "pie",
      data: {
        labels: [
          'Facturas vigentes',
          'Facturas vencidas por cobrar.',
        ],
        datasets: [{
          data: [2, 10], // TOOD: grab default data from somewhere else
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
          ],
        }],
      },

      options: {
        aspectRatio: 1,
        plugins: {
          legend: {
            labels: pieLabelsStyles,
          },
        }
      }

    }
  );

  document.body.addEventListener("createnewchart",(evt)=>{

    // Update chart
    const data = evt.detail;

    if (evt.detail.chartName === despachadasPendientesId){
      chartDespachadasPendientes.data.datasets[0].data = data.data;
      chartDespachadasPendientes.update()
    }
  });
});

// WARNING: esto no puede estar en dentro del DOMContentLoaded
// Si no, da referencias nulas
document.addEventListener('alpine:init', () => {
  Alpine.data('formComponent', (initialTab) => ({
    currentTab: initialTab,
    diaErrors: {},
    mesErrors: {},
    rangeErrors: {},
    toggle() {
      this.open = ! this.open
    },
    input: {
      ["@htmx:response-error.window"](){
        resData = JSON.parse(this.$event.detail.xhr.response)
        this.diaErrors = resData["day_form"] || {}
        this.mesErrors = resData["month_form"] || {}
        this.rangeErrors = resData["range_form"] || {}
      }
    }
  }));
});
