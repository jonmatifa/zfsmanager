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
ui_print_footer("status.cgi?pool=$in{'pool'}", $in{'pool'});
}

if ($in{'snap'})
{
	print "Attempting to create snapshot $in{'snap'} with command... <br />";
	my @result = cmd_snapshot($in{'zfs'}."@".$in{'snap'});
	print $result[0], "<br />";
	if ($result[1] == //)
	{
		print "Success! <br />";
	} else
	{
	print "error: ", $result[1], "<br />";
	}
ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
}

if ($in{'destroy'})
{
	print "Attempting to destroy $in{'destroy'} with command... <br />";
	my @result = cmd_destroy_zfs($in{'destroy'}, $in{'confirm'});
	print $result[0], "<br />";
	if (!$in{'confirm'})
	{
		print "<h3>Warning, this action will result in data loss, do you really want to continue?</h3>";
		print "<a href='cmd.cgi?destroy=", $in{'destroy'}, "&confirm=yes'>Yes</a> <a href='index.cgi?mode=snapshot'>No</a>";
	} else {
		if (($result[1] == //))
		{
			print "Success! <br />";
		} else
		{
		print "error: ", $result[1], "<br />";
		}
	}
ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
}