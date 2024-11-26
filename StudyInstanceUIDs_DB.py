# -*- coding:utf-8 -*-
"""
Created on Tue. Nov. 19 13:17:22 2024
@author: JUN-SU PARK

This script orchestrates the DICOM metadata extraction process by:
1. Traversing through patient directories
2. Extracting metadata (PatientID, StudyDate, Modality, StudyInstanceUID)
3. Saving the extracted metadata into a CSV file
"""
import os
import pandas as pd
import pydicom


def extract_dicom_metadata(data_path, output_csv, stop_patient_id=None):
    """
    Extracts metadata from DICOM files and saves it to a CSV file.

    Parameters:
    - data_path (str): Path to the directory containing patient folders.
    - output_csv (str): Path where the output CSV file will be saved.
    - stop_patient_id (str, optional): Stop processing after this patient ID. Default is None.

    CSV Columns:
    - PatientID
    - StudyDate
    - Modality
    - StudyInstanceUID
    """
    # Initialize an empty list to store DICOM metadata
    dicom_metadata = []

    # List all patient directories
    patient_list = os.listdir(data_path)

    for patient_id in patient_list:
        # Navigate study date folders
        study_date_list = os.listdir(os.path.join(data_path, patient_id))
        for study_date in study_date_list:
            dcm_folder_path = os.path.join(data_path, patient_id, study_date, 'dcm')

            if os.path.exists(dcm_folder_path):
                dcm_list = os.listdir(dcm_folder_path)
                for dcm in dcm_list:
                    dcm_path = os.path.join(dcm_folder_path, dcm)

                    dcm_ps = pydicom.read_file(dcm_path)

                    try:
                        # Mock DICOM reading logic (replace with real metadata later if `pydicom` is available)
                        PatientID = dcm_ps.PatientID  # Placeholder for patient ID
                        StudyDate = dcm_ps.StudyDate  # Placeholder for study date
                        Modality = dcm_ps.Modality  # Placeholder for modality
                        StudyInstanceUID = dcm_ps.StudyInstanceUID  # Placeholder for Study Instance UID

                        # Append metadata to the list
                        dicom_metadata.append({
                            'PatientID': PatientID,
                            'StudyDate': StudyDate,
                            'Modality': Modality,
                            'StudyInstanceUID': StudyInstanceUID
                        })

                    except Exception as e:
                        print(f"Error processing {dcm_path}: {e}")

                    break  # Process only one file per folder as in the original code

        # Break condition for specific patient
        if stop_patient_id and patient_id.endswith(stop_patient_id):
            break

    # Convert the metadata list into a pandas DataFrame
    dicom_df = pd.DataFrame(dicom_metadata)

    # Save the DataFrame to a CSV file
    dicom_df.to_csv(output_csv, index=False, encoding='utf-8')

    print(f"DICOM metadata has been successfully saved to {output_csv}.")


# Example usage
if __name__ == "__main__":
    data_path = r'E:\헬스케어인공지능연구과 의료영상 데이터\최종 제출\1차\dataset\COV-CCO'
    output_csv = r'C:\Users\BMC\Desktop\GenomicsPACs-Linker\dicom_metadata_pandas.csv'
    stop_patient_id = '073'  # Stop after this patient ID (optional)

    extract_dicom_metadata(data_path, output_csv, stop_patient_id)
