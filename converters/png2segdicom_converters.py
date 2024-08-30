# -*- coding:utf-8 -*-
"""
Created on Thu. Aug. 29 17:19:21 2024
@author: JUN-SU Park
"""
import os
import json
import shutil
import pydicom
from utils.png2dicom_utils import convert_png_to_dicom
from utils.create_seg_dcm_utils import create_seg_dicom


def convert_png_to_segdicom(png_name, labels, input_dir, output_dir=None):
    """
    Process data for a single patient.

    Args:
    patient_dir (str): Directory containing patient data.
    seg_name (str): Name of the segmentation type (e.g., 'lobe', 'lesion').
    """
    png_dir = os.path.join(input_dir, f'png_{png_name}')
    dcm_dir = os.path.join(input_dir, 'dcm')
    temp_dcm_dir = os.path.join(input_dir, 'temp_dcm')

    os.makedirs(temp_dcm_dir, exist_ok=True)

    # Initialize variables
    temp_dcm_files = []
    series_num = 0
    initial_series_number = None

    ref_dcm_files = sorted(os.listdir(dcm_dir))
    print(ref_dcm_files)

    for dcm_file in ref_dcm_files:
        if dcm_file.endswith('.dcm'):
            png_file = os.path.join(png_dir, dcm_file.replace('.dcm', '.png'))
            dcm_ref_file = os.path.join(dcm_dir, dcm_file)
            temp_dcm_file = os.path.join(temp_dcm_dir, dcm_file)
            if os.path.exists(dcm_ref_file):
                # Read reference DICOM to check series number
                dcm_ref = pydicom.dcmread(dcm_ref_file)
                current_series_number = dcm_ref.SeriesNumber
                print(initial_series_number, current_series_number)

                # If this is the first file, set the initial series number
                if initial_series_number is None:
                    initial_series_number = current_series_number

                # Check if series number has changed
                if current_series_number != initial_series_number and series_num > 5:
                    print(series_num)
                    print(f"Series number changed. Stopping processing")
                    break
                elif current_series_number != initial_series_number and series_num < 5:
                    for file in temp_dcm_files:
                        os.remove(file)
                        temp_dcm_files.pop()
                    temp_dcm_files = []

                if initial_series_number != current_series_number:
                    initial_series_number = current_series_number

                series_num += 1
                convert_png_to_dicom(png_file, dcm_ref_file, temp_dcm_file)
                temp_dcm_files.append(temp_dcm_file)

    if temp_dcm_files:
        # Create SEG.DICOM
        create_seg_dicom(temp_dcm_dir, output_dir=output_dir, labels=labels)

        for file in temp_dcm_files:
            os.remove(file)
        os.rmdir(temp_dcm_dir)
    else:
        print(f"No DICOM files were created for {input_dir}")


if __name__ == '__main__':
    input_dir = r'D:\DATASET\COVID_CT_Dataset\COV-CCO\COV-CCO-001\20210112'
    png_name = 'lobe'
    labels = ['lobe1', 'lobe2', 'lobe3', 'lobe4', 'lobe5']
    convert_png_to_segdicom(png_name, labels, input_dir)
