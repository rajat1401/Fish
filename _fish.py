import sys
import hashlib
import argparse
import os
import stat
import time
import csv
import logging

logging= logging.getLogger(__name__)


def ParseInput():

    #setup a parser using argparse
    parser= argparse.ArgumentParser('Welcome to Pfish Version 1.0')
    parser.add_argument('-v', '--verbose', help= 'allows progress messages to be displayed', action= 'store_true')

    #setup a group for the hash type user would like to generate
    group= parser.add_mutually_exclusive_group(required= True)
    group.add_argument('--md5', help= 'specifies MD5 Algorithm', action= 'store_true')
    group.add_argument('--sha256', help= 'specifies SHA256 Algorithm', action= 'store_true')
    group.add_argument('--sha512', help= 'specifies SHA512 Algorithm', action= 'store_true')

    #to specify the root directory for the program
    parser.add_argument('-d', '--rootPath', type= ValidateDirectory, required= True, help= 'specify the root path for hashing')
    parser.add_argument('-r', '--reportPath', type= ValidateDirectoryWritable, required= True, help= 'specify the path where reports and logs will be written')

    #create a global object to hold the validated arguments
    global gl_args
    global gl_hashType

    #parser is invoked to store the resulting arguments once validated
    gl_args= parser.parse_args()

    '''now as the parser was successful, we determine which hash algorithm the user selected@'''

    if(gl_args.md5):
        gl_hashType= 'MD5'
    elif(gl_args.sha256):
        gl_hashType= 'SHA256'
    elif(gl_args.sha512):
        gl_hashType= 'SHA512'
    else:
        gl_hashType= 'UNKNOWN'
        logging.error('Unknown hash type selected!\n')

    DisplayMessage('Command line processed successfully')
    return


def ValidateDirectoryWritable(theDir):

    #validate if the path is a directory
    if(not os.path.isdir(theDir)):
        raise argparse.ArgumentTypeError('Directory doesn\'t exist')

    #validates if the directory is writable or not
    if(os.access(theDir, os.W_OK)):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory isn\'t writable')
    

def ValidateDirectory(theDir):

    #validate if the path is a directory
    if(not os.path.isdir(theDir)):
        raise argparse.ArgumentTypeError('Directory doesn\'t exist')

    #should be readable
    if(os.access(theDir, os.R_OK)):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory isn\'t readable')


def Walk():

    #returns filecount and logs events simultaneously
    filesCount= 0
    errorCount= 0
    
    logging.info('RootPath: ' + gl_args.rootPath + '\n')

    #next we initialise the csv writer with the reportPath provided by the user(hashType will be included in the header if the csv file created in the reportPath
    opcsv= _CSVWriter(gl_args.reportPath + 'fileSystemReport.csv', gl_hashType)

    for root,dirs,files in os.walk(gl_args.rootPath):
        for file in files:
            #formatting the path of the new file
            fname= os.path.join(root, file)
            #returns boolean
            result= HashFile(fname, file, opcsv)

            if result is True:
                filesCount+= 1
            else:
                errorCount+= 1

    opcsv.writerClose()
    A= []
    A.append(filesCount)
    A.append(errorCount)
    return A


def HashFile(filepath, filename, opcsv):

    #check if the path really exists
    if(os.path.exists(filepath)):
        try:
            #rb denotes the read only option for the open keyword
            f= open(filepath, 'rb')
        except IOError:
            #maybe restricted file or corrupted!
            logging.warning('Open Failed: ' + filepath + '\n')
            return
        else:
            try:
                #attempt to read the file
                rd= f.read()
            except IOError:
                f.close()
                logging.warning('Read Failed: ' + filepath + '\n')
                return
            else:
                filestats= os.stat(filepath)
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)= os.stat(filepath)
                DisplayMessage('Processing file: ' + filepath)

                #processing the values before logging to make them comprehendible
                filesize= str(size)
                modtime= time.ctime(mtime)
                acctime= time.ctime(atime)
                createtime= time.ctime(ctime)
                ownerID= str(uid)
                groupID= str(gid)
                filemode= bin(mode)

                #simple if-else reasonings
                if(gl_args.md5):
                    hashto= hashlib.md5()
                    hashto.update(rd)
                    hexMD5= hashto.hexdigest()
                    hashValue= hexMD5.upper()
                elif(gl_args.sha256):
                    hashto= hashlin.sha256()
                    hashto.update(rd)
                    hexSHA256= hashto.hexdigest()
                    hashValue= hexSHA256.upper()
                elif(gl_args.sha512):
                    hashto= hashlin.sha512()
                    hashto.update(rd)
                    hexSHA512= hashto.hexdigest()
                    hashValue= hexSHA512.upper()
                else:
                    logging.error('Hash-Type not valid\n')

            #always be sure to close the file
            f.close()
            #write to the .csv op file
            opcsv.writeCSVRow(filename, filepath, filesize, modtime, acctime, createtime, hashValue, ownerID, groupID, filemode)
            return True
    else:
        logging.warning(filepath + ' Path doesn\'t exist\n')
        return False


def DisplayMessage(msg):

    if(gl_args.verbose):
        print(msg)

    return



class _CSVWriter:

    #init method initialisation
    def __init__(self, filepath, hashType):
        try:
            #create a writer object and write the header row
            self.csvfile= open(filepath, 'wb')
            self.writer= csv.writer(self.csvfile, delimiter= ',', quoting= csv.QUOTE_ALL)
            self.writer.writerow('File', 'Path', 'Size', 'Modified time', 'Access time', 'Created time', hashType, 'Owner', 'Group', 'Mode')
        except:
            #failure occurs and file isnt able to be writed
            logging.error('CSV File Failure\n')


    def writeCSVRow(self, filename, filepath, filesize, modtime, acctime, createtime, hashValue, owner, group, mode):
        self.writer.writerow((filename, filepath, filesize, modtime, acctime, createtime, hashValue, owner, group, mode))


    def writerClose(self):
        self.csvfile.close()
    

    



    
    
