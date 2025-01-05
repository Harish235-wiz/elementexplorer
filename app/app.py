from flask import Flask, render_template, request, jsonify
from element_logic import fetch_element_data, generate_bohr_model, generate_orbital_visualization
import logging

app = Flask(__name__)

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_element():
    try:
        data = request.get_json()
        element_name = data.get('elementName')
        if not element_name:
            return jsonify({"error": "Element name is required."}), 400

        element_data = fetch_element_data(element_name)
        return jsonify(element_data)
    except Exception as e:
        logging.error(f"Error fetching data for element: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/bohr_model/<element>', methods=['GET'])
def bohr_model(element):
    try:
        # Look up the atomic number for the element
        element_data = {
    'hydrogen': 1,
    'helium': 2,
    'lithium': 3,
    'beryllium': 4,
    'boron': 5,
    'carbon': 6,
    'nitrogen': 7,
    'oxygen': 8,
    'fluorine': 9,
    'neon': 10,
    'sodium': 11,
    'magnesium': 12,
    'aluminum': 13,
    'silicon': 14,
    'phosphorus': 15,
    'sulfur': 16,
    'chlorine': 17,
    'argon': 18,
    'potassium': 19,
    'calcium': 20,
    'scandium': 21,
    'titanium': 22,
    'vanadium': 23,
    'chromium': 24,
    'manganese': 25,
    'iron': 26,
    'cobalt': 27,
    'nickel': 28,
    'copper': 29,
    'zinc': 30,
    'gallium': 31,
    'germanium': 32,
    'arsenic': 33,
    'selenium': 34,
    'bromine': 35,
    'krypton': 36,
    'rubidium': 37,
    'strontium': 38,
    'yttrium': 39,
    'zirconium': 40,
    'niobium': 41,
    'molybdenum': 42,
    'technetium': 43,
    'ruthenium': 44,
    'rhodium': 45,
    'palladium': 46,
    'silver': 47,
    'cadmium': 48,
    'indium': 49,
    'tin': 50,
    'antimony': 51,
    'tellurium': 52,
    'iodine': 53,
    'xenon': 54,
    'cesium': 55,
    'barium': 56,
    'lanthanum': 57,
    'cerium': 58,
    'praseodymium': 59,
    'neodymium': 60,
    'promethium': 61,
    'samarium': 62,
    'europium': 63,
    'gadolinium': 64,
    'terbium': 65,
    'dysprosium': 66,
    'holmium': 67,
    'erbium': 68,
    'thulium': 69,
    'ytterbium': 70,
    'lutetium': 71,
    'hafnium': 72,
    'tantalum': 73,
    'tungsten': 74,
    'rhenium': 75,
    'osmium': 76,
    'iridium': 77,
    'platinum': 78,
    'gold': 79,
    'mercury': 80,
    'thallium': 81,
    'lead': 82,
    'bismuth': 83,
    'polonium': 84,
    'astatine': 85,
    'radon': 86,
    'francium': 87,
    'radium': 88,
    'actinium': 89,
    'thorium': 90,
    'protactinium': 91,
    'uranium': 92,
    'neptunium': 93,
    'plutonium': 94,
    'americium': 95,
    'curium': 96,
    'berkelium': 97,
    'californium': 98,
    'einsteinium': 99,
    'fermium': 100,
    'mendelevium': 101,
    'nobelium': 102,
    'lawrencium': 103,
    'rutherfordium': 104,
    'dubnium': 105,
    'seaborgium': 106,
    'bohrium': 107,
    'hassium': 108,
    'meitnerium': 109,
    'darmstadtium': 110,
    'roentgenium': 111,
    'copernicium': 112,
    'nihonium': 113,
    'flerovium': 114,
    'moscovium': 115,
    'livermorium': 116,
    'tennessine': 117,
    'oganesson': 118,
}

        atomic_number = element_data.get(element.lower())
        if not atomic_number:
            raise ValueError(f"Atomic number for {element} not found.")

        # Generate the Bohr model
        bohr_model_path = generate_bohr_model(atomic_number)

        # Return the image path to be displayed on the frontend
        return jsonify({'image_path': bohr_model_path})
    except Exception as e:
        logging.error(f"Error generating Bohr model for {element}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/visualize_orbital/<orbital_type>', methods=['GET'])
def visualize_orbital(orbital_type):
    try:
        # Generate orbital visualization (adjust based on your logic)
        message = generate_orbital_visualization(orbital_type)

        return jsonify({"message": f"{orbital_type.upper()} orbital visualization successful!"})
    except Exception as e:
        logging.error(f"Error visualizing orbital {orbital_type}: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

