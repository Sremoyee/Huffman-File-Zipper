# File Zipper using Huffman Coding

A simple file compression and decompression tool using Huffman coding algorithm.

## Features
- Compress any file using Huffman coding
- Decompress previously compressed files
- Command-line interface
- No external dependencies required

## Usage
1. Run the script:
```bash
python zipper.py
```

2. Choose from the following options:
   - 1: Compress a file
   - 2: Decompress a file
   - 3: Exit

3. When compressing or decompressing, you'll need to provide:
   - Input file path
   - Output file path

## How it works
The program uses Huffman coding to create optimal variable-length codes for file compression:
1. Builds a frequency dictionary of bytes in the input file
2. Creates a Huffman tree based on these frequencies
3. Generates binary codes for each byte
4. Compresses/decompresses the file using these codes

## Note
The compression ratio depends on the input file's content. Files with more repeated patterns will achieve better compression.


![alt text](image.png)