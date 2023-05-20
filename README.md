# QRconvert
converts bluetooth mac address to proper XX:YY format, creates a qrcode, sends it to a label printer

qrconvert-final.py - the finished product (for now)
  1. asks for printer name (you can scan the existing qr code on the printer)
  2. asks for printer serial number (you can scan the barcode on the bottom of the printer)
  3. asks for printer bt mac address (you can scan the other barcode on the bottom of the printer)
  4. it will then convert the bt mac from aabbccddeeff format to AA:BB:CC:DD:EE:FF format, and add the reformated mac address, name, and serial number to a csv file
  5. then it creates a qr code from the reformatted mac address, and uses that to create the final png with the qr code and the reformatted mac address in text under it
  6. finally, it prints directly to your default printer in windows, make this a zd620 (or similar) label printer, configured with the labels of your choice 

NOW AVAILABLE AS AN EXCITING NEW AND SOTRA PORTABLE EXE 
