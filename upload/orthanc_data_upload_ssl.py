# -*- coding:utf-8 -*-
"""
Created on Mon. Sep. 09 10:06:21 2024
@author: JUN-SU Park

Orthanc DICOM Upload Module with SSL Support

This module provides functionality to:
1. Upload DICOM files to an Orthanc server
2. Handle secure connections with SSL
3. Verify server connectivity and accessibility
4. Track upload progress and provide detailed feedback
"""
import os
import sys
import socket
import requests
import pydicom
import urllib3
from requests.auth import HTTPBasicAuth


class OrthancUploader:
    """
    A class to handle secure DICOM uploads to an Orthanc server.
    Includes connection testing, SSL verification, and upload tracking.
    """

    def __init__(self, server_config: dict):
        """
        Initialize uploader with server configuration.

        Args:
            server_config: Dictionary containing:
                - url: Server URL
                - username: Authentication username
                - password: Authentication password
                - verify_ssl: Whether to verify SSL certificates
                - timeout: Connection timeout in seconds
        """
        self.server_url = server_config['url']
        self.auth = HTTPBasicAuth(server_config['username'], server_config['password'])
        self.verify_ssl = server_config['verify_ssl']
        self.timeout = server_config.get('timeout', 30)

        # Disable SSL warnings if verification is disabled
        if not self.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def test_server_connection(self) -> bool:
        """
        Test basic network connectivity to server.

        Returns:
            bool: True if connection successful, False otherwise
        """
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

    def check_connection(self) -> bool:
        """
        Check if the remote Orthanc server is accessible and responding.

        Returns:
            bool: True if server is accessible, False otherwise
        """
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

    def is_dicom(self, file_path: str) -> bool:
        """
        Check if a file is a valid DICOM file.

        Args:
            file_path: Path to the file to check

        Returns:
            bool: True if file is valid DICOM, False otherwise
        """
        try:
            pydicom.dcmread(file_path)
            return True
        except:
            return False

    def upload_dicom(self, file_path: str) -> dict:
        """
        Upload a single DICOM file to the remote server.

        Args:
            file_path: Path to the DICOM file to upload

        Returns:
            dict: Server response if successful, None if failed
        """
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

    def upload_folder(self, folder_path: str) -> None:
        """
        Upload all DICOM files from a folder to the remote server.
        Tracks progress and provides upload statistics.

        Args:
            folder_path: Path to folder containing DICOM files
        """
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
        'url': 'http://:8042',  # Replace with actual server IP or domain
        'username': '',  # Username
        'password': '',  # Password
        'verify_ssl': False,
        'timeout': 30
    }

    # Local folder path containing DICOM files
    dicom_folder_path = r'C:\Users\BMC\Desktop\COV-CCO-test_ver.2'

    print("=== Orthanc DICOM Uploader ===")
    print(f"Target Server: {server_config['url']}")
    print(f"Source Folder: {dicom_folder_path}")

    # Initialize and run uploader
    uploader = OrthancUploader(server_config)
    uploader.upload_folder(dicom_folder_path)