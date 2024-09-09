from bs4 import BeautifulSoup
import numpy as np
import os
import requests


# print("\033c") # Another way to hide file paths


# 1) Extract values from the URL using BeautifulSoup
def grab_characters(url: str) -> list:
    response = requests.get(url)
    html_data = response.content  # Request access to URL

    soup = BeautifulSoup(html_data, "html.parser")
    table = soup.find('table')
    td_tags = table.find_all('td')  # Get desired tags from URL

    values = [item.get_text() for item in td_tags]

    return values  # Extracted values from URL, not yet processed


# 2) Process x-coordinates, characters, and y-coordinates into a numpy array
def fix_characters(values: list) -> np.ndarray:
    tuple_values = list(zip(values[0::3][1:], values[1::3][1:], values[2::3][1:]))  # Create list of tuples, removing the first tuple
    numpy_grid = np.array(tuple_values, dtype=object)  # Convert tuples to a numpy array

    numpy_grid[:, 0] = np.array(numpy_grid[:, 0], dtype=int)  # Convert x-coordinates to integers
    numpy_grid[:, 2] = np.array(numpy_grid[:, 2], dtype=int)  # Convert y-coordinates to integers

    return numpy_grid


# 3) Convert the numpy values into a grid of characters based on x- and y-coordinates
def create_grid(numpy_grid: np.ndarray) -> None:
    max_x = np.max(numpy_grid[:, 0]) + 1  # Width of the grid
    max_y = np.max(numpy_grid[:, 2]) + 1  # Height of the grid

    # Create an empty grid filled with spaces
    grid = [[' ' for _ in range(max_x)] for _ in range(max_y)]

    # # Populate the grid with characters
    for x, char, y in numpy_grid:
        grid[max_y - 1 - y][x] = char  # Flip the y-coordinate (x-coordinate increases to the right, y-coordinate increases downwards)

    # Print the grid
    for row in grid:
        print(''.join(row))


# Main function to run the program
def main(url) -> None:
    values = grab_characters(url)         # Step 1: Get URL values
    numpy_grid = fix_characters(values)   # Step 2: Process values for use
    create_grid(numpy_grid)               # Step 3: Create and print grid of characters

# urls = ["https://docs.google.com/document/d/e//O3YoUB1ecq/pub", "https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub"]
# for url in urls:
#     main(url)

# sample_1 = "https://docs.google.com/document/d/e//O3YoUB1ecq/pub" # (Coding assessment input data example)
coding_assessment = "https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub" # Coding assessment input data
main(coding_assessment)