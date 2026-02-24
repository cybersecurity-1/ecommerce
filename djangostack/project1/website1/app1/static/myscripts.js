
  // Validate on input and on submit
  document.getElementById("myForm").addEventListener("input", validateForm);
  document.getElementById("myForm").addEventListener("submit", function(event) {
    if (!validateForm()) {
      event.preventDefault(); // Prevent form submission if validation fails
    }
  });

  function validateForm() {
    let formIsValid = true;

    // Validate each field
    formIsValid &= validateField("name", "Please enter a first name.", "nameError");
    formIsValid &= validateField("lastName", "Please enter a last name.", "lastNameError");
    formIsValid &= validateField("address", "Please enter an address.", "addressError");
    formIsValid &= validateField("zip", "Please enter a zip code.", "zipError");
    formIsValid &= validateField("city", "Please enter a city.", "cityError");
    formIsValid &= validateField("state", "Please enter a state.", "stateError");

    // Enable or disable the continue button based on form validation
    document.querySelector(".btn.button-order").disabled = !formIsValid;

    return formIsValid; // Return the validation result
  }

  function validateField(fieldId, errorMessage, errorElementId) {
    const field = document.getElementById(fieldId);
    const errorElement = document.getElementById(errorElementId);
    
    if (field.value.trim() === "") {
      errorElement.textContent = errorMessage;
      return false;
    } else {
      errorElement.textContent = "";
      return true;
    }
  }


