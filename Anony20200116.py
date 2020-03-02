# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 13:08:28 2019

@author: xhuae08006
"""

import os
import pydicom
import sys

def demographic_update(currentPID, newPID,newPatientName):
    with open("demographic." + currentPID, 'r', encoding="utf8") as df:
        lines = df.readlines()
        currentPTName = lines[2].rstrip("\n")
        if currentPID == lines[3].rstrip("\n"):
            print(currentPID + " confirmed.")
    df.close()
    tempString = ""
    with open("demographic." + currentPID, 'r', encoding="utf8") as df:
        for line in df:
            if line.rstrip("\n") == currentPTName:
                tempString += newPatientName + "\n"
            elif line.rstrip("\n") == currentPID:
                tempString += newPID + "\n"
            else:
                tempString += line
    df.close()
    with open("demographic." + currentPID, 'w', encoding="utf8") as wdf:
        wdf.write(tempString)
    wdf.close()

    os.rename("demographic." + currentPID, "demographic." + newPID)
    print("demographic." + currentPID + " is updated as " "demographic." + newPID)
    return(currentPTName)

def info_update(currentPID, newPID):
    tempString = ""
    current_path = os.getcwd()
    print(current_path)
    with open("info", "r", encoding="utf8") as f:
        for infoLine in f:
            # Update Patient ID
            if infoLine == "1~" + currentPID + "\n":
                infoLine = "1~" + newPID + "\n"
                tempString += infoLine
            else:
                tempString += infoLine
        print(tempString)
    f.close()
    with open("info", "w", encoding="utf8") as wff:
        wff.write(tempString)
    wff.close()

def dicom_update(currentPID, newPID, newPhysician,newPatientName):
    numberofDCMFiles = 0
    for f in os.listdir():
        f_name, f_ext = os.path.splitext(f)
        if f_ext != ".DCM":
            continue
        else:
            ds = pydicom.dcmread(f, force=True)
            print(f_name)
            # get current patient ID and name
            dicomPatientID = ds.PatientID
            # dicomPatientName = ds.PatientName
            if dicomPatientID != currentPID:
                print(f + " DICOM patient ID does not match")

            # update patient ID and name in the DCM file
            ds.PatientName = newPatientName
            ds.PatientID = newPID
            ds.PhysicianName = newPhysician

            ds.save_as(f)
            numberofDCMFiles += 1
    print(str(numberofDCMFiles) + " DCM file in " + os.getcwd() + " have been updated.")

def plan_update(currentPID, newPID):

    planFolder = os.getcwd()
    print(os.getcwd())
    planFolders = os.listdir()
    plan_path_org = os.getcwd()

    
    for folder in planFolders:
        
        plan_path = os.path.join(plan_path_org,folder)
        planfilename = os.listdir(plan_path)
        flag = [folder_.split('.')[-1] for folder_ in planfilename]
        print('=================================')
        print(flag)
        print('=================================')
        tempString = ""
        adtPlanFlag = False
        os.chdir(planFolder + "\\" + folder)
        for file in os.listdir():
            f_name, f_ext = os.path.splitext(file)
            if f_ext != ".art":
                continue
            else:
                adtPlanFlag = True
        if adtPlanFlag == False:
            if 'hyp' in flag:
                print(folder + " is a master plan.")
                os.rename(currentPID + ".hyp", newPID + ".hyp")
            else:
                continue
        else:
            if 'hyp' in flag:
                print(folder + "is an adapted plan.")
                os.rename(currentPID + ".hyp", newPID + ".hyp")
                os.rename(currentPID + ".art", newPID + ".art")
            else:
                continue

        print(os.getcwd())
        # if
        with open("plan", "r", encoding="utf8") as pf:
            for planFileLine in pf:
                print(planFileLine)
                if planFileLine == currentPID + "\n":
                    planFileLine = newPID + "\n"
                    tempString += planFileLine
                else:
                    tempString += planFileLine
            print(tempString)
        pf.close()

        with open("plan", "w", encoding="utf8") as wpf:
            wpf.write(tempString)
        wpf.close()
        print(os.getcwd() + " \"plan\" has been updated.")


def Anonymization(dirName,patientList,SD_table,SD_table1):

    for patient in patientList:
        
        # create new patientID,name,physicianName
        newPatientID = SD_table[patient]
        newPatientName = SD_table1[patient]
        newPhysicianName = SD_table[patient]
        print(newPatientID)
        
        
        os.chdir(dirName+ "\\" + patient)
        # os.chdir(patient)
        currentPatientID = patient.split("~")[-1]
    
        #create a list of the folders in the patient directory
        subDirectory = os.listdir()
        print(subDirectory)
        for subDir in subDirectory:
            # Assume subfolders start with "1~" are image folders
            # update the studyset information as well as patient ID, name, physician name
            if "1~" in subDir:
                os.chdir(subDir)
                print(os.getcwd())
                print("Working on " + subDir)
    
                info_update(currentPatientID, newPatientID)
                print(os.getcwd() + " \"info\" is updated" )
    
                os.chdir("DCMData")
                dicom_update(currentPatientID, newPatientID, newPhysicianName,newPatientName)
                print("DICOM files are updated")
                os.chdir("..\..")
                print(os.getcwd())
                print("test")
            elif subDir == "plan":
                os.chdir("plan")
                plan_update(currentPatientID, newPatientID)
                
        print(os.getcwd())
        os.chdir("..\..")
        print(os.getcwd())
    
        # Call function to update currentPatientID demographic
        currentPatientName = demographic_update(currentPatientID, newPatientID, newPatientName)
        print("demographic is updated")
    
        # Change the patientID to anonymized ID
        os.chdir(dirName)
        os.rename("1~" + currentPatientID, "1~" + newPatientID)
        print("1~" + currentPatientID + " is renamed as " + "1~" + newPatientID)
    
    # keep a log file for recording the original paient ID, name and updated ID, name
    with open("C:\\Temp\\Patient_RenameLog.txt", 'a', encoding="utf8") as logf:
        patientRecord = currentPatientID + ", " + currentPatientName + "\t" + newPatientID + ", " + newPatientName
        logf.write(patientRecord)
    logf.close()
    print("Done")


# SD_table = {'1~0000607648':'201001','1~0000571965':'201002',
#          '1~0000549717':'201003','1~0000628540':'201004',
#          '1~0000374609':'201005','1~0000638492':'201006',
#          '1~0000510498':'201007','1~0000492064':'201008',
#          '1~0000638485':'201009','1~0000592485':'201010',
#          '1~0000592485A':'201010A','1~0000634180':'201011',
#          '1~0000653191':'201012','1~0000463294':'201013',
#          '1~0000659931':'201014','1~0000596190':'201015',
#          '1~0000674381':'201016','1~0000383280':'201017',
#          '1~0000623100':'201018','1~0000662101':'201019'}


# SD_table1 = {'1~0000607648':'Site01^Case01','1~0000571965':'Site01^Case02',
#          '1~0000549717':'Site01^Case03','1~0000628540':'Site01^Case04',
#          '1~0000374609':'Site01^Case05','1~0000638492':'Site01^Case06',
#          '1~0000510498':'Site01^Case07','1~0000492064':'Site01^Case08',
#          '1~0000638485':'Site01^Case09','1~0000592485':'Site01^Case10',
#          '1~0000592485A':'Site01^Case10A','1~0000634180':'Site01^Case11',
#          '1~0000653191':'Site01^Case12','1~0000463294':'Site01^Case13',
#          '1~0000659931':'Site01^Case14','1~0000596190':'Site01^Case15',
#          '1~0000674381':'Site01^Case16','1~0000383280':'Site01^Case17',
#          '1~0000623100':'Site01^Case18','1~0000662101':'Site01^Case19'}


#dirName = "C:\\Users\\Public\\Documents\\CMS\\FocalData\\Installation\\UnityTESTcopy4"
dirName = sys.argv[1]
#anony_mapping_path = "C:\\Users\\Downloads\\SD~Anonymization.txt"
anony_mapping_path = sys.argv[2]

os.chdir(dirName)  #         change to the working directory
patientRecord = ""
print(os.getcwd())      # make sure we are in the right place

# Create a list of patient ID as in Monaco
subDirs = os.listdir(dirName)
patientList = [dirname for dirname in subDirs if "1~" in dirname]
print(patientList)

# Set the patient directory as the working directory
os.chdir(dirName)

with open(anony_mapping_path,'r+') as f: line = f.readlines()
SD_table = {item.split('  ')[0]:item.split('  ')[1] for item in line}
SD_table1 = {item.split('  ')[0]:item.split('  ')[2].split('\n')[0] for item in line}

Anonymization(dirName,patientList,SD_table,SD_table1)