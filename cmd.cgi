#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
ui_print_header(undef, $text{'cmd_title'}, "", undef, 1, 1);
%conf = get_zfsmanager_config();

if ($text{$in{'cmd'}."_desc"}) { 
	print ui_table_start($text{$in{'cmd'}."_cmd"}, "width=100%", "10", ['align=left'] );
	print ui_table_row("Command Description:", $text{$in{'cmd'}."_desc"});
	print ui_table_end();
};

print ui_table_start($text{'cmd_title'}, "width=100%", "10", ['align=left'] );
	
if ($in{'cmd'} =~ "setzfs") {
	$in{'confirm'} = "yes";
	if (($in{'set'} =~ "inherit") && ($conf{'zfs_properties'} =~ /1/)) { $cmd = "zfs inherit $in{'property'} $in{'zfs'}"; 
	} elsif ($conf{'zfs_properties'} =~ /1/) { $cmd =  "zfs set $in{'property'}=$in{'set'} $in{'zfs'}"; }
	print ui_cmd("set zfs property $in{'property'} to $in{'set'} in $in{'zfs'}", $cmd);
}
elsif ($in{'cmd'} =~ "setpool")  {
	$in{'confirm'} = "yes";
	if ($in{'property'} =~ 'comment') { $in{'set'} = '"'.$in{'set'}.'"'; }
	my $cmd = ($conf{'pool_properties'} =~ /1/) ? "zpool set $in{'property'}=$in{'set'} $in{'pool'}": undef;
	print ui_cmd("set pool property $in{'property'} to $in{'set'} in $in{'pool'}", $cmd);
}
elsif ($in{'cmd'} =~ "snapshot")  {
		my $cmd = ($conf{'snap_properties'} =~ /1/) ? "zfs snapshot ".$in{'zfs'}."@".$in{'snap'} : undef;
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
	print ui_cmd("clone ".$in{'clone'}, $cmd);
	@footer = ("status.cgi?snap=".$in{'clone'}, $in{'clone'})
	#$in{'snap'} = $in{'clone'};
}
elsif ($in{'cmd'} =~ "rename")  {
        #$in{'confirm'} = "yes";
	#print "Rename ".$in{'zfs'}." to ".ui_textbox("name", $in{"name"});
	if (index($in{'zfs'}, '@') != -1) { 
		#is a snapshot
		#$in{'snap'} = $in{'zfs'};  
		#$in{'name'} = $in{'parent'}.'@'.$in{'name'};
		#$in{'parent'} = undef;
		$cmd = ($conf{'snap_properties'} =~ /1/) ? "zfs rename ".$in{'force'}.$in{'recurse'}.$in{'zfs'}." ".$in{'parent'}.'@'.$in{'name'} : undef;
		#print ui_hidden('zfs', $in{'zfs'});
		#$in{'zfs'} = undef;
		@footer = ('status.cgi?snap='.$in{'zfs'}, $in{'zfs'});
	} elsif (index($in{'zfs'}, '/') != -1) { 
		#is a filesystem
		#$in{'name'} = $in{'parent'}.'/'.$in{'name'};
		#$in{'parent'} = undef;
		$cmd = ($conf{'zfs_properties'} =~ /1/) ? "zfs rename ".$in{'force'}.$in{'prnt'}.$in{'zfs'}." ".$in{'parent'}.'/'.$in{'name'} : undef; 
	}
        print ui_cmd("rename ".$in{'zfs'}." to ".$in{'name'}, $cmd);
}
elsif ($in{'cmd'} =~ "createzpool")  {
	#if ($in{'add'}) { redirect('create.cgi?srl='.serialise_variable(%in)); }
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
	#print "", (!$result[1]) ? ui_zfs_list($in{'zfs'}) : undef;
	#^^^this doesn't work for some reason
}
elsif ($in{'cmd'} =~ "vdev") {
	$in{'confirm'} = "yes";
	my $cmd =  ($conf{'pool_properties'} =~ /1/) ? "zpool $in{'action'} $in{'pool'} $in{'vdev'}": undef;
	print ui_cmd("$in{'action'} $in{'vdev'}", $cmd);
}
elsif ($in{'cmd'} =~ "promote") {
	my $cmd = ($conf{'zfs_properties'} =~ /1/) ? "zfs promote $in{'zfs'}": undef;
	print ui_cmd("promote $in{'zfs'}", $cmd);
}
elsif ($in{'cmd'} =~ "scrub") {
	$in{'confirm'} = "yes";
	if ($in{'stop'}) { $in{'stop'} = "-s"; }
	my $cmd = ($conf{'pool_properties'} =~ /1/) ? "zpool scrub $in{'stop'} $in{'pool'}" : undef;
	print ui_cmd("scrub pool $in{'pool'}", $cmd);
}
elsif ($in{'cmd'} =~ "upgrade") {
	print "<p>".$text{'zpool_upgrade_msg'}."</p>";
	#$in{'confirm'} = "yes";
	my $cmd = ($conf{'pool_properties'} =~ /1/) ? "zpool upgrade $in{'pool'}" : undef;
	print ui_cmd("upgrade pool $in{'pool'}", $cmd);
}
elsif ($in{'cmd'} =~ "export") {
	$in{'confirm'} = "yes";
	my $cmd = ($conf{'pool_properties'} =~ /1/) ? "zpool export $in{'pool'}" : undef;
	print ui_cmd("scrub pool $in{'pool'}", $cmd);
	@footer = ("index.cgi?mode=pools", $text{'index_return'});
}
elsif ($in{'cmd'} =~ "import")  {
	my $dir = ();
	if ($in{'dir'}) { $dir .= " -d ".$in{'dir'}; }
	if ($in{'destroyed'}) { $dir .= " -D -f "; }
	my $cmd = ($conf{'pool_properties'} =~ /1/ ) ? "zpool import".$dir." ".$in{'import'}: undef;
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
		ui_zfs_list('-r '.$in{'zfs'});
		ui_list_snapshots('-r '.$in{'zfs'});
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
elsif ($in{'cmd'} =~ "snpdestroy")  {
	my $cmd = ($conf{'snap_destroy'} =~ /1/) ? "zfs destroy $in{'force'} $in{'snapshot'}" : undef;
	if (!$in{'confirm'})
	{
		print "Attempting to destroy $in{'snapshot'}...<br />";
		print ui_form_start('cmd.cgi', 'post');
		print ui_hidden('cmd', 'snpdestroy');
		print ui_hidden('snapshot', $in{'snapshot'});
		print "<b>This action will affect the following: </b><br />";
		ui_list_snapshots('-r '.$in{'snapshot'});
		if (($conf{'zfs_destroy'} =~ /1/) && ($conf{'snap_destroy'} =~ /1/)) { print ui_checkbox('force', '-r', 'Click to destroy all child dependencies (recursive)', undef ), "<br />"; }
		print "<h3>Warning, this action will result in data loss, do you really want to continue?</h3>";
		print ui_checkbox('confirm', 'yes', 'I understand', undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- checkbox must be selected</font>"; }
		print "<br /><br />";
		print ui_submit("Continue", undef, undef),;
		print ui_form_end();

	} else {
		print ui_cmd("destroy $in{'snapshot'}", $cmd);
	}
	print ui_form_end();
	@footer = ("index.cgi?mode=snapshot", $text{'snapshot_return'});
}
elsif ($in{'cmd'} =~ "pooldestroy")  {
my $cmd = ($conf{'pool_destroy'} =~ /1/) ? "zpool destroy $in{'pool'}" : undef;
	#print "<h2>Destroy</h2>";
	#ui_zfs_list('-r '.$in{'destroypool'});
	#print ui_list_snapshots($in{'destroy'});

	if (!$in{'confirm'})
	{
		print "Attempting to destroy $in{'pool'}... <br />";
		print ui_form_start('cmd.cgi', 'post');
		print ui_hidden('cmd', 'pooldestroy');
		print ui_hidden('pool', $in{'pool'});
		print "<b>This action will affect the following: </b><br />";
		ui_zfs_list('-r '.$in{'pool'});
		ui_list_snapshots('-r '.$in{'pool'});
		print "<h3>Warning, this action will result in data loss, do you really want to continue?</h3>";
		print ui_checkbox('confirm', 'yes', 'I understand', undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- checkbox must be selected</font>"; }
		print "<br /><br />";
		print ui_submit("Continue", undef, undef);
	} else {
		print ui_cmd("destroy $in{'pool'}", $cmd);
	}
	@footer = ("index.cgi?mode=pools", $text{'index_return'});
}
elsif ($in{'cmd'} =~ "multisnap")  {
	#my $cmd = ($conf{'snap_destroy'})
	my %snapshot = list_snapshots();
	@select = split(/;/, $in{'select'});
	print "<h2>Destroy</h2>";
	print "Attempting to destroy multiple snapshots... <br />";
	print ui_form_start('cmd.cgi', 'post');
	print ui_hidden('cmd', 'multisnap');
	print ui_hidden('select', $in{'select'});
	my %results = ();
	print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
	foreach $key (@select)
	{
		$key =~ s/.*[^[:print:]]+//;
		print ui_columns_row([ $key, $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
		$results{$key} = ($conf{'snap_destroy'}) ? "zfs destroy $key" : undef; 
	}
	print ui_columns_end();
	if (!$in{'confirm'})
	{
		print "<h2>Commands to be issued:</h2>";
		foreach $key (keys %results)
		{
			print $results{$key}, "<br />";
		}	
		print "<h3>Warning, this action will result in data loss, do you really want to continue?</h3>";
		print ui_checkbox('confirm', 'yes', 'I understand', undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- checkbox must be selected</font>"; }
		print "<br /><br />";
		print ui_submit("Continue", undef, undef), " | <a href='index.cgi?mode=snapshot'>Cancel</a>";
	} else {
		print "<h2>Results from commands:</h2>";
		foreach $key (keys %results)
		{
		my @result = (`$results{$key} 2>&1`);
			if (($result[1] eq undef))
			{
				print $results{$key}, "<br />";
				print "Success! <br />";
			} else
			{
				print $results{$key}, "<br />";
				print "error: ", $result[0], "<br />";
			}
		}
	}
	print ui_form_end();
	@footer = ('index.cgi?mode=snapshot', $text{'snapshot_return'});
}


print ui_table_end();
if (@footer) { ui_print_footer(@footer); }
if ($in{'zfs'} && !@footer) {
		print "<br />";
		ui_print_footer("status.cgi?zfs=".$in{'zfs'}, $in{'zfs'});
} elsif ($in{'pool'} && !@footer) {
		print "<br />";
		ui_print_footer("status.cgi?pool=".$in{'pool'}, $in{'pool'});
} elsif ($in{'snap'} && !@footer) {
		print "<br />";
		ui_print_footer("status.cgi?snap=".$in{'snap'}, $in{'snap'});
}
