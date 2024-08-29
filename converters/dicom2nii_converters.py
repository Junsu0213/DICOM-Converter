# -*- coding:utf-8 -*-
"""
Created on Wed. Aug. 28 17:24:07 2024
@author: JUN-SU Park
"""
import SimpleITK as sitk
import os


def convert_dicom_to_nii(input_dir, output_dir=None):
    if output_dir is None:
        parent_dir = os.path.dirname(input_dir)
        output_dir = os.path.join(parent_dir, 'nii')
    os.makedirs(output_dir, exist_ok=True)

    file_name = os.path.basename(input_dir)

    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(input_dir)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    sitk.WriteImage(image, f'{output_dir}/{file_name}.nii.gz')


if __name__ == '__main__':
    input_dir = r'D:\DATASET\DICOM_Converter_test\sub01\dcm'
    convert_dicom_to_nii(input_dir)
