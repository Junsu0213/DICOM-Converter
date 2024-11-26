# -*- coding:utf-8 -*-
from CCO_Converters.cco_json2segdcm_main import cco_segdcm_convert_process_all
from CCO_Converters.cco_metainfo_convert_main import cco_metainfo_convert_process_all
from upload.orthanc_data_upload_ssl import OrthancUploader


if __name__ == "__main__":
    # Local folder path containing DICOM files
    input_dir = r'C:\Users\BMC\Desktop\COV-CCO'
    # cco_segdcm_convert_process_all(input_dir)
    # cco_metainfo_convert_process_all(input_dir)

    # Server configuration
    server_config = {
        'url': 'http://192.168.44.190:8042',  # Replace with actual server IP or domain
        'username': 'wlsdud022',  # Username
        'password': 'wlsdud022',  # Password
        'verify_ssl': False,
        'timeout': 30
    }

    print("=== Orthanc DICOM Uploader ===")
    print(f"Target Server: {server_config['url']}")
    print(f"Source Folder: {input_dir}")

    # Initialize and run uploader
    uploader = OrthancUploader(server_config)
    uploader.upload_folder(input_dir)
