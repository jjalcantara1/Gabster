	document.getElementById("dropdownBtn").addEventListener("click", function() {
        var dropdown = document.getElementById("myDropdown");
        if (dropdown.style.display === "block") {
            dropdown.style.display = "none";
        } else {
            dropdown.style.display = "block";
        }
    });

    window.addEventListener("click", function(event) {
        if (!event.target.matches("#dropdownBtn")) {
            var dropdown = document.getElementById("myDropdown");
            if (dropdown.style.display === "block") {
                dropdown.style.display = "none";
            }
        }
    });