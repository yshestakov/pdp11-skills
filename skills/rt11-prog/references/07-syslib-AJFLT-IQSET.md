# RT-11 PRM reference: Ch.3 SYSLIB subroutines AJFLT through IQSET (3.1-3.43)

Source: RT-11 Programmer's Reference Manual AA-H378C-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' sometimes reads as ',' (`,MCALL` = `.MCALL`), 'R0' as 'RO', '#' as '\*' or '*'. Verify exact macro expansions against `sysmac_v53.mac`.

Contents:
- 3.1 AJFLT
- 3.2 CHAIN
- 3.3 CLOSEC/ICLOSE
- 3.4 CONCAT
- 3.5 CVTTIM
- 3.6 DEVICE (FB and XM Only)
- 3.7 DJFLT
- 3.8 GETSTR
- 3.9 GTIM
- 3.10 GTJB/IGTJB
- 3.11 GTLIN
- 3.12 IABTIO
- 3.13 IADDR
- 3.14 IAJFLT
- 3.15 IASIGN
- 3.16 ICDFN
- 3.17 ICHCPY (FB and XM Only)
- 3.18 ICLOSE
- 3.19 ICMKT
- 3.20 ICSI
- 3.21 ICSTAT
- 3.22 IDELET
- 3.23 IDJFLT
- 3.24 IDSTAT
- 3.25 IENTER
- 3.26 IFETCH
- 3.27 IFPROT
- 3.28 IFREEC
- 3.29 IGETC
- 3.30 IGETSP
- 3.32 IJCVT
- 3.33 ILUN
- 3.34 INDEX
- 3.35 INSERT
- 3.36 INTSET
- 3.37 IPEEK
- 3.38 IPEEKB
- 3.39 IPOKE
- 3.40 IPOKEB
- 3.41 INPUT
- 3.42 IQSET
- 3.43 IRAD50

---

# Chapter 3 System Subroutine Description and Examples

This chapter presents all SYSLIB functions and subroutines in alphabetical order and provides a detailed description of each one. An example of each call in a FORTRAN program is given.

## 3.1 AJFLT

The AJFLT function converts an INTEGER\*4 value to a REAL\*4 value and returns that result as the function value.

Form: a = AJFLT (jsrc)

where:

jsrc is the INTEGER\*4 variable to be converted

Function Results:

The function result is a REAL\*4 value.

Errors:

None.

Example:

The following example converts the INTEGER\*4 value contained in JVAL to single precision (REAL\*4), multiplies it by 3.5, and stores the result in VALUE.

REAL\*4 VALUE,AJFLT
INTEGER\*4 JVAL
.
.
.
VALUE=AJFLT(JVAL)\*3.5

## 3.2 CHAIN

The CHAIN subroutine allows a background program (or any program in the single-job system) to transfer control directly to another background program and pass specified information to it. CHAIN cannot be called from a completion or interrupt routine. The FORTRAN impure area is not preserved across a chain. Therefore, when chaining from one program to another, the information must be reset in the program being chained to. When chaining to any other program, the user should explicitly close the opened logical units with calls to the CLOSE routine. Any routines specified in a FORTRAN USEREX library call are not executed if a CHAIN is accomplished (see Appendix B in the RT-11/RSTS/E FORTRAN IV User's Guide).

## Form: CALL CHAIN (dblk,var,wcnt)

## where:

dblk is the address of a four-word Radix-50 descriptor of the file specification for the program to be run (see the PDP-11 FORTRAN Language Reference Manual for the format of the file specification)

var is the first variable (which must start on a word boundary) in a sequence of variables with increasing memory addresses to be passed between programs in the chain parameter area (absolute locations 510 to 777). A single array or a COMMON block (or portion of a COMMON block) is a suitable sequence of variables

wcnt is a word count specifying the number of words (beginning at var) to be passed to the called program. The argument wcnt may not exceed 60. If no words are passed, then a word count of 0 must be supplied

If the size of the chain parameter area is insufficient, it can be increased by specifying the /B (or /BOTTOM) option to LINK for both the program executing the CHAIN call and the program receiving control.

The data passed can be accessed through a call to the RCHAIN routine. For more information on chaining to other programs, see the .CHAIN programmed request (Section 2.6).

## Errors:

None.

## Example:

The following example transfers control from the main program to PROG.SAV on DT0, and passes it variables.

```txt
DIMENSION SPEC(2)
INTEGER*2 DATA(10)
DATA SPEC/GRDTOPRO, GRG SAV/
.
.
.
CALL CHAIN (SPEC,DATA,10)
```

## 3.3 CLOSEC/ICLOSE

The CLOSEC subroutine terminates activity on the specified channel and frees it for use in another operation. The handler for the associated device must be in memory. CLOSEC cannot be called from a completion or interrupt routine.

```txt
Form: CALL CLOSEC (chan[,i])
    i = CLOSEC(chan)
    CALL ICLOSE (chan[,i])
    i = ICLOSE(chan)
```

where:

chan is the channel number to be closed. This argument must be located so that the USR cannot swap over it

i is the error return if a protection violation occurs

A CLOSEC or PURGE must eventually be issued for any channel opened for input or output. A CLOSEC call specifying a channel that is not open is ignored.

A CLOSEC performed on a file that was opened via an IENTER causes the device directory to be updated to make that file permanent. If the device associated with the specified channel already contains a file with the same name and type, the old copy is deleted when the new file is made permanent. If the file name is protected, then a protection error is generated. A CLOSEC on a file opened via LOOKUP does not require any directory operations.

When an entered file is closed, its permanent length reflects the highest block of the file written since the file was entered; for example, if the highest block written is block number 0, the file is given a length of 1; if the file was never written, it is given a length of 0. If this length is less than the size of the area allocated at IENTER time, the unused blocks are reclaimed as an empty area on the device.

## Errors:

i = 0 Normal return.

= -4 A protected file with the same name already exists on a device. The CLOSEC is performed, resulting in two files on the device with the same name.

## Example:

The following example creates and processes a 56-block file.

```prolog
REAL*4 DBLK(2)
DATA DBLK/GRSYONEW,GRFILDAT/
DATA ISIZE/56/
.
.
.
ICHAN=IGETC()
IF(ICHAN,LT.0) GOTO 100
IERR=IENTER(ICHAN,DBLK,ISIZE)
IF(IERR,LT.0)GOTO 20
GOTO(110,120,130)ABS(IER)
CALL ICLOSE (ICHAN,I)
IF(I,EQ.-4) GOTO 200
CALL IFREEC(ICHAN)
CALL EXIT
STOP 'NO AVAILABLE CHANNELS'
STOP 'CHANNEL ALREADY IN USE'
STOP 'NOT ENOUGH ROOM ON DEVICE'
STOP 'DEVICE IN USE'
STOP 'PROTECTION ERROR'
END
```

## 3.4 CONCAT

The CONCAT subroutine concatenates two character strings.

Form: CALL CONCAT (a,b,out[,len[,err]])

where:

a is the array containing the left string. The string must be terminated with a null byte

b is the array containing the right string. The string must be terminated with a null byte

out is the array into which the concatenated result is placed. This array must be at least one element longer than the maximum length of the resultant string (that is, one greater than the value of len, if specified)

len is the integer number of characters representing the maximum length of the output string. The effect of len is to truncate the output string to a given length, if necessary

err is the logical error flag set if the output string is truncated to the length specified by len

CONCAT sets the string in the array out to be the string in array a immediately followed on the right by the string in array b and a terminating null character.

## NOTE

Any combination of string arguments is allowed, so long as b and out do not specify the same array.

Concatenation stops when a null character is detected in b, or when the number of characters specified by len has been moved.

If either the left or right string is a null string, the other string is copied to out. If both are null strings, then out is set to a null string. The old contents of out are lost when this routine is called.

## Errors:

Error conditions are indicated by err, if specified. If err is given and the output string would have been longer than len characters, then err is set to .TRUE.; otherwise, err is unchanged.

## Example:

The following example concatenates the string in array STR and the string in array IN and stores the resultant string in array OUT. OUT cannot be larger than 29 characters.

LOGICAL\*1 IN(22),OUT(30),STR(7)

CALL CONCAT(STR, IN, OUT, 29)

## 3.5 CVTTIM

The CVTTIM subroutine converts a two-word internal format time to hours, minutes, seconds, and ticks.

Form: CALL CVTTIM (time,hrs,min,sec,tick)

time is the two-word internal format time to be converted. If time is considered as a two-element INTEGER\*2 array, then:
    time (1) is the high-order time
    time (2) is the low-order time

hrs is the integer number of hours

min is the integer number of minutes

tick is the integer number of ticks (1/60 of a second for 60-cycle clocks; 1/50 of a second for 50-cycle clocks)

```txt
Errors:
    None.
Example:
    INTEGER*4 ITIME
    :
    :
    CALL GTIM(ITIME)          !GET CURRENT TIME-OF-DAY
    CALL CVTTIM(ITIME,IHRS,IMIN,ISEC,ITCK)
    IF(IHRS,GE,12,AND, IHRS,LT,13) GOTO 100 !TIME FOR LUNCH
```

## 3.6 DEVICE (FB and XM Only)

The DEVICE subroutine allows you to set up a list of addresses to be loaded with specified values when the program is terminated. If a job terminates or is aborted with a CTRL/C from the terminal, this list is picked up by the system and the appropriate addresses are set up with the corresponding values.

This function is primarily designed to allow user programs to load device registers with necessary values. In particular, it is used to turn off a device's interrupt enable bit when the program servicing the device terminates.

Only one address list can be active at any given time; hence, if multiple DEVICE calls are issued, only the last one has any effect. The list must not be modified by the program after the DEVICE call has been issued, and the list must not be located in an overlay or an area over which the USR swaps.

The second argument of the call (link) provides support for a linked list of tables. The link argument is optional and causes the first word of the list to be processed as the link word.

Form: CALL DEVICE (ilist[,link])

```txt
Errors:
    None.
Example:
    INTEGER*4 JVAL
    REAL*8 DJFLT,D
    ;
    ;
    D=DJFLT(JVAL)
```

## where:

ilist is an integer array that contains two-word elements, each composed of a one-word address and a one-word value to be put at that address, terminated by a zero word. On program termination, each value is moved to the corresponding address

link is an optional argument that can be any value. This indicates that a linked list table is to be used

If the linked list form is used the first word of the array is the link list pointer

For more information on loading values into device registers, see the .DEVICE programmed request (Section 2.19).

Errors:

Example:

```c
INTEGER*2 IDR11(3)          !DEVICE ARRAY SPEC
DATA IDR11(1)/"167770/      !DR11 CSR ADDRESS (OCTAL)
DATA IDR11(2)/0/         !VALUE TO CLEAR INTERRUPT ENABLE
DATA IDR11(3)/0/         !AND END-OF-LIST FLAG
CALL DEVICE(IDR11)           !SET UP FOR ABORT
```

## 3.7 DJFLT

The DJFLT function converts an INTEGER\*4 value into a REAL\*8 (DOUBLE PRECISION) value and returns that result as the function value.

<div class="docvortex-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Form: $\mathbf{d} = \mathbf{DJFLT}(\mathrm{jsrc})$
</div>

where:

```txt
jsrc    specifies the INTEGER*4 variable to be converted
```

If DJFLT is used, it must be defined in the FORTRAN program, either explicitly (REAL\*8 DJFLT) or implicitly (IMPLICIT REAL\*8 (D)). Without a definition, DJFLT is assumed to be REAL\*4 (single precision).

## Function Results:

The function result is the REAL\*8 value that is the result of the operation.

## 3.8 GETSTR

The GETSTR subroutine reads a formatted ASCII record from a specified FORTRAN logical unit into a specified array. The data is truncated (trailing blanks removed) and a null byte is inserted at the end to form a character string.

GETSTR can be used in main program routines or in completion routines, but it cannot be used in both at the same time. If GETSTR is used in a completion routine, it cannot be the first I/O operation on the specified logical unit.

Form: CALL GETSTR (lun,out,len,err)

## where:

lun is the integer FORTRAN logical unit number of a formatted sequential file from which the string is to be read

out is the array to receive the string; this array must be at least one element longer than len

len is the integer number representing the maximum length of the string that is allowed to be input

err is the LOGICAL\*1 error flag that is set to .TRUE. if an error occurred. If an error did not occur, the flag is .FALSE

## Errors:

Error conditions are indicated by err. If err is .TRUE., the values returned are as follows:

err = -1 End-of-file for a read operation.

err = -2    Hard error for a read operation.

err = -3 More than len bytes were contained in a record.

## Example:

The following example reads a string of up to 80 characters from logical unit 5 into the array STRING.

LOGICAL\*1 STRING(81),ERR
:
.
CALL GETSTR(5,STRING,80,ERR)

## 3.9 GTIM

The GTIM subroutine returns the current time of day. The time is returned in two words and is given in terms of clock ticks past midnight. If the system does not have a line clock, a value of 0 is returned. If an RT-11 monitor TIME command has not been entered, the value returned is the time elapsed since the system was bootstrapped, rather than the time of day.

```txt
Form: CALL GTIM (itime)
```

where:

itime is the two-word area to receive the time of day

The high-order time is returned in the first word, the low-order time in the second word. The CVTTIM routine (see Section 3.5) can be used to convert the time into hours, minutes, seconds, and ticks. CVTTIM performs the conversion based on the monitor configuration word for 50- or 60-cycle clocks. Under an FB or XM monitor, the time-of-day is automatically reset after 24:00 when a GTIM is executed; under the single-job monitor, it is not.

Errors

None.

Example:

```txt
INTEGER*4 JTIME
.
.
CALL GTIM(JTIME)
```

## 3.10 GTJB/IGTJB

The GTJB subroutine returns information about a job in the system.

```txt
Form: CALL GTJB (addr,[jobblk [,i]])
    i = GTJB (addr,[jobblk])
    CALL IGTJB (addr,[jobblk [,i]])
    i = IGTJB (addr,[jobblk])
```

where:

addr is the address of an eight- or twelve-word block into which the parameters are passed

The parameters returned are as follows:

Word 1 Job Number = priority level\*2 (background job is 0, system jobs are 2, 4, 6, 10, 12, 14, foreground job is 16 in system job monitors; background job is 0, foreground job is 2 in FB and XM monitors; job number is 0 in SJ monitor)
2 High-memory limit of job partition (last location plus 2)
3 Low-memory limit of job partition (first location)
4 Pointer to I/O channel space
5 Address of job's impure area in FB and XM monitors (0 in SJ)

6 Low byte: unit number of job's console terminal (only if the multiterminal option is present; 0 when the multiterminal feature is not used)

7 Virtual high limit for a job created with the linker /V option (XM only; 0 in SJ and FB and where the Linker /V option is not used)

8-9 Reserved for future use

10-12 ASCII, logical job name (system job monitors only)

jobblk is a pointer to a three-word ASCII job name for which data is being requested. Do not specify this argument when requesting the eight-word block

i is an error return if the job is not running

If one argument is used with the call, only the first eight parameters will be passed. For example,

```txt
INTEGER IJPARM(8)
CALL GTJB (IJPARM)
I = GTJB (IJPARM)
```

At least a comma must follow the argument to pass the information into a 12-word block. For example,

```sql
INTEGER IJPARM(12)
CALL GTJB (IJPARM,)
I = GTJB (IJPARM,)
```

```python
Errors:
    i = 0   Normal return.
    = -1  No such job currently running.

Example:
        C THIS IS AN EXAMPLE UNDER A SYSTEM
        C JOB MONITOR TO SEE IF THE FOREGROUND
        C JOB IS RUNNING
        DIMENSION JDATA(12)
        .
        .
        .
        I = GTJB (JDATA, 16)
        IF (I.EQ.0) GOTO 20
        TYPE 10
    10   FORMAT('NO FG JOB!')
        STOP
    20   .
        .
        .
```

## 3.11 GTLIN

The GTLIN subroutine transfers a line of input from the console terminal or an active indirect command file to the user program. This request allows you to input information at the console terminal, and it allows the program to operate through indirect files. This subroutine requires the USR. The maximum size of the input line is 80 characters. See the .GTLIN programmed request for setting bits in the Job Status Word to pass lowercase letters and to establish a nonterminating condition.

Form: CALL GTLIN (result[,prompt])

where:

result is the array receiving the string. This LOGICAL\*1 array contains a maximum of 80 characters plus 0 as the end indicator, and therefore must be dimensioned to at least 81 elements

prompt is a LOGICAL\*1 array containing an optional prompt string to be printed before the input line is received. The string format is the same as that used by the PRINT subroutine. If this argument is not present, no prompt is printed

Errors:

```txt
Errors:
    None.
Example:
    LOGICAL*1 INP(80),PROMT(G)
    DATA PROMT /'N','A','M','E','?',"200/
    .
    .
    .
    CALL GTLIN(INP,PROMT)
    .
    .
    .
```

## 3.12 IABTIO

The IABTIO function aborts I/O on a specified channel.

```txt
Form: CALL IABTIO (chan)
```

where:

chan is the channel number for which to abort I/O

Errors:

None.

## 3.13 IADDR

The IADDR function returns the 16-bit absolute memory address of its argument as the integer function value.

```txt
Form: i = IADDR (arg)
```

```txt
EXTERNAL CAREA
J=IADDR(CAREA)
```

## where:

arg is the variable or constant whose memory address is to be obtained. The value obtained by passing an expression as arg is unpredictable

Example:

IADDR can be used to find the address of an assembly language global area. For example:

## 3.14 IAJFLT

The IAJFLT function converts an INTEGER\*4 value to a REAL\*4 value and stores the result.

```txt
Form: i = IAJFLT (jsrc,ares)
```

where:

jsrc is the INTEGER\*4 variable to be converted

ares is the REAL\*4 variable or array element to receive the converted value

## Function Results:

```txt
i = -1    Normal return; the result is negative.
    = 0    Normal return; the result is 0.
    = 1    Normal return; the result is positive.
```

Errors:

i = -2 Significant digits were lost during the conversion.

Example:

```txt
INTEGER*4 JVAL
REAL*4 RESULT
:
:
IF(IAJFLT(JVAL,RESULT).EQ.-2) TYPE 99
99 FORMAT (' OVERFLOW IN INTEGER*4 TO REAL CONVERSION')
```

## 3.15 IASIGN

The IASIGN function sets information in the FORTRAN logical unit table (overriding the defaults) for use when the FORTRAN Object Time System (OTS) opens the logical unit. This function can be used with ICSI (see

Section 3.20) to allow a FORTRAN program to accept a standard CSI input specification. IASIGN must be called before the unit is opened; that is, before any READ, WRITE, PRINT, TYPE, ACCEPT, or OPEN statements are executed that reference the logical unit.

Form: i = IASIGN (lun,idev[,ifiltyp[,isize[,itype]]])

## where:

lun is an INTEGER\*2 variable, constant, or expression specifying the FORTRAN logical unit for which information is being specified

idev is a one-word Radix-50 device name; this can be the first word of an ICSI input or output file specification

ifiltyp is a three-word Radix-50 file name and file type; this can be words 2 through 4 of an ICSI input or output file specification

isize is the length (in blocks) to allocate for an output file; this can be the fifth word of an ICSI output specification. If 0, the larger of either one-half the largest empty segment or the entire second largest empty segment is allocated. If the value specified for length is -1, the entire largest empty segment is allocated

itype is an integer value determining the optional attributes to be assigned to the file. This value is obtained by adding the values that correspond to the desired operations:

1 Use double buffering for output.

2 Open the file as a temporary file.

4 Force a LOOKUP on an existing file during the first I/O operation. (Otherwise, the first FORTRAN I/O operation determines how the file is opened. Normally if the first I/O operation is a write, an IENTER would be performed on the specified logical unit. A read always causes a LOOKUP.)

8 Expand carriage control information (see Notes below).

16 Do not expand carriage control information.

32 File is read only.

## Notes:

Expanded carriage control information applies only to formatted output files and means that the first character of each record is used as a carriage control character when processing a write operation to the given logical unit. The first character is removed from the record and converted to the appropriate ASCII characters to simulate the requested carriage control.

If carriage control information is not expanded, the first character of each record is unmodified and the FORTRAN OTS outputs a line feed, followed by the record, followed by a carriage return.

If carriage control is unspecified, the FORTRAN OTS sends expanded carriage control information to the terminal and line printer and sends unexpanded carriage control information to all other devices and files. See the PDP-11 FORTRAN Language Reference Manual for further carriage control information.

## Errors:

$\mathbf{i} = 0$ Normal return.

<> 0 The specified logical unit is already in use, or there is no space for another logical unit association.

## Example:

The following example (1) creates an output file on logical unit 3, using the first output file given to the RT-11 Command String Interpreter (CSI), (2) sets up the output file for double buffering, (3) creates an input file on logical unit 4, based on the first input file specification given to the RT-11 CSI, and (4) makes the input file available for read-only access.

```txt
INTEGER*2 SPEC(39)
REAL*4 EXT(2)
DATA EXT/GRDATDAT,GRDATDAT/ !DEFAULT FILE TYPE IS DAT
:
.
10 IF(ICSI(SPEC,EXT,,,0),NE,0) GOTO 10
C
C DO NOT ACCEPT ANY SWITCHES
C
CALL IASIGN(3,SPEC(1),SPEC(2),SPEC(5),1)
CALL IASIGN(4,SPEC(16),SPEC(17),0,32)
```

## 3.16 ICDFN

The ICDFN function increases the number of input/output channels. Note that ICDFN defines new channels; any channels defined with an earlier ICDFN function are not used. Thus, an ICDFN for 20(decimal) channels (while the 16[decimal] original channels are defined) causes only 20 I/O channels to exist; the space for the original 16 is unused. The space for the new channel area is allocated out of the free space managed by the FORTRAN system.

Form: i = ICDFN(num[,area])

## where:

num is the integer number of channels to be allocated. The number of channels must be greater than 16 and can be a maximum of 256. The program can use all new channels greater than 16 without a call to IGETC; the FORTRAN system input/output uses only the first 16 channels. This argument must be positioned so that the USR cannot swap over it

area is the space allocated from within the calling program. Under FB and SJ monitors; be sure that the space is outside the USR swapping area. If this argument is not specified, the space for the channels is allocated in the FORTRAN OTS work area

Notes:

1. ICDFN cannot be issued from a completion or interrupt routine.

2. It is recommended that the ICDFN function be used at the beginning of the main program before any I/O operations are initiated.

3. If ICDFN is executed more than once, a completely new set of channels is created each time ICDFN is called.

4. ICDFN requires that extra memory space be allocated to foreground programs (see Section 1.2.4.1).

5. Any channels that were open prior to the ICDFN are copied over to the new set of channel status tables.

Function Results:

i = 0    Normal return.

= 1 An attempt was made to allocate fewer channels than already exist.

= 2 Not enough free space is available for the channel area.

Example:

$$
\text {IF} (\text {ICDFN} (2 4), \text {EQ}, 2) \text {STOP} ^ {\prime} \text {NOT ENOUGH MEMORY} ^ {\prime}
$$

## 3.17 ICHCPY (FB and XM Only)

The ICHCPY function opens a channel for input, logically connecting it to a file that is currently open by another job for either input or output. This function can be used by either the foreground or the background job. An ICHCPY must be done before the first read or write for the given channel.

Form: i = ICHCPY (chan,ochan[,jobblk])

where:

chan is the channel the job will use to read the data. You must obtain this channel through an IGETC call, or you can use channel 16 or higher if you have done an ICDFN call

ochan is the channel number of the other job that is to be copied

jobblk is a pointer to a three-word ASCII job name

## Notes:

1. If the other job's channel was opened with an IENTER function or a .ENTER programmed request to create a file, your channel indicates a file that extends to the highest block that the creator of the file had written at the time the ICHCPY was executed.

2. A channel that is open on a sequential-access device should not be copied, because buffer requests can become intermixed.

3. Your program can write on a copied channel to a file that is being created by the other job, just as your program could if it were the creator. When your channel is closed, however, no directory update takes place.

Errors:

$\mathrm{i} = 0$ Normal return.

= 1 Specified job does not exist or does not have the specified channel (ochan) open.

= 2 Channel (chan) is already open.

## 3.18 ICLOSE

See the SYSLIB subroutine CLOSEC.

## 3.19 ICMKT

The ICMKT function cancels one or more scheduling requests (made by an ISCHED, ITIMER, or MRKT routine). Support for ICMKT in SJ requires that timer support be created through SYSGEN.

Form: i = ICMKT (id,time)

where:

id is the identification integer of the request to be canceled. If id is equal to 0, all scheduling requests are canceled

time is the name of a two-word area in which the monitor returns the amount of time remaining in the canceled request

For further information on canceling scheduling requests, see the .CMKT programmed request (Section 2.9).

Errors:

i = 0    Normal return.
    = 1    id was not equal to 0 and no scheduling request with that identification could be found.

Example:

```prolog
INTEGER*4 J
.
.
.
CALL ICMKT(O,J)      !ABORT ALL TIMER REQUESTS NOW
.
.
.
END
```

## 3.20 ICSI

The ICSI function calls the RT-11 Command String Interpreter in special mode to parse a command string and return file descriptors and options to the program. In this mode, the CSI does not perform any handler IFETCHes, CLOSECs, IENTERs, or LOOKUPs. ICSI cannot be called from a completion or interrupt routine. This subroutine requires the USR.

Form: i = ICSI (filspc,deftyp,[cstring],[option],n)

where:

filspc is the 39-word area to receive the file specifications. The format of this area (considered as a 39-element INTEGER\*2 array) is:

Word 1 output file number 1
4 specification
5 output file number 1 length
6 output file number 2
9 specification
10 output file number 2 length
11 output file number 3
14 specification
15 output file number 3 length
16 input file number 1
19 specification
20 input file number 2
23 specification
24 input file number 3
27 specification
28 input file number 4
31 specification
32 input file number 5
35 specification
36 input file number 6
39 specification

deftyp is the table of Radix-50 default file types to be assumed when a file is specified without a file type:

deftyp(1) is the default for all input file types

deftyp(2) is the default file type for output file number 1

deftyp(3) is the default file type for output file number 2

deftyp(4) is the default file type for output file number 3

cstring is the area that contains the ASCIZ command string to be interpreted; the string must end in a zero byte. If the argument is omitted, the system prints the prompt character (\*) at the terminal and accepts a command string. If input is from an indirect command file, the next line of that file is used

## option

is the name of an INTEGER\*2 array dimensioned (4,n) where n represents the number of options defined to the program. This argument must be present if the value specified for n is non-zero. This array has the following format for the jth option described by the array:

option(1,j) is the one-character ASCII name of the option
option(2,j) is set by the routine to 0, if the option did not occur; to 1, if the option occurred without a value; to 2, if the option occurred with a value option(3,j) is set to the file number on which the option is specified

option(4,j) is set to the specified value if option(2,n) is equal to 2

n is the number of options defined in the array option

## Notes:

1. The array option must be set up to contain the names of the valid options. For example, use the following to set up names for five options:

```csv
INTEGER*2 SW(4,5)
DATA SW(1,1)/'S'/,SW(1,2)/'M'/,SW(1,3)/'I'/
DATA SW(1,4)/'L'/,SW(1,5)/'E'/
```

2. Multiple occurrences of the same option are supported by allocating an entry in the option array for each occurrence of the option. Each time the option occurs in the option array, the next unused entry for the named option is used.

3. The arguments of ICSI must be positioned so that the USR cannot swap over them. For more information on calling the Command String Interpreter, see the .CSISPC programmed request (Section 2.14).

## Errors:

$\mathrm{i} = 0$ Normal return.

= 1 Illegal command line; no data was returned.

$= 2$ An illegal device specification occurred in the string.

= 3 An illegal option was specified, or a given option was specified more times than were allowed for in the option array.

## Example:

The following example causes the program to loop until a valid command is typed at the console terminal.

```csv
INTEGER*2 SPEC(39)
REAL*4 EXT(2)
DATA EXT/GRDATDAT,GRDATDAT/
.
.
.
10 TYPE 99
99 FORMAT (' ENTER VALID CSI STRING WITH NO OPTIONS')
IF(ICSI(SPEC,EXT,,,O).NE.0) GOTO 10
```

## 3.21 ICSTAT

The ICSTAT function obtains information about a channel.

```txt
Form: i = ICSTAT (chan,addr)
```

where:

chan is the channel whose status is desired

addr is a six-word area to receive the status information. The area, as a six-element INTEGER\*2 array, has the following format:

Word 1 channel status word

2 starting absolute block number of file on this channel

3 length of file

4 highest block number written since file was opened

5 unit number of device with which this channel is associated

6 Radix-50 of device name with which the channel is associated

Errors:

```python
i = 0    Normal return.
    = 1    Channel specified is not open.
```

## Example:

The following example obtains channel status information about channel I.

```txt
INTEGER*2 AREA(6)
I=7
IF(ICSTAT(I,AREA),NE,0) TYPE 99,I
99 FORMAT(1X,'CHANNEL',I4,'IS NOT OPEN')
```

## 3.22 IDELET

The IDELET function deletes a named file from an indicated device. IDELET requires the USR and cannot be issued from a completion or interrupt routine.

```txt
Form: i = IDELET (chan, dblk[, seqnum])
```

where:

chan is the channel to be used for the delete operation. You must obtain this channel through an IGETC call, or you can use channel 16(decimal) or higher if you have done an ICDFN call

dblk is the four-word Radix-50 specification (dev:filnam.typ) for the file to be deleted

seqnum is the file number for cassette operations: if this argument is blank, a value of 0 is assumed

For magtape operation, it describes a file sequence number that can have the following values:

## Value

## Meaning

-1 This value suppresses rewinding and searching for a file name from the current tape position. Note that if the position is unknown, the handler executes a positioning algorithm that involves backspacing until an end-of-file label is found. The user should not use any other value since all other negative values are reserved for future use.

0 This value rewinds the magtape and spaces forward until the file name is found.

n Where n is any positive number. This value positions the magtape at file sequence number n. If the file represented by the file sequence number is greater than two files away from the beginning of the tape, a rewind is performed. If not, the tape is backspaced to the file.

## NOTE

The arguments of IDELET must be located so that the USR cannot swap over them.

The specified channel is left inactive when the IDELET is complete. IDELET requires that the handler to be used be resident (via an IFETCH call or a LOAD command from KMON) at the time the IDELET is issued. If the handler is not resident, a monitor error occurs.

For further information on deleting files, see the .DELETE programmed request (Section 2.18).

## Errors:

$\mathrm{i} = 0$ Normal return.

= 1 Channel specified is already open.

= 2 File specified was not found.

= 3 Device in use.

= 4 The file is protected and cannot be deleted.

## Example:

The following example deletes a file named FTN5.DAT from SY0.

```txt
REAL*4 FILNAM(2)
DATA FILNAM/GRSYOFTN,GR5  DAT/
.
.
.
I=IGETC()
IF(I,LT,O) STOP 'NO CHANNEL'
CALL IDELET(I,FILNAM)
CALL IFREEC(I)
```

## 3.23 IDJFLT

The IDJFLT function converts an INTEGER\*4 value into a REAL\*8 (DOUBLE PRECISION) value and stores the result.

```txt
Form: i = IDJFLT (jsrc,dres)
```

jsrc    specifies the INTEGER\*4 variable that is to be converted
dres    specifies the REAL\*8 (or DOUBLE PRECISION) variable to receive the converted value

## Function Results:

```txt
i = -1    Normal return; the result is negative.
= 0    Normal return; the result is 0.
= 1    Normal return; the result is positive.
Errors:
None.
Example:
INTEGER*4 JJ
REAL*8 DJ
:
:
IF(IDJFLT(JJ,DJ),LE,0) TYPE 99
99 FORMAT (' VALUE IS NOT POSITIVE')
```

## 3.24 IDSTAT

The IDSTAT function obtains information about a particular device. It requires the USR and cannot be issued from a completion or interrupt routine.

```txt
Form: i = IDSTAT (devnam,cblk)
```

where:

```txt
devnam is the Radix-50 device name
```

cblk is the four-word area used to store the status information. The area, as a four-element INTEGER\*2 array, has the following format:

Word 1 device status word (see Section 2.29)

3 entry point of handler (non-zero implies that the handler is in memory)

4 size of the device (in 256-word blocks) for block-replaceable devices; zero for sequential-access devices

## NOTE

The arguments of IDSTAT must be positioned so that the USR cannot swap over them.

IDSTAT looks for the device specified by devnam and, if found, returns four words of status in cblk.

## Errors:

$\mathbf{i} = 0$ Normal return.

= 1 Device not found in monitor tables.

## Example:

The following example determines whether the line printer handler is in memory. If it is not, the program stops and prints a message to indicate that the handler must be loaded.

```csv
INTEGER IDNAM
INTEGER*2 CBLK(4)
DATA IDNAM/3RLP /
DATA CBLK/4*0/
CALL IDSTAT(IDNAM,CBLK)
IF(CBLK(3),EQ.0) STOP 'LOAD THE LP HANDLER AND RERUN'
```

## 3.25 IENTER

The IENTER function allocates space on the specified device and creates a tentative directory entry for the named file. If a file of the same name already exists on the specified device, it is not deleted until the tentative entry is made permanent by CLOSEC or ICLOSE. The file is attached to the channel number specified. This routine requires the USR.

Form: i = IENTER (chan,dblk,length[,seqnum])

where:

chan is the integer specification for the RT-11 channel to be associated with the file. You must obtain this channel through an IGETC call, or you can use channel 16 or higher if you have done an ICDFN call

dblk is the four-word Radix-50 descriptor of the file to be operated upon

length is the integer number of blocks to be allocated for the file. If 0, the larger of either one-half the largest empty segment or the entire second largest empty segment is allocated. If the value specified for length is -1, the entire largest empty segment is allocated (see the .ENTER programmed request, Section 2.32)

seqnum is a file number for cassette. If this argument is blank, a value of 0 is assumed.

For magtape, it describes a file sequence number that can have the following values:

-2 Rewind the magtape and space forward until the file name is found, or until logical-end-of-tape is detected. The magtape is now positioned correctly. A new logical-end-of-tape is implied.

-1 Space to the logical-end-of-tape and enter file.

0 Rewind the magtape and space forward until the file name is found or the logical-end-of-tape is detected. If the file name is found, an error is generated. If the file name is not found, then enter file.

n Position magtape at file sequence number n if n is greater than zero and the file name is not null.

## Notes:

1. IENTER cannot be issued from a completion or interrupt routine.

2. IENTER requires that the appropriate device handler be in memory.

3. The arguments of IENTER must be positioned so that the USR does not swap over them.

For further information on creating tentative directory entries, see the .ENTER programmed request (Section 2.32).

## Errors:

i = n    Normal return; number of blocks actually allocated (n = 0 for non-file-structured IENTER).

= -1 Channel (chan) is already in use.

= -2 In a fixed-length request, no space greater than or equal to length was found.

= -3 Device in use.

= -4 A file by that name already exists and is protected.

= -5 File sequence number not found.

## Example:

The following example allocates a channel for file TEMP.TMP on SY0. If no channel is available, the program prints a message and halts.

```m4
REAL*4 DBLK(2)
DATA DBLK/GRSYOTEM,GRP TMP/
ICHAN=IGETC()
IF(ICHAN,LT.0) STOP 'NO AVAILABLE CHANNEL'
C
C CREATE TEMPORARY WORK FILE
C
IF(IENTER(ICHAN,DBLK,20).LT.0) STOP 'ENTER FAILURE'
.
.
.
CALL PURGE(ICHAN)
CALL IFREEC(ICHAN)
```

## 3.26 IFETCH

The IFETCH function loads a device handler into memory from the system device, making the device available for input/output operations. The handler is loaded into the free area managed by the FORTRAN system. Once the handler is loaded, it cannot be released and the memory in which it resides cannot be reclaimed. IFETCH requires the USR and cannot be issued from a completion or interrupt routine. IFETCH issued from a foreground job will fail unless the handler is already in memory.

```javascript
Form: i = IFETCH (devnam)
```

## where:

devnam is the one-word Radix-50 name of the device for which the handler is desired. This argument can be the first word of an ICSI input or output file specification. This argument must be positioned so that the USR cannot swap over it

For further information on loading device handlers into memory, see the .FETCH programmed request (Section 2.34).

## Errors:

i = 0 Normal return.

= 1 Device name specified does not exist.

= 2    Not enough room exists to load the handler.

= 3 No handler for the specified device exists on the system device.

## Example:

The following example requests that the DX handler be loaded into memory; execution stops if the handler cannot be loaded.

```txt
REAL*4 IDNAM
DATA IDNAM/3RDX/
.
.
IF (IFETCH(IDNAM).NE.0) STOP 'FATAL ERROR FETCHING HANDLER'
```

## 3.27 IFPROT

The IFPROT function sets or removes file protection for a file.

Form: i = IFPROT (chan, filspc, prot)

where:

chan is the channel number to be used for the protect operation. You must obtain this channel through an IGETC call, or you can use the channel 16(decimal) or higher if you have done an ICDFN call

filspc is the file specification of the file to be protected or unprotected, in Radix-50

```txt
prot 1 = protect the file
0 = remove protection from the file
```

```python
Errors:
    i = 0    Normal return.
    = 1    Channel is in use.
    = 2    File not found.
    = 3    Invalid operation.
    = 4    Invalid prot value.
```

This example protects the file SY:RT11FB.SYS against deletion.

```matlab
ICHAN = IGETC()          !ALLOCATE CHANNEL
IF (ICHAN,LT,O) STOP 'CANNOT ALLOCATE CHANNEL'
I=IFPROT(ICHAN,'SY:RT11FB.SYS',1)
.
.
.
END
```

## 3.28 IFREEC

The IFREEC function returns a specified RT-11 channel to the available pool of channels. Before IFREEC is called, the specified channel must be closed or deactivated with a CLOSEC or ICLOSE (see Section 3.3) or a PURGE (see Section 3.92) call. IFREEC cannot be called from a completion or interrupt routine. IFREEC calls must be issued only for channels that have been successfully allocated by IGETC calls; otherwise, the results are unpredictable.

```txt
Form: i = IFREEC (chan)
```

<div class="docvortex-algorithm" style="white-space: pre-wrap; font-family:monospace;">
$\mathrm{i} = 0$ Normal return.  
$= 1$ Specified channel is not currently allocated.
</div>

## 3.29 IGETC

The IGETC function allocates an RT-11 channel, in the range 0 to 15(decimal), to be used by other SYSLIB routines and marks it in use so that the FORTRAN I/O system will not access it. IGETC cannot be issued from a completion or interrupt routine.

```javascript
Form: i = IGETC()
```

Example:
    ICHAN=IGETC()          !ALLOCATE CHANNEL
    IF(ICHAN,LT,O) STOP 'CANNOT ALLOCATE CHANNEL'
    .
    .
    .
    CALL IFREEC(ICHAN)          !FREE IT WHEN THROUGH
    .
    .
    .
END

## 3.30 IGETSP

The IGETSP subroutine obtains free space from the FORTRAN system and returns the address and size (in number of words) of the allocated space. When this space is obtained, it is allocated for the duration of the program.

Form: i = IGETSP (min,max,iaddr)

where:

min is the minimum space to be obtained without an error indicating that the desired amount of space is not available

max is the maximum space to be obtained

iaddr is the integer specifying the address of the start of the free space (buffer). Note that iaddr does not directly denote the storage area as a standard FORTRAN variable would. Rather, it denotes a word that contains the address of the storage space. It is most useful with IPEEK and IPOKE, or with assembly language subroutines

## NOTE

Extreme caution should be exercised to avoid using all of the free space allocated by the FORTRAN system. If the FORTRAN system runs out of dynamic free space, fatal errors (Error 29, 30, 42, and so forth) occur. See the RT-11 System Message Manual.

## Function Results:

i = n The actual size allocated whose value is min .LE. n .LE. max. The size (min, max, n) is specified in words.

Error:

i = -1 Not enough free space is available to meet the minimum requirements; no allocation was taken from the FORTRAN system free space.

Example:

```vba
N=IGETSP(256,256,IBUFF)          !GET 25G WORD BUFFER
IF(N.LT.O) STOP 'CANNOT GET BUFFER SPACE!'  !NO SPACE AVAILABLE
```

```txt
The IJCVT function converts an INTEGER*4 value to INTEGER*2 format.
If ires is not specified, the result returned is the INTEGER*2 value of jsrc.
If ires is specified, the result is stored there.
Form: i = IJCVT (jsrc[,ires])
where:
    jsrc specifies the INTEGER*4 variable or array element whose
    value is to be converted
    ires specifies the INTEGER*2 entity to receive the conversion re-
    sult
Function Results (if ires is specified):
    i = -2 An overflow occurred during conversion.
    = -1 Normal return; the result is negative.
    = 0 Normal return; the result is 0.
    = 1 Normal return; the result is positive.
Errors:
    None.
Example:
        INTEGER*4 JVAL
        INTEGER*2 IVAL
        .
        .
        .
        IF(IJCVT(JVAL,IVAL),EQ,-2) TYPE 99
99 FORMAT('NUMBER TOO LARGE IN IJCVT CONVERSION')

The ILUN function returns the RT-11 channel number with which a FOR-
TRAN logical unit is associated.
Form: i = ILUN (lun)
where:
    lun is an integer expression whose value is a FORTRAN logical
    unit number in the range 1-99
Function Results:
    = +n RT-11 channel number n is associated with lun.
Errors:
    i = -1 Logical unit is not open.
    = -2 Logical unit is opened to console terminal.
```

```txt
3.31 IGTJB See the SYSLIB subroutine GTJB, Section 3.10.
```

## 3.32 IJCVT

## 3.33 ILUN

## 3.34 INDEX

The INDEX subroutine searches a source string for the occurrence of a pattern string and returns the character position of the first occurrence of the pattern within the source.

Form: CALL INDEX (a,pattrn,[i],m)

or

$$
\mathbf {m} = \text {INDEX} (\mathrm{a}, \text {pattrn[,i]})
$$

where:

a is the array containing the source string to be searched; it must be terminated by a null byte

pattrn is the string being sought; it must be terminated by a null byte

i is the integer starting character position of the search in $a$. If $i$ is omitted, $a$ is searched beginning at the first character position

m is an integer variable to store the result of the search; m is set to the starting character position of pattrn in a, if found; otherwise m is 0

Errors:

None.

Example:

The following example searches the array STRING for the first occurrence of strings EFG and XYZ and searches the string ABCABCABC for the occurrence of string ABC after position 5.

```txt
CALL SCOPY('ABCDEFGHIJKLMNOPQRSTUVWXYZ',STRING)      !INITIALIZE STRING
CALL INDEX(STRING,'EFG',,M)          !M=5
CALL INDEX(STRING,'XYZ',,N)          !N=0
CALL INDEX('ABCABCABC','ABC',5,L)   !L=7
```

## 3.35 INSERT

The INSERT subroutine replaces a portion of one string with another string.

Form: CALL INSERT (in,out,i[,m])

where:

in is the array containing the string being inserted. The string must be terminated with a null if the number of characters is less than the value of m (below), or if m is not specified

out is the array containing the string being modified. The string must be terminated with a null

i is the integer specifying the character position in out at which the insertion begins

m is the integer maximum number of characters to be inserted

If the maximum number of characters (m) is not specified, all characters to the right of the specified character position (i) in the string being modified are replaced by the string being inserted. The insert string (in) and the string being modified (out) can be in the same array only if the maximum number of characters (m) is specified and is less than or equal to the difference between the position of the insert (i) and the maximum string length of the array.

```python
Errors:
    None.
Example:
    CALL SCOPY('ABCDEFGHIJKLMNOPQRSTUVWXYZ',S1)          !INITIALIZE STRING 1
    CALL SCOPY(S1,S2)                  !INITIALIZE STRING 2
    CALL INSERT('123',S1,6,3)         !S1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    CALL INSERT('123',S2,4)           !S2 = 'ABC123'
```

## 3.36 INTSET

The INTSET function establishes a FORTRAN subroutine as an interrupt service routine, assigns it a priority, and attaches it to a vector. INTSET requires that extra memory be allocated to foreground programs that use it (see Section 1.2.4.1).

```txt
Form: i = INTSET (vect,pri,id,crtn)
```

where:

vect is the integer specifying the address of the interrupt vector to which the subroutine is to be attached

pri is the integer specifying the actual priority level (4–7) at which the device interrupts

id is the identification integer to be passed as the single argument to the FORTRAN routine when an interrupt occurs. This allows a single crtn to be associated with several INTSET calls

crtn is a FORTRAN subroutine to be established as the interrupt routine. This name should be specified in an EXTERNAL statement in the FORTRAN program that calls INTSET. The subroutine has one argument:

SUBROUTINE crtn(id)
INTEGER id

When the routine is entered, the value of the integer argument is the value specified for id in the appropriate INTSET call

## Notes:

1. The id argument can be used to distinguish between interrupts from different vectors if the routine to be activated services multiple devices.

2. When using INTSET in FB or XM, the SYSLIB call DEVICE must be used in almost all cases to prevent interrupts from interrupting beyond program termination.

3. If the interrupt routine (crtn) has control for a period of time longer than the time in which two more interrupts using the same vector occur, interrupt overrun is considered to have occurred. The error message:

## ?SYSLIB-F-Interrupt overrun

is printed and the job is aborted. Jobs requiring very fast interrupt response are not viable with FORTRAN, since FORTRAN overhead lowers RT-11's interrupt response rate.

4. The interrupt routine (crtn) is actually run as a completion routine by the RT-11 .SYNCH macro. The pri argument is used for the RT-11 .INTEN macro.

5. A .PROTECT request is issued for the vector, but no attempt is made to report an error if the vector is already protected; furthermore, the vector is taken over unconditionally. See the .PROTECT programmed request (Section 2.64) for more information.

6. The FORTRAN interrupt service subroutine (crtn) cannot call the USR.

7. INTSET cannot be called from a completion or interrupt routine.

8. Interrupt enable should not be set on the associated device until the INTSET call has been successfully executed.

## Errors:

i = 0 Normal return.

= 1 Invalid vector specification.

= 2 Reserved for future use.

= 3 No space is available for the linkage setup.

```asm
Example:
    EXTERNAL CLKSUB          !SUBR TO HANDLE KW11-P CLOCK
    :
    :
    I=INTSET("104,6,0,CLKSUB)      !ATTACH ROUTINE
    IF (I,NE,0) GOTO 100         !BRANCH IF ERROR
    :
    :
    END
    SUBROUTINE CLKSUB(ID)
    :
    :
END
```

## 3.37 IPEEK

The IPEEK function returns the contents of the word located at a specified absolute 16-bit memory address. This function can examine device registers or any location in memory.

Form: i = IPEEK (iaddr)

where:

iaddr is the integer specification of the absolute address to be examined. If this argument is not an even value, a trap results (except on LSI-11 or a PDP-11/23)

Function Result:

The function result (i) is set to the value of the word examined.

Example:

```txt
ISWIT = IPEEK("177570) !GET VALUE OF CONSOLE SWITCHES
```

## 3.38 IPEEKB

The IPEEKB subroutine returns the contents of a byte located at a specified absolute byte address. Since this routine operates in a byte mode, the address supplied can be odd or even. This subroutine can examine device registers or any byte in memory. The return is zero extended, that is, the high byte is 0.

Form: i = IPEEKB (iaddr)

where:

iaddr is the integer specification of the absolute byte address to be examined. Unlike the IPEEK subroutine, the IPEEKB subroutine allows odd addresses

Function Result:

The function result (i) is set to the value of the byte examined.

Example:

```txt
IERR = IPEEKB("53) !Get error byte
```

## 3.39 IPOKE

The IPOKE subroutine stores a specified 16-bit integer value into a specified absolute memory location. This subroutine can store values in device registers.

Form: CALL IPOKE (iaddr, ivable)

where:

iaddr is the integer specification of the absolute address to be modified. If this argument is not an even value, a trap results (except on LSI-11 or PDP-11/23)

ivalue is the integer value to be stored in the given address specified by the iaddr argument

Errors:

None.

Example:

The following example displays the value of IVAL in the console display register (this is possible only on certain processors).

CALL IPOKE("177570, IVAL)

To set bit 12 in the JSW without zeroing any other bits in the JSW, use the following procedure.

CALL IPOKE("44,"10000,OR,IPEEK("44))

## 3.40 IPOKEB

The IPOKEB subroutine stores a specified eight-bit integer value into a specified byte location. Since this routine operates in a byte mode, the address supplied can be odd or even. This subroutine can store values in device registers.

Form: CALL IPOKEB (iaddr, ivable)

where:

iaddr is the integer specification of the absolute address to be modified. Unlike the IPOKE subroutine, the IPOKEB subroutine allows odd addresses

ivalue is the integer value to be stored in the given address specified by the iaddr argument

Errors:

None.

Example:

CALL IPOKEB("53,"20) ! Tell KMON unconditionally fatal error

```python
i = old (replaced) value of the fixed offset location.
Example:
    ISIZE = INPUT ("314, 100) ! Change default file size used by ENTER
```

## 3.41 INPUT

The IPUT function replaces the value of a monitor fixed offset. IPUT uses the monitor .PVAL programmed request.

```txt
Form: i = IPUT (ioff,value)
```

where:

ioff         is the offset (from the base of RMON) to be modified
value       is the integer value to replace the current contents of the
                offset location

Function Result:

## 3.42 IQSET

The IQSET function is used to make the RT-11 I/O queue larger — that is, to add available elements to the queue. These elements are allocated out of the free space managed by the FORTRAN system. IQSET cannot be called from a completion or interrupt routine.

Form: i = IQSET (qleng[,area])

where:

qleng is the integer number of elements to be added to the queue. This argument must be positioned so that the USR does not swap over it

area is the space allocated from within the calling program. Under FB and SJ monitors, make sure that the space is outside the USR swapping area. If this argument is not specified, the space for the elements is allocated in the FORTRAN OTS work area

All RT-11 I/O transfers are done through a centralized queue management system. If I/O traffic is very heavy and not enough queue elements are available, the program issuing the I/O requests is suspended until a queue element becomes available. In an FB or XM system, the other job can run while the first program waits for the element. When IQSET is used in a program to be run in the foreground, the FRUN command must be modified to allocate space for the queue elements (see Section 1.2.4.1).

A general rule to follow is that each program should contain one more queue element than the total number of I/O and timer requests that will be active simultaneously. Timing functions such as ITWAIT and MRKT also cause elements to be used and must be considered when allocating queue elements for a program. Note that if synchronous I/O is done (for example, IREADW/IWRITW) and no timing functions are done, no additional queue elements need be allocated. Note also that FORTRAN IV allocates four queue elements by default.

The following subroutines require queue elements:

IRCVD/IRCVDC/IRCVDF/IRCVDW ITIMER
IREAD/IREADC/IREADF/IREADW ITWAIT
ISCHED IUNTIL
ISDAT/ISDATC/ISDATF/ISDATW IWRITE/IWRITC/IWRITF/IWRITW
ISLEEP MRKT
ISPFN/ISPFNC/ISPFNF/ISPFNW MWAIT

For further information on adding elements to the queue, see the .QSET programmed request.

Errors:

i = 0 Normal return.

= 1 Not enough free space is available for the number of queue elements to be added; no allocation was made.

Example:

```txt
IF(IQSET(5),NE,0) STOP 'NOT ENOUGH FREE SPACE FOR QUEUE ELEMENTS'
```

## 3.43 IRAD50

The IRAD50 function converts a specified number of ASCII characters to Radix-50 and returns the number of characters converted. Conversion stops on the first non-Radix-50 character encountered in the input, or when the specified number of ASCII characters have been converted.

Form: n = IRAD50 (icnt,input,output)

where:

n is the integer number of input characters actually connected

icnt is the number of ASCII characters to be converted

input is the area from which input characters are taken

output is the area in which Radix-50 words are stored

Three characters of text are packed into each word of output. The number of output words modified is computed by the expression (in integer words):

(icnt + 2)/3

Thus, if a count of 4 is specified, two words of output are written even if only a one-character input string is given as an argument.

## Function Result:

The integer number of input characters actually converted (n) is returned as the function result.

Example:

REAL\*8 FSPEC
CALL IRAD50(12,'SYOTEMP DAT',FSPEC)
