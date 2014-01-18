#!/usr/bin/perl

require './zfsmanager-lib.pl';
&ReadParse();
use Data::Dumper;
ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1, 0, &help_search_link("zfs, zpool", "man", "doc", "google"), undef, undef, $text{'index_version'} );

$conf = get_zfsmanager_config();

#start tabs
@tabs = ();
push(@tabs, [ "pools", "ZFS Pools", "index.cgi?mode=pools" ]);
push(@tabs, [ "zfs", "ZFS File Systems", "index.cgi?mode=zfs" ]);
push(@tabs, [ "snapshot", "Snapshots", "index.cgi?mode=snapshot" ]);
print &ui_tabs_start(\@tabs, "mode", $in{'mode'} || $tabs[0]->[0], 1);

#start pools tab
print &ui_tabs_start_tab("mode", "pools");
%zpool = list_zpools();
print ui_columns_start([ "Pool Name", "Size", "Alloc", "Free", "Cap", "Dedup", "Health"]);
foreach $key (sort(keys %zpool))
{
    print ui_columns_row(["<a href='status.cgi?pool=$key'>$key</a>", $zpool{$key}{size}, $zpool{$key}{alloc}, $zpool{$key}{free}, $zpool{$key}{cap}, $zpool{$key}{dedup}, $zpool{$key}{health} ]);
}
print ui_columns_end();
print &ui_tabs_end_tab("mode", "pools");

#start zfs tab
print &ui_tabs_start_tab("mode", "zfs");
%zfs = list_zfs();
print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
foreach $key (sort(keys %zfs)) 
{
    print ui_columns_row(["<a href='status.cgi?zfs=$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
}
print ui_columns_end();
print &ui_tabs_end_tab("mode", "zfs");

#start snapshots tab
print &ui_tabs_start_tab("mode", "snapshot");
ui_list_snapshots();
print "<a href='snapshot.cgi?new=1'>Create snapshot</a>";
print &ui_tabs_end_tab("mode", "snapshot");

#end tabs
print &ui_tabs_end(1);

#alerts
print "<h3>Alerts: </h3>", get_alerts(), "";

ui_print_footer("/", $text{'index'});
