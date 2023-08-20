document.addEventListener("DOMContentLoaded", function() {
    const sectionSelect = document.querySelector("select[name='section']");
    const bevandeSelect = document.getElementById("bevande");
    const viniSelect = document.getElementById("vini");
    const antipastiSelect = document.getElementById("antipasti");
  
    sectionSelect.addEventListener("change", function() {
        if (sectionSelect.value === "bevande") {
            bevandeSelect.style.display = "block";
            viniSelect.style.display = "none";
            antipastiSelect.style.display = "none";
        } else if (sectionSelect.value === "vini") {
            bevandeSelect.style.display = "none";
            viniSelect.style.display = "block";
            antipastiSelect.style.display = "none";
        } else if (sectionSelect.value === "antipasti") {
            bevandeSelect.style.display = "none"
            viniSelect.style.display = "none";
            antipastiSelect.style.display = "block";
        } else {
            bevandeSelect.style.display = "none";
            viniSelect.style.display = "none";
        }
    });
  });