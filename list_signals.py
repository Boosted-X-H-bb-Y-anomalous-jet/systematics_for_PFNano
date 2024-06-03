import subprocess
import matplotlib.pyplot as plt
import numpy as np

class Masspoint:
    def __init__(self, mx, my):
        self.mx = int(mx)
        self.my = int(my)
        self.folder2016APV = ""
        self.folder2016 = ""
        self.folder2017 = ""
        self.folder2018 = ""

    def set_folder(self, folder_type, folder_name):
        if folder_type == "2016APV":
            if self.folder2016APV != "":
                print("EXITING: Duplicate folder: ", self.folder2016APV, folder_name)
                exit()
            self.folder2016APV = folder_name
        elif folder_type == "2016":
            if self.folder2016 != "":
                print("EXITING: Duplicate folder: ", self.folder2016, folder_name)
                exit()
            self.folder2016 = folder_name
        elif folder_type == "2017":
            if self.folder2017 != "":
                print("EXITING: Duplicate folder: ", self.folder2017, folder_name)
                exit()
            self.folder2017 = folder_name
        elif folder_type == "2018":
            if self.folder2018 != "":
                print("EXITING: Duplicate folder: ", self.folder2018, folder_name)
                exit()
            self.folder2018 = folder_name
        else:
            print("Invalid folder type")

    def count_non_empty_folders(self):
        count = 0
        if self.folder2016APV != "":
            count += 1
        if self.folder2016 != "":
            count += 1
        if self.folder2017 != "":
            count += 1
        if self.folder2018 != "":
            count += 1
        return count

def year_from_path(path):
    if "2016APV" in path:
        return "2016APV"
    elif "2016" in path:
        return "2016"
    elif "2017" in path:
        return "2017"
    elif "2018" in path:
        return "2018"
    else:
        print("Invalid folder: ", path)
        return "-1"

def mass_points_in_folder(store_path,massPoints):
    fNames  = subprocess.check_output(['{} {}'.format(eosls,store_path)],shell=True,text=True).split('\n')
    fNames.remove('')
    for fName in fNames:
        year = year_from_path(store_path)
        mx = fName.split("MX")[1].split("_")[0].strip("-")#Format is either ..._MX2400_MY100... or ..._MX-2400_MY-100...
        my = fName.split("MY")[1].split("_")[0].strip("-")
        mxmy=f"MX{mx}_MY{my}"
        if mxmy in massPoints:
            massPoints[mxmy].set_folder(year, f"/eos/uscms/{store_path}/{fName}")
        else:
            massPoint = Masspoint(mx,my)
            massPoint.set_folder(year, f"/eos/uscms/{store_path}/{fName}")
            massPoints[mxmy] = massPoint

def plot_mass_points(massPoints):
    x_coords = []
    y_coords = []
    for key in massPoints:
        massPoint = massPoints[key]
        nYears = massPoint.count_non_empty_folders()
        if nYears!=4:
            continue
        x_coords.append(massPoint.mx)
        y_coords.append(massPoint.my)
    plt.scatter(x_coords, y_coords)
    plt.xlabel('MX')
    plt.ylabel('MY')
    plt.grid(True)

    x_values = np.linspace(min(x_coords), max(x_coords), 100)
    y_values = 1./6. * x_values + 125./6.
    plt.plot(x_values, y_values, color='red')

    plt.savefig("signal_grid.png")
    plt.savefig("signal_grid.pdf")

def get_rootfiles_path(folder):
    fNames  = subprocess.check_output(['{} {}'.format(eosls,folder)],shell=True,text=True).split('\n')
    fNames.remove('')
    if any(fname.endswith(".root") for fname in fNames):
        return folder
    else:
        sub_folder = fNames[0]#We assume that there will only be one!
        new_folder = f"{folder}/{sub_folder}"
        return get_rootfiles_path(new_folder)

#ls path: /eos/uscms/
eosls ="eos root://cmseos.fnal.gov ls"

if __name__ =="__main__":
    dirs = [
    #"/store/group/lpcpfnano/ammitra/v2_3/2017/XHYPrivate",
    "/store/group/lpcpfnano/ammitra/v2_3/2017/XHY",
    #"store/group/lpcpfnano/cmantill/v2_3/2017/XHYPrivate",
    "store/group/lpcpfnano/cmantill/v2_3/2018/XHY",
    "store/group/lpcpfnano/rkansal/v2_3/2016/XHY",
    "store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY",
    #"store/group/lpcpfnano/rkansal/v2_3/2017/XHYPrivate",   
    "store/group/lpcpfnano/rkansal/v2_3/2018/XHY"   
    ]

    massPoints = {}
    string_2016APV = ""
    string_2016 = ""
    string_2017 = ""
    string_2018 = ""

    for dir in dirs:
        mass_points_in_folder(dir,massPoints)

    for key in massPoints:
        massPoint = massPoints[key]
        nYears = massPoint.count_non_empty_folders()
        if nYears!=4:
            continue
        mx = massPoint.mx
        my = massPoint.my
        #Boosted criterion, based on pT > 2m/R, where R=0.8
        #pT is approximated as (MX-MY-MH)/2.
        if my > (1./6. * mx + 125./6.):
            continue

        if my!=90:#Just processing 90 GeV for now
            continue

        if mx<1200.:#We have a MJJ cut of 1100
            continue
        
        p = get_rootfiles_path(massPoint.folder2016APV)
        string_2016APV+=f'"MX{mx}_MY{my}":"{p}",\n'

        p = get_rootfiles_path(massPoint.folder2016)
        string_2016+=f'"MX{mx}_MY{my}":"{p}",\n'

        p = get_rootfiles_path(massPoint.folder2017)
        string_2017+=f'"MX{mx}_MY{my}":"{p}",\n'

        p = get_rootfiles_path(massPoint.folder2018)
        string_2018+=f'"MX{mx}_MY{my}":"{p}",\n'
    
    # print("\n2016APV")
    # print(string_2016APV)
    # print("\n2016")
    # print(string_2016)
    # print("\n2017")
    # print(string_2017)
    print("\n2018")
    print(string_2018)

