#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
ui_print_header(undef, $text{'status_title'}, "", undef, 1, 1);
$conf = get_zfsmanager_config();

#show pool status
if ($in{'pool'})
{
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
}

#show filesystem status
if ($in{'zfs'})
{
print zfs_get($in{'zfs'}, "all");
}

#show snapshot status
#if ($in{'snapshot'})
#{
#print snapshot_status($in{'snapshot'});
#}

ui_print_footer('', $text{'index_return'});