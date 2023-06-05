$(document).ready(function() {
    $('#draftForm').on('submit', function(event) {
      event.preventDefault(); // Formun varsayılan submit işlemini engelle
      for (var instanceName in CKEDITOR.instances) {
        CKEDITOR.instances[instanceName].updateElement();
      }
  
      var form_data = new FormData(this);
      var content = $('#id_content').val();
      // Draft ID değerini de FormData nesnesine ekleyin
      var draft_id = $('#draft-id').val();
      form_data.append('draft_id', draft_id);
  
      console.log('Form submitted...');
      console.log(form_data.get('draft_id'));
      console.log($(this).find('[name="title"]').val());
      console.log($(this).find('[name="content"]').val());
      console.log(content)
  
      // AJAX isteği gönder
      $.ajax({
        url: '/author/publishajax/',
        type: 'POST',
        data: form_data,
        processData: false,
        contentType: false,
        success: function(response) {
          console.log(response.success);
          $('#publishBtn').show();
        },
        error: function(xhr, status, error) {
          console.log(xhr.responseText);
        }
      });
    });
  });
  