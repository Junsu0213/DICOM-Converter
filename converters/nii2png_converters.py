# -*- coding:utf-8 -*-
"""
Created on Sat. Aug. 10 18:01:08 2024
@author: JUN-SU Park
"""
import nii2png
import os
import logging


def convert_nii_to_png(input_file, output_dir=None):
    # If output_dir is not provided, create a new directory
    if output_dir is None:
        # Get the directory of the input file
        input_dir = os.path.dirname(input_file)
        # Go up one level
        parent_dir = os.path.dirname(input_dir)
        # Create a new 'png' directory next to the 'nii' directory
        output_dir = os.path.join(parent_dir, 'png')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Convert NII to PNG using nii to png function
        nii2png.convert_nii_to_png(input_file, output_dir)
        logging.info(f"Converted {output_dir} to PNG")
    except Exception as e:
        logging.error(f"Error converting {input_file}: {str(e)}")