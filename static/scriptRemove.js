document.addEventListener("DOMContentLoaded", function() {
    const sectionSelect = document.querySelector("select[name='section']");
    const bevandeSelect = document.getElementById("bevande");
    const viniSelect = document.getElementById("vini");
  
    sectionSelect.addEventListener("change", function() {
        if (sectionSelect.value === "bevande") {
            bevandeSelect.style.display = "block";
            viniSelect.style.display = "none";
        } else if (sectionSelect.value === "vini") {
            bevandeSelect.style.display = "none";
            viniSelect.style.display = "block";
        } else {
            bevandeSelect.style.display = "none";
            viniSelect.style.display = "none";
        }
    });
  });