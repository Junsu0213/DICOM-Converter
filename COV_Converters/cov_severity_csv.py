# -*- coding:utf-8 -*-
"""
Created on Fri. Nov. 29 13:32:01 2024
@author: JUN-SU PARK

Script Title: Clinical Metadata Extraction

This script automates the extraction of clinical metadata from JSON annotation files
and generates a summary CSV file containing:

1. Patient information
2. Clinical labels (e.g., disease and severity)
3. Timestamps and grouping information

The output is saved as a CSV file for further analysis.
"""

import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm


def extract_metadata(base_dir: str, save_dir: str, output_file: str = 'COV_Feedback.csv') -> None:
    """
    Extracts clinical metadata from JSON annotation files and saves it as a CSV file.

    Args:
        base_dir (str): Path to the base directory containing patient folders.
        save_dir (str): Path to the directory where the CSV file will be saved.
        output_file (str): Name of the output CSV file (default: 'COV_Feedback.csv').

    Returns:
        None: The function saves the extracted metadata in the specified output directory.
    """
    # List all patient directories in the base directory
    patient_dirs = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

    meta_info_list = []  # List to store metadata for all patients
    num = 1  # Counter for numbering rows

    for patient_dir in tqdm(patient_dirs, total=len(patient_dirs), desc='Extracting clinical metadata', unit=' patients'):
        # Extract patient ID and group information
        patient_id = os.path.basename(patient_dir)
        try:
            mc_name = patient_id.split('-')[1]  # Group name extraction (e.g., hospital or cohort name)
        except IndexError:
            mc_name = patient_id.split('_')[1]

        # List all date directories for the current patient
        ord_dirs = [os.path.join(patient_dir, f) for f in os.listdir(patient_dir) if os.path.isdir(os.path.join(patient_dir, f))]

        for ord_dir in ord_dirs:
            try:
                # Extract date information
                date_ = os.listdir(ord_dir)[0]

                # Define the path to the JSON annotation directory
                json_dir = os.path.join(ord_dir, date_, 'TargetSequence', 'annotation', 'original')
                json_files = [os.path.join(json_dir, f) for f in os.listdir(json_dir) if f.endswith('.json')]

                # Initialize default metadata values
                severity = None
                disease = None

                for json_file in json_files:
                    with open(json_file, 'r') as f:
                        json_data = json.load(f)

                    try:
                        # Extract severity information from the JSON data
                        nih_severity = json_data['clinical information']['severity']['NIH']
                        who_severity = json_data['clinical information']['severity']['WHO']
                    except KeyError:
                        # Handle alternative severity key format
                        nih_severity = json_data['clinical information']['severity (measure at 1st visit)']['NIH']
                        who_severity = json_data['clinical information']['severity (measure at 1st visit)']['WHO']

                    severity = f'{nih_severity} ({who_severity})'

                    try:
                        # Extract disease label from the JSON data
                        disease = json_data["annotations"]['shapes'][0]["label"]
                        break  # Use the first valid disease label found
                    except Exception:
                        disease = 'Normal'

                # Append metadata to the list
                meta_info = [num, mc_name, patient_id, date_, disease, severity]
                meta_info_list.append(meta_info)
                num += 1

            except Exception as e:
                print(f"Error processing {patient_id} - {date_}: {str(e)}")
                continue

    # Convert the metadata list into a Pandas DataFrame
    meta_info_array = np.array(meta_info_list)
    columns = ['Num.', 'Group', 'Patient ID', 'Date', 'Label', 'Severity (NIH (WHO))']
    df = pd.DataFrame(meta_info_array, columns=columns)

    # Save the DataFrame to a CSV file
    save_path = os.path.join(save_dir, output_file)
    df.to_csv(save_path, index=False)
    print(f"Metadata successfully saved to {save_path}")


if __name__ == '__main__':
    # Input and output directory paths
    base_dir = r'D:\DATASET\Healthcare\dataset\CT'
    save_dir = r'D:\DATASET\Healthcare'

    # Run the metadata extraction process
    extract_metadata(base_dir, save_dir)
