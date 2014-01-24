#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
#ui_print_header(undef, $text{'cmd_title'}, "", undef, 1, 1);
popup_header($text{'cmd_title'});
%conf = get_zfsmanager_config();

if (($in{'online'}) && ($conf{'pool_properties'} =~ /1/))
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

if (($in{'offline'}) && ($conf{'pool_properties'} =~ /1/))
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

if (($in{'remove'}) && ($conf{'pool_properties'} =~ /1/))
{
	print "Attempting to remove $in{'remove'} with command... <br />";
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

if (($in{'snap'}) && ($conf{'snap_properties'} =~ /1/))
{
	print "Attempting to create snapshot $in{'snap'} with command... <br />";
	my @result = cmd_snapshot($in{'zfs'}."@".$in{'snap'});
	print $result[0], "<br />";
	if ($result[1] == //)
	{
		print "Success! <br />";
		print "<a onClick=\"\window.close('cmd');document.getElementById('right').contentWindow.location.reload()\"\ href=''>Close</a>";
	} else
	{
	print "error: ", $result[1], "<br />";
	}
#ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
popup_footer();
}

if (($in{'destroy'}) && ($conf{'zfs_destroy'} =~ /1/))
{
	print "<h2>Destroy</h2>";
	print "Attempting to destroy $in{'destroy'} with command... <br />";
	print ui_form_start('cmd.cgi', 'get', 'cmd');
	print ui_hidden('destroy', $in{'destroy'});
	my $result = cmd_destroy_zfs($in{'destroy'}, $in{'force'}, $in{'confirm'});
	print $result[0], "<br />";
	print "<br />";
	if (!$in{'confirm'})
	{
		print "<b>This action will affect the following: </b><br />";
		ui_zfs_list('-r '.$in{'destroy'});
		ui_list_snapshots('-r '.$in{'destroy'});
		if (($conf{'zfs_destroy'} =~ /1/) && ($conf{'snap_destroy'} =~ /1/)) { print ui_checkbox('force', '-r', 'Click to destroy all child dependencies (recursive)', undef ), "<br />"; }
		print "<h3>Warning, this action will result in data loss, do you really want to continue?</h3>";
		#print ui_confirmation_form('cmd.cgi', 'Warning, this action will result in data loss...', [ 'destroy' => $in{'destroy'}, 'confirm' => 'yes' ], undef, undef, "Are you absolutely sure?");
		print ui_checkbox('confirm', 'yes', 'I understand', undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- checkbox must be selected</font>"; }
		print "<br /><br />";
		#print "";
		#print "<a href='cmd.cgi?destroy=", $in{'destroy'}, "&confirm=yes'>Yes</a> | <a onClick=\"\window.close('cmd')\"\ href=''>No</a>";
		print ui_submit("Continue", undef, undef), " | <a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
	} else {
		if (($result[1] eq undef))
		{
			print "Success! <br />";
			#print Dumper(@result);
			print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
		} else
		{
		print "error: ", $result[1], "<br />";
		print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
		}
	}
print ui_form_end();
#ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
popup_footer();
}

if (($in{'destroysnap'}) && ($conf{'snap_destroy'} =~ /1/))
{
	print "<h2>Destroy</h2>";
	print "Attempting to destroy $in{'destroysnap'} with command... <br />";
	print ui_form_start('cmd.cgi', 'get', 'cmd');
	print ui_hidden('destroysnap', $in{'destroysnap'});
	my $result = cmd_destroy_zfs($in{'destroysnap'}, $in{'force'}, $in{'confirm'});
	print $result[0], "<br />";
	print "<br />";
	if (!$in{'confirm'})
	{
		print "<b>This action will affect the following: </b><br />";
		ui_list_snapshots('-r '.$in{'destroysnap'});
		if (($conf{'zfs_destroy'} =~ /1/) && ($conf{'snap_destroy'} =~ /1/)) { print ui_checkbox('force', '-r', 'Click to destroy all child dependencies (recursive)', undef ), "<br />"; }
		print "<h3>Warning, this action will result in data loss, do you really want to continue?</h3>";
		print ui_checkbox('confirm', 'yes', 'I understand', undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- checkbox must be selected</font>"; }
		print "<br /><br />";
		print ui_submit("Continue", undef, undef), " | <a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
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
print ui_form_end();
popup_footer();
}

if (($in{'destroypool'}) && ($conf{'pool_destroy'} =~ /1/))
{
	print "<h2>Destroy</h2>";
	#ui_zfs_list('-r '.$in{'destroypool'});
	#print ui_list_snapshots($in{'destroy'});
	print "Attempting to destroy $in{'destroypool'} with command... <br />";
	print ui_form_start('cmd.cgi', 'get', 'cmd');
	print ui_hidden('destroypool', $in{'destroypool'});
	my @result = cmd_destroy_zpool($in{'destroypool'}, undef, $in{'confirm'});
	print $result[0], "<br />";
	if (!$in{'confirm'})
	{
		print "<b>This action will affect the following: </b><br />";
		ui_zfs_list('-r '.$in{'destroypool'});
		ui_list_snapshots('-r '.$in{'destroypool'});
		if (($conf{'zfs_destroy'} =~ /1/) && ($conf{'snap_destroy'} =~ /1/)) { print ui_checkbox('force', '-r', 'Click to destroy all child dependencies (recursive)', undef ), "<br />"; }
		print "<h3>Warning, this action will result in data loss, do you really want to continue?</h3>";
		print ui_checkbox('confirm', 'yes', 'I understand', undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- checkbox must be selected</font>"; }
		print "<br /><br />";
		#print "<a href='cmd.cgi?destroypool=", $in{'destroypool'}, "&confirm=yes'>Yes</a> | <a onClick=\"\window.close('cmd')\"\ href=''>No</a>";
		print ui_submit("Continue", undef, undef), " | <a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
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
print ui_form_end();
#ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
popup_footer();
}

# cmd.cgi?zfs=&property=&set=&confirm=
if (($in{'set'}) && ($conf{'zfs_properties'} =~ /1/))
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

if (($in{'mount'}) && ($conf{'zfs_properties'} =~ /1/))
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

if (($in{'create'} =~ 'zfs') && ($in{'parent'}) && ($conf{'zfs_properties'} =~ /1/))
{
	print "Attempting to create filesystem $in{'parent'}/$in{'zfs'} with command... <br />";
	my %createopts = create_opts();
	%options = ();
	foreach $key (sort (keys %createopts))
	{
		if ($in{$key})
		{
			$options{$key} = $in{$key};
		}
	}
	if ($in{'mountpoint'}) { $options{'mountpoint'} = $in{'mountpoint'}; }
	#print Dumper (\%options);
	my @result = cmd_create_zfs($in{'parent'}."/".$in{'zfs'}, $options);
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

if (($in{'create'} =~ 'zpool') && ($in{'pool'})  && ($conf{'pool_properties'} =~ /1/))
{
	if (length($in{'mountpoint'}) == 0) { $in{'mountpoint'} = ""; };
	print "Attempting to create pool $in{'pool'} with command... <br />";
	#@opts = split(', ', $in{'options'});
	my %createopts = create_opts();
	%options = ();
	foreach $key (sort (keys %createopts))
	{
		if ($in{$key})
		{
			$options{$key} = $in{$key};
		}
		#($prop, $value) = split('=', $ref);
		#$options{$prop} = $options{$value};
	}
	my @result = cmd_create_zpool($in{'pool'}, $in{'dev'}, $options, $in{'mountpoint'}, $in{'force'});
	print $result[0], "<br />";
	if ($result[1] == //)
	{
		print "Success! <br />";
		print "<a onClick=\"\window.close('cmd'),window.reload('right')\"\ href=''>Close</a>";
	} else
	{
	print "error: ", $result[1], "<br />";
	}
#ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
popup_footer();
}

if (($in{'export'})  && ($conf{'pool_properties'} =~ /1/))
{
	
	print "Attempting to export pool $in{'export'} with command... <br />";
	#@opts = split(', ', $in{'options'});
	my $result = cmd_zpool($in{'export'}, 'export', undef, undef, $in{'confirm'});
	print $result[0], "<br />";
	if (!$in{'confirm'})
	{
		print "<h3>Would you lke to continue?</h3>";
		print "<a href='cmd.cgi?export=$in{'export'}&confirm=yes'>Yes</a> | <a onClick=\"\window.close('cmd')\"\ href=''>No</a>";
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
#ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
popup_footer();
}

if (($in{'import'})  && ($conf{'pool_properties'} =~ /1/))
{
	
	print "Attempting to import pool $in{'import'} with command... <br />";
	if ($in{'dir'}) { $dir = "-d ".$in{'dir'}; }
	my $result = cmd_zpool($in{'import'}, 'import', $dir, undef, $in{'confirm'});
	print $result[0], "<br />";
	if (!$in{'confirm'})
	{
		print "<h3>Would you lke to continue?</h3>";
		print "<a href='cmd.cgi?import=$in{'import'}&dir=$in{'dir'}&confirm=yes'>Yes</a> | <a onClick=\"\window.close('cmd')\"\ href=''>No</a>";
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
#ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
popup_footer();
}
