#!/usr/bin/perl

require './zfsmanager-lib.pl';
#foreign_require('fdisk', 'fdisk-lib.pl');
ReadParse();
use Data::Dumper;
#popup_header('Create '.$in{'create'});
my %createopts = create_opts();
my %proplist = properties_list();

#create zpool
if ($in{'create'} =~ "zpool")
{
	ui_print_header(undef, "Create Pool", "", undef, 1, 1);
	#if ($in{srl}) { %in = unserialise_variable($in{srl}); }
	print ui_table_start("Create Zpool", 'width=100%');
	print ui_form_start("cmd.cgi", "post");
	print ui_hidden('cmd', 'createzpool');
	print ui_hidden('create', 'zpool');
	print ui_table_row(undef, '<b>Pool name:</b> '.ui_textbox('pool', $in{'pool'}));
	print ui_table_row(undef, '<b>Mount point</b> (blank for default)'.ui_filebox('mountpoint', $in{'mountpoint'}, 25, undef, undef, 1));
	#print ui_select('vdev', ['sdb1', 'sdc1'], ['sdb1', 'sdc1'], undef, 1);
	#print ui_table_row(undef, '<b>vdev configuration:</b> '.ui_textbox('dev', ''));
	#print ui_table_row(undef, '<b>Activate all features:</b> '.ui_checkbox('allfeat', '1'));
	if (!$in{'version'}) { $in{'version'} = 'default'; }
	print ui_table_row(undef, '<b>Pool version:</b> '.ui_select('version', $in{'version'}, ['default', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28'], 1, 0, 1));
	print ui_table_row(undef, '<b>Force</b> '.ui_checkbox('force', '-f'));
	print ui_table_row(undef, "<br />");
	delete $createopts{'sparse'};
	delete $createopts{'volblocksize'};
	print ui_table_end();
	print ui_table_start("File system options", "width=100%", undef);
	#print 'File system options: <br />';
	foreach $key (sort(keys %createopts))
	{
		my @select = [ split(", ", $proplist{$key}) ];
		if ($proplist{$key} eq 'boolean') { @select = [ 'default', 'on', 'off' ]; }
		print ui_table_row($key, ui_select($key, 'default', @select, 1, 0, 1));
		#print $key, ': ', ui_select($key, 'default', @select, 1, 0, 1), '<br />';
	}
	#print ui_table_row('Pool version:', ui_select('version', 'default', ['default', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', 'features-disabled', 'features-enabled'], 1, 0, 1));
	#print 'Pool version: ', ui_select('version', 'default', ['default', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', 'features-disabled','features-enabled'], 1, 0, 1), '<br />';
	print ui_table_row(undef, "<br />");
	print ui_table_end();
	print ui_table_start("Device Configuration:", "width=100%", undef);
	#print ui_select('vdev0', 'pool', ['pool', 'mirror', 'raidz1', 'raidz2', 'raidz3', 'log', 'cache'], undef, undef, undef, undef, '');
	#print 'vdev configuration: ', ui_textbox('vdev', '');
	#print ui_popup_link('Add vdev', 'select.cgi'), "<br />";
	
	#print "vdev type: ", ui_radio('vdev', 'stripe', [ ['stripe', 'stripe'], ['mirror', 'mirror'], ['raidz1', 'raidz1'],  ['raidz2', 'raidz2'], ['raidz3', 'raidz3'] ] );
	if (!$in{'vdev'}) { $in{'vdev'} = 'stripe'; }
	print "vdev type: ", ui_select('vdev', $in{'vdev'}, ['stripe', 'mirror', 'raidz1', 'raidz2', 'raidz3'], 1, 0, 1);
	print "<br />";
	my %hash = list_disk_ids();
	#delete $hash{'byuuid'};
	#@byid = ();
	#foreach $key (sort(keys %{ $hash{byid}})) {
	#	push (@byid, $key);
	#}
	#print Dumper (\%hash);
	#print "By Disk-ID: ", ui_select("byid", undef, [keys %{ $hash{byid} }]);
	#print "<br />";
	#print ui_select("devs", undef, [keys %{ $hash{byid} }], undef, 1);
	
	my @devs = (sort(keys %{$hash{byid}}));
	my @prev = split(";", $in{'prev'});
	push (@prev, $in{'adtl'});
	print ui_hidden("prev", join(';', @prev));
	#print ui_form_start('create.cgi', 'post');
	#print "Add custom file to selection: ".ui_filebox("adtl")." ".ui_submit('Add', 'add')."<br />";
	#print file_choose_button('adtl', 0);
	#print ui_form_end();
	push (@devs, @prev);
	#print ui_multi_select("devs", undef, [(sort(keys %{ $hash{byid}}))], 8, undef, undef , 'available', 'selected', 425);
	print ui_multi_select("devs", undef, [@devs], 8, undef, undef, 'available', 'selected', 425);
        #print "By UUID: ", ui_select("byuuid", undef, [keys %{ $hash{byuuid} }]);
	#print "<br />";
	#print 'Manual selection: ', ui_filebox('byfile', '', 25, undef, undef, 1);
	#print "<br />";
	print ui_table_end();
	print ui_submit('Create', 'create');
	print ui_form_end();

	print ui_form_start('create.cgi', 'post');
	print ui_hidden('prev', join(';', @prev));
	print ui_hidden('create', 'zpool');
	print "Add custom file to selection: ".ui_filebox("adtl")." ".ui_submit('Add');
	print ui_form_end();
	#print Dumper (\%hash);
	#print " | ";
	ui_print_footer('', $text{'index_return'});
	#print "<a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
	#print popup_window_button( 'cmd.cgi', '600', '400', '1', [ [ 'pool', 'pool', 'pool'], ['create', 'create', 'create'], ['dev', 'dev', 'dev'], ['mountpoint', 'mountpoint', 'mountpoint'], ['force', 'force', 'force'] ] );
	#mount::generate_location("vdev", "");
	#print ui_table_row();
	#mount::generate_location("vdev", "");
	#print ui_table_end();
	#print &ui_form_end([ [ undef, "create" ] ]);
	#print Dumper(\%in)

#create zfs file system
#TODO the $in{'pool'} variable should be changed to $in{'parent'}, but it still works
} elsif (($in{'create'} =~ "zfs") & ($in{'parent'} eq undef)) {
	ui_print_header(undef, "Create File System", "", undef, 1, 1);
	print "<b>Select parent for file system</b>";
	ui_zfs_list(undef, "create.cgi?create=zfs&parent=");
	ui_print_footer('index.cgi?mode=zfs', $text{'zfs_return'});
} elsif (($in{'create'} =~ "zfs")) {
	ui_print_header(undef, "Create File System", "", undef, 1, 1);
	#print "Pool:";
	#ui_zpool_status($in{'pool'});
	#Show associated file systems
	
	print "Parent file system:";
	ui_zfs_list("-r ".$in{'parent'}, "");
	
	@tabs = ();
	push(@tabs, [ "zfs", "Create Filesystem", "create.cgi?mode=zfs" ]);
	push(@tabs, [ "zvol", "Create Volume", "create.cgi?mode=zvol" ]);
	print &ui_tabs_start(\@tabs, "mode", $in{'mode'} || $tabs[0]->[0], 1);
	
	print &ui_tabs_start_tab("mode", "zfs");
	#%zfs = list_zfs("-r ".$in{'parent'});
	#print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
	#foreach $key (sort(keys %zfs)) 
	#{
	#	print ui_columns_row(["<a href=''>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
	#}
	#print ui_columns_end();
	
	print ui_form_start("cmd.cgi", "post");
	#print ui_hidden('property', $in{'property'});
	print ui_table_start('New File System', 'width=100%', '6');
	#print "<h3>New File System: </h3>";
	print ui_table_row(undef, "<b>Name: </b>".$in{'parent'}."/".ui_textbox('zfs'));
	print ui_table_row(undef, '<b>Mount point</b> (blank for default)'.ui_filebox('mountpoint', '', 25, undef, undef, 1));
	print ui_hidden('parent', $in{'parent'});
	print ui_hidden('create', 'zfs');
	print ui_hidden('cmd', 'createzfs');
	print ui_table_row(undef, "<br />");
	#print ui_table_row(undef, 'File system options: ');
	#delete $createopts{'sparse'};
	#delete $createopts{'volblocksize'};
	#my %list = ( 'atime' => 'on', 'compression' => 'off', 'exec' => 'on', 'readonly' => 'off', 'utf8only' => 'off');
	print ui_table_end();
	print ui_table_start("File system options", "width=100%", undef);
	foreach $key (sort(keys %createopts))
	{
		my @select = [ split(", ", $proplist{$key}) ];
		if ($proplist{$key} eq 'boolean') { @select = [ 'default', 'on', 'off' ]; }
		print ui_table_row($key.': ', ui_select($key, 'default', @select, 1, 0, 1));
	}
	print ui_table_end();
	print ui_submit('Create');
	print ui_form_end();
	print &ui_tabs_end_tab("mode", "zfs");

	print &ui_tabs_start_tab("mode", "zvol");
	print ui_form_start("cmd.cgi", "post");
	#print ui_hidden('property', $in{'property'});
	print ui_table_start('New Volume', 'width=100%', '6');
	#print "<h3>New File System: </h3>";
	print ui_table_row(undef, "<b>Name: </b>".$in{'parent'}."/".ui_textbox('zfs'));
	print ui_table_row(undef, "<b>Size: </b>".ui_textbox('size'));
	print ui_table_row(undef, '<b>Blocksize:</b> '.ui_select('volblocksize', 'default', ['default', '512', '1K', '2K', '4K', '8K', '16K', '32K', '64K', '128K'], 1, 0, 1));
	#delete $createopts{'volblocksize'};
	print ui_table_row(undef, '<b>Sparse volume:</b> '.ui_checkbox('sparse', '1'));
	#delete $createopts{'sparse'};
	print ui_hidden('parent', $in{'parent'});
	print ui_hidden('create', 'zfs');
	print ui_hidden('cmd', 'createzfs');
	print ui_hidden('zvol', '1');
	print ui_table_row(undef, "<br />");
	#print ui_table_row(undef, 'File system options: ');
	print ui_table_end();
	print ui_table_start("Volume options", "width=100%", undef);
	foreach $key (sort(keys %createopts))
	{
		my @select = [ split(", ", $proplist{$key}) ];
		if ($proplist{$key} eq 'boolean') { @select = [ 'default', 'on', 'off' ]; }
		print ui_table_row($key.': ', ui_select($key, 'default', @select, 1, 0, 1));
	}
	print ui_table_end();
	print ui_submit('Create');
	print ui_form_end();
	#print " | ";
	print &ui_tabs_end_tab("mode", "zvol");

	#end tabs
	print &ui_tabs_end(1);
	ui_print_footer("status.cgi?zfs=$in{'parent'}", $in{'parent'});
	#ui_print_footer('index.cgi?mode=zfs', $text{'zfs_return'});
	
} elsif ($in{'import'}) {
	ui_print_header(undef, "Import Pool", "", undef, 1, 1);
	print ui_table_start("Import Zpool", 'width=100%');
	print ui_form_start("create.cgi", "post");
	print ui_hidden('import', '1');
	print ui_table_row(undef, "Import search directory (blank for default):".ui_filebox('dir', $in{'dir'}, 25, undef, undef, 1));
	print ui_table_row(undef, ui_checkbox('destroyed', '-D', 'Search for destroyed pools', undef ), "<br />");
	#print "<br />";
	print ui_table_row(undef, ui_submit('Search'));
	print ui_form_end();
	#print " | ";
	#print ui_table_row();
	%imports = zpool_imports($in{'dir'}, $in{'destroyed'});
	#print Dumper (\%imports);
	print "<br />";
	#my @array = split("\n", `zpool import -d $in{'dir'}`);
	#print Dumper (@array);
	#print ui_table_row('');
	#print ui_table_start();
	foreach $key (sort(keys %imports))
	{
		print ui_columns_start([ "Pool", "ID", "State" ]);
		print ui_columns_row(["<a href='cmd.cgi?cmd=import&import=$key&dir=$in{'dir'}&destroyed=$in{destroyed}'>".$key."</a>", "<a href='cmd.cgi?cmd=import&import=$imports{$key}{'id'}&dir=$in{'dir'}&destroyed=$in{destroyed}'>".$imports{$key}{'id'}."</a>", $imports{$key}{'state'}]);
		#print ui_table_row("<a href='cmd.cgi?import=$key&dir=$in{'dir'}'>".$key."</a>", $imports{$key}{'id'}." ".$imports{$key}{'state'}, 3);
		#print ui_columns_end();
		print ui_table_start();
		#print ui_table_row(undef, "Devices: ");
		if ($imports{$key}{vdevs}) { foreach $dev (sort(keys %{ $imports{$key}{vdevs} }))
		{
			#print ui_columns_start([ "Dev", "State" ]);
			#print ui_columns_row([$dev, $imports{$key}{'vdevs'}{$dev}{'state'}]);
			print ui_table_row($dev, "State: ".$imports{$key}{'vdevs'}{$dev}{'state'});
		} }
		print ui_table_end();
		print ui_columns_end();
	}
	
	print ui_table_end();
	ui_print_footer('', $text{'index_return'});
	#print "<a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
} elsif ($in{'clone'}) {
	ui_print_header(undef, "Clone Snapshot", "", undef, 1, 1);
	#ui_zfs_list("-r ".$in{'parent'}, "");
	my ($parent) = split('/', $in{'clone'});
	($parent) = split('@', $parent);
	print ui_form_start("cmd.cgi", "post");
	print ui_table_start('Clone Snapshot', 'width=100%', '6');
	print ui_table_row(undef, '<b>Snapshot:</b> '.$in{'clone'});
	print ui_table_row(undef, "<b>Name: </b>".$parent."/".ui_textbox('zfs'));
	print ui_table_row(undef, '<b>Mount point</b> (blank for default)'.ui_filebox('mountpoint', '', 25, undef, undef, 1));
	print ui_hidden('cmd', 'clone');
	print ui_hidden('clone', $in{'clone'});
	print ui_hidden('parent', $parent);
	print ui_table_row(undef, "<br />");
	print ui_table_row(undef, '<b>File system options:</b> ');
	foreach $key (sort(keys %createopts))
	{
		my @select = [ split(", ", $proplist{$key}) ];
		if ($proplist{$key} eq 'boolean') { @select = [ 'default', 'on', 'off' ]; }
		print ui_table_row($key.': ', ui_select($key, 'default', @select, 1, 0, 1));
	}
	print ui_table_end();
	print ui_submit('Create');
	print ui_form_end();
	#print " | ";
	ui_print_footer("status.cgi?snap=".$in{'clone'}, $in{'clone'});
	#print "<a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
} elsif ($in{'send'}) {
	ui_print_header(undef, "Send Snapshot", "", undef, 1, 1);
	print ui_form_start("cmd.cgi", "get");
	print ui_table_start('Send Snapshot', 'width=100%', '6');
	print ui_table_row(undef, '<b>Snapshot:</b> '.$in{'send'});
	print ui_table_row(undef, ui_oneradio('type', 'new', '<b>New local filesystem</b> ', 1));
	%hash = list_zfs();
	@zfs = keys(%hash);
	print ui_table_row(undef, "<b>Name: </b>".ui_select('parent', undef, [@zfs])."/".ui_textbox('zfs'));
	print ui_table_row(undef, ui_checkbox('replicate', '1', 'Replicate entire file system?', 0));
	print ui_hidden('send', $in{'send'});
	print ui_table_row(undef, "<br />");
	print ui_table_row(undef, ui_oneradio('type', 'exist', '<b>Existing local filesystem</b> ', 0));
	print ui_table_row(undef, "<b>Name: </b>".ui_select('existzfs', undef, [@zfs]));
	print ui_table_row(undef, ui_checkbox('increment', '1', 'Incremental?', 0));
	print ui_table_row(undef, ui_checkbox('force', '1', 'Force overwrite?', 0));
	print ui_table_row(undef, "<br />");
	print ui_table_row(undef, ui_oneradio('type', 'ssh', '<b>Remote filesystem by SSH</b> ', 0, undef, 1));
	print ui_table_row(undef, "<i>Not yet implemented</i>");
	print ui_table_row(undef, "<br />");
	print ui_table_end();
	print ui_submit('Send');
	print " | ";
	ui_print_footer('index.cgi?mode=snapshot', $text{'snapshot_return'});
	#print "<a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
} elsif (($in{'create'} =~ "snapshot") &&  ($in{'zfs'} eq undef)) {
	ui_print_header(undef, $text{'snapshot_new'}, "", undef, 1, 1);
	%zfs = list_zfs();
	#print "Select filesystem for snapshot";
	print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
	foreach $key (sort(keys %zfs)) 
	{
		print ui_columns_row(["<a href='create.cgi?create=snapshot&zfs=$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
	}
	print ui_columns_end();
	ui_print_footer('index.cgi?mode=snapshot', $text{'snapshot_return'});
#handle creation of snapshot
} elsif ($in{'create'} =~ "snapshot") {
	ui_print_header(undef, $text{'snapshot_create'}, "", undef, 1, 1);
	%zfs = list_zfs($in{'zfs'});
	print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
	foreach $key (sort(keys %zfs)) 
	{
		print ui_columns_row(["<a href='status.cgi?zfs=$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
	}
	print ui_columns_end();
	#show list of snapshots based on filesystem
	print "Snapshots already on this filesystem: <br />";
	%snapshot = list_snapshots();
	print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
	foreach $key (sort(keys %snapshot)) 
	{
		if ($key =~ ($in{'zfs'}."@") ) { print ui_columns_row(["<a href='snapshot.cgi?snap=$key'>$key</a>", $snapshot{$key}{used}, $snapshot{$key}{refer} ]); }
	}
	print ui_columns_end();
	print ui_create_snapshot($in{'zfs'});
	ui_print_footer('index.cgi?mode=snapshot', $text{'snapshot_return'});
}

