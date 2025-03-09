from flask import Flask, render_template, request, jsonify
import os
import PyPDF2
import docx
import json
from ai_dm import AIDungeonMaster

app = Flask(__name__)
ai_dm = AIDungeonMaster()
UPLOAD_FOLDER = 'uploads'
MEMORY_FILE = 'memory.json'  # File to store long-term memory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_text_from_file(filepath):
    """Extract text from PDF, DOCX, or TXT files."""
    text = ""
    if filepath.endswith(".pdf"):
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    elif filepath.endswith(".docx"):
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif filepath.endswith(".txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    return text

def load_memory():
    """Load stored memory from a file."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    """Save memory data to a file."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)

memory_data = load_memory()  # Load stored memory at startup

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    global memory_data
    user_input = request.json.get('user_input')
    response = ai_dm.player_action("Player", user_input)
    
    # Store conversation in memory
    memory_data.setdefault("conversation", []).append({"player": user_input, "ai": response})
    save_memory(memory_data)
    
    return jsonify({"response": response})

@app.route('/upload', methods=['POST'])
def upload_file():
    global memory_data
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Extract text from the uploaded file and store it in memory
    extracted_text = extract_text_from_file(filepath)
    memory_data.setdefault("knowledge", []).append(extracted_text)
    save_memory(memory_data)
    
    return jsonify({"message": "File uploaded successfully", "filename": file.filename, "extracted_text": extracted_text[:500]})

@app.route('/memory', methods=['GET'])
def get_memory():
    """Retrieve stored memory."""
    return jsonify(memory_data)

if __name__ == '__main__':
    app.run(debug=True)
