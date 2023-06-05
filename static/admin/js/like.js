$(document).ready(function() {
    // Beğenme düğmesine tıklandığında AJAX isteğini gerçekleştir
    console.log('like.js loaded...');
    $('.like-btn').click(function(e) {
      e.preventDefault();
  
      // Beğenme düğmesini seç
      var likeBtn = $(this);
  
      // Beğenilen blogun ID'sini al
      var blogId = likeBtn.attr('data-blog-id');
  
      // AJAX isteği gönder
      $.ajax({
        url: '/likeajax/',  // Beğenme işlemini gerçekleştiren bir URL'yi belirtin
        method: 'POST',  // Beğenme işlemi için POST isteği yapılacak
        data: {
          "blog_id": blogId  // Gönderilecek veriler arasında blog ID'sini ekleyin
        },
        success: function(response) {
          // AJAX isteği başarılı olduğunda yapılacak işlemler
          // Örneğin, beğenme sayısını güncelleyebilir veya beğenme düğmesinin durumunu değiştirebilirsiniz
          // Burada örnek bir güncelleme yapılacak:
                var likeCountSpan = likeBtn.next('.like-count');
            likeCountSpan.text(response.count);
                            likeBtn.removeClass('btn-primary btn-outline-primary');  // Tüm sınıfları temizle
                if (response.liked) {
                    likeBtn.addClass('btn-primary');  // Beğenildi durumunda btn-success sınıfını ekle
                } else {
                    likeBtn.addClass('btn-outline-primary');  // Beğenilmedi durumunda btn-outline-success sınıfını ekle
                }
            // Beğenme durumuna göre düğmenin içeriğini güncelle
            if (response.liked) {
                likeBtn.text('Beğenildi');
            } else {
                likeBtn.text('Beğen');
            }
            likeBtn.blur(); // Butonun odaklanmasını kaldır
        },
        error: function(xhr, textStatus, error) {
          // AJAX isteği sırasında bir hata oluştuğunda yapılacak işlemler
          console.log(error);  // Hata mesajını konsola yazdırabilirsiniz
        }
      });
    });
  });
  