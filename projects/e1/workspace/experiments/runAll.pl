#!/usr/bin/perl

use strict;

my $exe = "$ENV{HOME}/sf.net/CellMLSimulator/build/release/CellMLSimulator";
my $output = "generated";

mkdir $output;

my @experiments = ("IK-gating-kinetics","INa-gating-kinetics",
                   "periodic-stimulus","voltage-clamp");

foreach my $exp (@experiments) {
  my $o = $output . "/" . $exp;
  my $g = $exp . "-graphs.xml";
  mkdir $o;
  system("$exe --graph-directory=$o --reference-description --data=$o/data.h5 $g");
}
