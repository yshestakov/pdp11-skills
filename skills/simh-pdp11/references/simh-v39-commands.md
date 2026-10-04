# SIMH v3.9 simulator control commands (generic, all simulators)

Source: "SIMH Users' Guide" V3.9 (simh_doc, R. Supnik, 2012), converted from doc/simh_doc.doc
of the v3.9-0 release (same text as bitsavers simh_doc.pdf). Tab-aligned tables kept as-is.

NOT in v3.9 (SIMH v4 / open-simh only - don't use): EXPECT, SEND, GOTO, IF, CALL/RETURN,
SET ENVIRONMENT and %ENV% substitution, SHIFT, NOEXPECT, RUNLIMIT, ON <condition>, SHOW ON,
SCREENSHOT, SET CONSOLE SPEED, LOAD with address options. Use scripts/simh_run.py for
expect/send-style automation instead.

Contents: 2 Conventions; 3 Commands (3.1 LOAD/DUMP, 3.2 SAVE/RESTORE, 3.3 RESET, 3.4 ATTACH/DETACH,
3.5 EXAMINE/DEPOSIT, 3.6 EVAL, 3.7 RUN/GO/CONT/STEP/BOOT + THROTTLE, 3.8 stops and BREAK,
3.9 SET, 3.10 SHOW, 3.11 ENABLE/DISABLE/ASSIGN, 3.12 SET CONSOLE (TELNET, LOG, WRU, DEL),
3.13 DO files with %1..%9, ECHO, ASSERT, 3.14 ! shell escape, 3.15 HELP, 3.16 debug output,
3.17 EXIT); Appendix 1 host file formats (disk, floppy, tape, printer, DECtape).

---

## 2 Simulator Conventions

A simulator consists of a series of devices, the first of which is always the CPU.  A device consists of named registers and one or more numbered units.  Registers correspond to device state, units to device address spaces.  Thus, the CPU device might have registers like PC, ION, etc, and a unit corresponding to main memory; a disk device might have registers like BUSY, DONE, etc, and units corresponding to individual disk drives.  Except for main memory, device address spaces are simulated as unstructured binary disk files in the host file system.  The SHOW CONFIG command displays the simulator configuration.

A simulator keeps time in terms of arbitrary units, usually one time unit per instruction executed.  Simulated events (such as completion of I/O) are scheduled at some number of time units in the future.  The simulator executes synchronously, invoking event processors when simulated events are scheduled to occur.  Even asynchronous events, like keyboard input, are handled by polling at synchronous intervals.  The SHOW QUEUE command displays the simulator event queue.

## 3 Commands

Simulator commands consist of a command verb, optional switches, and optional arguments.  Switches take the form:

	-<letter>{<letter>...}

Multiple switches may be specified separately or together: -abcd and -a -b -c -d are treated identically.  Verbs, switches, and other input (except for file names) are case insensitive.

Any command beginning with semicolon (;) is considered a comment and ignored.
### 3.1 Loading and Saving Programs

The LOAD command (abbreviation LO) loads a file in binary loader format:

	load <filename> {implementation options}

The types of formats supported are implementation specific.  Options (such as load within range) are also implementation specific.

The DUMP command (abbreviation DU) dumps memory in binary loader format:

	dump <filename> {implementation options}

The types of formats supported are implementation specific.  Options (such as dump within range) are also implementation specific.
### 3.2 Saving and Restoring State

The SAVE command (abbreviation SA) save the complete state of the simulator to a file.  This includes the contents of main memory and all registers, and the I/O connections of devices except network devices (such as Ethernet controllers and terminal multiplexers):

	save <filename>

The RESTORE command (abbreviation REST, alternately GET) restores a previously saved simulator state:

	restore <filename>

Note: SAVE file format compresses zeroes to minimize file size.
### 3.3 Resetting Devices

The RESET command (abbreviation RE) resets a device or the entire simulator to a predefined condition.  If switch -p is specified, the device is reset to its power-up state:

	RESET					reset all devices
	RESET -p				powerup all devices
	RESET ALL				reset all devices
	RESET <device>			reset specified device

Typically, RESET stops any in-progress I/O operation, clears any interrupt request, and returns the device to a quiescent state.  It does not clear main memory or affect I/O connections.
### 3.4 Connecting and Disconnecting Devices

Except for main memory and network devices, units are simulated as unstructured binary disk files in the host file system.  Before using a simulated unit, the user must specify the file to be accessed by that unit.  The ATTACH (abbreviation AT) command associates a unit and a file:

	ATTACH <unit> <filename>

If the file does not exist, and the -e switch was not specified, a new file is created, and an appropriate message is printed.  If the -e switch was specified, a new file is not created, and an error message is printed.

If the -r switch is specified, or the file is write protected, ATTACH tries to open the file read only.  If the file does not exist, or the unit does not support read only operation, an error occurs.  Input-only devices, such as paper-tape readers, and devices with write lock switches, such as disks and tapes, support read only operation; other devices do not.  If a file is attached read only, its contents can be examined but not modified. 

For simulated magnetic tapes, the ATTACH command can specify the format of the attached tape image file:

	ATTACH -f <tape_unit> <format> <filename>

The currently supported tape image file formats are:

	SIMH					SIMH simulator format
	E11					E11 simulator format
	TPC					TPC format
	P7B					Pierce simulator 7-track format

The tape format can also be set with the SET command prior to ATTACH:

	SET <tape_unit> FORMAT=<format>
	ATT <tape_unit> <filename>

The format of an attached file can be displayed with the SHOW command:

	SHOW <tape_unit> FORMAT

For Telnet-based terminal emulators, the ATTACH command associates the master unit with a TCP/IP port:

	ATTACH <unit> <port>

The port is a decimal number between 1 and 65535 that is not used by standard TCP/IP protocols.

For Ethernet emulators, the ATTACH command associates the simulated Ethernet with a physical Ethernet device:

	ATTACH <unit> <physical device name>

The DETACH (abbreviation DET) command breaks the association between a unit and a file, port, or network device:

	DETACH ALL				detach all units
	DETACH <unit>			detach specified unit

The EXIT command performs an automatic DETACH ALL.
### 3.5 Examining and Changing State

There are four commands to examine and change state:

    - EXAMINE (abbreviated E) examines state
    - DEPOSIT (abbreviated D) changes state
    - IEXAMINE (interactive examine, abbreviated IE) examines state and allows the user to interactively change it
    - IDEPOSIT (interactive deposit, abbreviated ID) allows the user to interactively change state

All four commands take the form

	command {modifiers} <object list>

Deposit must also include a deposit value at the end of the command.

There are four kinds of modifiers: switches, device/unit name, search specifier, and for EXAMINE, output file.  Switches have been described previously.  A device/unit name identifies the device and unit whose address space is to be examined or modified.  If no device is specified, the CPU (main memory)is selected; if a device but no unit is specified, unit 0 of the device is selected.

The search specifier provides criteria for testing addresses or registers to see if they should be processed.  A specifier consists of a logical operator, a relational operator, or both, optionally separated by spaces.

	{<logical op> <value>} <relational op> <value>

where the logical operator is & (and), | (or), or ^ (exclusive or), and the relational operator is = or == (equal), ! or != (not equal), >= (greater than or equal), > (greater than), <= (less than or equal), or < (less than).  If a logical operator is specified without a relational operator, it is ignored.  If a relational operator is specified without a logical operator, no logical operation is performed.  All comparisons are unsigned.

The output file modifier redirects command output to a file instead of the console.  An output file modifier consists of @ followed by a valid file name.

Modifiers may be specified in any order.  If multiple modifiers of the same type are specified, later modifiers override earlier modifiers.  Note that if the device/unit name comes after the search specifier, the search values will interpreted in the radix of the CPU, rather than of the device/unit.

The "object list" consists of one or more of the following, separated by commas:

	register				the specified register
	register[sub1-sub2]		the specified register array locations,
						starting at location sub1 up to and
						including location sub2
	register[sub1/length]		the specified register array locations,
						starting at location sub1 up to but
						not including sub1+length
	register[ALL]			all locations in the specified register
						array
	register1-register2		all the registers starting at register1
						up to and including register2
	address				the specified location
	address1-address2			all locations starting at address1 up to
						and including address2
	address/length			all location starting at address up to
						but not including address+length
	STATE					all registers in the device
	ALL					all locations in the unit

Switches can be used to control the format of display information:

	-a					display as ASCII
	-c					display as character string
	-m					display as instruction mnemonics
	-o					display as octal
	-d					display as decimal
	-h					display as hexadecimal

The simulators typically accept symbolic input (see documentation with each simulator).

Examples:

	ex 1000-1100			examine 1000 to 1100
	de PC 1040				set PC to 1040
	ie 40-50				interactively examine 40:50
	ie >1000 40-50			interactively examine the subset
				   		of locations 40:50 that are >1000
	ex rx0 50060			examine 50060, RX unit 0
	ex rx sbuf[3-6]			examine SBUF[3] to SBUF[6] in RX
	de all 0				set main memory to 0
	de &77>0 0				set all addresses whose low order
				   		bits are non-zero to 0
	ex -m @memdump.txt 0-7777	dump memory to file

Note: to terminate an interactive command, simply type a bad value (eg, XYZ) when input is requested.
### 3.6 Evaluating Instructions

The EVAL command evaluates a symbolic instruction and returns the equivalent numeric value.  This is useful for obtaining numeric arguments for a search command:

	EVAL <expression>
### 3.7 Running A Simulated Program

The RUN command (abbreviated RU) resets all devices, deposits its argument (if given) in the PC, and starts execution.  If no argument is given, execution starts at the current PC.

The GO command does not reset devices, deposits its argument (if given) in the PC, and starts execution.  If no argument is given, execution starts at the current PC.

The CONT command (abbreviated CO) does not reset devices and resumes execution at the current PC.

The STEP command (abbreviated S) resumes execution at the current PC for the number of instructions given by its argument.  If no argument is supplied, one instruction is executed.

The BOOT command (abbreviated BO) resets all devices and bootstraps the device and unit given by its argument.  If no unit is supplied, unit 0 is bootstrapped.  The specified unit must be attached.
#### 3.7.1 Controlling The Simulation Rate

By default, the simulator runs as fast as possible (although at lower than normal priority) and will consume all available processing resources on the host system.  This will raise power consumption (and the operating temperature) of many PC's, and drain the battery of a laptop.

The SET THROTTLE command allows the user to reduce the effective execution rate to a specified number of instructions per second, or to a specified percentage of total host computing time:

	SET THROTTLE xM				set execution rate to x mips
	SET THROTTLE xK				set execution rate to x kips
	SET THROTTLE x%				limit simulator to x% of host time

Throttling is only available on host systems that implement a precision real-time delay function.

The SET NOTHROTTLE command turns off throttling.  The SHOW THROTTLE command shows the current settings for throttling.

Some simulators implement a different form of resource management called idling.  Idling suspends simulated execution whenever the program running on the simulator is doing nothing, and runs the simulator at full speed when there is work to do.  Throttling and idling are mutually exclusive.
### 3.8 Stopping The Simulator

Programs run until the simulator detects an error or stop condition, or until the user forces a stop condition.
#### 3.8.1 Simulator Detected Stop Conditions

These simulator-detected conditions stop simulation:

    - HALT instruction.  If a HALT instruction is decoded, simulation stops.

    - Breakpoint.  The simulator may support breakpoints (see below).

    - I/O error.  If an I/O error occurs during simulation of an I/O operation, and the device stop-on-I/O-error flag is set, simulation usually stops.

    - Processor condition.  Certain processor conditions can stop simulation; these are described with the individual simulators.
#### 3.8.2 User Specified Stop Conditions

Typing the interrupt character stops simulation.  The interrupt character is defined by the WRU (where are you) console option and is initially set to 005 (^E).
#### 3.8.3 Breakpoints

A simulator may offer breakpoint capability.  A simulator may define breakpoints of different types, identified by letter (for example, E for execution, R for read, W for write, etc).  At the moment, most simulators support only E (execution) breakpoints.

Associated with a breakpoint are a count and, optionally, one or more actions.  Each time the breakpoint is taken, the associated count is decremented.  If the count is less than or equal to 0, the breakpoint occurs; otherwise, it is deferred.  When the breakpoint occurs, the optional actions are automatically executed.

A breakpoint is set by the BREAK command:

	BREAK {-types} {<addr range>{[count]},{addr range...}}{;action;action...}

If no type is specified, the simulator-specific default breakpoint type (usually E for execution) is used.  If no address range is specified, the current PC is used.  As with EXAMINE and DEPOSIT, an address range may be a single address, a range of addresses low-high, or a relative range of address/length.  Examples:

	BREAK					set E break at current PC
BREAK -e 200			set E break at 200
	BREAK 2000/2[2]			set E breaks at 2000,2001 with count = 2
	BREAK 100;EX AC;D MQ 0		set E break at 100 with actions EX AC and
 D MQ 0
	BREAK 100;				delete action on break at 100

Currently set breakpoints can be displayed with the SHOW BREAK command:

	SHOW {-types} BREAK {ALL|<addr range>{,<addr range>...}}

Locations with breakpoints of the specified type are displayed.

Finally, breakpoints can be cleared by the NOBREAK command.
### 3.9 Setting Device Parameters

The SET command (abbreviated SE) changes the status of one or more device parameters:

	SET <device> <parameter>{=<value},{<parameter>{=<value>},...}

or one or more unit parameters:

	SET <unit> <parameter>{=<value>},{<parameter>{=<value>},...}

Most parameters are simulator and device specific.  Disk drives, for example, can usually be set WRITEENABLED or write LOCKED; if a device supports multiple drive types, the SET command can be used to specify the drive type.

All devices recognize the following parameters:

	OCT					sets the data radix = 8
	DEC					sets the data radix = 10
	HEX					sets the data radix = 16
### 3.10 Displaying Parameters and Status

The SHOW command (abbreviated SH) displays the status of one or more device parameters:

	SHOW {<modifiers} <device> <parameter>{=<value>},
{<parameter>{=<value>},...}

or one or more unit parameters:

	SHOW {<modifiers} <unit> <parameter>{=<value>},
		{<parameter>{=<value>},...}

There are two kinds of modifiers: switches and output file.  Switches have been described previously.  The output file modifier redirects command output to a file instead of the console.  An output file modifier consists of @ followed by a valid file name.

All devices implement parameters RADIX (the display radix), MODIFIERS (list of valid modifiers), and NAMES (logical name).  Other device and unit parameters are implementation-specific.

SHOW is also used to display global simulation state:
 
SHOW CONFIGURATION 		shows the simulator configuration and
the status of all devices and units
SHOW DEVICES			shows the simulator configuration
SHOW MODIFIERS			shows all available modifiers
SHOW NAMES				show all logical names
SHOW QUEUE	shows the simulator event queue
SHOW TIME				shows the elapsed time since the last RUN
SHOW VERSION			show the simulator version and options
SHOW <device>			shows the status of the named device
SHOW <unit> 			shows the status of the named unit

SHOW QUEUE and SHOW TIME display time in simulator-specific units; typically, one time unit represents one instruction execution.
### 3.11 Altering The Simulated Configuration

In most simulators, the SET <device> DISABLED command removes the specified device from the configuration.  A DISABLED device is invisible to running programs.  The device can still be RESET, but it cannot be ATTAChed, DETACHed, or BOOTed.  SET <device> ENABLED restores a disabled device to a configuration.

Most multi-unit devices allow units to be enabled or disabled:

	SET <unit> ENABLED
	SET <unit> DISABLED

When a unit is disabled, it will not be displayed by SHOW DEVICE.

The standard device names can be supplemented with logical names.  Logical names must be unique within a simulator (that is, they cannot be the same as an existing device name).  To assign a logical name to a device:

	ASSIGN <device> <log-name>	assign log-name to device

To remove a logical name:

	DEASSIGN <device>			remove logical name

To show the current logical name assignment:

	SHOW <device> NAMES		show logical name, if any

To show all logical names:

	SHOW NAMES
### 3.12 Console Options

Console options are controlled by the SET CONSOLE command.

The console terminal normally runs in the controlling window.  Optionally, the console terminal can be connected to a Telnet port.  This allows systems to emulate a VT100 using the built-in terminal emulation of the Telnet client.

	SET CONSOLE TELNET=<port>	connect console terminal to Telnet session
on port
	SET CONSOLE NOTELNET		disable console Telnet

Output to the console can be logged simultaneously to a file:

	SET CONSOLE LOG=<filename>	log console output to file
	SET CONSOLE NOLOG			disable logging

The console provides a limited key remapping capability:

	SET CONSOLE WRU=<value>		interpret ASCII code value as WRU
	SET CONSOLE BRK=<value>		interpret ASCII code value as BREAK
(0 disables)
	SET CONSOLE DEL=<value>		interpret ASCII code value as DELETE
	SET CONSOLE PCHAR=<value>	bit mask of printable characters in range
[31,0]

Values are hexadecimal on hex CPU's, octal on all others.

The SHOW CONSOLE command displays the current state of console options:

	SHOW CONSOLE			show all console options
	SHOW CONSOLE TELNET		show console Telnet state
	SHOW CONSOLE LOG			show console logging state
	SHOW CONSOLE WRU			show value assigned to WRU
	SHOW CONSOLE BRK			show value assigned to BREAK
	SHOW CONSOLE DEL			show value assigned to DELETE
	SHOW CONSOLE PCHAR		show value assigned to PCHAR

Both SET CONSOLE and SHOW CONSOLE accept multiple parameters, separated by commas, e.g.,

	SET CONSOLE WRU=5,DEL=177	set code values for WRU and DEL
### 3.13 Executing Command Files

The simulator can execute command files with the DO command:

	DO <filename> {arguments...}	execute commands in file

The DO command allows command files to contain substitutable arguments.  The string %n, where n is between 1 and 9, is replaced with argument n from the DO command line. The string %0 is replaced with <filename>.  The sequences \% and \\ are replaced with the literal characters % and \, respectively.  Arguments with spaces can be enclosed in matching single or double quotation marks.

If the switch -v is specified, the commands in the file are echoed before they are executed.

If the switch -e is specified, command processing (including nested command invocations) will be aborted if a command error is encountered.  (Simulation stop never abort processing; use ASSERT to catch unexpected stops.)  Without the switch, all errors except ASSERT failures will be ignored, and command processing will continue.

DO commands may be nested up to ten invocations deep.

Several commands are particularly useful within command files.  While they may be executed interactively, they have only limited functionality when so used.
#### 3.13.1 Displaying Arbitrary Text
 
The ECHO command is a useful way of annotating command files.  ECHO prints out its argument on the console:
 
	ECHO <string>			output string to console
 
If there is no argument, ECHO prints a blank line on the console.  This may be used to provide spacing in the console display or log.
#### 3.13.2 Testing Simulator State

The ASSERT command tests a simulator state condition and halts command file execution if the condition is false:

	ASSERT {<dev>} <reg>{<logical-op><value>}<conditional-op><value>

If <dev> is not specified, CPU is assumed.  <reg> is a register (scalar or subscripted) belonging to the indicated device.  The <conditional-op> and optional <logical-op> are the same as those used for "search specifiers" by the EXAMINE and DEPOSIT commands (see above).  The <value>s are expressed in the radix specified for <reg>, not in the radix for the device.

If the <logical-op> and <value> are specified, the target register value is first altered as indicated.  The result is then compared to the <value> via the <conditional-op>.  If the result is false, an "Assertion failed" message is printed, and any running command file is aborted.  Otherwise, the command has no effect.

For example, a command file might be used to bootstrap an operating system that halts after the initial load from disk.  The ASSERT command is then used to confirm that the load completed successfully by examining the CPU's "A" register for the expected value:

	; OS bootstrap command file
	;
	ATTACH DS0 os.disk
	BOOT DS
	; A register contains error code; 0 = good boot
	ASSERT A=0
	ATTACH MT0 sys.tape
	ATTACH MT1 user.tape
	RUN

In the example, if the A register is not 0, the "ASSERT A=0" command will be echoed, the command file will be aborted with an "Assertion failed" message.  Otherwise, the command file will continue to bring up the operating system.
### 3.14 Executing System Commands

The simulator can execute operating system commands with the ! (spawn) command:

	! <host operating system command>

If no operating system command is provided, the simulator attempts to launch the host operating system's command shell.
### 3.15 Getting Help

The HELP command prints out information about a command or about all commands:

	HELP					print all HELP messages
	HELP <command>			print HELP for command
### 3.16 Controlling Debugging

Some simulated devices may provide debug printouts to help in diagnosing complicated problems.  Debug output may be sent to a variety of places, or disabled entirely:

	SET CONSOLE DEBUG=STDOUT	direct debug output to stdout
	SET CONSOLE DEBUG=STDERR	direct debug output to stderr
	SET CONSOLE DEBUG=LOG	  	direct debug output to log file
	SET CONSOLE DEBUG=<filename>	direct debug output to file
	SET CONSOLE NODEBUG	  	disable debug output

If debug output is enabled, individual devices can be controlled with the SET command.  If a device has only a single debug flag:

	SET <device> DEBUG		enable device debug output
	SET <device> NODEBUG	  	disable device debug output

If the device has individual, named debug flags:

	SET <device> DEBUG		enable all debug flags
	SET <device> DEBUG=n1;n2;...	enable debug flags n1, n2, ...
	SET <device> NODEBUG=n1;n2;... disable debug flags n1, n2, ...
	SET <device> NODEBUG		disable all debug flags

If debug output is directed to stdout, it will be intermixed with normal simulator output.
### 3.17 Exiting The Simulator

EXIT (synonyms QUIT and BYE) returns control to the operating system.

## Appendix 1: File Representations

All file representations are little-endian.  On big-endian hosts, the simulator automatically performs any required byte swapping.
## A.1 Hard Disks

Hard disks are represented as unstructured binary files of 16b data items for the 12b and 16b simulators, of 32b data items for the 18b, 24b, and 32b simulators, and 64b for the 36b simulators.
## A.2 Floppy Disks

Floppy disks are represented as unstructured binary files of 8b data items.  They are nearly identical to the floppy disk images for Doug Jones' PDP-8 simulator but lack the initial 256 byte header.  A utility for converting between the two formats is easily written.
## A.3 Magnetic Tapes

Magnetic tapes are represented as unstructured binary files of 8b data items.  Each record starts with a 32b record header, in little endian format.  If the record header is not a special header, it is followed by n 8b bytes of data, followed by a repeat of the 32b record header.  A 1 in the high order bit of the record header indicates an error in the record. If the byte count is odd, the record is padded to even length; the pad byte is undefined.

Special record headers occur only once and have no data.  The currently defined special headers are:

	0x00000000		file mark
	0xFFFFFFFF		end of medium
	0xFFFFFFFE		erase gap

Magnetic tapes are endian independent and consistent across simulator families.  A magnetic tape produced by the Nova simulator will appear to have its 16b words byte swapped if read by the PDP-11 simulator.

SIMH can read and write E11-format magnetic tape images.  E11 format differs from SIMH format only for odd-length records; the data portion of E11 records is not padded with an extra byte.

SIMH can read TPC-format magnetic tape images.  TPC format uses a 16b record header, with 0x0000 denoting file mark.  The record header is not repeated at the end of the record.  Odd-length records are padded with an extra byte.

SIMH can read Pierce-format seven-track magnetic tape images.  Pierce format uses only 6 data bits, and one parity bit, in each byte.  The high order bit indicates start of record.  End of file is indicated by a record of one (occasionally two) bytes consisting of code 017 (octal).
## A.4 Line Printers

Line printer output is represented by an ASCII file of lines separated by the newline character.  Overprinting is represented by a line ending in return rather than newline.
## A.5 DECtapes

DECtapes are structured as fixed length blocks.  PDP-1/4/7/9/15 DECtapes use 578 blocks of 256 32b words.  Each 32b word contains 18b (6 lines) of data.  PDP-11 DECtapes use 578 blocks of 256 16b words.  Each 16b word contains 6 lines of data, with 2b omitted.  This is compatible with native PDP-11 DECtape dump facilities, and with John Wilson's PUTR Program.  PDP-8 DECtapes use 1474 blocks of 129 16b words.  Each 16b word contains 12b (4 lines) of data.  PDP-8 OS/8 does not use the 129th word of each block, and OS/8 DECtape dumps contain only 128 words per block.  A utility, DTOS8CVT.C, is provided to convert OS/8 DECtape dumps to simulator format.

A known issue in DECtape format is that when a block is recorded in one direction and read in the other, the bits in a word are scrambled (to the complement obverse).  The PDP-11 deals with this problem by performing an automatic complement obverse on reverse writes and reads.  The other systems leave this problem to software.

The simulator represents this difference as follows.  On the PDP-11, all data is represented in normal form.  Data reads and writes are not direction sensitive; read all and write all are direction sensitive.  Real DECtapes that are read forward will generate images with the correct representation of the data.

On the other systems, forward write creates data in normal form, while reverse write creates data in complement obverse form.  Forward read (and read all) performs no transformations, while reverse read (and read all) changes data to the complement obverse.  Real DECtapes that are read forward
will generate data in normal form for blocks written forward, and complement obverse data for blocks written in reverse, corresponding to the simulator format.

