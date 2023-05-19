import pyqrcode
from PIL import Image, ImageDraw, ImageFont

def convert_mac_format(mac):
    return mac.replace("-", ":").upper()

# Directory to save the generated QR codes
output_directory = "qr_codes/"

# Define the dimensions of the image and QR code
image_width = 300
image_height = 350
qr_size = 200
text_font_size = 24

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

print("QR codes with converted MAC addresses created.")
