# -*- coding:utf-8 -*-
from CCO_Converters.cco_json2segdcm_main import cco_segdcm_convert_process_all
from CCO_Converters.cco_metainfo_convert_main import cco_metainfo_convert_process_all
from upload.orthanc_data_upload_ssl import OrthancUploader


if __name__ == "__main__":
    input_dir = r'C:\Users\BMC\Desktop\COV-CCO TEST\COV-CCO-test_ver.3'
    cco_segdcm_convert_process_all(input_dir)
    cco_metainfo_convert_process_all(input_dir)

    # Server configuration
    server_config = {
        'url': 'http://192.168.44.190:8042',  # 실제 서버 IP나 도메인으로 변경
        'username': 'wlsdud022',  # Orthanc 사용자 이름
        'password': 'wlsdud022',  # Orthanc 비밀번호
        'verify_ssl': False,
        'timeout': 30
    }

    print("=== Orthanc DICOM Uploader ===")
    print(f"Target Server: {server_config['url']}")
    print(f"Source Folder: {input_dir}")

    uploader = OrthancUploader(server_config)
    uploader.upload_folder(input_dir)
