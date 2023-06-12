const API_KEY = "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";

//const API_KEY = "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";
  const blogContent = document.querySelector("#blog-content");
  const plainText = blogContent.innerHTML.replace(/(<([^>]+)>)/gi, "");
  const langSelection = document.querySelector("#langs");



  const changing = async () => {
    if (langSelection.value != "turkish") {
      console.log(langSelection.value);
      $('.dlb').text('Bekleyiniz...');
      try {
        const response = await fetch("/author/translateajax/", {
          method: "POST",
          body: JSON.stringify({
            "text": plainText,
            "lang": langSelection.value
          }),
        });
  
        if (response.ok) {
          // İsteğin başarılı olduğu durum
          const data = await response.json();
          const translate = data.translate;
          console.log(translate);
          blogContent.textContent = translate
          $('.dlb').text('');
        } else {
          // İsteğin hatalı olduğu durum
          console.error("HTTP isteği başarısız: " + response.status);
        }
      } catch (error) {
        console.log(error);
      }
    } else {
      console.log("blank");
      document.location.reload(true)
    }
  }

  langSelection.addEventListener("change", changing);