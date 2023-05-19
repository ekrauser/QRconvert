import csv
import pyqrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

def convert_mac_format(mac):
    return ":".join(mac[i:i+2] for i in range(0, 12, 2)).upper()

# Directory to save the generated QR codes
output_directory = "qr_codes/"

# Define the dimensions of the image and QR code
image_width = 525  # Adjust to your label width
image_height = 375  # Adjust to your label height
qr_size = min(image_width, image_height) - 50
text_font_size = 24

# CSV file to store the name, MAC address, and serial number
csv_file = "mac_addresses.csv"

# Check if the CSV file exists, create it if not
if not os.path.exists(csv_file):
    with open(csv_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "MAC Address", "Serial Number"])

while True:
    # Read name and MAC addresses from the terminal
    name = input("Enter Name (or 'q' to quit): ")
    if name.lower() == 'q':
        break

    serial_number = input("Enter Serial Number: ")

    mac_addresses = input("Enter MAC addresses (separated by commas): ").split(",")

    # Iterate through each MAC address
    for mac_address in mac_addresses:
        mac_address = mac_address.strip()

        converted_mac = convert_mac_format(mac_address)

        # Generate QR code
        qr = pyqrcode.create(converted_mac)

        # Save QR code image
        qr_filename = f"qr_{mac_address}.png"
        qr_path = output_directory + qr_filename
        qr.png(qr_path, scale=10)

        # Create an image with the QR code and converted MAC address
        img = Image.new("RGB", (image_width, image_height), "white")

        qr_img = Image.open(qr_path)
        qr_img = qr_img.resize((qr_size, qr_size))
        qr_position = ((image_width - qr_size) // 2, 5)  
        img.paste(qr_img, qr_position)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", text_font_size)
        text = converted_mac
        text_width, text_height = draw.textsize(text, font=font)
        text_position = ((image_width - text_width) // 2, qr_position[1] + qr_size + 5)
        draw.text(text_position, text, font=font, fill="black")

        # Save the final image with the QR code and original MAC address as the file name
        final_filename = f"qr_with_mac_{mac_address}.png"
        final_path = output_directory + final_filename
        img.save(final_path)

        # Append name, converted MAC address, and serial number to the CSV file
        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name.strip(), converted_mac.strip(), serial_number.strip()])

print("QR codes with converted MAC addresses created and saved to CSV.")

