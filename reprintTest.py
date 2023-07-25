#created by ekrauser@ for UIL2 and whoever else can get some use out of it

import csv
import pyqrcode
import win32print
import win32ui
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageWin
import os

def convert_mac_format(mac):
    return ":".join(mac[i:i+2] for i in range(0, 12, 2)).upper()

def create_and_print_qr(label_text, output_directory, image_width, image_height, qr_size, text_font_size):
    # Generate QR code
    qr = pyqrcode.create(label_text)

    # Create a safe filename by replacing colons with underscores
    safe_label_text = label_text.replace(":", "_")

    # Save QR code image
    qr_filename = f"qr_{safe_label_text}.png"
    qr_path = output_directory + qr_filename
    qr.png(qr_path, scale=10)

    # Create an image with the QR code and label text
    img = Image.new("RGB", (image_width, image_height), "white")

    qr_img = Image.open(qr_path)
    qr_img = qr_img.resize((qr_size, qr_size))
    qr_position = ((image_width - qr_size) // 2, 5)
    img.paste(qr_img, qr_position)

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", text_font_size)
    text = label_text
    text_width, text_height = draw.textsize(text, font=font)
    text_position = ((image_width - text_width) // 2, qr_position[1] + qr_size + 5)
    draw.text(text_position, text, font=font, fill="black")

    # Save the final image with the QR code and label text as the file name
    final_filename = f"qr_with_text_{safe_label_text}.png"
    final_path = output_directory + final_filename
    img.save(final_path)

    # Print image using Windows DEFAULT printer
    print_image(img)


def print_image(img):
    HORZRES = 8
    VERTRES = 10

    printer_name = win32print.GetDefaultPrinter()

    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)

    printer_name = win32print.GetPrinter(win32print.OpenPrinter(printer_name), 2)["pPrinterName"]
    job = win32print.StartDoc(hdc.GetHandleOutput(), (printer_name, None, "RAW", 0))

    win32print.StartPage(hdc.GetHandleOutput())

    ratios = [1.0 * img.size[i] / hdc.GetDeviceCaps(j) for i, j in enumerate((HORZRES, VERTRES))]
    ratio = min(ratios)

    img = img.resize([int(ratio * i) for i in img.size], Image.ANTIALIAS)

    dib = ImageWin.Dib(img)

    r = [0, 0, hdc.GetDeviceCaps(HORZRES), hdc.GetDeviceCaps(VERTRES)]
    dib.draw(hdc.GetHandleOutput(), r)

    win32print.EndPage(hdc.GetHandleOutput())
    win32print.EndDoc(hdc.GetHandleOutput())

    hdc.DeleteDC()

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
    name = input("Scan Printer Name - This is the existing QR code (or 'q' to quit): ")
    if name.lower() == 'q':
        break

    serial_number = input("Scan Printer Serial Number: ")

    mac_addresses = input("Scan Bluetooth MAC addresses: ").split(",")

    # Iterate through each MAC address
    for mac_address in mac_addresses:
        mac_address = mac_address.strip()

        converted_mac = convert_mac_format(mac_address)

        # Create and print QR code for MAC
        create_and_print_qr(converted_mac, output_directory, image_width, image_height, qr_size, text_font_size)

        # Create and print QR code for name
        create_and_print_qr(name.strip(), output_directory, image_width, image_height, qr_size, text_font_size)
        
        # Append name, converted MAC address, and serial number to the CSV file
        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name.strip(), converted_mac.strip(), serial_number.strip()])

print("QR codes with converted MAC addresses created and data saved to CSV.")



# Check if the directory exists, create it if not
if not os.path.exists(output_directory):
    os.mkdir(output_directory)