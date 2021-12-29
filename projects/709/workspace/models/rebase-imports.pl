#!/usr/bin/perl

use strict;
use File::Find;
use File::Spec;

@ARGV = ('.') unless @ARGV;

sub processFile {
  if (/\.xml$/) {
    my $file = $_;
    my $out = $file . ".tmp";
    open IN,"<$file" or die "Error opening input file ($file): $!\n";
    open OUT,">$out" or die "Error opening output file ($out): $!\n";
    while (<IN>) {
      if (/\"http:\/\/www.physiome.org.nz\/publications\/PBMB-2005-89\/Nickerson\/models\/(\S+)\"/) {
	my $f = "/home/andre/pmr2/a1/models/" . $1;
	my $r = File::Spec->abs2rel($f);
	s/\"http:\/\/www.physiome.org.nz\/.*\"/\"$r\"/;
      }
      print OUT $_;
    }
    close OUT;
    close IN;
    system("mv $out $file");
  }
}

find(\&processFile,@ARGV);

exit;





