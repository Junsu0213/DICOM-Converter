# -*- coding:utf-8 -*-
"""
Created on Wed. Aug. 14 10:47:07 2024
@author: JUN-SU Park

This module provides functions to:
1. Extract clinical labels and patient information from JSON annotations
2. Update DICOM metadata with the extracted information
"""

import os
import json
import pydicom
from typing import Tuple, Optional


def extract_label_form_json(json_dir: str) -> Tuple[str, str]:
    """
    Extract clinical labels and patient sex from JSON annotation files.

    Args:
        json_dir: Directory containing JSON annotation files

    Returns:
        Tuple containing:
            - study_description: String describing diagnosis and severity
            - sex: Patient's sex information
    """
    label = None
    severity_nih = None
    severity_who = None

    json_files = os.listdir(json_dir)

    # Iterate through JSON files to find valid annotations
    for json_file in json_files:
        json_path = os.path.join(json_dir, json_file)

        with open(json_path, 'r') as f:
            data = json.load(f)

        try:
            # Extract clinical information
            label = data["annotations"]["shapes"][0]["label"]
            severity_nih = data["clinical information"]["severity"]["NIH"]
            severity_who = data["clinical information"]["severity"]["WHO"]
            sex = data["clinical information"]["sex"]
        except IndexError:
            # Handle cases without annotation shapes
            sex = data["clinical information"]["sex"]
            continue

        if label is not None:
            break

    # Format study description
    study_description = ("Normal" if label is None
                        else f"{label}({severity_nih}({severity_who}))")

    return study_description, sex


def convert_dicom_metainfo(dcm_dir: str, label: str, sex: str) -> None:
    """
    Update DICOM metadata with provided clinical information.

    Args:
        dcm_dir: Directory containing DICOM files
        label: Study description to be added to DICOM metadata
        sex: Patient sex information to be added to DICOM metadata
    """
    # Iterate through all DICOM files in directory
    for dcm_file in os.listdir(dcm_dir):
        dcm_path = os.path.join(dcm_dir, dcm_file)

        # Read and update DICOM metadata
        dcm_ds = pydicom.dcmread(dcm_path)
        dcm_ds.StudyDescription = label
        dcm_ds.PatientSex = sex

        # Save updated DICOM file
        dcm_ds.save_as(dcm_path)
