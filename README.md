# EkahauAutomation

This repo serves the purpose of automating data extraction from Ekahau ESX files for reports and BOMs.

====================

BOM_AP.py

====================

PRE-REQUISITES :
1. Python 3
2. Pip3
3. Python module zipfile38

--------------------

HOW TO USE :

1. Git clone this repo or download it
2. Open a shell (Linux or Windows)
3. Use the command : python3 /path/to/script/BOM_AP.py [ -s | -m | -y ] file /path/to/your/esx/file.esx

Options -s/-m/-y are mandatory. Use them to define what kind of Ekahau file you are using the script for.

- Only measured access points : -m
- Only simulated access points : -s
- Mix of simulated and measured access points : -y

QoL tip : cd to the directory where you want to CSV file to end up before using the python command. The BOM is generated in the current directory, as well as the extracted esx archive. I recommend the following file structure :

- Parent Directory/
    L--> scripts/
         L--> BOM_AP.py
    L--> customers/
         L--> cust.1/ <===== /!\ CD HERE /!\
              L--> BOM.csv
              L--> Ekahau_Extracted_Archive/