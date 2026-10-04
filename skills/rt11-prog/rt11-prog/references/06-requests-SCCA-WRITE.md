# RT-11 PRM reference: Ch.2 programmed requests .SCCA through .WRITE: .SDAT/.SDATC/.SDATW .SDTTM .SETTOP .SFDAT .SFPA SOB .SPCPS .SPFUN .SPND/.RSUM .SRESET .SYNCH .TIMIO .TLOCK .TRPSET .TTYIN/.TTINR .TTYOUT/.TTOUTR .TWAIT .UNMAP .WAIT .WDBBK .WDBDF .WRITE/.WRITC/.WRITW

Source: RT-11 Programmer's Reference Manual AA-H378C-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' sometimes reads as ',' (`,MCALL` = `.MCALL`), 'R0' as 'RO', '#' as '\*' or '*'. Verify exact macro expansions against `sysmac_v53.mac`.

Contents:
- 2.79 .SCCA
- 2.80 .SDAT/.SDATC/.SDATW (FB and XM Only)
- 2.81 .SDTTM
- 2.82 .SERR
- 2.83 .SETTOP
- 2.83.1 .SETTOP in an Extended Memory Environment
- 2.84 .SFDAT
- 2.85 .SFPA (Special Feature)
- 2.86 SOB
- 2.87 .SPCPS (FB and XM SYSGEN Option)
- 2.88 .SPFUN
- 2.89 .SPND/.RSUM (FB and XM Only)
- 2.90 .SRESET
- 2.91 .SYNCH (Device Handler and Interrupt Service Routine Only)
- 2.92 .TIMIO (Device Handler Only)
- 2.93 .TLOCK
- 2.94 .TRPSET
- 2.95 .TTYIN/.TTINR
- 2.96 .TTYOUT/.TTOUTR
- 2.97 .TWAIT (SYSGEN Option for SJ)
- 2.98 .UNLOCK
- 2.99 .UNMAP (XM Only)
- 2.100 .UNPROTECT
- 2.101 .WAIT
- 2.102 .WDBBK (XM Only)
- 2.103 .WDBDF (XM Only)
- 2.104 .WRITE/.WRITC/.WRITW

---

## 2.79 .SCCA

The .SCCA programmed request:

Inhibits a CTRL/C abort

Indicates when a double CTRL/C is initiated at the keyboard

Distinguishes between single and double CTRL/C commands

CTRL/C characters are placed in the input ring buffer and treated as normal control characters without specific system functions. The request requires a terminal status word address (addr) that is used to report consecutive CTRL/C input sequences. Bit 15 of the status word is set when consecutive CTRL/C characters are detected. The program must clear that bit. An .SCCA request with a status word address of 0 disables the intercept and reenables CTRL/C system action.

Normally, the .SCCA request affects only the job currently running. When the program exits, CTRL/C aborts are automatically reenabled. However, if your FB or XM monitor includes global SCCA support enabled through system generation, you can choose to disable CTRL/C aborts throughout the system for as long as you need. Set the argument type to GLOBAL (type = GLOBAL) and set addr to any valid SCCA control word. Thereafter, all CTRL/C aborts will be inhibited until another global .SCCA request is issued to set addr to 0. Only background jobs can issue global .SCCA requests, and these do not affect foreground or system job operation. Global .SCCA requests issued by foreground and system jobs act as local .SCCA requests.

There are three cautions to observe when using .SCCA:

\- The request can cause CTRL/C to appear in the terminal input stream, and the program must provide a way to handle it.

\- The request makes it impossible to terminate program loops from the console; therefore, it should be used only in thoroughly tested, reliable programs.

When .SCCA is in effect and the program enters an infinite loop, the system must be halted and rebootstrapped.

\- CTRL/Cs from indirect command files or indirect control files are not intercepted by the .SCCA.

Macro Call: .SCCA area,addr[,type = GLOBAL]

where:

area is the address of a two-word parameter block

addr is the address of a terminal status word (an address of 0 re- enables double CTRL/C aborts)

type is the mode of SCCA operation. Type is an optional argument that selects either LOCAL (default) or GLOBAL .SCCA

Request format for LOCAL:

```txt
R0 → area: 35 0
addr
```

Request format for GLOBAL:

[figure omitted]

Errors:

None.

Example:

```asm
.MCALL      .SCCA,.EXIT,.PRINT,.GTLIN
START:     ,SCCA     *AREA,#ADDR,TYPE=GLOBAL       #Program to Prompt for a
                   .GTLIN     #NAME,#PROMPT              #name. User cannot CTRL/C
                   .SCCA     *AREA,#0,TYPE=GLOBAL       #out until entering name,
                   .EXIT
AREA:     ,BLKW     4
ADDR:     ,WORD     0
NAME:     ,BLKW     12
PROMPT:    .ASCII   /Enter your name /<200>
                   .END START
```

## 2.80 .SDAT/.SDATC/.SDATW (FB and XM Only)

The .SDAT/.SDATC/.SDATW requests are used with the .RCVD/.RCVDW/.RCVDC calls to allow message transfers between a foreground job and a background job under the FB or XM monitors. .SDAT transfers are similar to .WRITE requests, where data transfer is not to a peripheral but from one job to another. Additional I/O queue elements should be allocated for buffered I/O operations in .SDAT and .SDATC requests (see .QSET).

Message handling in the FB monitor does not check for a word count of zero before queuing a send or receive data request. Since RT-11 distinguishes a send from a receive by complementing the word count, a .SDATW of zero words is treated as a .RCVDW of zero words. Thus, avoid a word count of zero at all times when using a .SDATW request.

Be particularly careful if you use both synchronous (.RCVDW and .SDATW) and asynchronous (.RCVDC and .SDATC) requests in the same program. If you issue a mainline .SDATW while there is a pending .RCVDC, the .SDATW will wait until the .RCVDC is satisfied. If the completion routine for the .RCVDC issues another .RCVDC, the mainline .SDATW will never complete. In general, you should avoid the use of both synchronous and asynchronous message requests in the same program.

.SDAT

Macro Call: .SDAT area,buf,wcnt

where:

area is the address of a five-word EMT argument block

buf is the buffer address of the beginning of the message to be transferred

wcnt is the number of words to transfer

Request Format:

<table><tr><td>25</td><td>0</td></tr><tr><td colspan="2">unused</td></tr><tr><td colspan="2">buf</td></tr><tr><td colspan="2">wcnt</td></tr><tr><td colspan="2">1</td></tr></table>

Errors:

Code

## Explanation

0 No other job exists. (A job exists as long as it is loaded, whether or not it is active.)

Example:

```asm
;+
; .SDAT/.RCVD - This is an example in the use of the .SDAT/.RCVD
; requests. The example is actually two Programs, a Background Job
; which sends messages, and a Foreground Job, which receives them.
;NOTE: Each Program should be assembled and linked separately.
;-

    .TITLE      SDATF.MAC
;+
; Foresround Program...
;-

    .MCALL      .RCVD,.MWAIT,.PRINT,.EXIT

STARTF:   .RCVD      #AREA,#MBUFF,#40.     ;Request a message up to 80 char.
        ;          ,                          ;No error Possible - always a BG
        ;          ,                          ;
        ;          ,                          ;Do some other processing
        .PRINT      #FGJOB         ;like announcing FG active...,
        ;          ,                          ;
        ;          ,                          ;
        .MWAIT                       ;Wait for message to arrive...,
        TST       MBUFF+2         ;Null message?
        BEQ      FEXIT         ;Yes...exit the Program
        .PRINT      *FMSG         ;Announce we got the message...,
        .PRINT      *MBUFF+2         ;and echo it back
        BR      STARTF         ;Loop to set another one
FEXIT:   .EXIT                      ;Exit Program
AREA:   .BLKW      5             ;EMT Argument Block
MBUFF:   .BLKW      41.           ;Buffer - Msg length + 1
        .WORD      0             ;Make sure 80 char message ends ASCIZ
FGJOB:   .ASCIZ      /Hi - FG alive and well and waiting for a message!;
FMSG:   .ASCIZ      /Hey BG - Got your message it reads:/
        .END      STARTF

    .TITLE      STARTB.MAC
;+
; Background Program ... Send a 'null' message to stop both programs
;-
```

STARTB:    CLR     BUFF           ;Clear 1st word
        .GTLIN   #BUFF,\*PROMT       ;Get somethins to send to FG from TTY
        .SDAT     \*AREA,\*BUFF,#40.      ;Send input as message to FG
        BCS      1\$               ;Branch on error - No FG
        .MWAIT                   ;Wait for message to be sent
        TST      BUFF           ;Sent a null message?
        BNE      STARTB       ;No...loop to send another message.
        .EXIT                   ;Yes...exit Program
1\$:    .PRINT   #NOFG          ;No FG !
        .EXIT                   ;Exit Program
AREA:    .BLKW   5              ;EMT Argument Block
BUFF:    .BLKW   40.      ;UP to BO char message
PROMT:    .ASCII   /Enter message to be sent to FG Job/<15><12>/>/<200>
NOFG:    .ASCIZ   /?No FG?/
        .END      STARTB

## .SDATC

Macro Call: .SDATC area,buf,wcnt,crtn

## where:

area is the address of a five-word EMT argument block

buf is the buffer address of the beginning of the message to be transferred

wcnt is the number of words to transfer

crtn is the address of the completion routine to be entered when the message has been transmitted

## Request Format:

<table><tr><td>25</td><td>0</td></tr><tr><td colspan="2">unused</td></tr><tr><td colspan="2">buf</td></tr><tr><td colspan="2">wcnt</td></tr><tr><td colspan="2">crtn</td></tr></table>

## Errors:

## Explanation

0 No other job exists. (A job exists as long as it is loaded, whether or not it is active.)

## Example:

See the example following .SDATW.

## .SDATW

Macro Call: .SDATW area,buf,wcnt

where:

area is the address of a five-word EMT argument block

buf is the buffer address of the beginning of the message to be transferred

wcnt is the number of words to transfer

Request Format:

[figure omitted]

Errors:

Code

## Explanation

0 No other job exists. (A job exists as long as it is loaded, whether or not it is active.)

## Example:

```txt
;
; .SDATW/RCVDW - This is an example in the use of the .SDATW/.RCVDW
; requests. The example consists of two Programs; a Foresround job
; which creates a file and sends a message to a Background Program
; which copies the FG channel and reads a record from the file. Both
; Programs must be assembled and linked separately.
;-
```

```txt
;+
; This is the Foreground Program ...
;-
,MCALL .ENTER,,PRINT,,SDATW,,EXIT,,RCVDW,,CLOSE,,WRITW
```

```asm
STARTF:    MOV     *AREA,R5          ;R5 => EMT argument block
        .ENTER     R5,*,0,*FILE,*,5       ;Create a 5 block file
        .WRITW     R5,*,0,*RECRD,*,256,,,*,4      ;Write a record BG is interested in
        BCS         ENTERR           ;Branch on error
        .SDATW     R5,*,BUFR,*,2       ;Send message with info to BG
        ;          .              ;Do some other processing
        .RCVOW     R5,*,BUFR,*,1       ;When it's time to exit, make sure
        .CLOSE     *0               ;BG is done with the file
        .PRINT     *FEXIT           ;Tell user we're exiting
        .EXIT             ;Exit the program
ENTERR:    .PRINT     *ERMSG          ;Print error message
        .EXIT             ;then exit
FILE:    .RAD50     /DK QUFILE/       ;File spec for ,ENTER
        .RAD50     /TMP/
AREA:    .BLKW     5                ;EMT argument block
BUFR:    .WORD     0                ;Channel #
        .WORD     4                ;Block #
RECRD:    .BLKW     256.           ;File record
ERMSG:    .ASCIZ     /?Enter Error?/       ;Error message text
FEXIT:    .ASCIZ     /FG Job exiting/       ;Exit message
        .END     STARTF
```

```txt
;+
; This is the Background Program ...
;-
    .MCALL     .CHCOPY,,RCVDW,,READW,,EXIT,,PRINT,,SDATW

STARTB:   MOV     *AREA,R5          #R5 => EMT ars block
    ,RCVDW    R5,#MSG,#2          #Wait for message from FG
    BCS      1$               #Branch if no FG
    ,CHCOPY    R5,#0,MSG+2          #Channel * is 1st word of message
    BCS      2$               #Branch if FG channel not open
    ,READW    R5,#0,#BUFF,#25G,,MSG+4 #Read block which is 2nd word of msg
    BCS      3$               #Branch if read error
    ;              .                       #Continue processing...,
    ,SDATW    R5,#MSG,#1          #Tell FG we're thru with file
    ,PRINT     *BEXIT           #Tell user we're thru
    ,EXIT                   #then exit Program
```

```asm
1$:        MOV     *NOJOB,RO      ;RO => No FG error msg
            BR       4$           ;Branch to Print msg
2$:        MOV     *NOCH,RO      ;RO => FG ch not open msg
            BR       4$           ;Branch...
3$:        MOV     #RDERR,RO      ;RO => Read err msg
4$:        .PRINT                  ;Print proper error msg
            .EXIT                   ;then exit,
AREA:    .BLKW     5           ;EMT argument blk
MSG:    .BLKW     3           ;Message buffer
BUFF:    .BLKW     25G,       ;File buffer
BEXIT:    .ASCIZ     /Channel-Record copy successful/
NOJOB:    .ASCIZ     /?No FG Job?/      ;Error messages...
NOCH:    .ASCIZ     /?FG channel not open?/
RDERR:    .ASCIZ     /?Read Error?/
            .END         STARTB
```

## 2.81 .SDTTM

The .SDTTM (Set date and time) request allows your program to set the system date and time.

Macro Call: .SDTTM area,addr

where:

area is the address of a two-word EMT argument block

addr is the address of a three-word block in user memory that contains the new date and time

Request Format:

<table><tr><td rowspan="2">R0 → area:</td><td>40</td><td>0</td></tr><tr><td colspan="2">addr</td></tr></table>

The first word of the three-word parameter block contains the new system date in internal format (see the .DATE programmed request). If this word is -1 (represents an illegal date), the monitor ignores it. Put a -1 in the first word of the parameter block if you want to change only the system time. If the first parameter word is positive, it becomes the new system date. Note that the monitor does no further checking on the date word. To be sure of a valid system date, you must specify a value between 1 and 12(decimal) in the month field (bits 13–10) and a value between 1 and the month length in the day field (bits 9–5). Bits 14 and 15 must be zero.

The second and third words of the parameter block are the new high-order and low-order time values, respectively. This value is the double-precision number of ticks since midnight. If the high-order time word is negative, the monitor ignores the new time. Put a negative value in the second word of the parameter block if you want to change only the system date. If the second parameter word is positive, the new time becomes the system time. The monitor does no further checking on the new time. To be sure of a valid system time, you must specify a legal number of ticks for the system line frequency. For a 60 Hz clock, the high-order time may not be larger than 117(octal), and if it is equal to 117, the low-order time may not be equal to or larger than 15000(octal). For a 50 Hz clock, the high-order time may not be larger than 101(octal), and if it is equal to 101, the low-order time may not be equal to or larger than 165400(octal).

Changing the date and/or time has no effect on any outstanding mark time or timed wait requests.

Errors:

Example:

|  | .MCALL | .SDTTM,.PRINT,.EXIT,.GTIM |  |
| --- | --- | --- | --- |
|  | .GLOBL | STD,DALITE |  |
| STD: | COM | HR | Switch to STD time... |
|  | NEG | HR+2 | Make one hr in clock ticks |
| DALITE: | .GTIM | *AREA,#TIME | Get the current time |
|  | CALL | JADD | Adjust +/- 1 hour |
|  | .SDTTM | *AREA,#NEWDT | Set the new system time |
|  | .GTIM | *AREA,#TIME | Force date rollover (if any) |
|  | RETURN |  | Return to caller |
| NEWDT: | .WORD | -1 | .SDTTM arguments - No new date |
| TIME: | .WORD | 0,0 | New time |
| HR: | .WORD | 3 | One hour in clock ticks (60 cycle |
|  |  |  | clock!) |
|  | .WORD | 45700 |  |
| AREA: | .WORD | 0,0 | EMT Argument Block |
| JADD: |  |  | Double Precision integer add |
|  | MOV | *HR,R4 | R4 => Low order of System time + 2 |
|  | MOV | *AREA,R3 | R3 => Low order of One hour + 2 |
|  | MOV | *HR,R1 | R1 => Low order of new time |
|  | MOV | -(R4),R2 | Put low order of 1st operand in R2 |
|  | ADD | -(R3),R2 | Add in low order of operand #2 |
|  | MOV | -(R4),R5 | Put high order of operand #1 in R5 |
|  | ADC | R5 | Add in carry (no overflow possible!) |
|  | ADD | -(R3),R5 | Add in high order of operand #2 |
|  |  |  | (ditto!) |
|  | MOV | R2,-(R1) | Store result where wanted |
|  | MOV | R5,-(R1) |  |
|  | RETURN |  | Return to caller |
|  | .END |  |  |

## 2.82 .SERR

See .HERR/.SERR (Section 2.42).

## 2.83 .SETTOP

The .SETTOP request specifies a new address as a program's upper limit. The monitor determines whether this address is legal and whether or not a memory swap is necessary when the USR is required. For instance, if the program specified an upper limit below the start address of USR (normally specified in offset 266 in the resident monitor), no swapping is necessary, as the program does not overlay the USR. If .SETTOP from the background specifies a high limit greater than the address of the USR and a SET USR

NOSWAP command has not been given, a memory swap is required. The use of .SETTOP in an extended memory environment is described at the end of this section.

Careful use of the .SETTOP request provides a significant improvement in the performance of your program. An approach that is used by several of the system-supplied programs is as follows:

1. A .SETTOP is done to the high limit of the code in a program before buffers or work areas are allocated. If the program is aborted, minimal writing of the user program to the swap blocks (SWAP.SYS) occurs. However, the program is allowed to be restarted successfully.

2. A user command line is now read through .CSISPC or .GTLIN. An appropriate USR swap address is set in location 46. Successive .DSTATUS, .SETTOP, and .FETCH requests are performed to load necessary device handlers. This attempts to keep the USR resident as long as possible during the procedure.

3. Buffers and work areas are allocated as needed with appropriate .SETTOP requests being issued to account for their size. Frequently, a .SETTOP of #-2 is performed to request all available memory to be given to the program. This can be more useful than keeping the USR resident.

4. If the process has a well-defined closing phase, another .SETTOP can be issued to cause the USR to become resident again to close files (the user should remember to set location 46 to zero if this is done, so that the USR again swaps in the normal area). On return from .SETTOP, both R0 and the word in location 50(octal) contain the highest memory address allocated for use. If the job requested an address higher than the highest address legal for the requesting job, the address returned is the highest legal address for the job rather than the requested address.

When doing a final exit from a program, the monitor writes the program to the file SWAP.SYS and then reads in the KMON. A .SETTOP #0 at exit time prevents the monitor from swapping out the program to the swap blocks (SWAP.SYS) before reading in the KMON, thus saving time. This procedure is especially useful on a diskette system when indirect command files are used to run a sequence of programs. The monitor command SET EXIT NOSWAP also disables program swapping.

Macro Call: .SETTOP addr

where:

addr is the address of the highest word of the area desired (the last word the program will modify, not the first word it leaves untouched)

## Notes:

1. A program should never do a .SETTOP and assume that its new upper limit is the address it requested. It must always examine the returned contents of R0 or location 50 to determine its actual high address.

2. It is imperative that the value returned in R0 or location 50 be used as the absolute upper limit. If this value is exceeded, vital parts of the monitor can be destroyed.

Errors:

None.

Example:

```asm
,TITLE SETTOP.MAC
;+
; .SETTOP - This is an example in the use of the .SETTOP request, The
; example tries to obtain as much memory as possible using the .SETTOP
; request, which will force the USR into a swapping mode. The .LOCK request
; will bring the USR into memory (over the high 2K of our little program!)
; and force it to remain there until an .UNLOCK is issued.
;-
.MCALL ,LOCK,.UNLOCK,.LOOKUP
.MCALL ,SETTOP,.PRINT,.EXIT
SYSPTR=54          ;Pointer to beginnings of RMON
START: .SETTOP @*SYSPTR      ;Try to allocate all of memory (up to
                                ;IMON)
,LOCK                      ;brins USR into memory
,LOOKUP *AREA,#0,#FILE1   ;LOOKUP a file on channel 0
BCC    1$           ;Branch if successful
2$: .PRINT *LMSG       ;Print Error Message
,EXIT                      ;then exit program
1$: .PRINT *F1FND      ;Announce our success
MOV     *AREA,RO      ;RO => EMT Argument Block
INC     @RO         ;Increment low byte of 1st arg (chan *)
MOV     *FILE2,2(RO)   ;Fill in pointer to new filespec
,LOOKUP                      ;Do the .LOOKUP from filled in arg block
                                ;Pointed to by RO,
BCS    2$           ;Branch on error
.PRINT *F2FND      ;Say we found it
.UNLOCK        ,       ;now release the USR
,EXIT                      ;and exit program
AREA: .BLKW 3          ;EMT Argument Block
FILE1: .RAD50 /DK/          ;A File we're sure to find
,RAD50 /PIP /
,RAD50 /SAV/
FILE2: .RAD50 /DK/          ;Another file we might find
,RAD50 /TECO /
,RAD50 /SAV/
LMSG: .ASCIZ /?Error on .LOOKUP?/ ;Error message
F1FND: .ASCIZ /...Found PIP.SAV/
F2FND: .ASCIZ /...Found TECO.SAV/
.EVEN
.END     START
```

## 2.83.1 .SETTOP in an Extended Memory Environment

You can enable the extended memory feature of the .SETTOP programmed request with the linker /V option or the LINK command with the /XM option (see Chapter 11 in the RT-11 System Utilities Manual or Chapter 4 of the RT-11 System User's Guide). The RT-11 Software Support Manual describes in detail the .SETTOP request in an extended memory environment. The .SETTOP request operates in privileged and virtual jobs as follows:

## Privileged Jobs

1. A .SETTOP that requests an upper limit below the virtual high limit of the program will always return the virtual high limit of the program. The virtual high limit is the last address in the highest PAR that the program uses. In this case, a value can never be returned below the job's virtual high limit.

2. A .SETTOP that requests a job's upper limit above the program's virtual high limit will return the highest available address as follows:

a. Either the address requested or SYSLOW-2 (last used address, SYSLOW is next address available) is returned, whichever is lower. SYSLOW is defined as the start of the USR in the XM monitor.

b. If the program's virtual high limit is greater than SYSLOW (the user program maps over the monitor or USR), the virtual high limit of the program will always be returned.

## Virtual Jobs

1. As in privileged jobs, a .SETTOP request can never get less than the virtual high limit of the job.

2. If a .SETTOP requests an upper limit greater than the virtual high limit, the following occurs:

a. If the virtual high limit equals 177776, this value is returned since this is the address limit in virtual memory. Otherwise, a new region and window will be created. The size of the region and window will be determined by the argument specified to the .SETTOP or by the amount of extended memory that is available, whichever value is smaller. The .SETTOP argument rounded to a 32-word boundary minus the high .LIMIT value for the program equals the size of the region and window (see the LINK chapter of the RT-11 System Utilities Manual and the RT-11 Software Support Manual for a description of the .LIMIT directive in extended memory). If there are no region control blocks, window control blocks, or extended memory available, the program's virtual high limit is returned. The .SETTOP request uses one of the region and window control blocks allocated to the user, thus one less block is available to the program if the linker /V option is used.

b. Additional .SETTOP requests can only remap the original window created by the first .SETTOP. Thus, additional requests will return an address no higher than that established by the first request and no lower than the program virtual high limit. An additional .SETTOP request whose argument is higher than the first request will cause the entire first window to be mapped. An additional .SETTOP request whose argument specifies a value below the virtual high limit eliminates the region and window. If another .SETTOP request then follows, it may create a new region and window.

## 2.84 .SFDAT

The .SFDAT programmed request allows a program to set or modify the creation date in a file's directory entry. Dates on protected as well as unprotected files can be changed.

Macro Call: .SFDAT area, chan, dblk, date

where:

area is the address of a three-word EMT argument block

chan is a channel number in the range 0–376

dblk is the address of a four-word block containing a filespec in Radix-50

date is the address of the new date, in RT-11 format If this argument is #0, the system date is used; bits 14 and 15 are always set to 0, but no other check is made for an illegal date

Request Format:

<table><tr><td rowspan="3">R0 → area:</td><td>42</td><td>chan</td></tr><tr><td colspan="2">dblk</td></tr><tr><td colspan="2">date</td></tr></table>

Errors:

Code Explanation

0 Channel in use

1 File not found

2 Invalid operation (device not file structured)

Example:

Refer to the example for the .FPROT request.

## 2.85 .SFPA (Special Feature)

The .SFPA request allows users with floating-point hardware to set trap addresses to be entered when a floating-point exception occurs. If no user trap address is specified and a floating-point (FP) exception occurs, a ?MON-F-FPU trap occurs, and the job is aborted.

```txt
Macro Call: .SFPA area,addr
```

where:

area is the address of a two-word EMT argument block

addr is the address of the routine to be entered when an exception occurs

Request Format:

<table><tr><td rowspan="2">R0 → area:</td><td>30</td><td>0</td></tr><tr><td colspan="2">addr</td></tr></table>

## Notes:

1. The user trap routine must save and restore any registers it uses. It exits with an RTI instruction.

2. If the address argument is #0, user floating-point routines are disabled and the fatal ?MON-F-FPU trap error is produced by any further traps.

3. In the FB environment, an address value of #1 indicates that the FP registers should be switched when a context switch occurs, but no user traps are enabled. This allows both jobs to use the FP unit. An address of #1 to the SJ monitor is equivalent to an address of #0.

4. When the user routine is activated, it is necessary to re-execute an .SFPA request, as the monitor disables user traps as soon as one is serviced. It does this to prevent a possible infinite loop from being set up by repeated floating-point exceptions.

5. If the FP11 is being used, the instruction STST-(SP) is executed by the monitor before entering the user's trap routine. Thus, the trap routine must pop the two status words off the stack before doing an RTI. The program can tell if FP hardware is available by examining the configuration word in the monitor.

Errors:

```asm
None.
Example:
    .TITLE  SFPA.MAC
+;
; .SFPA - This is an example in the use of the ,SFPA request, This
; example is a skeleton Program which demonstrates how to set up a
; Floating Point trap routine, and the minimum action that routine
; must take before dismissing the error trap.
;-
        .MCALL   .SFPA,.EXIT
        SYSPTR     = 54          #Loc of beginnings of Monitor
        CONFIG     = 300          #Offset to Monitor configuration wd
        FP11      = 100          #FPU Present bit
START:    ;          ,                  #Mainline Program...
        ;          .
        ;          .
```

```asm
.SFPA      *AREA,#FPTRAP       ;Set up FPU error trap
;               .
;               .                       ;continue mainline Program
;               .
,EXIT                     ;Exit Program

FPTRAP:
;               .                       ;FPU exception routine
;               .
;               .
;               .
CKFPU:    MOV     @*SYSPTR,RO       ;RO => base of RMON
BIT       #FP11,CONFIG(RO)   ;Check for FPU hdwe
BEQ       1$                 ;Branch if none
CMP         (SP)+,(SP)+        ;Must POP status ress off stack!
1$:    RTI                      ;Before returning from interrupt
.END       START
```

## 2.86 SOB

The SOB macro simulates the SOB instruction (subtract one and branch if not equal) by generating the code:

DEC register
BNE location

You can use the SOB macro on all processors, but it is especially useful for processors that do not have the hardware SOB instruction. If you are running on a processor that supports the SOB instruction, simply eliminate the MACRO call to SOB (.MCALL SOB), and the SOB instruction executes. Note that SOB is not preceded by a dot (.).

The SOB macro has the following syntax:

SOB reg,addr

where:

reg is the register whose contents will be decremented by 1

addr is the location to branch to if the register contents do not equal 0 after the decrement

In the following example, register R0 is decremented by 1 and then tested. If the contents do not equal 0, the program branches to the label HERE.

SOB RQ,HERE

Note: The SOB instruction does not change any condition codes. The SOB macro can change the N, Z, and V (but not the C) condition codes.

## 2.87 .SPCPS (FB and XM SYSGEN Option)

The .SPCPS (save/set mainline PC and PS) request allows a program's completion routine to change the flow of control of the mainline code. .SPCPS saves the mainline code PC and PS, and changes the mainline PC to a new value. If the mainline code is performing a monitor request, the monitor allows that request to finish before doing any rerouting. The actual rerouting is deferred until the mainline code is about to run. Therefore, the .SPCPS request returns an error if it is reissued before an earlier request has been honored. Furthermore, the data saved in the user block is not valid until the new mainline code is running.

The .SPCPS request is a system generation feature and is available only in FB and XM. If a program issues this call under SJ or under a monitor not generated for the call, no action is taken and no error is returned.

Macro Call: .SPCPS area,addr

where:

area is the address of a two-word EMT argument block

addr is the address of a three-word block in user memory that contains the new mainline PC, and that is to contain the old mainline PC and PS

## Request Format:

```txt
R0 → area: 41 0
addr
```

Errors:

## Explanation

0 The program issued the .SPCPS call from the mainline code rather than a completion routine.

1 A previous .SPCPS request is outstanding.

When the program issues the .SPCPS request, the monitor saves the old mainline PS in the third word of the three-word block and the old mainline PC in the second word of the block. The monitor then changes the mainline PC to the contents of the first word of the block.

Example:

```csv
,TITLE SPCPS.MAC
,ENABL LC
+:
; .SPCPS - This is an example in the use of the ,SPCPS request. In this
; example .SPCPS is used to reroute the mainline code after an I/O
; error or EOF is detected by a completion routine.
;-
.MCALL ,READC,,WRITC,,CLOSE,,PRINT,,CSIGEN,,EXIT,,WAIT,,SRESET
,MCALL ,SPCPS
ERRBYT = 52 ;Error Byte location in SYSCOM
,ENABL LSB
START: .CSIGEN *DSPACE,#DEFEXT ;Use CSIGEN to get handlers, files
CALL IOXFER ;Start I/O
.PRINT #MESSG ;Now simulate other mainline Process
1$: DEC R5 ; (Kill some time)
BR 1$
FINI: .CLOSE *0 ;EOF > 0 = End of File
MOV *DONE,RO ;RO → We're done message
BR GBYE ;Merge to exit Program
WERR: MOV *WRERR,RO ;Set up error messages here...
BR GBYE
RERR: MOV *RDERR,RO
```

<table><tr><td rowspan="3">GBYE:</td><td>.PRINT</td><td></td><td>;Print message</td></tr><tr><td>.SRESET</td><td></td><td>;Dismiss fetched handlers</td></tr><tr><td>.EXIT</td><td></td><td>;Exit Program</td></tr><tr><td rowspan="2">WRDONE:</td><td>.WAIT</td><td>*0</td><td>;Write compl rtne...write successful?</td></tr><tr><td>BCS</td><td>3$</td><td>;Branch if not...</td></tr><tr><td rowspan="4">IOXFER:</td><td>.READC</td><td>*AREA, *3,,, *6$</td><td>;Queue up a read</td></tr><tr><td>BCC</td><td>5$</td><td>;Branch if ok...</td></tr><tr><td>TSTB</td><td>@*ERRBYT</td><td>;Error - is it EOF?</td></tr><tr><td>BEQ</td><td>4$</td><td>;Branch if yes</td></tr><tr><td rowspan="2">2$:</td><td>MOV</td><td>*RERR, SBLOK</td><td>;Move Read err rtne addr to ars block</td></tr><tr><td>BR</td><td>4$</td><td>;Merse...</td></tr><tr><td>3$:</td><td>MOV</td><td>*WERR, SBLOK</td><td>;Move Write err rtne addr to ars block</td></tr><tr><td rowspan="5">4$:</td><td>TSTB</td><td>SPCALL</td><td>;Already done a ,SPCPS?</td></tr><tr><td>BNE</td><td>5$</td><td>;Yes...don&#x27;t do another</td></tr><tr><td>.SPCPS</td><td>*AREA, *SBLOK</td><td>;De-rail mainline code</td></tr><tr><td>INCB</td><td>SPCALL</td><td>;Flag we&#x27;ve done this</td></tr><tr><td>BCS</td><td>7$</td><td>;Ooops! Something&#x27;s amiss!</td></tr><tr><td>5$:</td><td>RETURN</td><td></td><td>;Leave completion code</td></tr><tr><td rowspan="6">6$:</td><td>.WAIT</td><td>*3</td><td>;Completion routine #2 - was read ok?</td></tr><tr><td>BCS</td><td>2$</td><td>;Branch if not</td></tr><tr><td>.WRITC</td><td>*AREA, *0,,, *WRDONE</td><td>;Queue up a write...</td></tr><tr><td>BCS</td><td>3$</td><td>;Branch if error</td></tr><tr><td>INC</td><td>BLOK</td><td>;Bump block # for next read</td></tr><tr><td>RETURN</td><td></td><td>;Leave Completion code...</td></tr><tr><td rowspan="2">7$:</td><td>.PRINT</td><td>*SPERR</td><td>;Print ,SPCPS failed message</td></tr><tr><td>RETURN</td><td></td><td></td></tr><tr><td>AREA::</td><td>.WORD</td><td>0</td><td>;EMT Area block</td></tr><tr><td rowspan="4">BLOK:</td><td>.WORD</td><td>0</td><td>;Block #.</td></tr><tr><td>.WORD</td><td>BUFF</td><td>;Buffer addr &amp; word count</td></tr><tr><td>.WORD</td><td>256.</td><td>;already fixed in block...</td></tr><tr><td>.WORD</td><td>0</td><td>;Completion routine addr</td></tr><tr><td>SBLOK:</td><td>.WORD</td><td>FINI, 0, 0</td><td>;, SPCPS Argument block (FINI default)</td></tr><tr><td>BUFF:</td><td>.BLKW</td><td>256.</td><td>;I/O buffer</td></tr><tr><td>DEFEXT:</td><td>.WORD</td><td>0, 0, 0, 0</td><td>;No default extensions for CSIGEN</td></tr><tr><td rowspan="3">SPCALL:</td><td>.BYTE</td><td>0</td><td>;, SPCPS called flag in case I/O error</td></tr><tr><td></td><td></td><td>;(compl rtne gets sched, regardless!)</td></tr><tr><td>.NLIST</td><td>BEX</td><td></td></tr><tr><td>DONE:</td><td>.ASCIZ</td><td>/I-O Transfer Complete/</td><td>;Messages...</td></tr><tr><td>MESSG:</td><td>.ASCIZ</td><td colspan="2">/&lt; Simulating Mainline Processing &gt;/</td></tr><tr><td>WRERR:</td><td>.ASCIZ</td><td colspan="2">/?Write Error?/</td></tr><tr><td>RDERR:</td><td>.ASCIZ</td><td colspan="2">/?, Read Error?/</td></tr><tr><td rowspan="2">SPERR:</td><td>.ASCIZ</td><td colspan="2">/?, SPCPS Error?/</td></tr><tr><td>.EVEN</td><td></td><td></td></tr><tr><td rowspan="2">DSPACE</td><td>= .</td><td></td><td>;Handlers may be loaded starting here</td></tr><tr><td>.END</td><td>START</td><td></td></tr></table>

## 2.88 .SPFUN

This request is used with certain device handlers to do device dependent functions, such as rewind and backspace. It can be used with diskettes and some disks to allow reading and writing of absolute sectors. This request can determine the size of a volume mounted in a particular device unit for RX02 diskettes, RD50/RD51 disks, RK06/RK07 disks, RL01/RL02 disks, MSCP disks, and logical disks.

Macro Call: .SPFUN area,chan,func,buf,wcnt,blk[,crtn]

where:

area is the address of a six-word EMT argument block

chan is a channel number in the range 0 to 376(octal)

func is the numerical code of the function to be performed; these codes must be negative

buf is the buffer address; this parameter must be set to zero if no buffer is required

wcnt is defined in terms of the device handler associated with the specified channel and in terms of the specified special function code

blk is also defined in terms of the device handler associated with the specified channel and in terms of the specified special function code

crtn is the entry point of a completion routine. If left blank, 0 is automatically inserted. This value is the same as for .READ, .READC, and .READW.

$$
0 = \text { wait   I / O (.READW) }
$$

1 = real time (.READ)

Value >500 = completion routine

Request Format:

<table><tr><td>32</td><td>chan</td></tr><tr><td colspan="2">blk</td></tr><tr><td colspan="2">buf</td></tr><tr><td colspan="2">wcnt</td></tr><tr><td>func</td><td>377</td></tr><tr><td colspan="2">crtn</td></tr></table>

The chan, blk, and wcnt arguments are the same as those defined for .READ/.WRITE requests. They are only required when doing a .WRITE with extended record gap to magnetic tape. If the crtn argument is left blank, the requested operation completes before control returns to the user program. Specifying crtn as #1 is similar to executing a .READ or .WRITE in that the function is initiated and returns immediately to the user program. Use a .WAIT on the channel to make sure that the operation is completed. The crtn argument is a completion routine address to be entered when the operation is complete.

The available functions and function codes for magtape and cassette are as follows:

| Function | MM, MS, MT | CT |
| --- | --- | --- |
| Forward to last file |  | 377 |
| Forward to last block |  | 376 |
| Forward to next file |  | 375 |
| Forward to next block |  | 374 |
| Rewind to load point | 373 | 373 |
| Write file gap |  | 372 |
| Write EOF | 377 |  |
| Forward one block | 376 |  |
| Backspace one block | 375 |  |
| Write with extended file gap | 374 |  |
| Off-line rewind | 372 |  |
| Write | 371 |  |
| Read | 370 |  |
| Stream at 100 ips (MS only) | 367 |  |

The available functions and function codes for diskettes, RK06/RK07 disks, RL01 and RL02 disks, the logical disk handler, MSCP disks, and RD50/RD51 disks are as follows:

| Function | DX | DZ | DM | DY | DL | LD | DU | DW |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Read | 377 | 377 | 377 | 377 | 377 |  |  | 377 |
| Write | 376 | 376 | 376 | 376 | 376 |  |  | 376 |
| Write with deleted data mark | 375 |  |  | 375 |  |  |  |  |
| Force a read by the handler of the bad block replacement table from block 1 of the disk |  |  | 374 |  | 374 |  |  |  |
| Return device size | 373 |  | 373 | 373 | 373 | 373 | 373 | 373 |
| Read/write translation table |  |  |  |  |  | 372 | 372 |  |
| Direct MSCP access |  |  |  |  |  |  | 371 |  |

To use the .SPFUN request, the handler must be in memory and a channel must be associated with a file via a non-file-structured .LOOKUP request.

A .SPFUN request to write absolute blocks on RX01/RX02 diskettes should not write anything in track 0 if you want to use DUP or the COPY/DEVICE command to back up the volume. DUP does not copy data in track 0. Also, you should be careful to specify a valid buffer address and word count. The monitor checks that the buf argument is in the job area, but it does not check buf + wcnt. If you use the .SPFUN request, and the device handler for that device does not support special functions or the particular .SPFUN code used, the call simply returns to the program without reporting an error.

When using special functions 376 and 377 with DW or DZ:

wcnt is the track to be read or written.

blk is the sector.

buf is the address of a 256-word buffer.

SPFUN 376 and 377 with DZ handler do not interleave sectors. RX50 diskettes, handled by DZ, have 80 tracks. SPFUN 376 and 377 wrap to track 0 after track 79.

When using special function 373 with DW:

chan is the channel on which DW was opened with .LOOKUP.

buf is the address of a one-word buffer in which the size of the volume will be returned: 9727(decimal) blocks for an RD50, 19519(decimal) blocks for an RD51.

blk is not used and should be set to 0.

For the RK06/07 handler (DM), special function codes 377 and 376 require the buffer size to be one word larger than necessary for the data. The first word of the buffer contains the error information returned as a result of the .SPFUN request. The data transferred as a result of the read or write request is found in the second and following words of the buffer. The error codes and information are as follows:

Code Meaning

100000 The I/O operation is successful.

100200 A bad block was detected (BSE error).

100001 An ECC error is corrected.

100002 An error recovered on retry.

100004 An error recovered through an offset retry.

100010 An error recovered after recalibration.

1774xx An error did not recover.

Other device-specific information is included in the RT-11 Software Support Manual.

Errors:

## Code Explanation

0 Attempt to read or write past end-of-file, or invalid function value.

1 Hard error occurred on channel.

2 Channel is not open.

Additional qualifying information for these errors is returned in the first two words of the blk argument status block. This information is given in Chapter 10 of the RT-11 Software Support Manual.

Example:

```csv
,TITLE SPFUN.MAC
;+
; .SPFUN - This is an example in the use of the .SPFUN request. The
; example rewinds a cassette and writes out a 256-word buffer and
; then a file sap,
;-
.MCALL .FETCH,.LOOKUP,.SPFUN,.WRITW
.MCALL .EXIT,.PRINT,.WAIT,.CLOSE
START: .FETCH *HSPC,#CT ;Fetch the CT Handler
BCS 1$ ;Branch if failed
.LOOKUP *AREA,#4,#CT ;Open channel 4 for output
BCS 2$ ;Branch if error (should never hap-
;pen!)
.SPFUN *AREA,#4,#373,#0 ;Rewind to BOT using Synchronous I/O
BCS 3$ ;Branch on error
.WRITW *AREA,#4,#BUFF,#256.,BLK ;Write one block
BCS 4$ ;Branch on error
.SPFUN *AREA,#4,#372,#0,,#1 ;Write a file sap with Asynch I/O
.PRINT *DONE ;Announce that we're done
.WAIT #4 ;Wait for file sap operation to finish
.CLOSE #4 ;Close the file
.EXIT ;then exit the program
1$: MOV *FERR,RO ;Process errors here...
BR 5$
```

```asm
2$:      MOV     #LKERR,RO
        BR       5$
3$:      MOV     #SPERR,RO
        BR       5$
4$:      MOV     #WERR,RO
5$:      .PRINT                  ;Print error message
        .EXIT                   ;then exit program

AREA:      .WORD     0               ;EMT Argument block
BLK:      .WORD     0,0,0,0,0
CT:      .RAD50    /CT /           ;Cassette Device Descriptor
        .WORD     0,0,0               ;Null filespec
BUFF:      .BLKW     25G.            ;Output buffer
DONE:      .ASCIZ     /All done !/          ;Message text...,
FERR:      .ASCIZ     /?,FETCH Error?/
LKERR:      .ASCIZ     /?,LOOKUP Error?/
SPERR:      .ASCIZ     /?Special Function Error?/
WERR:      .ASCIZ     /?Write Error?/
        .EVEN
        HSPC = ,                    ;Handler can load in here...,
        .END     START
```

## 2.89 .SPND/.RSUM (FB and XM Only)

The .SPND/.RSUM requests control execution of a job's mainline code (the code that is not executing as a result of a completion routine). .SPND suspends the mainline and allows only completion routines (for I/O and mark time requests) to run. .RSUM from one of the completion routines resumes the mainline code. These functions enable a program to wait for a particular I/O or mark time request by suspending the mainline and having the selected event's completion routine issue a .RSUM. This differs from the .WAIT request, which suspends the mainline until all I/O operations on a specific channel have completed.

Macro Calls: .SPND
.RSUM

Request Formats:

$$
\begin{array}{l l} \text {(.SPND)} & \mathrm{R0} = \\ \text {(.RSUM)} & \mathrm{R0} = \end{array} \boxed { \begin{array}{c c} 1 & 0 \\ \hline 2 & 0 \end{array} }
$$

## Notes:

1. The monitor maintains a suspension counter for each job. This counter is decremented by .SPND and incremented by .RSUM. A job is suspended only if this counter is negative. Thus, if a .RSUM is issued before a .SPND, the latter request returns immediately.

2. A program must issue an equal number of .SPND and .RSUM requests.

3. A .RSUM request from the mainline code increments the suspension counter.

4. A .SPND request from a completion routine decrements the suspension counter, but does not suspend the mainline. If a completion routine does a .SPND, the mainline continues until it also issues a .SPND, at which time it is suspended and requires two .RSUMs to proceed.

5. Since a .TWAIT is simulated in the monitor using suspend and resume, a .RSUM issued from a completion routine without a matching .SPND can cause the mainline to continue past a timed wait before the entire time interval has elapsed.

6. A .SPND or .RSUM, like most other programmed requests, can be issued from within a user-written interrupt service routine if the .INTEN/.SYNCH sequence is followed. All notes referring to .SPND/.RSUM from a completion routine also apply to this case.

Errors:

None.

Example:

```asm
,TITLE SPND,MAC
+.
; .SPND/.RSUM- This is an example in the use of the .SPND/.RSUM requests,
; The example is a simulation of a mainline Foresground Program which is
; currently suspended waiting for a message from the Background, but which
; needs to close a file (Perhaps opened by a .ENTER ?) before aborting
; from CTRL-C action. A completion routine periodically inspects the CTRL-C
; status word and resumes the mainline if double CTRL-C is entered.
; NOTE: This example MUST be run as a FG job under an FB monitor.
;-
.MCALL SCCA,.RCVDC,.EXIT,.PRINT,.MRKT
.MCALL .QSET,.SPND,.RSUM
START: .QSET #QELEM,#1 ;Allocate another Q-Element
.SCCA #MAREA,*SCCA ;Inhibit ^C^C action by monitor
1$: CALL CWATCH ;Start "watchdog" completion rtne
.RCVDC #MAREA,*MBUFF,#40,,*MESG ;Look for a message
; ; ;No errors - there's always BG
; ; ;Other processing here...
; ; ;
.PRINT #SLEEP ;Announce we're going to suspend
.SPND ;Suspend to wait for message
TST SCCA ;We've been ,RSUMed...^C^C hit???
BNE CLOSE ;Branch if yes
; ; ;otherwise assume message came in...
; <Process message here>
; .
BR 1$ ;Loop...
CWATCH: TST SCCA ;Check if ^C^C entered...
BEQ MARK ;Branch if no
MESG: .RSUM ;Yes...wake up the mainline
RETURN ;then leave completion code
MARK: .MRKT #CAREA,*TIME,*CWATCH,#1 ;Schedule to run again in 10 sec.
RETURN ;then leave completion code
CLOSE: .PRINT *ABORT ;Announce we're aborting
; <Output file(s) closed here> ;Proceed with "orderly" abort
; .
.EXIT ;Exit the Program
QELEM: .BLKW 7 ;Extra Q-Element
MBUFF: .BLKW 41, ;Message buffer
MAREA: .BLKW 5 ;EMT Argument blocks
CAREA: .BLKW 4 ;
TIME: .WORD 0,600, ;Time out in 10 seconds
SCCA: .WORD 0 ;^C^C Status word
ABORT: .ASCIZ /?! Abort Acknowledged...Closing Output File(s) !?/
SLEEP: .ASCIZ /! Mainline Suspending !/
.END START
```

2-134 Programmed Request Description and Examples

## 2.90 .SRESET

The .SRESET (software reset) request:

1. Cancels any messages sent by the job.

2. Waits for all job I/O to complete, which includes waiting for all completion routines to run.

3. Dismisses any device handlers that were brought into memory via .FETCH calls. Handlers loaded via the keyboard monitor LOAD command remain resident, as does the system device handler.

4. Purges any currently open files. Files opened for output with .ENTER are never made permanent.

5. Reverts to using only 16(decimal) I/O channels. Any channels defined with .CDFN are discarded. A .CDFN must be reissued to open more than 16 channels after a .SRESET is performed.

6. Clears the job's .SPND/.RSUM counter.

7. Resets the I/O queue to one element. A .QSET request must be reissued to allocate extra queue elements.

8. Cancels all outstanding .MRKT requests.

Macro Call: .SRESET

Errors:

None.

Example:

```csv
,TITLE SRESET.MAC
;+
; .SRESET - This is an example in the use of the .SRESET request.
; The example renames a file according to filespecs entered using the
; .CSISPC request.
;-
,MCALL ,RENAME,,PRINT,,EXIT
,MCALL ,CSISPC,,FETCH,,SRESET
ERRBYT = 52 ;Error byte location
START: ,CSISPC #FILESP,#DEFEXT ;Use .CSISPC to set file specs
,FETCH #HANLOD,#FILESP ;Get Handler from outspec
BCS 2\$ ;Branch if failed
MOV *FILESP,R2 ;R2 => Outspec
MOV *FILESP+46,R3 ;R3 => Inspec
MOV @R2,FILESP+36 ;Copy device spec to inspec
,REPT 4 ;Copy outspec behind inspec
MOV (R2)+,(R3)+ ;for .RENAME,..
,ENDR
,RENAME #AREA,#0,#FILESP+36 ;Rename input file
BCC 1\$ ;Operation successful
DECB @@ERRBYT ;Make error code -1,O or +1
BEQ 3\$ ;Branch if File-Not-Found
MOV *ILLOP,RO ;Illegal operation-set up mss
BR 5\$ ;Branch to report error
```

1\$:          .SRESET
        .EXIT
2\$:          MOV         #NOHAN,RO
        BR           5\$
3\$:          MOV         #NOFIL,RO
5\$:          .PRINT
        BR           1\$
AREA:       .BLKW      5
DEFEXT:       .WORD     0,0,0,0
NOFIL:       .ASCIZ    /?File not found?/
ILLOP:       .ASCIZ    /?Illegal Operation?/
NOHAN:       .ASCIZ    /?.FETCH Failed?/
        .EVEN
FILESP:       .BLKW      39.
HANLOD     = .
        .END     START

## 2.91 .SYNCH (Device Handler and Interrupt Service Routine Only)

This macro call enables your program to issue programmed requests from within an interrupt service routine. Code following the .SYNCH call runs at priority level 0 as a completion routine in the issuing job's context. Programmed requests issued from interrupt routines are not supported by the system and should not be performed unless a .SYNCH is used. .SYNCH, like .INTEN, is not an EMT monitor request, but rather a subroutine call to the monitor.

Macro Call: .SYNCH area[,pic]

where:

area is the address of a seven-word block that you must set aside for use by .SYNCH. This argument, area, represents a special seven-word block used by .SYNCH as a queue element. This is not the same as the regular area argument used by many other programmed requests. The user must not confuse the two; he should set up a unique seven-word block specifically for the .SYNCH request. The seven-word block appears as:

Word 1 RT-11 maintains this word; its contents should not be altered by the user

2 The current job's number. This must be set up by the user program. It can be obtained by a .GTJB call or from the I/O queue element in a device handler

3 Unused

4 Unused

5 R0 argument. When a successful return is made from .SYNCH, R0 contains this argument

6 Must be -1

7 Must be 0

pic is an optional argument that, if non-blank, causes the .SYNCH macro to produce position-independent code for use by device drivers

Note:

.SYNCH assumes that the user has not pushed anything on the stack between the .INTEN and .SYNCH calls. This rule must be observed for proper operation.

## Errors:

The monitor returns to the location immediately following the .SYNCH if the .SYNCH was rejected. The routine is still unable to issue programmed requests, and R4 and R5 are available for use. An error is returned if another .SYNCH that specified the same seven-word block is still pending.

## NOTE

The monitor dismisses the interrupt without returning to the .SYNCH routine if one of the following conditions occur:

1. You specified an illegal job number.

2. The job number does not exist (for example, you specify 2, and there is no foreground job).

3. The job is exited or terminated with an .EXIT programmed request.

You can find out if the block is in use by:

1. Checking location Q.COMP (offset 14 octal). If this location contains a zero, the block is available.

2. Performing a .SYNCH call. If the block is busy, an error return will be performed.

Normal return is to the word after the error return. At this point, the routine is in user state and is thus allowed to issue programmed requests. R0 contains the argument that was in word 5 of the block. R0 and R1 are free for use without having to be saved. R4 and R5 are not free, and do not contain the same information they contained before the .SYNCH request. A long time can elapse before the program returns from a .SYNCH request since all interrupts must be serviced before the main program can continue. Exit from the routine should be done via an RTS PC.

## Example:

## .TITLE SYNCH.MAC

;+
; .SYNCH - This is an example of the .SYNCH request.
; The example is a skeleton of a Program which could input data
; from the outside world by means of an in-line interrupt service routine,
; buffer it until a whole block's worth has been input, then use
; a .WRITE request to store the data on an RT-11 device.
;-

[figure omitted]

## 2.92 .TIMIO (Device Handler Only)

The .TIMIO macro issues the device time-out call in the handler I/O initiation section. This request schedules a completion routine to run after the specified time interval has elapsed. The completion routine runs in the context of the job indicated in the timer block. In XM systems, the completion routine executes with kernel mapping, since it is still a part of the interrupt service routine. (See the RT-11 Software Support Manual for more information about interrupt service routines and the XM monitor.) As usual with completion routines, R0 and R1 are available for use. When the completion routine is entered, R0 contains the sequence number of the request that timed out.

Macro Call: .TIMIO tbk,hi,lo

## where:

tbk is the address of the timer block, a seven-word pseudo timer queue element. (The timer block format is shown in Table 2-1 under the .CTIMIO request.) You must set up the address of the completion routine in the seventh word of the timer block in a position-independent manner

hi is the high-order word of a two-word time interval

lo is the low-order word of a two-word time interval

Example:

```asm
.TITLE TIMIO.MAC
+:
; TIMIO.MAC - This is an example of a simple, RT-11 device driver,
; to illustrate the use of the .TIMIO/.CTIMIO requests. The timeout
; completion routine will be entered if a character hasn't been
; successfully transmitted in 1/10 sec (approx. 110 baud). In this
; example the completion routine takes no explicit action; the fact
; that the timeout occurred is enough to be considered a "hard" error.
;-
.MCALL .DRBEG,.DRAST,.DRFIN,.DREND,.QELDF,.TIMIO,.CTIMIO
.IIF NDF MMG\$T, MMG\$T=0 ;Define these in case not
.IIF NDF ERL\$G, ERL\$G=0 ;assembled with SYSCND.MAC
.IIF NDF TIM\$IT, TIM\$IT=0
.IIF NDF SP\$VEC, SP\$VEC=304 ;Define default vector
.IIF NDF SP\$CSR, SP\$CSR=176504 ;Define default CSR addr
.IIF NDF SP\$PRI, SP\$PRI=4 ;Define default device priority
IOERR = 1 ;Hard I/O error bit definition
SPSTS = 20000 ;Device Status = Write only
SPSIZ = 0 ;Device Size = 0 (Char device)
TIME = 6 ;Timeout interval = 1/10 sec
COD = 377 ;Device i.d. code
.QELDF ;Use .QELDF to define Q-Elem offsets
.DRBEG SP,SP\$VEC,SPSIZ,SPSTS ;Begin driver code with .DRBEG
MOV SPCQE,R4 ;R4 => Current Q-Element
ASL Q\$WCNT(R4) ;Make word count byte count
BCC SPERR ;A read from a write/only device?
BEQ SPDUN ;Zero word count...just exit
SPRET: MOV PC,R5 ;Calculate PIC address
ADD *SPTOUT-.,R5 ;completion routine
MOV R5,TBLK+14 ;Move it to argument block
.TIMIO TBLK,0,TIME ;Schedule a marktime
BIS *100,@#SP\$CSR ;Enable DL-11 interrupt
RETURN ;Return to monitor
; INTERRUPT SERVICE ROUTINE
.DRAST SP,SP\$PRI ;Use .DRAST to define Int Svc Sect.
MOV SPCQE,R4 ;R4 => Q-Element
TST @*SP\$CSR ;Error?
BMI SPRET ;Yes...'hans' until ready
TSTB @*SP\$CSR ;Is device ready?
BPL SPRET ;No...so wait 'till it is
.CTIMIO TBLK ;Cancel completion routine
BCS SPERR ;Too late - it timed out!
MOVB @Q\$BUFF(R4),@*SP\$CSR+2 ;Xfer byte from buffer to DL-11
INC Q\$BUFF(R4) ;Bump the buffer pointer
INC Q\$WCNT(R4) ;and the word count (it's negative!)
```

```txt
BEQ SPDUN #Branch if done
BR SPRET #Go wait 'till char xmitted
SPTOUT: ; . #Timeout completion routine
; . #In this example, it does nothing,
; . #In real life it may want to try
RETURN #to take some corrective action...
SPERR: BIS *IOERR,@Q$CSW(R4) #Set error bit in CSW
SPDUN: .DRFIN SP #Use .DRFIN to return to Monitor
TBLK: .WORD 0,TIME,0,0,177000+COD #TIMIO argument block
.DREND SP #Use .DREND to end code
.END
```

## 2.93 .TLOCK

The .TLOCK (test lock) request is used in an FB environment to attempt to gain ownership of the USR. It is similar to .LOCK in that, if successful, the user job returns with the USR in memory (it is identical to .LOCK in the SJ monitor). However, if a job attempts to .LOCK the USR while another job is using it, the requesting job is suspended until the USR is free. With .TLOCK, if the USR is not available, control returns immediately with the C bit set to indicate the .LOCK request failed.

Macro Call: .TLOCK

Request Format:

[figure omitted]

Errors:

0 USR is already in use by another job.

Example:

```asm
.TITLE TLOCK.MAC
+.
.TLOCK - This is an example in the use of the .TLOCK request.
In this example, the user Program needs the USR for a sub-Job it is
executins. If it fails to set the USR it "suspend" that sub-Job and
runs another sub-Job (that perhaps doesn't need the USR for execution).
This type of procedure is useful to schedule several sub-Jobs within
a single background or foreground Program.
-:
.MCALL .TLOCK,.LOOKUP,.UNLOCK,.EXIT,.PRINT
START:
.TLOCK .Begin Mainline Program
BCS SUSPND Try to set the USR for 1st "Job"
LOOKUP #AREA,#4,#FILE Failed...branch to "suspend" 1st Job
BCS LKERR Succeeded...Proceed with 1st Job
; . Branch if error on LOOKUP
.PRINT #J1MSG 1st Job involves file Processing...do it!
.UNLOCK $Tell user we executed...
TSTB J2SW $1st job finished...release USR
BNE 1$ Check if we ran Job #2 while USR busy
CALL JOB2 $Yup - we did
1$: .EXIT ?Nope - do it now
```

<table><tr><td rowspan="6">SUSPND:</td><td></td><td></td><td>\&quot;Suspend&quot; current &quot;Job&quot;</td></tr><tr><td>TSTB</td><td>J2SW</td><td>Did we already run Job #2</td></tr><tr><td>BNE</td><td>START</td><td>Yes - don&#x27;t do it again</td></tr><tr><td>JSR</td><td>PC,JOB2</td><td>&quot;Run&quot; other &quot;Job&quot;</td></tr><tr><td>INC</td><td>J2SW</td><td>Set switch that says we ran Job #2</td></tr><tr><td>BR</td><td>START</td><td>When it&#x27;s finished, try 1st job again</td></tr><tr><td>AREA:</td><td>,BLKW</td><td>5</td><td>EMT argument block</td></tr><tr><td rowspan="3">FILE:</td><td>,RAD50</td><td>/DK/</td><td>File spec for Job #1</td></tr><tr><td>,RAD50</td><td>/QUFILE/</td><td>;</td></tr><tr><td>,RAD50</td><td>/TMP/</td><td>;</td></tr><tr><td rowspan="2">LKERR:</td><td>,PRINT</td><td>*LKMSG</td><td>Error on ,LOOKUP - Report it!</td></tr><tr><td>,EXIT</td><td></td><td></td></tr><tr><td>LKMSG:</td><td>,ASCIZ</td><td>/?File Not Found?/</td><td></td></tr><tr><td>J1MSG:</td><td>,ASCIZ</td><td>/Job #1 Executed/</td><td></td></tr><tr><td>J2MSG:</td><td>,ASCIZ</td><td>/Job #2 Executed/</td><td></td></tr><tr><td rowspan="2">J2SW:</td><td>,BYTE</td><td>0</td><td>Switch to control Job #2 execution</td></tr><tr><td>,EVEN</td><td></td><td></td></tr><tr><td rowspan="3">JOB2:</td><td>,PRINT</td><td>#J2MSG</td><td>2nd &quot;Job&quot; - Doesn&#x27;t need USR</td></tr><tr><td>RTS</td><td>PC</td><td>Return when done</td></tr><tr><td>.END</td><td>START</td><td></td></tr></table>

## 2.94 .TRPSET

.TRPSET allows the user job to intercept traps to 4 and 10 instead of having the job aborted with a ?MON-F-Trap to 4 or ?MON-F-Trap to 10 message. If .TRPSET is in effect when an error trap occurs, the user-specified routine is entered. The status of the carry bit on entry to the routine determines which trap occurred: carry bit clear indicates a trap to 4; carry bit set indicates a trap to 10. The user routine should exit with an RTI instruction. Traps to 4 can also be caused by user stack overflow on some processors (check your processor handbook). These traps are not intercepted by the .TRPSET request, but they do cause job abort and a printout of the message ?MON-F-Stack overflow in the SJ monitor or ?MON-F-Trap to 4 in the FB and XM monitors (see the RT-11 System Message Manual).

Macro Call: .TRPSET area,addr

where:

area is the address of a two-word EMT argument block

addr is the address of the user's trap routine. If an address of 0 is specified, trap interception is disabled

Request Format:

[figure omitted]

Notes:

1. Reissue a .TRPSET request whenever an error trap occurs and the user routine is entered. The monitor disables user trap interception prior to entering the user trap routine. Thus, if a trap should occur from within the user's trap routine, an error message is generated and the job is aborted. The last operation the user routine should perform before an RTI is to reissue the .TRPSET request.

2. In the XM monitor, traps dispatched to a user program by .TRPSET execute in user mode. They appear as interrupts of the user program by a synchronous trap operation. Programs that intercept error traps by trying to steal the trap vectors must be carefully designed to handle two cases accurately: programs that are virtual jobs and programs that are privileged jobs.

If the program is a virtual job, the stolen vector is in user virtual space that is not mapped to kernel vector space. The proper method is to use .TRPSET; otherwise interception attempts fail and the monitor continues to handle traps to 4 and 10.

If the program is a privileged job, it is mapped to the kernel vector page. The user can steal the error trap vectors from the monitor, but the benefits of doing so must be carefully evaluated in each case. Trap routines run in the mapping mode specified by bits 14 and 15 of the trap vector PS word. With both bits set to 0, kernel mode is set. However, kernel mapping is not always equivalent to user mapping, particularly when extended memory is being used. With both bits 14 and 15 of the PS set to 1, user mode is set, and the trap routine executes in user mapping.

## Errors:

None.

Example:

## .TITLE TRPSET.MAC

```asm
;+
; .TRPSET - This is an example in the use of the .TRPSET request.
; In this example a user trap routine is set, then deliberate
; traps to 4 & 10 are caused (not very practical but it demonstrates
; that .TRPSET really works!).  
;-
    .MCALL        .TRPSET,,EXIT,,PRINT
    DIVZ = 67                      #Divide by zero - illegal instruction
START:                     #Begin example
    .TRPSET     #AREA,#TRPLOC      #Set up a trap routine to handle traps
    DIVZ                          #to 4 & 10... 
    TST             @*166666          #Illegal instruction - Trap to 10
    .EXIT                          #Address non-existent memory - Trap to 4
    TRPLOC:                     #Exit Program
    BCS            1$                 #Trap routine
    .PRINT       #C bit set = TRAP 10
    BR           2$                 #Report Trap to 4
1$:      .PRINT     #Report trap to 10
    .TRPSET     #Reset trap routine address
2$:      RTI                          #Return to offending code
AREA:      .WORD     0,0              #EMT argument block
TRP4:      .ASCIZ     /?Trap to 4?/   #Error messages...
TRP10:      .ASCIZ     /?Trap to 10?/
    .END         START
```

## 2.95 .TTYIN/.TTINR

The requests .TTYIN and .TTINR transfer a character from the console terminal to the user program. The character thus obtained appears right-justified (even byte) in R0. The user can cause the characters to be returned in R0 only, or in R0 and other locations.

The expansion of .TTYIN is:

EMT 340

BCS.-2

The expansion of .TTINR is:

EMT 340

If no characters or lines are available when an EMT 340 is executed, return is made with the carry bit set. The implication of these calls is that .TTYIN causes a tight loop waiting for a character/line to appear, while the user can either wait or continue processing using .TTINR.

If the carry bit is set when execution of the .TTINR request is completed, it indicates that no character was available; the user has not yet typed a valid line. Under the FB or XM monitor and under an SJ monitor with multiterminal support, .TTINR does not return the carry bit set unless bit 6 of the job status word (JSW) was on when the request was issued.

There are two modes of doing console terminal input. The choice is governed by bit 12 of the job status word. If bit 12 is 0, normal I/O is performed. In this mode, the following conditions apply:

1. The monitor echoes all characters typed.

2. CTRL/U and the DELETE key perform line deletion and character deletion, respectively.

3. A carriage return, line feed, CTRL/Z, or CTRL/C must be struck before characters on the current line are available to the program. When one of these is typed, characters on the line typed are passed one by one to the user program.

If bit 12 is 1, the console is in special mode. The effects are:

1. The monitor does not echo characters typed except for CTRL/C and CTRL/O.

2. CTRL/U and the DELETE key do not perform special functions.

3. Characters are immediately available to the program.

In special mode, the user program must echo the characters received. However, CTRL/C and CTRL/O are acted on by the monitor in the usual way. Bit 12 in the JSW must be set by the user program. This bit is cleared when the program terminates.

Regardless of the setting of bit 12, when a carriage return is entered, both carriage return and line feed characters are passed to the program; if bit 12 is 0, these characters will be echoed.

Lowercase conversion is determined by the setting of bit 14 in the JSW. If bit 14 is 0, lowercase characters are converted to uppercase before being echoed (if bit 12 is 0) and passed to a program; if bit 14 is 1, lowercase characters are echoed (if bit 12 is 0) and passed as received. Bit 14 is cleared when the program terminates.

CTRL/F and CTRL/B (and CTRL/X in system job monitors) are not affected by the setting of bit 12. The monitor always acts on these characters (unless the SET TT NOFB command is issued).

CTRL/S and CTRL/Q are intercepted by the monitor (unless, under the FB or XM monitor, the SET TT NOPAGE command is issued).

Under the FB or XM monitor, if a terminal input request is made and no character is available, job execution is blocked until a character is ready. This is true for both .TTYIN and .TTINR, and for both normal and special modes. If a program requires execution to continue and the carry bit to be returned, it must set bit 6 of the Job Status Word before the .TTINR request. Bit 6 is cleared when a program terminates.

If the single-line editor has been enabled by the commands SET SL ON and SET SL TTYIN, and if bits 4 and 12 of the JSW are 0, input from a .TTYIN or .TTINR request will be edited by SL. If either bit 4 or bit 12 is set, SL will not edit input. If SL is editing input, the state of bit 6 (inhibit TT wait) is ignored and a .TTINR request will not return until an edited line is available.

## NOTE

The .TTYIN request does not get characters from indirect files. If this function is desired, the .GTLIN request must be used.

Macro Calls: .TTYIN char
.TTINR

## where:

char is the location where the character in R0 is to be stored. If char is specified, the character is in both R0 and the address represented by char. If char is not specified, the character is in R0

## Errors:

Code Explanation

0 No characters available in ring buffer.

## Example:

Refer to the example following the description of .TTYOUT/.TTOUTR.

## 2.96 .TTYOUT/.TTOUTR

The requests .TTYOUT and .TTOUTR cause a character to be transmitted to the console terminal. The difference between the two requests, as in the .TTYIN/.TTINR requests, is that if there is no room for the character in the monitor's buffer, the .TTYOUT request waits for room before proceeding, while the .TTOUTR does not wait for room and the character is not output.

If the carry bit is set when execution of the .TTOUTR request is completed, it indicates that there is no room in the buffer and that no character was output. Under the FB or XM monitor, .TTOUTR normally does not return the carry bit set. Instead, the job is blocked until room is available in the output buffer. If a job requires execution to continue and the carry bit to be returned, it must turn on bit 6 of the Job Status Word before issuing the request.

The .TTINR and .TTOUTR requests have been supplied to help those users who want to continue rather than suspend program execution until a console operation is complete. With these modes of I/O, if a no-character or no-room condition occurs, the user program can continue processing and try the operation again at a later time.

## NOTE

If a foreground job leaves bit 6 set in the Job Status Word, any further foreground .TTYIN or .TTYOUT requests cause the system to lock out the background until a character is available. Note also that each job in the foreground/background environment has its own Job Status Word, and therefore can be in different terminal modes independently of the other job.

Macro Call: .TTYOUT char
.TTOUTR

## where:

char is the location containing the character to be loaded in R0 and printed. If not specified, the character in R0 is printed. Upon return from the request, R0 still contains the character

## Errors:

Code Explanation

0 Output ring buffer full.

## Example:

.TITLE TTYIN.MAC

; .TTYIN / .TTYOUT - This is an example in the use of the .TTYIN
; & .TTYOUT requests. The example accepts a line of input from the
; console keyboard, then echoes it on the terminal. Usings .TTYIN &
; .TTYOUT requests illustrate Synchronous terminal I/O; i.e., the
; Monitor retains control (the Job is blocked) until the requests
; are satisfied,

<table><tr><td></td><td>.MCALL</td><td>.TTYIN,,TTYOUT</td><td></td></tr><tr><td rowspan="2">START:</td><td>MOV</td><td>*BUFFER,R1</td><td>;R1 =&gt; Character buffer</td></tr><tr><td>CLR</td><td>R2</td><td>;Clear character count</td></tr><tr><td rowspan="5">INLOOP:</td><td>.TTYIN</td><td>(R1)+</td><td>;Read char into buffer</td></tr><tr><td>INC</td><td>R2</td><td>;Bump count</td></tr><tr><td>CMPB</td><td>#12,RO</td><td>;Was last char a LF ?</td></tr><tr><td>BNE</td><td>INLOOP</td><td>;No...set next character</td></tr><tr><td>MOV</td><td>*BUFFER,R1</td><td>;Yes...point R1 to beginnings of buffer</td></tr><tr><td rowspan="4">OUTLOOP:</td><td>.TTYOUT</td><td>(R1)+</td><td>;Print a character</td></tr><tr><td>DEC</td><td>R2</td><td>;Decrease count...</td></tr><tr><td>BEQ</td><td>START</td><td>;Done if count = 0</td></tr><tr><td>BR</td><td>OUTLOOP</td><td>;Loop to print another character</td></tr><tr><td rowspan="3">BUFFER:</td><td>.BLKW</td><td>64.</td><td>;Character buffer...</td></tr><tr><td>.END</td><td>START</td><td></td></tr><tr><td colspan="3">.TITLE TTINR.MAC</td></tr><tr><td colspan="4">+</td></tr><tr><td colspan="4">; .TTINR / ,TTOUTR - This is an example in the use of the .TTINR &amp;</td></tr><tr><td colspan="4">; .TTOUTR requests. Like TTYIN.MAC, this example accepts lines of</td></tr><tr><td colspan="4">; input from the console keyboard, then echoes it on the terminal.</td></tr><tr><td colspan="4">; But rather than waiting for the user to type something at &#x27;INLOOP&#x27;</td></tr><tr><td colspan="4">; or wait for the output buffer to have available space at &#x27;OUTLOOP&#x27;,</td></tr><tr><td colspan="4">; the routine has been recoded using .TTINR and .TTOUTR to allow</td></tr><tr><td colspan="4">; other processing to be carried out if a wait condition is reached.</td></tr><tr><td colspan="4">;-</td></tr><tr><td rowspan="3"></td><td>.MCALL</td><td>.TTYIN,,TTYOUT</td><td></td></tr><tr><td>.MCALL</td><td>.TTINR,,TTOUTR,,EXIT</td><td></td></tr><tr><td colspan="2">JSW = 44</td><td>;Location of Job Status Word in SYSCOM</td></tr><tr><td rowspan="4">START:</td><td>MOV</td><td>*BUFFER,R1</td><td>;Point R1 to buffer</td></tr><tr><td>CLR</td><td>R2</td><td>;Clear character count</td></tr><tr><td>BIS</td><td>*100,@JSW</td><td>;Set bit #6 in JSW so ,TTINR/.TTOUTR will</td></tr><tr><td></td><td></td><td>;return C bit set if no char/no room...</td></tr><tr><td rowspan="2">INLOOP:</td><td>.TTINR</td><td></td><td>;Get char from terminal</td></tr><tr><td>BCS</td><td>NOCHAR</td><td>;None available</td></tr><tr><td rowspan="5">CHRIN:</td><td>MOVB</td><td>RO,(R1)+</td><td>;Put char in buffer</td></tr><tr><td>INC</td><td>R2</td><td>;Increase count</td></tr><tr><td>CMPB</td><td>RO,#12</td><td>;Was last char = LF?</td></tr><tr><td>BNE</td><td>INLOOP</td><td>;No...set next char</td></tr><tr><td>MOV</td><td>*BUFFER,R1</td><td>;Yes...Point R1 to beginnings of buffer</td></tr><tr><td rowspan="3">OUTLOOP:</td><td>MOVB</td><td>(R1),RO</td><td>;Put char in RO</td></tr><tr><td>.TTOUTR</td><td></td><td>;Try to print it</td></tr><tr><td>BCS</td><td>NOROOM</td><td>;Branch if no room in output buffer</td></tr><tr><td rowspan="4">CHROUT:</td><td>DEC</td><td>R2</td><td>;Decrease count</td></tr><tr><td>BEQ</td><td>START</td><td>;Done if count=0</td></tr><tr><td>INC</td><td>R1</td><td>;Dump buffer pointer</td></tr><tr><td>BR</td><td>OUTLOOP</td><td>;then branch to print next char</td></tr><tr><td rowspan="7">NOCHAR:</td><td></td><td></td><td>;Comes here if no char avail</td></tr><tr><td>.TTINR</td><td></td><td>;Try to asain to set one</td></tr><tr><td>BCC</td><td>CHRIN</td><td>;There&#x27;s one avail this time!</td></tr><tr><td>;</td><td>.</td><td>;</td></tr><tr><td>;</td><td>.</td><td>;Do other processing</td></tr><tr><td>;</td><td>.</td><td>;</td></tr><tr><td>BR</td><td>NOCHAR</td><td>;Try asain</td></tr><tr><td rowspan="11">NOROOM:</td><td></td><td></td><td>;Comes here if no room in buffer</td></tr><tr><td>MOVB</td><td>(R1),RO</td><td>;Put char in RO</td></tr><tr><td>.TTOUTR</td><td></td><td>;Try to print it asain</td></tr><tr><td>BCC</td><td>CHROUT</td><td>;Successful !</td></tr><tr><td>;</td><td>.</td><td>;Code to be executed while waiting</td></tr><tr><td>;</td><td>.</td><td>;</td></tr><tr><td>;</td><td>.</td><td>;Now we must hans to wait...</td></tr><tr><td>BIC</td><td>#100,@JSW</td><td>;Clear bit #6 in JSW</td></tr><tr><td>.TTYOUT</td><td>(R1)</td><td>;Use ,TTYOUT to wait for room</td></tr><tr><td>BIS</td><td>#100,@JSW</td><td>;Finally successful - reset bit #6</td></tr><tr><td>BR</td><td>CHROUT</td><td>;then return to output loop</td></tr><tr><td rowspan="2">BUFFER:</td><td>.BLKW</td><td>64.</td><td>;Buffer</td></tr><tr><td>.END</td><td>START</td><td></td></tr></table>

## 2.97 .TWAIT (SYSGEN Option for SJ)

The .TWAIT request suspends the user's job for an indicated length of time. .TWAIT requires a queue element and thus should be considered when the .QSET request is issued.

Macro Call: .TWAIT area,time

where:

area is the address of a two-word EMT argument block

time is a pointer to two words of time (high order first, low order second), expressed in ticks

Request Format:

<table><tr><td rowspan="2">R0 → area:</td><td>24</td><td>0</td></tr><tr><td colspan="2">time</td></tr></table>

## Notes:

1. Since a .TWAIT is simulated in the monitor using suspend and resume, a .RSUM issued from a completion routine without a matching .SPND can cause the mainstream to continue past a timed wait before the entire time interval has elapsed. In addition, a .TWAIT issued within a completion routine is ignored by the monitor, since it would block the job from ever running again.

2. The unit of time for this request is clock ticks, which can be 50 Hz or 60 Hz, depending on the local power supply, if your system has a line frequency clock. This must be kept in mind when the time interval is specified.

Errors:

Code Explanation

0 No queue element was available.

Example:

```csv
,TITLE TWAIT.MAC
;+
; .TWAIT - This is an example in the use of the .TWAIT request.
; .TWAIT is useful in applications where a Program must be only
; activated Periodically. This example will 'wake up' every five seconds
; to perform a simulated "task", and then 'sleep' again. (For example
; Purposes this cycle will be repeated for a maximum of about 35 sec).
;-
,MCALL ,TWAIT,,QSET,,EXIT,,PRINT
START: CALL TASK ;Perform task...
1$: ,TWAIT #DAREA,#TIME ;Go to sleep for 5 seconds
BCS NOQ ;Branch if no queue element
CALL TASK ;Perform task again
DEC COUNT ;Bump counter - example good for 35 sec
BNE 1$ ;Branch if time's not up
,PRINT *BYE ;Say we're thru
,EXIT ;Exit Program
```

| TASK: |  |  | ;Periodic task simulated here |
| --- | --- | --- | --- |
|  | INC | TCNT | ;Bump a counter |
|  | BIT | #1,TCNT | ;Is it odd? |
|  | BEQ | 1$ | ;Branch if not |
|  | .PRINT | *TICK | ;Odd counter Prints "tick..." |
|  | RETURN |  | ;Return to caller |
| 1$: | .PRINT | *TOCK | ;Even counter Prints "took" |
|  | RETURN |  | ;Return to caller |
| NOQ: | .PRINT | #QERR | ;Print error message |
|  | .EXIT |  | ;Exit Program |
| AREA: | .WORD | 0,0 | ;EMT Argument block |
| TIME: | .WORD | 0,GO.*5. | ;GO ticks/sec * 5 seconds |
| COUNT: | .WORD | 7 | ;Maximum cycles for example |
| TCNT: | .WORD | 0 | ;Tick,tock count |
| TICK: | .ASCI I | /Tick.../&lt;200> | ;Message text |
| TOCK: | .ASCI Z | /Tock/ |  |
| BYE: | .ASCI Z | /Example Concluded/ |  |
| QERR: | .ASCI Z | /?No Q-Element Available?/ |  |
|  | .END | START |  |

## 2.98 .UNLOCK

See .LOCK/.UNLOCK (Section 2.45).

## 2.99 .UNMAP (XM Only)

The .UNMAP request unmaps a window and flags that portion of the program's virtual address space as being inaccessible. When an unmap operation is performed for a virtual job, attempts to access the unmapped address space cause a memory management fault. For a privileged job, the default (kernel) mapping is restored when a window is unmapped.

Macro Call: .UNMAP area,addr

where:

area is the address of a two-word argument block

addr is the address of the window control block that describes the window to be unmapped

Request Format:

<table><tr><td rowspan="2">R0 → area:</td><td>36</td><td>5</td></tr><tr><td colspan="2">addr</td></tr></table>

Errors:

| Code | Explanation |
| --- | --- |

3 An illegal window identifier was specified.

5 The specified window was not already mapped.

Example:

Refer to the example following the description of .CRAW.

## 2.100 .UNPROTECT

See .PROTECT/.UNPROTECT (Section 2.64).

## 2.101 .WAIT

The .WAIT request suspends program execution until all input/output requests on the specified channel are completed. The .WAIT request, combined with the .READ/.WRITE requests, makes double buffering a simple process.

.WAIT also conveys information through its error returns. An error is returned if either the channel is not open or the last I/O operation resulted in a hardware error.

If an asynchronous operation on a channel results in end-of-file, the following .WAIT programmed request will not detect it. The .WAIT request detects only hard error conditions. A subsequent operation on that channel will detect end-of-file and will return to the user immediately with the carry bit set and the end-of-file code in byte 52. Under these conditions, the subsequent operation is not initiated.

In an FB system, executing a .WAIT when I/O is pending causes that job to be suspended and another job to run, if possible.

Macro Call: .WAIT chan

## Request Format:

[figure omitted]

Errors:

## Explanation

0 Channel specified is not open.

1 Hardware error occurred on the previous I/O operation on this channel.

Example:

```csv
,TITLE WAIT.MAC
;+
; WAIT - This is an example in the use of the ,WAIT request. The
; example demonstrates asynchronous I/O where a mainline program
; initiates input via ,READ requests, does some other processing,
; makes sure input has completed via the ,WAIT request, then out-
; Puts the block just read. Another ,WAIT is issued before the next
; read is issued to make sure the previous write has finished. This
; example is a single file copy program, utilizing ,CSIGEN to input
; the file specs, load the required handlers and open the files.
;-

,MCALL READ,,WRITE,,CLOSE,,PRINT
,MCALL CSIGEN,,EXIT,,WAIT,,SRESET

ERRBYT = 52 %Error Byte location in SYSCOM
```

,ENABL     LSB          ;Enable local symbol block
START:     .CSIGEN   #DSPACE,#DEFEXT       ;Use CSIGEN to set handlers, files
        MOV     #AREA,R5           ;R5 => EMT Argument list
1\$:     .READ     R5,\*3           ;Read a block...
        BCS      G\$               ;Branch on error
        ;              .
        BIT       #1,IOBLK         ;Then simulate
        BNE      2\$               ;some other
        .PRINT    #MESSG         ;meaningful(?) process...
        ;              .
2\$:     .WAIT     #3           ;Did read finish OK?
        BCS      5\$               ;Branch if not
        .WRITE    R5,#0           ;Now write the block just read
        BCS      3\$               ;Branch on error
        ;              .                   ;Could do some more processing here...
        ;              .
        INC      IOBLK           ;Bump block # for next read
        .WAIT     #0               ;Wait for write to finish
        BCC      1\$               ;Branch if successful
3\$:     MOV     #WRERR,RO          ;RO => Write error msg
4\$:     .PRINT                  ;Report error
        .EXIT                  ;then exit program
5\$:     MOV     #RDERR,RO          ;RO => Read error msg
        BR      4\$               ;Branch to report error
6\$:     TSTB    @#ERRBYT          ;Read error...EOF?
        BNE      5\$               ;Branch if not
        .PRINT    #DONE           ;Yes...announce completion
        .CLOSE     #0               ;Make output file permanent
        .SRESET                  ;Dismiss fetched handlers
        .EXIT                  ;then exit program
AREA::     .WORD     0               ;EMT Area block
IOBLK:     .WORD     0               ;Block #,
        .WORD    BUFF             ;Buffer addr & word count
        .WORD    25G.          ;already fixed in block...
        .WORD     0               ;
BUFF:     .BLKW     25G.          ;I/O buffer
DEFEXT:     .WORD    0,0,0,0           ;No default extensions for CSIGEN
DONE:     .ASCIZ    /I-O Transfer Complete/ ;Messages...
MESSAGE:     .ASCIZ    <15><12>/< Simulating Mainline Processing >/
WRERR:     .ASCIZ    /?Write Error?/
RDERR:     .ASCIZ    /?Read Error?/
EOF:     .BYTE      0               ;EOF flag
        .EVEN                  ;
DSPACE = ,                       ;Handlers may be loaded starting here
        .END     START

## 2.102 .WDBBK (XM Only)

The .WDBBK macro defines symbols for the window definition block and reserves space for it. Information provided to the arguments of this macro permits the creation and mapping of a window through the use of the .CRAW request. Note that .WDBBK automatically invokes .WDBDF.

Macro Call: .WDBBK wnapr,wnsiz[,wnrid,wnoff,wnlen,wnsts]

where:

wnapr is the number of the Active Page Register set that includes the window's base address. A window must start on a 4K-word boundary. The valid range of values is from 0 through 7

wnsiz is the size of this window (expressed in 32-word units)

wnrid is the identification for the region to which this window maps. This argument is optional; supply it if you need to map this window. Use the value of R.GID from the region definition block for this argument after you create the region to which this window must map

wnoff is the offset into the region at which to start mapping this window (expressed in 32-word units). This argument is optional; supply it if you need to map this window. The default is 0, which means that the window starts mapping at the region's base address

wnlen is the amount of this window to map (expressed in 32-word units). This argument is optional; supply it if you need to map this window. The default value is 0, which maps as much of the window as possible

wnsts is the window status word. This argument is optional; supply it if you need to map this window when you issue the .CRAW request. Set bit 8, called WS.MAP, to cause .CRAW to perform an implied mapping operation

Example:

See Chapter 4 of the RT-11 Software Support Manual for an example that uses the .WDBBK macro and a detailed description of the extended memory feature.

## 2.103 .WDBDF (XM Only)

The .WDBDF macro defines the symbolic offset names for the window definition block and the names for the window status word bit patterns. In addition, this macro also defines the length of the window definition block by setting up the following symbol:

W.NLGH = 16

The .WDBDF macro does not reserve any space for the window definition block (see .WDBBK).

```txt
Macro Call: .WDBDF
```

The .WDBDF macro expands as follows:

W.NID = 0
W.NAPR = 1
W.NBAS = 2
W.NSIZ = 4
W.NRID = 6
W.NOFF = 10
W.NLEN = 12
W.NSTS = 14
W.NLGH = 16
WS.CRW = 100000
WS.UNM = 40000
WS.ELW = 20000
WS.MAP = 400

## 2.104 .WRITE/.WRITC/.WRITW

Write operations for the three modes of RT-11 I/O are done using the .WRITE, .WRITC, and .WRITW programmed requests.

Note that in the case of .WRITE and .WRITC, additional queue elements should be allocated for buffered I/O operations (see .QSET programmed request).

Under an FB monitor with the system job feature, .WRITE/C/W requests may be used to send messages to other jobs in the system.

## .WRITE

The .WRITE request transfers a specified number of words from memory to the specified channel. Control returns to your program immediately after the request is queued.

Macro Call: .WRITE area,chan,buf,wcnt,blk

## where:

area is the address of a five-word EMT argument block

chan is a channel number in the range 0 to 376(octal)

buf is the address of the memory buffer to be used for output

wcnt is the number of words to be written

blk is the block number to be written. For a file-structured .LOOKUP or .ENTER, the block number is relative to the start of the file. For a non-file-structured .LOOKUP or .ENTER, the block number is the absolute block number on the device. The user program should normally update blk before it is used again. Some devices, such as LP, may assign the blk argument special meaning. For example, if blk = 0, LP: issues a form feed

Request Format:

<table><tr><td rowspan="5">R0 → area:</td><td>11</td><td>chan</td></tr><tr><td colspan="2">blk</td></tr><tr><td colspan="2">buf</td></tr><tr><td colspan="2">wcnt</td></tr><tr><td colspan="2">1</td></tr></table>

## NOTE

When any .WRITE, .WRITC, or .WRITW programmed request is returned, R0 contains the number of words requested if the write is to a sequential-access device (for example, magtape). If the write is to a random-access device (disk or DECtape), R0 contains the number of words that will be written (.WRITE or .WRITC) or have been written (.WRITW). If a request is made to write past the end-of-file on a random-access device, the word count is shortened and an error is returned. The shortened word count is returned in R0. If a write goes past EOT on magtape, an error is returned and R0 = 0. Note that the write is done and a completion routine, if specified, is entered, unless the request cannot be partially filled (shortened word count = 0).

## Errors:

Code Explanation

0 Attempted to write past end-of-file.

. 1 Hardware error.

2 Channel was not opened.

Example:

Refer to the example following .READ.

## .WRITC

The .WRITC request transfers a specified number of words from memory to a specified channel. Control returns to the user program immediately after the request is queued. Execution of the user program continues until the .WRITC is complete, then control passes to the routine specified in the request. When an RTS PC is encountered in the completion routine, control returns to the user program.

Macro Call: .WRITC area,chan,buf,wcnt,crtn,blk

where:

area is the address of a five-word EMT argument block

chan is a channel number in the range 0 to 376(octal)

buf is the address of the memory buffer to be used for output

wcnt is the number of words to be written

crtn is the address of the completion routine to be entered

blk is the block number to be written. For a file-structured .LOOKUP or .ENTER, the block number is relative to the start of the file. For a non-file-structured .LOOKUP or .ENTER, the block number is the absolute block number on the device. Your program should normally update blk before it is used again. See the RT-11 Software Support Manual for the significance of the block number for devices such as line printers and paper tape punchers

Request Format:

R0 → area:

[figure omitted]

<table><tr><td>11</td><td>chan</td></tr><tr><td colspan="2">blk</td></tr><tr><td colspan="2">buf</td></tr><tr><td colspan="2">wcnt</td></tr><tr><td colspan="2">crtn</td></tr></table>

## NOTE

When any .WRITE, .WRITC, or .WRITW programmed request is returned, R0 contains the number of words requested if the write is to a sequential-access device (for example, magtape). If the write is to a random-access device (disk or DECtape), R0 contains the number of words that will be written (.WRITE or .WRITC) or have been written (.WRITW). If a request is made to write past the end-of-file on a random-access device, the word count is shortened and an error is returned. The shortened word count is returned in R0. If a write goes past EOF on magtape, the handler returns an error and R0 = 0. Note that the write is done and a completion routine, if specified, is entered, unless the request cannot be partially filled (shortened word count = 0).

When a .WRITC completion routine is entered, the following conditions are true:

1. R0 contains the contents of the channel status word for the operation. If bit 0 of R0 is set, a hardware error occurred during the transfer: Consequently, the data may be unreliable.

2. R1 contains the octal channel number of the operation. This is useful when the same completion routine is to be used for several different transfers.

3. Registers R0 and R1 are available for use by the routine, but all other registers must be saved and restored. Data cannot be passed between the main program and completion routines in any register or on the stack.

Errors:

## Code

## Explanation

0 End-of-file on output. Tried to write outside limits of file.

1 Hardware error occurred.

2 Specified channel is not open.

Example:

Refer to the example following .READC.

## .WRITW

The .WRITW request transfers a specified number of words from memory to the specified channel. Control returns to your program when the .WRITW is complete.

Macro Call: .WRITW area,chan,buf,wcnt,blk

where:

area is the address of a five-word EMT argument block

chan is a channel number in the range 0 to 376(octal)

buf is the address of the buffer to be used for output

wcnt is the number of words to be written. The number must be positive

blk is the block number to be written. For a file-structured .LOOKUP or .ENTER, the block number is relative to the start of the file. For a non-file-structured .LOOKUP or .ENTER, the block number is the absolute block number on the device. Your program should normally update blk before it is used again. See the RT-11 Software Support Manual for the significance of the block number for devices such as line printers and paper tape punchers

## Request Format:

[figure omitted]

<table><tr><td>11</td><td>chan</td></tr><tr><td colspan="2">blk</td></tr><tr><td colspan="2">buf</td></tr><tr><td colspan="2">wcnt</td></tr><tr><td colspan="2">0</td></tr></table>

## NOTE

When any .WRITE, .WRITC, or .WRITW programmed request is returned, R0 contains the number of words requested if the write is to a sequential-access device (for example, magtape). If the write is to a random-access device (disk or DECtape), R0 contains the number of words that will be written (.WRITE or .WRITC) or have been written (.WRITW). If a request is made to write past the end-of-file on a random-access device, the word count is shortened and an error is returned. The shortened word count is returned in R0. If a write goes past end-of-file on magtape, the handler returns an error and R0 = 0. Note that the write is done and a completion routine, if specified, is entered, unless the request cannot be partially filled (shortened word count = 0).

Errors:

Code Explanation

0 Attempted to write past EOF.

1 Hardware error.

2 Channel was not opened.

## Example:

Refer to the example following .READW.

(1)
