Title: Building a ZX81/TS1000 machine code monitor
Category: Blog
Date: 11-11-2021 23:10:00
Modified: 11-11-2021 23:10:00
Status: Draft

A couple months ago I started collecting 8-bit computers of the late 70s and early 80s. As 
of writing this I've an Atari 600XL, TRS-80 Color Computer 2, TI-99/4a, Apple IIe, and a Timex Sinclair 1000. 
I'm fond of all these machines but in particular I've been spending a lot of time with the latter.

The Timex Sinclair 1000 (TS1000) is the first of these machines I really want to spend some time developing games for. 
Now the TS1000 is limited in its capabilities and to truly the leverage the hardware you really need to write programs 
in machine code.

The included Sinclair BASIC provides a means for entering and running machine code but alas the TS1000 lacks any kind of 
machine code monitor that would allow you to easily manipulate memory.

This means before I go about writing any games I'm going to need to build a tool. I decided to model my machine code monitor 
after the one included with the Apple IIe. Below are the features that are required.

* Display bytes for an address range
* Insert bytes at an address
* Copy an address range

Additionally the Apple IIe monitor has the capability to dissassemble machine code as well as invoke a mini-assembler. If I have enough time 
I might try implementing these but for now they're just nice-to-haves.

Eventually the monitor will itself be written in machine code, but initially I'll write it in BASIC so I have an easier means replace the internals with 
machine code routines.