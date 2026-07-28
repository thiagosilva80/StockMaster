document.addEventListener("DOMContentLoaded", function () {
    const pesquisa = document.querySelector("#pesquisa-movimentacao");
    const linhas = document.querySelectorAll("#tabela-historico tbody tr");

    if (!pesquisa) {
        return;
    }

    pesquisa.addEventListener("input", function () {
        const termo = pesquisa.value.toLowerCase().trim();

        linhas.forEach(function (linha) {
            const texto = linha.textContent.toLowerCase();

            linha.style.display = texto.includes(termo) ? "" : "none";
        });
    });
});