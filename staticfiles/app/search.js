let all = document.querySelector('.search__all')
let reviews = document.querySelector('.search__reviews')
let user = document.querySelector('.search__users')
var quem = document.querySelectorAll('.quem')
var paragrafo = document.querySelectorAll('.paragrafo')
var filme = document.querySelectorAll('.filme__opcoes')
var filmeContainer = document.querySelectorAll('.filme__container')
var profile = document.querySelectorAll('.followers__card')

all.addEventListener('click', () => {
    quem.forEach((q) =>{
        q.style.display = ''
    })
    paragrafo.forEach((para) =>{
        para.style.display = ''
    })
    filme.forEach((fil) =>{
        fil.style.display = ''
    })
    profile.forEach((prof) =>{
        prof.style.display = ''
    })
    filmeContainer.forEach((filmo)=>{
        filmo.style.display = ''
    })
})

reviews.addEventListener('click', () => {
    quem.forEach((q) =>{
        q.style.display = ''
    })
    paragrafo.forEach((para) =>{
        para.style.display = ''
    })
    filme.forEach((fil) =>{
        fil.style.display = ''
    })
    profile.forEach((prof) =>{
        prof.style.display = 'none'
    })
    filmeContainer.forEach((filmo)=>{
        filmo.style.display = ''
    })
})

user.addEventListener('click', () => {
    quem.forEach((q) =>{
        q.style.display = 'none'
    })
    paragrafo.forEach((para) =>{
        para.style.display = 'none'
    })
    filme.forEach((fil) =>{
        fil.style.display = 'none'
    })
    profile.forEach((prof) =>{
        prof.style.display = ''
    })
    filmeContainer.forEach((filmo)=>{
        filmo.style.display = 'none'
    })
})