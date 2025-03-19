import datetime
import os
import subprocess
from PIL import Image

# Configuration
IMAGE_PATH = "pacman.png"  # Input image file
TARGET_YEAR = 2024  # Year for the contribution graph
REPO_DIR = "2024-contribution-graph"  # Git repository directory
INVERTED_COLORS = False  # If True, inverts the contribution intensity


def get_full_week_dates(year):
    """Returns a list of all dates in full weeks (Sunday to Saturday) for the given year."""
    # Find the first Sunday of the year
    start_date = datetime.date(year, 1, 1)
    while start_date.weekday() != 6:
        start_date += datetime.timedelta(days=1)

    # Optimize for 50 columns (shift to second Sunday if necessary)
    if start_date.day == 1:
        start_date = datetime.date(year, 1, 8)

    # Find the last Saturday of the year
    end_date = datetime.date(year, 12, 31)
    while end_date.weekday() != 5:
        end_date -= datetime.timedelta(days=1)

    # Generate and return the list of dates
    return [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]


def load_image(image_path):
    """Loads and validates the input image."""
    image = Image.open(image_path)
    width, height = image.size
    assert image.mode == "RGB", "Error: Image must be in RGB mode."
    assert width == 50 and height == 7, "Error: Image must be 50x7 pixels."
    return image


def parse_image_to_values(image, dates, inverted_colors):
    """Parses image pixels to determine commit intensity for each date."""
    width, height = image.size
    pixels = image.load()
    values = []

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            brightness = min(4, int((0.2 * r + 0.7 * g + 0.1 * b) / 255 * 5))
            if inverted_colors:
                brightness = 4 - brightness
            values.append((dates[y + x * height], brightness))

    return values


def setup_git_repo(repo_dir):
    """Creates and initializes a new Git repository."""
    assert not os.path.exists(repo_dir), "Error: Repository folder already exists."
    os.mkdir(repo_dir)
    os.chdir(repo_dir)
    subprocess.run(["git", "init"], check=True)
    with open("dummy.txt", "w") as file:
        file.write("Initial commit.\n")


def create_commits(values):
    """Creates git commits based on parsed image values."""
    for date, commit_count in values:
        commit_datetime = f"{date}T12:00:00"
        for i in range(commit_count):
            with open("file.txt", "a") as file:
                file.write(f"Commit number {i+1} on {commit_datetime}\n")
            subprocess.run(["git", "add", "file.txt"], check=True)
            subprocess.run([
                "git", "commit", "-m", f"Commit {i+1} on {commit_datetime}", "--date", commit_datetime
            ], check=True)


def display_preview(values, width, height):
    """Displays a simple terminal preview of the contribution graph."""
    shades_of_green = [
        "\033[38;5;232m",  # Black (no commits)
        "\033[38;5;22m",   # Dark green
        "\033[38;5;28m",   # Medium green
        "\033[38;5;34m",   # Bright green
        "\033[38;5;46m",   # Intense green
    ]

    for y in range(height):
        for x in range(width):
            _, color_idx = values[y + x * height]
            print(f"{shades_of_green[color_idx]}{chr(9608)}\033[0m", end=" ")
        print()


if __name__ == "__main__":
    dates = get_full_week_dates(TARGET_YEAR)
    image = load_image(IMAGE_PATH)
    values = parse_image_to_values(image, dates, INVERTED_COLORS)
    setup_git_repo(REPO_DIR)
    create_commits(values)
    display_preview(values, image.width, image.height)
