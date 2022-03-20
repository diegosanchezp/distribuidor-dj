document.addEventListener('alpine:init', () => {
  Alpine.data('selectionForm', (props) => ({
    currentForm: '',
    message: '',
    invoiceState: props.invoiceState,
    error: false,
    errorMessage: '',
    successMessage: '',
    makingRequest: false,
    setMessages(){
      resData = JSON.parse(this.$event.detail.xhr.response);
      if(this.$event.detail.failed){
        this.errorMessage = resData.error;
      }
      if(this.$event.detail.successful){
        this.successMessage = resData.success;
        // Update state to success
        this.invoiceState = "PAID"
      }
      // For the loading spinner
      this.makingRequest = false;
    }
  }));
});
