PyCLU - Python Convert Length Units
Convert between length units
==============================

A simple library that converts lengths in different units. For example:

    6 m to yard = 6.562 yd
    2.5 yd to inch = 90 in

The units supported are: metre (m), yard (yd) and inch (in).
The design of the library should support adding new units easily.

It also supports representing the measures as user-friendly strings (e.g.,
"2.3 m", "6 yd", "0.4 in").

To keep things simple, capturing and handling user input is not required. So
parsing strings like "6 m to yd" isn't needed, unless you consider this to be a
useful development aid.

