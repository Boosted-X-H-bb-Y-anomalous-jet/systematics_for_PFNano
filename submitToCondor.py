import os
jdl_tpl = '''
universe = vanilla
Executable = exe.sh
Should_Transfer_Files = YES
request_cpus = 1
request_memory = 2000
Output = logs/output_$(Cluster)_$(Process).stdout
Error = logs/output_$(Cluster)_$(Process).stderr
Log = logs/output_$(Cluster)_$(Process).log
Arguments = "$(args)"
transfer_input_files = tarball.tgz
Queue args from ARGFILE.txt
'''

MX = ["1400","1600","1800","2200","2600","3000"]
MY = ["90","125","190","250","300","400"]

def fill_signal_datasets(datasets,MX, MY):
    base_path_template = "/eos/uscms/store/group/lpcpfnano/{user}/v2_3"
    users = {
        "2016APV": "rkansal",
        "2016": "rkansal",
        "2017": "ammitra",
        "2018": "cmantill"
    }

    signal_datasets = {}

    for mx in MX:
        for my in MY:
            signal_datasets[(mx, my)] = []

            for era, user in users.items():
                base_path = f"{base_path_template.format(user=user)}/{era}/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-{mx}_MY-{my}_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-{mx}_MY-{my}"

                try:
                    date_dirs = os.listdir(base_path)
                    for date_dir in date_dirs:
                        full_path = os.path.join(base_path, date_dir, "0000")
                        if os.path.exists(full_path):
                            signal_datasets[(mx, my)].append(full_path)
                            datasets[era][f"MX{mx}_MY{my}"] = full_path
                            break
                except FileNotFoundError:
                    print("Did not find: ", base_path)
                    continue

datasets = {    
    "2016": {
        "TTToSemiLeptonic": "/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2016/TTbar/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TTToSemiLeptonic/220808_181840/0000/",
        "TTToHadronic": "/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2016/TTbar/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TTToHadronic/220808_181812/0000/"
    },
    "2016APV": {
        "TTToSemiLeptonic": "/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2016APV/TTbar/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TTToSemiLeptonic/220808_173625/0000/",        
        "TTToHadronic": "/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2016APV/TTbar/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TTToHadronic/220808_173601/0000/"
    },
    "2017": {
        "TTToSemiLeptonic": "/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2017/TTbar/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TTToSemiLeptonic/220705_160227/0000/",
        "TTToHadronic": "/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2017/TTbar/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TTToHadronic/220705_160139/0000/"
    },
    "2018": {
        "TTToSemiLeptonic": "/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/TTbar/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TTToSemiLeptonic/220808_151244/0000/",
        "TTToHadronic": "/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/TTbar/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TTToHadronic/220808_151154/0000/"
    }
}


fill_signal_datasets(datasets,MX,MY)

def write_arg_files(process,year,outdir,filelist,n=50):
    counter = 0
    for i in range(0,len(filelist), n):  
        files_chunk = filelist[i:i + n]
        counter+=1

        f = open(f"args_{process}_{year}_{counter}.txt","w")
        for file in files_chunk:
            f.write(f"-i {file} -o {outdir} -y {year} \n") 
        f.close()
    return counter

if(__name__ == "__main__"):
    #for year in ["2016APV","2016","2017","2018"]:
    for year in ["2016","2017","2018"]:
        for process, inputDir in datasets[year].items():
            input_dir_root = inputDir.replace("/eos/uscms/","root://cmseos.fnal.gov//")

            root_dir = f"root://cmseos.fnal.gov//store/user/roguljic/XHYAnomalous/PFNanoExtensions_v2/{year}/{process}/"
            eos_dir  = root_dir.replace("root://cmseos.fnal.gov/","/eos/uscms/")
            
            if not os.path.exists(eos_dir):
                print(f"Making dir {eos_dir}")
                os.makedirs(eos_dir)

            file_list = os.listdir(inputDir)
            to_do     = []
            for name in file_list:
                if not ".root" in name:
                    continue
                output_name = eos_dir+name
                if os.path.exists(output_name):
                    continue
                else:
                    to_do.append(f"{input_dir_root}/{name}")
            
            if to_do:
                n_jobs = write_arg_files(process,year,root_dir,to_do)
                f      = open(f"args_{process}_{year}.txt","w")
                for job_id in range(1,n_jobs+1):
                    f.write(f"args_{process}_{year}_{job_id}.txt\n")

                condor_tpl = jdl_tpl.replace("ARGFILE",f"args_{process}_{year}")
                f = open(f"jdl_{process}_{year}.txt","w")
                f.write(condor_tpl)
                f.close()

                print(f"condor_submit jdl_{process}_{year}.txt")
                os.system(f"condor_submit jdl_{process}_{year}.txt")

    os.system("tar cf tarball.tgz addSys.py THmodules.cc args*txt")