
import os
import platform

def make_exceptions():
    exceptions = {}
    #The exceptions dict is for the mod that don't have the same naming convention
    #in the .cfg and in the .craft. The structure of the dic is like this
    #
    #          'mod name'         'folder name'  replace rule
    exceptions['B9 Aerospace'] = ('B9_Aerospace',('_','.'))
    exceptions['B9 Style Shuttle Wings'] = ('GilB9Shuttle_Wings',('_','.'))
    #add more as necessary when mods inevitably fail
    return exceptions


#In the following functions p is for part,... rs for right_scale and rl for right_loc
def make_dict(path):
    cfgs = probe_large(path)
    p,rs,rl = make_dict_aux(cfgs,path)
    #exceptions = make_exceptions()
    #exceptions_manager(p,rl,exceptions)
    return(p,rl)
    
def make_dict_with_rs(path):
    cfgs = probe_large(path)
    p,rs,rl = make_dict_aux(cfgs,path)
    #exceptions = make_exceptions()
    #exceptions_manager(p,rs,rl,exceptions)
    return(p,rs,rl)

    
    
def probe(path):
#The path must be the directory path for KSP not the .exe path, eg: "C:\\ksp-090\KSP" not ""C:\\ksp-090\KSP\KSP.exe"
#otherwise it won't find anything
#This function is for finding all the .cfg.
    cfgs=[]
    for p,d,f in os.walk(os.path.join(path,"GameData")): #os.walk creates the list of dirs, subdirs and files
        for i in f:
            if ".cfg" in i and "Parts" in p: #Select the files needed for later
                cfgs.append((p,i))
    return(cfgs)
    
def probe_large(path):
#This one is for the mod which don't have a 'Parts' folder, but it will pick useless .cfg files too 
    cfgs=[]
    for p,d,f in os.walk(os.path.join(path,"GameData")): #os.walk creates the list of dirs, subdirs and files
        for i in f:
            if ".cfg" in i: #Select the files needed for later
                cfgs.append((p,i))
    return(cfgs)
    
    
def make_dict_aux(cfgs,kspdir): #This function is the one making the dict
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
        scale=(1,1,1)
        rescale_fact = 1.25
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
#                if len(line_in) == 3: #For lines : scale  = 22
#                    sc = float(line_in[-1])
#                    scale= (sc,sc,sc)
#                    got_scale = True
                if len(line_in) == 5: #For lines : scale = 22,10,50
                    line = line.replace(","," ") 
                    sx,sy,sz=line_in[-3:]
                    scale = (float(sx),float(sy),float(sz))
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
                if ".DAE" in part_path or ".dae" in part_path:
                    part_path = "model.mu"                  # or at least I hope so
                part_path = os.path.join(path,part_path)
                got_path = True
                
        f.close()      
        if got_name: #Adds the part to the dict if the the name was acquired
            partdir[part_name] = [os.path.join(part_path),category]
            if not(got_rescale) and not(got_scale):
                right_scale[part_name]= (1.25,1.25,1.25)
            if not(got_rescale) and got_scale:
                right_scale[part_name]= scale
            if got_rescale and not(got_scale):
                right_scale[part_name]= (rescale_fact,rescale_fact,rescale_fact)
            if got_rescale and got_scale:
                sx,sy,sz=scale
                sx*=rescale_fact
                sy*=rescale_fact
                sz*=rescale_fact
                right_scale[part_name]= (sx,sy,sz)
            if got_pos:
                right_loc[part_name] = pos
    return(partdir,right_scale,right_loc)


         
def exceptions_manager(partdir,rs,rl,exceptions):
#def exceptions_manager(partdir,rl,exceptions):
    def add_to_dir(modif_list,dic):
        for modif in modif_list:
            dic[modif[0]]=modif[1]
        return(dic)
    def del_from_dir(modif_list,dic):
        for modif in modif_list:
            del dic[modif]
        return(dic)
    p_del = []
    p_add = []
    rs_del= []
    rs_add= []
    rl_del= []
    rl_add= []
    for mod in exceptions:
        direc=exceptions[mod][0]
        rule=exceptions[mod][1]
        for part in partdir:
            if direc in partdir[part][0]:
                new_name= part.replace(rule[0],rule[1])
                p_add.append((new_name,partdir[part]))
                p_del.append(part)
                if part in rs:
                    rs_add.append((new_name,rs[part]))
                    rs_del.append(part)
                if part in rl:
                    rl_add.append((new_name,rl[part]))
                    rl_del.append(part)
    add_to_dir(p_add,partdir)
    add_to_dir(rs_add,rs)
    add_to_dir(rl_add,rl)
    del_from_dir(p_del,partdir)
    del_from_dir(rs_del,rs)
    del_from_dir(rl_del,rl)
    return()
