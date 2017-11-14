ZFS Manager
==========

ZFS administration tool for Webmin

This is in early development, not for production. That being said, try this out in a virtual machine or anywhere else where data is non-critical. My hope is that this will ultimately provide Webmin with similar ZFS functionality to FreeNAS and NAS4Free.

This project lives at https://github.com/jonmatifa/zfsmanager provide all feedback and bug reports there. I am brand new to Perl and Webmin's API. so first I apologize for the shabby state the code is in, second any further contributions are greatly welcomed. I am learning a fair amount about ZFS along the way as well.

I am currently developing this under ZFS on Linux in Ubuntu, but all varients of ZFS/Webmin are planned to be supported in the future.

**Installation**

You can either use a *.wbm.gz from the releases tab, or "# git clone https://github.com/jonmatifa/zfsmanager.git" from the webmin root directory (Centos/REHL: /usr/libexec/webmin, Debian/Ubuntu: /usr/share/webmin), this will clone everything into the zfsmanager subfolder (which will be created). Then copy the "config" file to /etc/webmin/zfsmanager once that is done, you can then keep up to date with by "# git pull" from the webmin/zfsmanager directory.

**Feedback**

I am interested in what you think, even during this early alpha phase. The issue tracker can be used not only for bug reports but also feature requests and comments in general. Tracking and fixing bugs is important, but I also want to know what you think about the idea of the project and things like usability and UI design.

**Contribution**

Right now its just me developing this. I'm not a programmer by trade, but I'm happy to work on this project whenever I can. I would love help from someone more seasoned at perl (don't judge me too hard), but also someone who "gets" the design philosophy of this project and understands the Webmin API. I'm a beginner myself so I'm not looking for too much.

**Thank you**

Thank you for stopping by and I hope you enjoy this plugin!
