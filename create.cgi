#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
ui_print_header(undef, "Create Zpool", "", undef, 1, 1);

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
	print 'vdev configuration: ', ui_textbox('dev', '');


	#print ui_select('vdev0', 'pool', ['pool', 'mirror', 'raidz1', 'raidz2', 'raidz3', 'log', 'cache'], undef, undef, undef, undef, '');
	#print 'vdev configuration: ', ui_textbox('vdev', '');
	#print ui_popup_link('Add vdev', 'select.cgi'), "<br />";
	print ui_checkbox('force', '-f', 'Force', 0), "<br />";
	#print ui_submit('Create');
	print popup_window_button( 'cmd.cgi', '600', '400', '1', [ [ 'pool', 'pool', 'pool'], ['create', 'create', 'create'], ['dev', 'dev', 'dev'], ['mountpoint', 'mountpoint', 'mountpoint'], ['force', 'force', 'force'] ] );
	#mount::generate_location("vdev", "");
	#print ui_table_row();
	#mount::generate_location("vdev", "");
	#print ui_table_end();
	#print &ui_form_end([ [ undef, "create" ] ]);
	#print Dumper(\%in)

#create zfs file system
} elsif (($in{'create'} =~ "zfs") & ($in{'pool'} eq undef)) {
	#ui_print_header(undef, "Create File System", "", undef, 1, 1);
	print "Select pool for file system";
	ui_zpool_status(undef, "create.cgi?create=zfs&pool=");
	ui_print_footer("index.cgi?mode=zfs", $text{'zfs_return'});
} elsif (($in{'create'} =~ "zfs")) {
	#ui_print_header(undef, "Create File System", "", undef, 1, 1);
	print "Pool:";
	ui_zpool_status($in{'pool'});
	#Show associated file systems
	%zfs = list_zfs("-r ".$in{'pool'});
	print "Filesystems:";
	print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
	foreach $key (sort(keys %zfs)) 
	{
		print ui_columns_row(["<a href='status.cgi?zfs=$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
	}
	print ui_columns_end();
	print ui_form_start("cmd.cgi", "post");
	#print ui_hidden('property', $in{'property'});
	print $in{'pool'}, "/", ui_textbox('zfs');
	print ui_hidden('pool', $in{'pool'});
	print ui_hidden('create', 'zfs');
	#print ui_submit('Create');
	print popup_window_button( 'cmd.cgi', '600', '400', '1', [ [ 'pool', 'pool', 'pool'], ['create', 'create', 'create'], ['zfs', 'zfs', 'zfs'] ] );
	ui_print_footer("index.cgi?mode=zfs", $text{'zfs_return'});
}

