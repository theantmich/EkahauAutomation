import time
import zipfile
import json
import argparse
import csv

def main():

    ap_list = []

    #Read arguments, aka the ESX file.
    parser = argparse.ArgumentParser()
    parser.add_argument('file', metavar='esx_file', help='Ekahau project file')
    args = parser.parse_args()
    
    
    
    #Extract the content of the ESX file.
    with zipfile.ZipFile(args.file, 'r') as zip:
        zip.extractall('project')
        
    #Open the required JSON files.
    with open('project/accessPoints.json') as ap:
        apJSON = json.load(ap)
        
    with open('project/simulatedRadios.json') as sRadio:
        sRadioJSON = json.load(sRadio)
        
    with open('project/antennaTypes.json') as antenna:
        antennaJSON = json.load(antenna)

    with open('project/floorPlans.json') as floor:
        floorJSON = json.load(floor)
    
    #Create CSV file.
    with open('BOM_AP.csv', 'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["AP_NUMBER", "AP_NAME", "AP_FLOOR", "AP_VENDOR", "AP_MODEL", "AP_ANTENNA", "AP_HEIGHT (FT)", "AP_TILT", "AP_MOUNTING"])
        
        ap_num = 0
        
        #Assignation of variables (AP, antenna, height, angle, floor, mounting)
        for ap in apJSON['accessPoints']:
            for radio in sRadioJSON['simulatedRadios']:
                for antenna in antennaJSON['antennaTypes']:
                    for floor in floorJSON['floorPlans']:

                        #Get AP info (height, tilt, mounting)
                        if ap['id'] == radio['accessPointId']:
                            
                            ap_height_meter = radio['antennaHeight']
                            ap_height_feet = round(ap_height_meter * 3.28084,2)
                            
                            ap_tilt = radio['antennaTilt']
                            ap_mounting = radio['antennaMounting']
                            

                        #Get AP model and antenna (internal/external)
                        if "+" in ap['model']:
                            
                            plusPosition = ap['model'].index('+')
                            
                            ap_model = ap['model'][:plusPosition]
                            ap_antenna = ap['model'][plusPosition+3:]
                            
                        else :
                            ap_model = ap['model']
                            ap_antenna = "Internal Antenna"


                        #Get floor name
                        if ap['location']['floorPlanId'] == floor['id']:
                            ap_floor = floor['name']
                            

            #Write AP data in the CSV file.           
            if ap['name'] not in ap_list:
                ap_num += 1
            
                writer.writerow([ap_num, ap['name'], ap_floor, ap['vendor'], ap_model, ap_antenna, ap_height_feet, ap_tilt, ap_mounting])
                ap_list.append(ap['name'])
                #print(ap_list)



main()

#Adds runtime
if __name__ == "__main__":
    start_time = time.time()
    print('** Updating AP Model Names...\n')
    main()
    run_time = time.time() - start_time
    print("\n** Time to run: %s sec" % round(run_time, 2))