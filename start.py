#!/usr/bin/env python3

import urllib.request

import subprocess 

import os
import sys
import ssl



from io import BytesIO
from zipfile import ZipFile







def isWritable(path):
    try:
        filename  = os.path.join(path, '___is_path_writable.txt')
        f = open(filename,"w")
        f.write("bla bla bla")
        f.close()
        
        
        ret = (open(filename, "r").read().strip() == "bla bla bla")
        
        os.remove(filename)
        return ret
    except:
        return False

def getMinerDir():


    try:
        if os.name == 'nt':   
            profile_dir = os.path.abspath(os.environ['USERPROFILE'])         
        elif os.name == 'posix':    
            profile_dir = os.path.abspath(os.path.expanduser('~')) 
        else:
            profile_dir = ""        
    except:
        profile_dir = ""

        
    if profile_dir != "":
        try:
            os.mkdir(profile_dir)
        except:
            pass
        
    gpuminer_dir = os.path.join(profile_dir,"ocvcoin_gpuminer")

    try:
        os.mkdir(gpuminer_dir)
    except:
        pass
        
    if isWritable(gpuminer_dir):
        return gpuminer_dir
    elif isWritable(""):  
        return ""
    else:
        return False


def runMiner(miner_file):

    cd = os.path.dirname(os.path.abspath(__file__))
    
        
    py_bin = None
    if os.name == 'nt':
    
    
    
        if os.environ['PROCESSOR_ARCHITECTURE'] == "AMD64":
            #Running under 64-bit EXE on 64-bit Windows...
            file = os.path.join(cd,"python-3.6.0-embed-amd64","python.exe")
            if os.path.exists(file):
                py_bin = file
        else:

            if os.environ['PROCESSOR_ARCHITECTURE'] == "x86" and "PROCESSOR_ARCHITEW6432" in os.environ and os.environ["PROCESSOR_ARCHITEW6432"] == "AMD64":
                #Running under 32-bit EXE on 64-bit Windows...
                file = os.path.join(cd,"python-3.6.0-embed-amd64","python.exe")
                if os.path.exists(file):
                    py_bin = file
            else:
                #Running under 32-bit EXE on 32-bit Windows...
                file = os.path.join(cd,"python-3.6.0-embed-win32","python.exe")
                if os.path.exists(file):
                    py_bin = file    
    
    
    
    
    
    
        
        if py_bin != None:
            
            subprocess.call([py_bin,miner_file])
        else:
            if os.system('py -3.6 -V') != 0:                
                subprocess.call(["py","-3",miner_file])
            else:                
                subprocess.call(["py","-3.6",miner_file])
            
    
    else:        
        subprocess.call(["python3",miner_file])
        
    
 
    sys.exit()


if __name__ == "__main__":

    cd = os.path.dirname(os.path.abspath(__file__))
    MINER_DIR = getMinerDir()
    
    if MINER_DIR != False:
        EXTRACT_SUCCEED_FILE = os.path.join(os.path.join(MINER_DIR, 'gpuminer-main'), 'extract_succeed.txt')


    try:
    
        if MINER_DIR == False:
            raise Exception("no miner dir!")

        BUILT_IN_MINER_VERSION = open(os.path.join(MINER_DIR, 'gpuminer-main',"version.txt"), "r").read().strip()
        BUILT_IN_MINER_FILE = os.path.join(MINER_DIR, 'gpuminer-main',"ocvcoin_miner.py")
        if not os.path.exists(EXTRACT_SUCCEED_FILE):
            raise Exception("no succeed file!")
        
    except:
        
        try:

            BUILT_IN_MINER_VERSION = open(os.path.join(cd,"gpuminer-main","version.txt"), "r").read().strip()
            BUILT_IN_MINER_FILE = os.path.join(cd, 'gpuminer-main',"ocvcoin_miner.py")
            
        except:
            
            print("\nbuilt-in miner not found!\n")
            sys.exit()
    
    



    CA_CERT_FILE = os.path.join(cd,"cacert.pem")
    GLOBAL_SSL_CONTEXT = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    GLOBAL_SSL_CONTEXT.load_verify_locations(CA_CERT_FILE)

    
    try:           
        request = urllib.request.Request("https://raw.githubusercontent.com/ocvcoin/gpuminer/main/version.txt")                
        f = urllib.request.urlopen(request,timeout=5,context=GLOBAL_SSL_CONTEXT)
        LATEST_VERSION = f.read().decode('ascii').strip()
    except:
        LATEST_VERSION = None
    
    if BUILT_IN_MINER_VERSION == LATEST_VERSION or LATEST_VERSION == None:
        runMiner(BUILT_IN_MINER_FILE)
    
    else:
    
    
        
    
        if MINER_DIR == False:
            runMiner(BUILT_IN_MINER_FILE)
        
        else:

            if not sys.__stdin__.isatty():
                runMiner(BUILT_IN_MINER_FILE)
                
                
            user_input = input("\nA new version is available!\nWould you like to use the latest version?(YES/no):\n")
            if user_input.lower().strip() not in ["yes", "y",""]:
                runMiner(BUILT_IN_MINER_FILE)    

               
            new_file = None

            try:
            
            
                if os.path.exists(EXTRACT_SUCCEED_FILE):
                    os.remove(EXTRACT_SUCCEED_FILE)            
            
            
            
            
                zipurl = 'https://github.com/ocvcoin/gpuminer/archive/refs/heads/main.zip'
                with urllib.request.urlopen(zipurl,timeout=10,context=GLOBAL_SSL_CONTEXT) as zipresp:
                    with ZipFile(BytesIO(zipresp.read())) as zfile:
                        if zfile.testzip() is None:
                        
                        
                            is_safe_file = True
                            zipfile_contents = zfile.namelist()
                            for _filename in zipfile_contents:
                                if _filename.startswith('gpuminer-main/') != True:
                                    is_safe_file = False
                                    break
                            
                            if is_safe_file:                          
                        
                                zfile.extractall(MINER_DIR) 
                                new_file = os.path.join(os.path.join(MINER_DIR, 'gpuminer-main'), 'ocvcoin_miner.py') 
                                
                                if os.path.exists(new_file) and os.path.getsize(new_file) > 0:

                                    
                                    f = open(EXTRACT_SUCCEED_FILE, "w")
                                    f.write("OK!")
                                    f.close()

                                else:
                                    new_file = None
                                
                                    
            except:
                new_file = None

            if new_file == None:
                runMiner(BUILT_IN_MINER_FILE)
            else:
                runMiner(new_file)



