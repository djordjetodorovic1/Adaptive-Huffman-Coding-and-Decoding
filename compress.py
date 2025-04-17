from coding import AdaptiveHuffmanCoding
import os, time

input_file = "input_file.txt"
output_file = "compressed_file.bin"

ahc = AdaptiveHuffmanCoding()

start_time = time.time()
ahc.encode(input_file, output_file)
compression_time = time.time() - start_time

original_size = os.path.getsize(input_file)
compressed_size = os.path.getsize(output_file)
compression_ration = (1 - compressed_size / original_size) * 100

print(f"Original size: {original_size} bytes")
print(f"Compressed size: {compressed_size} bytes")
print(f"Compression ratio: {compression_ration:.2f}%")
print(f"Compression time: {compression_time:.6f} seconds")
