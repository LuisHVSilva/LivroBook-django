// Função acontece quando a tela é carregada.
window.addEventListener('DOMContentLoaded', function () { nBooks(), nPages() });


function nBooks() {
    var data = {
        labels: ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
        datasets: [
            {
                backgroundColor: ["#E02ACD"],
                data: nBooksData
            }
        ]
    }

    var options = {
        scales: {
            y: { display: true }, // Configuração para desativar as linhas de grade no eixo Y
            x: { display: true }, // Configuração para desativar as linhas de grade no eixo X
        },
        plugins: {
            legend: { display: false } // Configuração para desativar a exibição da legenda
        },
    };

    var canvas = document.getElementById('nBooks');

    if (window.innerWidth < 1000) {
        canvas.width = 350; // Defina a largura desejada
    } else {
        canvas.width = 600; // Defina a largura desejada
    }

    canvas.height = canvas.offsetHeight; // Mantenha a altura atual

    var ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: options
    });
}

function nPages() {
    var data = {
        labels: ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
        datasets: [
            {
                backgroundColor: ["#E02ACD"],
                data: nPagesData
            }
        ]
    }

    var options = {
        scales: {
            y: { display: true }, // Configuração para desativar as linhas de grade no eixo Y
            x: { display: true }, // Configuração para desativar as linhas de grade no eixo X
        },
        plugins: {
            legend: { display: false } // Configuração para desativar a exibição da legenda
        },
    };

    var canvas = document.getElementById('nPages');

    if (window.innerWidth < 1000) {
        canvas.width = 350; // Defina a largura desejada
    } else {
        canvas.width = 600; // Defina a largura desejada
    }

    canvas.height = canvas.offsetHeight; // Mantenha a altura atual

    var ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: options
    });
}