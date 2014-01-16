#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;

ui_print_header(undef, "Create Zpool", "", undef, 1, 1);
$conf = get_zfsmanager_config();

print ui_form_start("create.cgi", "post");
print ui_table_start("Create Zpool");


#mount::generate_location("vdev", "");
#print ui_table_row();
#mount::generate_location("vdev", "");
print ui_table_end();
print &ui_form_end([ [ undef, "create" ] ]);

print Dumper(\%in)