# -*- coding:utf-8 -*-
"""
Created on Mon. Sep. 09 10:06:21 2024
@author: JUN-SU Park
"""
import requests
import os
import pydicom
import sys


def is_dicom(file_path):
    """
    Check if the given file is a DICOM file.

    Args:
    file_path (str): Path to the file to be checked.

    Returns:
    bool: True if the file is a DICOM file, False otherwise.
    """
    try:
        pydicom.dcmread(file_path)
        return True
    except:
        return False


def check_orthanc_connection(orthanc_url):
    """
    Check if the Orthanc server is accessible.

    Args:
    orthanc_url (str): URL of the Orthanc server.

    Returns:
    bool: True if the server is accessible, False otherwise.
    """
    try:
        response = requests.get(f'{orthanc_url}/system')
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def upload_dicom(file_path, orthanc_url):
    """
    Upload a single DICOM file to the Orthanc server.

    Args:
    file_path (str): Path to the DICOM file to be uploaded.
    orthanc_url (str): URL of the Orthanc server.
    """
    try:
        with open(file_path, 'rb') as dicom_file:
            headers = {'Content-Type': 'application/dicom'}
            response = requests.post(f'{orthanc_url}/instances', data=dicom_file, headers=headers)

        if response.status_code == 200:
            print(f"File uploaded successfully: {file_path}")
            print("Orthanc response:", response.json())
        else:
            print(f"File upload failed: {file_path}")
            print("Status code:", response.status_code)
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error uploading file {file_path}: {e}")


def upload_dicom_folder(folder_path, orthanc_url):
    """
    Upload all DICOM files from a given folder to the Orthanc server.

    Args:
    folder_path (str): Path to the folder containing DICOM files.
    orthanc_url (str): URL of the Orthanc server.
    """
    if not check_orthanc_connection(orthanc_url):
        print(f"Unable to connect to Orthanc server at {orthanc_url}")
        print("Please check if the server is running and the URL is correct.")
        sys.exit(1)

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_dicom(file_path):
                upload_dicom(file_path, orthanc_url)
            else:
                print(f"Not a DICOM file, skipped: {file_path}")


if __name__ == '__main__':

    # Set the Orthanc server URL
    orthanc_url = 'http://localhost:8043'  # Adjust this to match your Docker container's port

    # Set the path to the folder containing DICOM files
    dicom_folder_path = r'D:\DATASET\COVID_CT_Dataset\COV-CCO'  # Change this to your actual DICOM folder path

    # Upload all DICOM files in the folder
    upload_dicom_folder(dicom_folder_path, orthanc_url)
