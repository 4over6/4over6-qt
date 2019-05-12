#!/usr/bin/env python

import sys, os, subprocess, socket, glob, signal
import urllib.request, re
from PyQt5 import QtCore, QtGui, QtWidgets

from thu4over6.ui_thu4over6logviewer import Ui_THU4Over6LogViewer
from thu4over6.ui_thu4over6settings import Ui_THU4Over6Settings


# Allow CTRL+C and/or SIGTERM to kill us (PyQt blocks it otherwise)
signal.signal(signal.SIGINT, signal.SIG_DFL)
signal.signal(signal.SIGTERM, signal.SIG_DFL)


class THU4Over6Settings(QtWidgets.QDialog, Ui_THU4Over6Settings):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        settings = QtCore.QSettings()
        self.sudoCommandEdit.setText(settings.value("sudo_command") or "sudo")
        self.sudoCheckBox.setChecked(settings.value("use_sudo", True, type=bool))
        self.warningCheckBox.setChecked(settings.value("show_warning", False, type=bool))

        # find executable
        try:
            output = subprocess.check_output(["/usr/bin/env", "4over6-client", "--help"])
        except subprocess.CalledProcessError as e:
            output = e.output
        except OSError:
            print("4over6 client executable not found!", file=sys.stderr)
            output = ""

        settings.setValue("config_location", "/etc/4over6/*.conf")
        settings.setValue("service_name", "thu4over6-client")

        # Fill VPN combo box with .conf files
        for f in sorted(glob.glob(settings.value("config_location"))):
            vpn_name = os.path.splitext(os.path.basename(f))[0]
            self.vpnNameComboBox.addItem(vpn_name)

        i = self.vpnNameComboBox.findText(settings.value("vpn_name"))
        if i > -1:
            self.vpnNameComboBox.setCurrentIndex(i)

    def accept(self):
        settings = QtCore.QSettings()
        settings.setValue("sudo_command", self.sudoCommandEdit.text())
        settings.setValue("use_sudo", self.sudoCheckBox.isChecked())
        settings.setValue("show_warning", self.warningCheckBox.isChecked())
        settings.setValue("vpn_name", self.vpnNameComboBox.currentText())
        QtWidgets.QDialog.accept(self)


class THU4Over6LogViewer(QtWidgets.QDialog, Ui_THU4Over6LogViewer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.refreshButton.clicked.connect(self.refresh)
        self.refresh()

    def journalctl(self):
        """Run journalctl command and get logs"""
        settings = QtCore.QSettings()
        cmdline = []
        if settings.value("use_sudo", type=bool):
            cmdline.append(settings.value("sudo_command") or "sudo")
        cmdline.extend([
            "journalctl", "-b", "--no-pager", "-u",
            "{}@{}".format(settings.value("service_name"), settings.value("vpn_name"))
        ])
        try:
            output = subprocess.check_output(cmdline)
        except subprocess.CalledProcessError as e:
            output = e.output
        return output

    def getip(self):
        """Get tunnel IP address and hostname"""
        try:
            ip = os.popen('ip addr show 4over6').read().split("inet ")[1].split("/")[0]
        except:
            ip = ""

        return ip

    def refresh(self):
        """Refresh logs"""
        self.logViewerEdit.setPlainText(self.journalctl().decode("utf8"))
        QtCore.QTimer.singleShot(0, self.refresh_timeout)

    def refresh_timeout(self):
        """Move scrollbar to bottom and refresh IP address
        (must be called by single shot timer or else scrollbar sometimes doesn't move)"""
        self.logViewerEdit.verticalScrollBar().setValue(self.logViewerEdit.verticalScrollBar().maximum())

        ip = self.getip()
        self.ipAddressEdit.setText(ip)


class THU4Over6Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vpn_enabled = False

        self.create_actions()
        self.create_menu()
        self.create_icon()
        self.update_status()

        # Update status every 10 seconds
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(5000)

        # Setup system tray icon doubleclick timer
        self.icon_doubleclick_timer = QtCore.QTimer(self)
        self.icon_doubleclick_timer.setSingleShot(True)
        self.icon_doubleclick_timer.timeout.connect(self.icon_doubleclick_timeout)

    def create_actions(self):
        """Create actions and connect relevant signals"""
        self.startAction = QtWidgets.QAction(self.tr("&Start"), self)
        self.startAction.triggered.connect(self.vpn_start)
        self.stopAction = QtWidgets.QAction(self.tr("S&top"), self)
        self.stopAction.triggered.connect(self.vpn_stop)
        self.settingsAction = QtWidgets.QAction(self.tr("S&ettings ..."), self)
        self.settingsAction.triggered.connect(self.settings)
        self.logsAction = QtWidgets.QAction(self.tr("Show &logs ..."), self)
        self.logsAction.triggered.connect(self.logs)
        self.quitAction = QtWidgets.QAction(self.tr("&Quit"), self)
        self.quitAction.triggered.connect(self.quit)

    def create_menu(self):
        """Create menu and add items to it"""
        self.trayIconMenu = QtWidgets.QMenu(self)
        self.trayIconMenu.addAction(self.startAction)
        self.trayIconMenu.addAction(self.stopAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.settingsAction)
        self.trayIconMenu.addAction(self.logsAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

    def create_icon(self):
        """Create system tray icon"""
        self.iconActive = QtGui.QIcon("{}/4over6.png".format(os.path.dirname(os.path.abspath(__file__))))
        self.iconDisabled = QtGui.QIcon("{}/4over6_disabled.png".format(os.path.dirname(os.path.abspath(__file__))))

        # Workaround for Plasma 5 not showing SVG icons
        self.iconActive = QtGui.QIcon(self.iconActive.pixmap(128, 128))
        self.iconDisabled = QtGui.QIcon(self.iconDisabled.pixmap(128, 128))

        self.trayIcon = QtWidgets.QSystemTrayIcon(self)
        self.trayIcon.activated.connect(self.icon_activated)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(self.iconDisabled)
        self.trayIcon.setToolTip("THU4Over6")
        self.trayIcon.show()

    def update_status(self, disable_warning=False):
        """Update GUI according to VPN status"""
        settings = QtCore.QSettings()
        vpn_status = self.vpn_status()
        if vpn_status:
            self.trayIcon.setIcon(self.iconActive)
            self.startAction.setEnabled(False)
            self.stopAction.setEnabled(True)
            self.vpn_enabled = True
        else:
            self.trayIcon.setIcon(self.iconDisabled)
            self.startAction.setEnabled(True)
            self.stopAction.setEnabled(False)

            if not disable_warning and settings.value("show_warning", type=bool) and self.vpn_enabled:
                QtWidgets.QMessageBox.warning(self, self.tr("THU4Over6 - Warning"),
                                              self.tr("You have been disconnected from VPN!"))
            self.vpn_enabled = False

    def systemctl(self, command, disable_sudo=False, quiet=False):
        """Run systemctl command"""
        settings = QtCore.QSettings()
        cmdline = []
        if not disable_sudo and settings.value("use_sudo", type=bool):
            cmdline.append(settings.value("sudo_command") or "sudo")
        cmdline.extend([
            "systemctl", command,
            "{}@{}".format(settings.value("service_name"), settings.value("vpn_name"))
        ])
        stdout = stderr = subprocess.DEVNULL if quiet else None
        return subprocess.call(cmdline, stdout=stdout, stderr=stderr)

    def vpn_start(self):
        """Start service"""
        retcode = self.systemctl("start")
        if retcode == 0:
            self.update_status()

    def vpn_stop(self):
        """Stop service"""
        retcode = self.systemctl("stop")
        if retcode == 0:
            self.update_status(disable_warning=True)

    def vpn_status(self):
        """Check if service is running"""
        retcode = self.systemctl("is-active", disable_sudo=True, quiet=True)
        return True if retcode == 0 else False

    def settings(self):
        """Show settings dialog"""
        dialog = THU4Over6Settings(self)
        if dialog.exec_() and self.vpn_enabled:
            self.vpn_stop()
            self.vpn_start()

    def logs(self):
        """Show log viewer dialog"""
        dialog = THU4Over6LogViewer(self)
        dialog.exec_()

    def icon_activated(self, reason):
        """Start or stop VPN by double-click on tray icon"""
        if reason == QtWidgets.QSystemTrayIcon.Trigger or reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            if self.icon_doubleclick_timer.isActive():
                self.icon_doubleclick_timer.stop()
                if self.vpn_enabled:
                    self.vpn_stop()
                else:
                    self.vpn_start()
            else:
                self.icon_doubleclick_timer.start(QtWidgets.QApplication.doubleClickInterval())

    def icon_doubleclick_timeout(self):
        """Action performed after single-click on tray icon"""
        pass

    def quit(self):
        """Quit GUI (and ask before quitting if VPN is still running)"""
        if self.vpn_enabled:
            reply = QtWidgets.QMessageBox.question(
                self, self.tr("THU4Over6 - Quit"),
                self.tr("You are still connected to VPN! Do you really want to quit "
                        "4over6 GUI (service will keep running in background)?"),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                QtWidgets.QApplication.quit()
        else:
            QtWidgets.QApplication.quit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("THU4Over6")
    app.setOrganizationDomain("4over6.gycis.me")
    app.setApplicationName("THU4Over6")
    app.setQuitOnLastWindowClosed(False)
    window = THU4Over6Widget()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
