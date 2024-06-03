#!/bin/bash
tar -cf timber_tar.tgz TIMBER
xrdcp -f timber_tar.tgz root://cmseos.fnal.gov//store/user/roguljic/timber_tar.tgz