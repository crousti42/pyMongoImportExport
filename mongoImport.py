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

sDbName = "serverSidePluginDb"    # Nom de la base de donnée où seront importées les données
sCollectionName = "products" # Nom de la collection où seront importées les données

sInputFile = "" # Si vide il prend tous les fichiers dans le dossier
sInputPath = "Imports"

sServerToDeliver = "entr-maas" # entreprise | entr-maas | entr-sword | entr-seo | entr-offerComparator | entr-userbox | community | searchmiddle | swordcluster | localhost
sEnvToDeliver    = "dev" # dev | recette | preprod | prod

sMode = "insert" # insert | upsert | merge 
bToBeDelivered = False # True | False # Attention à ne pas activer, la livraison ne fonctionne pas encore

# ------------------

print ("-- Debut --")

oConfigFile = configparser.ConfigParser()
oConfigFile.read(sCurrentPath+"\\aalibs\configuration.ini")
sClusterConf = "cs_"+sServerToDeliver + "_" + sEnvToDeliver

## Recuperation du ou des fichiers d'import

aImportFilePath = []
if sInputFile == "":
    # Si le nom est vide on prend tous les fichiers JSON du dossier
    for sCurrentFile in os.listdir(sCurrentPath+"\\"+sInputPath+"\\"):
        if sCurrentFile.endswith(".json") or sCurrentFile.endswith(".JSON"):    
            aImportFilePath.append(sCurrentPath+"\\"+sInputPath+"\\"+sCurrentFile)

else: 
    # Si le nom est rempli on prend juste le fichiers en question
    sImportFilePath = sCurrentPath+"\\"+sInputPath+"\\"+sInputFile
    manageInputFile(sImportFilePath)
    aImportFilePath.append(sImportFilePath)

sLogfilePath = sCurrentPath+"\\"+"log_"+str(date.year)+"-"+date.strftime('%m')+"-"+date.strftime('%d')+".txt"
oLogFile = open(sLogfilePath,"w")

## Génération des commandes 

aCommandLines = []

for sImportFilePath in aImportFilePath:

    sCommandLine = "mongoimport -v"
    
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
    sCommandLine += " --file \""+sImportFilePath+"\""
    
    # Mode
    sCommandLine += " --mode "+sMode
    
    # Arguments divers de fin de commande
    sCommandLine += " --type json  --jsonArray --legacy"
    
    aCommandLines.append(sCommandLine)

## Affichiage des commandes

logAndPrint("["+sClusterConf+"] Liste des commandes d'import:"+"\n", oLogFile)

for sCommandLine in aCommandLines:
    print (sCommandLine)

## Livraison des imports

if (not bToBeDelivered):
    logAndPrint("\n["+sClusterConf+"] Livraison annulee par l'utilisateur", oLogFile)
    
else:
    sReturn = os.system(sCommandLine)

    if (sReturn == 0):
        logAndPrint("******** Script livre sans erreur ********", oLogFile)
    else:
        logAndPrint("####################### ERROR #######################", oLogFile)

    logAndPrint("["+sClusterConf+"] Import Fini: "+sImportFilePath, oLogFile)

oLogFile.close()

print ("-- Fin --")