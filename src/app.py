from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from src.midi import MidiController
from src.patch import Patch, Modulation, Macro
from src.jv1080 import JV1080Patch
from src.xv5080 import XV5080Patch
from src.mu128 import MU128Patch

app = Flask(__name__)
CORS(app)

midi_controller = MidiController()
patches = {
    'JV-1080': JV1080Patch("Default JV-1080 Patch", {}),
    'XV-5080': XV5080Patch("Default XV-5080 Patch", {}),
    'MU-128': MU128Patch("Default MU-128 Patch", {})
}
current_patch = 'JV-1080'

@app.route('/api/midi/ports', methods=['GET'])
def get_midi_ports():
    return jsonify(midi_controller.available_ports)

@app.route('/api/midi/ports/open', methods=['POST'])
def open_midi_port():
    port_name = request.json.get('port_name')
    try:
        midi_controller.open_port(port_name)
        return jsonify({'status': 'success'})
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/midi/ports/close', methods=['POST'])
def close_midi_port():
    midi_controller.close_port()
    return jsonify({'status': 'success'})

@app.route('/api/patch', methods=['GET'])
def get_patch():
    patch = patches[current_patch]
    if isinstance(patch, XV5080Patch):
        return jsonify(patch.to_dict())
    return jsonify(patch.__dict__)

@app.route('/api/patch/parameter', methods=['POST'])
def set_parameter():
    address = request.json.get('address')
    value = request.json.get('value')
    patches[current_patch].set_parameter(address, value)
    return jsonify({'status': 'success'})

@app.route('/api/patch/modulation', methods=['POST'])
def add_modulation():
    source = request.json.get('source')
    destination = request.json.get('destination')
    amount = request.json.get('amount')
    try:
        modulation = Modulation(source, destination, amount)
        patches[current_patch].modulation_matrix.add_modulation(modulation)
        return jsonify({'status': 'success'})
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/patch/modulation/<int:index>', methods=['DELETE'])
def remove_modulation(index):
    try:
        patches[current_patch].modulation_matrix.remove_modulation(index)
        return jsonify({'status': 'success'})
    except IndexError:
        return jsonify({'status': 'error', 'message': 'Modulation not found'}), 404

@app.route('/api/patch/macro', methods=['POST'])
def add_macro():
    name = request.json.get('name')
    parameters = request.json.get('parameters')
    min_value = request.json.get('min_value', 0)
    max_value = request.json.get('max_value', 127)
    macro = Macro(name, parameters, min_value, max_value)
    # We'll use a high, otherwise unused address for the macro
    address = len(patches[current_patch].macros) + 0x1000
    patches[current_patch].macros[address] = macro
    return jsonify({'status': 'success', 'address': address})

@app.route('/api/patch/macro/<int:address>', methods=['DELETE'])
def remove_macro(address):
    if address in patches[current_patch].macros:
        del patches[current_patch].macros[address]
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Macro not found'}), 404

@app.route('/api/patch/macro/<int:address>/apply', methods=['POST'])
def apply_macro(address):
    value = request.json.get('value', 64)
    patch = patches[current_patch]
    if address not in patch.macros:
        return jsonify({'status': 'error', 'message': 'Macro not found'}), 404
    macro = patch.macros[address]
    scaled_value = macro.scale(value)
    for param_addr in macro.parameters:
        patch.set_parameter(param_addr, scaled_value)
    return jsonify({'status': 'success'})


@app.route('/api/patch/macro/randomize', methods=['POST'])
def randomize_macros():
    # Optional filters
    include_macros = request.json.get('addresses')  # list of addresses to include
    intensity = request.json.get('intensity', 1.0)  # scale 0..1 of how extreme the randomization is
    randomness = max(0.0, min(1.0, float(intensity)))

    patch = patches[current_patch]
    macro_items = patch.macros.items()
    if include_macros:
        include_set = set(include_macros)
        macro_items = [(addr, m) for addr, m in macro_items if addr in include_set]

    for addr, macro in macro_items:
        base = 64
        span = int(64 * randomness)
        value = max(0, min(127, base + random.randint(-span, span)))
        scaled_value = macro.scale(value)
        for param_addr in macro.parameters:
            patch.set_parameter(param_addr, scaled_value)

    return jsonify({'status': 'success'})

@app.route('/api/patch/select', methods=['POST'])
def select_patch():
    global current_patch
    patch_name = request.json.get('patch_name')
    if patch_name in patches:
        current_patch = patch_name
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Patch not found'}), 404

@app.route('/api/patch/send', methods=['POST'])
def send_patch():
    patch = patches[current_patch]
    try:
        sysex_data = patch.to_sysex()
        if not isinstance(sysex_data, list) or not sysex_data:
            return jsonify({'status': 'error', 'message': 'Patch cannot be converted to SysEx'}), 400
        midi_controller.send_sysex(sysex_data)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
