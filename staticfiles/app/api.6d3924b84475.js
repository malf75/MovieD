document.addEventListener('DOMContentLoaded', async () => {
const selectFilmes = document.createElement('select')

await fetch(`/api/filme_info/`)
  .then(res => res.json())
  .then((filmes) => {

    selectFilmes.style.position = "absolute"
    selectFilmes.style.display = "none"
    selectFilmes.title = "opções de filme"

    filmes.filmes.forEach((filme) => {
      const option = document.createElement('option')
      option.value = filme.Series_Title
      option.text = filme.Series_Title
      selectFilmes.appendChild(option)
    });
    
    const inputTexto = document.getElementById('postagem')
    if (inputTexto) {
    
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
    });
  });
