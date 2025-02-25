function previewImage(event) {
  const input = event.target;
  const preview = document.getElementById('preview');

  if (input.files && input.files[0]) {
      const reader = new FileReader();

      reader.onload = function (e) {
          preview.src = e.target.result;
          preview.style.display = 'block'; // Show the preview
      };

      reader.readAsDataURL(input.files[0]); // Read the image file
  } else {
      preview.src = '';
      preview.style.display = 'none';  // Hide if no image
  }
}


function validateForm() {
// Basic form validation: Check that fields are not empty
  const patientName = document.getElementById('patient_name').value.trim();
  const prescriptionImage = document.getElementById('prescription_image').value;

  if (!patientName) {
      alert('Please enter a patient name.');
      return false; // Prevent form submission
  }

  if (!prescriptionImage) {
    alert("Please select a prescription image");
    return false;
  }

  return true; // Allow form submission if valid
}

document.addEventListener('DOMContentLoaded', (event) => {
  const fileInput = document.getElementById('prescription_image');
  if(fileInput){
    fileInput.addEventListener('change', previewImage);
  }

  //attach event listener to validate the form when submit is pressed
  const form = document.querySelector('form'); // Selects the FIRST form it finds!
  if (form) { // Make sure the form exists.
    form.addEventListener('submit', validateForm); //Correct Event
  }

});