document.addEventListener("DOMContentLoaded", function () {
    const campoPesquisa = document.querySelector("#pesquisa-produto");
    const linhasProdutos = document.querySelectorAll("#tabela-produtos tbody tr");

    if (campoPesquisa) {
        campoPesquisa.addEventListener("input", function () {
            const pesquisa = campoPesquisa.value.toLowerCase().trim();

            linhasProdutos.forEach(function (linha) {
                const textoLinha = linha.textContent.toLowerCase();

                if (textoLinha.includes(pesquisa)) {
                    linha.style.display = "";
                } else {
                    linha.style.display = "none";
                }
            });
        });
    }

    const botoesExcluir = document.querySelectorAll(".btn-excluir");

    botoesExcluir.forEach(function (botao) {
        botao.addEventListener("click", function (evento) {
            const confirmarExclusao = confirm(
                "Tem certeza de que deseja excluir este produto?"
            );

            if (!confirmarExclusao) {
                evento.preventDefault();
            }
        });
    });
});