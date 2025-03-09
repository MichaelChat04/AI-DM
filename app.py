from flask import Flask, render_template, request, jsonify
import os
import PyPDF2
import docx
from ai_dm import AIDungeonMaster

app = Flask(__name__)
ai_dm = AIDungeonMaster()
UPLOAD_FOLDER = 'uploads'
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

uploaded_knowledge = ""  # Store uploaded knowledge dynamically

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    global uploaded_knowledge
    user_input = request.json.get('user_input')
    response = ai_dm.player_action("Player", user_input)
    
    # If uploaded knowledge exists, AI will use it
    if uploaded_knowledge:
        response += f"\n\n(Based on uploaded knowledge: {uploaded_knowledge[:200]}...)"
    
    return jsonify({"response": response})

@app.route('/upload', methods=['POST'])
def upload_file():
    global uploaded_knowledge
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Extract text from the uploaded file and store it
    extracted_text = extract_text_from_file(filepath)
    uploaded_knowledge = extracted_text  # Store extracted knowledge for AI use
    
    return jsonify({"message": "File uploaded successfully", "filename": file.filename, "extracted_text": extracted_text[:500]})

if __name__ == '__main__':
    app.run(debug=True)
