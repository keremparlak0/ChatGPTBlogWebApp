document.addEventListener("DOMContentLoaded", function() {
    const button1 = document.getElementById("addsuggest");
    const suggestionDiv = document.querySelector("#suggestion-div");
    
    const clicking = async () => {
      console.log("Butona tıklandı! İşlemler başladı...");
      var titleInput = document.getElementById('id_title');
      var title = titleInput.value;
      console.log(title);
      $('.yukleniyor').text('Yükleniyor');
      try {
        const response = await fetch("/author/getsuggestions/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            "title": title,
          }),
        });
    
        if (response.ok) {
          // İsteğin başarılı olduğu durum
          const data = await response.json();
          console.log(data);
          $('.yukleniyor').text('');
          suggestionDiv.innerHTML = '';
          suggestionDiv.innerHTML += `
            <div class="sticky-top">
              <div class="suggestion">
                <h5>Öneri</h5>
                <hr>
                <p>${data.suggest}</p>
              </div>
            </div>`;
            
        } else {
          // İsteğin hatalı olduğu durum
          console.error("HTTP isteği başarısız: " + response.status);
        }
      } catch (error) {
        console.error("Bir hata oluştu:", error);
      }
      finally {
        button1.disabled = false;
      }
    }
    
    // Butonun click olayına clicking fonksiyonunu bağlayın
    button1.addEventListener("click", clicking);
    
    });
    
    
    