document.addEventListener('DOMContentLoaded', () => {
const postagens = document.querySelectorAll('.postagem__paragrafo')
const selectFilmes = document.createElement('select')



fetch("https://jsvx4qwrvwso7batrajoavuoysd0rvjpi9dg90wure.vercel.app/filmes")
  .then(res => res.json())
  .then((filmes) => {

// Cria o container de opções do filme //

    selectFilmes.style.position = "absolute"
    selectFilmes.style.display = "none"
    selectFilmes.title = "opções de filme"

    filmes.forEach((filme) => {
      const option = document.createElement('option')
      option.value = filme.Series_Title
      option.text = filme.Series_Title
      selectFilmes.appendChild(option)
    });
    
    const inputTexto = document.getElementById('postagem')
    if (inputTexto) {
    selectFilmes.style.display = 'none'
    
    inputTexto.addEventListener('input', (event) => {
      const textoDigitado = event.target.value.substring(event.target.value.indexOf('@') + 1)
      const inputRect = inputTexto.getBoundingClientRect()
      selectFilmes.style.left = `${inputRect.left}px`
      selectFilmes.style.top = `${inputRect.bottom}px`
      selectFilmes.style.backgroundColor = "var(--cor-principal)"
      selectFilmes.style.border = "1px solid var(--cor-secundaria)"
      selectFilmes.style.borderRadius = "20px"
      selectFilmes.style.fontFamily = "var(--fonte-principal)"
      selectFilmes.style.color = "var(--cor-secundaria)"
      selectFilmes.style.padding = "1em 2em"
      selectFilmes.style.left = "600px"
      selectFilmes.style.top = "300px"
      selectFilmes.style.width = "300px" 
      if (event.target.value.includes('@')) {
        selectFilmes.style.display = 'block'
        const options = selectFilmes.getElementsByTagName('option')
        for (let i = 0; i < options.length; i++) {
          if (options[i].value.toLowerCase().includes(textoDigitado.toLowerCase())) {
            options[i].style.display = 'block'
          } else {
            options[i].style.display = 'none'
          }
        }
      } else {
        selectFilmes.style.display = 'none'
      }
    })
    
    selectFilmes.addEventListener('change', (event) => {
      inputTexto.value = inputTexto.value.replace(/@[\w\s]*/g, '') + `${event.target.value}`
      selectFilmes.style.display = 'none'
    })
    
    document.body.appendChild(selectFilmes)
  }

// Printa as informações nas Postagens //

    postagens.forEach((postagem, index) => {
      let filmeEncontrado = false
      filmes.forEach((filme) => {
        if (!filmeEncontrado) {
          let titulo = filme.Series_Title;
          let regex = new RegExp(`\\b(?!:.)\\s*${titulo}\\b(?!:.)\\s*`, 'ig')
          if (regex.test(postagem.textContent)) {
            const containerFilmes = document.createElement('div')
            containerFilmes.classList.add('filme__container')
            containerFilmes.innerHTML = `
              <img class="imagem__filme" src="${filme.Poster_Link}" alt="Poster do Filme">
              <li class="filme__item">
                <p class="filme__item-p">Name: ${filme.Series_Title}</p>
                <p class="filme__item-p">Overview: ${filme.Overview}</p>
                <p class="filme__item-p">Runtime: ${filme.Runtime}</p>
                <p class="filme__item-p">IMDB Rating: ${filme.IMDB_Rating}</p>
                <p class="filme__item-p">Released: ${filme.Released_Year}</p>
                <p class="filme__item-p">Genre: ${filme.Genre}</p>
              </li>
            `;
            const existingElement = postagem.nextSibling;
            postagem.parentNode.insertBefore(containerFilmes, existingElement);
            filmeEncontrado = true;
          }
        }
      });
    });
  });
});
