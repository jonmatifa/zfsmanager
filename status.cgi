#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
$conf = get_zfsmanager_config();

#show pool status
if ($in{'pool'})
{
ui_print_header(undef, $text{'status_title'}, "", undef, 1, 1);
%status = zpool_status($in{'pool'});
#print Dumper(\%status);

#Show pool information
%zpool = list_zpools($in{'pool'});
print "Pool:";
print ui_columns_start([ "Pool Name", "Size", "Alloc", "Free", "Cap", "Dedup", "Health"]);
foreach $key (sort(keys %zpool))
{
    print ui_columns_row(["<a href='status.cgi?pool=$key'>$key</a>", $zpool{$key}{size}, $zpool{$key}{alloc}, $zpool{$key}{free}, $zpool{$key}{cap}, $zpool{$key}{dedup}, $zpool{$key}{health} ]);
}
print ui_columns_end();

#Show associated file systems
%zfs = list_zfs("-r ".$in{'pool'});
print "Filesystems:";
print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
foreach $key (sort(keys %zfs)) 
{
    print ui_columns_row(["<a href='status.cgi?zfs=$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
}
print ui_columns_end();

#Show device configuration
#TODO: show devices by vdev hierarchy 
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
	%zfs = list_zfs($in{'zfs'});
	print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
	foreach $key (sort(keys %zfs)) 
	{
		print ui_columns_row(["<a href='status.cgi?zfs=$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
	}
	print ui_columns_end();

	#show properties for filesystem
	my %hash = zfs_get($in{'zfs'}, "all");
	my %properties = properties_list();
	#my %boolean = map { $_ => 1 } @properties;
	#print Dumper(\%properties);
	#print $properties{boolean}[0];
	print ui_table_start("Properties", "width=100%", "10");
	foreach $key (sort(keys $hash{$in{'zfs'}}))
	{
		if ($properties{$key} =~ 'boolean')
		{
			if ($hash{$in{'zfs'}}{$key}{value} =~ "on") {
				print ui_table_row(ui_popup_link($key,'cmd.cgi?zfs='.$in{zfs}.'&property='.$key.'&set=off'), $hash{$in{'zfs'}}{$key}{value});
			} else {
				print ui_table_row(ui_popup_link($key,'cmd.cgi?zfs='.$in{zfs}.'&property='.$key.'&set=on'), $hash{$in{'zfs'}}{$key}{value});
			}
		} else {
		print ui_table_row($key, $hash{$in{'zfs'}}{$key}{value});
		}
	}
	print ui_table_end();

	#show list of snapshots based on filesystem
	print "Snapshots on this filesystem: <br />";
	%snapshot = list_snapshots();
	print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
	foreach $key (sort(keys %snapshot)) 
	{
		if ($key =~ ($in{'zfs'}."@") ) { print ui_columns_row(["<a href='snapshot.cgi?snap=$key'>$key</a>", $snapshot{$key}{used}, $snapshot{$key}{refer} ]); }
	}
	print ui_columns_end();
	ui_create_snapshot($in{'zfs'});
	#print &ui_tabs_end_tab("mode", "status");
	
	#show edit tab
	#print &ui_tabs_start_tab("mode", "edit");

	#print &ui_tabs_end_tab("mode", "edit");
	
	#start snapshot tab
	#print &ui_tabs_start_tab("mode", "snapshot");

	#print &ui_tabs_end_tab("mode", "snapshot");
	
	#print &ui_tabs_end(1);
	ui_print_footer('index.cgi?mode=zfs', $text{'zfs_return'});
}

#show snapshot status
#if ($in{'snapshot'})
#{
#ui_print_header(undef, "ZFS File System Status", "", undef, 1, 1);
#print snapshot_status($in{'snapshot'});
#ui_print_footer('', $text{'snapshot_return'});
#}

