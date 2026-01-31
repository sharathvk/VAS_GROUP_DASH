import re

def validate_vehicle_number(vehicle_number):
    # Remove spaces and convert to uppercase
    vehicle_number = vehicle_number.replace(" ", "").upper()

    # Regular expressions for both formats
    state_format = r'^[A-Z]{2}\d{2}[A-Z]{1,2}\d{1,4}$'  # Standard state format (e.g., MH12AB1234)
    bharat_format = r'^[A-Z]{2}BH\d{4}[A-Z]{2}$'  # Bharat Series format (e.g., MH BH 1234 AB)
    state_old_format1 = r'^[A-Z]{2}\d{2}[A-Z]{1}\d{4}$' # Old State Format1 (e.g., KA36T3436)
    state_old_format2 = r'^[A-Z]{2}\d{6}$'  # Old State Format2 (e.g., KA363436)

    # Check if the input is exactly 10 or 9  characters and matches one of the formats
    if len(vehicle_number) not in [10, 9, 8]:
        return False
        # return "Invalid vehicle number. It must be exactly 10 characters."

    if re.match(state_format, vehicle_number) or re.match(bharat_format, vehicle_number) \
            or re.match(state_old_format1, vehicle_number) or re.match(state_old_format2, vehicle_number):
        return True
    else:
        return False

def validate_mobile_number(mobile_number):
    # Remove spaces, dashes, and convert to standard format
    mobile_number = re.sub(r"[^\d]", "", mobile_number)

    # Remove country code if present
    if mobile_number.startswith("91") and len(mobile_number) == 12:
        mobile_number = mobile_number[2:]
    elif mobile_number.startswith("0") and len(mobile_number) == 11:
        mobile_number = mobile_number[1:]

    # Check if it's a valid 10-digit mobile number starting with 6-9
    if re.fullmatch(r"[6-9]\d{9}", mobile_number):
        return True
    else:
        return False