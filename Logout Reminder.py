#Logout Reminder
#github.com/smcclennon/Logout-Reminder
build=4


print('Importing requirements...')
import time,string,os,socket,getpass
from ctypes import windll
from random import randint
from pathlib import Path

windll.kernel32.SetConsoleTitleW('Logout Reminder - Build '+str(build)) #Set console window title

def cmd(x):
    os.system(str(x))
def sleep(x):
    time.sleep(x)
def asciiRaw():
    print('''  _                             _     _____                _           _
 | |                           | |   |  __ \              (_)         | |
 | |     ___   __ _  ___  _   _| |_  | |__) |___ _ __ ___  _ _ __   __| | ___ _ __
 | |    / _ \ / _` |/ _ \| | | | __| |  _  // _ \ '_ ` _ \| | '_ \ / _` |/ _ \ '__|
 | |___| (_) | (_| | (_) | |_| | |_  | | \ \  __/ | | | | | | | | | (_| |  __/ |
 |______\___/ \__, |\___/ \__,_|\__| |_|  \_\___|_| |_| |_|_|_| |_|\__,_|\___|_|
               __/ |''')
    print('              |___/                                                    Build '+str(build)+'\n')
def display():
    cmd('cls')
    asciiRaw()
computer=str(socket.gethostname())
username=str(getpass.getuser())
driveArray = [] #Search for drives
bitmask = windll.kernel32.GetLogicalDrives()
for letter in string.ascii_uppercase:
    if bitmask & 1:
        driveArray.append(letter)
    bitmask >>= 1

#You can customise this!
defaultMsg='You forgot to logout of '+computer+'!\nThis is a friendly reminder that you should probably do that next time.'


def setupMessage():
    display()
    print('Computer: '+computer)
    print('Username: '+username)
    print('\nEnter your custom message: (leave blank to skip)')
    global customMessage
    customMessage=input(str('> '))
    confirmMessage()

def confirmMessage():
    display()
    global msg
    if customMessage=='':
        print('Custom Message: Disabled')
        msg=defaultMsg
        print('\n______ Message ______\n\n'+msg+'\n\n______ Message ______\n')
    else:
        print('Custom Message: Enabled')
        msg=defaultMsg+'\n\nCustom Message:\n'+customMessage
        print('\n______ Message ______\n\n'+msg+'\n\n______ Message ______\n')
    confirm=input(str('\nConfirm? [Y/n] ')).upper()
    if confirm=='Y':
        setupDrive()
    else:
        setupMessage()

def setupDrive():
    display()
    print('Available Drives:')
    i=0
    for x in driveArray:
        i=i+1
        print('{}. {}'.format(i,str(x))) #format what {} values are
    print('\nPlease type the drive letter you wish to select (leave blank to go back)')
    global selectedDrive
    selectedDrive=input(str('> ')).upper()
    if selectedDrive=='':
        setupMessage()
    if not selectedDrive in driveArray:
        print('Specified drive not found. Please try again.')
        sleep(1)
        setupDrive()
    else:
        confirmDrive()

def confirmDrive():
    display()
    print('Selected Drive: '+selectedDrive)
    time.sleep(0.5)
    confirm=input(str('Confirm? [Y/n] ')).upper()
    if confirm=='Y':
        confirmWrite()
    else:
        setupDrive()

def confirmWrite():
    display()
    print('Computer: '+computer)
    print('Username: '+username)
    if customMessage=='':
        print('Custom Message: Disabled')
    else:
        print('Custom Message: Enabled')
    print('Selected Drive: '+selectedDrive)
    print('\n______ Message ______\n'+msg+'\n______ Message ______\n')
    time.sleep(1)
    print('\nYou are about to flood all subdirectories in ['+selectedDrive+':\\]!')
    time.sleep(0.5)
    confirm=input(str('Are you sure? [Y/n] ')).upper()
    if confirm=='Y':
        commitWrite()
    else:
        setupDrive()

def commitWrite():
    rand=randint(10000,99999) #Create a random number for confirmation and filenames
    display()
    print('\nSelected Drive: '+selectedDrive+'\n\nTo begin flooding, please type this confirmation code: '+str(rand))
    confirm=input(str('\n>>> '))
    if confirm!=str(rand):
        confirmWrite()
    removalMsg='\n\n\n\nInstructions to remove the files:\n\nAutomatic:\n1. Navigate to "'+selectedDrive+':\\"\n2. Run "Removal Tool ['+str(rand)+'].py"\n\nManual:\n1. Navigate to "'+selectedDrive+':\\"\n2. Search for "READ_ME ['+str(rand)+']"\n3. Select everything and delete'
    removalScriptP1='#Logout Reminder: Removal Tool\n#github.com/smcclennon/Logout-Reminder\nBuild='+str(build)+'\nrand='+str(rand)
    removalScriptP2='''
import os,glob
from ctypes import windll
windll.kernel32.SetConsoleTitleW('Logout Reminder: Removal Tool - Build '+str(build))
y=str(os.getcwd()[0].upper())
filenameEstimate='READ_ME ['+str(rand)
scriptnameEstimate='Removal Tool ['+str(rand)
i=0
for x in glob.glob(str(os.getcwd()[0].upper())+':\\*'+filenameEstimate+'**.txt'):
    try:
        os.remove(str(x))
        i=i+1
        print(str(i)+'. Deleted: '+str(x))
    except OSError:
        print('[FAILED]: '+str(x))
for x in glob.glob(str(os.getcwd()[0].upper())+':\\**\\**'+filenameEstimate+'**.txt'):
    try:
        os.remove(str(x))
        i=i+1
        print(str(i)+'. Deleted: '+str(x))
    except OSError:
        print('[FAILED]: '+str(x))
for x in glob.glob(str(os.getcwd()[0].upper())+':\\*'+scriptnameEstimate+'**.py'):
    try:
        os.remove(str(x))
        i=i+1
        print(str(i)+'. Deleted: '+str(x))
    except OSError:
        print('[FAILED]: '+str(x))
print('\n\nFile cleanup complete!')
os.system('timeout 3')'''
    
    global i
    global start
    i=0
    print('\nCreating files...')
    start=time.time() #take note of the current time
    for x in Path(selectedDrive+':/').glob('**'):
        if i==0:
            try:
                filename='Removal Tool ['+str(rand)+'].py'
                f=open(str(x)+'\\'+filename, 'w')
                f.write(removalScriptP1)
                f.write(removalScriptP2)
                i=i+1
                print(str(i)+'. Created: '+str(x)+'\\'+filename)
                f.close()
            except:
                print('[FAILED: REMOVAL SCRIPT]: '+str(x)+'\\'+filename)
                print('***Failed to create removal script!***')
        try:
            filename='READ_ME ['+str(rand)+'] [#'+str(i)+'].txt'
            f=open(str(x)+'\\'+filename, 'w')
            f.write(msg+removalMsg)
            f.close()
            i=i+1
            print(str(i)+'. Created: '+str(x)+'\\'+filename)
        except:
            print('[FAILED]: '+str(x)+'\\'+filename)
    
    global taken
    taken=time.time()-start #calculate how long the operation took

#Run the script
setupMessage() #Start at the setupMessage module
print('\n')
asciiRaw()
print('Created '+str(i)+' files in '+str(round(taken, 2))+' seconds!\nPress any key to exit...')
cmd('pause>nul')
