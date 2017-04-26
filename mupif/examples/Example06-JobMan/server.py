from __future__ import print_function
from builtins import str
import serverConfig as sConf
import os
from mupif import *
import logging
logger = logging.getLogger()

# required firewall settings (on ubuntu):
# for computer running daemon (this script)
# sudo iptables -A INPUT -p tcp -d 0/0 -s 0/0 --dport 44361 -j ACCEPT
# for computer running a nameserver
# sudo iptables -A INPUT -p tcp -d 0/0 -s 0/0 --dport 9090 -j ACCEPT

#if you wish to run no SSH tunnels, set to True
noSSH=False

#locate nameserver
ns = PyroUtil.connectNameServer(nshost=sConf.nshost, nsport=sConf.nsport, hkey=sConf.hkey)

if noSSH:
    sConf.server = sConf.serverNathost
    sConf.jobManNatport = sConf.jobManPort

#Run a daemon for jobManager on this machine
daemon = sConf.cfg.Pyro4.Daemon(host=sConf.server, port=sConf.jobManPort, nathost=sConf.serverNathost, natport=sConf.jobManNatport)
#Run job manager on a server
jobMan = SimpleJobManager.SimpleJobManager2(daemon, ns, sConf.applicationClass, sConf.jobManName, sConf.jobManPortsForJobs, sConf.jobManWorkDir, os.getcwd(), 'serverConfig', sConf.jobMan2CmdPath, sConf.jobManMaxJobs, sConf.jobManSocket)

PyroUtil.runJobManagerServer(server=sConf.server, port=sConf.jobManPort, nathost=sConf.serverNathost, natport=sConf.jobManNatport, nshost=sConf.nshost, nsport=sConf.nsport, nsname=sConf.jobManName, hkey=sConf.hkey, jobman=jobMan, daemon=daemon)

