# Helpers pour les scripts MongoDb
# Version 1.0
# Author gbrugere
# coding: utf8

import os
import sys
import string
import random

# Print ameliore
def printThisLine(sToBeDisplayed, sTitle=''):
    if (sTitle != ''):
        print ('['+sTitle+']: '+sToBeDisplayed)
    else:
        print (sToBeDisplayed)
        
def logAndPrint(sToBeDisplayed, oLogFile):
    print (sToBeDisplayed)
    oLogFile.writelines(str(sToBeDisplayed)+"\n")    
        
# Verifie si un fichier existe, s'il n'existe pas erreur
def manageInputFile(sPathToFile):
    if not os.path.exists(sPathToFile) :
        print("Erreur: Fichier Input manquant: " + sPathToFile)
        sys.exit()

# Verifie si un fichier existe, s'il n'existe pas creation
def manageResultFile(sPathToFile):
    oCurrentFile = open(sPathToFile, "w")
    oCurrentFile.close()

# Genere un mot de passe avec dif�rents types de caracteres    
def getPassword(iNbrCharsTotal=6, sCharsPoolGlobal=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(sCharsPoolGlobal) for _ in range(iNbrCharsTotal))