#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;

#show pool status
if ($in{'pool'})
{
ui_print_header(undef, $text{'status_title'}, "", undef, 1, 1);

#Show pool information
ui_zpool_list($in{'pool'});

#show properties for pool
ui_zpool_properties($in{'pool'});

#Show associated file systems

ui_zfs_list("-r ".$in{'pool'});

#Show device configuration
#TODO: show devices by vdev hierarchy
my %status = zpool_status($in{'pool'});
print ui_columns_start([ "Virtual Device", "State", "Read", "Write", "Cksum" ]);
foreach $key (sort {$a <=> $b} (keys %status))
{
	if (($status{$key}{parent} =~ /pool/) && ($key != 0)) {
		print ui_columns_row(["<a href='config-vdev.cgi?pool=".$status{0}{pool}.'&dev='.$key."'>".$status{$key}{name}."</a>", $status{$key}{state}, $status{$key}{read}, $status{$key}{write}, $status{$key}{cksum}]);
	} elsif ($key != 0) {
		print ui_columns_row(["<a href='config-vdev.cgi?pool=".$status{0}{pool}.'&dev='.$key."'>|_".$status{$key}{name}."</a>", $status{$key}{state}, $status{$key}{read}, $status{$key}{write}, $status{$key}{cksum}]);
	}
	
}
print ui_columns_end();
print ui_table_start("Status", "width=100%", "10");
print ui_table_row("Scan:", $status{0}{scan});
print ui_table_row("Read:", $status{0}{read});
print ui_table_row("Write:", $status{0}{write});
print ui_table_row("Checkum:", $status{0}{cksum});
print ui_table_row("Errors:", $status{0}{errors});
print ui_table_end();

if ($status{0}{status} or $status{0}{action} or $status{pool}{see}) {
	print ui_table_start("Attention", "width=100%", "10");
	if ($status{0}{status}) { print ui_table_row("Status:", $status{0}{status}); }
	if ($status{0}{action}) { print ui_table_row("Action:", $status{0}{action}); }
	if ($status{0}{see}) { print ui_table_row("See:", $status{0}{see}); }
	print ui_table_end();
}
	

#--tasks table--
print ui_table_start("Tasks", "width=100%", "10", ['align=left'] );
if ($config{'zfs_properties'} =~ /1/) { 
	print ui_table_row("New file system: ", "<a href='create.cgi?create=zfs&parent=$in{pool}'>Create file system</a>"); 
}
if ($config{'pool_properties'} =~ /1/) { 
	if ($status{0}{scan} =~ /scrub in progress/) { print ui_table_row('Scrub ',"<a href='cmd.cgi?cmd=scrub&stop=y&pool=$in{pool}'>Stop scrub</a>"); } 
	else { print ui_table_row('Scrub ', "<a href='cmd.cgi?cmd=scrub&pool=$in{pool}'>Scrub pool</a>");}
	print ui_table_row('Upgrade ', "<a href='cmd.cgi?cmd=upgrade&pool=$in{pool}'>Upgrade pool</a>");
	print ui_table_row('Export ',  "<a href='cmd.cgi?cmd=export&pool=$in{pool}'>Export pool</a>");
}
if ($config{'pool_destroy'} =~ /1/) { print ui_table_row("Destroy ", "<a href='cmd.cgi?cmd=pooldestroy&pool=$in{pool}'>Destroy this pool</a>"); }
print ui_table_end();

ui_print_footer('', $text{'index_return'});
}

#show filesystem status
if ($in{'zfs'})
{
	ui_print_header(undef, "ZFS File System", "", undef, 1, 1);
	#start status tab
	ui_zfs_list($in{'zfs'});

	#show properties for filesystem
	ui_zfs_properties($in{'zfs'});
	
	#show list of snapshots based on filesystem
	ui_list_snapshots('-rd1 '.$in{'zfs'}, 1);
	my %hash = zfs_get($in{'zfs'}, "all");
	
	#--tasks table--
	print ui_table_start("Tasks", "width=100%", "10");
	if ($config{'snap_properties'} =~ /1/) { print ui_table_row("Snapshot: ", ui_create_snapshot($in{'zfs'})); }
	if ($config{'zfs_properties'} =~ /1/) { 
		print ui_table_row("New file system: ", "<a href='create.cgi?create=zfs&parent=".$in{'zfs'}."'>Create child file system</a>"); 
		if (index($in{'zfs'}, '/') != -1) { print ui_table_row("Rename: ", "<a href='create.cgi?rename=".$in{'zfs'}."'>Rename ".$in{'zfs'}."</a>"); }
		if ($hash{$in{'zfs'}}{origin}) { print ui_table_row("Promote: ", "This file system is a clone, <a href='cmd.cgi?cmd=promote&zfs=$in{zfs}'>promote $in{zfs}</a>"); }
	}
	if ($config{'zfs_destroy'} =~ /1/) { print ui_table_row("Destroy: ", "<a href='cmd.cgi?cmd=zfsdestroy&zfs=$in{zfs}'>Destroy this file system</a>"); }
	print ui_table_end();
	ui_print_footer('index.cgi?mode=zfs', $text{'zfs_return'});
	
}

#show snapshot status
#show status of current snapshot
if ($in{'snap'})
{
	ui_print_header(undef, $text{'snapshot_title'}, "", undef, 1, 1);
	%snapshot = list_snapshots($in{'snap'});
	print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
	foreach $key (sort(keys %snapshot)) 
	{
		print ui_columns_row(["<a href='status.cgi?snap=$snapshot{$key}{name}'>$snapshot{$key}{name}</a>", $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
	}
	print ui_columns_end();
	ui_zfs_properties($in{'snap'});

	my $zfs = $in{'snap'};
	$zfs =~ s/\@.*//;
	
	#--tasks table--
	print ui_table_start('Tasks', 'width=100%', undef);
	print ui_table_row('Differences', "<a href='diff.cgi?snap=$in{snap}'>Show differences in $in{'snap'}</a>");
	if ($config{'snap_properties'} =~ /1/) { 
		print ui_table_row("Snapshot: ", ui_create_snapshot($zfs));
		print ui_table_row("Rename: ", "<a href='create.cgi?rename=".$in{'snap'}."'>Rename ".$in{'snap'}."</a>");
		print ui_table_row("Send: ", "<a href='cmd.cgi?cmd=send&snap=".$in{'snap'}."'>Send ".$in{'snap'}." to gzip</a>");
	}
	if ($config{'zfs_properties'} =~ /1/) { 
		print ui_table_row('Clone:', "<a href='create.cgi?clone=$in{snap}'>Clone $in{'snap'} to new file system</a>"); 
		print ui_table_row('Rollback:', "Rollback $zfs to $in{'snap'}");
	}
	if (($config{'snap_properties'} =~ /1/) && ($config{'zfs_properties'} =~ /1/)) { 
	}
	if ($config{'snap_destroy'} =~ /1/) { print ui_table_row('Destroy:',"<a href='cmd.cgi?cmd=snpdestroy&snapshot=$in{snap}'>Destroy snapshot</a>", ); }
	print ui_table_end();
	%parent = find_parent($in{'snap'});
	ui_print_footer('status.cgi?zfs='.$parent{'filesystem'}, $parent{'filesystem'});
}

