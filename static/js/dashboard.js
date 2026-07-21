document.addEventListener("DOMContentLoaded", function () {
    const botaoMenu = document.querySelector("#botao-menu");
    const sidebar = document.querySelector(".sidebar");
    const elementoData = document.querySelector("#data-atual");

    if (botaoMenu && sidebar) {
        botaoMenu.addEventListener("click", function () {
            sidebar.classList.toggle("sidebar-aberta");
        });
    }

    if (elementoData) {
        const dataAtual = new Date();

        elementoData.textContent = dataAtual.toLocaleDateString("pt-BR", {
            weekday: "long",
            day: "2-digit",
            month: "long",
            year: "numeric"
        });
    }
});