import requests, shutil, json, os

#Please disable SSL for Hololens and connect your hololens directly to your pc via USB
username = "test"
password = "test"
packageName = "7A37D94C-C432-4875-8C57-FA185E1C92B4"
connectionHost = "127.0.0.1:10080"
folder = "./outputs"

def createFolder(folderName):
    ret = False
    if not os.path.exists(folderName):
        os.makedirs(folderName)
        ret = True
    elif(os.path.exists(folderName)):
        ret = True
    return ret

def downloadToFolder(fileName, filePath, folderName):
    global username, password, packageName, connectionHost
    ret = False
    request_url = "http://"+username+":"+password+"@"+connectionHost+"/api/filesystem/apps/file?knownfolderid=LocalAppData&filename="+fileName+"&packagefullname="+packageName+"&path="+filePath

    r = requests.get(request_url, stream=True)
    if r.status_code == 200:
        file_name = folderName+os.path.sep+fileName
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        ret = True
    return ret

def downloadAllFiles(path, folder):
    json_data = ''
    if(createFolder(folder)):
        file_list_url = "http://"+username+":"+password+"@"+connectionHost+"/api/filesystem/apps/files?knownfolderid=LocalAppData&packagefullname="+packageName+"&path="+path
        r = requests.get(file_list_url, stream=True)
        if r.status_code == 200:
            file_name = folder+os.path.sep+'filelist.txt'
            with open(file_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f) 

            with open(file_name) as json_file_data:
                json_data = json.load(json_file_data)
            items = json_data['Items']
            for jData in items:
                if(jData['Type']==32):
                    tempFileDir = jData['CurrentDir']
                    tempFileName = jData['Name']
                    downloadToFolder(tempFileName, tempFileDir, folder)
                elif(jData['Type']==16):
                    tempFolderName = folder+os.path.sep+jData['Name']
                    if(createFolder(tempFolderName)):
                        downloadAllFiles(jData['SubPath'], tempFolderName)

downloadAllFiles("\\\\TempState", folder)