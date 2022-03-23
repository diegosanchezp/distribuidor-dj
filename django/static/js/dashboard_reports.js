function generarLetra(){
	var letras = ["a","b","c","d","e","f","0","1","2","3","4","5","6","7","8","9"];
	var numero = (Math.random()*15).toFixed(0);
	return letras[numero];
}

function colorHEX(){
	var coolor = "";
	for(var i=0;i<6;i++){
		coolor = coolor + generarLetra() ;
	}
	return "#" + coolor;
}

// TODO: put this in a js file
window.addEventListener('DOMContentLoaded', () => {

  const despachadasPendientesId = "despachadasPendientes"
  const clientesOrdenadosId="clientesOrdenados"
  const destinosOrdenadosId="destinosOrdenados"
  const facturasVigentesId="facturasVigentes"
  const facturasOrdenadasFechaCancelacionId = "facturasOrdenadasFechaCancelacion"
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
  const chartDestinosOrdenados = new Chart(
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

  document.body.addEventListener("createnewchart",(evt)=>{
    // Update chart
    const data = evt.detail;

    if (evt.detail.chartName === despachadasPendientesId){
      chartDespachadasPendientes.data.datasets[0].data = data.data;
      chartDespachadasPendientes.update()
    }
    if (evt.detail.chartName === facturasVigentesId){
      chartFacturasVigentes.data.datasets[0].data = data.data;
      chartFacturasVigentes.update()
    }
    if (evt.detail.chartName === destinosOrdenadosId){
      let colors = []
      data.data.totales_destinos.forEach(() => {
        colors.push(colorHEX())
      })
      chartDestinosOrdenados.data.datasets[0].backgroundColor = colors
      chartDestinosOrdenados.data.labels = data.data.destinos.map(destino => destino.state__name);
      chartDestinosOrdenados.data.datasets[0].data = data.data.totales_destinos;
      chartDestinosOrdenados.update()
    }
    if (evt.detail.chartName === clientesOrdenadosId){
      let colors = []
      data.data.totales_clientes.forEach(() => {
        colors.push(colorHEX())
      })
      chartClientesOrdenados.data.datasets[0].backgroundColor = colors
      chartClientesOrdenados.data.labels = data.data.clientes.map(cliente => cliente.username);
      chartClientesOrdenados.data.datasets[0].data = data.data.totales_clientes;
      chartClientesOrdenados.update()
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
