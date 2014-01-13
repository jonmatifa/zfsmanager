#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
ui_print_header(undef, $text{'status_title'}, "", undef, 1, 1);

print zpool_status($in{'pool'});
$conf = get_zfsmanager_config();

ui_print_footer('', $text{'index_return'});