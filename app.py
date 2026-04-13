import os
import io
from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

# Apni API Key yahan dalein
API_KEY = "YOUR_API_KEY_HERE"
genai.configure(api_key=API_KEY)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Test Maker</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white min-h-screen flex items-center justify-center p-4">
    <div class="max-w-xl w-full bg-slate-800 p-6 rounded-xl shadow-2xl border border-slate-700">
        <h1 class="text-2xl font-bold mb-4 text-center text-blue-400">Photo to Test Paper</h1>
        <input type="file" id="imgInp" accept="image/*" class="block w-full mb-4 text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:bg-blue-600 file:text-white cursor-pointer">
        <button onclick="makeTest()" id="btn" class="w-full bg-emerald-600 hover:bg-emerald-500 py-3 rounded-lg font-bold transition">Generate Test</button>
        <div id="load" class="hidden mt-4 text-center animate-pulse text-blue-400">AI is working...</div>
        <div id="res" class="mt-6 p-4 bg-slate-950 rounded-lg hidden whitespace-pre-wrap border border-slate-700 text-sm overflow-auto max-h-96"></div>
    </div>
    <script>
        async function makeTest() {
            const file = document.getElementById('imgInp').files[0];
            if(!file) return alert("Photo select karein!");
            document.getElementById('load').classList.remove('hidden');
            const fd = new FormData();
            fd.append('image', file);
            try {
                const resp = await fetch('/generate', { method: 'POST', body: fd });
                const data = await resp.json();
                document.getElementById('res').innerText = data.result || data.error;
                document.getElementById('res').classList.remove('hidden');
            } catch (e) { alert("Error!"); }
            finally { document.getElementById('load').classList.add('hidden'); }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    img_file = request.files['image']
    img = Image.open(io.BytesIO(img_file.read()))
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(["Extract questions and make a test paper with answers.", img])
    return jsonify({"result": response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
