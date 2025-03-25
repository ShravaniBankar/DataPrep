from flask import Flask, request, jsonify
import pandas as pd
import os
from data_preprocessing.pipeline import clean_data, transform_data

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path})

@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    file_path = data.get('file_path')
    impute_strategy = data.get('impute_strategy', 'mean')
    remove_outliers = data.get('remove_outliers', False)
    outlier_method = data.get('outlier_method', 'IQR')

    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'Invalid file path'}), 400

    df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
    cleaned_df = clean_data(df, impute_strategy, remove_outliers, outlier_method)
    transformed_df = transform_data(cleaned_df)
    
    processed_file = os.path.join(UPLOAD_FOLDER, 'processed_' + os.path.basename(file_path))
    transformed_df.to_csv(processed_file, index=False)
    
    return jsonify({'message': 'Data processed successfully', 'processed_file': processed_file})

if __name__ == '__main__':
    app.run(debug=True)
