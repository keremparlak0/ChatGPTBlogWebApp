$(document).ready(function() {
    $('#deneme-btn').click(function(e) {
        e.preventDefault();
        var denemeBtn = document.getElementById("deneme-btn");
        console.log('burada...');
        var draftId = denemeBtn.getAttribute("data-draft-id");
          console.log(draftId);
        console.log('Form submitted...');
          // AJAX isteği gönder
          $.ajax({
            url: '/author/ajaxdeneme/',
            type: 'POST',
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            data: {
                "draft_id": draftId,
            },
            success: function(response) {
              console.log(response.success);
              console.log(response.blog);
              var publishBtn = document.getElementById("publishBtn");
                if (response.blog) {
                publishBtn.innerText = "Güncelle";
                } else {
                publishBtn.innerText = "Yayınla";
                }
              
            },
            error: function(xhr, status, error) {
              console.log(xhr.responseText);
            },
            
          });


    });
});