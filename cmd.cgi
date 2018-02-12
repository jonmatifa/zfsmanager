#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
ui_print_header(undef, $text{'cmd_title'}, "", undef, 1, 1);

if ($text{$in{'cmd'}."_desc"}) { 
	print ui_table_start($text{$in{'cmd'}."_cmd"}, "width=100%", "10", ['align=left'] );
	print ui_table_row($text{'cmd_dscpt'}, $text{$in{'cmd'}."_desc"});
	print ui_table_end();
};

print ui_table_start($text{'cmd_title'}, "width=100%", "10", ['align=left'] );
	
if ($in{'cmd'} =~ "setzfs") {
	$in{'confirm'} = "yes";
	if (($in{'set'} =~ "inherit") && ($config{'zfs_properties'} =~ /1/)) { $cmd = "zfs inherit $in{'property'} $in{'zfs'}"; 
	} elsif ($config{'zfs_properties'} =~ /1/) { $cmd =  "zfs set $in{'property'}=$in{'set'} $in{'zfs'}"; }
	ui_cmd("$in{'property'} to $in{'set'} on $in{'zfs'}", $cmd);
}
elsif ($in{'cmd'} =~ "setpool")  {
	$in{'confirm'} = "yes";
	if ($in{'property'} =~ 'comment') { $in{'set'} = '"'.$in{'set'}.'"'; }
	my $cmd = ($config{'pool_properties'} =~ /1/) ? "zpool set $in{'property'}=$in{'set'} $in{'pool'}": undef;
	ui_cmd("$in{'property'} to $in{'set'} in $in{'pool'}", $cmd);
}
elsif ($in{'cmd'} =~ "snapshot")  {
	my $cmd = ($config{'snap_properties'} =~ /1/) ? "zfs snapshot ".$in{'zfs'}."@".$in{'snap'} : undef;
	$in{'confirm'} = "yes";
	ui_cmd($in{'snap'}, $cmd);
	print "", (!$result[1]) ? ui_list_snapshots($in{'zfs'}."@".$in{'snap'}) : undef;
}
elsif ($in{'cmd'} =~ "send") {
	if (!$in{'dest'}) {
                print $text{'cmd_send'}." ".$in{'snap'}." ".$text{'cmd_gzip'}."  <br />";
                print "<br />";
                print ui_form_start('cmd.cgi', 'post');
                print ui_hidden('cmd', $in{'cmd'});
		print ui_hidden('snap', $in{'snap'});
		my $newfile = $in{'snap'} =~ s![/@]!_!gr;
		print "<b>$text{'destination'} </b>".ui_filebox('dest', $config{'last_send'}, 35, undef, undef, undef, 1)."<br />";
		print "<b>$text{'filename'} </b>".ui_textbox('file', $newfile.'.gz', 50)."<br />";
		print ui_submit($text{'continue'}, undef, undef);
                print ui_form_end();
	} else { 
		$in{'confirm'} = "yes";
		my $cmd = ($config{'snap_properties'} =~ /1/) ? "zfs send ".$in{'snap'}." | gzip > ".$in{'dest'}."/".$in{'file'} : undef;
		ui_cmd($in{'snap'}, $cmd);
		$config{'last_send'} = $in{'dest'};
		save_module_config();
		print `ls -al $in{'dest'}'."/".$in{'file'}`;
	}
}
elsif ($in{'cmd'} =~ "createzfs")  {
	my %createopts = create_opts();
	my %options = ();
	foreach $key (sort (keys %createopts)) {
		$options{$key} = ($in{$key}) ? $in{$key} : undef;
	}
	if ($in{'mountpoint'}) { $options{'mountpoint'} = $in{'mountpoint'}; }
	if ($in{'zvol'} == '1') { 
		$options{'zvol'} = $in{'size'};
		$options{'sparse'} = $in{'sparse'};
		$options{'volblocksize'} = $in{'volblocksize'};
	} 
	my $cmd = (($in{'parent'}) && ($config{'zfs_properties'} =~ /1/)) ? cmd_create_zfs($in{'parent'}."/".$in{'zfs'}, \%options) : undef;
	$in{'confirm'} = "yes";
	ui_cmd("$in{'parent'}/$in{'zfs'}", $cmd);
	#print "", (!$result[1]) ? ui_zfs_list($in{'zfs'}) : undef;
	#^^^this doesn't work for some reason
	@footer = ("status.cgi?zfs=".$in{'parent'}."/".$in{'zfs'}, $in{'parent'}."/".$in{'zfs'});
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
	my $cmd =  ($config{'zfs_properties'} =~ /1/) ? "zfs clone ".$in{'clone'}." ".$in{'parent'}.'/'.$in{'zfs'}." ".$opts : undef;
	ui_cmd($in{'clone'}, $cmd);
	@footer = ("status.cgi?snap=".$in{'clone'}, $in{'clone'})
}
elsif ($in{'cmd'} =~ "rename")  {
	if (index($in{'zfs'}, '@') != -1) { 
		$cmd = ($config{'snap_properties'} =~ /1/) ? "zfs rename ".$in{'force'}.$in{'recurse'}.$in{'zfs'}." ".$in{'parent'}.'@'.$in{'name'} : undef;
		@footer = ('status.cgi?snap='.$in{'parent'}.'@'.$in{'name'}, $in{'parent'}.'@'.$in{'name'});
	} elsif (index($in{'zfs'}, '/') != -1) { 
		$cmd = ($config{'zfs_properties'} =~ /1/) ? "zfs rename ".$in{'force'}.$in{'prnt'}.$in{'zfs'}." ".$in{'parent'}.'/'.$in{'name'} : undef; 
	}
        ui_cmd($in{'zfs'}." to ".$in{'name'}, $cmd);
}
elsif ($in{'cmd'} =~ "createzpool")  {
	my %createopts = create_opts();
	my %options = ();
	$in{'volblocksize'} = "default";
	$in{'sparse'} = "default";
	foreach $key (sort (keys %createopts)) {
		$options{$key} = ($in{$key}) ? $in{$key} : undef;
	}
	if ($in{'mountpoint'}) { $options{'mountpoint'} = $in{'mountpoint'}; }
	if ($in{'vdev'} =~ 'stripe') { delete $in{'vdev'}; } else{ $in{'vdev'} .= " "; }
	$in{'devs'} =~ s/\R/ /g;
	%poolopts = ( 'version' => $in{'version'} );
	my $cmd = (($config{'pool_properties'} =~ /1/)) ? cmd_create_zpool($in{'pool'}, $in{'vdev'}.$in{'devs'}, \%options, \%poolopts, $in{'force'}) : undef;
	$in{'confirm'} = "yes";
	ui_cmd($in{'pool'}, $cmd);
	#print "", (!$result[1]) ? ui_zfs_list($in{'zfs'}) : undef;
	#^^^this doesn't work for some reason
}
elsif ($in{'cmd'} =~ "vdev") {
	$in{'confirm'} = "yes";
	my $cmd =  ($config{'pool_properties'} =~ /1/) ? "zpool $in{'action'} $in{'pool'} $in{'vdev'}": undef;
	ui_cmd("$in{'action'} $in{'vdev'}", $cmd);
}
elsif ($in{'cmd'} =~ "promote") {
	my $cmd = ($config{'zfs_properties'} =~ /1/) ? "zfs promote $in{'zfs'}": undef;
	ui_cmd($in{'zfs'}, $cmd);
}
elsif ($in{'cmd'} =~ "scrub") {
	$in{'confirm'} = "yes";
	if ($in{'stop'}) { $in{'stop'} = "-s"; }
	my $cmd = ($config{'pool_properties'} =~ /1/) ? "zpool scrub $in{'stop'} $in{'pool'}" : undef;
	ui_cmd($in{'pool'}, $cmd);
}
elsif ($in{'cmd'} =~ "upgrade") {
	print "<p>".$text{'zpool_upgrade_msg'}."</p>";
	my $cmd = ($config{'pool_properties'} =~ /1/) ? "zpool upgrade $in{'pool'}" : undef;
	ui_cmd($in{'pool'}, $cmd);
}
elsif ($in{'cmd'} =~ "export") {
	my $cmd = ($config{'pool_properties'} =~ /1/) ? "zpool export $in{'pool'}" : undef;
	ui_cmd($in{'pool'}, $cmd);
	@footer = ("index.cgi?mode=pools", $text{'index_return'});
}
elsif ($in{'cmd'} =~ "import")  {
	my $dir = ();
	if ($in{'dir'}) { $dir .= " -d ".$in{'dir'}; }
	if ($in{'destroyed'}) { $dir .= " -D -f "; }
	my $cmd = ($config{'pool_properties'} =~ /1/ ) ? "zpool import".$dir." ".$in{'import'}: undef;
	ui_cmd($in{'import'}, $cmd);
	@footer = ("index.cgi?mode=pools", $text{'index_return'});
}
elsif ($in{'cmd'} =~ "zfsact")  {
	my $cmd = ($config{'zfs_properties'} =~ /1/) ? "zfs $in{'action'} $in{'zfs'}" : undef;
	ui_cmd("$in{'action'} $in{'zfs'}", $cmd);
}
elsif ($in{'cmd'} =~ "zfsdestroy")  {
	my $cmd = ($config{'zfs_destroy'} =~ /1/) ? "zfs destroy $in{'force'} $in{'zfs'}" : undef;
	if (!$in{'confirm'})
	{
		print $text{'cmd_destroy'}." $in{'zfs'}... <br />";
		print "<br />";
		print ui_form_start('cmd.cgi', 'post');
		print ui_hidden('cmd', $in{'cmd'});
		print ui_hidden('zfs', $in{'zfs'});
		print "<b>$text{'cmd_affect'} </b><br />";
		ui_zfs_list('-r '.$in{'zfs'});
		ui_list_snapshots('-r '.$in{'zfs'});
		if (($config{'zfs_destroy'} =~ /1/) && ($config{'snap_destroy'} =~ /1/)) { print ui_checkbox('force', '-r', 'Click to destroy all child dependencies (recursive)', undef ), "<br />"; }
		print "<h3>$text{'cmd_warning'}</h3>";
		print ui_checkbox('confirm', 'yes', $text{'cmd_understand'}, undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- $text{'cmd_checkbox'}</font>"; }
		print "<br /><br />";
		print ui_submit($text{'continue'}, undef, undef);
		print ui_form_end();
	} else {
		ui_cmd($in{'zfs'}, $cmd);
	}
	@footer = ("index.cgi?mode=zfs", $text{'zfs_return'});
}
elsif ($in{'cmd'} =~ "snpdestroy")  {
	my $cmd = ($config{'snap_destroy'} =~ /1/) ? "zfs destroy $in{'force'} $in{'snapshot'}" : undef;
	if (!$in{'confirm'})
	{
		print $text{'cmd_destroy'}." $in{'snapshot'}...<br />";
		print ui_form_start('cmd.cgi', 'post');
		print ui_hidden('cmd', 'snpdestroy');
		print ui_hidden('snapshot', $in{'snapshot'});
		print "<b>$text{'cmd_affect'} </b><br />";
		ui_list_snapshots('-r '.$in{'snapshot'});
		if (($config{'zfs_destroy'} =~ /1/) && ($config{'snap_destroy'} =~ /1/)) { print ui_checkbox('force', '-r', 'Click to destroy all child dependencies (recursive)', undef ), "<br />"; }
		print "<h3>$text{'cmd_warning'}</h3>";
		print ui_checkbox('confirm', 'yes', $text{'cmd_understand'}, undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- $text{'cmd_checkbox'}</font>"; }
		print "<br /><br />";
		print ui_submit($text{'continue'}, undef, undef),;
		print ui_form_end();

	} else {
		ui_cmd($in{'snapshot'}, $cmd);
	}
	print ui_form_end();
	%parent = find_parent($in{'snapshot'});
	@footer = ("status.cgi?zfs=".$parent{'filesystem'}, $parent{'filesystem'});
}
elsif ($in{'cmd'} =~ "pooldestroy")  {
my $cmd = ($config{'pool_destroy'} =~ /1/) ? "zpool destroy $in{'pool'}" : undef;
	if (!$in{'confirm'})
	{
		print $text{'cmd_destroy'}." $in{'pool'}... <br />";
		print ui_form_start('cmd.cgi', 'post');
		print ui_hidden('cmd', 'pooldestroy');
		print ui_hidden('pool', $in{'pool'});
		print "<b>$text{'cmd_affect'} </b><br />";
		ui_zfs_list('-r '.$in{'pool'});
		ui_list_snapshots('-r '.$in{'pool'});
		print "<h3>$text{'cmd_warning'}</h3>";
		print ui_checkbox('confirm', 'yes', $text{'cmd_understand'}, undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- $text{'cmd_checkbox'}</font>"; }
		print "<br /><br />";
		print ui_submit($text{'continue'}, undef, undef);
	} else {
		ui_cmd($in{'pool'}, $cmd);
	}
	@footer = ("index.cgi?mode=pools", $text{'index_return'});
}
elsif ($in{'cmd'} =~ "multisnap")  {
	%snapshot = ();
	@select = split(/;/, $in{'select'});
	print "<h2>$text{'destroy'}</h2>";
	print $text{'cmd_multisnap'}." <br />";
	print ui_form_start('cmd.cgi', 'post');
	print ui_hidden('cmd', 'multisnap');
	print ui_hidden('select', $in{'select'});
	my %results = ();
	print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
	foreach $key (@select)
	{
		$key =~ s/.*[^[:print:]]+//;
		my %snapshot = list_snapshots($key);
		print ui_columns_row([ $key, $snapshot{'00000'}{used}, $snapshot{'00000'}{refer} ]);
		#print Dumper(\%snapshot);
		$results{$key} = ($config{'snap_destroy'}) ? "zfs destroy $key" : undef; 
	}
	print ui_columns_end();
	if (!$in{'confirm'})
	{
		print "<h2>$text{'cmd_issue'}</h2>";
		foreach $key (keys %results)
		{
			print $results{$key}, "<br />";
		}	
		print "<h3>$text{'cmd_warning'}</h3>";
		print ui_checkbox('confirm', 'yes', $text{'cmd_understand'}, undef );
		print ui_hidden('checked', 'no');
		if ($in{'checked'} =~ /no/) { print " <font color='red'> -- $text{'cmd_checkbox'}</font>"; }
		print "<br /><br />";
		print ui_submit($text{'continue'}, undef, undef), " | <a href='index.cgi?mode=snapshot'>Cancel</a>";
	} else {
		print "<h2>$text{'cmd_results'}</h2>";
		foreach $key (keys %results)
		{
		my @result = (`$results{$key} 2>&1`);
			if (($result[1] eq undef))
			{
				print $results{$key}, "<br />";
				print "$text{'cmd_success'} <br />";
			} else
			{
				print $results{$key}, "<br />";
				print "$text{'cmd_error'} ", $result[0], "<br />";
			}
		}
	}
	print ui_form_end();
	@footer = ('index.cgi', $text{'index_return'});
}
elsif ($in{'cmd'} =~ "replace") {
	#$in{'confirm'} = "yes";
	if ($in{'new'}) {
		my $cmd =  ($config{'pool_properties'} =~ /1/) ? "zpool replace $in{'pool'} $in{'vdev'} $in{'new'}": undef;
		print ui_hidden("new", $in{'new'});
		ui_cmd("replace $in{'vdev'} on $in{'pool'} with $in{'new'}", $cmd);
	} else {
		print "Replace $in{'vdev'} on $in{'pool'}: <br />";
		print ui_form_start('cmd.cgi', 'post');
		print ui_hidden("cmd", 'replace');
		print ui_hidden("vdev", $in{'vdev'});
		print ui_hidden("pool", $in{'pool'});
		print "New device: ".ui_filebox("new", "/dev/disk/by-id/")." ".ui_submit('Select');
		print ui_form_end();
	}
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
