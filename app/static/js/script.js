// Event listener for the search button
document.getElementById("search-button").addEventListener("click", () => {
    const elementName = document.getElementById("element-input").value.trim();

    if (!elementName) {
        alert("Please enter an element name or symbol.");
        return;
    }

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ elementName: elementName }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            document.getElementById("error-message").textContent = data.error;
            document.getElementById("error-message").style.display = "block";
        } else {
            document.getElementById("error-message").style.display = "none";
            displayElementData(data);
        }
    })
    .catch(error => {
        console.error("Error fetching element data:", error);
        alert("An error occurred while fetching element data.");
    });
});

// Event listener for the Bohr model generation button
document.getElementById("bohr-button").addEventListener("click", () => {
    const elementInput = document.getElementById("element-input").value.trim();

    if (!elementInput) {
        alert("Please enter an element name or symbol.");
        return;
    }

    fetch(`/bohr_model/${elementInput}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(`Error generating Bohr model: ${data.error}`);
            } else if (data.image_path) {
                const bohrModelContainer = document.getElementById("bohr-model-container");
                bohrModelContainer.innerHTML = `<img src="${data.image_path}" alt="Bohr Model">`;
            }
        })
        .catch(error => {
            console.error("Error generating Bohr model:", error);
            alert("An error occurred while generating the Bohr model.");
        });
});

// Event listeners for orbital visualization buttons
document.querySelectorAll(".orbital-button").forEach(button => {
    button.addEventListener("click", () => {
        const orbitalType = button.getAttribute("data-orbital");

        fetch(`/visualize_orbital/${orbitalType}`, { method: 'GET' })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    alert(`Error generating ${orbitalType} orbital: ${data.error}`);
                } else {
                    const orbitalContainer = document.getElementById("orbital-visualization-container");
                    orbitalContainer.innerHTML = `<img src="${data.image_path}" alt="${orbitalType.toUpperCase()} Orbital">`;
                }
            })
            .catch(error => {
                console.error(`Error generating ${orbitalType} orbital:`, error);
                alert(`An error occurred while generating the ${orbitalType} orbital.`);
            });
    });
});

// Function to display element data
function displayElementData(data) {
    // Display the general summary
    document.getElementById("element-summary").textContent = data.summary || "No summary available.";

    // Display the detailed data
    const detailsList = document.getElementById("element-details");
    detailsList.innerHTML = ""; // Clear previous details

    Object.entries(data.details || {}).forEach(([key, value]) => {
        const listItem = document.createElement("li");
        listItem.textContent = `${key}: ${value}`;
        detailsList.appendChild(listItem);
    });
}
