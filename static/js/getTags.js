const tagsInput = document.querySelector("#id_tags");
const publishButton = document.querySelector(".btnRenk");

const API_KEY = "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";
const content = sessionStorage.getItem("content");
// console.log(content);
const getTags = async () => {
  if (content !== "") {
    console.log(content);
    try {
      const response = await fetch("https://api.openai.com/v1/completions", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: "text-davinci-003",
          prompt: `Bana '${content}' metni ile ilgili etiketler çıkar, virgülle ayır. Başlarında da '#' olsun`,
          temperature: 0.9,
          max_tokens: 150,
          top_p: 1,
          frequency_penalty: 0.0,
          presence_penalty: 0.6,
          stop: [" Human:", " AI:"],
        }),
      });
      const data = await response.json();
      const cleaned = data.choices[0].text;
      const tags = cleaned.split("\n\n")[1];

      tagsInput.value = tags;

      publishButton.addEventListener("click", () => {
        sessionStorage.clear();
      });
    } catch (error) {
      console.log(error);
    }
  } else {
    console.log("Empty");
  }
};
document.addEventListener("DOMContentLoaded", getTags);
