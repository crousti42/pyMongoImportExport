# Script pour réaliser des imports Mongo
# Version 1.0
# Author gbrugere
# coding: utf8

import configparser
import datetime
import os
from pymongo import MongoClient
from aalibs.helpers import *

sCurrentPath = os.getcwd()
date = datetime.datetime.now()

# ------------------

sOuputFile = "extract_01.json"
sDbName = "offerScoringEngineDb"    # Nom de la base de donnée où seront importées les données
sCollectionName = "productScoringData" # Nom de la collection où seront importées les données

sServerToDeliver = "community" # entreprise | community 
sEnvToDeliver    = "dev" # dev | recette | preprod | prod

bToBeDelivered = False # True | False # Attention à ne pas activer, la livraison ne fonctionne pas encore

# ------------------

print ("-- Debut --")

oConfigFile = configparser.ConfigParser()
oConfigFile.read(sCurrentPath+"\\aalibs\configuration.ini")
sClusterConf = "cs_"+sServerToDeliver + "_" + sEnvToDeliver

sExportFilePath = sCurrentPath+"\\Exports\\"+sOuputFile

oExportFile = open(sExportFilePath, "w")

sLogfilePath = sCurrentPath+"\\"+"log_"+str(date.year)+"-"+date.strftime('%m')+"-"+date.strftime('%d')+".txt"
oLogFile = open(sLogfilePath,"w")

print(sClusterConf)

# mongoexport -v --out "C:\temp\myFile.json"

sCommandLine = "mongoexport -v"

# Host
if (oConfigFile.get(sClusterConf, "replicaset") != ""):
    sCommandLine += " --host "+oConfigFile.get(sClusterConf, "replicaset")+"/"+oConfigFile.get(sClusterConf, "serverList")
else:
    sCommandLine += " --host "+oConfigFile.get(sClusterConf, "serverList")

# User
sCommandLine += " --username "+oConfigFile.get(sClusterConf, "login")

# Password
sCommandLine += " --password "+oConfigFile.get(sClusterConf, "password")

# authenticationDatabase
sCommandLine += " --authenticationDatabase admin"

# Database
sCommandLine += " -d "+sDbName

# Collection
sCommandLine += " -c "+sCollectionName

# Fichier d'import
sCommandLine += " --out \""+sExportFilePath+"\""

# Arguments divers de fin de commande
sCommandLine += "  --type json  --jsonArray --pretty"

print (sCommandLine)

if (not bToBeDelivered):
    logAndPrint("["+sClusterConf+"] Livraison annulee par l'utilisateur", oLogFile)
    
else:
    sReturn = os.system(sCommandLine)

    if (sReturn == 0):
        logAndPrint("******** Script livre sans erreur ********", oLogFile)
    else:
        logAndPrint("####################### ERROR #######################", oLogFile)

    logAndPrint("["+sClusterConf+"] Import Fini: "+sExportFilePath, oLogFile)

oExportFile.close()
oLogFile.close()

print ("-- Fin --")