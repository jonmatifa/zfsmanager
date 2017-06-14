#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();

#show pool status
ui_print_header(undef, $text{'about_title'}, "", undef, 1, 1);

print ui_table_start("ZFS Manager info", "width=100%", undef);
print "ZFS manager is in early development but relatively stable. Please understand the risks and have backups for important data. Updates, feedback, bug reports and more information can be found through the github link below.<br />";
print ui_table_row("GitHub:", "<a href='https://github.com/jonmatifa/zfsmanager' target='_blank'>https://github.com/jonmatifa/zfsmanager</a>");
print ui_table_row("Blog:", "<a href='https://zfsmanager.wordpress.com/' target='_blank'>https://zfsmanager.wordpress.com/</a>");
print ui_table_end();

print ui_table_start("ZFS general info", "width=100%", undef);
print ui_table_row("OpenZFS Main Page", "<a href='http://www.open-zfs.org/wiki/Main_Page' target='_blank'>http://www.open-zfs.org/wiki/Main_Page</a>");
print ui_table_row("FreeBSD wiki on ZFS", "<a href='https://wiki.freebsd.org/ZFS' target='_blank'>https://wiki.freebsd.org/ZFS</a>");
print ui_table_row("ZFS on Linux:", "<a href='http://zfsonlinux.org/' target='_blank'>http://zfsonlinux.org/</a>");
print ui_table_end();


ui_print_footer('', $text{'index_return'});
