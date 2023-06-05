$(document).ready(function() {
    var form = document.getElementById('commentForm');
    form.addEventListener('submit', function(event) {
      event.preventDefault(); // Sayfanın yeniden yüklenmesini engeller
      console.log('Form submitted...');
      var blogIdInput = document.querySelector('input[name="blog_id"]');
      var blogId = blogIdInput.value;
      var comment = document.getElementById('comment').value;
      console.log(blogId, comment);
      // AJAX isteği gönderme
      $.ajax({
        url: '/commentajax/',  // Yorum ekleme işlemini gerçekleştiren bir URL'yi belirtin
        method: 'POST',  // Yorum ekleme işlemi için POST isteği yapılacak
        data: {
          "blog_id": blogId,  // Gönderilecek veriler arasında blog ID'sini ekleyin
          "message": comment  // Gönderilecek veriler arasında yorumu ekleyin
        },
        success: function(response) {
          // Başarılı durumda yapılacak işlemler
          var commentItem = document.createElement('div');
          commentItem.classList.add('col-12', 'mb-3', 'comment');
          commentItem.innerHTML = `
           
            <div class="card">
                <div class="card-body d-flex align-items-center">
                <img src="${response.profile_picture}" alt="Profil Fotoğrafı" class="profile-picture">
                <div>
                    <h5 class="card-title">${response.user}</h5>
                    <p class="card-text" style="word-wrap: break-word;">${response.message}</p>
                    <!-- İstenilen değişiklikler buraya eklenebilir -->
                </div>
                </div>
            </div>
          `;
          document.getElementById('comment-list').appendChild(commentItem); // Yeni yorumu sayfaya ekleyin
          document.getElementById('comment').value = ''; // Yorum alanını temizleyin
        },
        error: function(xhr, status, error) {
          // Hata durumunda yapılacak işlemler
          console.error('Error:', error);
        }
      });
    });
  });
  