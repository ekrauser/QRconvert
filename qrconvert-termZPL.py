import pyqrcode
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

def convert_mac_format(mac):
    return mac.replace("-", ":").upper()

# Directory to save the generated QR codes
output_directory = "qr_codes/"

# Define the dimensions of the image and QR code
image_width = 300
image_height = 350
qr_size = 200
text_font_size = 24

# ZPL command to start the print format
zpl_start = "^XA"

# ZPL command to set the label home position
zpl_home = "^LH0,0"

# ZPL command to define the QR code field
zpl_qr_code = "^FO50,50^BQN,2,10^FDMA,MAC_ADDRESS^FS"

# ZPL command to define the text field
zpl_text = "^FO50,275^A0N,28,28^FDMA,MAC_ADDRESS^FS"

# ZPL command to end the print format
zpl_end = "^XZ"

while True:
    # Read MAC addresses from the terminal
    mac_addresses = input("Enter MAC addresses (separated by commas), or 'q' to quit: ")

    if mac_addresses.lower() == 'q':
        break

    mac_addresses = mac_addresses.split(",")

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

        # Generate the ZPL file contents
        zpl_contents = zpl_start + zpl_home
        zpl_contents += zpl_qr_code.replace("MAC_ADDRESS", mac_address) + "\n"
        zpl_contents += zpl_text.replace("MAC_ADDRESS", mac_address) + "\n"
        zpl_contents += zpl_end

        # Save the ZPL file
        zpl_filename = f"qr_with_mac_{mac_address}.zpl"
        zpl_path = output_directory + zpl_filename
        with open(zpl_path, "w") as zpl_file:
            zpl_file.write(zpl_contents)

        # Print the ZPL file to the Zebra printer
        print_command = f"lp -d YOUR_PRINTER_NAME {zpl_path}"
        subprocess.run(print_command, shell=True)

print("QR codes with converted MAC addresses created and printed.")
