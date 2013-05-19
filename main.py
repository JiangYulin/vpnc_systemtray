#!/usr/bin/env python2
import sys
import os
import threading
import pynotify

from PyQt4 import QtCore
from PyQt4 import QtGui

iconPath = './icon.png'

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    appexit = None
    appconnect = None
    appdisconnected = None

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QtGui.QIcon(iconPath))
        self.Menu = QtGui.QMenu(parent)
        self.appconnect = self.Menu.addAction("Connect")
        self.appexit = self.Menu.addAction("Exit")
        self.setContextMenu(self.Menu)
        self.appconnect.triggered.connect(lambda:self._fork(self.connectVPN))
        #self.connect(self.appconnect,QtCore.SIGNAL('triggered()'),self._fork('self.connectVPN'))
        self.connect(self.appexit,QtCore.SIGNAL('triggered()'),self.appExit)
        self.show()

    def _fork(self,_fun):
			t=threading.Thread(target=_fun)
			t.start()

    def connectVPN(self):
			flag = os.path.isfile('/var/run/vpnc/pid')
			if flag:
					self.appdisconnected = self.Menu.addAction('Disconnect')
					self.connect(self.appdisconnected,QtCore.SIGNAL('triggered()'),self.disconnected)
					self._notification("vpn connected!")
			else:
					self.Menu.removeAction(self.appconnect)
					os.system('vpnc')
					self.connectVPN()

    def disconnected(self):
			flag = os.path.isfile('/var/run/vpnc/pid')
			if flag:
					os.system('vpnc-disconnect')
					self.appconnect = self.Menu.addAction('Connect')
					self.appconnect.triggered.connect(lambda:self._fork(self.connectVPN))
					self.Menu.removeAction(self.appdisconnected)
			else:
					pass

    def _notification(self,message):
	    pynotify.init("Notify")
	    noti = pynotify.Notification(message)
	    noti.show()

    def appExit(self):
        sys.exit()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print "This program must be run as root.Aborting."
        sys.exit(1)
    app = QtGui.QApplication(sys.argv)
    trayIcon = SystemTrayIcon()
    trayIcon.show()
    sys.exit(app.exec_())
