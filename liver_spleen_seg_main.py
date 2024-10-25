# -*- coding:utf-8 -*-
"""
Created on Mon. Sep. 30 14:44:22 2024
@author: JUN-SU PARK
"""
import os
from converters.dicom2nii_converters import convert_dicom_to_nii

data_path = r'D:\DATASET\CT\liver_pancrease_dataset'
dcm_dir = rf'{data_path}\dcm_output'
nii_dir = rf'{data_path}\nii_output'

os.makedirs(nii_dir, exist_ok=True)

sub_list = os.listdir(dcm_dir)

for sub in sub_list:
    sub_dcm_path = os.path.join(dcm_dir, sub)
    sub_nii_path = os.path.join(nii_dir, sub)
    os.makedirs(sub_nii_path, exist_ok=True)

    dcm_file_list = os.listdir(sub_dcm_path)

    for dcm_file in dcm_file_list:
        print(f'Subject: {sub}, file name: {dcm_file}')
        dcm_file_path = os.path.join(sub_dcm_path, dcm_file)
        nii_file_path = os.path.join(sub_nii_path, dcm_file)

        if len(os.listdir(sub_dcm_path)) < 5:
            pass
        else:
            try:
                os.makedirs(nii_file_path, exist_ok=True)
                convert_dicom_to_nii(dcm_file_path, nii_file_path)
                print(f'Nifti file saved to {nii_file_path}')
            except Exception as e:
                print(e)
