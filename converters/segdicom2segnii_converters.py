import SimpleITK as sitk
import nibabel as nib
import os


def convert_segdcm_to_segnii(input_dir: str, output_dir: str = None, file_name: str = None) -> None:
    if output_dir is None:
        output_dir = input_dir
    os.makedirs(output_dir, exist_ok=True)

    seg_dcm = [f for f in os.listdir(input_dir) if f.endswith('.dcm')]
    if file_name is None:
        file_name = seg_dcm[0].split('.dcm')[0]

    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(input_dir)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()

    save_path = os.path.join(output_dir, f'{file_name}.nii.gz')

    sitk.WriteImage(image, save_path)

    nii = nib.load(save_path)
    data = nii.get_fdata()

    modified_data = data/255.0

    modified_nii = nib.Nifti1Image(modified_data, affine=nii.affine, header=nii.header)

    nib.save(modified_nii, save_path)


if __name__ == '__main__':
    input_dir = r'C:\Users\BMC\Desktop\Dataset\TEST DATASET\Healthcare_seg_nii_test\TargetSequence\dcm_seg'
    convert_segdcm_to_segnii(input_dir)
