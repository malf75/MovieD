document.addEventListener('DOMContentLoaded', function() {
  let post = document.getElementById('postagem');
  
  if (post) {
      post.addEventListener('click', () => {
          post.style.height = '350px';
      });
  }
});