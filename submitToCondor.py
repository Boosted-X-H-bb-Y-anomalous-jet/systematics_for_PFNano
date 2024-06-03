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

datasets = {    
    "2016": {
        "TTToHadronic": "/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2016/TTbar/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TTToHadronic/220808_181812/0000/",
        "MX1200_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1200_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1200_MY-90/230323_182915/0000",
        "MX1400_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1400_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1400_MY-90/230323_195611/0000",
        "MX1600_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1600_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1600_MY-90/230323_195509/0000",
        "MX1800_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1800_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1800_MY-90/230323_193756/0000",
        "MX2000_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2000_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2000_MY-90/230323_192110/0000",
        "MX2200_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2200_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2200_MY-90/230323_194405/0000",
        "MX2400_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2400_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2400_MY-90/230323_194905/0000",
        "MX2500_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2500_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2500_MY-90/230323_180409/0000",
        "MX2600_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2600_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2600_MY-90/230323_181825/0000",
        "MX2800_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2800_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2800_MY-90/230323_200851/0000",
        "MX3000_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-3000_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-3000_MY-90/230323_185042/0000",
        "MX3500_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-3500_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-3500_MY-90/230323_185439/0000",
        "MX4000_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-4000_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-4000_MY-90/230323_194505/0000",
    },
    "2016APV": {
        "TTToHadronic": "/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2016APV/TTbar/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TTToHadronic/220808_173601/0000/",
        "MX1200_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1200_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1200_MY-90/230323_163901/0000",
        "MX1400_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1400_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1400_MY-90/230323_180135/0000",
        "MX1600_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1600_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1600_MY-90/230323_180040/0000",
        "MX1800_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1800_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1800_MY-90/230323_174652/0000",
        "MX2000_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2000_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2000_MY-90/230323_172344/0000",
        "MX2200_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2200_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2200_MY-90/230323_175300/0000",
        "MX2400_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2400_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2400_MY-90/230323_175638/0000",
        "MX2500_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2500_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2500_MY-90/230323_162104/0000",
        "MX2600_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2600_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2600_MY-90/230323_163125/0000",
        "MX2800_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2800_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2800_MY-90/230323_191442/0000",
        "MX3000_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-3000_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-3000_MY-90/230323_165405/0000",
        "MX3500_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-3500_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-3500_MY-90/230323_165647/0000",
        "MX4000_MY90":"/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2016APV/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-4000_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-4000_MY-90/230323_175352/0000",
    },
    "2017": {
        "TTToHadronic": "/eos/uscms/store/group/lpcpfnano/rkansal/v2_3/2017/TTbar/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TTToHadronic/220705_160139/0000/",
        "MX2400_MY100": "/eos/uscms/store/group/lpcpfnano/ammitra/v2_3/2017/XHYPrivate/NMSSM_XToYH_MX2400_MY100_HTo2bYTo2W_hadronicDecay/NMSSM_XToYH_MX2400_MY100_HTo2bYTo2W_hadronicDecay/221013_153330/0000/",
        "MX1200_MY90":"/eos/uscms//store/group/lpcpfnano/ammitra/v2_3/2017/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1200_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1200_MY-90/230323_173430/0000",
        "MX1400_MY90":"/eos/uscms//store/group/lpcpfnano/ammitra/v2_3/2017/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1400_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1400_MY-90/230323_190106/0000",
        "MX1600_MY90":"/eos/uscms//store/group/lpcpfnano/ammitra/v2_3/2017/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1600_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1600_MY-90/230323_185942/0000",
        "MX1800_MY90":"/eos/uscms//store/group/lpcpfnano/ammitra/v2_3/2017/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1800_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1800_MY-90/230323_183813/0000",
        "MX2000_MY90":"/eos/uscms//store/group/lpcpfnano/ammitra/v2_3/2017/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2000_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2000_MY-90/230323_181642/0000",
        "MX2200_MY90":"/eos/uscms//store/group/lpcpfnano/ammitra/v2_3/2017/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2200_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2200_MY-90/230323_184540/0000",
        "MX2400_MY90":"/eos/uscms//store/group/lpcpfnano/ammitra/v2_3/2017/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2400_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2400_MY-90/230323_185206/0000",
        "MX2500_MY90":"/eos/uscms//store/group/lpcpfnano/ammitra/v2_3/2017/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2500_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2500_MY-90/230323_171831/0000",
        "MX2600_MY90":"/eos/uscms//store/group/lpcpfnano/ammitra/v2_3/2017/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2600_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2600_MY-90/230323_172734/0000",
        "MX2800_MY90":"/eos/uscms//store/group/lpcpfnano/ammitra/v2_3/2017/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2800_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2800_MY-90/230323_191800/0000",
        "MX3000_MY90":"/eos/uscms//store/group/lpcpfnano/ammitra/v2_3/2017/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-3000_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-3000_MY-90/230323_174810/0000",
        "MX3500_MY90":"/eos/uscms//store/group/lpcpfnano/ammitra/v2_3/2017/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-3500_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-3500_MY-90/230323_175051/0000",
        "MX4000_MY90":"/eos/uscms//store/group/lpcpfnano/ammitra/v2_3/2017/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-4000_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-4000_MY-90/230323_184703/0000",
    },
    "2018": {
        "TTToHadronic": "/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/TTbar/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TTToHadronic/220808_151154/0000/",
        "MX1200_MY90":"/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1200_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1200_MY-90/230323_140756/0000",
        "MX1400_MY90":"/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1400_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1400_MY-90/230323_180330/0000",
        "MX1600_MY90":"/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1600_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1600_MY-90/230323_180132/0000",
        "MX1800_MY90":"/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-1800_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-1800_MY-90/230323_173225/0000",
        "MX2000_MY90":"/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2000_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2000_MY-90/230323_170430/0000",
        "MX2200_MY90":"/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2200_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2200_MY-90/230323_174255/0000",
        "MX2400_MY90":"/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2400_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2400_MY-90/230323_175200/0000",
        "MX2500_MY90":"/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2500_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2500_MY-90/230323_134523/0000",
        "MX2600_MY90":"/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2600_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2600_MY-90/230323_135807/0000",
        "MX2800_MY90":"/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-2800_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-2800_MY-90/230323_182514/0000",
        "MX3000_MY90":"/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-3000_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-3000_MY-90/230323_142659/0000",
        "MX3500_MY90":"/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-3500_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-3500_MY-90/230323_143041/0000",
        "MX4000_MY90":"/eos/uscms/store/group/lpcpfnano/cmantill/v2_3/2018/XHY/NMSSM_XToYHTo2W2BTo4Q2B_MX-4000_MY-90_TuneCP5_13TeV-madgraph-pythia8/NMSSM_XToYHTo2W2BTo4Q2B_MX-4000_MY-90/230323_170454/0000",
    }
}
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
    for year in ["2016APV","2016","2017","2018"]:
        for process, inputDir in datasets[year].items():
            input_dir_root = inputDir.replace("/eos/uscms/","root://cmseos.fnal.gov//")

            root_dir = f"root://cmseos.fnal.gov//store/user/roguljic/XHYAnomalous/PFNanoExtensions/{year}/{process}/"
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

    os.system("tar cf tarball.tgz addSys.py THmodules.cc args*txt")