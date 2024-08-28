# -*- coding:utf-8 -*-
"""
Created on Mon. Aug. 05 10:32:11 2024
@author: JUN-SU Park
"""
import os
import numpy as np
import pydicom
import SimpleITK as sitk
import pydicom_seg
from utils.metainfo_json_utils import create_metainfo_json


def create_seg_dicom(dicom_dir, output_dir=None, labels=None):
    """Create a SEG.DICOM file from DICOM files and metainfo."""
    if output_dir is None:
        parent_dir = os.path.dirname(dicom_dir)
        output_dir = os.path.join(parent_dir, 'dcm_seg')

    os.makedirs(output_dir, exist_ok=True)

    if labels is None:
        labels = ['Pneumonia']

    labels = list(labels)

    metainfo_file = os.path.join(output_dir, f'{labels[0]}_metainfo.json')

    create_metainfo_json(metainfo_file, labels)

    # Load template from metainfo.json
    template = pydicom_seg.template.from_dcmqi_metainfo(metainfo_file)

    # Set up writer
    writer = pydicom_seg.MultiClassWriter(
        template=template,
        inplane_cropping=False,
        skip_empty_slices=False,
        skip_missing_segment=True,
    )

    # Get list of DICOM files
    dcm_files = [f for f in os.listdir(dicom_dir) if f.endswith('.dcm')]

    if not dcm_files:
        raise ValueError(f"No DICOM files found in {dicom_dir}")

    # Read Series Instance UID from the first DICOM file
    dcm_uid = pydicom.dcmread(os.path.join(dicom_dir, dcm_files[0])).SeriesInstanceUID

    # Read DICOM series using SimpleITK
    reader = sitk.ImageSeriesReader()
    dcm_files = reader.GetGDCMSeriesFileNames(dicom_dir, str(dcm_uid))
    reader.SetFileNames(dcm_files)
    image = reader.Execute()

    # Get segmentation data and convert to unsigned integer
    segmentation_data = sitk.GetArrayFromImage(image).astype(np.uint8)

    # Create a SimpleITK image from the segmentation data
    segmentation = sitk.GetImageFromArray(segmentation_data)
    segmentation.CopyInformation(image)

    # Read source DICOM images
    source_images = [pydicom.dcmread(x, stop_before_pixels=True) for x in dcm_files]

    # Write segmentation to DICOM
    dcm = writer.write(segmentation, source_images)

    seg_seq = dcm.SegmentSequence

    # Process each segment
    for segment in seg_seq:
        if 'SegmentDescription' in segment:
            # Get label information from Segment Description
            label = segment.SegmentDescription

            # Set label information to Segment Label
            segment.SegmentLabel = label

            # Set the Series Description to the segmentation name
            segment.SeriesDescription = f'segmentation'

            # Optional: Delete the original SegmentDescription
            # del segment.SegmentDescription
    dcm.ImageComments = "NOT FOR CLINICAL USE"

    output_file = os.path.join(output_dir, f'{labels[0]}_segmentation.dcm')

    # Save the DICOM-SEG file
    dcm.save_as(output_file)
    print(f"DICOM-SEG file saved: {output_file}")
