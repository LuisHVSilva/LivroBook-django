// Deixa as letras em maiúsculo.
function upperCase(elemento) {
  var texto = elemento.value;
  elemento.value = texto.toUpperCase();
}

// Desabilitar os campos de data no UpdateView quando o botão de excluir for clicado.
function deleteFieldRequired(){
    endInput.required = false;
    startInput.required = false;
}

// Função acontece quando a tela é carregada.
window.addEventListener('DOMContentLoaded', function () {
  beginFunction();
});


// Função para determinar quando as demais funções relacionadas a tamanho de tela devem ou não acontecer.
function beginFunction() {
  var width = window.innerWidth; // Pega o tamanho da tela.

  if (width <= 1000) { // Se a tela for menor ou igual a 1000 px.
    if (document.getElementById('firstTable')) {
      const table = document.getElementById('firstTable');
      removeColumn(table);
    }
    if (document.getElementsByClassName("right")[0]) {
      const right = document.getElementsByClassName("right")[0];
      rightRemoveLeftCenter(right);
    }
  }

  if (document.getElementById('id_concluded')) {
      const concluded = document.getElementById('id_concluded');
      const wish = document.getElementById('id_wish');
      const endInput = document.getElementById('id_finish');
      const startInput = document.getElementById('id_begin');
      checkUpdateView(concluded, wish, endInput, startInput);
    }
}

// Função para remover colunas de acordo com o tamanho do dispositivo.
function removeColumn(table) {
  // const table = document.getElementById('firstTable');
  var columnIndex = 1; // Índice da coluna a ser removida (começando em 0).
  var columRemoveQuantity = 3; // Quantidade de colunas que será removida.
  var rows = table.getElementsByTagName('tr'); // Pega todas as linhas da coluna.

  for (var j = 1; j <= columRemoveQuantity; j++) {  // Loop para repetir o que está interno pela quantidade de vezes de 'columRemoveQuantity'.
    var th = table.getElementsByTagName('th')[1];  // Pega o cabeçalho da coluna que está em primeira posição (lembrando que começa por 0).
    if (th) {
      th.remove();  // Remove o cabeçalho da coluna.

      for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        if (cells.length > columnIndex) {
          cells[columnIndex].remove();
        }
      }
    }
  }
}

// Função para remover o lado direito da tela e centralizar o lado direito.
function rightRemoveLeftCenter(right) {
  if (right) {
    right.remove();
  }
}

// Função para manter os campos desabilitados na URL 'book-update' caso o checkbox de desejo ou de terminado tenham sido marcados na hora de criar o cadastro daquele respectivo livro.
function checkUpdateView(concluded, wish, endInput, startInput) {
  endInput.disabled = false;
  endInput.required = true;
  startInput.disabled = false;
  startInput.required = true;

  if (wish.checked) { // Como quando o livro é marcado como desejo ainda não foi terminado, no banco é salvo como não terminado. Tira o checkbox do terminado quando renderiza a página.
    concluded.checked = false;
    endInput.disabled = true;
    endInput.required = false;
    startInput.disabled = true;
    startInput.required = false;
  }

  if (concluded.checked) {
    startInput.disabled = false;
    startInput.required = true;
  }
}
