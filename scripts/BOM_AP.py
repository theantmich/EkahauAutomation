import zipfile
import json
import argparse
import csv

def main():

    ap_list = []

    #Lire les arguments fournis lors du lancement du script, c'est-à-dire le nom du fichier Esx.
    parser = argparse.ArgumentParser()
    parser.add_argument('file', metavar='esx_file', help='Ekahau project file')
    args = parser.parse_args()
    
    
    
    #Extraire le contenu du fichier Esx
    with zipfile.ZipFile(args.file, 'r') as zip:
        zip.extractall('project')
        
    #Ouvrir les fichiers JSON requis
    with open('project/accessPoints.json') as ap:
        apJSON = json.load(ap)
        
    with open('project/simulatedRadios.json') as sRadio:
        sRadioJSON = json.load(sRadio)
        
    with open('project/antennaTypes.json') as antenna:
        antennaJSON = json.load(antenna)

    with open('project/floorPlans.json') as floor:
        floorJSON = json.load(floor)
    
    with open('BOM_AP.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["AP_NUMBER", "AP_NAME", "AP_FLOOR", "AP_VENDOR", "AP_MODEL", "AP_ANTENNA", "AP_HEIGHT (FT)", "AP_TILT", "AP_MOUNTING"])
        
        ap_num = 0
        
        for ap in apJSON['accessPoints']:
            for radio in sRadioJSON['simulatedRadios']:
                for antenna in antennaJSON['antennaTypes']:
                    for floor in floorJSON['floorPlans']:
                        # Obtention des informations des points d'acces (hauteur, angle et installation)
                        if ap['id'] == radio['accessPointId']:
                            
                            ap_height_meter = radio['antennaHeight']
                            ap_height_feet = round(ap_height_meter * 3.28084,2)
                            #print(ap_height_feet,ap_height_meter)
                            
                            ap_tilt = radio['antennaTilt']
                            ap_mounting = radio['antennaMounting']
                            

                        # Obtention du modele d'AP et d'antenne (interne/externe)
                        if "+" in ap['model']:
                            
                            plusPosition = ap['model'].index('+')
                            
                            ap_model = ap['model'][:plusPosition]
                            ap_antenna = ap['model'][plusPosition+3:]

                            print(ap_model)
                            
                        else :
                            ap_model = ap['model']
                            ap_antenna = "Internal Antenna"


                        # Obtention du nom d'etage
                        if ap['location']['floorPlanId'] == floor['id']:
                            ap_floor = floor['name']
                            

            #Ecriture des informations dans le document CSV           
            if ap['name'] not in ap_list:
                ap_num += 1
            
                writer.writerow([ap_num, ap['name'], ap_floor, ap['vendor'], ap_model, ap_antenna, ap_height_feet, ap_tilt, ap_mounting])
                ap_list.append(ap['name'])
                #print(ap_list)

main()