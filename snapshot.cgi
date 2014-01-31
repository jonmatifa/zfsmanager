#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;

%conf = get_zfsmanager_config();

#show status of current snapshot
if ($in{'snap'})
{
	ui_print_header(undef, $text{'snapshot_title'}, "", undef, 1, 1);
	#print zfs_get($in{'snap'}, "all");
	%snapshot = list_snapshots($in{'snap'});
	print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
	foreach $key (sort(keys %snapshot)) 
	{
		print ui_columns_row(["<a href='snapshot.cgi?snap=$key'>$key</a>", $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
	}
	print ui_columns_end();
	ui_zfs_properties($in{'snap'});

	#print "<a href='cmd.cgi?destroy=", $in{'snap'}, "'>Destroy snapshot</a> |";
	my $zfs = $in{'snap'};
	$zfs =~ s/\@.*//;
	#if ($conf{'snap_properties'} =~ /1/) { print " <a href='snapshot.cgi?zfs=", $zfs, "'>Create new snapshot based on ", $zfs, "</a> | Rename snapshot "; }
	#if (($conf{'snap_properties'} =~ /1/) && ($conf{'zfs_properties'} =~ /1/)) { print " | Clone snapshot | Rollback to snapshot | Send snapshot "; }
	#if ($conf{'snap_destroy'} =~ /1/) { print "| ", ui_popup_link('Destroy snapshot', "cmd.cgi?destroy=".$in{'snap'}); }
	print ui_table_start('Tasks', 'width=100%', undef);
	print ui_table_row('Differences', "Show differences in $in{'snap'}");
	if ($conf{'snap_properties'} =~ /1/) { 
		print ui_table_row('Snapshot:', "<a href='snapshot.cgi?zfs=$zfs'>Create new snapshot based on $zfs</a>");
		print ui_table_row('Rename:', "Rename $in{'snap'}");
	}
	if ($conf{'zfs_properties'} =~ /1/) { 
		print ui_table_row('Clone:', ui_popup_link("Clone $in{'snap'} to new file system", "create.cgi?clone=".$in{'snap'})); 
		print ui_table_row('Send:', ui_popup_link("Send $in{'snap'}", "create.cgi?send=".$in{'snap'}));
	}
	if (($conf{'snap_properties'} =~ /1/) && ($conf{'zfs_properties'} =~ /1/)) { 
		#print ui_table_row('Clone:', "Clone $in{'snap'} to new file system"); 
		print ui_table_row('Rollback:', "Rollback $zfs to $in{'snap'}");
		#print ui_table_row('Send:', "Send $in{'snap'}");
	}
	if ($conf{'snap_destroy'} =~ /1/) { print ui_table_row('Destroy:', ui_popup_link('Destroy snapshot', "cmd.cgi?destroysnap=".$in{'snap'})); }
	print ui_table_end();

#prompt for which filesystem snapshot should be based on
} elsif ($in{'new'}) {
	ui_print_header(undef, $text{'snapshot_new'}, "", undef, 1, 1);
	%zfs = list_zfs();
	#print "Select filesystem for snapshot";
	print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
	foreach $key (sort(keys %zfs)) 
	{
		print ui_columns_row(["<a href='snapshot.cgi?zfs=$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
	}
	print ui_columns_end();
#handle creation of snapshot
} elsif ($in{'zfs'}){
	ui_print_header(undef, $text{'snapshot_create'}, "", undef, 1, 1);
	%zfs = list_zfs($in{'zfs'});
	print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
	foreach $key (sort(keys %zfs)) 
	{
		print ui_columns_row(["<a href='status.cgi?zfs=$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
	}
	print ui_columns_end();
	#show list of snapshots based on filesystem
	print "Snapshots already on this filesystem: <br />";
	%snapshot = list_snapshots();
	print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
	foreach $key (sort(keys %snapshot)) 
	{
		if ($key =~ ($in{'zfs'}."@") ) { print ui_columns_row(["<a href='snapshot.cgi?snap=$key'>$key</a>", $snapshot{$key}{used}, $snapshot{$key}{refer} ]); }
	}
	print ui_columns_end();
	print ui_create_snapshot($in{'zfs'});
} else {
	%snapshot = list_snapshots();
	print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
	foreach $key (sort(keys %snapshot)) 
	{
		print ui_columns_row(["<a href='snapshot.cgi?snap=$key'>$key</a>", $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
	}
	print ui_columns_end();
}


ui_print_footer('index.cgi?mode=snapshot', $text{'snapshot_return'});
