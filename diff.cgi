#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
ui_print_header(undef, $text{'diff_title'}, "", undef, 1, 1);

print "Snapshot: ".$in{'snap'};
@array = diff($in{'snap'}, undef);
%type = ('B' => 'Block device', 'C' => 'Character device', '/' => 'Directory', '>' => 'Door', 'F' => 'Regular file');
%action = ('-' => 'removed', '+' => 'created', 'M' => 'Modified', 'R' => 'Renamed');
print ui_columns_start([ "File", "Action", "Type" ]);
foreach $key (@array)
{
	@file = split("\t", $key);
	print ui_columns_row([ @file[2], $action{@file[0]}, $type{@file[1]} ]);
}
print ui_columns_end();

ui_print_footer("status.cgi?snap=$in{'snap'}", $in{'snap'});
