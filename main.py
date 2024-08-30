# -*- coding:utf-8 -*-
import pydicom

if __name__ == '__main__':
    dcm_path = r'D:\DATASET\COVID_CT_Dataset\COV-CCO\COV-CCO-001\20210112\dcm\00000284.dcm'
    dcm = pydicom.dcmread(dcm_path)
    print(dcm)
