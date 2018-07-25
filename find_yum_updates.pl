#!/usr/bin/perl

use warnings;
use strict;

my @updates = `yum updateinfo list security`;

# Trim the fat from yum output.
for my $index ( 0 .. $#updates) {
  $updates[$index] =~ s/^\s+//;
  if ($updates[$index] =~  /^\*|^Load|^updateinfo/) {
    undef $updates[$index];
   } else {
    next;
 }
}

@updates = grep{ defined }@updates;

if ($#updates >= 0) {
  print "SECURITY UPDATES AVAILABLE:\n";
  foreach (@updates) {
      print $_ ;
    }
  exit 1
} else {
   print "No security updates found.\n";
   exit 0
}
