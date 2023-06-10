$(document).ready(function() {
document.getElementById('edit2-btn').addEventListener('click', function() {
    var aboutText = document.getElementById('about-text').textContent;
    
    console.log(aboutText);

    $.ajax({
        url: '/author/aboutajax/',
        type: 'POST',

        data: {
            'about': aboutText
        },
        
        success: function(response) {
          console.log(response.success);
          
        },
        error: function(xhr, status, error) {
          console.log(xhr.responseText);
        }
      });
  });
});