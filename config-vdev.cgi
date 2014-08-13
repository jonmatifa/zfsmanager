#!/usr/bin/perl

require './zfsmanager-lib.pl';
#foreign_require("fdisk", "fdisk-lib.pl");
#foreign_require("mount", "mount-lib.pl");
ReadParse();
use Data::Dumper;

ui_print_header(undef, $text{'vdev_title'}, "", undef, 1, 1);
#popup_header($text{'cmd_title'});

%conf = get_zfsmanager_config();

my %status = zpool_status($in{'pool'});

#foreach $key (sort(keys %status))
#{
#	if ($status{$key}{name} =~ $in{'dev'})
#	{
#		my %dev = $status{$key};
#		#print "seeing device";
#	}
#}
print ui_table_start($text{'vdev_title'}, "width=100%", "10", ['align=left'] );
print "Pool: ", $status{pool}{pool}, "<br />";
print "Pool State: ", $status{pool}{state}, "<br />";
print "Virtual Device: ", $in{'dev'}, "<br />";
if ($status{$in{'dev'}}{parent} =~ "pool") 
{
	#print "Parent: <a href='status.cgi?pool=", $status{pool}{pool}, "'>pool</a><br />";
	print "Parent: pool<br />";
} else {
	print "Parent: <a href='config-vdev.cgi?pool=", $in{'pool'}, "&dev=", $status{$in{'dev'}}{parent}, "'>", $status{$in{'dev'}}{parent}, "</a><br />";
}
if (($in{'dev'} =~ "cache") || ($in{'dev'} =~ "logs") || ($in{'dev'} =~ "spare") || ($in{'dev'} =~ /mirror/) || ($in{'dev'} =~ /raidz/))
{
print "Children: ";
	foreach $key (sort(keys %status))
	{
		if ($status{$key}{parent} =~ $in{'dev'}) 
		{
			print "<a href='config-vdev.cgi?pool=", $in{'pool'}, "&dev=", $status{$key}{name}, "'>", $status{$key}{name}, "</a>  ";
		}
	}
} elsif ($conf{'pool_properties'} =~ /1/) {
	print "VDEV Status: ", $status{$in{'dev'}}{state}, "<br />";
	print ui_table_start("Tasks", "width=100%", "10", ['align=left'] );
	if ($status{$in{'dev'}}{state} =~ "OFFLINE")	{
		#print ui_popup_link('bring device online', "cmd.cgi?pool=$in{'pool'}&online=$in{'dev'}"), "<br />";
		print ui_table_row("Online: ", "<a href='cmd.cgi?pool=$in{'pool'}&online=$in{'dev'}'>Bring device online</a><br />");
		#print "<a href='cmd.cgi?pool=$in{'pool'}&remove=$in{'dev'}'>remove device</a><br />";
		#print "<a href='cmd.cgi?pool=$in{'pool'}&remove=$in{'dev'}'>replace device</a><br />";
	}
	elsif ($status{$in{'dev'}}{state} =~ "ONLINE") {
		#print ui_popup_link('bring device offline', "cmd.cgi?pool=$in{'pool'}&offline=$in{'dev'}"), "<br />";
		print ui_table_row("Offline: ", "<a href='cmd.cgi?pool=$in{'pool'}&offline=$in{'dev'}'>Bring device offline</a><br />");
		#print "<a href='cmd.cgi?pool=$in{'pool'}&remove=$in{'dev'}'>remove device</a><br />";
		#print "<a href='cmd.cgi?pool=$in{'pool'}&remove=$in{'dev'}'>replace device</a><br />";
	}
	print ui_table_row("Replace: ", "<a href='#'>Replace device</a><br />");
	print ui_table_row("Remove: ", "<a href='#'>Remove device</a><br />");
	print ui_table_row("Detach: ", "<a href='#'>Detach device</a><br />");
	print ui_table_row("Clear: ", "<a href='#'>Clear errors</a><br />");
	print ui_table_end();
}
#print $gconfig{'os_type'};
#print mount::get_mount();
#print "<a href='create.cgi'>create</a>";

#print "<a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
#popup_footer();
print ui_table_end();

ui_print_footer("status.cgi?pool=$in{'pool'}", $in{'pool'});
