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
  var url = $(this).attr("href");
  var postId = $(this).data('post-id');
  var csrfToken = $(this).data('csrf-token');

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

