console.log(localStorage)
const realFileBtn = document.getElementById("real-file");
const customBtn = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");

customBtn.addEventListener("click", function() {
  realFileBtn.click();
});

realFileBtn.addEventListener("change", function() {
  const reader= new FileReader();
  reader.addEventListener("load", () => {
    localStorage.setItem("recent-image", reader.result);
  });
  reader.readAsDataURL(this.files[0]); 
  if (realFileBtn.value) {
    customTxt.innerHTML = realFileBtn.value.match(
      /[\/\\]([\w\d\s\.\-\(\)]+)$/
    )[1];
  } else {
    customTxt.innerHTML = "No file chosen, yet.";
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const recentImageDataUrl= localStorage.getItem("recent-image");
  if (recentImageDataUrl) {
    document.querySelector("imgPreview").setAttribute("src", recentImageDataUrl);
  }
});
