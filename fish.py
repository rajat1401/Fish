import sys
import logging
import time
import _fish

if __name__== '__main__':
    FISH_VERSION= '1.0'

    #Turn on Logging
    logging.basicConfig(filename= 'FishLog.log', level= logging.DEBUG, format= '%(asctime)s %(message)s', datefmt= '%d/%m/%Y %H/%M/%S %p')
    #set the logging level to debug to ensure all messages sent to logger be visible

    #Process the inputs
    _fish.ParseInput()

    #start recording time
    startTime= time.time()

    #signify the starting of the log
    logging.info('Welcome to Fish Version' + FISH_VERSION + '... Scan started!\n')
    _fish.DisplayMessage('Welcome to the Fish Version' + FISH_VERSION)
    
    logging.info('System: ' + sys.platform + '\n')
    logging.info('Platform: ' + sys.version + '\n')

    #traverse the directories and hash the files
    A= _fish.Walk()

    endTime= time.time()
    duration= endTime-startTime

    logging.info('Files Processed: ' + str(A[0]) + '\n')
    logging.info('Files Failed: ' + str(A[1]) + '\n')
    logging.info('Elapsed time: ' + str(duration) + ' seconds\n')

    #terminates the program.
    logging.info('Program Terminated!!!\n')
    _fish.DisplayMessage('Program Execution ends') 

    
