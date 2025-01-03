document.getElementById("search-button").addEventListener("click", () => {
    const elementName = document.getElementById("element-input").value.trim();
    if (!elementName) {
        alert("Please enter an element name.");
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
                document.getElementById("error-message").style.display = 'block';
                document.getElementById("error-message").textContent = data.error;
            } else {
                displayElementData(data);
                document.getElementById("error-message").style.display = 'none';
            }
        })
        .catch(error => {
            console.error(error);
            alert("An error occurred while fetching element data.");
        });
});

document.getElementById('bohr-button').addEventListener('click', function () {
    const elementInput = document.getElementById('element-input').value;

    if (!elementInput) {
        alert('Please enter an element name.');
        return;
    }

    fetch('/bohr_model/' + elementInput)
        .then(response => response.json())
        .then(data => {
            if (data.image_path) {
                // Display the Bohr model image
                const bohrModelContainer = document.getElementById('bohr-model-container');
                bohrModelContainer.innerHTML = `<img src="${data.image_path}" alt="Bohr Model">`;
            } else {
                alert('Error generating Bohr model: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching the Bohr model.');
        });
});

document.querySelectorAll(".orbital-button").forEach(button => {
    button.addEventListener("click", () => {
        const orbitalType = button.getAttribute("data-orbital");

        fetch(`/visualize_orbital/${orbitalType}`, {
            method: 'GET',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    alert(data.message);  // Show the message returned from the backend
                }
            })
            .catch(error => {
                console.error(error);
                alert("An error occurred while generating the orbital visualization.");
            });
    });
});

function displayElementData(data) {
    document.getElementById("element-summary").textContent = data.summary || "No summary available.";
    const detailsList = document.getElementById("element-details");
    detailsList.innerHTML = ""; // Clear previous details
    if (data.details) {
        for (const [key, value] of Object.entries(data.details)) {
            const listItem = document.createElement("li");
            listItem.textContent = `${key}: ${value}`;
            detailsList.appendChild(listItem);
        }
    } else {
        detailsList.innerHTML = "<li>No detailed data available.</li>";
    }
}
