# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 22:39:50 2020

@author: xhuae08006
"""

import pydicom as dicom
import os

path1 = 'C:/Users/xhuae08006/Desktop/anonymize py/1~T2/DCMData'
file_name = os.listdir(path1)
for item in file_name:
    dcm = dicom.read_file(os.path.join(path1,item),force=True)
    if dcm.PatientID == '0000409897':
        dcm.PatientID = '202001'
    if dcm.PatientName == 'ma xun':
        dcm.PatientName = 'Site02^Case01'
        
    dcm.save_as(os.path.join(path1,item))
print(dcm.PatientID)
print(dcm.PatientName)