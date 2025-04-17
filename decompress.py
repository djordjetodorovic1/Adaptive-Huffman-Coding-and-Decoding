from coding import AdaptiveHuffmanCoding
import time

input_file = "compressed_file.bin"
output_file = "decompressed.txt"

ahc = AdaptiveHuffmanCoding()

start_time = time.time()
ahc.decode(input_file, output_file)
decompression_time = time.time() - start_time

print(f"Decompression time: {decompression_time:.6f} seconds")