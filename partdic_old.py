import os
import platform
#import mathutils



    
def cheaters_probe(path):
#The path must be the directory path for KSP not the .exe path, eg: "C:\\ksp-090\KSP" not ""C:\\ksp-090\KSP\KSP.exe"
#otherwise it won't find anything
#This function is for finding all the .cfg. Cheating because an already made function is used
    cfgs=[]
    for p,d,f in os.walk(os.path.join(path,"GameData")): #os.walk creates the list of dirs, subdirs and files <- Cheating :p
        for i in f:
            if ".cfg" in i and "Parts" in p: #Select the files needed for later
                cfgs.append((p,i))
    return(cfgs)
    
def cheaters_probe_large(path):
#This one is for the mod which don't have a 'Parts' folder, but it will pick useless .cfg files too 
    cfgs=[]
    for p,d,f in os.walk(os.path.join(path,"GameData")): #os.walk creates the list of dirs, subdirs and files <- Cheating :p
        for i in f:
            if ".cfg" in i: #Select the files needed for later
                cfgs.append((p,i))
    return(cfgs)
    
    
def make_dic(cfgs,kspdir): #This function is the one making the dic
    if platform.system() == 'Windows': #Thanks Dasoccerguy for that part :)
        sep = "\\" #The path separator to use, used just one time 
    else:
        sep = "/"
        
    partdir = {}
    right_loc = {}
    right_scale = {}
    for part_tuple in cfgs: #Search in each .cfg
        path,cfg=part_tuple
        part_name = ""
        pos = (0,0,0)
        scale=(0,0,0)
        rescale_fact = 1
        f=open(os.path.join(path,cfg))
        part_path = ""
        got_path = False
        got_name = False
        got_rescale = False
        got_scale = False
        got_pos = False
        got_cat = False
        category = "part"
        for line in f: #Looks for the name,scale,... in a .cfg
            if "name =" in line and not(got_name):
                part_name=line.split()[-1]
                got_name= True
            if "rescaleFactor = " in line and not(got_rescale):
                rescale_fact = float(line.split()[-1])
                got_rescale= True
            if ("scale =" in line) and not(got_scale):
                line = line.replace(","," ")
                line_in=line.strip().split()
                if len(line_in) == 3: #For lines : scale  = 22
                    sc = float(line_in[-1])
                    scale= (sc,sc,sc)
                    got_scale = True
                if len(line_in) == 5: #For lines : scale = 22,10,50
                    line = line.replace(","," ") 
                    x,y,z=line_in[-3:]
                    scale = (float(x),float(y),float(z))
                    got_scale = True
            if "position =" in line and not(got_pos):
                line = line.replace(","," ")
                x,y,z=line.strip().split()[-3:]
                pos = (float(x),float(y),float(z))
                got_pos=True
            if "category =" in line and not(got_cat):
                category = line.split()[-1]
                got_cat=True
            if "model =" in line and not(got_path):
                part_path = line.split()[-1]
                part_path = part_path.replace("/",sep) #The sep is used here
                part_path = os.path.join(os.path.join(kspdir,"GameData"),part_path)+".mu"
                got_path= True
            if "mesh =" in line and not(got_path):
                part_path = line.split()[-1]
                part_path = os.path.join(path,part_path)
                got_path = True
                
        f.close()      
        if got_name: #Adds the part to the dic if the the name was acquired
            partdir[part_name] = [os.path.join(part_path),category]
            if got_scale and got_rescale:
                x,y,z=scale
                x*=rescale_fact
                y*=rescale_fact
                z*=rescale_fact 
                right_scale[part_name] = ((x,y,z)) #Change to Vector((x,y,z)) when importing to blender
            if got_rescale and not(got_scale):
                right_scale[part_name] = ((rescale_fact,rescale_fact,rescale_fact)) #Same here
            if got_scale and not(got_rescale):
                right_scale[part_name] = (scale)   #Here again
            if got_pos:
                right_loc[part_name] = (pos) #And finally here
    return(partdir,right_scale,right_loc)
    

#To create the dictionnaries:
#a=cheaters_probe(kspdir)
#parts,right_sc,right_loc=make_dic(a,kspdir)
