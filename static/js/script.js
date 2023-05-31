// Slider
$(document).ready(function() {
    $('#slider').carousel({
      interval: false
    });
  });

// Profil resmi yükleme
  function previewImage() {
      const preview = document.getElementById('profile-picture-preview');
      const file = document.getElementById('profile-picture-input').files[0];
      const reader = new FileReader();
      
      reader.addEventListener("load", function () {
          preview.src = reader.result;
      }, false);
      
      if (file) {
          reader.readAsDataURL(file);
      }
  }

// Hakkında düzenle

$(document).ready(function() {
var originalText = $('#about-text').text();
var editInput = $('<textarea class="form-control">' + originalText + '</textarea>');
var editBtn = $('<button id="edit-btn" class="btn btn-primary">Düzenle</button>');
var saveBtn = $('<button id="save-btn" class="btn btn-success">Kaydet</button>');

// Düzenle butonuna tıklandığında düzenleme alanını göster
$(document).on('click', '#edit-btn', function() {
editInput.val(originalText);
$('#about-text').replaceWith(editInput);
$(this).replaceWith(saveBtn);
});

// Kaydet butonuna tıklandığında düzenlemeleri kaydet
$(document).on('click', '#save-btn', function() {
var updatedText = editInput.val();
var updatedParagraph = $('<p id="about-text">' + updatedText + '</p>');
editInput.replaceWith(updatedParagraph);
$(this).replaceWith(editBtn);
originalText = updatedText;
});
});

// Takip et butonu

function followUser() {
var btn = document.getElementById("follow-btn");
if (btn.classList.contains("following")) {
btn.innerHTML = '<i class="fa-solid fa-xs fa-user-plus" style="color: #090606;"></i>';
btn.classList.remove("following");
btn.classList.add("follow-button");
} else {
btn.innerHTML = '<i class="fa-solid fa-xs fa-user-check" style="color: #1b6407;"></i>';
btn.classList.remove("follow-button");
btn.classList.add("following");
}
}

// Yorumlar

document.getElementById('comment-form').addEventListener('submit', function(e) {
  e.preventDefault();
  var comment = document.getElementById('comment').value;
  var commentItem = document.createElement('div');
  commentItem.classList.add('col-12', 'mb-3', 'comment');
  commentItem.innerHTML = `
    <div class="card">
      <div class="card-body d-flex align-items-center">
        <img src="/img/1.png" alt="Profil Fotoğrafı" class="profile-picture">
        <div>
          <h5 class="card-title">Ad Soyad</h5>
          <p class="card-text" style="word-wrap: break-word;">${comment}</p>
        </div>
      </div>
    </div>
  `;
  document.getElementById('comment-list').appendChild(commentItem);
  document.getElementById('comment').value = '';
});