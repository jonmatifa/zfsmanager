#!/usr/bin/perl

require './zfsmanager-lib.pl';
#foreign_require('fdisk', 'fdisk-lib.pl');
ReadParse();
use Data::Dumper;
#ui_print_header(undef, "Create Zpool", "", undef, 1, 1);
popup_header('Create '.$in{'create'});
my %createopts = create_opts();
my %proplist = properties_list();

#create zpool
if ($in{'create'} =~ "zpool")
{
	#ui_print_header(undef, "Create Zpool", "", undef, 1, 1);
	print ui_form_start("cmd.cgi", "post");
	print ui_table_start("Create Zpool");
	print ui_hidden('create', 'zpool');
	print 'Pool name: ', ui_textbox('pool', ''), "<br />";
	print 'Mount point (blank for default)', ui_filebox('mountpoint', '', 25, undef, undef, 1), "<br />";
	#print ui_select('vdev', ['sdb1', 'sdc1'], ['sdb1', 'sdc1'], undef, 1);
	#print 'vdev configuration: ', ui_textarea('vdev', '', ), '<br />';
	print 'vdev configuration: ', ui_textbox('dev', ''), '<br />';
	print 'File system options: <br />';
	foreach $key (sort(keys %createopts))
	{
		my @select = [ split(", ", $proplist{$key}) ];
		if ($proplist{$key} eq 'boolean') { @select = [ 'default', 'on', 'off' ]; }
		print $key, ': ', ui_select($key, 'default', @select, 1, 0, 1), '<br />';
	}
	print 'Pool version: ', ui_select('version', 'default', ['default', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '5000'], 1, 0, 1), '<br />';
	#print ui_select('vdev0', 'pool', ['pool', 'mirror', 'raidz1', 'raidz2', 'raidz3', 'log', 'cache'], undef, undef, undef, undef, '');
	#print 'vdev configuration: ', ui_textbox('vdev', '');
	#print ui_popup_link('Add vdev', 'select.cgi'), "<br />";
	
	%hash = list_disk_ids();
	#print Dumper (\%hash);
	print "By Disk-ID: ", ui_select("byid", undef, [keys($hash{byid})]);
	print "<br />";
	print "By UUID: ", ui_select("byuuid", undef, [keys($hash{byuuid})]);
	print "<br />";
	print 'Manual selection: ', ui_filebox('byfile', '', 25, undef, undef, 1);
	print "<br />";
	print ui_checkbox('force', '-f', 'Force', 0), "<br />";
	print ui_submit('Create');
	print " | ";
	print "<a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
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
	#ui_print_header(undef, "Create File System", "", undef, 1, 1);
	print "Select parent for file system";
	ui_zfs_list(undef, "create.cgi?create=zfs&parent=");
	print "<a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
} elsif (($in{'create'} =~ "zfs")) {
	#ui_print_header(undef, "Create File System", "", undef, 1, 1);
	#print "Pool:";
	#ui_zpool_status($in{'pool'});
	#Show associated file systems
	
	print "Parent file system:";
	ui_zfs_list("-r ".$in{'parent'}, "");
	
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
	print ui_table_span("<b>Name: </b>".$in{'parent'}."/".ui_textbox('zfs'));
	print ui_table_span('Mount point (blank for default)'.ui_filebox('mountpoint', '', 25, undef, undef, 1));
	print ui_hidden('parent', $in{'parent'});
	print ui_hidden('create', 'zfs');
	print ui_table_span("<br />");
	print ui_table_span('File system options: ');
	foreach $key (sort(keys %createopts))
	{
		my @select = [ split(", ", $proplist{$key}) ];
		if ($proplist{$key} eq 'boolean') { @select = [ 'default', 'on', 'off' ]; }
		print ui_table_row($key.': ', ui_select($key, 'default', @select, 1, 0, 1));
	}
	print ui_table_end();
	print ui_submit('Create');
	print " | ";
	print "<a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
	#print popup_window_button( 'cmd.cgi', '600', '400', '1', [ [ 'pool', 'pool', 'pool'], ['create', 'create', 'create'], ['zfs', 'zfs', 'zfs'] ] );
	#ui_print_footer("index.cgi?mode=zfs", $text{'zfs_return'});
} elsif ($in{'import'}) {
	print ui_form_start("create.cgi", "post");
	print ui_table_start("Import Zpool");
	print ui_hidden('import', '1');
	print "Import search directory (blank for default):", ui_filebox('dir', $in{'dir'}, 25, undef, undef, 1);
	print "<br />";
	print ui_submit('Search');
	print ui_form_end();
	#print " | ";
	#print ui_table_row();
	%imports = zpool_imports($in{'dir'});
	#print Dumper (\%imports);
	print "<br />";
	my @array = split("\n", `zpool import -d $in{'dir'}`);
	#print Dumper (@array);
	#print ui_table_row('');
	#print ui_table_start();
	foreach $key (sort(keys %imports))
	{
		print ui_columns_start([ "Pool", "ID", "State" ]);
		print ui_columns_row(["<a href='cmd.cgi?import=$key&dir=$in{'dir'}'>".$key."</a>", "<a href='cmd.cgi?import=$imports{$key}{'id'}&dir=$in{'dir'}'>".$imports{$key}{'id'}."</a>", $imports{$key}{'state'}]);
		#print ui_table_row("<a href='cmd.cgi?import=$key&dir=$in{'dir'}'>".$key."</a>", $imports{$key}{'id'}." ".$imports{$key}{'state'}, 3);
		#print ui_columns_end();
		print ui_table_start();
		#print ui_table_span("Devices: ");
		if ($imports{$key}{vdevs}) { foreach $dev (sort(keys $imports{$key}{vdevs}))
		{
			#print ui_columns_start([ "Dev", "State" ]);
			#print ui_columns_row([$dev, $imports{$key}{'vdevs'}{$dev}{'state'}]);
			print ui_table_row($dev, "State: ".$imports{$key}{'vdevs'}{$dev}{'state'});
		} }
		print ui_table_end();
		print ui_columns_end();
	}
	
	print ui_table_end();
	
	print "<a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
} elsif ($in{'clone'}) {
	#ui_zfs_list("-r ".$in{'parent'}, "");
	my ($parent) = split('/', $in{'clone'});
	($parent) = split('@', $parent);
	print ui_form_start("cmd.cgi", "get");
	print ui_table_start('Clone Snapshot', 'width=100%', '6');
	print ui_table_span('<b>Snapshot:</b> '.$in{'clone'});
	print ui_table_span("<b>Name: </b>".$parent."/".ui_textbox('zfs'));
	print ui_table_span('<b>Mount point</b> (blank for default)'.ui_filebox('mountpoint', '', 25, undef, undef, 1));
	print ui_hidden('clone', $in{'clone'});
	print ui_hidden('parent', $parent);
	print ui_table_span("<br />");
	print ui_table_span('File system options: ');
	foreach $key (sort(keys %createopts))
	{
		my @select = [ split(", ", $proplist{$key}) ];
		if ($proplist{$key} eq 'boolean') { @select = [ 'default', 'on', 'off' ]; }
		print ui_table_row($key.': ', ui_select($key, 'default', @select, 1, 0, 1));
	}
	print ui_table_end();
	print ui_submit('Create');
	print " | ";
	print "<a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
} elsif ($in{'send'}) {
	print ui_form_start("cmd.cgi", "get");
	print ui_table_start('Send Snapshot', 'width=100%', '6');
	print ui_table_span('<b>Snapshot:</b> '.$in{'send'});
	print ui_table_span(ui_oneradio('type', 'new', '<b>New local filesystem</b> ', 1));
	%hash = list_zfs();
	@zfs = keys(%hash);
	print ui_table_span("<b>Name: </b>".ui_select('parent', undef, [@zfs])."/".ui_textbox('zfs'));
	print ui_table_span(ui_checkbox('replicate', '1', 'Replicate entire file system?', 0));
	print ui_hidden('send', $in{'send'});
	print ui_table_span("<br />");
	print ui_table_span(ui_oneradio('type', 'exist', '<b>Existing local filesystem</b> ', 0));
	print ui_table_span("<b>Name: </b>".ui_select('existzfs', undef, [@zfs]));
	print ui_table_row(undef, ui_checkbox('increment', '1', 'Incremental?', 0));
	print ui_table_row(undef, ui_checkbox('force', '1', 'Force overwrite?', 0));
	print ui_table_span("<br />");
	print ui_table_span(ui_oneradio('type', 'ssh', '<b>Remote filesystem by SSH</b> ', 0, undef, 1));
	print ui_table_span("<i>Not yet implemented</i>");
	print ui_table_span("<br />");
	print ui_table_end();
	print ui_submit('Send');
	print " | ";
	print "<a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
}

