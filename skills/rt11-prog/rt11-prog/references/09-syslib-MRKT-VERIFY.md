# RT-11 PRM reference: Ch.3 SYSLIB subroutines 3.80 through 3.113

Source: RT-11 Programmer's Reference Manual AA-H378C-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' sometimes reads as ',' (`,MCALL` = `.MCALL`), 'R0' as 'RO', '#' as '\*' or '*'. Verify exact macro expansions against `sysmac_v53.mac`.

Contents:
- 3.80 MRKT (SYSGEN Option in SJ)
- 3.81 MTATCH (Special Feature)
- 3.82 MTDTCH (Special Feature)
- 3.83 MTGET (Special Feature)
- 3.84 MTIN (Special Feature)
- 3.85 MTOUT (Special Feature)
- 3.86 MTPRNT (Special Feature)
- 3.87 MTRCTO (Special Feature)
- 3.88 MTSET (Special Feature)
- 3.89 MTSTAT (Special Feature)
- 3.90 MWAIT (FB and XM Only)
- 3.91 PRINT
- 3.92 PURGE
- 3.93 PUTSTR
- 3.94 R50ASC
- 3.95 RAD50
- 3.96 RCHAIN
- 3.97 RCTRLLO
- 3.98 REPEAT
- 3.99 RESUME (FB and XM Only)
- 3.100 SCCA
- 3.101 SCOMP/ISCOMP
- 3.102 SCOPY
- 3.103 SECNDS
- 3.104 SETCMD
- 3.105 STRPAD
- 3.106 SUBSTR
- 3.107 SUSPND (FB and XM Only)
- 3.108 TIMASC
- 3.109 TIME
- 3.110 TRANSL
- 3.111 TRIM
- 3.112 UNLOCK
- 3.113 VERIFY

---

## 3.80 MRKT (SYSGEN Option in SJ)

The MRKT function schedules an assembly language completion routine to be entered after a specified time interval has elapsed. Support for MRKT in SJ requires timer support.

Form: i = MRKT (id, crtn, time)

where:

id is an integer identification number to be passed to the routine being scheduled

crtn is the name of the assembly language routine to be entered when the time interval elapses. This name must be specified in an EXTERNAL statement in the FORTRAN routine that issues the MRKT call

time is the two-word, internal format time interval; when this interval elapses, the routine is entered. If considered as a two-element INTEGER\*2 array:

time(1) is the high-order time.

time(2) is the low-order time.

## Notes:

1. MRKT requires a queue element, which should be considered when the IQSET function (Section 3.42) is executed.

2. If the system is busy, the time interval that elapses before the completion routine is run can be greater than that requested.

For further information on scheduling completion routines, see the .MRKT programmed request (Section 2.49).

```python
Errors:
    i = 0   Normal return.
      = 1   No queue element was available; unable to schedule request.
Example:
    INTEGER*2 TINT(2)
    EXTERNAL ARTN
    .
    .
    CALL MRKT(4,ARTN,TINT)
```

## 3.81 MTATCH (Special Feature)

The MTATCH subroutine attaches a terminal for exclusive use by the requesting job. This operation must be performed before any job can use a terminal with multiterminal programmed requests.

```m4
Form: i = MTATCH (unit[,addr][,jobnum])
```

where:

unit is the logical unit number (lun) of the terminal

addr is the optional address of an asynchronous terminal status word. Omit this argument if the asynchronous terminal status word is not required by specifying a comma. For example:

```txt
I = MTATCH (unit,,jobnum)
```

jobnum is the job number associated with the terminal if the terminal is not available

= 5 Unit attached by another job (job number returned in jobnum)

= 6 In XM monitor, the optional status word address is not in a valid user virtual address space

## Example:

```txt
C     TEST SYSLIB MULTITERMINAL ROUTINES
        INTEGER*2 UNIT,SBLOK(4),STAT(8),ASW,STRING(41),PROMT(8)
        LOGICAL*1 TEND(11)
        REAL*4 TESTM(9)
        DATA PROMT/'EN','TE','R','ST','RI','NG',''>","200/
        DATA TEND/'*','E','N','D','','T','E','S','T','*',0/
        DATA TESTM/'STAT','ATCH','GET','SET','','',''','','DTCH'/

C     USE MTSTAT TO GET & DISPLAY NO. OF UNITS
        TYPE 106                                      ! ANNOUNCE TEST
        L=1                                       ! L = FUNC CODE
        IF(MTSTAT(STAT),NE,0)GOTO 999                 ! GET MTTY STATUS
5     TYPE 99,STAT(3)                                     ! DISPLAY # UNITS
```

```csv
C GET UNIT # TO TEST
TYPE 100
ACCEPT 101,UNIT
IF(UNIT,EQ,99) STOP 'END OF MULTITERMINAL TEST'! UNIT #89 STOPS TEST
C ATTACH UNIT TO THIS JOB THEN GET TCB STATUS WORDS
TYPE 110
ACCEPT 111,IASW
IF(IASW,EQ,'Y')IER=MTATCH(UNIT,ASW,JOB)
IF(IASW,NE,'Y')IER=MTATCH(UNIT,O,JOB)
L=2
IF(IER)GOTO 999
L=3
IF(MTGET(UNIT,SBLOK(1)).NE,0)GOTO 999
TYPE 102,UNIT,SBLOK
C GET NEW STATUS, PUT IT IN TCB, THEN DISPLAY IT
CALL SETUP(SBLOK,UNIT)
L=4
IF(MTSET(UNIT,SBLOK(1)).NE,0)GOTO 999
TYPE 102,UNIT,SBLOK
C PERFORM TEST - FIRST ECHO INPUT THEN REPEAT IT USING MTIN & MTOUT
20 TYPE 103
TYPE 104
TYPE 105
30 CALL MTIN(UNIT,J)
CALL MTOUT(UNIT,J)
IF(J,NE,10)GOTO 30
CALL MTRCTO(UNIT)
C NOW TEST W/ TTSPC$ BIT ON - ECHO INPUT WITH MTOUT (DON'T REPEAT)
C THEN TURN TTSPC$ BIT OFF...
IF(SBLOK(1),AND,"10000)GOTO 40
SBLOK(1)=SBLOK(1),OR,"10000
IF(MTSET(UNIT,SBLOK(1)),NE,0)GOTO 999
GOTO 30
40 SBLOK(1)=SBLOK(1),AND.,NOT,"10000
IF(MTSET(UNIT,SBLOK(1)),NE,0)GOTO 999
IF(IASW,NE,'Y')GOTO 60
C ASYNCHRONOUS STATUS WORD TEST - "POLL" TERMINAL UNTIL INPUT
C AVAILABLE - ECHO INPUT THEN REPEAT IT ON NEXT LINE
TYPE 109
50 IF(.NOT,ASW,AND,"40000)GOTO 50
55 CALL MTIN(UNIT,J)
CALL MTOUT(UNIT,J)
IF(J,NE,10)GOTO 55
CALL MTRCTO(UNIT)
C TEST MTPRNT BY OUTPUTTING 2 STRINGS, 1 FROM USER & 1 INTERNAL
60 CALL GTLIN(STRING,PROMT)
CALL MTPRNT(UNIT,STRING)
CALL MTPRNT(UNIT,TEND)
C DETACH UNIT FROM JOB AND START OVER
L=9
TYPE 108,UNIT
IF(MTDTCH(UNIT),EQ,0)GOTO 5
```

```txt
Form: i = MTDTCH(unit)
where:
    unit is the logical unit number (lun) of the terminal to be detached
Errors:
    i = 0 Normal return.
    = 2 Invalid unit number; terminal is not attached.
    = 3 Nonexistent unit number.
```

```txt
C ERROR REPORTING
999 TYPE 909,TESTM(L),IER ! ANNOUNCE ERROR
GOTO 5 ! THEN START OVER
99 FORMAT('OTHER ARE',I3,' UNITS ON THIS SYSTEM')
100 FORMAT('\$UNIT * TO BE TESTED?')
101 FORMAT(I2)
102 FORMAT('OUNIT',I3,' STATUS =',408)
103 FORMAT('OGO TO TERMINAL BEING TESTED...ENTER 2 LINES + RET')
104 FORMAT(' 1ST LINE: INPUT WILL BE ECHOED THEN REPEATED')
105 FORMAT(' 2ND LINE: TEST TTSPC$ ON - INPUT ECHOED VIA MTOUT'/)
106 FORMAT('1    SYSLIB MULTITERMINAL ROUTINE TEST PROGRAM')
108 FORMAT(' ABOUT TO DETACH UNIT * ',I2)
109 FORMAT(' TEST ASW - INPUT WILL BE ECHOED, THEN REPEATED'/)
110 FORMAT('\$TEST ASYNCH STATUS WORD FUNCTION?')
111 FORMAT(A1)
909 FORMAT('OMT',A4,' ERROR CODE =',I3)
END
C SUBROUTINE TO GET NEW STATUS WORD VALUES
SUBROUTINE SETUP(SBLOK,UNIT)
INTEGER SBLOK(4),UNIT
TYPE 100 ! PROMPT FOR NEW CONFIG WORD
ACCEPT 101,J ! ACCEPT INPUT
IF(J)SBLOK(1)=J ! UPDATE IF ANY INPUT
TYPE 102 ! ASK FOR FILL CHAR
ACCEPT 101,J ! ACCEPT IT
TYPE 103 ! ASK FOR # OF FILL CHARS
ACCEPT 101,I ! ACCEPT IT TOO
IF(I,OR,J)SBLOK(3)=I*25G+J ! PUT IN PROPER BYTES
5 TYPE 104 ! ASK FOR CARRIAGE WIDTH
ACCEPT 105,I ! ACCEPT IT
IF(I)SBLOK(4)=SBLOK(4)/25G*25G+I ! SET BUT DON'T MESS WITH
RETURN ! STATE WORD ... RETURN
100 FORMAT('\$CONFIG BIT MASK:')
101 FORMAT(OG)
102 FORMAT('\$CHAR REQUIRING FILLER:')
103 FORMAT('\$* OF FILL CHARS:')
104 FORMAT('\$CARRIAGE WIDTH:')
105 FORMAT(I3)
END
```

## 3.82 MTDTCH (Special Feature)

The MTDTCH subroutine is the complement of the MTATCH subroutine. Its function is to detach a terminal from a particular job and make it available for other jobs.

Example:

Refer to the example under MTATCH.

## 3.83 MTGET (Special Feature)

The MTGET subroutine furnishes the user with information about a specific terminal in a multiterminal system. You do not need to do an MTATCH before using MTGET.

Form: i = MTGET (unit,addr[,jobnum])

where:

unit is the unit number of the line and terminal whose status is desired

addr is the four-word area to receive the status information. The area is a four-element INTEGER\*2 array (see the .MTSET programmed request, Section 2.58, for area format)

jobnum is the job number associated with the terminal if the terminal is not available

Status information including bit definitions for the terminal configuration words and the terminal state byte are described in detail under the .MTGET programmed request.

Errors:

i = 0 Normal return.

= 2 Unit not attached.

= 3 Nonexistent unit number.

= 4 Unit attached by another job (job number returned in job-num).

= 6 In XM monitor, the address of the terminal buffer is outside the valid program limits.

Example:

Refer to the example under MTATCH.

## 3.84 MTIN (Special Feature)

The MTIN subroutine transfers characters from a specified terminal to the user program. This subroutine is a multiterminal form of ITTINR. If no characters are available, an error flag is set to indicate an error upon return from the subroutine. If no character count argument is specified, one character is transferred.

Form: i = MTIN (unit,char[,chrcnt ][,ocnt])

where:

unit is the unit number of the terminal

char is the variable to contain the characters read in from the terminal indicated by the unit number

chrcnt is an optional argument that indicates the number of characters to be read

ocnt is an optional argument that indicates the number of characters actually transferred

When a request for a multiple-character transfer is requested, if the optional fourth argument (ocnt) is specified and bit 6 of the M.TSTS word is set, the variable specified as the argument will have a value equal to the actual number of characters transferred upon return from the subroutine.

Errors:

i = 0 Normal return.

= 1 No input available.

= 2 Unit not attached.

= 3 Nonexistent unit number.

Example:

Refer to the example under MTATCH.

## 3.85 MTOUT (Special Feature)

The MTOUT subroutine transfers characters to a specified terminal. This subroutine is a multiterminal form of ITTOUR. If no room is available in the output ring buffer, an error flag is set to indicate an error upon return from the subroutine. If no character count argument is specified, one character is transferred.

Form: i = MTOUT (unit,char[,chrcnt][,ocnt])

where:

unit is the unit number of the terminal

char is the variable or array containing the characters to be output, right-justified in the integer (can be LOGICAL\*1 if desired)

chrcnt is an optional argument that indicates the number of characters to be output

ocnt is an optional argument that indicates the number of characters actually transferred

When a request for a multiple-character transfer is requested, if the optional fourth argument (ocnt) is specified and bit 6 of the M.TSTS word is set, the variable specified as the argument will have a value equal to the actual number of characters transferred upon return from the subroutine.

Errors:

i = 0 Normal return.

= 1 No room in output ring buffer.

= 2 Unit not attached.

= 3 Nonexistent unit number.

= 5 In the XM monitor, the address of the user buffer is outside the valid program limits.

Example:

Refer to the example under MTATCH.

## 3.86 MTPRNT (Special Feature)

The MTPRNT subroutine allows output to be printed at any terminal in a multiterminal environment. This subroutine has the same effect as the PRINT subroutine (Section 3.91).

```txt
Form: i = MTPRNT (unit,string)
```

where:

unit is the unnit number associated with the terminal

string is the character string to be printed. Note that all quoted literals used in FORTRAN subroutine calls are in ASCIZ format, which ends in zero for a CR/LF or a 200 if no action is to be taken

Errors:

i = 0 Normal return.

= 2 Unit not attached.

= 3 Nonexistent unit number.

= 5 In the XM monitor, the address of the character string is outside the valid program limits.

## 3.87 MTRCTO (Special Feature)

The MTRCTO subroutine resets the CTRL/O command typed at the specified terminal in a multiterminal environment. This subroutine has the same effect as the .MTRCTO programmed request (Section 2.57).

```txt
Form: i = MTRCTO(unit)
```

where:

unit is the unit number associated with the terminal

Errors:

i = 0 Normal return.

= 2 Unit not attached.

= 3 Nonexistent unit number.

Example:

Refer to the example under MTATCH.

## 3.88 MTSET (Special Feature)

The MTSET subroutine sets terminal and line characteristics. The set conditions remain in effect until the system is booted or the terminal and line characteristics are reset. See the .MTSET programmed request (Section 2.58) for more details.

## Form: i = MTSET (unit,addr)

where:

unit is the unit number of the line and terminal whose characteristics are to be changed

addr is a four-word area to pass the status information. The area is a four-element INTEGER\*2 array

## Errors:

i = 0 Normal return.

= 2 Unit not attached.

= 3 Nonexistent unit number.

= 6 In the XM monitor, the address of the status block is outside the valid program limits.

Example:

Refer to the example under MTATCH.

## 3.89 MTSTAT (Special Feature)

The MTSTAT subroutine returns multiterminal system status in an eight-word status block.

Form: i = MTSTAT (addr)

where:

addr is the address of an eight-word array where multiterminal status information is returned. The status block contains the following information:

## Contents

addr(1) Offset from the base of the resident monitor to the first Terminal Control Block (TCB).

addr(2) Offset from the base of the resident monitor to the terminal control block of the console terminal for the program.

addr(3) The value (0–16 decimal) of the highest logical unit number (LUN) built into the system.

addr(4) The size of the terminal control block in bytes.

addr(5)-(8) Reserved.

## Errors:

i = 0 Normal return.

= 5 In the XM monitor, the address of the status block is not in valid user address space.

## Example:

Refer to the example under MTATCH.

## 3.90 MWAIT (FB and XM Only)

The MWAIT subroutine suspends main program execution of the current job until all messages sent to or from the other job have been transmitted or received. It provides a means for ensuring that a required message has been processed. MWAIT is used primarily in conjunction with the IRCVD and ISDAT calls, where no action is taken when a message transmission is completed. This subroutine requires a queue element, which should be considered when the IQSET function (Section 3.42) is executed.

Form: CALL MWAIT

Errors:

None.

Example:

Refer to the example under ISDAT, Section 3.51.

## 3.91 PRINT

The PRINT subroutine prints output from a specified string at the console terminal. This routine can be used to print messages from completion routines without using the FORTRAN formatted I/O system. Control returns to the user program after all characters have been placed in the output buffer.

The string to be printed can be terminated with either a null (0) byte or a 200(octal) byte. If the null (ASCIZ) format is used, the output is automatically followed by a carriage return/line feed pair (octal 15 and 12). If a 200 byte terminates the string, no carriage return/line feed pair is generated.

In the FB monitor, a change in the job that is controlling terminal output is indicated by a B> or F>. Any text following the message has been printed by the job indicated (foreground or background) until another B> or F> is printed. When PRINT is used by the foreground job, the message appears immediately, regardless of the state of the background job. Thus, for urgent messages, PRINT should be used rather than ITTOUR.

Form: CALL PRINT (string)

where:

string is the string to be printed. Note that all quoted literals used in FORTRAN subroutine calls are in ASCIZ format, as are all strings produced by the SYSLIB string-handling package (The CONCAT routine can be used to append an octal 200 to an ASCIZ string; see example.)

Errors:

None.

Example:

```txt
CALL PRINT ('THE COFFEE IS READY')

or

BYTE QUESTION(80)
!APPEND BYTE 200
CALL CONCAT('WHAT IS YOUR NAME?,"200,QUESTION)
CALL PRINT(QUESTION) !QUESTION PRINTS WITHOUT CR,LF
```

## 3.92 PURGE

The PURGE subroutine deactivates a channel without performing an ISAVES, CLOSEC, or ICLOSE. Any tentative file currently associated with the channel is not made permanent. This subroutine prevents entered (IENTER or .ENTER) files from becoming permanent directory entries.

Form: CALL PURGE (chan)

where:

chan is the integer specification for the RT-11 channel to be deactivated

Errors:

None.

Example:

Refer to the example under IENTER, Section 3.25.

## 3.93 PUTSTR

The PUTSTR subroutine writes a variable-length character string to a specified FORTRAN logical unit. PUTSTR can be used in main program routines or in completion routines but not in both in the same program at the same time. If PUTSTR is used in a completion routine, it must not be the first I/O operation on the specified logical unit.

Form: CALL PUTSTR (lun,in,char,err)

where:

lun is the integer specification of the FORTRAN logical unit number to which the string is to be written

in is the array containing the string to be written

char is an ASCII character that is appended to the beginning of the string before it is output. If 0, no extra character is output. This character is used primarily for carriage control purposes

err         is a LOGICAL\*1 variable that is .TRUE. for an error condition and .FALSE. for a no-error condition

Errors:

```txt
err = -1    End-of-file for write operation.
        -2    Hardware error for write operation.
```

Example:

```txt
LOGICAL*1 STRNG(81),ERR
:
:
!
!OUTPUT STRING WITH DOUBLE SPACING
CALL PUTSTR(7,STRING,'0',ERR)
```

## 3.94 R50ASC

The R50ASC subroutine converts a specified number of Radix-50 characters to ASCII.

Form: CALL R50ASC (icnt,input,output)

where:

icnt is the integer number of ASCII characters to be produced

input is the area from which words of Radix-50 values to be converted are taken. Note that  $(icnt+2)/3$  words are read for conversion

output is the area into which the ASCII characters are stored

Errors:

If an input word contains illegal Radix-50 codes — that is, if the input word is greater (unsigned) than 174777(octal) — the routine outputs question marks for the value.

Example:

```txt
REAL*8 NAME
LOGICAL*1 OUTP(12)
.
.
.
CALL R50ASC(12,NAME,OUTP)
```

## 3.95 RAD50

The RAD50 function provides a method of encoding RT-11 file descriptors in Radix-50 notation. The RAD50 function converts six ASCII characters from the specified area, returning a REAL\*4 result that is the two-word Radix-50 value.

Form: a = RAD50 (input)

where:

input is the area from which the ASCII input characters are taken

The RAD50 call:

```txt
A = RAD50 (LINE)
```

is exactly equivalent to the IRAD50 call:

```txt
CALL IRAD50 (G, LINE, A)
```

Function Results:

The two-word Radix-50 value is returned as the function result.

## 3.96 RCHAIN

The RCHAIN subroutine allows a program to determine whether it has been chained to and to access variables passed across a chain. If RCHAIN is used, it must be used in the first executable FORTRAN statement in a program.

Form: CALL RCHAIN (flag,var,wcnt)

where:

flag is an integer variable that RCHAIN will set to -1 (true) if the program has been chained to; otherwise, it is 0 (false)

var is the first variable in a sequence of variables with increasing memory addresses to receive the information passed across the chain (see Section 3.2)

wcnt is the number of words to be moved from the chain parameter area to the area specified by var. RCHAIN moves wcnt words into the area beginning at var

Errors:

```txt
None.
Example:
    INTEGER*2 PARMS(50)
    CALL RCHAIN(IFLAG,PARMS,50)
    IF(IFLAG) GOTO 10      !GOTO 10 IF CHAINED TO
    .
    .
    .
```

## 3.97 RCTRLLO

The RCTRLO subroutine resets the effect of any console terminal CTRL/O command that was typed. After an RCTRLO call, any output directed to the console terminal prints until another CTRL/O is typed.

Form: CALL RCTRLO

Errors:

None.

Example:
    CALL RCTRLO
    CALL PRINT ('PRINT UNTIL ANOTHER CTRL/O TYPED')

## 3.98 REPEAT

The REPEAT subroutine concatenates a specified string with itself to produce the indicated number of copies. REPEAT places the resulting string in a specified array.

Form: CALL REPEAT (in,out,i[,len[,err]])

where:

in is the array containing the string to be repeated; it must be terminated with a null byte

out is the array into which the resultant string is placed. This array must be at least one element longer than the value of len, if len is specified. It also must be terminated with a null byte if len is specified

i is the integer number of times to repeat the string

len is the integer number representing the maximum length of the output string

err is the logical error flag set if the output string is truncated to the length specified by len

Input and output strings can specify the same array only if the repeat count (i) is 1 or 0. When the repeat count is 1, this routine is the equivalent of SCOPY; when the repeat count is 0, out is replaced by a null string. The old contents of out are lost when this routine is called.

## Errors:

Error conditions are indicated by err, if specified. If err is given and the output string would have been longer than len characters, then err is set to .TRUE.; otherwise, err is unchanged.

Example:

LOGICAL\*1 SIN(21),SOUT(101)

CALL REPEAT(SIN,SOUT,5)

## 3.99 RESUME (FB and XM Only)

The RESUME subroutine allows a job to resume execution of the main program. A RESUME call is normally issued from an asynchronous FORTRAN routine entered on I/O completion or because of a schedule request (see the SUSPND subroutine, Section 3.107, for more information).

Form: CALL RESUME
Errors:
    None.
Example:
    Refer to the example under SUSPND.

## 3.100 SCCA

The SCCA subroutine provides a CTRL/C intercept to:

1. Inhibit a CTRL/C abort

2. Indicate that a CTRL/C command is active

3. Distinguish between single and double CTRL/C commands

Form: CALL SCCA [(iflag)]

where:

iflag is an integer terminal status word that must be tested and cleared to determine if two CTRL/Cs were typed at the console terminal; the iflag must be an INTEGER\*2 variable (not LOGICAL\*1)

When a CTRL/C is typed, the SCCA subroutine places it in the input ring buffer. While residing in the buffer, the character can be read by the program. The program must test and clear the iflag to determine if two CTRL/C commands were typed consecutively. The iflag is set to non-zero when two CTRL/Cs are typed together. It is the responsibility of the program to abort itself, if appropriate, on an input of CTRL/C from the terminal. The SCCA subroutine with no argument disables the CTRL/C intercept. A CTRL/C from indirect command files is not intercepted by SCCA.

Errors:

None.

Example:

PROGRAM SCCA
C SCCA.FOR SYSLIB TEST FOR SCCA
C
CALL PRINT ('PROGRAM HAS STARTED, TYPE')
IFLAG=0
CALL SCCA (IFLAG)
10 I = ITTINR() !GET A CHARACTER
IF (I .NE, 3) GOTO 10
C A CTRL/C WAS TYPED
CALL PRINT ('A CTRL/C WAS TYPED')
IF (IFLAG .EQ, 0) GOTO 10
CALL PRINT ('A DOUBLE CTRL/C WAS TYPED')
TYPE 19,IFLAG
19 FORMAT (' IFLAG = ',OG,/)
CALL SCCA !DISABLE CTRL/C INTERCEPT
CALL PRINT ('TYPE A CTRL/C TO EXIT')
20 GOTO 20 !LOOP UNTIL CTRL/C TYPED
END

```matlab
Form 1: CALL SCOMP (a,b,i)
        or
    i = ISCOMP (a,b)
Form 2: CALL ISCOMP (a,b,i)
        or
    i = SCOMP (a,b)
```

## 3.101 SCOMP/ISCOMP

The SCOMP routine compares two character strings and returns the integer result of the comparison.

Form 1: CALL SCOMP (a,b,i)

where:

a is the array containing the first string; it must be terminated with a null byte

b is the array containing the second string; it must be terminated with a null byte

i is the integer variable that receives the result of the comparison

The strings are compared from left to right, one character at a time, using the collating sequence specified by the ASCII codes for each character. If the two strings are not equal, the absolute value of variable i (or the result of the function ISCOMP) is the character position of the first inequality found. Strings are terminated by a null (0) character.

If the strings are not the same length, the shorter one is treated as if it were padded on the right with blanks to the length of the other string. A null string argument is equivalent to a string containing only blanks.

Function Results:

```matlab
function Results:
    i <0    If a is less than b.
        =0    If a is equal to b.
        >0    If a is greater than b.
Example:
    LOGICAL*1 INSTR(81)
    :
    :
    CALL GETSTR(5,INSTR,80)
    CALL SCOMP('YES',INSTR,IVAL)
    IF(IVAL,NE,0) GOTO 10      !IF INPUT STRING IS NOT YES GOTO 10
```

## 3.102 SCOPY

The SCOPY routine copies a character string from one array to another. Copying stops either when a null (0) character is encountered or when a specified number of characters have been moved.

Form: CALL SCOPY (in,out[,len[,err]])

where:

in is the array containing the string to be copied; it must be terminated with a null byte if len is not specified, or if the string is shorter than len

out is the array to receive the copied string. This array must be at least one element longer than the value of len, if len is specified. It also must be terminated with a null byte if len is specified

len is the integer number representing the maximum length of the output string. The effect of len is to truncate the output string to a given length

err is a logical variable that receives the error indication if the output string was truncated to the length specified by len

The input (in) and output (out) arguments can specify the same array. The string previously contained in the output array is lost when this subroutine is called.

## Errors:

Error conditions are indicated by err, if specified. If err is given and the output string was truncated to the length specified by len, then err is set to .TRUE.; otherwise, err is unchanged.

## Example:

SCOPY is useful for initializing strings to a constant value, for example:

```sql
LOGICAL*1 STRING(80)
CALL SCOPY('THIS IS THE INITIAL VALUE',STRING)
```

## 3.103 SECNDS

The SECNDS function returns the current system time, in seconds past midnight, minus the value of a specified argument. Thus, SECNDS can be used to calculate elapsed time. The value returned is single-precision floating point (REAL\*4).

Form: a = SECNDS (atime)

where:

atime is a REAL\*4 variable, constant, or expression whose value is subtracted from the current time of day to form the result

Notes:

This function does floating-point arithmetic. Elapsed time can also be calculated by using the GTIM call and the INTEGER\*4 support functions.

Function Result:

The function result (a) is the REAL\*4 value returned.

Errors:

None.

Example:
    C START OF TIMED SEQUENCE
        T1=SECNDS(0,)
    C
    C CODE TO BE TIMED GOES HERE
    C
        DELTA=SECNDS(T1) !DELTA IS ELAPSED TIME

## 3.104 SETCMD

The SETCMD routine allows a user program to pass a command line to the keyboard monitor to be executed after the program exits. This routine can be used in a program running under the SJ monitor, or in a program running in the background under the FB or XM monitor. The command lines are passed to the chain information area (500–777 octal) and stored beginning at location 512(octal). No check is made to determine if the string extends into the stack space. For this reason, the command line should be short and the subroutine call should be made in the main program unit near the end of the program just before completion. When several commands are involved, an indirect command file that contains several command lines should be used.

The monitor commands REENTER, START, and CLOSE are not allowed if the SETCMD feature is used.

Form: CALL SETCMD (string)

where:

string is a keyboard monitor command line in ASCIZ format with no embedded carriage returns or line feeds

Errors:

None.

Example:

```sql
LOGICAL*1 INPUT(134),PROMPT(8)
DATA PROMPT/'P','R','O','M','P','T',''>',"200/
CALL GTLIN (INPUT,PROMPT)
CALL SETCMD (INPUT)
END
```

## NOTE

Set USR NOSWAP, or specify /NOSWAP with the COMPILE, FORTRAN, or EXECUTE command to control the swapping state of the USR. A LOCK would inhibit another job from using the USR.

A STOP or CALL EXIT must also be issued after the SETCMD to cause an exit.

## 3.105 STRPAD

The STRPAD routine pads a character string with rightmost blanks until that string is a specified length. This padding is done in place; the result string is contained in its original array. If the present length of the string is greater than or equal to the specified length, no padding occurs.

Form: CALL STRPAD (a,len[,err])

## where:

a is the array containing the string to be padded. This array must be one element longer than the value of len if len is specified. It will be terminated by a null byte

len is the integer length of the desired result string

err is the logical error flag that is set to .TRUE. if the string specified by a exceeds the value of len in length

## Errors:

Error conditions are indicated by err, if specified. If err is given and the string indicated is longer than len characters, err is set to .TRUE.; otherwise, the value of err is unchanged.

## Example:

This routine is especially useful for preparing strings to be output in A-type FORMAT fields. For example:

```txt
LOGICAL*1 STR(81)
:
.
.
CALL STRPAD(STR,80) !ASSURE 80 VALID CHARACTERS
PRINT 100,(STR(I),I=1,80) !PRINT STRING OF 80 CHARACTERS
100 FORMAT(80A1)
```

## 3.106 SUBSTR

The SUBSTR routine copies a substring from a specified position in a character string. If desired, the substring can then be placed in the same array as the string from which it was taken.

Form: CALL SUBSTR (in,out,i[,len])

## where:

in is the array from which the substring is taken; it is terminated by a null byte

out is the array to contain the substring result. This array must be one element longer than len, if len is specified. It also is terminated by a null byte if len is specified

i is the integer character position in the input string of the first character of the desired substring

len is the integer number of characters representing the maximum length of the substring

If a maximum length (len) is not given, the substring contains all characters to the right of character position i in array in and is not terminated by a null byte. If len is given, the string is copied and terminated with a null byte. If len is equal to zero, out is replaced by the null string. The old contents of array out are lost when this routine is called.

Errors:

None.

## 3.107 SUSPND (FB and XM Only)

The SUSPND subroutine suspends main program execution of the current job and allows only completion routines (for I/O and scheduling requests) to run.

Form: CALL SUSPND

Notes:

1. The monitor maintains a suspension counter for each job. This count is decremented by SUSPND and incremented by RESUME (see Section 3.99). A job will actually be suspended only if this counter is negative. Thus, if a RESUME is issued before a SUSPND, the latter routine will return immediately.

2. A program must issue an equal number of SUSPND and RESUME calls.

3. A SUSPND subroutine call from a completion routine decrements the suspension counter but does not suspend the main program. If a completion routine does a SUSPND, the main program continues until it also issues a SUSPND, at which time it is suspended. Two RESUME calls are then required to proceed.

4. Because SUSPND and RESUME are used to simulate an ITWAIT (see Section 3.61) in the monitor, a RESUME issued from a completion routine and not matched by a previously executed SUSPND can cause the main program execution to continue past a timed wait before the entire time interval has elapsed.

For further information on suspending main program execution of the current job, see the .SPND programmed request (Section 2.89).

Errors:

None.

Example:

```txt
INTEGER IAREA(4)
COMMON /RDBLK/ IBUF(256)
EXTERNAL RDFIN
.
.
.
```

```prolog
IF(IREADF(256,IBUF,IBLK,ICHAN,IAREA,RDFIN).NE.0) GOTO 1000
C GOTO 1000 FOR ANY TYPE OF ERROR
C
C DO OVERLAPPED PROCESSING
.
.
.
CALL SUSPND !SYNCHRONIZE WITH COMPLETION ROUTINE
.
.
.
END
SUBROUTINE RDFIN(IARG1,IARG2)
COMMON /RDBLK/ IBUF(256)
.
.
.
CALL RESUME !CONTINUE MAIN PROGRAM
.
.
.
END
```

## 3.108 TIMASC

The TIMASC subroutine converts a two-word internal format time into an ASCII string of the form:

hh:mm:ss

where:

hh is the two-digit hours indication

mm is the two-digit minutes indication

ss is the two-digit seconds indication

Form: CALL TIMASC (itime,string)

where:

itime is the two-word internal format time to be converted.
itime(1) is the high-order time, itime(2) is the low-order time

strng is the eight-element array to contain the ASCII time

Errors:

None.

Example:

The following example determines the amount of time from the time the program is run until 5 p.m. and prints it.

```txt
INTEGER*4 J1,J2,J3
LOGICAL*1 STRNG(8)
.
.
.
```

```txt
CALL JTIME(17,0,0,0,J1)
CALL GTIM(J2)
CALL JJCVT(J1)
CALL JJCVT(J2)
CALL JSUB(J1,J2,J3)
CALL JJCVT(J3)
CALL TIMASC(J3,STRNG)
TYPE 99,(STRNG(I),I=1,B)
99 FORMAT(' IT IS ',8A1,' TILL 5 P.M.')
.
.
.
```

## 3.109 TIME

The TIME subroutine returns the current system time of day as an eight-character ASCII string of the form:

hh:mm:ss

where:

hh is the two-digit hours indication

mm is the two-digit minutes indication

ss is the two-digit seconds indication

Form: CALL TIME (strng)

where:

string is the eight-element array to receive the ASCII time

Notes:

A 24-hour clock is used (for example, 1:00 p.m. is represented as 13:00:00).

Errors:

None.

Example:

```sql
LOGICAL*1 STRNG(8)
.
.
.
CALL TIME(STRNG)
TYPE 99,(STRNG(I),I=1,8)
99 FORMAT (' IT IS NOW ',8A1)
```

## 3.110 TRANSL

The TRANSL routine performs character translation on a specified string and requires approximately 64(decimal) words on the R6 stack for its execution. This space should be considered when allocating stack space.

Form: CALL TRANSL (in,out,r[,p])

where:

in is the array containing the input string; it is terminated by a null byte

out is the array to receive the translated string; it is not terminated by a null byte

r is the array containing the replacement string; it is terminated by a null byte

p is the array containing the characters in in to be translated; it is terminated by a null byte

The string specified by array out is replaced by the string specified by array in, modified by the character translation process specified by arrays r and p. If any character position in in contains a character that appears in the string specified by p, it is replaced in out by the corresponding character from string r. If the array p is omitted, it is assumed to be the 127 seven-bit ASCII characters arranged in ascending order, beginning with the character whose ASCII code is 001. If strings r and p are given and differ in length, the longer string is truncated to the length of the shorter. If a character appears more than once in string p, only the last occurrence is significant. A character can appear any number of times in string r.

## Errors:

None.

## Examples:

The following example causes the string in array A to be copied to array B. All periods within A become minus signs, and all question marks become exclamation points.

CALL TRANSL(A,B,'-!',',?')

The following is an example of TRANSL being used to format character data.

```txt
LOGICAL*1 STRING(27),RESULT(27),PATRN(27)
C SET UP THE STRING TO BE REFORMATTED
C
CALL SCOPY('THE HORN BLOWS AT MIDNIGHT',STRING)
C SET UP NUMBER-CHARACTER DATA RELATIONSHIP
C
C 000000000111111112222222
C 12345678901234567890123456
C THE HORN BLOWS AT MIDNIGHT
C NOW SET UP PATRN TO CONTAIN THE FOLLOWING PATTERN:
C 16,17,18,19,20,21,22,23,24,25,26,15,1,2,3,4,5,6,7,8,9,10,11,12,13,14,0
C
DO 10 I=16,26
10 PATRN(I-15)=I
PATRN(12)=15
DO 20 I=1,14
20 PATRN(I+12)=I
PATRN(27)=0
```

```txt
C
C THE FOLLOWING CALL TO TRANSL REARRANGES THE CHARACTERS OF
C THE INPUT STRING TO THE ORDER SPECIFIED BY PATRN:
C
CALL TRANSL(PATRN,RESULT,STRING)
C
C RESULT NOW CONTAINS THE STRING 'AT MIDNIGHT THE HORN BLOWS'
C IN GENERAL, THIS METHOD CAN BE USED TO FORMAT INPUT STRINGS
C OF UP TO 127 CHARACTERS. THE RESULTANT STRING WILL BE
C AS LONG AS THE PATTERN STRING (AS IN THE ABOVE EXAMPLE).
```

## 3.111 TRIM

The TRIM routine shortens a specified character string by removing all trailing blanks. A trailing blank is a blank that has no non-blanks to its right. If the specified string contains all blank characters, it is replaced by the null string. If the specified string has no trailing blanks, it is unchanged.

Form: CALL TRIM (a)

where:

a is the array containing the string to be trimmed; it is terminated by a null byte on input and output

Errors:

None.

Example:

```txt
LOGICAL*1 STRING(81)
ACCEPT 100,(STRING(I),I=1,80)
100 FORMAT(80A1)
CALL SCOPY(STRING,STRING,80)      !MAKE ASCIZ
CALL TRIM(STRING)          !TRIM TRAILING BLANKS
```

## 3.112 UNLOCK

The UNLOCK subroutine releases the User Service Routine (USR) from memory if it was placed there by the LOCK routine. If the LOCK required a swap, the UNLOCK loads the user program back into memory. If the USR does not require swapping, the UNLOCK involves no I/O. The USR is always resident in XM.

Form: CALL UNLOCK

Notes:

1. It is important that at least as many UNLOCK calls are given as LOCK calls. If more LOCK calls were done, the USR remains locked in memory. Extra UNLOCK calls are ignored.

2. When running two jobs in the FB system, use the LOCK/UNLOCK pairs only when absolutely necessary. If one job locks the USR, the other job cannot use the USR until it is unlocked.

3. In an FB system, calling the CSI (ICSI) with input coming from the console terminal performs a temporary implicit UNLOCK.

For further information on releasing the USR from memory, see the .LOCK/.UNLOCK programmed requests (Section 2.45).

Errors:

None.

Example:

```txt
C     GET READY TO DO MANY USR OPERATIONS
      CALL LOCK          !DISABLE USR SWAPPING
C     PERFORM THE USR CALLS
      .
      .
      .
C     FREE THE USR
      CALL UNLOCK
      .
      .
      .
```

## 3.113 VERIFY

The VERIFY routine checks that a given string is composed entirely of characters from a second string. If a character does not exist in the string being examined, VERIFY returns the position of the first character in the string being examined that is not in the source string. If all characters exist, VERIFY returns a 0.

Form: CALL VERIFY (a,b,i)

```txt
or
i = IVERIF (a,b)
```

where:

a is the array containing the string to be scanned; it is terminated by a null byte

b is the array containing the string of characters to be accepted in a; it is terminated by a null byte

Function Result:

i = 0 If all characters of $a$ exist in $b$; also if $a$ is a null string.
= n Where $n$ is the character position of the first character in array $a$ that does not appear in array $b$; if $b$ is a null string and $a$ is not, $i$ equals 1.

## Example:

The following example accepts a one- to five-digit unsigned decimal number and returns its value.

```prolog
LOGICAL*1 INSTR(81)
.
.
.
CALL VERIFY(INSTR,'0123456789',I)
IF(I.EQ.1) STOP 'NUMBER MISSING'
IF(I.EQ.0) I=LEN(INSTR)
IF(I.GT.5) STOP 'TOO MANY DIGITS'
NUM=IVALUE(INSTR,I)
.
.
END
```
