let map;

async function initMap() {
  // The location of Uluru
  const position = { lat: 41.108306, lng: 16.864571 };
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map, centered at Uluru
  map = new Map(document.getElementById("map"), {
    zoom: 16,
    center: position,
    mapId: "DEMO_MAP_ID",
  });

  // The marker, positioned at Uluru
  const marker = new AdvancedMarkerElement({
    map: map,
    position: position,
    title: "Uluru",
  });
}

initMap();







function handleTableChange() {
  var selectedOption = document.querySelector('select[name="sort"]');
  var selectedTableId;

  // Nascondi tutte le tabelle
  var tables = document.querySelectorAll('table');
  tables.forEach(function(table) {
      table.classList.add('hidden');
  });

  // Mostra la tabella corrispondente all'opzione selezionata
  if (selectedOption.value === 'today') {
      selectedTableId = 'today';
  } else if (selectedOption.value === 'past') {
      selectedTableId = 'past';
  } else if (selectedOption.value === 'incoming') {
      selectedTableId = 'future';
  } else {
      // Opzione predefinita o "Tutti"
      selectedTableId = 'all';
  }

  document.getElementById(selectedTableId).classList.remove('hidden');

  // Imposta l'opzione corrente nel menu a tendina
  selectedOption.selectedIndex = Array.from(selectedOption.options).findIndex(option => option.value === selectedTableId);
}

var selectElement = document.querySelector('select[name="sort"]');
selectElement.addEventListener('change', handleTableChange);

handleTableChange(); // Esegui la funzione inizialmente
