from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload Raw Excel File</h1>
    <form action="/process" method="post" enctype="multipart/form-data">
        <input type="file" name="file" />
        <button type="submit">Upload and Process</button>
    </form>
    '''

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)

    # Load and process the Excel file
    raw_data = pd.ExcelFile(file_path)
    data_sheet = raw_data.parse("Data")
    final_data = pd.DataFrame()
    final_data["Customer Name"] = "AgileApt Solutions Pvt Ltd"
    final_data["Start Date"] = "November 13, 2024"
    final_data["End Date"] = "November 30, 2024"
    final_data["Subscription ID"] = data_sheet["Unnamed: 3"].fillna(method='ffill')
    final_data["Meter Name"] = data_sheet["Unnamed: 2"]
    final_data["Service Type"] = "Azure Service"
    final_data["Resource Name"] = data_sheet["Unnamed: 1"]
    final_data["Region"] = "Global"
    final_data["Total Cost"] = data_sheet["Unnamed: 4"]

    # Save the processed file
    output_path = os.path.join("uploads", "Transformed_Billing.xlsx")
    final_data.to_excel(output_path, index=False)

    return jsonify({"message": "File processed successfully.", "output": output_path})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
