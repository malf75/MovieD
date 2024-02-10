const postagens = document.querySelectorAll('.postagem__paragrafo');
const tabelaTrend = document.querySelector('.tabela-trend')
const trends = document.querySelectorAll('.trend')

  fetch(`/api/filme_info/`)
    .then(res => res.json())
    .then((filmes) => {

      let filmesMencionados = {};
      postagens.forEach((postagem) => {
        filmes.forEach((filme) => {
          let titulo = filme.Series_Title;
          let regex = new RegExp(`\\b(?!:.)\\s*${titulo}\\b(?!:.)\\s*`, 'ig')
          if (regex.test(postagem.textContent)) {
            if (filmesMencionados[titulo]) {
              filmesMencionados[titulo] += 1;
            } else {
              filmesMencionados[titulo] = 1;
            }
          }
        });
      });
  
      const filmesMencionadosArray = Object.entries(filmesMencionados)
        .sort((a, b) => b[1] - a[1]);
  
      const top3Filmes = filmesMencionadosArray.slice(0, 3);
      
      top3Filmes.forEach((filme)=>{
        const containerFilmes = document.createElement('p')
            containerFilmes.classList.add('trend')
            containerFilmes.hidden = true;
            containerFilmes.innerHTML = filme[0]
            tabelaTrend.appendChild(containerFilmes)
      })

      const trends = document.querySelectorAll('.trend');

      trends.forEach((trend, index) => {
        let filmeEncontrado = false;
        filmes.forEach((filme) => {
          if (!filmeEncontrado) {
            let titulo = filme.Series_Title;
            let regex = new RegExp(`\\b(?!:.)\\s*${titulo}\\b(?!:.)\\s*`, 'ig')
            if (regex.test(trend.textContent)) {
              const containerFilmesTrend = document.createElement('div');
              containerFilmesTrend.classList.add('filme__trend');
              containerFilmesTrend.innerHTML = `
                <img class="imagem__filme-trend" src="${filme.Poster_Link}" alt="Poster do Filme">
                <li class="filme__item-trend">
                  <p class="filme__item-p-trend">Name: ${filme.Series_Title}</p>
                  <p class="filme__item-p-trend">Rating: ${filme.IMDB_Rating}</p>
                  <p class="filme__item-p-trend">Released: ${filme.Released_Year}</p>
                </li>
              `;
              const existingElement = trend.nextSibling;
              trend.parentNode.insertBefore(containerFilmesTrend, existingElement);
              filmeEncontrado = true;
            }
          }
        });
      });
    });


    