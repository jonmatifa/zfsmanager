#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;

ui_print_header(undef, $text{'vdev_title'}, "", undef, 1, 1);

my %status = zpool_status($in{'pool'});

print ui_columns_start([ "Virtual Device", "State", "Read", "Write", "Cksum" ]);
print ui_columns_row([$status{$in{'dev'}}{name}, $status{$in{'dev'}}{state}, $status{$in{'dev'}}{read}, $status{$in{'dev'}}{write}, $status{$in{'dev'}}{cksum}]);
print ui_columns_end();

$parent = $status{$in{'dev'}}{parent};
if ($status{$in{'dev'}}{parent} =~ 'pool') 
{
} else {
	print ui_columns_start([ "Parent", "State", "Read", "Write", "Cksum" ]);
	print ui_columns_row(["<a href='config-vdev.cgi?pool=$in{'pool'}&dev=$status{$in{'dev'}}{parent}'>$status{$parent}{name}</a>", $status{$parent}{state}, $status{$parent}{read}, $status{$parent}{write}, $status{$parent}{cksum}]);
	print ui_columns_end();
}
ui_zpool_list($in{'pool'});
if (($status{$in{'dev'}}{name} =~ "cache") || ($status{$in{'dev'}}{name} =~ "logs") || ($status{$in{'dev'}}{name} =~ "spare") || ($status{$in{'dev'}}{name} =~ /mirror/) || ($status{$in{'dev'}}{name} =~ /raidz/))
{
print "Children: ";
	foreach $key (sort(keys %status))
	{
		if ($status{$key}{parent} =~ $in{'dev'}) 
		{
			print "<a href='config-vdev.cgi?pool=$in{pool}&dev=$key'>".$status{$key}{name}."</a>  ";
		}
	}
} elsif ($config{'pool_properties'} =~ /1/) {
	print ui_table_start("Tasks", "width=100%", "10", ['align=left'] );
	if ($status{$in{'dev'}}{state} =~ "ONLINE")	{
		print ui_table_row("Offline: ", "<a href='cmd.cgi?cmd=vdev&action=offline&pool=$in{'pool'}&vdev=$status{$in{'dev'}}{name}'>Bring device offline</a><br />");
	}
	else { #elsif ($status{$in{'dev'}}{state} =~ "OFFLINE") {
		print ui_table_row("Online: ", "<a href='cmd.cgi?cmd=vdev&action=online&pool=$in{'pool'}&vdev=$status{$in{'dev'}}{name}'>Bring device online</a><br />");
	}
	print ui_table_row("Replace: ", "<a href='cmd.cgi?cmd=replace&vdev=$status{$in{'dev'}}{name}&pool=$in{'pool'}'>Replace device</a><br />");
	print ui_table_row("Remove: ", "<a href='cmd.cgi?cmd=vdev&action=remove&pool=$in{'pool'}&vdev=$status{$in{'dev'}}{name}'>Remove device</a><br />");
	print ui_table_row("Detach: ", "<a href='cmd.cgi?cmd=vdev&action=detach&pool=$in{'pool'}&vdev=$status{$in{'dev'}}{name}'>Detach device</a><br />");
	print ui_table_row("Clear: ", "<a href='cmd.cgi?cmd=vdev&action=clear&pool=$in{'pool'}&vdev=$status{$in{'dev'}}{name}'>Clear errors</a><br />");
	print ui_table_end();
}

ui_print_footer("status.cgi?pool=$in{'pool'}", $in{'pool'});
