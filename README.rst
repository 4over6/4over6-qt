4over6-qt
========

Client GUI for a custom 4over6 tunnel

Requirements
------------

- Python >= 3.3
- PyQt 5
- 4over6
- systemd with journald
- sudo and/or kdesu

Usage
-----

If you want to use systemctl without password prompt, you should add this line to /etc/sudoers (use visudo command for it)::

    %wheel ALL=(ALL) NOPASSWD: /usr/bin/systemctl

And then add yourself to wheel group::

    gpasswd -a your_username wheel

An alternative is to use kdesu instead of sudo (set this in QOpenVPN settings), but then you have to use password for every operation.

You should also add yourself to adm group for log viewer to work::

    gpasswd -a your_username adm
