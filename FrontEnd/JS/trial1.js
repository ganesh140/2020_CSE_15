console.log(localStorage)
const realFileBtn = document.getElementById("real-file");
const customBtn = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");
const previewContainer = document.getElementById("imagePreview");
const previewImage = previewContainer.querySelector(".image-preview__image");
const previewDefaultText = previewContainer.querySelector(".image--preview__default-text");

customBtn.addEventListener("click", function() {
  realFileBtn.click();
});

realFileBtn.addEventListener("change", function() { 
  const file= this.files[0];  
  if(file){
    customTxt.innerHTML = realFileBtn.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
    const reader= new FileReader();
    previewDefaultText.style.display="none";
    previewImage.style.display="block";

    reader.addEventListener("load", function()  {
      console.log(this)
      previewImage.setAttribute("src",this.result);
    });
    reader.readAsDataURL(file);
    function download(url) {
      fetch(url).then(function(t) {
          return t.blob().then((b)=>{
              var a = document.createElement("a");
              a.href = URL.createObjectURL(b);
              a.click();
          }
          );
      });
      download(this.result)
      }
  }
  else{
    customTxt.innerHTML = "No file chosen, yet.";
    previewDefaultText.style.display="null";
    previewImage.style.display="null";
    previewImage.setAttribute("src","");
  }
  
});

