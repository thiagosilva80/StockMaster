document.addEventListener("DOMContentLoaded", function () {
    const pesquisa = document.querySelector("#pesquisa-categoria");
    const linhas = document.querySelectorAll("#tabela-categorias tbody tr");
    const botoesExcluir = document.querySelectorAll(".btn-excluir");

    if (pesquisa) {
        pesquisa.addEventListener("input", function () {
            const termo = pesquisa.value.toLowerCase().trim();

            linhas.forEach(function (linha) {
                const texto = linha.textContent.toLowerCase();

                linha.style.display = texto.includes(termo) ? "" : "none";
            });
        });
    }

    botoesExcluir.forEach(function (botao) {
        botao.addEventListener("click", function (evento) {
            const confirmar = confirm(
                "Tem certeza de que deseja excluir esta categoria?"
            );

            if (!confirmar) {
                evento.preventDefault();
            }
        });
    });
});