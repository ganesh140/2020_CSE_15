function readURL(input) {
  if (input.files && input.files[0]) {++
    var reader = new FileReader();

    reader.onload = function(e) {
      $('.image-upload-wrap').hide();
      $('.file-upload-image').attr('src', e.target.result);
      $('.file-upload-content').show();
      $('.image-title').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

    // Bind `input` event on both the inputs
// $('.file-upload-input').on('input', function() {
//   // toggle: If argument passed is 
//   //         true:  show
//   //         false: hide
//     // if ($('#file')[0].files.length === 0) {
//       var img = document.getElementsByClassName('file-upload-input').src; //= 'Images/Minus.gif';
//       if (img) {
//         document.getElementsByClassName('file-upload-input').src = 'static/images/tick.gif';
//       } else if (!img) {
//         document.getElementsByClassName('file-upload-input').src = 'static/images/cross.gif';
//         alert(img);
//       }
// }).trigger('input'); // Trigger event to call on page load

  } 
  
  else {
    removeUpload();
  }
}

function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $('.image-upload-wrap').show();
}

$('.image-upload-wrap').bind('dragover', function () {
  $('.image-upload-wrap').addClass('image-dropping');
});
$('.image-upload-wrap').bind('dragleave', function () {
  $('.image-upload-wrap').removeClass('image-dropping');
});