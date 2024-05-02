import os
import time
from LZW.compress import LZWCompressor
from LZW.decompress import LZWDecompressor
from HuffmanCoding.huffman_coding import HuffmanCompress
from prettytable import PrettyTable


TEXT_FILE_FOLDER = "src/textfiles"
BINARY_FILE_FOLDER = "src/BinFiles"
DECOMPRESSED_FILE_FOLDER = "src/decompressedFiles"
CLEAN_FOLDERS = ["src/BinFiles", "src/decompressedFiles"]
# OUTPUT_FILE_HUFFMAN = "src/BinFiles/compressed_W_Huff_example.bin"
# OUTPUT_FILE_LZW = "src/BinFiles/compressed_W_LZW_example.bin"
# DECOMPRESSED_FILE_HUFFMAN = "src/decompressed_W_Huff.txt"
# DECOMPRESSED_FILE_LZW = "src/decompressed_W_LZW.txt"




def compress_with_lzw(input_file, output_file):
    compressor = LZWCompressor()
    compressor.compress(input_file, output_file)

def decompress_with_lzw(input_file, output_file):
    decompressor = LZWDecompressor()
    decompressor.decompress(input_file, output_file)

h = HuffmanCompress()


def is_txt_file(file_path):
    return file_path.lower().endswith(".txt")


def get_file_size(file_path):
    return os.path.getsize(file_path)


def list_files(folder, file_type):
    files = [file for file in os.listdir(folder) if file.endswith(file_type)]
    return files

def display_file_lists():
    text_files = list_files(TEXT_FILE_FOLDER, ".txt")
    binary_files = list_files(BINARY_FILE_FOLDER, ".bin")

    if not text_files and not binary_files:
        print("No files found in the folders.")
    else:
        max_files = max(len(text_files), len(binary_files))

        table = PrettyTable()
        table.field_names = ["Available Text Files", "Available Binary Files"]

        for i in range(max_files):
            text_file = text_files[i] if i < len(text_files) else ""
            binary_file = binary_files[i] if i < len(binary_files) else ""
            table.add_row([text_file, binary_file])
        print(table)



def display_compression_stats(algorithm, original_size, compressed_size, compression_time):
    table = PrettyTable()
    table.field_names = ["Algorithm", "Original Size", "Compressed Size", "Compression Ratio", "Compression Time"]
    table.add_row([algorithm, original_size, compressed_size, ((original_size - compressed_size) / original_size) * 100, compression_time])
    print()
    print("Compression Statistics:")
    print(table)


def display_decompression_stats(algorithm, decompression_time):
    table = PrettyTable()
    table.field_names = ["Algorithm", "deompression Time"]
    table.add_row([algorithm, decompression_time])
    print("Decompression Statistics:")
    print(table)


def compare_compression(filename):
    input_file = os.path.join(TEXT_FILE_FOLDER, filename)
    huffman_output_file = os.path.join(BINARY_FILE_FOLDER, f"{os.path.splitext(filename)[0]}_compressed_with_Huffman.bin")
    lzw_output_file = os.path.join(BINARY_FILE_FOLDER, f"{os.path.splitext(filename)[0]}_compressed_with_LZW.bin")

    # Compress with Huffman
    huffman_start_time = time.time()
    h.compress(input_file, huffman_output_file)
    huffman_end_time = time.time()
    huffman_compressed_size = get_file_size(huffman_output_file)

    # Compress with LZW
    LZW_start_time = time.time()
    compress_with_lzw(input_file, lzw_output_file)
    lzw_end_time = time.time()
    lzw_compressed_size = get_file_size(lzw_output_file)

    # Display compression statistics in a pretty table
    table = PrettyTable()
    table.field_names = ["Algorithm", "Original Size", "Compressed Size", "Compression Ratio", "Compression Time"]
    table.add_row(["Huffman", get_file_size(input_file), huffman_compressed_size, ((get_file_size(input_file) - huffman_compressed_size) / get_file_size(input_file)) * 100, huffman_end_time - huffman_start_time])
    table.add_row(["LZW", get_file_size(input_file), lzw_compressed_size, ((get_file_size(input_file) - lzw_compressed_size) / get_file_size(input_file)) * 100, lzw_end_time - LZW_start_time])
    print("Comparison of Compression Algorithms:")
    print(table)

def delete_files_in_folder(folder):
    files = os.listdir(folder)
    for file in files:
        file_path = os.path.join(folder, file)
        os.remove(file_path)


def clean_up():
    for folder in CLEAN_FOLDERS:
        delete_files_in_folder(folder)
    

def main():
    while True:
        display_file_lists()
        print("1. Compress with Huffman")
        print("2. Decompress with Huffman")
        print("3. Compress with LZW")
        print("4. Decompress with LZW")
        print("5. Compare algorithms")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            filename = input("Enter the name of the text file to compress with Huffman: ")
            input_file = os.path.join(TEXT_FILE_FOLDER, filename)
            if not os.path.isfile(input_file):
                print("Invalid filename. Please check the filename and try again.")
                continue
            output_file = os.path.join(BINARY_FILE_FOLDER, f"{os.path.splitext(filename)[0]}_Huff.bin")
            start_time = time.time()
            h.compress(input_file, output_file)
            end_time = time.time()
            compressed_size = get_file_size(output_file)
            original_size = get_file_size(input_file)
            display_compression_stats("Huffman", original_size, compressed_size, end_time - start_time)

            # compression_ratio = ((original_size - compressed_size) / original_size) * 100

            # print(f"File compressed with Huffman.\nCompression ratio: {compression_ratio}\nCompression time: {end_time - start_time} seconds")

        elif choice == "2":
            filename = input("Enter the name of the compressed file to decompress with Huffman: ")
            check = is_txt_file(filename)
            if check == True:
                print("File must be compressed first")
            else:
                input_file = os.path.join(BINARY_FILE_FOLDER, filename)
                if not os.path.isfile(input_file):
                    print("Invalid filename. Please check the filename and try again.")
                    continue
                output_file = os.path.join(DECOMPRESSED_FILE_FOLDER, f"{os.path.splitext(filename)[0]}.txt")
                start_time = time.time()
                h.decompress(input_file, output_file)
                end_time = time.time()
                display_decompression_stats("Huffman", end_time - start_time)


        elif choice == "3":
            filename = input("Enter the name of the text file to compress with LZW: ")
            input_file = os.path.join(TEXT_FILE_FOLDER, filename)
            if not os.path.isfile(input_file):
                print("Invalid filename. Please check the filename and try again.")
                continue
            output_file = os.path.join(BINARY_FILE_FOLDER, f"{os.path.splitext(filename)[0]}_LZW.bin")
            start_time = time.time()
            compress_with_lzw(input_file, output_file)
            end_time = time.time()
            compressed_size = get_file_size(output_file)
            original_size = get_file_size(input_file)
            display_compression_stats("LZW", original_size, compressed_size, end_time - start_time)
            # compression_ratio = ((original_size - compressed_size) / original_size) * 100

            # print(f"File compressed with LZW.\nCompression ratio: {compression_ratio}\nCompression time: {end_time - start_time} seconds")

        elif choice == "4":
            filename = input("Enter the name of the compressed file to decompress with LZW: ")
            check = is_txt_file(filename)
            if check == True:
                print("File must be compressed first")
            input_file = os.path.join(BINARY_FILE_FOLDER, filename)
            if not os.path.isfile(input_file):
                print("Invalid filename. Please check the filename and try again.")
                continue
            output_file = os.path.join(DECOMPRESSED_FILE_FOLDER, f"compressed_{os.path.splitext(filename)[0]}.txt")
            start_time = time.time()
            decompress_with_lzw(input_file, output_file)
            end_time = time.time()

            display_decompression_stats("LZW", end_time - start_time)

        elif choice == "5":
            # Compare compression algorithms
            filename = input("Enter the name of the text file to compare compression algorithms: ")
            if not os.path.isfile(filename):
                print("Invalid filename. Please check the filename and try again.")
                continue
            compare_compression(filename)


        elif choice == "6":
            clean_up()
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
