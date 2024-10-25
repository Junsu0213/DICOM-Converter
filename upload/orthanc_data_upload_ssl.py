# -*- coding:utf-8 -*-
"""
Created on Mon. Sep. 09 10:06:21 2024
@author: JUN-SU Park

Modified with timeout settings and connection debugging
"""
import requests
import os
import pydicom
import sys
from requests.auth import HTTPBasicAuth
import urllib3
import socket


class OrthancUploader:
    def __init__(self, server_config):
        """
        Initialize uploader with server configuration.
        """
        self.server_url = server_config['url']
        self.auth = HTTPBasicAuth(server_config['username'], server_config['password'])
        self.verify_ssl = server_config['verify_ssl']
        self.timeout = server_config.get('timeout', 30)

        if not self.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def test_server_connection(self):
        """Test basic network connectivity to server"""
        url_parts = self.server_url.replace('https://', '').replace('http://', '').split(':')
        host = url_parts[0]
        port = int(url_parts[1]) if len(url_parts) > 1 else 8042

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()

            if result == 0:
                print(f"✓ Successfully connected to port {port} on {host}")
                return True
            else:
                print(f"✗ Port {port} is closed on {host}")
                return False
        except socket.error as e:
            print(f"✗ Network error: {e}")
            return False

    def check_connection(self):
        """Check if the remote Orthanc server is accessible."""
        if not self.test_server_connection():
            return False

        try:
            print(f"Attempting to connect to {self.server_url}")
            response = requests.get(
                f'{self.server_url}/system',
                auth=self.auth,
                verify=self.verify_ssl,
                timeout=self.timeout
            )
            print(f"✓ Server response status code: {response.status_code}")
            if response.status_code == 200:
                server_info = response.json()
                print(f"✓ Connected to Orthanc server version: {server_info.get('Version', 'unknown')}")
            return response.status_code == 200
        except requests.exceptions.SSLError as e:
            print(f"✗ SSL Error: {e}")
            return False
        except requests.exceptions.ConnectionError as e:
            print(f"✗ Connection Error: {e}")
            return False
        except requests.exceptions.Timeout as e:
            print(f"✗ Timeout Error: {e}")
            return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Request Error: {e}")
            return False

    def is_dicom(self, file_path):
        try:
            pydicom.dcmread(file_path)
            return True
        except:
            return False

    def upload_dicom(self, file_path):
        """Upload a single DICOM file to the remote server."""
        try:
            with open(file_path, 'rb') as dicom_file:
                headers = {'Content-Type': 'application/dicom'}
                response = requests.post(
                    f'{self.server_url}/instances',
                    data=dicom_file,
                    headers=headers,
                    auth=self.auth,
                    verify=self.verify_ssl,
                    timeout=self.timeout
                )

            if response.status_code == 200:
                print(f"✓ Successfully uploaded: {os.path.basename(file_path)}")
                return response.json()
            else:
                print(f"✗ Upload failed for {os.path.basename(file_path)}: {response.status_code}")
                print(f"  Error: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"✗ Error uploading {os.path.basename(file_path)}: {e}")
            return None

    def upload_folder(self, folder_path):
        """Upload all DICOM files from a folder to the remote server."""
        if not self.check_connection():
            print(f"✗ Cannot connect to server at {self.server_url}")
            sys.exit(1)

        successful_uploads = 0
        failed_uploads = 0
        total_files = 0

        print("\nStarting DICOM upload process...")

        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if self.is_dicom(file_path):
                    total_files += 1
                    result = self.upload_dicom(file_path)
                    if result:
                        successful_uploads += 1
                    else:
                        failed_uploads += 1
                else:
                    print(f"ℹ Skipped non-DICOM file: {file}")

        print(f"\n=== Upload Summary ===")
        print(f"Total DICOM files found: {total_files}")
        print(f"Successfully uploaded: {successful_uploads} files")
        print(f"Failed uploads: {failed_uploads} files")

        if successful_uploads == total_files:
            print("✓ All files uploaded successfully!")
        else:
            print("⚠ Some uploads failed. Check the logs above for details.")


if __name__ == '__main__':
    # Server configuration
    server_config = {
        'url': 'http://192.168.44.190:8042',  # 실제 서버 IP나 도메인으로 변경
        'username': 'wlsdud022',  # Orthanc 사용자 이름
        'password': 'wlsdud022',  # Orthanc 비밀번호
        'verify_ssl': False,
        'timeout': 30
    }

    # DICOM 파일이 있는 로컬 폴더 경로
    dicom_folder_path = r'C:\Users\BMC\Desktop\COV-CCO-test_ver.2'

    print("=== Orthanc DICOM Uploader ===")
    print(f"Target Server: {server_config['url']}")
    print(f"Source Folder: {dicom_folder_path}")

    # 업로더 초기화 및 실행
    uploader = OrthancUploader(server_config)
    uploader.upload_folder(dicom_folder_path)