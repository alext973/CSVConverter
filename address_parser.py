import re

def extract_street_and_number(street, street2):
    match = re.search(r"^(\D*?)(\d.*)?$", street.strip())
    if match:
        street_name = match.group(1).strip()
        house_number = match.group(2).strip() if match.group(2) else ""
        
        if street2 and re.fullmatch(r"\d+.*", street2.strip()):
            house_number = street2.strip()
        
        return street_name, house_number
    return street, street2 if street2 and re.fullmatch(r"\d+.*", street2.strip()) else ""