import os
import subprocess
import sys
import xbmc
import xbmcaddon

sys.path.append('/usr/share/kodi/addons/service.libreelec.settings')
import oe

__author__      = 'Josh.5'
__addon__       = xbmcaddon.Addon()
__path__        = __addon__.getAddonInfo('path')


def update_symlink():
    restart_mergerfs = False

    if restart_mergerfs:
        restart_mergerfs()

def restart_mergerfs():
    if not os.path.islink('/storage/.config/system.d/storage-pool.mount'):
        os.symlink(os.path.join(__path__, 'system.d', 'storage-pool.mount'), '/storage/.config/system.d/storage-pool.mount')
    if not os.path.islink(os.path.join(__path__, 'bin', 'mount.mergerfs')):
        os.symlink(os.path.join(__path__, 'bin', 'mergerfs'), os.path.join(__path__, 'bin', 'mount.mergerfs'))
    subprocess.call(['systemctl', 'daemon-reload'])
    subprocess.call(['systemctl', 'enable', 'storage-pool.mount'])
    subprocess.call(['systemctl', 'restart', 'storage-pool.mount'])

def restart_docker():
    # TODO: This can be removed now that the systemd unit stops and starts dockerd on a restart. Test to be sure.
    subprocess.call(['systemctl', 'restart', 'docker.service'])

class Monitor(xbmc.Monitor):

   def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)
        self.id = xbmcaddon.Addon().getAddonInfo('id')

   def onSettingsChanged(self):
        restart_mergerfs()
        restart_docker()


if __name__ == '__main__':
    restart_mergerfs()
    restart_docker()
    Monitor().waitForAbort()
