import csv
import pyqrcode
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import zebra

def convert_mac_format(mac):
    return ":".join(mac[i:i+2] for i in range(0, 12, 2)).upper()

def convert_image_to_zpl(image_path):
    img = Image.open(image_path).convert('1')
    width, height = img.size
    data = list(img.getdata())
    hex_data = ''.join(['{:02X}'.format(data[i]//255) for i in range(0, len(data))])
    zpl = '^GFA,{0},{1},{2},{3}'.format(len(hex_data), len(hex_data)//2, width//8, hex_data)
    return zpl

# Directory to save the generated QR codes
output_directory = "qr_codes/"

# Define the dimensions of the image and QR code
image_width = 300
image_height = 350
qr_size = 200
text_font_size = 24

# CSV file to store the name, MAC address, and serial number
csv_file = "mac_addresses.csv"

# Check if the CSV file exists, create it if not
if not os.path.exists(csv_file):
    with open(csv_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "MAC Address", "Serial Number"])  # Added "Serial Number"

# Ask the user for the printer name
printer_name = input("Enter the name of your printer: ")

# Initialize the selected printer
printer = zebra.Usb(0xPID, 0xVID, 0, 0, 0) #replace PID and VID with your printer's PID and VID, that's probably why you're seeing this error

while True:
    # Read name and MAC addresses from the terminal
    name = input("Enter Name (or 'q' to quit): ")
    if name.lower() == 'q':
        break

    serial_number = input("Enter Serial Number: ")  # Get the serial number

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
        qr_position = ((image_width - qr_size) // 2, 50)
        img.paste(qr_img, qr_position)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", text_font_size)
        text = converted_mac
        text_width, text_height = draw.textsize(text, font=font)
        text_position = ((image_width - text_width) // 2, qr_position[1] + qr_size + 10)
        draw.text(text_position, text, font=font, fill="black")

        # Save the final image with the QR code and original MAC address as the file name
        final_filename = f"qr_with_mac_{mac_address}.png"
        final_path = output_directory + final_filename
        img.save(final_path)

        # Convert the final image to ZPL
        zpl_data = convert_image_to_zpl(final_path)

        # ZPL command to start the print format
        zpl_start = "^XA"

        # ZPL command to set the label home position
        zpl_home = "^LH0,0"

        # ZPL command to end the print format
        zpl_end = "^XZ"

        # Generate the ZPL file contents
        zpl_contents = zpl_start + zpl_home + zpl_data + zpl_end

        # Print the ZPL command to the Zebra printer
        printer.output(zpl_contents)

        # Append name, converted MAC address, and serial number to the CSV file
        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name.strip(), converted_mac.strip(), serial_number.strip()])  # Added serial_number

print("QR codes with converted MAC addresses created, printed, and saved to CSV.")
