# RT-11 System Utilities Manual: Ch.14 RESORC resource utility (SHOW command details: devices, jobs, memory, terminals, configuration)

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 14.1 Calling and Terminating RESORC
- 14.2 Options
- 14.2.1 All Option (/A)
- 14.2.2 Software Configuration Option (/C)
- 14.2.3 Device Handler Status Option ([dd:]/D)
- 14.2.4 Hardware Configuration Option (/H)
- 14.2.5 Loaded Jobs Option (/J)
- 14.2.6 Device Assignments Option (/L)
- 14.2.7 Current Monitor Option (/M)
- 14.2.8 Special Features Option (/O)
- 14.2.9 Show Queue Option (/Q)
- 14.2.10 Disk Subsetting Option (/S)
- 14.2.11 Terminal Status Option (/T)
- 14.2.12 Physical Memory Layout Option (/X)
- 14.2.13 Summary Option (/Z)

---

## Chapter 14 Resource Utility Program (RESORC)

The resource utility program lists system resource information on the terminal. You can use RESORC to display the following data about your system:

\- Monitor version number

\- SET options in effect

\- Hardware configuration

\- Total amount of memory in system

\- Organization of physical memory

\- Currently loaded jobs

\- System generation special features in effect

\- Device assignments

\- Status of currently active terminals (on multiterminal systems)

\- Device handler status

\- Logical disk subsetting information

## 14.1 Calling and Terminating RESORC

To call RESORC from the system device, respond to the keyboard monitor dot (.) by typing:

• R RESORC (RET)

The Command String Interpreter (CSI) prints an asterisk (\*) at the left margin of the terminal and waits for your input. At this point, enter the RESORC option or options required to obtain the information you need. Section 14.2 describes these options, and Table 14-1 summarizes them.

If you enter only a carriage return in response to the asterisk, RESORC prints its name and current version number. To abort RESORC while it is executing, type two CTRL/Cs. Type one CTRL/C to return control to the monitor when RESORC is waiting for input (that is, when an asterisk has printed on the terminal).

## 14.2 Options

By specifying one or more of the options /C, /D, /H, /J, /L, /M, /O, /S, /T, and /X, you choose the information that RESORC lists on the terminal. If you use two or more options, you can enter them in any order, although RESORC lists the information in the order /M, /C, /H, /O, /D, /L, /J, /T, /X, /S.

RESORC offers two additional options that are equivalent to combinations of options. The /Z option has the same effect as a combination of the /M, /C, /H, /J, and /O options. The /A option has the same effect as a combination of all the options except /Q and /Z.

Table 14-1: RESORC Options

| Option | Display |
| --- | --- |
| /A | The result of a combination of all RESORC options (except /Z) |
| /C | The device from which you bootstrapped the system and the monitor SET options in effect |
| [dd:]/D | A list of the device handlers, their status, and their vectors; when [dd:] is included, lists the status of only that device |
| /H | The hardware configuration, including the system's total amount of memory (in bytes) |
| /J | Information about the currently running and loaded jobs |
| /L | Device assignments |
| /M | The monitor type, version number, and update level |
| /O | The system generation special features in effect |
| /Q | Lists the contents of the queue for QUEUE or SPOOL or both |
| /S | Information about logical disk subsetting |
| /T | The status and options in effect for currently active terminals on multiterminal systems |
| /X | The organization of physical memory |
| /Z | The result of a combination of /M, /C, /H, /J, and /O options |

## 14.2.1 All Option (/A)

The /A option has the same effect as a combination of all the other RESORC options (except /Z). When you enter /A, all RESORC information is printed on the terminal in the order shown below.

1. Monitor configuration (that is, the monitor type and version number; the device from which the monitor was bootstrapped; what the SET options are; whether a foreground job is loaded; and the indirect file nesting depth)

2. Hardware configuration

3. System generation special features in effect

4. Device handler status

5. Device assignments

6. Job status

7. Status of currently active terminals

8. Organization of physical memory

9. Subsetting of physical disks into logical disks

See the following sections for details on these topics.

## 14.2.2 Software Configuration Option (/C)

The /C option displays:

1. The device from which you bootstrapped the system

2. Whether a foreground job is loaded (if applicable)

3. The monitor SET options

4. Indirect file nesting depth

5. Global .SCCA flag support (enabled or disabled)

The following example uses the /C option.

```txt
*/C
Booted from DLO:RT11FB

USR is set SWAP
EXIT is set SWAP
KMON is set IND
TT is set QUIET
ERROR is set ERROR
SL is set OFF
EDIT is set EDIT
KMON nesting depth is 3
Global .SCCA flag is disabled
```

## 14.2.3 Device Handler Status Option ([dd:]/D)

RESORC's /D option displays a list of your system's device handlers, along with their status, CSR addresses, and vectors. The /D option lists only those handlers whose special features match those of the currently booted monitor. If a handler is loaded, RESORC prints its load address.

If you specify a device name in front of the /D option (dd:/D), RESORC lists information for only that device. The variable dd represents the 2-letter permanent device name for the device (see Table 3-1 in the RT-11 System User's Guide). If you specify DU as the device, RESORC lists the device's unit, port, and partition settings.

The following sample shows the table that RESORC prints when you use the /D option.

| DEVICE | STATUS | CSR | VECTOR(S) |
| --- | --- | --- | --- |
| DY | 122620 | 177170 | 264 |
| DD | Installed | 176500 | 300 304 |
| DL | Installed | 174400 | 160 |
| DX | Not installed | 177170 | 264 |
| LS | Installed | 176500 | 300 304 |
| LP | Installed | 177514 | 200 |
| MS | Installed | 172522 | 224 300 |
| DU | Installed | 172150 | 154 |
| NL | Installed | 000000 | 000 |
| LD | Installed | 000000 | 000 |
| DM | Installed | 177440 | 210 |
| VM | Installed | 177572 | 000 |
| RK | Resident | 177400 | 220 |
| SL | Not installed | 000000 | 000 |
| MT | Installed | 172520 | 224 |
| MM | Not installed | 172440 | 224 |

In this table, the status column can list one of the following messages:

| Message | Meaning |
| --- | --- |
| Installed | The device handler is in the system tables, but you have not loaded it in main memory (you can load it with the LOAD command). |
| Not installed | The device handler is not in the system tables, but you can add the handler with the INSTALL command (if there is a free slot). |
| -Not installed | The device handler special features do not match those of the monitor; you cannot install the handler. (The minus sign in front of any message means that you cannot install the handler.) |
| Resident | The device handler is permanently in memory; you cannot remove or unload it. |
| nnnnnn | The beginning address of a loaded handler. |

The last column in the /D listing identifies vectors. If the handler has multiple vectors, the /D option prints the additional vectors in this column.

The next example shows handler status information for the device DU.

```txt
* DU:/D
DU0: is set UNIT=0, PART=0, PORT=0
DU1: is set UNIT=1, PART=0, PORT=0
DU2: is set UNIT=4, PART=0, PORT=1
DU3: is set UNIT=5, PART=0, PORT=1
DU4: is set UNIT=6, PART=0, PORT=1
DU5: is set UNIT=17, PART=2, PORT=1
DU6: is set UNIT=22, PART=0, PORT=0
DU7: is set UNIT=23, PART=0, PORT=0
```

## 14.2.4 Hardware Configuration Option (/H)

When you use the /H option, RESORC lists the processor type, the total amount of memory (in bytes) that the system contains, and all the special hardware features in your system configuration. The processor is one of the following:

| LSI 11 | PDP 11/23 |
| --- | --- |
| MICRO/PDP-11 | PDP 11/23 PLUS |
| PC325/PC350 | PDP 11/24 |
| PDT 130/150 | PDP 11/34 |
| PDP 11/04 | PDP 11/35,40 |
| PDP 11/05,10 | PDP 11/44 |
| PDP 11/15,20 | PDP 11/45,50,55 |
| SBC 11/21 | PDP 11/60 |
| SBC 11/21 PLUS | PDP 11/70 |

Any special hardware is chosen from the following list. (The /H option displays the features in the order they occur in the list.)

```txt
FP11 Hardware Floating Point Unit
Commercial Instruction Set (CIS)
Extended Instruction Set (EIS)
Floating Point Instruction Set (FIS)
KT11 Memory Management Unit
Parity Memory
Cache Memory
VT11 or VS60 Graphics Hardware
```

The next item that appears in the /H listing is the clock frequency (50 or 60 cycles), and the last is the KW11–P programmable clock (if your system has one and you are not using it as the system clock).

The following example shows the /H option.

```txt
*/H
PDP 11/23 PLUS Processor
1024KB of memory
FP11 Hardware Floating Point Unit
Extended Instruction Set (EIS)
KT11 Memory Management Unit
Parity Memory
GO Cycle System Clock
```

## 14.2.5 Loaded Jobs Option (/J)

The /J option prints information about the currently loaded jobs. For each job, RESORC displays:

1. The job number and name (if you have not enabled system job support on your monitor, the foreground job name appears as FORE, and its priority level is 1 in FB or XM)

2. The console the job is running on (with a nonmultiterminal monitor, this space is blank)

3. The priority level of the job

4. The job's state (running, suspended, or done but not unloaded)

5. The low and high memory limits of the job

6. The start address of the job's impure area

The following example uses the /J option.

```csv
*/J
Job Name Console Level State Low High Impure
16 MFUNCT 1 7 Suspend 115350 127444 114412
14 EL 0 6 132404 141452 130663
12 QUEUE 0 5 152345 163243 144231
0 RESORC 0 0 Run 000000 113144 133374
```

## 14.2.6 Device Assignments Option (/L)

When you type /L in response to the CSI asterisk, RESORC displays your system's device assignments. The devices RESORC lists are those in the system tables. The listing also includes additional information about particular devices. The informational messages and their meanings follow.

| Message | Meaning |
| --- | --- |
| (RESORC) or = RESORC | The device or unit is assigned to the background job RESORC (for FB and XM monitors only). |
| (F) or = F | The device or unit is assigned to the foreground job (only for FB and XM monitors that do not have system job support). |
| (jobname) or =jobname | The device or unit is assigned to the system or foreground job (only for FB and XM monitors that have system job support), where jobname represents the name of the foreground or system job. |
| (Loaded) | The handler for the device has been loaded into memory with the LOAD command. |
| (Resident) | The handler for the device is included in the resident monitor. |
| =logical-device-name(1), logical-device-name(2)... ,logical-device-name(n) | The device or unit has been assigned the indicated logical device names with the ASSIGN command. |
| xx free slots | The last line tells the number of unassigned (free) devices. |

The following example was created under an FB monitor. It shows the status of all devices known to the system.

```asm
* /L
TT (Resident)
DL (Resident)
DL1 = SY, DK, OBJ, SRC, BIN
DL2 = LST, MAP
MQ (Resident)
RK -
DM
DX (Loaded)
DX0: (F)
DX1: (RESORC)
MT
LP
BA
NL
9 free slots
```

## 14.2.7 Current Monitor Option (/M)

When you use the /M option RESORC prints the type, version number, and update level of the currently running monitor. The designation BL, SJ, FB, or XM identifies the monitor type as base-line, single-job, foreground/background, or extended memory, respectively.

The following example uses the /M option.

\* /M

RT-11FB (S) V05.00

## 14.2.8 Special Features Option (/O)

The special features chosen during system generation are listed on the terminal when you use the /O option. Whatever features are in effect are printed out in the same order as the following list of possible special features.

Device I/O timeout support Permits device handlers to do the equivalent of a mark time without doing a .SYNCH request; DECnet applications require this support.

Error logging support Keeps a statistical record of all I/O operations on devices that are supported by this feature; detects and stores data on any errors that occur during I/O operations.

Multiterminal support Permits you to use as many as 16 terminals.

Memory parity support Causes the system to print an error message when a memory parity error occurs.

SJ timer support Configures the SJ monitor to include mark-time and cancel mark-time programmed requests and to support the .FORK process.

Allows you to run up to six jobs in the foreground in addition to the foreground and background jobs.

Reports whether global .SCCA support was chosen during system generation.

The following example shows the /O option.

```txt
* /0
Device I/O time-out support
Error lossing support
Multi-terminal support
Memory Parity support
```

If there are no special features in effect, RESORC prints NO SYSGEN options enabled.

## 14.2.9 Show Queue Option (/Q)

The /Q option lists the contents of the queue for QUEUE, SPOOL, or both if both are running. If there are no files in a queue, RESORC prints:

```txt
?RESORC-I-No queues active
```

The following example shows files queued for printing with SPOOL running:

```txt
* /Q

Unit 0 status
Device is active
00045 blocks are spooled for output
00954 blocks are free to be spooled
```

## 14.2.10 Disk Subsetting Option (/S)

The /S option displays information about the subsetting of physical disks into logical disks. When you use the /S option, RESORC displays the logical disk unit with the file name to which it is assigned, and the size of the logical disk in decimal blocks.

The following example illustrates the /S option by showing the logical disks into which the physical disks DL0: and DL1: are divided.

```c
* /S
LDO is DLO:DISK,LST[4000,]
LD2 is DL1:DISK,SRC[1200,]*
LD1 is DL1:WORK,DSK[600,]
```

An asterisk (\*) following the file information indicates that, although the logical disk assignment exists, the file does not exist on the volume that is currently mounted in the drive unit. A pound sign (#) indicates that the device handler is not loaded. These symbols are especially useful to determine the status of logical disk assignments after you use the SET LD CLEAN command or the LD /C option.

## 14.2.11 Terminal Status Option (/T)

The /T option displays information about currently running active terminals on multiterminal systems. Therefore, if your system does not include multiterminal support, RESORC prints:

No multi-terminal support

Since multiterminal support is not part of the distributed RT-11 monitors, such support is present on your system only if you have included it during system generation; that is, multiterminal support is a special feature.

If your system does include multiterminal support, and you enter the /T option in response to RESORC's asterisk, RESORC prints a table similar to the following:

<table><tr><td colspan="10">* /T</td></tr><tr><td>Unit</td><td>Owner</td><td>Type</td><td></td><td>WIDTH</td><td>TAB</td><td>CRLF</td><td>FORM</td><td>SCOPE</td><td>SPEED</td></tr><tr><td>0</td><td>RESORC</td><td>S-Console</td><td>DL</td><td>132</td><td>No</td><td>Yes</td><td>No</td><td>No</td><td>N/A</td></tr><tr><td>1</td><td>FORE</td><td>Local</td><td>DZ</td><td>80</td><td>Yes</td><td>No</td><td>No</td><td>Yes</td><td>4800</td></tr></table>

Note that in this table, the unit number refers to the terminal; RT-11 multi-terminal support permits you to use as many as 16 terminals.

The Unit column lists the terminal unit number, and the Owner column lists the name of the job (foreground, system, background, or none) to which the terminal is assigned. If the running monitor does not have system job support, RESORC prints FORE and RESORC, where applicable.

The Type column of this table shows the type of terminal — local, remote, console, or S-console (a console shared between background, system, and foreground jobs) — and the type of hardware interface the terminal uses — DL or DZ.

The WIDTH column indicates the width in characters (up to 255) of the terminal listing or display text.

The next four columns indicate which SET options are in effect on the terminal. If you have set TAB, the terminal can execute hardware tabs. If you have set CRLF, the terminal issues a carriage return and line feed whenever you attempt to type past the right margin. The terminal is capable of executing hardware form feeds if you have set FORM and, on graphics terminals, capable of echoing RUBOUT characters as backspace-space-backspace if you have set SCOPE.

The last column, SPEED, lists the terminal's baud rate (if interface is DZ). An N/A under the SPEED column indicates that the baud rate is not alterable (DL interface).

## 14.2.12 Physical Memory Layout Option (/X)

The /X option shows the organization of physical memory. The listing displays such information as where jobs are loaded, where the device handlers are loaded, where KMON and the USR reside, and the number of words of memory each occupies. Memory addresses are displayed in octal.

If you are running under the XM monitor, the listing is divided into two sections, the first for extended memory and the second for kernel memory.

The following example displays the organization of physical memory when running under the SJ monitor.

Kernel Memory

<table><tr><td colspan="3">* /X</td></tr><tr><td>Address</td><td>Module</td><td>Words</td></tr><tr><td>160000</td><td>IOPAGE</td><td>4096.</td></tr><tr><td>157400</td><td>RK</td><td>120.</td></tr><tr><td>127274</td><td>RMON</td><td>6170.</td></tr><tr><td>126112</td><td>DY</td><td>313.</td></tr><tr><td>001000</td><td>..BG..</td><td>21797.</td></tr></table>

The next example shows the organization of physical memory when running under the XM monitor.

| Address | Module | Words |
| --- | --- | --- |
| 01000000 | VM | 393216. |
| 00160000 | ...... | 102400. |

| Address | Module | Words |
| --- | --- | --- |
| 160000 | IOPAGE | 4096. |
| 157350 | RK | 140. |
| 124144 | RMON | 6970. |
| 122612 | DY | 365. |
| 111610 | USR | 2305. |
| 001000 | ..BG... | 10620. |

## 14.2.13 Summary Option (/Z)

The /Z option has the same effect as a combination of the /M, /C, /H, /J, and /O options. In other words, /Z lists the following information about your system:

• Monitor configuration

\- Set options in effect on the monitor

\- Hardware configuration

\- System generation special features in effect

This information prints out in the order shown in the following sample.

```txt
* /Z

RT-11FB(S) V05.xx
Booted from DLO:RT11FB

USR is set SWAP
EXIT is set SWAP
KMON is set IND
TT is set NOQUIET
ERROR is set ERROR
SL is set OFF
EDIT is set EDIT
KMON nesting depth is 3
Global .SCCA flag is disabled

PDP 11/23 PLUS Processor
1024KB of Memory
Extended Instruction Set (EIS)
KT11 Memory Management Unit
Parity Memory
GO Cycle System Clock
```

(1)
