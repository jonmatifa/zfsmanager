#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
#ui_print_header(undef, $text{'cmd_title'}, "", undef, 1, 1);
popup_header($text{'cmd_title'});
$conf = get_zfsmanager_config();

if ($in{'online'})
{
	print "Attempting to bring $in{'online'} online with command... <br />";
	my @result = cmd_online($in{'pool'}, $in{'online'});
	print $result[0], "<br />";
	if ($result[1] == //)
	{
		print "Success! <br />";
		print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
	} else
	{
	print "error: ", $result[1], "<br />";
	}
#ui_print_footer("status.cgi?pool=$in{'pool'}", $in{'pool'});
popup_footer();
}

if ($in{'offline'})
{
	print "Attempting to bring $in{'offline'} offline with command... <br />";
	my @result = cmd_offline($in{'pool'}, $in{'offline'});
	print $result[0], "<br />";
	if ($result[1] == //)
	{
		print "Success! <br />";
		print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
	} else
	{
	print "error: ", $result[1], "<br />";
	}
#ui_print_footer("status.cgi?pool=$in{'pool'}", $in{'pool'});
popup_footer();
}

if ($in{'remove'})
{
	print "Attempting to remove $in{'offline'} with command... <br />";
	my @result = cmd_remove($in{'pool'}, $in{'remove'});
	print $result[0], "<br />";
	if ($result[1] == //)
	{
		print "Success! <br />";
		print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
	} else
	{
	print "error: ", $result[1], "<br />";
	}
#ui_print_footer("status.cgi?pool=$in{'pool'}", $in{'pool'});
popup_footer();
}

if ($in{'snap'})
{
	print "Attempting to create snapshot $in{'snap'} with command... <br />";
	my @result = cmd_snapshot($in{'zfs'}."@".$in{'snap'});
	print $result[0], "<br />";
	if ($result[1] == //)
	{
		print "Success! <br />";
		print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
	} else
	{
	print "error: ", $result[1], "<br />";
	}
#ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
popup_footer();
}

if ($in{'destroy'})
{
	print "<h2>Destroy</h2>";
	ui_zfs_list($in{'destroy'});
	ui_list_snapshots($in{'destroy'});
	print "Attempting to destroy $in{'destroy'} with command... <br />";
	my @result = cmd_destroy_zfs($in{'destroy'}, $in{'confirm'});
	print $result[0], "<br />";
	if (!$in{'confirm'})
	{
		print "<h3>Warning, this action will result in data loss, do you really want to continue?</h3>";
		print "<a href='cmd.cgi?destroy=", $in{'destroy'}, "&confirm=yes'>Yes</a> | <a onClick=\"\window.close('cmd')\"\ href=''>No</a>";
	} else {
		if (($result[1] eq undef))
		{
			print "Success! <br />";
			print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
		} else
		{
		print "error: ", $result[1], "<br />";
		print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
		}
	}
#ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
popup_footer();
}

# cmd.cgi?zfs=&property=&set=&confirm=
if ($in{'set'})
{
	print "Attempting to set zfs property $in{'property'} to $in{'set'} in $in{'zfs'} with command... <br />";
	my @result = cmd_zfs_set($in{'zfs'}, $in{'property'}, $in{'set'}, $in{'confirm'});
	print $result[0], "<br />";
	if (!$in{'confirm'})
	{
		print "<h3>Would you lke to continue?</h3>";
		print "<a href='cmd.cgi?zfs=$in{'zfs'}&property=$in{'property'}&set=$in{'set'}&confirm=yes'>Yes</a> | <a onClick=\"\window.close('cmd')\"\ href=''>No</a>";
	} else {
		if (($result[1] == //))
		{
			print "Success! <br />";
			print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
		} else
		{
		print "error: ", $result[1], "<br />";
		}
	}
#ui_print_footer("index.cgi?mode=zfs", $text{'zfs_return'});
popup_footer();
}

if ($in{'mount'})
{
	print "Attempting to set zfs property $in{'property'} to $in{'set'} in $in{'zfs'} with command... <br />";
	my @result = cmd_zfs_mount($in{'zfs'}, $in{'mount'}, $in{'confirm'});
	print $result[0], "<br />";
	if (!$in{'confirm'})
	{
		print "<h3>Would you lke to continue?</h3>";
		print "<a href='cmd.cgi?zfs=$in{'zfs'}&mount=$in{'mount'}&confirm=yes'>Yes</a> | <a onClick=\"\window.close('cmd')\"\ href=''>No</a>";
	} else {
		if (($result[1] == //))
		{
			print "Success! <br />";
			print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
		} else
		{
		print "error: ", $result[1], "<br />";
		}
	}
#ui_print_footer("index.cgi?mode=zfs", $text{'zfs_return'});
popup_footer();
}

if (($in{'create'} =~ 'zfs') && ($in{'pool'}))
{
	print "Attempting to create filesystem $in{'pool'}/$in{'zfs'} with command... <br />";
	my @result = cmd_create_zfs($in{'pool'}."/".$in{'zfs'});
	print $result[0], "<br />";
	if ($result[1] == //)
	{
		print "Success! <br />";
		print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
	} else
	{
	print "error: ", $result[1], "<br />";
	}
#ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
}

if (($in{'create'} =~ 'zpool') && ($in{'pool'}))
{
	print "Attempting to create pool $in{'pool'} with command... <br />";
	my @result = cmd_create_zpool($in{'pool'}, $in{'dev'}, $in{'options'}, $in{'mountpoint'}, $in{'force'});
	print $result[0], "<br />";
	if ($result[1] == //)
	{
		print "Success! <br />";
		print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
	} else
	{
	print "error: ", $result[1], "<br />";
	}
#ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
popup_footer();
}
