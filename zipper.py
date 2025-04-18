import heapq
from collections import defaultdict
import os
import argparse

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanZipper:
    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}

    def _build_frequency_dict(self, data):
        frequency = defaultdict(int)
        for byte in data:
            frequency[byte] += 1
        return frequency

    def _build_huffman_tree(self, frequency):
        heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            internal = HuffmanNode(None, left.freq + right.freq)
            internal.left = left
            internal.right = right
            heapq.heappush(heap, internal)

        return heap[0]

    def _build_codes(self, root, code=""):
        if root is None:
            return
        if root.char is not None:
            self.codes[root.char] = code
            self.reverse_codes[code] = root.char
            return
        self._build_codes(root.left, code + "0")
        self._build_codes(root.right, code + "1")

    def compress(self, input_file, output_file):
        with open(input_file, 'rb') as f:
            data = f.read()

        frequency = self._build_frequency_dict(data)
        huffman_tree = self._build_huffman_tree(frequency)
        self.codes.clear()
        self.reverse_codes.clear()
        self._build_codes(huffman_tree)

        encoded = ''.join(self.codes[byte] for byte in data)
        padding = (8 - len(encoded) % 8) % 8
        encoded += '0' * padding

        encoded_bytes = bytearray()
        for i in range(0, len(encoded), 8):
            encoded_bytes.append(int(encoded[i:i+8], 2))

        with open(output_file, 'wb') as f:
            f.write(len(frequency).to_bytes(4, byteorder='big'))
            for byte, freq in frequency.items():
                f.write(bytes([byte]))
                f.write(freq.to_bytes(4, byteorder='big'))
            f.write(padding.to_bytes(1, byteorder='big'))
            f.write(encoded_bytes)

        # Print file sizes and compression ratio
        original_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(output_file)
        ratio = compressed_size / original_size if original_size else 0

        print(f"✅ Compression complete: '{input_file}' → '{output_file}'")
        print(f"📏 Original size: {original_size} bytes")
        print(f"📦 Compressed size: {compressed_size} bytes")
        print(f"📉 Compression ratio: {ratio:.2f}")

    def decompress(self, input_file, output_file):
        with open(input_file, 'rb') as f:
            freq_dict_size = int.from_bytes(f.read(4), byteorder='big')
            frequency = {}
            for _ in range(freq_dict_size):
                byte = f.read(1)[0]
                freq = int.from_bytes(f.read(4), byteorder='big')
                frequency[byte] = freq
            padding = int.from_bytes(f.read(1), byteorder='big')
            encoded_data = f.read()

        huffman_tree = self._build_huffman_tree(frequency)
        self.codes.clear()
        self.reverse_codes.clear()
        self._build_codes(huffman_tree)

        binary_string = ''.join(format(byte, '08b') for byte in encoded_data)
        binary_string = binary_string[:-padding] if padding else binary_string

        current_code = ''
        decoded_data = bytearray()
        for bit in binary_string:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded_data.append(self.reverse_codes[current_code])
                current_code = ''

        with open(output_file, 'wb') as f:
            f.write(decoded_data)

        print(f"✅ Decompression complete: '{input_file}' → '{output_file}'")

def main():
    parser = argparse.ArgumentParser(description="📦 File Zipper using Huffman Coding")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Compress command
    compress_parser = subparsers.add_parser('compress', help='Compress a file')
    compress_parser.add_argument('input', help='Input file path')
    compress_parser.add_argument('output', help='Output compressed file path')

    # Decompress command
    decompress_parser = subparsers.add_parser('decompress', help='Decompress a file')
    decompress_parser.add_argument('input', help='Input compressed file path')
    decompress_parser.add_argument('output', help='Output decompressed file path')

    args = parser.parse_args()
    zipper = HuffmanZipper()

    if args.command == 'compress':
        if os.path.exists(args.input):
            zipper.compress(args.input, args.output)
        else:
            print("❌ Error: Input file does not exist!")

    elif args.command == 'decompress':
        if os.path.exists(args.input):
            zipper.decompress(args.input, args.output)
        else:
            print("❌ Error: Compressed file does not exist!")

if __name__ == "__main__":
    main()
