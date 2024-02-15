from flask import Flask, render_template
from utils import parseGenOutputCapability, downloadFile, genNames
import pandas as pd

app = Flask(__name__)

@app.route('/')
def chart():
    downloadFile()
    df = parseGenOutputCapability(genNames())
    processed_data = []
    for _, row in df.iterrows():
        generator_name = row['Generator Name']
        try:
            energy = float(row['EnergyMW']) if row['EnergyMW'].lower() != 'n/a' else None
            capability = float(row['CapabilityMW'])
            if energy is None or capability is None:
                raise ValueError
            remaining_capacity = capability - energy
            if remaining_capacity <= 0:
                continue
            processed_data.append({
                'name': generator_name,
                'data': {'PowerOut': energy, 'RemainingCapacity': remaining_capacity}
            })
        except ValueError:
            processed_data.append({'name': generator_name, 'error': 'Data Unavailable'})

    return render_template('chart.html', generators=processed_data)

if __name__ == '__main__':
    app.run(debug=True)