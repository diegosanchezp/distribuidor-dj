window.addEventListener('DOMContentLoaded', (event) => {
  const form = document.getElementById("pay-form");
  form.addEventListener("submit", (e)=>{
    // on form submission, prevent default
    e.preventDefault();
    const formData = new FormData(form);

    const selectedBank = formData.get("bank");

    if(selectedBank === "degva"){
      const bankUrl = new URL("/paygateway","https://bank.vittorioadesso.com");

      bankUrl.searchParams.append("key", formData.get("public_key"));
      bankUrl.searchParams.append("order",formData.get("invoice_id"));
      bankUrl.searchParams.append("reason",formData.get("reason"));
      bankUrl.searchParams.append("logotype", formData.get("logotype"));
      bankUrl.searchParams.append("name", formData.get("reason"));
      bankUrl.searchParams.append("amount", parseFloat(formData.get("invoice_ammount")));
      bankUrl.searchParams.append("num", 1);

      // Redirect the user to the payment gateway
      window.location.replace(bankUrl);
    }

    if(selectedBank === "dakiti"){
      // Probably do a fetch
      console.log(selectedBank)
    }
  });

});
