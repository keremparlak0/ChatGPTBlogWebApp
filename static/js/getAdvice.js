const API_KEY = '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'
    const form = document.querySelectorAll('form')[1];
    const content = form.querySelector('#id_content');
    const adviceDiv = document.querySelector('.advice-div')
    const getAdvice = async (e) => {
        if (e.key === 'Enter') {
            // e.preventDefault()
            console.log(content.value);

            try {
                const response = await fetch('https://api.openai.com/v1/completions', {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${API_KEY}`,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        "model": "text-davinci-003",
                        "prompt": `${content.value} nedir?`,
                        "temperature": 0.9,
                        "max_tokens": 150,
                        "top_p": 1,
                        "frequency_penalty": 0.0,
                        "presence_penalty": 0.6,
                        "stop": [" Human:", " AI:"]
                    })
                });
                const data = await response.json();
                console.log(data.choices[0].text);

                const adviceText = document.createElement('p');
                adviceText.textContent = data.choices[0].text;
                adviceDiv.append(adviceText);


            } catch (error) {
                console.log(error);
            }
        }
    }

    content.addEventListener('keypress', getAdvice);