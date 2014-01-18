#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
ui_print_header(undef, "Create Zpool", "", undef, 1, 1);

if ($in{'create'} =~ "zpool")
{
	ui_print_header(undef, "Create Zpool", "", undef, 1, 1);
	print ui_form_start("create.cgi", "post");
	print ui_table_start("Create Zpool");
	mount::generate_location("vdev", "");
	print ui_table_row();
	#mount::generate_location("vdev", "");
	#print ui_table_end();
	#print &ui_form_end([ [ undef, "create" ] ]);
	print Dumper(\%in)
} elsif (($in{'create'} =~ "zfs") & ($in{'pool'} eq undef)) {
	ui_print_header(undef, "Create File System", "", undef, 1, 1);
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
	print $in{'pool'}, "/", ui_textbox('create');
	print ui_hidden('pool', $in{'pool'});
	#print ui_submit('Create');
	print popup_window_button( 'cmd.cgi', '600', '400', '1', [ [ 'pool', 'pool', 'pool'], ['create', 'create', 'create'] ] );
	ui_print_footer("index.cgi?mode=zfs", $text{'zfs_return'});
}

