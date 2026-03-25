import os


def load_reviews(file_path, limit=None):
    """
    Load reviews from a text file.

    Parameters:
        file_path (str): Path to the input file.
        limit (int, optional): Maximum number of reviews to load.

    Returns:
        list: List of cleaned review strings.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    reviews = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            cleaned = line.strip()
            if cleaned:  # ignore empty lines
                reviews.append(cleaned)

                if limit and len(reviews) >= limit:
                    break

    return reviews