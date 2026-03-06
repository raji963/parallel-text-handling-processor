# text_loader.py

def read_text(file_path):
    """
    Reads text file and returns full text.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def chunk_text(text, chunk_size=50):
    """
    Break text into word chunks.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks