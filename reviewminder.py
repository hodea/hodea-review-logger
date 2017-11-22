# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:22:12 2017

@author: Daniel
"""

__status__ = "Beta-Test"
__version__ ="0.0.1 Alpha"

import argparse
import os
from minder_config import minder_cfg 
from minder_database import minder_db
from itertools import product

    
########################################################
# Function: 
# command line argument parser
########################################################
def parse_cmdline():
    """Evaluates the parameters given per command line.
   
    returns
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description = "hodea review minder version  " + __version__,  
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--path','-p',
        help = "directory to be parsed from review minder",
        )
    parser.add_argument(
        '--verbose','-v',
        help = "keep console Open after parsing",
        default = "true",
        choices = ["false","true"],
        )
    parser.add_argument(
        '--noparse','-n',
        help = "create reports out of database only",
        default = "false",
        choices = ["false","true"],
        )
    parser.add_argument(
        '--htmlreport','-r',
        help = "create html report after parsing",
        default = "true",
        choices = ["false","true"],
        )
    parser.add_argument(
        '--pdfreport','-f',
        help = "create pdf report after parsing",
        default = "false",
        choices = ["false","true"],
        )

    
    args = parser.parse_args()
    return args



########################################################
# Global calls on start execution
########################################################                    
# Start the walk
class hodea_review_minder:

    
    def __init__(self, topdir):
        
        self.topdir = topdir
        
        try:
            config = minder_cfg(self.topdir)
            self.cfg_name = config.read_config(configname='name')
            self.cfg_type = config.read_config(configname='filetype')
            self.cfg_exclude = config.read_config(configname='exclude')
        except:
            raise Exception 
    #Debug print; TODO remove
        print("*****DEBUG:cfg name")
        print(self.cfg_name)
        print("*****")
        print("*****DEBUG:cfg type")
        print(self.cfg_type)
        print("*****")
        print("*****DEBUG:cfg exclude")
        print(self.cfg_exclude) 
        print("*****")
    #Debug End
        
        print("read config:     OK")
        
        
        try:
            minder_dict = minder_db(self.topdir)
            self.dict = minder_dict.Getdb()
        except:
            raise Exception
        print("read database:   OK")
    #Debug print; TODO remove
        print("*****DEBUG:")
        print(self.dict)
        print("*****")
    #Debug End
        
    def rm_access_check(self, Exception):
        
        for root, dirs, files in os.walk(self.topdir):
            for name in files:
                find = False
                for i in range(0,len(self.cfg_exclude)):
                    if self.cfg_exclude[i] in os.path.join(root, name):
                        find = True
                if find is True:
                    continue
                for j in range(0,len(self.cfg_type)): 
                    if name.lower().endswith(self.cfg_type[j]):
                        print(os.path.join(root, name))
                        try:
                            flog = open(os.path.join(root, name), "rb")
                            flog.close()  
                            flog = open(os.path.join(root, name), 'r+')  
                            flog.close() 
                        except:
                            print("ERROR: No Access to: " + os.path.join(root, name))
                            raise Exception


def main():
    
    args = parse_cmdline()  
    # use other source than default
    if args.path is not None:
        topdir = args.path.replace('\\','/')
    else:
        topdir = '.'
    print('top-dir:  '+topdir)
        
    try:
        minder = hodea_review_minder(topdir)
    except:
        print("Init ERROR: Stopping  minder! Please correct errors before proceeding.")
        return
    
    try:
        minder.rm_access_check(Exception)
    except:
        print("Access ERROR: Stopping  minder! Please correct errors before proceeding.")
        return
    
main()
