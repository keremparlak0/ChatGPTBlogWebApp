document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    const ckeditor = document.querySelector(".django-ckeditor-widget");
    const textArea = ckeditor.querySelector("#id_content");
    const plainText = textArea.value.replace(/(<([^>]+)>)/gi, "");
    const decodedText = new DOMParser().parseFromString(plainText, "text/html").documentElement.textContent;
    const publishButton = document.querySelector('#publish')

    console.log();
    

    // Adding text to the session storage
    publishButton.addEventListener('click', () => {
      sessionStorage.setItem("content", `${decodedText}`);
    })
   
  }, 1000);
});

