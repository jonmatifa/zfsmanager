#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
ui_print_header(undef, $text{'cmd_title'}, "", undef, 1, 1);
$conf = get_zfsmanager_config();

if ($in{'online'})
{
	print "Attempting to bring $in{'online'} online with command... <br />";
	my @result = cmd_online($in{'pool'}, $in{'online'});
	print $result[0], "<br />";
	if ($result[1] == //)
	{
		print "Success! <br />";
	} else
	{
	print "error: ", $result[1], "<br />";
	}
ui_print_footer("status.cgi?pool=$in{'pool'}", $in{'pool'});
}

if ($in{'offline'})
{
	print "Attempting to bring $in{'offline'} offline with command... <br />";
	my @result = cmd_offline($in{'pool'}, $in{'offline'});
	print $result[0], "<br />";
	if ($result[1] == //)
	{
		print "Success! <br />";
	} else
	{
	print "error: ", $result[1], "<br />";
	}
ui_print_footer("status.cgi?pool=$in{'pool'}", $in{'pool'});
}

if ($in{'remove'})
{
	print "Attempting to remove $in{'offline'} with command... <br />";
	my @result = cmd_remove($in{'pool'}, $in{'remove'});
	print $result[0], "<br />";
	if ($result[1] == //)
	{
		print "Success! <br />";
	} else
	{
	print "error: ", $result[1], "<br />";
	}
	print Dumper @result;
ui_print_footer("status.cgi?pool=$in{'pool'}", $in{'pool'});
}
