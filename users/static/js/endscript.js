const concluded = document.getElementById('id_concluded');
const wish = document.getElementById('id_wish');
const endInput = document.getElementById('id_finish');
const startInput = document.getElementById('id_begin');

if (concluded || wish) {
    endInput.required = true;
    startInput.required = true;

    function handleConcludedChange() {
        if (wish.checked) {
            wish.checked = false;
        }

        if (concluded.checked) {
            endInput.disabled = true;
            endInput.required = false;
            startInput.disabled = false;
        } else {
            endInput.disabled = false;
            endInput.required = true;
        }
        startInput.required = true;
    }

    function handleWishChange() {
        if (concluded.checked) {
            concluded.checked = false;
        }

        if (wish.checked) {
            endInput.disabled = true;
            endInput.required = false;
            startInput.disabled = true;
            startInput.required = false;
        } else {
            endInput.disabled = false;
            endInput.required = true;
            startInput.disabled = false;
            startInput.required = true;
        }
    }

    concluded.addEventListener('change', handleConcludedChange);
    wish.addEventListener('change', handleWishChange);
}

// Abrir e fechar o Menu Responsivo Toggle
if (document.querySelector(".navbar_toggle")) {
    const navToggle = document.querySelector(".navbar_toggle");
    const links = document.querySelector(".main_nav");

    navToggle.addEventListener('click', function () {
        links.classList.toggle("main_nav");
    });
}

// Função que ocorre quando a tela muda de tamanho
window.addEventListener('resize', function () {
    beginFunction();
});

