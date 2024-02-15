import requests
import os
from xml.etree import ElementTree as ET
import pandas as pd
import json

def downloadFile(filetype: str = 'GenOutputCapability') -> None:    
    if filetype == 'GenOutputCapability':
        url = 'http://reports.ieso.ca/public/GenOutputCapability/PUB_GenOutputCapability.xml'
        file_path = 'PUB_GenOutputCapability.xml'

    if os.path.exists(file_path):
        os.remove(file_path)

    response = requests.get(url)

    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        #TODO: Change to logger
        print("File downloaded and saved successfully.")
    else:
        #TODO: Change to logger
        print(f"Failed to download the file. HTTP status code: {response.status_code}")

def parseGenOutputCapability(sites: list) -> list:
    # Load and parse the XML file
    file_path = 'PUB_GenOutputCapability.xml'
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define the namespace to access the elements correctly
    ns = {'imo': 'http://www.theIMO.com/schema'}

    # Initialize a list to store the data
    data = []

    for site in sites:
        for generator in root.findall('.//imo:Generator', ns):
            generator_name = generator.find('.//imo:GeneratorName', ns).text
            if generator_name == site:
                fuel_type = generator.find('.//imo:FuelType', ns).text
                for output in generator.findall('.//imo:Outputs/imo:Output', ns):
                    hour = output.find('.//imo:Hour', ns).text
                    energy_mw = output.find('.//imo:EnergyMW', ns).text if output.find('.//imo:EnergyMW', ns) is not None else "N/A"
                    capability_mw = None
                    capability = generator.find(f'.//imo:Capabilities/imo:Capability[imo:Hour="{hour}"]', ns)
                    if capability is not None:
                        capability_mw = capability.find('.//imo:EnergyMW', ns).text

                    data.append({
                        'Generator Name': generator_name,
                        'Fuel Type': fuel_type,
                        'Hour': int(hour),  # Cast hour to int for comparison
                        'EnergyMW': energy_mw,
                        'CapabilityMW': capability_mw
                    })

    df = pd.DataFrame(data)
    df_filtered = df.loc[df.groupby('Generator Name')['Hour'].idxmax()]

    return df_filtered

# df = parseGenOutputCapability(["EAST WINDSOR-G1", "STEWARTVLE", "PRINCEFARM"])
# print(df.head())

from xml.etree import ElementTree as ET

def genNames():
    xml_file_path = 'PUB_GenOutputCapability.xml'
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Define the namespace to use for finding elements
    namespaces = {
        'imo': 'http://www.theIMO.com/schema'
    }

    # Extract all generator names
    generator_names = [elem.text for elem in root.findall('.//imo:GeneratorName', namespaces)]
    
    return generator_names