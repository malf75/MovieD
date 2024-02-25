function previewImage(event) {
    var input = event.target;
    var preview = document.getElementById('imagePreview');
    var file = input.files[0];
    
    if (file) {
      var reader = new FileReader();
      reader.onload = function(e) {
        var img = new Image();
        img.className = 'image-preview';
        img.src = e.target.result;
        img.style.maxWidth = '200px';
        preview.innerHTML = '';
        preview.appendChild(img);
      }
      reader.readAsDataURL(file);
    } else {
      preview.innerHTML = '';
    }
  }