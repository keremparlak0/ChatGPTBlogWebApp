$(document).ready(function() {
  // Öneri Al butonuna tıklandığında işlemleri gerçekleştirmek için bir event listener ekleyin
  $('#addsuggestdddd').on('click', function(e) {
  //document.getElementById('addsuggest').addEventListener('click', function() {
    // AJAX isteği yapmak için XMLHttpRequest nesnesini oluşturun
    e.preventDefault();
    var titleInput = document.getElementById('id_title');
    var title = titleInput.value;
  
    var suggestionDiv = document.querySelector("#suggestion-div");
    

    $.ajax({
        url: '/author/getsuggestions/',
        type: 'POST',
        data: {
            'title': title
            },
        
        success: function(response) {
          console.log(response.success);
          
          suggestionDiv.innerHTML += 
          `
            <div class="sticky-top">
                <div class="suggestion">
                <h5>Öneri</h5>
                <hr>
                <p>${response.suggest}</p>
                <!-- <button type="button" id="add" class="btn btnRenk">Ekle</button> -->
                </div>
            </div>`;
            
        },
       

        error: function(xhr, status, error) {
          console.log(xhr.responseText);
        }
      });
  });
});

