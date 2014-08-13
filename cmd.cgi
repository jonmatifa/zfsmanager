#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
use Switch;
ui_print_header(undef, $text{'cmd_title'}, "", undef, 1, 1);
#popup_header($text{'cmd_title'});
%conf = get_zfsmanager_config();

print ui_table_start($text{'cmd_title'}, "width=100%", "10", ['align=left'] );

switch ($in{'cmd'}) {
	
	case "setzfs" {
		my @result = ($conf{'zfs_properties'} =~ /1/) ? cmd_zfs_set($in{'zfs'}, $in{'property'}, $in{'set'}, $in{'confirm'}) : undef;
		print ui_cmd("set zfs property $in{'property'} to $in{'set'} in $in{'zfs'}", @result);
	}
	case "setpool" {
		my $cmd="zpool set $in{'property'}=$in{'set'} $in{'pool'}";
		my @result = (($conf{'pool_properties'} =~ /1/) && ($in{'confirm'} =~ /yes/)) ? ($cmd, `$cmd 2>&1`) : ($cmd, "" );
		#my @result = ($conf{'pool_properties'} =~ /1/) ?cmd_zpool($in{'pool'}, 'set', $in{'property'}.'='.$in{'set'}, undef, $in{'confirm'}): undef;
		print ui_cmd("set pool property $in{'property'} to $in{'set'} in $in{'pool'}", @result);
	}
	case "snap" {
			#my @result = ($conf{'snap_properties'} =~ /1/) ? cmd_snapshot($in{'zfs'}."@".$in{'snap'}) : undef;
			my $cmd = "zfs snapshot ".$in{'zfs'}."@".$in{'snap'};
			my @result = ($conf{'snap_properties'} =~ /1/) ? ( $cmd, `$cmd 2>&1` ) : undef;
			$in{'confirm'} = "yes";
			print ui_cmd("create snapshot $in{'snap'}", @result);
			print "", (!$result[1]) ? ui_list_snapshots($in{'zfs'}."@".$in{'snap'}) : undef;
	}
	case "createzfs" {
		#print "Attempting to create filesystem $in{'parent'}/$in{'zfs'} with command... <br />";
		my %createopts = create_opts();
		my %options = ();
		foreach $key (sort (keys %createopts)) {
			$options{$key} = ($in{$key}) ? $in{$key} : undef;
			#if ($in{$key}) { $options{$key} = $in{$key};}
		}
		if ($in{'mountpoint'}) { $options{'mountpoint'} = $in{'mountpoint'}; }
		if ($in{'zvol'} == '1') { $in{'zfs'} = "-V ".$in{'size'}." ".$in{'parent'}."/".$in{'zfs'}; } 
		else { $in{'zfs'} = $in{'parent'}."/".$in{'zfs'}; }
		my @result = (($in{'parent'}) && ($conf{'zfs_properties'} =~ /1/)) ? cmd_create_zfs($in{'zfs'}, $options) : undef;
		$in{'confirm'} = "yes";
		print ui_cmd("create filesystem $in{'parent'}/$in{'zfs'}", @result);
		#print "", (!$result[1]) ? ui_zfs_list($in{'zfs'}) : undef;
		#^^^this doesn't work for some reason
		$in{'zfs'} = $in{'parent'};
	}
	case "import" {
	#print "Attempting to import pool $in{'import'} with command... <br />";
	my $dir = ();
	if ($in{'dir'}) { $dir .= " -d".$in{'dir'}; }
	if ($in{'destroyed'}) { $dir .= " -D -f"; }
	my $cmd = "zpool import".$dir." ".$in{'import'};
	my @result = ($conf{'pool_properties'} =~ /1/ && ($in{'confirm'} =~ /yes/)) ? ($cmd, `$cmd 2>&1`) : ($cmd, "" );
	print ui_cmd("import pool $in{'import'}", @result);
	ui_print_footer("index.cgi?mode=pools", $text{'index_return'});
	}
	
}




#legacy commands

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

if (($in{'destroy'}) && ($conf{'zfs_destroy'} =~ /1/))
{
	#print "<h2>Destroy</h2>";
	print "Attempting to destroy $in{'destroy'} with command... <br />";
	print ui_form_start('cmd.cgi', 'post');
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
		print ui_submit("Continue", undef, undef);
		#print ui_submit("Continue", undef, undef), " | <a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
	} else {
		if (($result[1] eq undef))
		{
			print "Success! <br />";
			#print Dumper(@result);
			#print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
		} else
		{
		print "error: ", $result[1], "<br />";
		#print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
		}
	}
print ui_form_end();
ui_print_footer("index.cgi?mode=zfs", $text{'zfs_return'});
#popup_footer();
}

if (($in{'destroysnap'}) && ($conf{'snap_destroy'} =~ /1/))
{
	#print "<h2>Destroy</h2>";
	print "Attempting to destroy $in{'destroysnap'} with command... <br />";
	print ui_form_start('cmd.cgi', 'post');
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
		print ui_submit("Continue", undef, undef),;
		#print ui_submit("Continue", undef, undef), " | <a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
	} else {
		if (($result[1] eq undef))
		{
			print "Success! <br />";
			#print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
		} else
		{
		print "error: ", $result[1], "<br />";
		#print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
		}
	}
print ui_form_end();
ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
#popup_footer();
}

if (($in{'destroypool'}) && ($conf{'pool_destroy'} =~ /1/))
{
	#print "<h2>Destroy</h2>";
	#ui_zfs_list('-r '.$in{'destroypool'});
	#print ui_list_snapshots($in{'destroy'});
	print "Attempting to destroy $in{'destroypool'} with command... <br />";
	print ui_form_start('cmd.cgi', 'post');
	print ui_hidden('destroypool', $in{'destroypool'});
	my @result = cmd_destroy_zpool($in{'destroypool'}, undef, $in{'confirm'});
	print $result[0], "<br />";
	if (!$in{'confirm'})
	{
		print "<b>This action will affect the following: </b><br />";
		ui_zfs_list('-r '.$in{'destroypool'});
		ui_list_snapshots('-r '.$in{'destroypool'});
		#if (($conf{'zfs_destroy'} =~ /1/) && ($conf{'snap_destroy'} =~ /1/)) { print ui_checkbox('force', '-r', 'Click to destroy all child dependencies (recursive)', undef ), "<br />"; }
		print "<h3>Warning, this action will result in data loss, do you really want to continue?</h3>";
		print ui_checkbox('confirm', 'yes', 'I understand', undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- checkbox must be selected</font>"; }
		print "<br /><br />";
		#print "<a href='cmd.cgi?destroypool=", $in{'destroypool'}, "&confirm=yes'>Yes</a> | <a onClick=\"\window.close('cmd')\"\ href=''>No</a>";
		print ui_submit("Continue", undef, undef);
		#print ui_submit("Continue", undef, undef), " | <a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
	} else {
		if (($result[1] eq undef))
		{
			print "Success! <br />";
			#print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
		} else
		{
		print "error: ", $result[1], "<br />";
		#print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
		}
	}
print ui_form_end();
ui_print_footer("index.cgi?mode=pools", $text{'index_return'});
#print $in{'snapshot'};
#ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
#popup_footer();
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

#start a scrub
if (($in{'scrub'}) && ($conf{'pool_properties'} =~ /1/))
{
	print ui_cmd_zpool("scrub pool", $in{'scrub'}, ($in{'scrub'}, 'scrub', undef, undef, $in{'confirm'}));
}

#stop a scrub
if (($in{'scrubstop'}) && ($conf{'pool_properties'} =~ /1/))
{
	print ui_cmd_zpool("stop scrub pool", $in{'scrubstop'}, ($in{'scrubstop'}, 'scrub', '-s', undef, $in{'confirm'}));
}

#clone a snapshot
if (($in{'clone'}) && ($conf{'zfs_properties'} =~ /1/))
{
#($zfs, $action, $options, $confirm)
	my %createopts = create_opts();
	#%options = ();
	$opts = ();
	foreach $key (sort (keys %createopts))
	{
		if ($in{$key})
		{
			#$options{$key} = $in{$key};
			$opts = ($in{$key} =~ 'default') ? $opts : $opts.' -o '.$key.'='.$in{$key};
		}
	}
	#if ($in{'mountpoint'}) { $options{'mountpoint'} = $in{'mountpoint'}; }
	if ($in{'mountpoint'}) { $opts .= ' -o mountpoint='.$in{'mountpoint'}; }
	$in{'confirm'} = "yes";
	print ui_cmd_zfs("clone ", $in{'clone'}, ($in{'clone'}.' '.$in{'parent'}.'/'.$in{'zfs'}, 'clone', $opts, $in{'confirm'}));
	ui_print_footer("status.cgi?snap=".$in{'clone'}, $in{'clone'});
}

#promote filesystem
if (($in{'promote'}) && ($conf{'zfs_properties'} =~ /1/))
{
#($zfs, $action, $options, $confirm)
	print ui_cmd_zfs("promote ", $in{'promote'}, ($in{'promote'}, 'promote', undef, $in{'confirm'}));
}

#send snapshot
if (($in{'send'}) && ($conf{'zfs_properties'} =~ /1/))
{
#($zfs, $action, $options, $confirm)
	if ($in{'force'} =~1)  { $ropts .= " -F "; }
	my $opts = ();
	if ($in{'type'} =~ "new") { 
		$dest = "zfs recv $in{'parent'}/$in{'zfs'}";
		if ($in{'replicate'} =~ '1') { $opts .= " -R " }
	} elsif ($in{'type'} =~ "exist") { 
		$dest = "zfs recv $ropts $in{'existzfs'}"; 
		if ($in{'increment'} =~ '1') { $opts .= " -i " }
	}
	#my $opts = "-R";
	if ((!$in{'confirm'}) && ($in{'type'} =~ "exist")) {
		print "<b>This action will affect the following: </b><br />";
		ui_zfs_list('-r '.$in{'existzfs'});
		#ui_list_snapshots('-r '.$in{'existzfs'});
		#if (($conf{'zfs_destroy'} =~ /1/)) { print ui_checkbox('force', '-r', 'Click to destroy all child dependencies (recursive)', undef ), "<br />"; }
		print "<h3>Warning, this action will result in data loss, do you really want to continue?</h3>";
		#print ui_confirmation_form('cmd.cgi', 'Warning, this action will result in data loss...', [ 'destroy' => $in{'destroy'}, 'confirm' => 'yes' ], undef, undef, "Are you absolutely sure?");
		print ui_checkbox('confirm', 'yes', 'I understand', undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- checkbox must be selected</font>"; }
		print "<br /><br />";
	}
	my $result = cmd_zfs_send($in{'send'}, $dest, $opts, $in{'confirm'});
	print ui_cmd("send ", $in{'send'}, $result, $in{'confirm'});
}

if (($in{'multisnap'} =~ 1) && ($conf{'snap_destroy'}) =~ /1/) {
	my %snapshot = list_snapshots();
	#%conf = get_zfsmanager_config();
	#$in{'select'} =~ s/^\s*(.*?)\s*$/$1/;
	#$in{'select'} = s/([\w@-_]+)/$1/;
	@select = split(/;/, $in{'select'});
	print "<h2>Destroy</h2>";
	print "Attempting to destroy multiple snapshots... <br />";
	#print ui_form_start('cmd.cgi', 'post', 'cmd');
	print ui_form_start('cmd.cgi', 'post');
	print ui_hidden('multisnap', 1);
	print ui_hidden('select', $in{'select'});
	#print "<h1>multisnap</h1> <br />";
	print $in{'select'};
	my %results = ();
	print "<br />";
	print Dumper(@select);
	#print "<br />";
	#print Dumper(@array);
	#print Dumper(\%snapshot);
	print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
	foreach $key (@select)
	{
		#print "Selected snapshot: ", $key, "<br />";
		#my %snapshot = list_snapshots($key);
		#chomp($key);
		#$key = /[[:graph:]]$key/;
		print ui_columns_row([ $key, $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
		#print ui_columns_row([Dumper(\$snapshot{$key})]);
		$results{$key} = [ cmd_destroy_zfs($key, '', $in{'confirm'}) ]; 
	}
	print ui_columns_end();
	

	if (!$in{'confirm'})
	{
		print "<h2>Commands to be issued:</h2>";
		foreach $key (keys %results)
		{
			print $results{$key}[0], "<br />";
		}	
		print "<h3>Warning, this action will result in data loss, do you really want to continue?</h3>";
		print ui_checkbox('confirm', 'yes', 'I understand', undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- checkbox must be selected</font>"; }
		print "<br /><br />";
		#print ui_submit("Continue", undef, undef), " | <a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
		print ui_submit("Continue", undef, undef), " | <a href='index.cgi?mode=snapshot'>Cancel</a>";
	} else {
		print "<h2>Results from commands:</h2>";
		print Dumper(\%results);
		foreach $key (keys %results)
		{
			if (($results{$key}[1] eq undef))
			{
				print $results{$key}[0], "<br />";
				print "Success! <br />";
				#print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
			} else
			{
				print $results{$key}[0], "<br />";
				print "error: ", $results{$key}[1], "<br />";
			}
		}
	#print "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>";
	print ui_print_footer('index.cgi?mode=snapshot', $text{'snapshot_return'});
	}
	print ui_form_end();

}





print ui_table_end();

if ($in{'cmd'} && $in{'zfs'}) {
		print "<br />";
		ui_print_footer("status.cgi?zfs=".$in{'zfs'}, $in{'zfs'});
} elsif ($in{'cmd'} && $in{'pool'}) {
		print "<br />";
		ui_print_footer("status.cgi?pool=".$in{'pool'}, $in{'pool'});
} elsif ($in{'cmd'} && $in{'snap'}) {
		print "<br />";
		ui_print_footer("status.cgi?snap=".$in{'snap'}, $in{'snap'});
}

