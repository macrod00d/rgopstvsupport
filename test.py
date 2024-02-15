from xml.etree import ElementTree as ET
import pandas as pd

# Load and parse the XML file
file_path = 'PUB_GenOutputCapability.xml'
tree = ET.parse(file_path)
root = tree.getroot()

# Define the namespace to access the elements correctly
ns = {'imo': 'http://www.theIMO.com/schema'}

site = "ABKENORA"

# Initialize a list to store the data
data = []

# Find the generator element for the specified site
for generator in root.findall('.//imo:Generator', ns):
    if generator.find('.//imo:GeneratorName', ns).text == site:
        # Extract fuel type once, assuming it's the same for all entries
        fuel_type = generator.find('.//imo:FuelType', ns).text

        # Combine the logic for Outputs and Capabilities into a single loop
        for output in generator.findall('.//imo:Outputs/imo:Output', ns):
            hour = output.find('.//imo:Hour', ns).text
            energy_mw = output.find('.//imo:EnergyMW', ns).text
            
            # Initialize capability data to None to handle cases where it might be missing
            capability_mw = None
            capability = generator.find(f'.//imo:Capabilities/imo:Capability[imo:Hour="{hour}"]', ns)
            if capability is not None:
                capability_mw = capability.find('.//imo:EnergyMW', ns).text

            data.append({
                'Generator Name': site,
                'Fuel Type': fuel_type,
                'Hour': hour,
                'EnergyMW': energy_mw,
                'CapabilityMW': capability_mw
            })

# Convert the list to a DataFrame
df = pd.DataFrame(data)

print(df.head())