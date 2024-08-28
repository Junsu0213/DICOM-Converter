# -*- coding:utf-8 -*-
"""
Created on Mon. Aug. 12 14:25:31 2024
@author: JUN-SU Park
"""
import json
import numpy as np


def create_metainfo_json(output_file, labels):
    """
    Create metainfo.json file for SEG DICOM conversion.

    Args:
    output_file (str): Path to save the metainfo JSON file.
    labels (list): List of segment labels.
    seg_type (str): Type of segmentation (e.g., 'lobe', 'lesion').
    """
    # Fixed RGB values for the first 10 labels
    fixed_rgb_values = [
        [0, 255, 0],  # Green
        [255, 0, 0],  # Red
        [0, 0, 255],  # Blue
        [255, 255, 0],  # Yellow
        [255, 0, 255],  # Magenta
        [0, 255, 255],  # Cyan
        [128, 0, 0],  # Dark Red
        [0, 128, 0],  # Dark Green
        [0, 0, 128],  # Dark Blue
        [128, 128, 0],  # Olive
    ]

    metainfo = {
        "ContentCreatorName": "Reader1",
        "ClinicalTrialSeriesID": "Session1",
        "ClinicalTrialTimePointID": "1",
        "SeriesDescription": f"Original {labels[0]}",
        "SeriesNumber": "106",
        "InstanceNumber": "1",
        "segmentAttributes": [
            [{
                "labelID": i + 1,
                "SegmentDescription": label,
                "SegmentAlgorithmType": "MANUAL",
                "SegmentedPropertyCategoryCodeSequence": {
                    "CodeValue": "85756007",
                    "CodingSchemeDesignator": "SCT",
                    "CodeMeaning": "Tissue"
                },
                "SegmentedPropertyTypeCodeSequence": {
                    "CodeValue": "85756007",
                    "CodingSchemeDesignator": "SCT",
                    "CodeMeaning": "Tissue"
                },
                "recommendedDisplayRGBValue": fixed_rgb_values[i] if i < 10 else [
                    np.random.randint(0, 256),
                    np.random.randint(0, 256),
                    np.random.randint(0, 256)
                ]
            } for i, label in enumerate(labels)]
        ],
        "ContentLabel": "SEGMENTATION",
        "ContentDescription": f"Image segmentation for {labels[0]}",
        "ClinicalTrialCoordinatingCenterName": "dcmqi",
        "BodyPartExamined": "LUNG"
    }
    with open(output_file, 'w') as f:
        json.dump(metainfo, f, indent=2)
