from flask import Flask, jsonify, request
import os, random, string
from pathlib import Path

app = Flask(__name__)

filesDir = Path("C:/Users/chiran/PycharmProjects/files")
@app.route('/')
def helloWorld():
    return 'Hello World!'

@app.route('/files', methods=['GET'])
def getFileList():
    listOfFiles=os.listdir(filesDir)
    return jsonify(listOfFiles)

@app.route('/files/<filename>', methods=['GET'])
def getFileByName(filename):
    filePath = os.path.join(filesDir, filename)

    if os.path.isfile(filePath):
        file = open(filePath, 'r')
        return jsonify({'content': fileRead()})
    return jsonify({'error': 'File not found'}), 404

@app.route('/files/<filename>', methods=['DELETE'])
def deleteFileByName(filename):
    filePath = os.path.join(filesDir, filename)
    if os.path.isfile(filePath):
        os.remove(filePath)
        return jsonify({'message': 'File was deleted successfully.'}), 200
    return jsonify({'error': 'File not found.'}), 404

    filePath = os.path.join(filesDir, filename)
    if os.path.isfile(filePath):
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(newContent)
        return jsonify({'message': 'File was updated successfully.'}), 200
    return jsonify({'error': 'File not found.'}), 404

@app.route('/files', methods=['POST'])
def createFileByNameAndContent():
    data = request.get_json()
    filename = data.get('filename')
    content = data.get('content', '')

    if filename and content is not None:
        filePath = os.path.join(filesDir, filename)
        with open(filePath, 'w') as file:
            file.write(content)
        return jsonify({'message': 'File created', 'filename': filename}), 201

    return jsonify({'error': 'Filename and content are required'}), 400

@app.route('/files/content', methods=['POST'])
def create_file_by_content():
    data = request.get_json()
    content = data.get('content', '')

    if content is not None:
        random_digits = ''.join(random.choices(string.digits, k=5))
        filename = f'file{random_digits}.txt'
        filePath = os.path.join(filesDir, filename)
        with open(filePath, 'w') as file:
            file.write(content)
        return jsonify({'message': 'File created', 'filename': filename}), 201

    return jsonify({'error': 'Content are required'}), 400

if __name__ == '__main__':
    app.run()