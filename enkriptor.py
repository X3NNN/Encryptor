from flask import Flask, render_template, request, send_file, jsonify
import io
import numpy as np
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def vigenere_cipher(text, key, mode):
    result = []
    key_length = len(key)
    text = ''.join(filter(str.isalpha, text.upper()))
    key = key.upper()
    
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_length]) - 65
            if mode == 'encrypt':
                result.append(chr((ord(char) - 65 + shift) % 26 + 65))
            else:
                result.append(chr((ord(char) - 65 - shift) % 26 + 65))
    
    return ''.join(result).lower()

def auto_key_vigenere_cipher(text, key, mode):
    result = []
    text = ''.join(filter(str.isalpha, text.upper()))
    key = key.upper()
    
    if mode == 'encrypt':
        full_key = key + text[:len(text)-len(key)]
    else:
        full_key = key
        for i in range(len(text) - len(key)):
            full_key += chr((ord(text[i + len(key)]) - ord(full_key[i]) + 26) % 26 + 65)
    
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(full_key[i]) - 65
            if mode == 'encrypt':
                result.append(chr((ord(char) - 65 + shift) % 26 + 65))
            else:
                result.append(chr((ord(char) - 65 - shift) % 26 + 65))
    
    return ''.join(result).lower()

def playfair_cipher(text, key, mode):
    def create_matrix(key):
        key = ''.join(dict.fromkeys(key.upper().replace('J', 'I') + 'ABCDEFGHIKLMNOPQRSTUVWXYZ'))
        return [list(key[i:i+5]) for i in range(0, 25, 5)]

    def find_position(matrix, letter):
        for i, row in enumerate(matrix):
            if letter in row:
                return i, row.index(letter)

    matrix = create_matrix(key)
    text = ''.join(filter(str.isalpha, text.upper().replace('J', 'I')))
    if len(text) % 2 != 0:
        text += 'X'

    result = []
    for i in range(0, len(text), 2):
        row1, col1 = find_position(matrix, text[i])
        row2, col2 = find_position(matrix, text[i+1])

        if row1 == row2:
            if mode == 'encrypt':
                result.extend([matrix[row1][(col1+1)%5], matrix[row2][(col2+1)%5]])
            else:
                result.extend([matrix[row1][(col1-1)%5], matrix[row2][(col2-1)%5]])
        elif col1 == col2:
            if mode == 'encrypt':
                result.extend([matrix[(row1+1)%5][col1], matrix[(row2+1)%5][col2]])
            else:
                result.extend([matrix[(row1-1)%5][col1], matrix[(row2-1)%5][col2]])
        else:
            result.extend([matrix[row1][col2], matrix[row2][col1]])

    return ''.join(result).lower()

def hill_cipher(text, key, mode):
    def matrix_mod_inv(matrix, modulus):
        det = int(np.round(np.linalg.det(matrix))) % modulus
        det_inv = pow(det, -1, modulus)
        adjoint = det * np.linalg.inv(matrix)
        return (adjoint % modulus * det_inv) % modulus

    text = ''.join(filter(str.isalpha, text.upper()))
    key_size = int(len(key)**0.5)
    key_matrix = np.array([ord(c) - 65 for c in key.upper()]).reshape((key_size, key_size))

    if mode == 'decrypt':
        key_matrix = matrix_mod_inv(key_matrix, 26)

    result = []
    for i in range(0, len(text), key_size):
        chunk = text[i:i+key_size]
        if len(chunk) < key_size:
            chunk += 'X' * (key_size - len(chunk))
        chunk_vector = np.array([ord(c) - 65 for c in chunk])
        encrypted_vector = np.dot(key_matrix, chunk_vector) % 26
        result.extend([chr(int(c) + 65) for c in encrypted_vector])

    return ''.join(result).lower()

def super_encryption(text, vigenere_key, transposition_key, mode):
    if mode == 'encrypt':
        text = vigenere_cipher(text, vigenere_key, 'encrypt')
        return transposition_cipher(text, transposition_key, 'encrypt')
    else:
        text = transposition_cipher(text, transposition_key, 'decrypt')
        return vigenere_cipher(text, vigenere_key, 'decrypt')

def transposition_cipher(text, key, mode):
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    
    if mode == 'encrypt':
        padded_text = text + 'X' * ((len(key) - len(text) % len(key)) % len(key))
        rows = [padded_text[i:i+len(key)] for i in range(0, len(padded_text), len(key))]
        return ''.join(''.join(row[i] for row in rows) for i in key_order)
    else:
        columns = [''] * len(key)
        col_length, remainder = divmod(len(text), len(key))
        for i, j in enumerate(key_order):
            columns[j] = text[i*col_length + min(i, remainder):(i+1)*col_length + min(i+1, remainder)]
        return ''.join(''.join(col[i:i+1] for col in columns) for i in range(col_length + (1 if remainder else 0)))

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    text = request.form['text']
    key = request.form['key']
    cipher = request.form['cipher']
    mode = request.form['mode']
    
    if cipher == 'vigenere':
        result = vigenere_cipher(text, key, mode)
    elif cipher == 'auto_key_vigenere':
        result = auto_key_vigenere_cipher(text, key, mode)
    elif cipher == 'playfair':
        result = playfair_cipher(text, key, mode)
    elif cipher == 'hill':
        result = hill_cipher(text, key, mode)
    elif cipher == 'super':
        vigenere_key, transposition_key = key.split(',')
        result = super_encryption(text, vigenere_key, transposition_key, mode)
    else:
        return jsonify({'error': 'Invalid cipher method'})
    
    return jsonify({'result': result})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        os.remove(file_path)
        return jsonify({'content': content})

@app.route('/download', methods=['POST'])
def download():
    result = request.form['result']
    buffer = io.BytesIO()
    buffer.write(result.encode('utf-8'))
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='result.txt', mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)