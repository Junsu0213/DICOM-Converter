# -*- coding:utf-8 -*-
"""
Created on Fri. Nov. 29 13:56:11 2024
@author: JUN-SU PARK

Script Title: Full Pipeline for DICOM and ROI Processing

This script automates a complete workflow for processing DICOM files and
associated ROI (Region of Interest) files. It performs the following steps:

1. Converts JSON annotations to DICOM-SEG files.
2. Converts DICOM-SEG files to NIfTI (nii.gz) files for easier handling.
3. Moves and renames NIfTI files for consistency.
4. Extracts and saves metadata from JSON annotations to a CSV file.
5. Uploads the processed DICOM files to an Orthanc server for storage.

Dependencies:
- Custom modules:
  - `cov_json2segdcm_main`: Converts JSON to DICOM-SEG files.
  - `cov_metainfo_convert_main`: Extracts and updates DICOM metadata.
  - `cov_segdcm2segnii_main`: Converts DICOM-SEG to NIfTI.
  - `mv_roi_nii_files`: Moves and renames NIfTI files.
  - `orthanc_data_upload_ssl`: Handles secure DICOM upload to an Orthanc server.
"""

from COV_Converters.cov_json2segdcm_main import cov_segdcm_convert_process_all
from COV_Converters.cov_metainfo_convert_main import cov_metainfo_convert_process_all
from COV_Converters.cov_segdcm2segnii_main import cov_segdcm_to_segnii_preocess_all
from file_organizer.mv_roi_nii_files import move_and_rename_nii_files
from upload.orthanc_data_upload_ssl import OrthancUploader

if __name__ == "__main__":
    # Local folder path containing DICOM files
    base_dir = r'D:\DATASET\Healthcare\dataset\CT'  # Base directory for DICOM and JSON files
    save_dir = r'D:\DATASET\Healthcare\dataset_roi'  # Output directory for processed NIfTI files

    # Step 1: Convert JSON to DICOM-SEG
    print("Step 1: Converting JSON to DICOM-SEG...")
    cov_segdcm_convert_process_all(base_dir)

    # Step 2: Convert DICOM-SEG to NIfTI files
    print("Step 2: Converting DICOM-SEG to NIfTI files...")
    cov_segdcm_to_segnii_preocess_all(base_dir)

    # Step 3: Move and rename NIfTI files
    print("Step 3: Moving and renaming NIfTI files...")
    move_and_rename_nii_files(base_dir, save_dir)

    # Step 4: Extract metadata from JSON and save to CSV
    print("Step 4: Extracting metadata and saving to CSV...")
    cov_metainfo_convert_process_all(base_dir)

    # Server configuration for uploading DICOM files to Orthanc
    server_config = {
        'url': 'http://192.168.44.190:8042',  # Replace with actual server IP or domain
        'username': 'wlsdud022',  # Username for Orthanc
        'password': 'wlsdud022',  # Password for Orthanc
        'verify_ssl': False,  # Set to True if SSL verification is required
        'timeout': 30  # Timeout in seconds for server connection
    }

    print("=== Orthanc DICOM Uploader ===")
    print(f"Target Server: {server_config['url']}")
    print(f"Source Folder: {base_dir}")

    # Step 5: Upload processed DICOM files to the Orthanc server
    print("Step 5: Uploading files to Orthanc server...")
    uploader = OrthancUploader(server_config)
    uploader.upload_folder(base_dir)
    print("Upload complete!")
