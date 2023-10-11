from Google import Create_Service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)



class_name = input("What's the class called?\n")


# Retrieves out the amount of assignments in the class
assignments = input("Does the class have assignments? (type 'yes' or 'no')\n")
assignment_number = 0
out = False
while assignments != "yes" and assignments != "no":
    assignments = input("type 'yes' or 'no'\n")
if assignments == "yes":
    while out == False:
        num_in = input("How many assignments? (integer > 0)\n")
        try:
            assignment_number = int(num_in)
            if assignment_number > 0:
                out = True
        except Exception as e:
            print (e)

# Retrieves the lecture frequency
out = False
lecture_frequency = 0
while out == False:
    num_in = input("How many lectures are there a week? (integer>0 and <5)\n")
    try:
        lecture_frequency = int(num_in)
        if lecture_frequency > 0 and lecture_frequency < 5:
            out = True
    except Exception as e:
        print (e)

while out == True:
    term = input("which term is this class being taken in?(type 'f', 'w' or 's')\n")
    if term in {'f','w','s'} :
        out = False

create_id_request = service.files().generateIds(count=3,).execute()
folder_id = create_id_request.get('ids')

# Creates the master folder for the class
create_class_folder_request = {
    'name': class_name,
    'mimeType': 'application/vnd.google-apps.folder', 
    'id':folder_id[0],
}

service.files().create(supportsAllDrives=True,body=create_class_folder_request).execute()

# Creates a master assignments folder with a subfolder for each individual assignment
if assignment_number > 0:
    create_master_assignments_folder_request = {
        'name':'Assignments',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id[0]],
        'id':folder_id[1],
    }

    service.files().create(supportsAllDrives=True,body=create_master_assignments_folder_request).execute()

    create_id_request_2 = service.files().generateIds(count=assignment_number,).execute()
    folder_id_2 = create_id_request_2.get('ids')

    for i in range(assignment_number):
        create_assignment_folder_request = {
        'name':'AS'+ str(i+1),
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id[1]],
        'id':folder_id_2[i],
        }

        service.files().create(supportsAllDrives=True,body=create_assignment_folder_request).execute()

# Creates a folder for each lectures notes
create_master_notes_folder_request = {
    'name':'Notes',
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': [folder_id[0]],
    'id':folder_id[2],
}
service.files().create(supportsAllDrives=True,body=create_master_notes_folder_request).execute()

# A typical school semester lasts 13 weeks
counter = 13

# Creates folders for each weeks lecture notes
for i in range (counter):
    create_id_request_3 = service.files().generateIds(count=(lecture_frequency),).execute()
    folder_id_3 = create_id_request_3.get('ids')

    for x in range(lecture_frequency):
        if term == 'f' and x==0 and i==0:
            continue
        else:
            create_notes_folder_request = {
            'name':'Week '+ str(i+1)+": Lecture "+ str(x+1),
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [folder_id[2]],
            'id':folder_id_3[x],
            }
            service.files().create(supportsAllDrives=True,body=create_notes_folder_request).execute()




'''
id = '1ZjvZkvRRuPDjotaFzfOo3kPFByyG0Fgt'
query = f"parents = '{id}'"
create_folder_list = service.files().list(includeItemsFromAllDrives=True,supportsAllDrives=True, q=query).execute()
folders = create_folder_list.get('files')
nextPageToken = create_folder_list.get('nextPageToken')

while nextPageToken:
    create_folder_list = service.files().list(includeItemsFromAllDrives=True,supportsAllDrives=True, q=query, pageToken=nextPageToken).execute()
    folders.extend(create_folder_list.get('files'))
    nextPageToken = create_folder_list.get('nextPageToken')



folder_id_list=[]
folder_name_list=[]
for folder in folders:
    to_Str = str(folder)
    folder_id_list.append(to_Str[114:147])

    new_Str = to_Str[159:]
    folder_name_list.append(new_Str.split("'")[0])

len = len(folder_name_list)

create_id_request_2 = service.files().generateIds(count=len,).execute()
folder_id_2 = create_id_request_2.get('ids')

for sourceFolderId, folderName, folderId in zip(folder_id_list,folder_name_list, folder_id_2):
    if '(Client Name)' in folderName:
        folderName = folderName.replace('(Client Name)', companyName)

    create_folder_request = {
        'name': folderName,
        'mimeType': 'application/vnd.google-apps.folder', 
        'parents': [folder_id[1]],
        'id': folderId,
    }
    service.files().create(supportsAllDrives=True,body=create_folder_request).execute()


    #cycles through content
    qu = f"parents = '{sourceFolderId}'"
    create_file_list = service.files().list(includeItemsFromAllDrives=True,supportsAllDrives=True, q=qu).execute()
    files = create_file_list.get('files')
    nxtPageToken = create_file_list.get('nextPageToken')

    while nxtPageToken:
        create_file_list = service.files().list(includeItemsFromAllDrives=True,supportsAllDrives=True, q=qu, pageToken=nxtPageToken).execute()
        files.extend(create_file_list.get('files'))
        nxtPageToken = create_file_list.get('nextPageToken')
    

    file_id_list=[]
    file_name_list=[]

    for file in files:
        toStr = str(file)
        newStr_1 = toStr.split("'id': '")[1]
        file_id_list.append(newStr_1.split("'")[0])

        newStr_2 = toStr.split("'name': '")[1]
        file_name_list.append(newStr_2.split("'")[0])


    for file_Id, fileName in zip(file_id_list,file_name_list):
        if '(Client Name)' in fileName:
            fileName = fileName.replace('(Client Name)', companyName)

        copy_files = {
            'name': fileName,
            'parents': [folderId]
        }

        service.files().copy(
            fileId=file_Id,
            supportsAllDrives=True,
            body=copy_files
        ).execute()
  '''
