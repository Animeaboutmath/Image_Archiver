import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image
import requests
from io import BytesIO
import csv
import os

"""
Image Archiver Tool!
Requires pillow and requests libraries
run script within folder with CSV 
"""


def download_and_compress_single(url, quality):
    try:
        # Download the image and convert to RGB
        response = requests.get(url)
        response.raise_for_status()
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        # Converts to RGB to play nice with JPEG
        rgb_img = img.convert('RGB')

        # Compress the image
        filename = os.path.basename(url).split('?')[0]  # Extract filename from URL
        compressed_path = f"Processed_{filename}.jpg"
        
        # Saves picture locally with selected quality
        rgb_img.save(compressed_path, "JPEG", quality=quality)  # Use selected quality

        return f"Image compressed and saved as {compressed_path}"
    except Exception as e:
        return f"Error processing {url}: {e}"

# Download and fetches associated picture
def download_and_compress():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    # Clear the error output field
    error_output.delete(1.0, tk.END)

    # Determine quality based on user selection of radio button
    quality = 96 if quality_var.get() == "high" else 17

    result = download_and_compress_single(url, quality)
    error_output.insert(tk.END, result + "\n")
    if "Error" in result:
        messagebox.showerror("Error", result)
    else:
        messagebox.showinfo("Success", result)

# Accepts input of CSV file
def process_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    # Clear the error output field
    error_output.delete(1.0, tk.END)

    # Determine quality based on user selection
    quality = 95 if quality_var.get() == "high" else 22

    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Ensure the row is not empty
                    url = row[0]
                    result = download_and_compress_single(url, quality)
                    error_output.insert(tk.END, result + "\n")
        messagebox.showinfo("Success", "CSV processing completed.")
    except Exception as e:
        error_output.insert(tk.END, f"Error processing CSV: {e}\n")
        messagebox.showerror("Error", f"Failed to process the CSV file: {e}")

# Create the main window
root = tk.Tk()
root.title("Image Archive-o-matic")

# URL input
url_label = tk.Label(root, text="Image URL:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Quality selection
quality_var = tk.StringVar(value="low")  # Default to low quality
quality_label = tk.Label(root, text="Select Image Quality:")
quality_label.pack(pady=5)

low_quality_button = tk.Radiobutton(root, text="Low Quality", variable=quality_var, value="low")
low_quality_button.pack()

high_quality_button = tk.Radiobutton(root, text="High Quality", variable=quality_var, value="high")
high_quality_button.pack()

# Compress single photo button
compress_button = tk.Button(root, text="Compress Image", command=download_and_compress)
compress_button.pack(pady=10)

# Process CSV button
csv_button = tk.Button(root, text="Or Upload CSV of URLs", command=process_csv)
csv_button.pack(pady=10)

# Error output field
error_output_label = tk.Label(root, text="Output Log:")
error_output_label.pack(pady=5)

error_output = tk.Text(root, height=10, width=60, state=tk.NORMAL)
error_output.pack(pady=5)

# Run the application
root.mainloop()
