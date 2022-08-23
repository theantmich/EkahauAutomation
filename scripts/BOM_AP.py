import time
from typing import SupportsRound
import zipfile
import json
import argparse
import csv
import os
import sys

def main():

    ### Preparation of variables, opening of JSON files from Ekahau
    ap_list = []

    #Adds then reads the first argument to know whether the file is Simulated (-s), Measured (-m) or Hybrid (-y)
    #Adds the second argument, aka the ESX file.
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', help='For Mesured Ekahau project files')
    parser.add_argument('-s', help='For Simulated Ekahau project files')
    parser.add_argument('-y', help='For Hybrid Ekahau project files')

    parser.add_argument('file', metavar='esx_file', help='Ekahau project file')
    args = parser.parse_args()
    #print(args)

    #Tests out which argument was entered to define the type of survey.
    if sys.argv[1] == '-m':
        surveyType = "measured"
    elif sys.argv[1] == '-s':
        surveyType = "simulated"
    elif sys.argv[1] == '-y':
        surveyType = "hybrid"
    else:
        raise SystemExit(f"Usage: {sys.argv[0]} (-m | -s | -y) file ekahauProject.esx")
    
    #print(sys.argv[1], surveyType)

    #Extract the content of the ESX file.
    with zipfile.ZipFile(args.file, 'r') as zip:
        zip.extractall('project')
        
    #Open the required JSON files.
    with open('project/accessPoints.json') as ap:
        apJSON = json.load(ap)
        
    if surveyType == "simulated" or "hybrid":
        with open('project/simulatedRadios.json') as sRadio:
            sRadioJSON = json.load(sRadio)

    elif surveyType == "measured" or "hybrid":
        with open('project/measuredRadios.json') as mRadio:
            mRadioJSON = json.load(mRadio)
        
    with open('project/antennaTypes.json') as antenna:
        antennaJSON = json.load(antenna)

    with open('project/floorPlans.json') as floor:
        floorJSON = json.load(floor)
    

    ### Algorithm that goes through all access points and adds their information to a CSV file.

    #Create CSV file.
    with open('BOM_AP.csv', 'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["AP_NUMBER", "AP_NAME", "AP_FLOOR", "AP_VENDOR", "AP_MODEL", "AP_ANTENNA", "AP_HEIGHT (FT)", "AP_TILT", "AP_MOUNTING"])
        
        ap_num = 0
        
        #Depending of the Survey type, extracts data from different files and writes it to a CSV.
        #Survey types are Hybrid, Simulated and Measured

        if surveyType == "hybrid":
            #Assignation of variables (AP, antenna, height, angle, floor, mounting)
            for ap in apJSON['accessPoints']:
                for radio in sRadioJSON['simulatedRadios']:
                    #print(radio['status'])
                    #print(radio['accessPointId'])
                    
                    for antenna in antennaJSON['antennaTypes']:
                        for floor in floorJSON['floorPlans']:

                            #Verify if radio still exists
                            if radio['status'] != "DELETED":

                                #Get AP info (height, tilt, mounting)
                                if ap['id'] == radio['accessPointId']:

                                    ap_height_meter = radio['antennaHeight']
                                    ap_height_feet = round(ap_height_meter * 3.28084,2)
                                    
                                    ap_tilt = str(radio['antennaTilt'])+'\u00B0'
                                    ap_mounting = radio['antennaMounting']

                                    if 'vendor' in ap:
                                        ap_vendor = ap['vendor']
                                    else:
                                        ap_vendor = "N/A"
                                else:

                                    for mRadio in mRadioJSON['measuredRadios']:
                                        
                                        if ap['id'] == mRadio['accessPointId']:
                                            ap_height_meter = radio['antennaHeight']
                                            ap_height_feet = round(ap_height_meter * 3.28084,2)
                                            
                                            ap_tilt = str(radio['antennaTilt'])+'\u00B0'
                                            ap_mounting = radio['antennaMounting']

                                            if 'vendor' in ap:
                                                ap_vendor = ap['vendor']
                                            else:
                                                ap_vendor = "N/A"
                                    
                                #Verify if AP still exists
                                if ap['status'] != "DELETED":
                                    #Get AP model and antenna (internal/external). Model has to be present
                                    if 'model' in ap:
                                        if "+" in ap['model']:
                                            
                                            if "2.4GHz + 5GHz" in ap['model']:
                                                ap_model = ap['model']
                                                ap_antenna = "Internal Antenna"

                                            else:
                                                plusPosition = ap['model'].index('+')
                                                
                                                ap_model = ap['model'][:plusPosition]
                                                ap_antenna = ap['model'][plusPosition+3:]
                                        else :
                                            ap_model = ap['model']
                                            ap_antenna = "Internal Antenna"

                                        if floor['status'] != "DELETED":
                                            #Get floor name, verify first if the AP is located on a floor
                                            if 'location' in ap:
                                                if ap['location']['floorPlanId'] == floor['id']:
                                                    ap_floor = floor['name']
                                        else:
                                            print("Deleted Floorplan")
                                else:
                                    print("Deleted AP")
                            else:
                                print("Deleted Radio")

                #Verify if AP still exists
                if ap['status'] or radio['status'] or mRadio['status'] or floor['status'] != "DELETED":
                    #Write AP data in the CSV file.           
                    if ap['id'] not in ap_list:
                        ap_num += 1
                
                        writer.writerow([ap_num, ap['name'], ap_floor, ap_vendor, ap_model, ap_antenna, ap_height_feet, ap_tilt, ap_mounting, ap['id']])
                        ap_list.append(ap['id'])
                        print(ap['name'])
                        
                        #print(ap_list)

        elif surveyType == "simulated":
            for ap in apJSON['accessPoints']:
                for radio in sRadioJSON['simulatedRadios']:
                    #print(radio['status'])
                    #print(radio['accessPointId'])
                    
                    for antenna in antennaJSON['antennaTypes']:
                        for floor in floorJSON['floorPlans']:

                            #Verify if radio still exists
                            if radio['status'] != "DELETED":

                                #Get AP info (height, tilt, mounting)
                                if ap['id'] == radio['accessPointId']:

                                    ap_height_meter = radio['antennaHeight']
                                    ap_height_feet = round(ap_height_meter * 3.28084,2)
                                    
                                    ap_tilt = str(radio['antennaTilt'])+'\u00B0'
                                    ap_mounting = radio['antennaMounting']

                                    if 'vendor' in ap:
                                        ap_vendor = ap['vendor']
                                    else:
                                        ap_vendor = "N/A"
                                
                                #Verify if AP still exists
                                if ap['status'] != "DELETED":
                                    #Get AP model and antenna (internal/external). Model has to be present
                                    if 'model' in ap:
                                        if "+" in ap['model']:
                                            
                                            if "2.4GHz + 5GHz" in ap['model']:
                                                ap_model = ap['model']
                                                ap_antenna = "Internal Antenna"

                                            else:
                                                plusPosition = ap['model'].index('+')
                                                
                                                ap_model = ap['model'][:plusPosition]
                                                ap_antenna = ap['model'][plusPosition+3:]
                                        else :
                                            ap_model = ap['model']
                                            ap_antenna = "Internal Antenna"

                                        if floor['status'] != "DELETED":
                                            #Get floor name, verify first if the AP is located on a floor
                                            if 'location' in ap:
                                                if ap['location']['floorPlanId'] == floor['id']:
                                                    ap_floor = floor['name']
                                        else:
                                            print("Deleted Floorplan")
                                else:
                                    print("Deleted AP")
                            else:
                                print("Deleted Radio")

                #Verify if AP still exists
                if ap['status'] or radio['status'] or mRadio['status'] or floor['status'] != "DELETED":
                    #Write AP data in the CSV file.           
                    if ap['id'] not in ap_list:
                        ap_num += 1
                
                        writer.writerow([ap_num, ap['name'], ap_floor, ap_vendor, ap_model, ap_antenna, ap_height_feet, ap_tilt, ap_mounting, ap['id']])
                        ap_list.append(ap['id'])
                        print(ap['name'])
                        
                        #print(ap_list)

        elif surveyType == "measured":
            for ap in apJSON['accessPoints']:
                for radio in mRadioJSON['measuredRadio']:
                    #print(radio['status'])
                    #print(radio['accessPointId'])
                    
                    for antenna in antennaJSON['antennaTypes']:
                        for floor in floorJSON['floorPlans']:

                            #Verify if radio still exists
                            if radio['status'] != "DELETED":

                                #Get AP info (height, tilt, mounting)
                                if ap['id'] == radio['accessPointId']:

                                    ap_height_meter = radio['antennaHeight']
                                    ap_height_feet = round(ap_height_meter * 3.28084,2)
                                    
                                    ap_tilt = str(radio['antennaTilt'])+'\u00B0'
                                    ap_mounting = radio['antennaMounting']

                                    if 'vendor' in ap:
                                        ap_vendor = ap['vendor']
                                    else:
                                        ap_vendor = "N/A"
                                                                    
                                #Verify if AP still exists
                                if ap['status'] != "DELETED":
                                    #Get AP model and antenna (internal/external). Model has to be present
                                    if 'model' in ap:
                                        if "+" in ap['model']:
                                            
                                            if "2.4GHz + 5GHz" in ap['model']:
                                                ap_model = ap['model']
                                                ap_antenna = "Internal Antenna"

                                            else:
                                                plusPosition = ap['model'].index('+')
                                                
                                                ap_model = ap['model'][:plusPosition]
                                                ap_antenna = ap['model'][plusPosition+3:]
                                        else :
                                            ap_model = ap['model']
                                            ap_antenna = "Internal Antenna"

                                        if floor['status'] != "DELETED":
                                            #Get floor name, verify first if the AP is located on a floor
                                            if 'location' in ap:
                                                if ap['location']['floorPlanId'] == floor['id']:
                                                    ap_floor = floor['name']
                                        else:
                                            print("Deleted Floorplan")
                                else:
                                    print("Deleted AP")
                            else:
                                print("Deleted Radio")

                #Verify if AP still exists
                if ap['status'] or radio['status'] or mRadio['status'] or floor['status'] != "DELETED":
                    #Write AP data in the CSV file.           
                    if ap['id'] not in ap_list:
                        ap_num += 1
                
                        writer.writerow([ap_num, ap['name'], ap_floor, ap_vendor, ap_model, ap_antenna, ap_height_feet, ap_tilt, ap_mounting, ap['id']])
                        ap_list.append(ap['id'])
                        print(ap['name'])
                        
                        #print(ap_list)
                    
main()

#Adds runtime
if __name__ == "__main__":
    start_time = time.time()
    print('** Finishing up... **\n')
    main()
    run_time = time.time() - start_time
    print("\n** Time to run: %s sec" % round(run_time, 2))