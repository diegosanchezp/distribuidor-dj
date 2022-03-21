
const despachadasPendientesId = "despachadasPendientes"
const clientesOrdenadosId="clientesOrdenados"
const destinosOrdenadosId="destinosOrdenados"
const facturasVigentesId="facturasVigentes"
const facturasOrdenadasFechaCancelacionId = "facturasOrdenadasFechaCancelacion"

window.addEventListener('DOMContentLoaded', () => {
  const { jsPDF } = window.jspdf;

  const despachadasPendientesCanvas = document.getElementById(despachadasPendientesId)
  const pieLabelsStyles={
      color: "#ffffff",
      font: {
        size: 20,
      }
  }
  const chartDespachadasPendientes = new Chart(
    despachadasPendientesCanvas,
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
  const destinosOrdenados = new Chart(
    document.getElementById(destinosOrdenadosId),
    {
      type: "bar",
      data: {
        labels: [
          "Amazonas",
          "Anzoátegui",
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

  const facturasOrdenadasFechaCancelacionTable = document.getElementById(facturasOrdenadasFechaCancelacionId);
  const chartJsMap = {
    envios: {
      chart: chartDespachadasPendientes,
      id: despachadasPendientesId,
      canvas: despachadasPendientesCanvas,
    }
  }
  document.body.addEventListener("createnewchart",(evt)=>{
    // Update chart
    const data = evt.detail;
    console.log(evt.detail.chartName)

    if (evt.detail.chartName === despachadasPendientesId){
      chartDespachadasPendientes.data.datasets[0].data = data.data;
      chartDespachadasPendientes.update()
    }
    if (evt.detail.chartName === facturasVigentesId){
      chartFacturasVigentes.data.datasets[0].data = data.data;
      chartFacturasVigentes.update()
    }
    if (evt.detail.chartName === facturasOrdenadasFechaCancelacionId){
      console.log(facturasOrdenadasFechaCancelacionTable)
      console.log(data)
    }
  });

  // This event is triggered by the alpinejs component
  document.body.addEventListener("generatepdf", (evt)=>{
    const chart = chartJsMap[evt.detail.currentChart].chart;
    const canvas = chartJsMap[evt.detail.currentChart].canvas;

    // Reconfigure chart for PDF display
    chart.config.options.plugins.title = {
      display: true,
      text: "Custom Chart Title",
      color: "black",
    }
    chart.config.options.plugins.legend.labels = {
      color: "black",
      font: {
        size: 12,
      },
    }

    // Start PDF creation with jsPDF
    const doc = new jsPDF(
      // Set page size to letter
      {format: "letter"}
    );
    doc.setFontSize(15);

    // The width is in milimeters (mm)
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();

    // Scale down the chart
    chart.resize(350,350);
    chart.update();


    // Convert canvas height and width to mm
    // 1px = 0.2645833333mm
    const canvasWidthMM = (canvas.width *0.2645833333);
    const canvasHeightMM = (canvas.height *0.2645833333);

    // Calculate margins to center the chart
    const marginWidth = (pageWidth - canvasWidthMM) / 2;

    let offsetHeight = 30 + canvasHeightMM;

    doc.addImage(chart.canvas, "PNG", marginWidth , 10);
    if(chart.config.type === "pie"){
      // Insert chart numeric data below de chart
      const data = chart.data.datasets[0].data;
      for(let i=0; i<chart.data.labels.length; i++){
        const label = chart.data.labels[i];
        offsetHeight+= (i*10);
        doc.text(
          `${label}: ${data[i]}`,
          10,
          offsetHeight,
        )
      }
    };
    doc.save("chart.pdf");
    console.log(evt.detail.currentChart);
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
    currentChart: "envios",
    input: {
      // Si hay un error un error en la respuesta de htmx, renderizar
      // errores del formulario
      ["@htmx:response-error.window"](){
        resData = JSON.parse(this.$event.detail.xhr.response)
        this.diaErrors = resData["day_form"] || {}
        this.mesErrors = resData["month_form"] || {}
        this.rangeErrors = resData["range_form"] || {}
      }
    },
    generateGraphPDF(){
      // Dispatch a custom event, we dont have access to the canvas element
      // in this alpine component
      this.$dispatch('generatepdf', { currentChart: this.currentChart });
    },
    createNewChart(){
      console.log("NEW CHART")
    }
  }));
});
