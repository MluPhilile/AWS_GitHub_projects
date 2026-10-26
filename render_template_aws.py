from flask import Flask, request, jsonify, render_template
from typing import Union, List

app = Flask(__name__)

def add_numbers(numbers: List[Union[int, float]]) -> Union[int, float]:
    """Calculates the sum of a list of numbers with explicit type checking."""
    if not numbers:
        raise ValueError("The list of numbers cannot be empty.")
    for num in numbers:
        if isinstance(num, bool) or not isinstance(num, (int, float)):
            raise TypeError(f"All items must be numeric. Found invalid item: {num}")
    return sum(numbers)


# --- Key Feature: Template View Routing ---

@app.route('/')
def index():
    """
    Renders the central index.html frontend interface.
    Flask automatically looks inside the local /templates directory.
    """
    return render_template('index.html')


# --- API Endpoint (Unchanged) ---

@app.route('/api/add', methods=['POST'])
def handle_add_numbers():
    data = request.get_json(silent=True)
    if data is None or 'numbers' not in data:
        return jsonify({"status": "error", "message": "Invalid JSON blueprint structure."}), 400

    input_list = data['numbers']
    if not isinstance(input_list, list):
        return jsonify({"status": "error", "message": "The 'numbers' key must match a list."}), 400

    try:
        total_sum = add_numbers(input_list)
        return jsonify({"status": "success", "result": total_sum, "items_processed": len(input_list)}), 200
    except (TypeError, ValueError) as error:
        return jsonify({"status": "error", "message": str(error)}), 422

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=80)
