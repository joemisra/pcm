from flask import Flask, jsonify, request
from src.midi import MidiController
from src.patch import Patch
from src.jv1080 import JV1080Patch
from src.xv5080 import XV5080Patch

app = Flask(__name__)
midi_controller = MidiController()
patches = {
    'JV-1080': JV1080Patch("Default JV-1080 Patch", {}),
    'XV-5080': XV5080Patch("Default XV-5080 Patch", {})
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
    return jsonify(patches[current_patch].__dict__)

@app.route('/api/patch/parameter', methods=['POST'])
def set_parameter():
    address = request.json.get('address')
    value = request.json.get('value')
    patches[current_patch].set_parameter(address, value)
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

if __name__ == '__main__':
    app.run(debug=True)
