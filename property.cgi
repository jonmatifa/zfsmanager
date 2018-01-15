#!/usr/bin/perl

require './zfsmanager-lib.pl';
require './property-list-en.pl';
ReadParse();
use Data::Dumper;
ui_print_header(undef, $text{'property_title'}, "", undef, 1, 1);
%props =  property_desc();
%pool_proplist = pool_properties_list();
%proplist = properties_list();

print ui_table_start("$text{'property_title'}: $in{'property'}", "width=100%", "10", ['align=left'] );
if ($in{'zfs'}) { 
	%get = zfs_get($in{'zfs'}, $in{'property'}); 
	print "File system:  <b>".$in{'zfs'}."</b><br /> ";
	print "Property: <b>", $in{'property'}, "</b> is currently: <b>", $get{$in{'zfs'}}{$in{'property'}}{value}, "</b><br />";
	print "Source: <b>", $get{$in{'zfs'}}{$in{'property'}}{source}."</b>";
	print "<br />";
	print "<br />";
} elsif ($in{'pool'}) { 
	%get = zpool_get($in{'pool'},  $in{'property'}); 
	print "Pool:  <b>".$in{'pool'}."</b><br /> ";
	print "Property: <b>", $in{'property'}, "</b> is currently: <b>", $get{$in{'pool'}}{$in{'property'}}{value}, "</b><br />";
	print "Source: <b>", $get{$in{'pool'}}{$in{'property'}}{source}."</b><br />";
	print "<br />";	
}

if ($props{$in{'property'}})
{
	print "<b>Description:</b><br />";
	print $props{$in{'property'}};
	print "<br />";
	print "<br />";
}

if ($text{'prop_'.$in{'property'}})
{
        print "<b>Description:</b><br />";
        print $text{'prop_'.$in{'property'}};
        print "<br />";
        print "<br />";
}
print ui_table_end();

if (can_edit($in{'zfs'}, $in{'property'}) =~ 1) {
print ui_form_start('cmd.cgi', 'post');
print ui_hidden('property', $in{'property'});
print ui_hidden('zfs', $in{'zfs'});
print ui_hidden('pool', $in{'pool'});
if ($in{'property'} =~ 'mountpoint') {
	print ui_hidden('cmd', 'setzfs');
	print ui_filebox('set', $get{$in{'zfs'}}{$in{'property'}}{value}, 0, undef, undef, 1);
	print ui_submit('submit'), "<br />";
} elsif ($in{'property'} =~ 'mounted') {
	if ($get{$in{'zfs'}}{$in{'property'}}{value} =~ 'yes') {
		#fix this to a post command
		print ui_hidden('cmd', "unmount");
		print "<a href='cmd.cgi?zfs=$in{'zfs'}&cmd=zfsact&action=unmount'>Unmount this file system</a>";
	} else {
		print ui_hidden('cmd', "mount");
		print "<a href='cmd.cgi?zfs=$in{'zfs'}&cmd=zfsact&action=mount'>Mount this file system</a>";
	}
} elsif ($in{'property'} =~ 'comment') {
	print ui_hidden('cmd', 'setpool') ;
	print "Comment (limited to 32 characters): ".ui_textbox('set', $get{$in{'pool'}}{$in{'property'}}{value}, 32)."<br />";
	print ui_submit('submit', "<br />");

} elsif ($in{'property'} =~ 'sharesmb') {

} elsif ($in{'property'} =~ 'sharenfs') {

} elsif ($in{'property'} =~ 'utf8only') {

} elsif ($proplist{$in{'property'}} =~ 'text') {

	print "", ($in{'zfs'}) ? ui_hidden('cmd', 'setzfs') : "";
	print "Set ".$in{'property'}.": ".ui_textbox('set', $get{$in{'zfs'}}{$in{'property'}}{value});
	print ui_submit('submit'), "<br />";

} elsif ($proplist{$in{'property'}} =~ 'special' || $pool_proplist{$in{'property'}} =~ 'special') {

} elsif ($in{'property'} =~ /feature@/) {
	print ui_hidden('cmd', 'setpool');
	if ($get{$in{'pool'}}{$in{'property'}}{value} =~ 'disabled') {
	my @select = ['enabled', 'disabled']; 
	print "Change to: ", ui_select('set', $get{$in{'pool'}}{$in{'property'}}{value}, @select, 1, 0, 1); 
	print "<br />";
	print ui_submit('submit');
	print "<br />";
}
} else {

if ($in{'zfs'}) {
	print ui_hidden('cmd', 'setzfs');
	my @select = [ split(", ", $proplist{$in{'property'}}), 'inherit' ];
	if ($proplist{$in{'property'}} eq 'boolean') { @select = [ 'on', 'off', 'inherit' ]; }
	print "Change to: ";
	#The following line was specifically added when com.sun:auto-snapshot does not have a value
	if ($get{$in{'zfs'}}{$in{'property'}}{value} eq "-") { $get{$in{'zfs'}}{$in{'property'}}{value} = 'inherit'; }
	print ui_select('set', $get{$in{'zfs'}}{$in{'property'}}{value}, @select, 1, 0, 1); 
}
elsif ($in{'pool'}) { 
	print ui_hidden('cmd', 'setpool') ;
	my @select = [ split(", ", $pool_proplist{$in{'property'}}) ];
	if ($pool_proplist{$in{'property'}} eq 'boolean') { @select = [ 'on', 'off' ]; }
	print ui_select('set', $get{$in{'pool'}}{$in{'property'}}{value}, @select, 1, 0, 1); 
}
print ui_submit('submit');
print "<br />";
print "<br />";
}
print ui_form_end();
}

if ($in{'zfs'} && (index($in{'zfs'}, '@') != -1)) { ui_print_footer("status.cgi?snap=$in{'zfs'}", $in{'zfs'}); }
if ($in{'zfs'} && (index($in{'zfs'}, '@') =~ -1)) { ui_print_footer("status.cgi?zfs=$in{'zfs'}", $in{'zfs'}); }
if ($in{'pool'}) { ui_print_footer("status.cgi?pool=$in{'pool'}", $in{'pool'}); }
