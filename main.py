#! /usr/bin/env python

# Check for root user login
import os, sys
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\n")

# Get your username (not root)
import pwd
uname=pwd.getpwuid(1000)[0]

# The remastering process uses chroot mode.
# Check to see if this script is operating in chroot mode.
# /home/mint directory only exists in chroot mode
is_chroot = os.path.exists('/home/mint')
dir_develop=''
if (is_chroot):
	dir_develop='/usr/local/bin/develop'
	dir_user = '/home/mint'
else:
	dir_develop='/home/' + uname + '/develop'
	dir_user = '/home/' + uname

# Everything up to this point is common to all Python scripts called by shared-*.sh
# =================================================================================


# This is the script for updating the Apt-Get/Synaptic settings and repositories

import shutil

# Set Apt-Get/Synaptic to NOT install recommended packages
src=dir_develop+'/apt/etc_apt_apt_conf_d/99synaptic'
dest='/etc/apt/apt.conf.d/99synaptic'
shutil.copyfile(src, dest)

# Update sources.list to reflect Update Pack 3 (http://blog.linuxmint.com/?m=201109)
src=dir_develop+'/apt/etc_apt/sources.list'
dest='/etc/apt/sources.list'
shutil.copyfile(src, dest)

# Update the local repository
os.system ('apt-get update')

os.system ('echo PURGING pulseaudio to expedite the process of transforming LMDE into Swift Linux')
os.system ('echo pulseaudio will be reinstalled later in this process')
os.system ('apt-get purge -qq pulseaudio')

