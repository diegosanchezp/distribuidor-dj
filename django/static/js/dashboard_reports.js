// TODO: put this in a js file
window.addEventListener('DOMContentLoaded', () => {

  const despachadasPendientesId = "despachadasPendientes"
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
            labels: {
              color: "#ffffff",
              font: {
                size: 20,
              }
            }
          },
        }
      }
    }
  );

  // document.body.addEventListener('htmx:beforeSwap', (evt)=>{
  //   if(evt.detail.xhr.status==200){
  //     evt.detail.shouldSwap = false;
  //   }
  //   if(evt.detail.xhr.status === 400 ){
  //     // https://htmx.org/docs/#events
  //     evt.detail.shouldSwap = true;
  //     // set isError to false to avoid error logging in console
  //     evt.detail.isError = false;
  //   }
  // });
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
