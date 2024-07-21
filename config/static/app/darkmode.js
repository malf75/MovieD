document.addEventListener('DOMContentLoaded', function() {
    let body = document.body;
    let butao = document.querySelector('#btn');
    let logo = document.querySelector('.logo');
    let logosign = document.querySelector('.logo__signup');
  
    const disableDarkMode = () => {
        butao.classList.remove('active');
        document.body.classList.remove('dark-mode');
        if (logo) {
            logo.src = 'https://movied-bucket.s3.amazonaws.com/static/media/Design_sem_nome-removebg-preview.png';
        }
        if (logosign) {
            logosign.src = 'https://movied-bucket.s3.amazonaws.com/static/media/Design_sem_nome-removebg-preview.png';
        }
        localStorage.setItem('dark-mode', 'inactive');
        body.classList.remove('preload');
    }
  
    const enableDarkMode = () => {
        butao.classList.add('active');
        document.body.classList.add('dark-mode');
        if (logo) {
            logo.src = 'https://movied-bucket.s3.amazonaws.com/static/media/Design_sem_nome__1_-removebg-preview.png';
        }
        if (logosign) {
            logosign.src = 'https://movied-bucket.s3.amazonaws.com/static/media/Design_sem_nome__1_-removebg-preview.png';
        }
        localStorage.setItem('dark-mode', 'active');
        body.classList.remove('preload');
    }
  
    let darkMode = localStorage.getItem('dark-mode');
  
    if (darkMode === 'active') {
      enableDarkMode();
    } else {
      disableDarkMode();
    }
  
    butao.addEventListener('click', () => {
      if (butao.classList.contains('active')) {
          disableDarkMode();
      } else {
          enableDarkMode();
      }
    });
  });