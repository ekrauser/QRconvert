import datetime
import win32print

# Get the list of all printers
printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)

# Find the first printer with "ZQ630" in its name
printer_name = None
for _, _, name, _ in printers:
    if "ZQ630" in name:
        printer_name = name
        break

if printer_name is None:
    raise Exception("Could not find a printer with 'ZQ630' in its name")

# Define the CPCL template with placeholders for date and time
cpcl_template = '''! U1 setvar "power.inactivity_timeout" "14400"
! U1 setvar "netmanage.type" "none"
! U1 setvar "weblink.enable" "off"
! U1 setvar "weblink.ip.conn1.location" "https://awc-p2.us-east-1.prod.mdm.fc.a2z.com/zebra/weblink/""
! U1 setvar "weblink.enable" "on"
! U1 setvar "weblink.ip.conn1.enable" "on"
! U1 setvar "weblink.zebra_connector.enable" "off"
! U1 setvar "bluetooth.enable" "on"
! U1 setvar "bluetooth.discoverable" "on"
! U1 setvar "bluetooth.minimum_security_mode" "4"
! U1 setvar "bluetooth.bonding" "on"
! U1 setvar "bluetooth.enable_reconnect" "iOS_only"
! U1 setvar "bluetooth.allow_non_display_numeric_comparison" "print"
! U1 setvar "bluetooth.le.controller_mode" "classic"
! U1 setvar "rtc.date" "{date}"
! U1 setvar "rtc.time" "{time}"
! U1 setvar "device.location" "UIL2"
! U1 do "device.reset" ""'''

# Get the current date and time
now = datetime.datetime.now()
date_str = now.strftime('%m-%d-%Y')
time_str = now.strftime('%H:%M:%S')

# Replace the placeholders in the CPCL template with the current date and time
cpcl_data = cpcl_template.format(date=date_str, time=time_str)

# Send the CPCL data to the printer
hPrinter = win32print.OpenPrinter(printer_name)
try:
    win32print.StartDocPrinter(hPrinter, 1, ("CPCL Document", None, "RAW"))
    win32print.WritePrinter(hPrinter, cpcl_data.encode())
finally:
    win32print.EndDocPrinter(hPrinter)
    win32print.ClosePrinter(hPrinter)
