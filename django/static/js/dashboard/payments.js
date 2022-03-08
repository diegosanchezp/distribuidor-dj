
document.addEventListener('alpine:init', () => {
  Alpine.data('selectionForm', () => ({
    currentForm: '',
    dakitiSubmit(){
      console.log("dakiti");
    }
  }));
});
