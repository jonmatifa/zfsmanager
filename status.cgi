#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
%conf = get_zfsmanager_config();

#show pool status
if ($in{'pool'})
{
ui_print_header(undef, $text{'status_title'}, "", undef, 1, 1);

#Show pool information
#print "Pool:";
ui_zpool_status($in{'pool'});

#show properties for pool
ui_zpool_properties($in{'pool'});

#Show associated file systems
%zfs = list_zfs("-r ".$in{'pool'});
#print "Filesystems:";
print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
foreach $key (sort(keys %zfs)) 
{
    print ui_columns_row(["<a href='status.cgi?zfs=$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
}
print ui_columns_end();

#Show device configuration
#TODO: show devices by vdev hierarchy
my %status = zpool_status($in{'pool'});
#print "Config:";
print ui_columns_start([ "Virtual Device", "State", "Read", "Write", "Cksum" ]);
foreach $key (keys %status)
{
	if (($status{$key}{parent} =~ /pool/) && ($status{$key}{name} !~ $status{pool}{pool})) {
		print ui_columns_row(["<a href='config-vdev.cgi?pool=".$status{pool}{pool}.'&dev='.$status{$key}{name}."'>".$status{$key}{name}."</a>", $status{$key}{state}, $status{$key}{read}, $status{$key}{write}, $status{$key}{cksum}]);
		#print ui_columns_row([ui_popup_link($status{$key}{name}, 'config-vdev.cgi?pool='.$status{pool}{pool}.'&dev='.$status{$key}{name}), $status{$key}{state}, $status{$key}{read}, $status{$key}{write}, $status{$key}{cksum}]);
		#if (($status{$key}{name} =~ /logs/) || ($status{$key}{name} =~ /cache/) || ($status{$key}{name} =~ /mirror/) || ($status{$key}{name} =~ /raidz/))
		#{
		
		#}
	} elsif ($status{$key}{name} !~ $status{pool}{pool}) {
		print ui_columns_row(['|_'.ui_popup_link($status{$key}{name}, 'config-vdev.cgi?pool='.$status{pool}{pool}.'&dev='.$status{$key}{name}), $status{$key}{state}, $status{$key}{read}, $status{$key}{write}, $status{$key}{cksum}]);
		#print ui_columns_row(['|_'.ui_popup_link($status{$key}{name}, 'config-vdev.cgi?pool='.$status{pool}{pool}.'&dev='.$status{$key}{name}), $status{$key}{state}, $status{$key}{read}, $status{$key}{write}, $status{$key}{cksum}]);
	}
	
	#print ui_columns_row(["<a href=''>$status{$key}{name}</a>", $status{$key}{state}, $status{$key}{read}, $status{$key}{write}, $status{$key}{cksum}, $status{$key}{parent}]);
}
print ui_columns_end();
#print ui_table_start("Status", "width=100%", "10");
#print test_function($in{'pool'});
#print ui_table_row("Scan:", $status{pool}{scan});
#print ui_table_row("Read:", $status{pool}{read});
#print ui_table_row("Write:", $status{pool}{write});
#print ui_table_row("Checkum:", $status{pool}{cksum});
#print ui_table_row("Errors:", $status{pool}{errors});
#print ui_table_end();

#--tasks table--
print ui_table_start("Tasks", "width=100%", "10", ['align=left'] );
#print ui_table_row("Snapshot: ", ui_create_snapshot($in{'zfs'}));
if ($conf{'zfs_properties'} =~ /1/) { 
	print ui_table_row("New file system: ", "<a href='create.cgi?create=zfs&parent=$in{pool}'>Create file system</a>"); 
	print ui_table_row('Export ',  "<a href='cmd.cgi?export=$in{pool}'>Export pool</a>");
	#print ui_table_row("New file system: ", ui_popup_link('Create file system', "create.cgi?create=zfs&parent=$in{'pool'}")); 
	#print ui_table_row('Export ', ui_popup_link('Export pool', "cmd.cgi?export=$in{'pool'}"));
}
if ($conf{'pool_properties'} =~ /1/) { 
	if ($status{pool}{scan} =~ /scrub in progress/) { print ui_table_row('Scrub ',"<a href='cmd.cgi?scrubstop=$in{pool}'>Stop scrub</a>"); } 
	else { print ui_table_row('Scrub ', "<a href='cmd.cgi?scrub=$in{pool}'>Scrub pool</a>");}
	#if ($status{pool}{scan} =~ /scrub in progress/) { print ui_table_row('Scrub ', ui_popup_link('Stop scrub', "cmd.cgi?scrubstop=$in{'pool'}"));
	#} else { print ui_table_row('Scrub ', ui_popup_link('Scrub pool', "cmd.cgi?scrub=$in{'pool'}"));}
}
if ($conf{'pool_destroy'} =~ /1/) { print ui_table_row("Destroy ", "<a href='cmd.cgi?destroypool=$in{pool}'>Destroy this pool</a>"); }
#if ($conf{'pool_destroy'} =~ /1/) { print ui_table_row("Destroy ", ui_popup_link("Destroy this pool", "cmd.cgi?destroypool=$in{'pool'}")); }
print ui_table_end();
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
	ui_zfs_list('-r '.$in{'zfs'});

	#show properties for filesystem
	ui_zfs_properties($in{'zfs'});
	#print Dumper(\%ary)."<br />";
	
	#show list of snapshots based on filesystem
	#print "Snapshots on this filesystem: <br />";
	ui_list_snapshots('-rd1 '.$in{'zfs'}, 1);
	my %hash = zfs_get($in{'zfs'}, "all");
	
	#--tasks table--
	print ui_table_start("Tasks", "width=100%", "10");
	if ($conf{'snap_properties'} =~ /1/) { print ui_table_row("Snapshot: ", ui_create_snapshot($in{'zfs'})); }
	if ($conf{'zfs_properties'} =~ /1/) { 
		#print ui_table_row("New file system: ", ui_popup_link('Create child file system', "create.cgi?create=zfs&parent=$in{'zfs'}")); 
		print ui_table_row("New file system: ", "<a href='create.cgi?create=zfs&parent=".$in{'zfs'}."'>Create child file system</a>"); 
		if ($hash{$in{'zfs'}}{origin}) { print ui_table_row("Promote: ", "This file system is a clone, <a href='cmd.cgi?promote=$in{zfs}'>promote $in{zfs}</a>"); }
		#if ($hash{$in{'zfs'}}{origin}) { print ui_table_row("Promote: ", "This file system is a clone, ".ui_popup_link("promote $in{'zfs'}", "cmd.cgi?promote=$in{'zfs'}")); }
	}
	if ($conf{'zfs_destroy'} =~ /1/) { print ui_table_row("Destroy: ", "<a href='cmd.cgi?destroy=$in{zfs}'>Destroy this file system</a>"); }
	#if ($conf{'zfs_destroy'} =~ /1/) { print ui_table_row("Destroy: ", ui_popup_link("Destroy this file system", "cmd.cgi?destroy=$in{'zfs'}")); }
	print ui_table_end();
	ui_print_footer('index.cgi?mode=zfs', $text{'zfs_return'});
	
}

#show snapshot status
#show status of current snapshot
if ($in{'snap'})
{
	ui_print_header(undef, $text{'snapshot_title'}, "", undef, 1, 1);
	#print zfs_get($in{'snap'}, "all");
	%snapshot = list_snapshots($in{'snap'});
	print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
	foreach $key (sort(keys %snapshot)) 
	{
		print ui_columns_row(["<a href='status.cgi?snap=$key'>$key</a>", $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
	}
	print ui_columns_end();
	ui_zfs_properties($in{'snap'});

	#print "<a href='cmd.cgi?destroy=", $in{'snap'}, "'>Destroy snapshot</a> |";
	my $zfs = $in{'snap'};
	$zfs =~ s/\@.*//;
	
	#--tasks table--
	print ui_table_start('Tasks', 'width=100%', undef);
	print ui_table_row('Differences', "Show differences in $in{'snap'}");
	if ($conf{'snap_properties'} =~ /1/) { 
		#print ui_table_row('Snapshot:', "<a href='snapshot.cgi?zfs=$zfs'>Create new snapshot based on $zfs</a>");
		print ui_table_row("Snapshot: ", ui_create_snapshot($zfs));
		print ui_table_row('Rename:', "Rename $in{'snap'}");
	}
	if ($conf{'zfs_properties'} =~ /1/) { 
		print ui_table_row('Clone:', "<a href='create.cgi?clone=$in{snap}'>Clone $in{'snap'} to new file system</a>"); 
		#print ui_table_row('Clone:', ui_popup_link("Clone $in{'snap'} to new file system", "create.cgi?clone=".$in{'snap'})); 
		#print ui_table_row('Send:', ui_popup_link("Send $in{'snap'}", "create.cgi?send=".$in{'snap'}));
	}
	if (($conf{'snap_properties'} =~ /1/) && ($conf{'zfs_properties'} =~ /1/)) { 
		#print ui_table_row('Clone:', "Clone $in{'snap'} to new file system"); 
		print ui_table_row('Rollback:', "Rollback $zfs to $in{'snap'}");
		#print ui_table_row('Send:', "Send $in{'snap'}");
	}
	if ($conf{'snap_destroy'} =~ /1/) { print ui_table_row('Destroy:',"<a href='cmd.cgi?destroysnap=$in{snap}'>Destroy snapshot</a>", ); }
	#if ($conf{'snap_destroy'} =~ /1/) { print ui_table_row('Destroy:', ui_popup_link('Destroy snapshot', "cmd.cgi?destroysnap=".$in{'snap'})); }
	print ui_table_end();
	ui_print_footer('index.cgi?mode=snapshot', $text{'snapshot_return'});
}

