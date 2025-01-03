import wikipediaapi
import matplotlib
matplotlib.use('Agg')  # This forces Matplotlib to use a non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from mendeleev import element
from pubchempy import get_compounds
import os

# Hardcoded periodic table data for fallback
PERIODIC_TABLE = {
    "Hydrogen": 1, "Helium": 2, "Lithium": 3, "Beryllium": 4, "Boron": 5,
    "Carbon": 6, "Nitrogen": 7, "Oxygen": 8, "Fluorine": 9, "Neon": 10,
    "Sodium": 11, "Magnesium": 12, "Aluminum": 13, "Silicon": 14, "Phosphorus": 15,
    "Sulfur": 16, "Chlorine": 17, "Argon": 18, "Potassium": 19, "Calcium": 20,
    # Add more as needed
}

# Fetch Wikipedia Summary
def fetch_wikipedia_summary(element_name):
    wiki = wikipediaapi.Wikipedia(language="en", user_agent="ElementExplorer/1.0 (contact@example.com)")
    page = wiki.page(element_name)
    if page.exists():
        summary = page.summary[:2000]
        if "." in summary[1990:]:
            return summary[:summary[:2000].rfind(".") + 1]
        return summary
    return "No summary available."

# Fetch Element Data from Mendeleev Library
def fetch_mendeleev_data(element_name):
    try:
        elem = element(element_name.capitalize())
        data = {
            "Atomic Number": elem.atomic_number,
            "Symbol": elem.symbol,
            "Atomic Mass": f"{elem.atomic_weight:.2f} u" if elem.atomic_weight else "N/A",
            "Density": f"{elem.density:.2f} g/cm³" if elem.density else "N/A",
            "Electronegativity": f"{elem.en_pauling:.2f}" if elem.en_pauling else "N/A",
            "Oxidation States": ", ".join(map(str, elem.oxistates)) if elem.oxistates else "N/A",
            "Melting Point": f"{elem.melting_point} K" if elem.melting_point else "N/A",
            "Boiling Point": f"{elem.boiling_point} K" if elem.boiling_point else "N/A",
            "Electronic Configuration": str(elem.ec).replace("[", "").replace("]", "").replace(",", "").strip() if elem.ec else "N/A",
        }
        return data
    except Exception as e:
        return {"error": f"Failed to fetch data for {element_name}: {str(e)}"}

# Fetch PubChem Data
def fetch_pubchem_data(element_name):
    try:
        compound = get_compounds(element_name, 'name')[0]
        data = {
            "Molecular Weight": f"{compound.molecular_weight:.2f} u",
            "InChI Key": compound.inchikey,
            "SMILES": compound.isomeric_smiles,
        }
        return data
    except Exception:
        return {}

# Combine Data Fetchers
def fetch_element_data(element_name):
    wikipedia_summary = fetch_wikipedia_summary(element_name)
    pubchem_data = fetch_pubchem_data(element_name)
    mendeleev_data = fetch_mendeleev_data(element_name)

    atomic_number = PERIODIC_TABLE.get(element_name.capitalize(), None)
    if atomic_number and "Atomic Number" not in mendeleev_data:
        mendeleev_data["Atomic Number"] = str(atomic_number)

    return {
        "summary": wikipedia_summary,
        "details": {**mendeleev_data, **pubchem_data},
    }

# Bohr Model Visualization


def generate_bohr_model(atomic_number):
    """
    Generates a Bohr model based on the atomic number.
    
    Parameters:
        atomic_number (int): The atomic number of the element.
        
    Returns:
        str: Path to the saved Bohr model image.
    """
    if not isinstance(atomic_number, int) or atomic_number <= 0:
        raise ValueError("Invalid atomic number provided.")

    # Calculate the electron distribution across orbitals
    num_electrons = atomic_number
    orbitals = []
    max_electrons = [2, 8, 18, 32, 50, 72, 98]  # Max electrons in each shell (K, L, M, N, etc.)

    for max_e in max_electrons:
        if num_electrons <= 0:
            break
        if num_electrons >= max_e:
            orbitals.append(max_e)
            num_electrons -= max_e
        else:
            orbitals.append(num_electrons)
            break

    # Create the Bohr model plot
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw orbitals and place electrons
    for i, electrons in enumerate(orbitals):
        # Draw the circular orbital
        circle = plt.Circle((0, 0), i + 1, fill=False, color="blue", linewidth=1.5)
        ax.add_artist(circle)
        # Place the electrons on the orbital
        for j in range(electrons):
            angle = 2 * np.pi * j / electrons
            x, y = (i + 1) * np.cos(angle), (i + 1) * np.sin(angle)
            ax.plot(x, y, 'ro', markersize=6)

    # Add the nucleus
    ax.plot(0, 0, 'yo', markersize=15)
    plt.title(f"Bohr Model of Element with Atomic Number {atomic_number}")

    # Save the image
    filepath = os.path.join("static", "images", f"bohr_model_{atomic_number}.png")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    plt.savefig(filepath)
    plt.close()

    return filepath

# Orbital Visualization
def generate_orbital_visualization(orbital_type):
    fig = go.Figure()

    if orbital_type == 's':
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        fig.add_trace(go.Surface(z=z, x=x, y=y, colorscale='Blues'))

    elif orbital_type == 'p':
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(-1, 1, 100)
        x = np.outer(np.sin(u), v)
        y = np.outer(np.cos(u), v)
        z = np.outer(np.ones(np.size(u)), v)
        fig.add_trace(go.Surface(z=z, x=x, y=y, colorscale='Reds'))

    elif orbital_type == 'd':
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(-1, 1, 100)
        x = np.outer(np.sin(u)**2 * np.cos(2*u), v)
        y = np.outer(np.sin(u)**2 * np.sin(2*u), v)
        z = np.outer(np.cos(u), v)
        fig.add_trace(go.Surface(z=z, x=x, y=y, colorscale='Greens'))

    elif orbital_type == 'f':
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(-1, 1, 100)
        x = np.outer(np.sin(u)**3 * np.cos(3*u), v)
        y = np.outer(np.sin(u)**3 * np.sin(3*u), v)
        z = np.outer(np.cos(u), v)
        fig.add_trace(go.Surface(z=z, x=x, y=y, colorscale='Purples'))

    fig.update_layout(title=f"{orbital_type.upper()} Orbital Visualization", autosize=True)
    fig.show()
