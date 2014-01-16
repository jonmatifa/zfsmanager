#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;

ui_print_header(undef, $text{'snapshot_title'}, "", undef, 1, 1);
$conf = get_zfsmanager_config();

if ($in{'snap'})
{
	print zfs_get($in{'snapshot'}, "all");
} elsif ($in{'new'}) {
	%zfs = list_zfs();
	print "Select filesystem for snapshot";
	print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
	foreach $key (sort(keys %zfs)) 
	{
		print ui_columns_row(["<a href='snapshot.cgi?zfs=$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
	}
	print ui_columns_end();
} elsif ($in{'zfs'}){
	%zfs = list_zfs($in{'zfs'});
	print "Select filesystem for snapshot";
	print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
	foreach $key (sort(keys %zfs)) 
	{
		print ui_columns_row(["<a href='snapshot.cgi?zfs=$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
	}
	print ui_columns_end();
	print "create snapshot based on filesystem: ", $in{'zfs'};
} else {
	%snapshot = list_snapshots();
	print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
	foreach $key (sort(keys %snapshot)) 
	{
		print ui_columns_row(["<a href='snapshot.cgi?snap=$key'>$key</a>", $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
	}
	print ui_columns_end();
}


ui_print_footer('', $text{'index_return'});