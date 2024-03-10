let darkModeState = null

document.addEventListener('DOMContentLoaded', function() {
    let butao = document.querySelector('#btn');
    let logo = document.querySelector('.logo');
    let logosign = document.querySelector('.logo__signup');
  
    const disableDarkMode = () => {
        butao.classList.remove('active');
        document.body.classList.remove('dark-mode');
        if (logo) {
            logo.src = 'https://images-movied.s3.amazonaws.com/static/media/Design_sem_nome-removebg-preview.png';
        }
        if (logosign) {
            logosign.src = 'https://images-movied.s3.amazonaws.com/static/media/Design_sem_nome-removebg-preview.png';
        }
        localStorage.setItem('dark-mode', 'inactive');
        darkModeState = 'inactive';
    }
  
    const enableDarkMode = () => {
        butao.classList.add('active');
        document.body.classList.add('dark-mode');
        if (logo) {
            logo.src = 'https://images-movied.s3.amazonaws.com/static/media/Design_sem_nome__1_-removebg-preview.png';
        }
        if (logosign) {
            logosign.src = 'https://images-movied.s3.amazonaws.com/static/media/Design_sem_nome__1_-removebg-preview.png';
        }
        localStorage.setItem('dark-mode', 'active');
        darkModeState = 'active';
    }
  
    let darkMode = localStorage.getItem('dark-mode');
    if (darkMode !== darkModeState){
        if (darkMode === 'active') {
        enableDarkMode();
        } else {
        disableDarkMode();
        }
    }
    butao.addEventListener('click', () => {
      if (butao.classList.contains('active')) {
          disableDarkMode();
      } else {
          enableDarkMode();
      }
    });
  });