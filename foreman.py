#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

def check_root():
    if not os.geteuid() == 0:
        sys.exit("You need root privileges.")
        
check_root()

host_name = os.uname()[1]
print "Input the hostname: [%s]" % host_name
capture_host_name = raw_input().lower().strip()

if capture_host_name == "":
    host_name = os.uname()[1]
else:
    host_name = capture_host_name
    
cmd = ['localectl', 'set-locale', 'LANG=en_US.UTF-8']
subprocess.call(cmd)

os.system("yum -y update")
os.system("yum -y install https://yum.puppetlabs.com/puppet5/puppet5-release-el-7.noarch.rpm")
os.system("yum -y install http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm")
os.system("yum -y install https://yum.theforeman.org/releases/1.16/el7/x86_64/foreman-release.rpm")
os.system("yum -y update")

os.system("firewall-cmd --permanent --add-service=http")
os.system("firewall-cmd --permanent --add-service=https")
os.system("firewall-cmd --permanent --add-service=ldap")
os.system("firewall-cmd --permanent --add-service=ldaps")
os.system("firewall-cmd --permanent --add-port=69/udp")
os.system("firewall-cmd --permanent --add-port=3000/tcp")
os.system("firewall-cmd --permanent --add-port=5910-5930/tcp")
os.system("firewall-cmd --permanent --add-port=8140/tcp")
os.system("firewall-cmd --permanent --add-port=8443/tcp")
os.system("firewall-cmd --reload")

os.system("yum -y install foreman-installer")
os.system("foreman-installer --enable-foreman --enable-foreman-cli --enable-foreman-proxy --enable-puppet --enable-foreman-plugin-cockpit --enable-foreman-plugin-setup")
filelist = os.listdir("/opt/puppetlabs/bin")

for i in list(range(len(filelist))):
    cmd = ['ln', '-s', '/opt/puppetlabs/bin/'+filelist[i], '/bin/'+filelist[i]]
    subprocess.call(cmd)

os.system("sed -i -e \'s/os.present? \&\&/os.present? #\&\&/g\' -e \'s/%w(Redhat/#%w(Redhat/g\' /opt/theforeman/tfm/root/usr/share/gems/gems/foreman_cockpit-2.0.3/app/models/concerns/foreman_cockpit/host_extensions.rb")
os.system("puppet agent --enable")
os.system("puppet agent -t")
