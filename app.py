import os
from flask import Flask, request, render_template_string, send_from_directory
import file_handling
import huffman_coding

app = Flask(__name__)

# Carpetas de entrada y salida
INPUT_FOLDER = "IO/Inputs"
OUTPUT_FOLDER = "IO/Outputs"
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Página principal (formulario)
@app.route("/")
def index():
    return render_template_string("""
    <html>
    <head>
        <title>Compresor Huffman Online</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 40px; }
            form { margin: 20px auto; padding: 20px; border: 1px solid #ccc; width: 300px; }
            input[type=file] { margin: 10px 0; }
            .stats { margin-top: 20px; font-size: 18px; }
        </style>
    </head>
    <body>
        <h1> Compresor Huffman de Imágenes</h1>
        <form action="/compress" method="post" enctype="multipart/form-data">
            <input type="file" name="image" required><br>
            <button type="submit">Comprimir</button>
        </form>
    </body>
    </html>
    """)

# Ruta que maneja la compresión
@app.route("/compress", methods=["POST"])
def compress():
    file = request.files["image"]
    if not file:
        return "No se subió ningún archivo", 400

    # Guardar imagen original en carpeta de entrada
    input_path = os.path.join(INPUT_FOLDER, file.filename)
    file.save(input_path)

    # Leer imagen en bits
    bits = file_handling.read_image_bit_string(input_path)

    # Comprimir
    compressed = huffman_coding.compress(bits)

    # Guardar comprimido
    compressed_filename = file.filename + ".bin"
    compressed_path = os.path.join(OUTPUT_FOLDER, compressed_filename)
    file_handling.write_image(compressed, compressed_path)

    # Calcular estadísticas
    original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(compressed_path)
    ratio = original_size / compressed_size if compressed_size > 0 else 0

    return render_template_string(f"""
    <html>
    <head>
        <title>Resultado de Compresión</title>
        <style>
            body {{ font-family: Arial; text-align: center; padding: 40px; }}
            .stats {{ margin-top: 20px; font-size: 18px; }}
            a {{ display: inline-block; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>✅ Compresión Completa</h1>
        <div class="stats">
            <p><strong>Tamaño original:</strong> {original_size} bytes</p>
            <p><strong>Tamaño comprimido:</strong> {compressed_size} bytes</p>
            <p><strong>Ratio de compresión:</strong> {ratio:.2f}</p>
        </div>
        <a href="/download/{compressed_filename}" download>⬇️ Descargar archivo comprimido</a>
        <br><br>
        <a href="/">⬅️ Volver</a>
    </body>
    </html>
    """)

# Ruta para descargar el archivo comprimido
@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
