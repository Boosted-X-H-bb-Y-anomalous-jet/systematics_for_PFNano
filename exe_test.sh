#!/bin/bash
while read -r line
do
    echo python addSys.py ${line}
    python addSys.py ${line}
done < test.txt

#xrdcp -f rootfiles/THselection_*.root root://cmseos.fnal.gov//store/user/roguljic/2017/selection/
