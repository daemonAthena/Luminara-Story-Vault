The following is the precompiled binaries and sourcecode for the Luminara Calendar in case a user would like to have their own version that tracks to IRL days, months, and years! 

# Compilation

To compile simply run the file with a compiler like gcc, mingwc etc.
`gcc luminara-date.c`
Easy!

# Usage
You will need to use the command line for this so windows users fire up your powershell.

if you simply run the executable as is
`luminara-date.exe`
it prints today's Luminara date into standard output, pretty neat!

if you pass a gregorian calendar date as input
`luminara-date.exe 2026-11-10`
it gives you **that** date on the luminara calendar.

if you pass it a luminara date
`luminara-date.exe Gilding-23 1`
it gives you back that days gregorian date.

if the year is ommitted in either case you will get the next one! For instance Gilding-23 without a date will point to Gilding-23 E7 if it's Gilding-24 E6.

Day of the week is also included in the output.
The tool accounts for leap years, have fun!!

# Fun Fact
The start date for 1E1 is my transition year, 2021
