const API_KEY = "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";
  const blogContent = document.querySelector("#blog-content");
  const plainText = blogContent.innerHTML.replace(/(<([^>]+)>)/gi, "");
  const langSelection = document.querySelector("#langs");



  const changing = async () => {
    if (langSelection.value != "turkish") {
      console.log(langSelection.value);

      try {
        const response = await fetch("https://api.openai.com/v1/completions", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${API_KEY}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            model: "text-davinci-003",
            prompt: `'${plainText}' metnini, '${langSelection.value}' diline çevir.`,
            temperature: 0.9,
            max_tokens: 150,
            top_p: 1,
            frequency_penalty: 0.0,
            presence_penalty: 0.6,
            stop: [" Human:", " AI:"],
          }),
        });
        const data = await response.json();
        blogContent.textContent = data.choices[0].text;
        console.log(data);
      } catch (error) {
        console.log(error);
      }
    } else {
      console.log("blank");
      document.location.reload(true)
    }
  }

  langSelection.addEventListener("change", changing);