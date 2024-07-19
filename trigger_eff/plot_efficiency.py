import ROOT
import argparse

def calculate_efficiency(file, label):
    f = ROOT.TFile(file)
    h_den = f.Get("mjj_denominator")
    h_num = f.Get("mjj_numerator")
    
    if not h_den or not h_num:
        print(f"Error: Histograms not found in the file {file}.")
        return None
    
    efficiency = ROOT.TGraphAsymmErrors()
    efficiency.Divide(h_num, h_den, "cl=0.683 b(1,1) mode")
    efficiency.SetMarkerStyle(21)
    return efficiency

if __name__ == "__main__":
    # python plot_efficiency.py  signal_2016.root  TTToHadronic_TuneCP5_13TeV-powheg-pythia8_2016.root  Signal  TTbar 2016
    # python plot_efficiency.py  signal_2016APV.root  TTToHadronic_TuneCP5_13TeV-powheg-pythia8_2016APV.root  Signal  TTbar 2016APV
    # python plot_efficiency.py  signal_2017.root  TTToHadronic_TuneCP5_13TeV-powheg-pythia8_2017.root  Signal  TTbar 2017
    # python plot_efficiency.py  signal_2018.root  TTToHadronic_TuneCP5_13TeV-powheg-pythia8_2018.root  Signal  TTbar 2018
    parser = argparse.ArgumentParser(description="Calculate and plot efficiencies from two ROOT files.")
    parser.add_argument("file1", type=str, help="First ROOT file containing histograms.")
    parser.add_argument("file2", type=str, help="Second ROOT file containing histograms.")
    parser.add_argument("label1", type=str, help="Label for the first histogram set.")
    parser.add_argument("label2", type=str, help="Label for the second histogram set.")
    parser.add_argument("title", type=str, help="Title of the plot.")
    args = parser.parse_args()

    efficiency1 = calculate_efficiency(args.file1, args.label1)
    efficiency2 = calculate_efficiency(args.file2, args.label2)
    
    if efficiency1 and efficiency2:
        canvas = ROOT.TCanvas("canvas", "Efficiency", 800, 600)
        
        canvas.SetLeftMargin(0.15)
        canvas.SetBottomMargin(0.15)
        canvas.SetTopMargin(0.15)
        
        efficiency1.SetMarkerColor(ROOT.kBlue)
        efficiency1.Draw("AP")
        efficiency2.SetMarkerColor(ROOT.kRed)
        efficiency2.Draw("P same")
        
        efficiency1.GetXaxis().SetRangeUser(600, 2000)
        efficiency1.GetXaxis().SetTitle("M_{jj} [GeV]")
        efficiency1.GetYaxis().SetTitle("Trigger efficiency")
        
        efficiency1.GetXaxis().SetTitleSize(0.05)
        efficiency1.GetXaxis().SetLabelSize(0.04)
        efficiency1.GetYaxis().SetTitleSize(0.05)
        efficiency1.GetYaxis().SetLabelSize(0.04)
        
        legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
        legend.AddEntry(efficiency1, args.label1, "p")
        legend.AddEntry(efficiency2, args.label2, "p")
        legend.Draw()
        
        title = ROOT.TPaveText(0.1, 0.92, 0.9, 0.98, "NDC")
        title.AddText(args.title)
        title.SetFillColor(0)
        title.SetTextAlign(22)
        title.SetTextSize(0.04)
        title.Draw()
        
        canvas.SaveAs(f"efficiency_{args.title}.png")
        canvas.SaveAs(f"efficiency_{args.title}.pdf")
