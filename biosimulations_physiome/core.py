import requests
import os 
import zipfile
FULL_LIST= "https://staging.physiomeproject.org/exposure/listing/full-list"

def importProjects():
    """
    Imports all the projects in the database
    """
    links = getProjectsList()
    for link in links:
        print(link)
        #project = getProject(link)
        
        try:
            archive= getProjectArchive(link)
        except: 
            name = link.split('/')[-1]
            print(f'Error getting project {name}')
            continue
        
        

def getProjectArchive(link):
    name= link.split('/')[-1]
    os.makedirs(f'archives/{name}', exist_ok=True)

    req = requests.get(f'{link}/download_generated_omex',headers={'Accept': 'application/zip'})
    req.raise_for_status()
    with open(f'archives/{name}/{name}.omex','wb') as f:
        f.write(req.content)
    
    with zipfile.ZipFile(f'archives/{name}/{name}.omex') as zip_ref:
        zip_ref.extractall(f'archives/{name}')
    
    
    

    print(link)

def getProjectsList():
    """
    Returns a list of all the projects in the database
    """
    req = requests.get(FULL_LIST,headers={'Accept': 'application/json'})
    print(req.status_code)
    links = req.json()['collection']["links"]
    
    links = list(map(lambda x: x['href'], links))


    return links

def getProject(link):
    """
    
    """
    req = requests.get(link,headers={'Accept': 'application/json'})
    
    info = req.json()['collection']['href']
    req= requests.get(info,headers={'Accept': 'application/json'})
    
    
    return req.json()


    