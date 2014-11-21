#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
ui_print_header(undef, $text{'cmd_title'}, "", undef, 1, 1);
%conf = get_zfsmanager_config();
print ui_table_start($text{'cmd_title'}, "width=100%", "10", ['align=left'] );
	
if ($in{'cmd'} =~ "setzfs") {
	$in{'confirm'} = "yes";
	if (($in{'set'} =~ "inherit") && ($conf{'zfs_properties'} =~ /1/)) { $cmd = "zfs inherit $in{'property'} $in{'zfs'}"; 
	} elsif ($conf{'zfs_properties'} =~ /1/) { $cmd =  "zfs set $in{'property'}=$in{'set'} $in{'zfs'}"; }
	print ui_cmd("set zfs property $in{'property'} to $in{'set'} in $in{'zfs'}", $cmd);
}
elsif ($in{'cmd'} =~ "setpool")  {
	$in{'confirm'} = "yes";
	my $cmd = ($conf{'pool_properties'} =~ /1/) ? "zpool set $in{'property'}=$in{'set'} $in{'pool'}": undef;
	#my @result = (($conf{'pool_properties'} =~ /1/) && ($in{'confirm'} =~ /yes/)) ? ($cmd, `$cmd 2>&1`) : ($cmd, "" );
	print ui_cmd("set pool property $in{'property'} to $in{'set'} in $in{'pool'}", $cmd);
}
elsif ($in{'cmd'} =~ "snap")  {
		my $cmd = ($conf{'snap_properties'} =~ /1/) ?  "zfs snapshot ".$in{'zfs'}."@".$in{'snap'} : undef;
		#my @result = ($conf{'snap_properties'} =~ /1/) ? ( $cmd, `$cmd 2>&1` ) : undef;
		$in{'confirm'} = "yes";
		print ui_cmd("create snapshot $in{'snap'}", $cmd);
		print "", (!$result[1]) ? ui_list_snapshots($in{'zfs'}."@".$in{'snap'}) : undef;
}
elsif ($in{'cmd'} =~ "createzfs")  {
	#print "Attempting to create filesystem $in{'parent'}/$in{'zfs'} with command... <br />";
	my %createopts = create_opts();
	#$createopts{'volblocksize'} = '8k';
	#$createopts{'sparse'} = '0';
	my %options = ();
	foreach $key (sort (keys %createopts)) {
		$options{$key} = ($in{$key}) ? $in{$key} : undef;
		#if ($in{$key}) { $options{$key} = $in{$key};}
	}
	if ($in{'mountpoint'}) { $options{'mountpoint'} = $in{'mountpoint'}; }
	if ($in{'zvol'} == '1') { 
		#$in{'zfs'} = "-V ".$in{'size'}." ".$in{'parent'}."/".$in{'zfs'};
		$options{'zvol'} = $in{'size'};
		$options{'sparse'} = $in{'sparse'};
		$options{'volblocksize'} = $in{'volblocksize'};
	} 
	#else { $in{'zfs'} = $in{'parent'}."/".$in{'zfs'}; }
	#print Dumper(\%options);
	#my @result = (($in{'parent'}) && ($conf{'zfs_properties'} =~ /1/)) ? cmd_create_zfs($in{'parent'}."/".$in{'zfs'}, \%options) : undef;
	my $cmd = (($in{'parent'}) && ($conf{'zfs_properties'} =~ /1/)) ? cmd_create_zfs($in{'parent'}."/".$in{'zfs'}, \%options) : undef;
	$in{'confirm'} = "yes";
	print ui_cmd("create filesystem $in{'parent'}/$in{'zfs'}", $cmd);
	#print "", (!$result[1]) ? ui_zfs_list($in{'zfs'}) : undef;
	#^^^this doesn't work for some reason
	@footer = ("status.cgi?zfs=".$in{'parent'}, $in{'parent'});
}
elsif ($in{'cmd'} =~ "clone")  {
	my %createopts = create_opts();
	$opts = ();
	foreach $key (sort (keys %createopts))
	{
		if ($in{$key})
		{
			$opts = ($in{$key} =~ 'default') ? $opts : $opts.' -o '.$key.'='.$in{$key};
		}
	}
	if ($in{'mountpoint'}) { $opts .= ' -o mountpoint='.$in{'mountpoint'}; }
	$in{'confirm'} = "yes";
	my $cmd =  ($conf{'zfs_properties'} =~ /1/) ? "zfs clone ".$in{'clone'}." ".$in{'parent'}.'/'.$in{'zfs'}." ".$opts : undef;
	#my @result = ($conf{'zfs_properties'} =~ /1/) ? ( $cmd, `$cmd 2>&1` ) : undef;
	print ui_cmd("clone ".$in{'clone'}, $cmd);
	@footer = ("status.cgi?snap=".$in{'clone'}, $in{'clone'})
}
elsif ($in{'cmd'} =~ "createzpool")  {
	#print "Attempting to create filesystem $in{'parent'}/$in{'zfs'} with command... <br />";
	my %createopts = create_opts();
	my %options = ();
	$in{'volblocksize'} = "default";
	$in{'sparse'} = "default";
	foreach $key (sort (keys %createopts)) {
		$options{$key} = ($in{$key}) ? $in{$key} : undef;
		#if ($in{$key}) { $options{$key} = $in{$key};}
	}
	if ($in{'mountpoint'}) { $options{'mountpoint'} = $in{'mountpoint'}; }
	#if ($in{'version'}) { $options{'version'} = $in{'version'}; }
	#if ($in{'zvol'} == '1') { $in{'zfs'} = "-V ".$in{'size'}." ".$in{'parent'}."/".$in{'zfs'}; } 
	#else { $in{'zfs'} = $in{'parent'}."/".$in{'zfs'}; }
	if ($in{'vdev'} =~ 'stripe') { delete $in{'vdev'}; } else{ $in{'vdev'} .= " "; }
	$in{'devs'} =~ s/\R/ /g;
	%poolopts = ( 'version' => $in{'version'} );
	my $cmd = (($conf{'pool_properties'} =~ /1/)) ? cmd_create_zpool($in{'pool'}, $in{'vdev'}.$in{'devs'}, \%options, \%poolopts, $in{'force'}) : undef;
	$in{'confirm'} = "yes";
	print ui_cmd("create pool $in{'pool'}", $cmd);
	#print Dumper(\%in);
	#print Dumper(\%options);
	#print "", (!$result[1]) ? ui_zfs_list($in{'zfs'}) : undef;
	#^^^this doesn't work for some reason
	#$in{'pool'} = $in{'parent'};
}
elsif ($in{'cmd'} =~ "online") { #deprecate in favor of vdev
	$in{'confirm'} = "yes";
	my $cmd = ($conf{'pool_properties'} =~ /1/) ? "zpool online $in{'pool'} $in{'online'}" : undef;
	#my @result = ($conf{'pool_properties'} =~ /1/) ? ($cmd, `$cmd 2>&1`) : undef;
	print ui_cmd("bring $in{'online'} online", $cmd);
}
elsif ($in{'cmd'} =~ "offline") { #deprecate in favor of vdev
	$in{'confirm'} = "yes";
	my $cmd = ($conf{'pool_properties'} =~ /1/) ? "zpool offline $in{'pool'} $in{'offline'}": undef;
	#my @result = ($conf{'pool_properties'} =~ /1/) ? ($cmd, `$cmd 2>&1`) : undef;
	print ui_cmd("bring $in{'offline'} offline", $cmd);
}
elsif ($in{'cmd'} =~ "vdev") {
	$in{'confirm'} = "yes";
	my $cmd =  ($conf{'pool_properties'} =~ /1/) ? "zpool $in{'action'} $in{'pool'} $in{'vdev'}": undef;
	#my @result = ($conf{'pool_properties'} =~ /1/) ? ($cmd, `$cmd 2>&1`) : undef;
	print ui_cmd("$in{'action'} $in{'vdev'}", $cmd);
}
elsif ($in{'cmd'} =~ "promote") {
#($zfs, $action, $options, $confirm)
	my $cmd = ($conf{'zfs_properties'} =~ /1/) ? "zfs promote $in{'zfs'}": undef;
	#my @result = (($conf{'zfs_properties'} =~ /1/) && ($in{'confirm'} =~ /yes/)) ? ($cmd, `$cmd 2>&1`) : ($cmd, "" );
	print ui_cmd("promote $in{'zfs'}", $cmd);
}
elsif ($in{'cmd'} =~ "scrub") {
	$in{'confirm'} = "yes";
	if ($in{'stop'}) { $in{'stop'} = "-s"; }
	my $cmd = ($conf{'pool_properties'} =~ /1/) ? "zpool scrub $in{'stop'} $in{'pool'}" : undef;
	print ui_cmd("scrub pool $in{'pool'}", $cmd);
	#@footer = ("status.cgi?pool=".$in{'pool'}, $in{'pool'});
}
elsif ($in{'cmd'} =~ "export") {
	$in{'confirm'} = "yes";
	my $cmd = ($conf{'pool_properties'} =~ /1/) ? "zpool export $in{'pool'}" : undef;
	print ui_cmd("scrub pool $in{'pool'}", $cmd);
	@footer = ("index.cgi?mode=pools", $text{'index_return'});
}
elsif ($in{'cmd'} =~ "import")  {
	my $dir = ();
	if ($in{'dir'}) { $dir .= " -d".$in{'dir'}; }
	if ($in{'destroyed'}) { $dir .= " -D -f"; }
	my $cmd = ($conf{'pool_properties'} =~ /1/ ) ? "zpool import".$dir." ".$in{'import'}: undef;
	#my @result = ($conf{'pool_properties'} =~ /1/ && ($in{'confirm'} =~ /yes/)) ? ($cmd, `$cmd 2>&1`) : ($cmd, "" );
	print ui_cmd("import pool $in{'import'}", $cmd);
	@footer = ("index.cgi?mode=pools", $text{'index_return'});
}
elsif ($in{'cmd'} =~ "zfsact")  {
	my $cmd = ($conf{'zfs_properties'} =~ /1/) ? "zfs $in{'action'} $in{'zfs'}" : undef;
	print ui_cmd("$in{'action'} $in{'zfs'}", $cmd);
}
elsif ($in{'cmd'} =~ "zfsdestroy")  {
	my $cmd = ($conf{'zfs_destroy'} =~ /1/) ? "zfs destroy $in{'force'} $in{'zfs'}" : undef;
	if (!$in{'confirm'})
	{
		print "Attempting to destroy $in{'zfs'}... <br />";
		print "<br />";
		print ui_form_start('cmd.cgi', 'post');
		print ui_hidden('cmd', $in{'cmd'});
		print ui_hidden('zfs', $in{'zfs'});
		print "<b>This action will affect the following: </b><br />";
		ui_zfs_list('-r '.$in{'destroy'});
		ui_list_snapshots('-r '.$in{'destroy'});
		if (($conf{'zfs_destroy'} =~ /1/) && ($conf{'snap_destroy'} =~ /1/)) { print ui_checkbox('force', '-r', 'Click to destroy all child dependencies (recursive)', undef ), "<br />"; }
		print "<h3>Warning, this action will result in data loss, do you really want to continue?</h3>";
		print ui_checkbox('confirm', 'yes', 'I understand', undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- checkbox must be selected</font>"; }
		print "<br /><br />";
		print ui_submit("Continue", undef, undef);
		print ui_form_end();
		#print ui_cmd("destroy $in{'zfs'}", $cmd);
	} else {
		print ui_cmd("destroy $in{'zfs'}", $cmd);
	}
	@footer = ("index.cgi?mode=zfs", $text{'zfs_return'});
}

#legacy commands





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
@footer = ("index.cgi?mode=snapshot", $text{'snapshot_return'});
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
@footer = ("index.cgi?mode=pools", $text{'index_return'});
#print $in{'snapshot'};
#ui_print_footer("index.cgi?mode=snapshot", $text{'snapshot_return'});
#popup_footer();
}

if (($in{'multisnap'} =~ 1) && ($conf{'snap_destroy'}) =~ /1/) {
	my %snapshot = list_snapshots();
	#%conf = get_zfsmanager_config();
	#$in{'select'} =~ s/^\s*(.*?)\s*$/$1/;
	#$in{'select'} = s/([\w@-_]+)/$1/;
	#$in{'select'} =~ s/.*[^[:print:]]+//;
	@select = split(/;/, $in{'select'});
	#@select = param('select');
	#print "hexdump: ";
	#print Dumper(\$_GET);
	#print Dumper(\$in);
	#print "<br />";
	#print Dumper(\$in{'select'});
	#@select = split(/\R/m, $in{'select'});
	print "<h2>Destroy</h2>";
	print "Attempting to destroy multiple snapshots... <br />";
	#print ui_form_start('cmd.cgi', 'post', 'cmd');
	print ui_form_start('cmd.cgi', 'post');
	print ui_hidden('multisnap', 1);
	print ui_hidden('select', $in{'select'});
	#print "<h1>multisnap</h1> <br />";
	#print $in{'select'};
	my %results = ();
	#print "<br />";
	#print Dumper(@select);
	#print "<br />";
	#print Dumper(@array);
	#print Dumper(\%snapshot);
	print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
	foreach $key (@select)
	{
		$key =~ s/.*[^[:print:]]+//;
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
		#print Dumper(\%results);
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
	@footer = ('index.cgi?mode=snapshot', $text{'snapshot_return'});
	}
	print ui_form_end();

}





print ui_table_end();
if (@footer) { ui_print_footer(@footer); }
if ($in{'cmd'} && $in{'zfs'} && !@footer) {
		print "<br />";
		ui_print_footer("status.cgi?zfs=".$in{'zfs'}, $in{'zfs'});
} elsif ($in{'cmd'} && $in{'pool'} && !@footer) {
		print "<br />";
		ui_print_footer("status.cgi?pool=".$in{'pool'}, $in{'pool'});
} elsif ($in{'cmd'} && $in{'snap'} && !@footer) {
		print "<br />";
		ui_print_footer("status.cgi?snap=".$in{'snap'}, $in{'snap'});
}
