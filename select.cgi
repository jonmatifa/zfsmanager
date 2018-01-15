#!/usr/bin/perl

#deprecated
require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
popup_header($text{'select_title'});

print ui_form_start("create.cgi", "post");
print ui_table_start("Select VDEV");
mount::generate_location("vdev", "");
print ui_submit('Add to pool');
