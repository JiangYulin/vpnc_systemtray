#!/usr/bin/env python2
import sys
import os
from PyQt4 import QtCore
from PyQt4 import QtGui


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    appexit = None
    appconnect = None
    appdisconnected = None

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QtGui.QIcon("icon.png"))
        self.Menu = QtGui.QMenu(parent)
        self.appconnect = self.Menu.addAction("Connect")
        self.appconnect.setIcon(QtGui.QIcon('./connect-icon.png'))
        self.appexit = self.Menu.addAction("Exit")
        self.setContextMenu(self.Menu)
        self.connect(self.appconnect,QtCore.SIGNAL('triggered()'),self.connectVPN)
        self.connect(self.appexit,QtCore.SIGNAL('triggered()'),self.appExit)
        self.show()

    def connectVPN(self):
			flag = os.path.isfile('/var/run/vpnc/pid')
			if flag:
					self.iconMenu.removeAction(self.appconnect)
					self.appdisconnected = self.Menu.addAction('Disconnect')
					self.connect(self.appdisconnected,QtCore.SIGNAL('triggered()'),self.disconnected)
			else:
					os.system('vpnc')
					self.connectVPN()

    def disconnected(self):
			flag = os.path.isfile('/var/run/vpnc/pid')
			if flag:
					os.system('vpnc-disconnect')
					self.appconnect = self.Menu.addAction('Connect')
					self.connect(self.appconnect,QtCore.SIGNAL('triggered()'),self.connectVPN)
					self.Menu.removeAction(self.appdisconnected)
			else:
					pass

    def appExit(self):
        sys.exit()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    trayIcon = SystemTrayIcon()
    trayIcon.show()

    sys.exit(app.exec_())
