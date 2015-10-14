#!/bin/bash
# http://stackoverflow.com/a/246128/761090
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# removed -oPermitTTY=no since unsupported on older openssh servers (travis in particular, ubuntu 14.04LTS)
/usr/sbin/sshd -d -f /dev/null -oPort=2024 -oProtocol=2 -oListenAddress=127.0.0.1 -oForceCommand=/sbin/nologin -oHostKey=$DIR/test_ssh_server_rsa_key -oAuthorizedKeysFile=$DIR/test_ssh_client_rsa_key.pub -oUsePrivilegeSeparation=no -oPubkeyAuthentication=yes -oPasswordAuthentication=no

