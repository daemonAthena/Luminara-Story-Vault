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
```
Gilding 25, Luminara Year 6 E1
Weekday: Artemsday
```

if you pass a gregorian calendar date as input
`luminara-date.exe 2030-11-10`
it gives you **that** date on the luminara calendar.
```
Gilding 25, Luminara Year 10 E1
Weekday: Artemsday
```

if you pass it a luminara date
`luminara-date.exe Gilding-23 1`
it gives you back that days gregorian date.
```
Gilding-23 (Year 1) -> 2021-11-08 (Monday)
```

if the year is omitted then the current Luminara year is assumed! For instance Gilding-23 without a date will point to Gilding-23 6E1 which means the current year in some cases but not in January months which come at the **end** of the Luminara calendar.
```
gilding-23 (Year 6) -> 2026-11-08 (Sunday)
```

Day of the week is also included in the output.
The tool accounts for leap years, have fun!!

# Fun Fact
The start date for 1E1 is my transition year, 2021
