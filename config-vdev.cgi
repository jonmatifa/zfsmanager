#!/usr/bin/perl

require './zfsmanager-lib.pl';
#foreign_require("fdisk", "fdisk-lib.pl");
#foreign_require("mount", "mount-lib.pl");
ReadParse();
use Data::Dumper;

ui_print_header(undef, $text{'vdev_title'}, "", undef, 1, 1);
#popup_header($text{'cmd_title'});

#%conf = get_zfsmanager_config();

my %status = zpool_status($in{'pool'});

#print Dumper(\%status);
#foreach $key (sort(keys %status))
#{
#	if ($status{$key}{name} =~ $in{'dev'})
#	{
#		my %dev = $status{$key};
#		#print "seeing device";
#	}
#}
print ui_columns_start([ "Virtual Device", "State", "Read", "Write", "Cksum" ]);
print ui_columns_row([$status{$in{'dev'}}{name}, $status{$in{'dev'}}{state}, $status{$in{'dev'}}{read}, $status{$in{'dev'}}{write}, $status{$in{'dev'}}{cksum}]);
print ui_columns_end();

#print ui_table_start($text{'vdev_title'}, "width=100%", "10", ['align=left'] );
#print "Pool: ", $status{0}{pool}, "<br />";
#print "Pool State: ", $status{0}{state}, "<br />";
#print "Virtual Device: ", $status{$in{'dev'}}{name}, "<br />";
$parent = $status{$in{'dev'}}{parent};
if ($status{$in{'dev'}}{parent} =~ 'pool') 
{
	#print "Parent: <a href='status.cgi?pool=", $status{pool}{pool}, "'>pool</a><br />";
	#print "Parent: pool<br />";
} else {
	print ui_columns_start([ "Parent", "State", "Read", "Write", "Cksum" ]);
	print ui_columns_row(["<a href='config-vdev.cgi?pool=$in{'pool'}&dev=$status{$in{'dev'}}{parent}'>$status{$parent}{name}</a>", $status{$parent}{state}, $status{$parent}{read}, $status{$parent}{write}, $status{$parent}{cksum}]);
	print ui_columns_end();
	#print "Parent: <a href='config-vdev.cgi?pool=", $in{'pool'}, "&dev=", $status{$in{'dev'}}{parent}, "'>", $status{$in{'dev'}}{parent}, "</a><br />";
}
#ui_zpool_status($in{'pool'});
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
	#print "VDEV Status: ", $status{$in{'dev'}}{state}, "<br />";
	print ui_table_start("Tasks", "width=100%", "10", ['align=left'] );
	if ($status{$in{'dev'}}{state} =~ "ONLINE")	{
		print ui_table_row("Offline: ", "<a href='cmd.cgi?cmd=vdev&action=offline&pool=$in{'pool'}&vdev=$status{$in{'dev'}}{name}'>Bring device offline</a><br />");
	}
	else { #elsif ($status{$in{'dev'}}{state} =~ "OFFLINE") {
		print ui_table_row("Online: ", "<a href='cmd.cgi?cmd=vdev&action=online&pool=$in{'pool'}&vdev=$status{$in{'dev'}}{name}'>Bring device online</a><br />");
	}
	print ui_table_row("Replace: ", "<a href='#'>Replace device</a><br />");
	print ui_table_row("Remove: ", "<a href='cmd.cgi?cmd=vdev&action=remove&pool=$in{'pool'}&vdev=$status{$in{'dev'}}{name}'>Remove device</a><br />");
	print ui_table_row("Detach: ", "<a href='cmd.cgi?cmd=vdev&action=detach&pool=$in{'pool'}&vdev=$status{$in{'dev'}}{name}'>Detach device</a><br />");
	print ui_table_row("Clear: ", "<a href='cmd.cgi?cmd=vdev&action=clear&pool=$in{'pool'}&vdev=$status{$in{'dev'}}{name}'>Clear errors</a><br />");
	print ui_table_end();
}
#print $gconfig{'os_type'};
#print mount::get_mount();

ui_print_footer("status.cgi?pool=$in{'pool'}", $in{'pool'});
