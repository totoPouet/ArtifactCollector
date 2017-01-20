#!/usr/bin/python
# -*- coding: utf-8 -*-

import io
import os
import yaml
import logging
import csv

from artifacts import definitions
#from artifacts import errors
from artifacts import reader

# Init. 
img_mount_point_path = "~/artifacts/"
definitions_file_path = "~/artifacts"
log_lvl = 10 # DEBUG 
"""
CRITICAL    50
ERROR       40
WARNING     30
INFO        20
DEBUG       10
NOTSET      0
"""
logging.basicConfig(filename='log_collect_artifact.txt', level=log_lvl, format='%(asctime)s - %(levelname)s - %(message)s')

def debug_print(debug_msg):
    logging.debug(str(debug_msg))

# arg to mount point , next step mount img files OR

# Convert win env to paths 
def ExpandWinPath(win_path):
    if "%%" in win_path:
        env_var = win_path.split("%%",2)[1]
        with open('win_expand_path_list.csv', 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                for field in row:
                    if field == env_var:
                        print "is in file"
    #img_mount_point_path
# Convert win to unix paths  
def ConvWinToUnixPath(separator,win_path):
    ExpandWinPath(unix_path)
    unix_path = win_path.replace(separator,"/")
    return unix_path
# Get files artifact 

def CollectFilesArtifact():

    artifact_reader = reader.YamlArtifactsReader()
    def_file = os.path.join('.', 'test_def_win.yaml')

    with open(def_file, 'r') as file_object:
        artifact_definitions = list(artifact_reader.ReadFileObject(file_object))
    for artifact_definition in artifact_definitions:    
        debug_print("Artifact Name : " + artifact_definition.name)
        debug_print("Artifact OS : " + artifact_definition.supported_os[0])
        
        #TODO manage multiple sources
        source_type = artifact_definition.sources[0]
        #Windows file
        if source_type.type_indicator == definitions.TYPE_INDICATOR_FILE:
            debug_print("Artifact path : " + source_type.paths[0])
            dl_path = img_mount_point_path + ConvWinToUnixPath(source_type.separator,source_type.paths[0])
            print dl_path



CollectFilesArtifact()
