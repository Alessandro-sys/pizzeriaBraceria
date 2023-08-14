// popup.js

document.addEventListener("DOMContentLoaded", function() {
    const popup = document.getElementById("popup");
    const yesBtn = document.getElementById("yesBtn");
    const noBtn = document.getElementById("noBtn");
    const formNotFilled = document.getElementById("contenitoreNonRiempito");
    const formFilled = document.getElementById("contenitoreRiempito");
  
    popup.classList.remove("hide");
    popup.classList.add("show");
    formNotFilled.classList.remove("show");
    formNotFilled.classList.add("hide");
    formFilled.classList.remove("show");
    formFilled.classList.add("hide");
  
    yesBtn.addEventListener("click", () => {
      // Qui puoi aggiungere la logica per autocompletare i dati
        popup.classList.remove("show");
        popup.classList.add("hide");
        formFilled.classList.remove("hide");
        formFilled.classList.add("show");
    });
  
    noBtn.addEventListener("click", () => {
      // Qui puoi gestire l'alternativa se l'utente sceglie di non autocompletare i dati
      popup.classList.remove("show");
      popup.classList.add("hide");
      formNotFilled.classList.remove("hide");
      formNotFilled.classList.add("show");
    });
  });
  