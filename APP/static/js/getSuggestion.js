const API_KEY = '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'
  const titleInput = document.querySelector('#id_title');
  const suggestionDiv = document.querySelector('#suggestion-div');

  const getSuggestion = async () => {
    const value = titleInput.value;
    console.log(value);
    try {
      const response = await fetch('https://api.openai.com/v1/completions', {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${API_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "model": "text-davinci-003",
          "prompt": `${value} hakkında en fazla 150 karakterlik bir öneri yazısı yaz.`,
          "temperature": 0.9,
          "max_tokens": 150,
          "top_p": 1,
          "frequency_penalty": 0.0,
          "presence_penalty": 0.6,
          "stop": [" Human:", " AI:"]
        })
      });
      const data = await response.json();
      
      suggestionDiv.innerHTML += `
      <div class="sticky-top">
        <div class="suggestion">
          <h5>Öneri</h5>
          <hr>
          <p>${data.choices[0].text}</p>
          <!-- <button type="button" id="add" class="btn btnRenk">Ekle</button> -->
        </div>
      </div>`;

    } catch (error) {
      console.log(error);
    }
  }
  titleInput.addEventListener('blur', getSuggestion);

  // Buton sorununu çözünce açacağım
// const addButton = document.querySelector("#add");
// addButton.addEventListener("click", () => {
//   ckeditorTextarea.textContent = `<p>${
//     suggestionDiv.children[0].querySelector("p").textContent
//   }</p>`;
//   console.log(suggestionDiv.children[0].querySelector("p").textContent);
//   ckeditorTextarea.textContent = `<p>${suggestionDiv.children[0].children[0].children[2].textContent}</p>`;
// });