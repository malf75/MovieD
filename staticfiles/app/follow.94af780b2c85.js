document.addEventListener('DOMContentLoaded', function() {
    let botao = document.querySelector('.botao_follow');
    if (botao) {
        let botaoValue = botao.value;
        let botao2 = document.getElementsByName('follow')[0];

        if (botaoValue === 'unfollow') {
            botao2.style.border = '1px solid red';
            botao2.style.color = 'red';
        }
    }
});