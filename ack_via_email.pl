#!/usr/bin/perl
# Same thing as parsemail.py, just a little harder to read.
# Parse an email from stdin and acknowledge a Nagios alert.
# Passed in from /var/lib/nagios/.procmailrc

use strict;
my $ack;
my $command;
my $commandfile = '/var/lib/nagios3/rw/nagios.cmd';
my $from;
my $host;
my $now = `/bin/date +%s`;
my $service;
my $subject;

while (<>) {
    $from    = $_ if $_ =~ /^From:/ig ;
    $subject = $_ if $_ =~ /^Subject/ig;
    $ack     = 1  if $_ =~ /ack/ig;
}

exit if not $ack;

my $ph; #placeholder
chomp($from, $now);

if ($subject =~ /Host/) {
    ($ph, $ph, $host, $ph, $ph, $ph, $ph) = split(/ /, $subject);
    ($host) = ($host) =~ /(.*)\!/;
} else {
    ($ph, $ph, $host, $service, $ph, $ph) = split(/\ /, $subject);
}   

if ($subject =~ /Host/ ) {
    $command = "ACKNOWLEDGE_HOST_PROBLEM;$host;1;1;1;email;$from;ack'd by email";
} else {
    $command = "ACKNOWLEDGE_SVC_PROBLEM;$host;$service;1;1;1;$from;ack'd by email";
}

send_command("$command");

sub send_command {
    my $in=shift;
    open(F, ">$commandfile") or die "can't open $commandfile";
    print F "[$now] $in\n";
    close F;
}
