import os
from PIL import Image
import tkinter as tk

def get_grayscale_map(chars):
    """
    Creates a grayscale map using a provided character list.

    Args:
        chars (str): A string containing characters for different brightness levels.

    Returns:
        list: A list where each index represents a brightness level and
              the corresponding character.
    """
    brightness_range = 256
    grayscale_map = [chars[i * len(chars) // brightness_range] for i in range(brightness_range)]
    return grayscale_map

def get_ascii_art(image_path, char_map, window_width=None, window_height=None):
    """
    Converts an image to ASCII art and resizes it to fit a window (optional).

    Args:
        image_path (str): Path to the image file.
        char_map (list): A grayscale map (list of characters).
        window_width (int, optional): Desired width of the ASCII art in characters. Defaults to None.
        window_height (int, optional): Desired height of the ASCII art in characters. Defaults to None.

    Returns:
        str: The ASCII art representation of the image.
    """

    try:
        image = Image.open(image_path).convert('L')  # Convert to grayscale
        image_width, image_height = image.size

        # Use a denser character set for better detail
        denser_chars = "#@%8&WM#*\\/|()1[]?-_+~<>i!lI;:,^. "
        denser_char_map = get_grayscale_map(denser_chars)

        # Rescale image to fit a larger window (adjust dimensions as needed)
        if not window_width or not window_height:
            window_width = 160  # Adjust width for a larger output
            window_height = 80  # Adjust height for a larger output

        aspect_ratio = image_width / image_height
        char_aspect_ratio = 0.55  # Average aspect ratio for ASCII characters

        new_width = min(window_width, image_width)
        new_height = int(new_width / aspect_ratio / char_aspect_ratio)
        if new_height > window_height:
            new_height = window_height
            new_width = int(new_height * aspect_ratio * char_aspect_ratio)

        image = image.resize((new_width, new_height), Image.LANCZOS)

        ascii_grid = []
        for y in range(image.height):
            ascii_row = ''
            for x in range(image.width):
                pixel = image.getpixel((x, y))
                ascii_row += denser_char_map[pixel]
            ascii_grid.append(ascii_row)

        return '\n'.join(ascii_grid)

    except FileNotFoundError as e:
        print(f"Error: Image file not found. Please check the path: {image_path}")
        return None

def draw_ascii_art_to_window(ascii_art, window_title="ASCII Art"):
    """
    Displays the ASCII art in a tkinter window.

    Args:
        ascii_art (str): The ASCII art representation of the image.
        window_title (str, optional): Title for the window. Defaults to "ASCII Art".
    """

    if not ascii_art:  # Check if ascii_art is None (error case)
        return  # Exit the function if no art to display

    window = tk.Tk()
    window.title(window_title)

    # Create a text widget with a smaller font for better visibility
    text_widget = tk.Text(window, wrap=tk.WORD, font=("Courier New", 5))
    text_widget.insert(tk.END, ascii_art)

    # Make the text widget read-only
    text_widget.config(state="disabled")

    # Adjust the window size to accommodate the larger output
    window.geometry("1920x1024")  # Adjust window size as needed

    text_widget.pack(fill=tk.BOTH, expand=True)

    window.mainloop()  # Start the event loop to keep the window open

chars = "#@%8&WM#*\\/|()1[]?-_+~<>i!lI;:,^. "
char_map = get_grayscale_map(chars)

image_path = "C:/Users/91786/Pictures/Camera Roll/IMG_20230411_081236_433.jpg"

ascii_art = get_ascii_art(image_path, char_map, window_width=160, window_height=320)

draw_ascii_art_to_window(ascii_art)
