#!/usr/bin/perl

require './zfsmanager-lib.pl';
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
print "Parent: ", $status{$in{'dev'}}{parent}, "<br />";
print "VDEV Status: ", $status{$in{'dev'}}{state}, "<br />";
if ($status{$in{'dev'}}{state} =~ "OFFLINE")
{
	print "<a href='cmd.cgi?pool=$in{'pool'}&online=$in{'dev'}'>bring device online</a><br />";
	#print "<a href='cmd.cgi?pool=$in{'pool'}&remove=$in{'dev'}'>remove device</a><br />";
	print "<a href='cmd.cgi?pool=$in{'pool'}&remove=$in{'dev'}'>replace device</a><br />";
}
if ($status{$in{'dev'}}{state} =~ "ONLINE")
{
	print "<a href='cmd.cgi?pool=$in{'pool'}&offline=$in{'dev'}'>bring device offline</a><br />";
	#print "<a href='cmd.cgi?pool=$in{'pool'}&remove=$in{'dev'}'>remove device</a><br />";
	print "<a href='cmd.cgi?pool=$in{'pool'}&remove=$in{'dev'}'>replace device</a><br />";
}

ui_print_footer("status.cgi?pool=$in{'pool'}", $in{'pool'});