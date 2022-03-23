
const despachadasPendientesId = "despachadasPendientes"
const clientesOrdenadosId="clientesOrdenados"
const destinosOrdenadosId="destinosOrdenados"
const facturasVigentesId="vencidasVigentes"
const facturasOrdenadasFechaCancelacionId = "facturasOrdenadasFechaCancelacion"

window.addEventListener('DOMContentLoaded', () => {
  const { jsPDF } = window.jspdf;

  const pieLabelsStyles={
      color: "#ffffff",
      font: {
        size: 20,
      }
  };
  const titleStyles={
    ...pieLabelsStyles,
    display: true,
  };
  const facturasOrdenadasFechaCancelacionTable = document.getElementById(facturasOrdenadasFechaCancelacionId);

  const chartJsMap = {
    // chartDespachadasPendientes
    [despachadasPendientesId]: {
      chart: new Chart(
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
              title: {
                ...titleStyles,
                text: "Solicitudes Despachadas/Pendientes"
              },
            }
          }
        }
      ),
    },
    [clientesOrdenadosId]: {
      chart: new Chart(
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
            },
          }
        }
      ),
      title: "Clientes ordenados con la cantidad de solicitudes realizadas"
    },
    [destinosOrdenadosId]: {
      chart: new Chart(
        document.getElementById(destinosOrdenadosId),
        {
          type: "bar",
          data: {
            labels: [
              "Amazonas",
              "Anzoátegui",
              "Zulia",
              "Tachira",
            ],
            datasets: [{
              data: [2,10,11,14],
              backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
              ],
            }],
          },
          options: {
            indexAxis: 'y',
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        }
      ),
      title: "Destinos ordenados por su cantidad de solicitudes.",
    },
    [facturasVigentesId]: {
      chart: new Chart(
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
              title: {
                ...titleStyles,
                text: "Facturas vigentes/vencidas por cobrar.",
              },
            }
          }
        }
      ),
    },
  }
  // This event is triggered by htmx get response
  document.body.addEventListener("createnewchart",(evt)=>{
    // Update chart
    const data = evt.detail; // JSON
    const chart = chartJsMap[data.chartName].chart;
    chart.data.datasets[0].data = data.data;
    chart.update();
  });

  // This event is triggered by the alpinejs component
  document.body.addEventListener("generatepdf", (evt)=>{
    const chart = chartJsMap[evt.detail.currentChart].chart;
    const canvas = chart.canvas;
    const title = chartJsMap[evt.detail.currentChart].title;
    const doc = new jsPDF(
      // Set page size to letter
      {format: "letter"}
    );
    doc.setFontSize(15);

    // Reconfigure chart for PDF display
    if(chart.config.type === "pie"){
      chart.config.options.plugins.title.color = "black";
      chart.config.options.plugins.legend.labels = {
        color: "black",
        font: {
          size: 12,
        },
      }
    }else{
      // Bar chart doens't have top title, we to add one manually
      doc.text(`${title}`, 10,10);
    }

    // Start PDF creation with jsPDF

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

    let offsetHeight = 10 + canvasHeightMM;

    doc.addImage(chart.canvas, "PNG", marginWidth , 10);
    // Insert chart numeric data below de chart
    const data = chart.data.datasets[0].data;
    for(let i=0; i<chart.data.labels.length; i++){
      const label = chart.data.labels[i];
      offsetHeight+= (i+10);
      doc.text(
    `${label}: ${data[i]}`,
    10,
        offsetHeight,
      )
    }
    doc.save("chart.pdf");
  });

  // Generate a pdf using the browser
  document.body.addEventListener("genBrowserPDF", (evt)=>{
    window.print();
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
    currentChartIsEmpty: false,
    currentChart: despachadasPendientesId,
    input: {
      // Si hay un error un error en la respuesta de htmx, renderizar
      // errores del formulario
      ["@htmx:response-error.window"](){
        resData = JSON.parse(this.$event.detail.xhr.response)
        this.diaErrors = resData["day_form"] || {}
        this.mesErrors = resData["month_form"] || {}
        this.rangeErrors = resData["range_form"] || {}

        // Clear previous messages
        this.currentChartIsEmpty = false;
      }
    },
    form: {
      ["@htmx:before-request"](evt){
        // Clear any errors before the new request is made
        this.diaErrors = {};
        this.mesErrors = {}
        this.rangeErrors = {}
        // Clear previous messages
        this.currentChartIsEmpty = false;
      }
    },
    generateGraphPDF(){
      // Dispatch a custom event, we dont have access to the canvas element
      // in this alpine component
      if (this.currentChart === "ordenadas"){
        this.$dispatch('genBrowserPDF', { currentChart: this.currentChart });
        return
      }
      this.$dispatch('generatepdf', { currentChart: this.currentChart });

    },
    createNewChart(evt){
      this.currentChartIsEmpty = evt.detail.empty;
    }
  }));
});
