#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
$conf = get_zfsmanager_config();

#show pool status
if ($in{'pool'})
{
ui_print_header(undef, $text{'status_title'}, "", undef, 1, 1);

#Show pool information
print "Pool:";
ui_zpool_status($in{'pool'});

#show properties for pool
ui_zpool_properties($in{'pool'});

#Show associated file systems
%zfs = list_zfs("-r ".$in{'pool'});
print "Filesystems:";
print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
foreach $key (sort(keys %zfs)) 
{
    print ui_columns_row(["<a href='status.cgi?zfs=$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
}
print ui_columns_end();
print "<a href='create.cgi?create=zfs&pool=$in{'pool'}'>Create new file system</a><br />";

#Show device configuration
#TODO: show devices by vdev hierarchy
my %status = zpool_status($in{'pool'});
print "Config:";
print ui_columns_start([ "Name", "State", "Read", "Write", "Cksum" ]);
foreach $key (sort(keys %status)) 
{
	if (($status{$key}{parent} eq "pool") || ($status{$key}{name} !~ $status{pool}{pool})) {
		print ui_columns_row(["<a href='config-vdev.cgi?pool=$status{pool}{pool}&dev=$status{$key}{name}'>$status{$key}{name}</a>", $status{$key}{state}, $status{$key}{read}, $status{$key}{write}, $status{$key}{cksum}]);
		#if (($status{$key}{name} =~ /logs/) || ($status{$key}{name} =~ /cache/) || ($status{$key}{name} =~ /mirror/) || ($status{$key}{name} =~ /raidz/))
		#{
		
		#}
	}
	#print ui_columns_row(["<a href=''>$status{$key}{name}</a>", $status{$key}{state}, $status{$key}{read}, $status{$key}{write}, $status{$key}{cksum}, $status{$key}{parent}]);
}
print ui_columns_end();
print "<table border=0px width=100%><tr>";
print "<td width=40%>Scan: ", $status{pool}{scan}, " </td>";
print "<td width=20%>Read: ", $status{pool}{read}, " </td>";
print "<td width=20%>Write: ", $status{pool}{write}, " </td>";
print "<td width=20%>Cksum: ", $status{pool}{cksum}, " </td>";
print "</tr></table>";
print "Errors: ", $status{pool}{errors}, "<br />";
ui_print_footer('', $text{'index_return'});
}

#show filesystem status
if ($in{'zfs'})
{
	ui_print_header(undef, "ZFS File System", "", undef, 1, 1);
	#start tabs
	
	#@tabs = ();
	#push(@tabs, [ "status", "Status", "index.cgi?mode=status&zfs=$in{'zfs'}" ]);
	#push(@tabs, [ "edit", "Edit", "index.cgi?mode=edit&zfs=$in{'zfs'}" ]);
	#push(@tabs, [ "snapshot", "Snapshots", "index.cgi?mode=snapshot&zfs=$in{'zfs'}" ]);
	#print &ui_tabs_start(\@tabs, "mode", $in{'mode'} || $tabs[0]->[0], 1);

	#start status tab
	#print &ui_tabs_start_tab("mode", "status");
	ui_zfs_list($in{'zfs'});

	#show properties for filesystem
	ui_zfs_properties($in{'zfs'});
	print ui_popup_link("Destroy this file system", "cmd.cgi?destroy=$in{'zfs'}"), "<br />";
	#show list of snapshots based on filesystem
	print "Snapshots on this filesystem: <br />";
	ui_list_snapshots($in{'zfs'});
	ui_create_snapshot($in{'zfs'});
	ui_print_footer('index.cgi?mode=zfs', $text{'zfs_return'});
}

#show snapshot status
#if ($in{'snapshot'})
#{
#ui_print_header(undef, "ZFS File System Status", "", undef, 1, 1);
#print snapshot_status($in{'snapshot'});
#ui_print_footer('', $text{'snapshot_return'});
#}

