document.addEventListener('DOMContentLoaded', function() {
  let post = document.getElementById('postagem');
  
  if (post) {
      post.addEventListener('focus', () => {
          post.style.height = '350px';
          post.style.borderColor = '#2196F3'
      });
      post.addEventListener('blur', () => {
        post.style.height = '100px';
        post.style.borderColor = '';
        });
  }

});

$('.filme__like').on('click', function(event) {
  event.preventDefault();
  let url = $(this).attr("href");
  let postId = $(this).data('post-id');
  let csrfToken = $(this).data('csrf-token');

  $.post(url, { pk: postId, csrfmiddlewaretoken: csrfToken })
    .done(function(data) {
      if (data.user_liked) {
        $('.filme__like[data-post-id="' + postId + '"]').html('<i class="fa-solid fa-heart"></i>');
      } else {
        $('.filme__like[data-post-id="' + postId + '"]').html('<i class="fa-regular fa-heart"></i>');
      }
      $('.number__likes[data-post-id="' + postId + '"]').text(data.likes_count);
    })
    .fail(function(xhr, errmsg, err) {
    });

});

$('.filme__save').on('click', function(event) {
  event.preventDefault();
  let url = $(this).attr("href");
  let postId = $(this).data('post-id');
  let csrfToken = $(this).data('csrf-token');

  $.post(url, { pk: postId, csrfmiddlewaretoken: csrfToken })
  .done(function(data) {
    let iconClass = data.user_saved ? 'fa-solid' : 'fa-regular';
    $('.filme__save[data-post-id="' + postId + '"]').html('<i class="' + iconClass + ' fa-bookmark"></i>');
    $('.number__save[data-post-id="' + postId + '"]').text(data.save_count);
  })
  .fail(function(xhr, errmsg, err) {

  });

});

