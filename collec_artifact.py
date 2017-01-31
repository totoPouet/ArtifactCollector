#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import io
import os
import yaml
import logging
import csv
import datetime

from shutil import copy


from artifacts import definitions
from artifacts import reader
#from artifacts import errors

# Init.
img_mount_point_path = "/home/osboxes/ArtifactCollector/test_data"
definitions_file_path = "~/artifacts/test_data"
copy_dest = "./Collected_artifact"
log_lvl = 10 # DEBUG
"""
CRITICAL    50
ERROR       40
WARNING     30
INFO        20
DEBUG       10
NOTSET      0
"""
#create logger
logger = logging.getLogger('simple')
# TODO filter log_lvl setup log level from arguments
logger.setLevel(log_lvl)
# create console handler and set level to debug
fh = logging.FileHandler(filename='log_collect_artifact.txt')
fh.setLevel(log_lvl) 
# create formatter
formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s","%Y-%m-%d %H:%M:%S")
# add formatter to logger
fh.setFormatter(formatter)
# add fh to logger
logger.addHandler(fh)

def debug_print(debug_msg):
    logger.debug(str(debug_msg))

def info_print(info_msg): 
    logger.info(str(info_msg))
    print str(datetime.datetime.now().time()) +" - "+ str(info_msg)

# arg to mount point , next step mount img files OR

# Convert win env to paths
def ExpandWinPath(win_path):
    if "%%" in win_path:
        env_var = win_path.split("%%")[1]
        tmp_path = win_path.split("%%")[2]
        debug_print("To expand: \""+env_var+"\" Path: "+ tmp_path)
        with open('win_expand_path_list.csv', 'rt') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['env_var'] == env_var:
                    win_full_path = row['expand_path'] + tmp_path
                    debug_print("Expanded path: " + win_full_path)
    return win_full_path

# Convert win to unix paths
def ConvWinToUnixPath(separator,win_path):
    win_full_path = ExpandWinPath(win_path)
    unix_path = win_full_path.replace(separator,"/")
    #debug_print("Unix path: "+ unix_path)
    return unix_path

def CheckFileExist(file_path):
    if os.path.exists(file_path):
        debug_print("File exist")
        IsPresent = 1
    else:
        debug_print("File not exist in current image !")
        IsPresent = 0
    return IsPresent

# Get files artifact
def CopyArtifact(src_path,dest_dir):
    if os.path.isfile(src_path):
        if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
        copy(src_path, dest_dir)
        dest_file = dest_dir + "/" + os.path.basename(src_path)
        if os.path.exists(dest_file):
            info_print("Artifact download success: " + dest_file)




def CollectFilesArtifact():

    artifact_reader = reader.YamlArtifactsReader()
    def_file = os.path.join('.', 'test_data/definitions/windows.yaml')

    with open(def_file, 'r') as file_object:
        artifact_definitions = list(artifact_reader.ReadFileObject(file_object))
    for artifact_definition in artifact_definitions:
        info_print("Artifact Name: " + artifact_definition.name)
        debug_print("Artifact OS: " + artifact_definition.supported_os[0])

        #TODO manage multiple sources
        source_type = artifact_definition.sources[0]
        #Windows file
        if source_type.type_indicator == definitions.TYPE_INDICATOR_FILE:
            cp_path = img_mount_point_path + ConvWinToUnixPath(source_type.separator,source_type.paths[0])
            # Test if artifact is in the image
            if CheckFileExist(cp_path):
                info_print("Artifact present: " + cp_path)
                info_print("Start download of: " + cp_path)
                CopyArtifact(cp_path,copy_dest)
                info_print("End of download: " + cp_path)
            else:
                info_print("Artifact not found: " + cp_path)
        else:
            info_print("Artifact ignore is not a file")



CollectFilesArtifact()
