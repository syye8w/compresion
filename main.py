import os
import file_handling
import huffman_coding

input_folder = "IO/Inputs"
output_folder = "IO/Outputs"
os.makedirs(output_folder, exist_ok=True)

valid_ext = (".jpg", ".jpeg", ".png", ".bmp")
for filename in os.listdir(input_folder):
    if filename.lower().endswith(valid_ext):
        image_path = os.path.join(input_folder, filename)
        print(f"\n🔹 Procesando: {filename}")

        # Leer
        bits = file_handling.read_image_bit_string(image_path)

        # Comprimir
        compressed = huffman_coding.compress(bits)

        # Guardar comprimido
        compressed_path = os.path.join(output_folder, filename + ".bin")
        file_handling.write_image(compressed, compressed_path)

        # Mostrar ratio
        cr = len(bits) / len(compressed)
        print(f"   📊 Compression Ratio: {cr:.2f}")

        # Descomprimir
        decompressed = huffman_coding.decompress(compressed)
        decompressed_path = os.path.join(output_folder, "decompressed_" + filename)
        file_handling.write_image(decompressed, decompressed_path)
