#!/usr/bin/perl

require './zfsmanager-lib.pl';
#foreign_require("fdisk", "fdisk-lib.pl");
#foreign_require("mount", "mount-lib.pl");
ReadParse();
use Data::Dumper;

ui_print_header(undef, $text{'vdev_title'}, "", undef, 1, 1);
$conf = get_zfsmanager_config();

my %status = zpool_status($in{'pool'});

#foreach $key (sort(keys %status))
#{
#	if ($status{$key}{name} =~ $in{'dev'})
#	{
#		my %dev = $status{$key};
#		#print "seeing device";
#	}
#}

print "Pool: ", $status{pool}{pool}, "<br />";
print "Pool State: ", $status{pool}{state}, "<br />";
print "Virtual Device: ", $in{'dev'}, "<br />";
if ($status{$in{'dev'}}{parent} =~ "pool") 
{
	print "Parent: <a href='status.cgi?pool=", $status{pool}{pool}, "'>pool</a><br />";
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
} else
{
	print "VDEV Status: ", $status{$in{'dev'}}{state}, "<br />";
	if ($status{$in{'dev'}}{state} =~ "OFFLINE")
	{
		print ui_popup_link('bring device online', "cmd.cgi?pool=$in{'pool'}&online=$in{'dev'}"), "<br />";
		#print "<a href='cmd.cgi?pool=$in{'pool'}&online=$in{'dev'}'>bring device online</a><br />";
		#print "<a href='cmd.cgi?pool=$in{'pool'}&remove=$in{'dev'}'>remove device</a><br />";
		#print "<a href='cmd.cgi?pool=$in{'pool'}&remove=$in{'dev'}'>replace device</a><br />";
	}
	if ($status{$in{'dev'}}{state} =~ "ONLINE")
	{
		print ui_popup_link('bring device offline', "cmd.cgi?pool=$in{'pool'}&offline=$in{'dev'}"), "<br />";
		#print "<a href='cmd.cgi?pool=$in{'pool'}&offline=$in{'dev'}'>bring device offline</a><br />";
		#print "<a href='cmd.cgi?pool=$in{'pool'}&remove=$in{'dev'}'>remove device</a><br />";
		#print "<a href='cmd.cgi?pool=$in{'pool'}&remove=$in{'dev'}'>replace device</a><br />";
	}
}
#print $gconfig{'os_type'};
#print mount::get_mount();
#print "<a href='create.cgi'>create</a>";

ui_print_footer("status.cgi?pool=$in{'pool'}", $in{'pool'});