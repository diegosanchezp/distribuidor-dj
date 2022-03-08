window.addEventListener('DOMContentLoaded', (event) => {
  const bankSelectionForm = document.getElementById("select-banks-form");
  const degvaForm = document.getElementById("degvaForm");

  bankSelectionForm.addEventListener("submit", (e)=>{
    // on form submission, prevent default
    e.preventDefault();
    const SelectionFormData = new FormData(bankSelectionForm);

    const selectedBank = SelectionFormData.get("bank");

    if(selectedBank === "degva"){
      degvaForm.submit();
    }

    if(selectedBank === "dakiti"){
      // Probably do a fetch
      console.log(selectedBank);
    }
  });

});
