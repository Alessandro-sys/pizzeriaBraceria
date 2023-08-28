function validateForm() {
    var dataInput = document.getElementById("data");
    var oggi = new Date();
    var selectedDate = new Date(dataInput.value);
  
    // Impedisci la selezione di lunedì
    if (selectedDate.getDay() === 1) { // 1 rappresenta il lunedì
        alert("Non puoi selezionare un lunedì.");
        dataInput.value = ""; // Azzeriamo la data selezionata
        return false; // Impedisce l'invio del modulo
      }
    
    // Impedisci la selezione di giorni precedenti a oggi
    if (selectedDate < oggi) {
      alert("Non puoi selezionare una data precedente a oggi.");
      dataInput.value = oggi.toISOString().split('T')[0];
      return false; // Impedisce l'invio del modulo
    }
  
    
  
    return true; // Consente l'invio del modulo se la data è valida
  }


// script.js

// Funzione per gestire il cambiamento della data
function dateChanged() {
  // Ottieni l'elemento input della data
  var dateInput = document.getElementById("data");
  
  // Verifica se la data è stata selezionata
  if (dateInput.value) {
    // Invia il modulo
    document.getElementById("formPrenota").submit();
  }
}

// Aggiungi un gestore di eventi per il cambiamento della data
document.getElementById("data").addEventListener("change", dateChanged);

  


// Ottieni l'elemento dell'input
const telefonoInput = document.getElementById('telefonoInput');

// Aggiungi un gestore di eventi per l'input
telefonoInput.addEventListener('input', function() {
  const currentLength = telefonoInput.value.length;

  // Verifica se la lunghezza supera il limite di 15 caratteri
  if (currentLength > 15) {
    telefonoInput.value = telefonoInput.value.slice(0, 15);
    alert("Non puoi inserire un numero di telefono superiore a 15 caratteri");
     // Tronca il valore a 15 caratteri
  }
});
