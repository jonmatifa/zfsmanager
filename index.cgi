#!/usr/bin/perl

require './zfsmanager-lib.pl';
&ReadParse();
ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1, 0, "<a href='about.cgi'>About ZFS Manager</a><br />".&help_search_link("zfs, zpool", "man", "doc", "google"), undef, undef, $text{'index_version'} );

#start tabs
@tabs = ();
push(@tabs, [ "pools", "ZFS Pools", "index.cgi?mode=pools" ]);
push(@tabs, [ "zfs", "ZFS File Systems", "index.cgi?mode=zfs" ]);
if ($config{'show_snap'} =~ /1/) { push(@tabs, [ "snapshot", "Snapshots", "index.cgi?mode=snapshot" ]); }
print &ui_tabs_start(\@tabs, "mode", $in{'mode'} || $tabs[0]->[0], 1);

#start pools tab
print &ui_tabs_start_tab("mode", "pools");

ui_zpool_list();
if ($config{'pool_properties'} =~ /1/) { 
	print "<a href='create.cgi?create=zpool'>Create new pool<a/>";
	print " | ";
	print "<a href='create.cgi?import=1'>Import pool<a/>"; 
}
print &ui_tabs_end_tab("mode", "pools");

#start zfs tab
print &ui_tabs_start_tab("mode", "zfs");

print "<div>"; #div tags are needed for new theme apparently
ui_zfs_list();
if ($config{'zfs_properties'} =~ /1/) { print "<a href='create.cgi?create=zfs'>Create file system</a>"; }
print "</div>";
print &ui_tabs_end_tab("mode", "zfs");

#start snapshots tab
if ($config{'show_snap'} =~ /1/) {
print &ui_tabs_start_tab("mode", "snapshot");
ui_list_snapshots(undef, 1);
if ($config{'snap_properties'} =~ 1) { print "<a href='create.cgi?create=snapshot'>Create snapshot</a>"; }
print &ui_tabs_end_tab("mode", "snapshot");
}

#end tabs
print &ui_tabs_end(1);

#alerts
print "<h3>Alerts: </h3>", get_alerts(), "";

ui_print_footer("/", $text{'index'});
