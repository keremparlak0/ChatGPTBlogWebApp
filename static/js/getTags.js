const subject = document.querySelector("#content2");

const content = sessionStorage.getItem("content");

document.addEventListener("DOMContentLoaded", () => {
  console.log(content);
});


//Konuların etiketleri çıkarılacak