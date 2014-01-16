#!/usr/bin/perl

require './zfsmanager-lib.pl';
&ReadParse();
ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1, 0, &help_search_link("zfs, zpool", "man", "doc", "google"), undef, undef, "version 0.0.1" );

$conf = get_zfsmanager_config();

#start tabs
%zpool = list_zpools();
%zfs = list_zfs();
%snapshot = list_snapshots();
@tabs = ();
push(@tabs, [ "pools", "ZFS Pools", "index.cgi?mode=pools" ]);
push(@tabs, [ "zfs", "ZFS File Systems", "index.cgi?mode=zfs" ]);
push(@tabs, [ "snapshot", "Snapshots", "index.cgi?mode=snapshot" ]);
print &ui_tabs_start(\@tabs, "mode", $in{'mode'} || $tabs[0]->[0], 1);

#start pools tab
print &ui_tabs_start_tab("mode", "pools");
print ui_columns_start([ "Pool Name", "Size", "Alloc", "Free", "Cap", "Dedup", "Health"]);
while (my($name, @val) = each(%zpool)) 
{
    print ui_columns_row(["<a href='status.cgi?pool=$name'>$name</a>", $val[0][0], $val[0][1], $val[0][2], $val[0][3], $val[0][4], $val[0][5] ]);
}
print ui_columns_end();
print &ui_tabs_end_tab("mode", "pools");

#start zfs tab
print &ui_tabs_start_tab("mode", "zfs");
print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
while (my($name, @val) = each(%zfs)) 
{
    print ui_columns_row(["<a href='status.cgi?zfs=$name'>$name</a>", $val[0][0], $val[0][1], $val[0][2], $val[0][3] ]);
}
print ui_columns_end();
print &ui_tabs_end_tab("mode", "zfs");

#start snapshots tab
print &ui_tabs_start_tab("mode", "snapshot");
print ui_columns_start([ "Snapshot", "Used", "Avail", "Refer", "Mountpoint" ]);
while (my($name, @val) = each(%snapshot)) 
{
    print ui_columns_row(["<a href='status.cgi?zfs=$name'>$name</a>", $val[0][0], $val[0][1], $val[0][2], $val[0][3] ]);
}
print ui_columns_end();
print &ui_tabs_end_tab("mode", "zfs");

#end tabs
print &ui_tabs_end(1);

#alerts
print "<h3>Alerts:</h3>";


ui_print_footer("/", $text{'index'});
