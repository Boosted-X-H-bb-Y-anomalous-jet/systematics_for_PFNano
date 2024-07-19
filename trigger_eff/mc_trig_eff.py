import ROOT

import time, os
from optparse import OptionParser
from collections import OrderedDict

from TIMBER.Tools.Common import *
from TIMBER.Analyzer import *
import sys
import subprocess

redirector = 'root://cmseos.fnal.gov/'
eosls = 'eos root://cmseos.fnal.gov ls'

def eventSelection(fileName,outFile,year):

    #----Initialize RDataFrame-----#
    start_time = time.time()
    a = analyzer(fileName)

    # #For testing only, faster execution
    # nToRun=10000
    # small_rdf = a.GetActiveNode().DataFrame.Range(nToRun) 
    # small_node = Node('small',small_rdf)
    # a.SetActiveNode(small_node)
    histos          = []
    #----------Triggers------------#
    #beforeTrigCheckpoint    = a.GetActiveNode()
    if(year=="2016"):
        triggerList = ["HLT_PFHT800", "HLT_PFJet450"]
    elif(year=="2016APV"):
        triggerList = ["HLT_PFHT900","HLT_PFHT800","HLT_PFJet450"]
    else:
        triggerList = ["HLT_PFHT1050", "HLT_AK8PFJet500", "HLT_AK8PFJet380_TrimMass30", "HLT_AK8PFJet400_TrimMass30"]
    triggersStringTarget = a.GetTriggerString(triggerList)    
    print("Triggers: ", triggersStringTarget)
    #------------------------------#


    #----------Selection-----------#
    a.Cut("nFatJet","nFatJet>1")

    evtColumns = VarGroup("Event columns")
    evtColumns.Add("FatJet_pt0","FatJet_pt[0]")
    evtColumns.Add("FatJet_pt1","FatJet_pt[1]")
    evtColumns.Add("FatJet_eta0","FatJet_eta[0]")
    evtColumns.Add("FatJet_eta1","FatJet_eta[1]")

    dijetColumns = VarGroup("dijet Columns")
    dijetColumns.Add("DeltaEta","abs(FatJet_eta[0] - FatJet_eta[1])")
    dijetColumns.Add('LeadingVector', 'hardware::TLvector(FatJet_pt0,FatJet_eta[0],FatJet_phi[0],FatJet_msoftdrop[0])')
    dijetColumns.Add('SubleadingVector',  'hardware::TLvector(FatJet_pt1,FatJet_eta[1],FatJet_phi[1],FatJet_msoftdrop[1])')
    dijetColumns.Add('MJJ',     'hardware::InvariantMass({LeadingVector,SubleadingVector})') 

    a.Apply([evtColumns,dijetColumns])

    a.Cut("Jet0","FatJet_pt0>300 && abs(FatJet_eta0)<2.5")
    a.Cut("Jet1","FatJet_pt1>300 && abs(FatJet_eta1)<2.5")
    a.Cut("DeltaEtaCut","DeltaEta<1.3")
    a.Cut("MJJCut","MJJ>600")#Will plot it

    h_denom = a.GetActiveNode().DataFrame.Histo1D(('mjj_denominator',';$M_{JJ}$ [GeV]; Events/50 GeV;',28,600,2000),"MJJ")
    
    a.Cut("JetHT triggers",triggersStringTarget)
        
    h_numer = a.GetActiveNode().DataFrame.Histo1D(('mjj_numerator',';$M_{JJ}$ [GeV]; Events/50 GeV;',28,600,2000),"MJJ")

    histos.append(h_denom)
    histos.append(h_numer)
    #------------------------------#
    out_f = ROOT.TFile(outFile,"RECREATE")
    out_f.cd()
    for h in histos:
        h.Write()
    out_f.Close()
    #------------------------------#
    a.Close()
    #small_node.Close()

    #a.PrintNodeTree('node_tree.dot',verbose=True)
    print("Total time: "+str((time.time()-start_time)/60.) + ' min')



def getFilesForProcess(path):
    fNames   = subprocess.check_output(['{} {}'.format(eosls,path)],shell=True,text=True).split('\n')
    fNames.remove('')
    fNames.remove('log')
    if len(fNames)>100:
        fNames = fNames[:100]

    return fNames

def generateInput(proc, year, line, fileNames):
    output_file_name = f"{proc}_{year}.txt"
    line = line.rstrip()
    with open(output_file_name, 'w') as output_file:
        for fileName in fileNames:
            output_file.write(f"{line}{fileName}\n")

def run(options,report=True):
    inputFile = open(options.input,'r')
    lines     = inputFile.readlines()
    year      = options.year    

    for line in lines:
        print(line)
        proc        = line.split("/")[8]
        outFile  = f"{proc}_{year}.root"
        if os.path.isfile(outFile):
            print("Exists, skipping")
            continue
        fileNames = getFilesForProcess(line)
        generateInput(proc,year,line,fileNames)
        eventSelection(f"{proc}_{year}.txt",outFile,year)




parser = OptionParser()

parser.add_option('-i', '--input', metavar='IFILE', type='string', action='store',
                default   =   '',
                dest      =   'input',
                help      =   'A root file or text file with multiple root file locations to analyze')
parser.add_option('-y', '--year', metavar='year', type='string', action='store',
                default   =   '2016',
                dest      =   'year',
                help      =   'Dataset year')

(options, args) = parser.parse_args()
CompileCpp("TIMBER/Framework/src/common.cc") 
run(options,report=False)