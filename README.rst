Repetitive Element Parser

Importance of Repetitive Elements:

Repetitive elements make up ~50% of the mammalian genome. Previously, much of this genomic content was
labeled as 'junk' DNA, and geneticists and biologists ignored its importance. It is now clear that
repetitive elements are dynamic and important elements throughout the mammalian genome, and
understanding their expression patterns and localization throughout the genome may provide key
insights into mammalian genetics and biology that have been unappreciated.

To this end, this package - Repetitive Element Parser - functions to analyze RNA-seq expression
patterns as output by a piece of software outlining differential expression between two groups.
The package then extracts repetitive element data from these expression profiles, and
creates meaningful plots which a scientist can then use to investigate more detailed expression
patterns related to their area of interest.

The core functionality of the Repetitive Element Parser is to take a differential expression dataset,
and return a variety of plotting options for visualization of key groups of repetitive element.
The code is written in python3 and is very intuitive, allowing users to customize their catching of
groups and plot functionalities. Currently, only an MA-plot functionality is available, but this will be
added to and improved in subsequent releases.

This parser is fully functional from the command line and takes a variety of optional arguments that
specify its functionality. Check the '-h' option from the command line for more details.
