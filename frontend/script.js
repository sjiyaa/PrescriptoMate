function previewImage(event) {
  const input = event.target;
  const preview = document.getElementById('preview');

  if (input.files && input.files[0]) {
      const reader = new FileReader();

      reader.onload = function (e) {
          preview.src = e.target.result;
          preview.style.display = 'block'; // Show the preview
      };

      reader.readAsDataURL(input.files[0]); 
  } else {
      preview.src = '';
      preview.style.display = 'none';  // Hides if no image
  }
}


function validateForm() {
  const patientName = document.getElementById('patient_name').value.trim();
  const prescriptionImage = document.getElementById('prescription_image').value;

  if (!patientName) {
      alert('Please enter a patient name.');
      return false; 
  }

  if (!prescriptionImage) {
    alert("Please select a prescription image");
    return false;
  }

  return true;
}

document.addEventListener('DOMContentLoaded', (event) => {
  const fileInput = document.getElementById('prescription_image');
  if(fileInput){
    fileInput.addEventListener('change', previewImage);
  }

  const form = document.querySelector('form'); 
  if (form) { 
    form.addEventListener('submit', validateForm); 
  }

});
