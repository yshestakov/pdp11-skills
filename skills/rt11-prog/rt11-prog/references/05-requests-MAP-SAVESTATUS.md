# RT-11 PRM reference: Ch.2 programmed requests .MAP through .SAVESTATUS: .MFPS/.MTPS .MRKT .MTATCH .MTDTCH .MTGET .MTIN .MTOUT .MTPRNT .MTRCTO .MTSET .MTSTAT .MWAIT .PEEK/.POKE .PRINT .PROTECT .PURGE .QELDF .QSET .RCTRLO .RCVD/.RCVDC/.RCVDW .RDBBK .RDBDF .READ/.READC/.READW .RENAME .REOPEN .RSUM .SAVESTATUS

Source: RT-11 Programmer's Reference Manual AA-H378C-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' sometimes reads as ',' (`,MCALL` = `.MCALL`), 'R0' as 'RO', '#' as '\*' or '*'. Verify exact macro expansions against `sysmac_v53.mac`.

Contents:
- 2.47 .MAP (XM Only)
- 2.48 .MFPS/.MTPS
- 2.49 .MRKT (FB and XM; SJ Monitor Special Feature)
- 2.50 .MTATCH (Special Feature)
- 2.51 .MTDTCH (Special Feature)
- 2.52 .MTGET (Special Feature)
- 2.53 .MTIN (Special Feature)
- 2.54 .MTOUT (Special Feature)
- 2.55 .MTPRNT (Special Feature)
- 2.56 .MTPS
- 2.57 .MTRCTO (Special Feature)
- 2.58 .MTSET (Special Feature)
- 2.59 .MTSTAT (Special Feature)
- 2.60 .MWAIT (FB and XM Only)
- 2.61 .PEEK/.POKE
- 2.62 .POKE
- 2.63 .PRINT
- 2.64 .PROTECT/.UNPROTECT (FB and XM Only)
- 2.65 .PURGE
- 2.66 .PVAL
- 2.67 .QELDF (Device Handler Only)
- 2.68 .QSET
- 2.69 .RCTRLO
- 2.70 .RCVD/.RCVDC/.RCVDW (FB and XM Only)
- 2.71 .RDBBK (XM Only)
- 2.72 .RDBDF (XM Only)
- 2.73 .READ/.READC/.READW
- 2.74 .RELEAS
- 2.75 .RENAME
- 2.76 .REOPEN
- 2.77 .RSUM (FB and XM Only)
- 2.78 .SAVESTATUS

---

## 2.47 .MAP (XM Only)

The .MAP request maps a previously defined address window into a dynamic region of extended memory or into the static region in the lower 28K words of memory. If the window is already mapped to another region, an implicit unmapping operation is performed (see the .UNMAP programmed request).

Macro Call: .MAP area[,addr]

where:

area is the address of a two-word EMT argument block

addr is the address of the window definition block containing a description of the window to be mapped and the region to which it will map

Request Format:

[figure omitted]

Errors:

Code

## Explanation

2 An invalid region identifier was specified.

3 An invalid window identifier was specified.

4 The specified window was not mapped because the offset is beyond the end of the region, the region is larger than the window, or the window would extend beyond the bounds of the region.

Example:

Refer to example for the .CRAW request.

## 2.48 .MFPS/.MTPS

The .MFPS and .MTPS macro calls allow processor-independent user access to the processor status word. The contents of the registers are preserved across either call.

The .MFPS call is used to read the priority bits only. Condition codes are destroyed during the call and must be directly accessed (using conditional branch instructions) if they are to be read in a processor-independent manner.

In the XM monitor, .MFPS and .MTPS can be used only by privileged jobs and are not available for use by virtual jobs.

Macro Call: .MFPS addr

where:

addr is the address into which the processor status is to be stored; if addr is not present, the value is returned on the stack. Note that only the priority bits are significant

The .MTPS call is used to set the priority bits.

Macro Call: .MTPS value

## where:

value is either the value or the address of the value (depending on addressing mode) to be placed in the PSW. If value is not present, the processor status word is taken from the stack. Note that the high byte on the stack is set to 0 when value is present. If value is not present, you should set the stack to the appropriate value. In either case, the lower byte on the stack is put in the processor status word

## Note:

It is possible to perform MTPS and MFPS operations and access the condition codes by following this special technique:

1. In the beginning of your program, set up the IOT trap vector as follows:

. = 20
    .ASECT
    .WORD    GETPS
    .WORD    340
; SET UP IOT
; IOT SERVICE ADDRESS IN 'MFPS' SUBROUTINE
; PRIORITY 7

2. Elsewhere in your program place the following routines:

```asm
;+
; MFPS/MTPS ROUTINES ...
;-

MFPS:    IOT                     ;EXECUTE IOT
                                            ;WILL RETURN TO CALLER W/ PS ON STACK

GETPS:   MOV     4(SP),@SP      ;PUT USER RETURN ON TOP
           MOV     2(SP),4(SP)   ;MOVE PS SAVED BY IOT
MTPS:    RTI                     ;WILL RETURN TO CALLER W/ NEW PS
```

3. To get the PSW or to set the PSW to a desired value, follow this sequence of instructions:

```prolog
;+
; TO GET PS ...
;-
JSR PC,MFPS ;GET PS
;CONTINUE,PS IS ON STACK ...
```

```txt
;+
; TO PUT PS ...
;-

MOV     NEWPS,-(SP)    ;PUT DESIRED PS ON STACK ...
JSR     PC,MTPS        ;CALL MTSP
                                ;CONTINUE PROCESS W/ NEW PS ...
```

Errors:
    None.

```asm
.MCALL          .MFPS,,MTPS,,EXIT,,PRINT,,TTINR
JSW = 44                          ;Job Status Word location
TTSPC$ = 10000                   ;TTY Special bit

START:
BIS            *TTSPC$,@#JSW       ;Set TTY Special bit
;               .
;               .
CALL            GETQUE             ;Call subroutine to return next free
                        ;element - on return R5 => element
BCC            1$                 ;Branch if no error
.PRINT           #NOELEM         ;No more elements available
BIC            #TTSPC$,@#JSW       ;Reset special bit
.EXIT                         ;Exit program

1$:     NOP                          ;Program continues
NOP                          ;
.PRINT           #GOT1              ;Announce success
2$:     .TTINR                          ;Wait for a key to be hit on console
BCS            2$
BR            START

GETQUE:    MOV            #QHEAD,R4       ;Point to queue head
TST            @R4              ;Queue exhausted?
BEQ            11$             ;Yes...set error on leaving
.MFPS                          ;Save status on stack
.MTPS            #340             ;Raise Priority to 7
MOV            @R4,R5       ;R5 points to next element
MOV            @R5,@R4       ;Relink the queue
.MTPS                          ;Restore previous status
TST            (PC)+        ;This clears carry & skips next instruction
11$:     SEC                          ;Set carry bit (to flag error)
RETURN                       ;Return to caller

QHEAD:      .WORD Q1                          ;Queue head
Q1:      .WORD Q2,0,0                ;3 linked queue elements
Q2:      .WORD Q3,0,0
Q3:      .WORD 0,0,0

NOELEM:     .ASCIZ      /?No more Queue Elements Available?/
GOT1:      .ASCIZ      /Element acquired...Press any key to continue/

.END           START
```

## 2.49 .MRKT (FB and XM; SJ Monitor Special Feature)

The .MRKT request schedules a completion routine to be entered after a specified time interval (measured in clock ticks) has elapsed. The .MRKT request is an optional feature in the SJ monitor, and is selected as a system generation option.

A .MRKT request requires a queue element taken from the same list as the I/O queue elements. The element is in use until either the completion routine is entered or a cancel mark time request is issued (see .CMKT request). The user should allocate enough queue elements to handle at least as many mark time and I/O requests as are expected to be pending simultaneously.

```csv
.MCALL .MRKT,.TTINR,.EXIT,.PRINT,.TTYOUT,.CMKT,.TWAIT,.QSET
```

Macro Call: .MRKT area,time,crtn,id

where:

area is the address of a four-word EMT argument block

time is the address of a two word-block containing the time interval (high order first, low order second), specified as a number of clock ticks

crtn is the entry point of a completion routine

id is a non-zero number or memory address assigned by the user to identify the particular request to the completion routine and to any cancel mark time requests. The number must not be within the range 177700–177777, which is reserved for system use. The number need not be unique (several .MRKT requests can specify the same id). On entry to the completion routine, the id number is in R0

Request Format:

[figure omitted]

Errors:

0 No queue element was available.

Example:

```txt
;+
; .MRKT/.CMKT - This is an example in the use of the .MRKT/.CMKT requests
; The example illustrates a user implemented "Timed Read" to cancel an
; input request after a specified time interval,
;-
```

```matlab
LF = 12
JSW = 44
TCBIT$ = 100 ;Return C-bit bit in JSW
TTSPC$ = 10000
START: .QSET #XQUE,#1
1$: MOV #PROMT,RO
MOV #BUFFER,R1
CALL TREAD$
BCS 2$
,PRINT *LINE
BR 1$
2$: ,PRINT *TIMOUT
%Line Feed
%Job Status Word location
%TTY Special Mode bit in JSW
%Need an extra Q-Elem for this
%Mainline - RO => Prompt
%R1 => Input buffer
%Do a "timed read"
%C-bit set = Timed out
%"Process" data...
%Go back for more
%Read timed out - could process
%Partial data but we'll just exit
```

```txt
;* TREAD$ - "Timed Read" Subroutine
;* Input: RO => Prompt Strings / RO = 0 if no Prompt
;* R1 => Input Buffer
;* Output: Buffer contains input chars, if any, terminated
;* by a null char. C-Bit set if timed out
```

```asm
TREAD\$: TST RO ;See if we have to Prompt
BEQ 1\$ ;Branch if no...;
.PRINT ;Output Prompt
1\$: CLR TBYT ;Clear time-out flag
.MRKT *TAREA,#TIME,#TOUT,#1 ;Issue a ,MRKT for 10 sec
BIS *TCBIT\$,@JSW ;Set C-Bit bit in JSW (for F/B)
CLRB @R1 ;Start with "empty" buffer
TTIN: .TWAIT *AREA ;Wait so we don't lock out BG
.TTINR ;Look for a character
BIT #1,(PC)+ ;Timed out?
TBYT: .WORD 0 ;Time-out flag
BNE 2\$ ;Branch if yes
BCS TTIN ;Branch if input not complete
MOVB RO,(R1)+ ;Xfer 1st character
.CMKT *TAREA,#0 ;Cancel .MRKT
2\$: BIS *TTSPC\$,@JSW ;Turn on TT: Special mode
3\$: .TTINR ;Flush TT: ring buffer
MOVB RO,(R1)+ ;Putting characters in user buffer
BCC 3\$ ;If more char, so set 'em
CLRB -(R1) ;Terminate input with null byte
BIC *TCBIT\$!TTSPC\$,@JSW ;Clear bits in JSW
ROR TBYT ;Set carry if timed out
RETURN ;Return to caller
TOUT: INC TBYT
RETURN ;Leave completion code
XQUE: .BLKW 10, ;Extra Q-Element
AREA: .WORD 0,WAIT ;EMT Argument block for .TWAIT
TAREA: .BLKW 4 ;EMT Argument block for .MRKT
TIME: .WORD 0,GOO, ;Time-out interval (10 sec)
WAIT: .WORD 0,1 ;1/60 sec wait between .TTINRs
LINE: .ASCII /Not in stock - Part # / ;Dummy response
BUFFER: .BLKB 81, ;User input buffer
PROMT: .ASCIZ /Enter Part * >/<200> ;Prompt
TIMOUT: .ASCIZ /Timed read expired!/ ;Too bad message
.END START
```

## 2.50 .MTATCH (Special Feature)

The .MTATCH request attaches a terminal for exclusive use by the requesting job. This operation must be performed before any job can use a terminal with multiterminal programmed requests, although a job can issue a .MTGET request before a .MTATCH. If .MTATCH request fails because the terminal is owned by another job, the job number of the owner is returned in R0.

Macro Call: .MTATCH area,addr,unit

where:

area is the address of a three-word EMT argument block

addr is the optional address of an asynchronous terminal status word, or it must be #0 (The asynchronous terminal status word is a special feature that you can select during the system generation process.)

unit is the logical unit number of the terminal (The logical unit number is the number assigned by the system to a particular physical unit during the system generation process.)

Request Format:

<table><tr><td>37</td><td>5</td></tr><tr><td colspan="2">addr</td></tr><tr><td>0</td><td>unit</td></tr></table>

```txt
HNGUP$ = 4000 ;Terminal off-line bit
TTSPC$ = 10000 ;Special mode bit
TTLC$ = 40000 ;Lower-case mode bit
AS.INP = 40000 ;Input available bit
M.TSTS = 0 ;Terminal status word
M.TSTW = 7 ;Terminal state byte
M.NLUN = 4 ;# of LUNs word
```

## Errors:

Code Explanation

2 Nonexistent logical unit number.

3 Invalid request; function code out of range.

4 Unit attached by another job (job number returned in R0).

5 In the XM monitor, the optional status word address is not in valid user virtual address space.

## Example:

```prolog
;+
; MTXAMP.MAC - The following is an example Program that
; demonstrates the use of the multiterminal
; Programmed requests. The Program attaches all the
; terminals on a given system, then Proceeds with an
; input/echo exercise on all attached terminals until
; CTRL/C is sent to it.
;-
```

```txt
.MCALL          .MTATCH,.MTPRNT,.MTGET,.MTIN,.MTOUT
.MCALL          .PRINT,.MTRCTO,.MTSET,.MTSTAT,.EXIT
```

MTXAMP:
    .MTSTAT     \*MTA,#MSTAT         ;Get MTTY status
    MOV         MSTAT+M.NLUN,R4      ;R4 = # LUNs
    BEQ         MERR             ;None? Not MTTY!!!
    CLR         R1              ;Initial LUN = #0
    MOV         \*AST,R2          ;R2 → AST word array
10\$:   .MTATCH     \*MTA,R2,R1       ;Attach terminal
    BCC         20\$           ;Success!
    CLRB         TAI(R1)       ;Set attach failed
    BR         30\$           ;Proceed with next LUN
20\$:   MOVB     \*1,TAI(R1)       ;Attach successful
    MOV         R1,R3          ;Copy LUN
    ASL         R3            ;Multiply by 8 for offset
    ASL         R3            ;to the terminal status
    ASL         R3            ;block...
    ADD     \*TSB,R3          ;R3 → LUN's TSB
    .MTGET     \*MTA,R3,R1       ;Get LUN's status
    BIS     \*TTSPC\$+TTLC\$,M.TSTS(R3) ;Set special
                        ;mode and lower case
    .MTSET     \*MTA,R3,R1       ;Set LUN's status
    BITB     \*HNGUP\$/400,M.TSTW(R3) ;On line?
    BNE     30\$           ;Nope!
    .MTRCTO     \*MTA,R1          ;Reset CTRL/O
    .MTPRNT     \*MTA,#HELLO,R1      ;Say hello...,
30\$:   ADD     \*2,R2          ;R2 → Next AST word
    INC         R1              ;Get next LUN
    CMP         R1,R4          ;Done?
    BLO     10\$           ;Nope, go attach another

```asm
LOOP:
        CLR          R1              ;Input & echo forever
        MOV         *AST,R2           ;Initial LUN = 0
10\$:     TSTB      TAI(R1)       ;R2 → AST words
        BEQ          20\$               ;R2 → AST words
        BIT          #AS,INP,(R2)       ;Terminal attached?
        BEQ          20\$               ;Nope...
        .MTIN         #MTA,#MTCHAR,R1,#1   ;Any input?
        BCS          ERR             ;Nope...
        .MTOUT     #MTA,#MTCHAR,R1,#1   ;Input a character
        BCS          ERR             ;Ooops! Error on input
20\$:     ADD         #2,R2           ;Echo the character
        INC          R1               ;Point to next AST word
        CMP          R1,R4           ;Get next LUN
        BLO          10\$               ;Done them all?
        BR          LOOP           ;Doops! Error on output
ERR:     .PRINT     *UNEXP           ;Point to next AST word
        .EXIT            #UNEXP           ;Yes, repeat (forever!)
MERR:     .PRINT     *NOMTTY           ;Point to next AST word
        .EXIT            #NOMTTY           ;Get next LUN
AST:     .BLKW      16.                 ;Not multiterminal
TAI:     .BLKB      16.                 ;Print message & exit
MSTAT:     .BLKW      8.                 ;Print message & exit
TSB:     .BLKW      16.*4.                 ;Asynchronous Terminal
MTA:     .BLKW      4.                 ;Status Words (1/LUN)
MTCHAR:     .BYTE      0.                 ;Terminal attached list
HELLO:     .ASCII     <33>"H"<33>"J"       ;MTTY status block
        .ASCIZ         /Hello! Characters typed will be echoed/
NOMTTY:    .ASCIZ      /?Not multiterminal system?/
UNEXP:    .ASCIZ      /?Unexpected error...Program aborting?/
        .END         MTXAMP           ;O = Not attached
HELLO:     .ASCII     <33>"H"<33>"J"       ;MTTY status block
        .ASCIZ         /Hello! Characters typed will be echoed/
NOMTTY:    .ASCIZ      /?Not multiterminal system?/
UNEXP:    .ASCIZ      /?Unexpected error...Program aborting?/
        .END         MTXAMP           ;Character stored here
End of program
```

## 2.51 .MTDTCH (Special Feature)

The .MTDTCH request detaches a terminal from one job and makes it available for other jobs. When a terminal is detached, it is deactivated, and unsolicited interrupts are ignored. Input is disabled immediately, but any characters in the output buffer are printed. Attempts to detach a terminal attached by another job result in an error.

Macro Call: .MTDTCH area, unit

where:

area is the address of a three-word EMT argument block

unit is the logical unit number (lun) of the terminal to be detached Request Format:

<table><tr><td rowspan="3">R0 → area:</td><td>37</td><td>6</td></tr><tr><td colspan="2">unused</td></tr><tr><td>—</td><td>unit</td></tr></table>

Errors:

1 Invalid unit number, unit not attached.

2 Nonexistent logical unit number.

3 Invalid request; function code out of range.

Example:

```asm
.MCALL .MTDTCH,.MTPRNT,.MTATCH,.EXIT,.PRINT
START:
.MTATCH #MTA,#0,#3 ;ATTACH TO LUN 3
BCS 1\$ ;ATTACH ERROR
.MTPRNT MTA,#MESS,#3 ;PRINT MESSAGE
.MTDTCH #MTA,#3 ;DETACH LUN 3
.EXIT
1\$: PRINT *ATTERR ;ATTACH ERROR
; (PRINTED ON CONSOLE)
.EXIT
ATTERR: .ASCIZ/ATTACH ERROR/
MESS: .ASCIZ/DETACHING TERMINAL/
.EVEN
MTA: .BLKW 3
.END START
```

## 2.52 .MTGET (Special Feature)

The .MTGET request returns the status of the specified terminal unit to the caller. If a .MTGET request fails because the terminal is owned by another job, the job number of the owner is returned in R0. You do not need to do an .MTATCH before using the .MTGET request.

Macro Call: .MTGET area,addr,unit

where:

area is the address of a three-word EMT argument block

addr is the address of a four-word status block where the status information is returned

unit is the logical unit number (lun) of the terminal whose status is requested. A unit need not be attached to the job issuing a .MTGET request. If the unit is attached to another job (error code 4), the terminal status will be returned and the job number will be contained in R0. In any other error condition, the contents of R0 are undefined

Request Format:

<table><tr><td>37</td><td>1</td></tr><tr><td colspan="2">addr</td></tr><tr><td>—</td><td>unit</td></tr></table>

The status block has the following structure:

<table><tr><td colspan="2">M.TSTS</td></tr><tr><td colspan="2">M.TST2</td></tr><tr><td>M.FCNT</td><td>M.TFIL</td></tr><tr><td>M.TSTW</td><td>M.TWID</td></tr></table>

The following information is contained in the status block:

<table><tr><td colspan="2">Byte Offset</td><td>Description</td></tr><tr><td>0</td><td>(M.TSTS)</td><td>Terminal configuration word 1</td></tr><tr><td>2</td><td>(M.TST2)</td><td>Terminal configuration word 2</td></tr><tr><td>4</td><td>(M.TFIL)</td><td>Character requiring fillers</td></tr><tr><td>5</td><td>(M.FCNT)</td><td>Number of fillers</td></tr><tr><td>6</td><td>(M.TWID)</td><td>Carriage width</td></tr><tr><td>7</td><td>(M.TSTW)</td><td>Terminal status byte</td></tr></table>

Note that if an error occurs, and the error code is not 1 or 4, the status block will not have been modified.

## NOTE

Use the Bit Set (BIS) and Bit Clear (BIC) instructions instead of Move (MOV) and Clear (CLR) instructions when setting terminal and line characteristics. This avoids changing other bits inadvertently.

The bit definitions for terminal configuration word 1 (M.TSTS) are as follows:

| Value | Bit | Meaning |
| --- | --- | --- |
| 1 | 0 | Terminal has hardware tab |
| 2 | 1 | Output RET/LF when carriage width exceeded |
| 4 | 2 | Terminal has hardware form feed |
| 10 | 3 | Process CTRL/F and CTRL/B (and CTRL/X if system job) as special command characters (if clear, CTRL/F and CTRL/B are treated as ordinary characters) |
| 100 | 6 | Inhibit TT wait (similar to bit 6 in the Job Status Word) |
| 200 | 7 | Enable CTRL/S-CTRL/Q processing |
| 7400 | 8-11 | Line speed (baud rate) mask. Bits 8 through 11 indicate the terminal baud rate (DZ11 and DZV11 only). The values are as follows: |

| Octal Value of Line Speed Mask (M.TSTS bits 11–8) | Baud Rate |
| --- | --- |
| 0000 | 50 |
| 0400 | 75 |
| 1000 | 110 |
| 1400 | 134.5 |
| 2000 | 150 |
| 2400 | 300 |
| 3000 | 600 |
| 3400 | 1200 |

| 4000 | 1800 |
| --- | --- |
| 4400 | 2000 |
| 5000 | 2400 |
| 5400 | 3600 |
| 6000 | 4800 |
| 6400 | 7200 |
| 7000 | 9600 |
| 7400 | (unused) |

10000 12 Character mode input (similar to bit 12 in the Job Status Word)

20000 13 Terminal is remote (Read-only bit)

40000 14 Lowercase to uppercase conversion disabled

100000 15 Use backspace for rubout (video type display)

The bit definitions for terminal configuration word 2 (M.TST2) are as follows:

| Value | Bit | Meaning |
| --- | --- | --- |
| 3 | 0-1 | Character length, which can be 5(00), 6(01), 7(10), or 8(11) bits (DZ only) |
| 4 | 2 | Unit stop, which sends one stop bit when clear, two stop bits when set (DZ only) |
| 10 | 3 | Parity enable (DZ only) |
| 20 | 4 | Odd parity when set; even parity when clear |
| 140 | 5-6 | Reserved |
| 200 | 7 | Read pass all |
| 77400 | 8-14 | Reserved |
| 100000 | 15 | Write pass all |

The bit definitions for terminal status byte (M.TSTW) are as follows:

| Value | Bit | Meaning |
| --- | --- | --- |
| 2000 | 10 | Terminal is shared console |
| 4000 | 11 | Terminal has hung up |
| 10000 | 12 | Terminal interface is DZ11 |
| 40000 | 14 | Double CTRL/C was struck (the .MTGET request resets this bit in the terminal control block if it is on) |
| 100000 | 15 | Terminal is acting as console |

## Errors:

## Explanation

1 Invalid unit number, unit not attached.

2 Nonexistent logical unit number.

3 Invalid request; function code out of range.

4 Unit attached by another job (job number returned in R0).

5 In the XM monitor, the status block address is not in valid user virtual address space.

## Example:

Refer to the example for the .MTATCH request.

## 2.53 .MTIN (Special Feature)

The .MTIN request reads characters from the keyboard buffer. It is the multiterminal form of the .TTYIN request. The .MTIN request moves one or more characters from the input ring buffer to a buffer specified by you. The terminal must be attached. An updated user buffer address is returned in R0 if the request is successful. If bit 6 is set in the M.TSTS word (see the MTSET request), the .MTIN request returns immediately with the carry bit set (code 0) if there is no input available. Operation is similar for the system console if bit 6 is set in the JSW. If bit 12 in M.TSTS is clear, no line is available; if bit 12 is set, there are no characters in the buffer. If these conditions do not exist, the .MTIN request waits until input is available, and the job is suspended until input is available.

The meaning of bits 6 and 12 in the terminal configuration word (M.TSTS) for the programmed request .MTIN is as follows:

| Bit 6 | Bit 12 | Meaning |
| --- | --- | --- |
| 0 | 0 | Normal mode of input (echo provided); wait for line |
| 1 | 0 | Carry bit set: no line available |
| 1 | 1 | Carry bit set: no character available; no echo provided |
| 0 | 1 | No echo provided |

If a multiple-character request was made and the number of characters requested are not available, the request can either wait for the characters to become available, or it can return with a partial transfer. If bit 6 of M.TSTS is clear, the request waits for more characters. If bit 6 is set, the request returns with a partial transfer. In the latter case, R0 contains the updated buffer address (pointing past the last character transferred), the C bit is set, and the error code is 0.

The .MTIN request has the following form:

Macro Call: .MTIN area,addr,unit[,chrcnt]

where:

area is the address of a three-word EMT argument block

addr      is the byte address of the user buffer

unit is the logical unit number of the terminal input

chrcnt is a character count indicating the number of characters to transfer. The valid range is from 1 to 255(decimal). A character count of zero means one character

Request Format:

<table><tr><td>37</td><td>2</td></tr><tr><td colspan="2">addr</td></tr><tr><td>chrcnt</td><td>unit</td></tr></table>

Errors:

Code Explanation

0 No input available — bit 6 is set in the Job Status Word (for the system console) or in M.TSTS by the .MTSET request.

1 Invalid unit number, unit not attached.

2 Nonexistent logical unit number.

3 Invalid request; function code out of range.

5 In the XM monitor, the user buffer address is not in valid user virtual address space.

Example:

Refer to the example for the .MTATCH request.

## 2.54 .MTOUT (Special Feature)

The .MTOUT request transfers characters to the terminal output buffer. This request is the multiterminal form of the .TTYOUT request. The .MTOUT request moves one or more characters from the user's buffer to the output ring buffer of the terminal. The terminal must be attached. An updated user buffer address is returned in R0 if the request is successful. When there is no room in the output ring buffer, the carry bit is set and an error code of 0 is returned in byte 52 if bit 6 is set in M.TSTS. Otherwise, the job is suspended until room becomes available.

If a multiple-character request was made and there is not enough room in the output ring buffer to transfer the requested number of characters, the request can either wait for enough room to become available, or it can return with a partial transfer. If bit 6 in M.TSTS is clear, the request waits until it can complete the full transfer. If bit 6 is set, the request returns with a partial transfer. In the latter case, R0 contains the updated buffer address (pointing past the last character transferred), the C bit is set, and the error code is 0.

The meaning of bit 6 in the terminal configuration word (M.TSTS) for the .MTOUT request is as follows:

Bit 6 Meaning

0 Normal mode for output; wait for room in buffer

1 Carry bit set: no room in output ring buffer

Macro Call: .MTOUT area,addr,unit[,chrcnt]

where:

area is the address of a three-word EMT argument block

addr is the address of the caller's input buffer

unit is the unit number of the terminal

chrcnt is a character count indicating the number of characters to transfer. The valid range is from 1 to 255(decimal)

Request Format:

<table><tr><td rowspan="3">R0 → area:</td><td>37</td><td>3</td></tr><tr><td colspan="2">addr</td></tr><tr><td>chrcnt</td><td>unit</td></tr></table>

## Errors:

Code Explanation

0 No room in output buffer.

1 Invalid unit number, unit not attached.

2 Nonexistent logical unit number.

3 Invalid request; function code out of range.

5 In the XM monitor, the user buffer address is not in valid user virtual address space.

Example:

Refer to the example for the .MTATCH request.

## 2.55 .MTPRNT (Special Feature)

This .MTPRNT request allows one or more lines to be printed at the specified terminal in a multiterminal environment. It is equivalent to the .PRINT request (see .MTSET request for more details). The string to be printed must be terminated with a null byte or a 200 byte, similar to the string used with the .PRINT request as follows:

.ASCIZ /string/

or

.ASCII /string/<200>

The null byte causes a carriage return/line feed combination to be printed after the string. The 200 byte suppresses the carriage return/line feed combination and leaves the carriage positioned after the last character of the string. The request does not return until the transfer is complete.

Macro Call: .MTPRNT area,addr,unit

where:

area is the address of a three-word EMT argument block

addr is the starting address of the character string to be printed

unit is the unit number associated with the terminal

## Request Format:

<table><tr><td>37</td><td>7</td></tr><tr><td colspan="2">addr</td></tr><tr><td>—</td><td>unit</td></tr></table>

## Errors:

Code Explanation

1 Invalid unit number, unit not attached.

2 Nonexistent logical unit number.

3 Invalid request; function code out of range.

5 In the XM monitor, the character string address is not in valid user virtual address space.

Example:

Refer to the example for the .MTATCH request.

## 2.56 .MTPS

See .MFPS/.MTPS (Section 2.48).

## 2.57 .MTRCTO (Special Feature)

The .MTRCTO request resets the CTRL/O switch of the specified terminal and enables terminal output in a multiterminal environment. It is equivalent to the .RCTRLO request.

Macro Call: .MTRCTO area, unit

where:

area is the address of a three-word EMT argument block

unit is the unit number associated with the terminal

## Request Format:

<table><tr><td>37</td><td>4</td></tr><tr><td colspan="2">unused</td></tr><tr><td>—</td><td>unit</td></tr></table>

Errors:

Code Explanation

1 Invalid unit number, unit not attached.

2 Nonexistent logical unit number.

3 Invalid request; function code out of range.

## Example:

Refer to the example for the .MTATCH request.

## 2.58 .MTSET (Special Feature)

This multiterminal request sets terminal and line characteristics. It also determines the input/output mode of the terminal service requests for the specified terminal.

Macro Call: .MTSET area,addr,unit

where:

area is the address of a three-word EMT argument block

addr is the address of a four-word status block containing the line and terminal status being requested

unit is the logical unit number associated with the line and terminal

Request Format:

<table><tr><td rowspan="3">R0 → area:</td><td>37</td><td>1</td></tr><tr><td colspan="2">addr</td></tr><tr><td>—</td><td>unit</td></tr></table>

When the program returns from the request, the status block contains the following information:

Byte Offset Contents

0 Terminal configuration word 1 (The bit definitions are the same as those for the .MTGET request.)

2 Terminal configuration word 2 (The bit definitions are the same as those for the .MTGET request.)

4 Character requiring fillers

5 Number of fillers

6 Carriage width (byte)

## NOTE

The .MTSET request sets all of the parameters listed above. The recommended procedure for using .MTSET is: (1) precede it by an .MTGET request; (2) use BIS and BIC instructions to set or clear bit fields (modify only the bits or bytes that you intend to change); (3) issue the .MTSET request to replace the previous terminal status with the updated status.

Note that if an error occurs, and the error code is not 1, the status block will not have been modified.

Errors:

Code Explanation

1 Invalid unit number, lun not attached.

2 Nonexistent logical unit number.

3 Invalid request, function code out of range.

5 In the XM monitor, the status block address is not in valid user virtual address space.

Example:

Refer to the example for the .MTATCH request.

## 2.59 .MTSTAT (Special Feature)

The .MTSTAT request returns multiterminal system status information.

Macro Call: .MTSTAT area,addr

where:

area is the address of a three-word EMT block

addr is the address of an eight-word status block where multiterminal status information is returned. The status block contains the following information:

Byte Offset Contents

0 Offset from the base of the resident monitor to the first terminal control block (TCB)

2 Offset from the base of the resident monitor to the terminal control block of the console terminal for the program

4 The value (0–16 decimal) of the highest logical unit number (LUN) built into the system

6 The size of the terminal control block in bytes

10–17 Reserved

Request Format:

<table><tr><td rowspan="3">R0 → area:</td><td>37</td><td>10</td></tr><tr><td colspan="2">addr</td></tr><tr><td colspan="2">0</td></tr></table>

Errors:

Code Explanation

3 Invalid request; function code out of range

5 In XM, the status block address is not in valid user address space.

## Example:

Refer to the example for the .MTATCH request.

## 2.60 .MWAIT (FB and XM Only)

This request is similar to the .WAIT request. .MWAIT, however, suspends execution of the job issuing the request until all messages sent to the other job or requested from the other job have been received. It should be used with the .RCVD or .SDAT modes of message handling, where no action is taken when a message is completed.

Macro call: .MWAIT

Request Format:

Errors:

None.

Example:

```prolog
;+
; .MWAIT - This is an example in the use of the .MWAIT request.
; The example is actually two Programs, a Background job
; which sends messages, and a Foresround Job, which receives them.
; NOTE: Each Program should be assembled and linked separately.
;-

    .TITLE      MWAITF.MAC
;-+
; Foresround Program ...
;-

    .MCALL      .RCVD,.MWAIT,.PRINT,.EXIT

MWAITF:   .RCVD      *AREA,*MBUFF,#40,       ;Request a message up to 80 char.
        ;          .                      ;No error possible - always a BG
        ;          .                      ;
        ;          .                      ;Do some other processing
        .PRINT     *FGJOB           ;like announcing FG active...
        ;          .                      ;
        ;          .                      ;
        .MWAIT                       ;Wait for message to arrive...
        TST         MBUFF+2           ;Null message?
        BEQ         FEXIT           ;Yes...exit the program
        .PRINT     *FMSG           ;Announce we got the message...
        .PRINT     *MBUFF+2           ;and echo it back
        BR         MWAITF           ;Loop to set another one

FEXIT:   .EXIT                     ;Exit Program
AREA:   .BLKW      5               ;EMT Argument Block
MBUFF:   .BLKW      41.           ;Buffer - Msg length + 1
        .WORD      0               ;Make sure 80 char message ends ASCIZ
FGJOB:   .ASCIZ      /Hi - FG alive and well and waiting for a message!/
FMSG:   .ASCIZ      /Hey BG - Got your message it reads:/
        .END         MWAITF

    .TITLE      MWAITB.MAC
;-+
; Background Program - Send a 'null' message to stop both Programs
;-

    .MCALL      .SDAT,.MWAIT,.GTLIN,.EXIT,.PRINT

MWAITB:   CLR      BUFF             ;Clear 1st word
        .GTLIN     *BUFF,*PROMT       ;Get something to send to FG from TTY
        .SDAT     *AREA,*BUFF,#40,       ;Send input as message to FG
        BCS         1$                 ;Branch on error - No FG
        .MWAIT                       ;Wait for message to be sent
```

TST BUFF ;Sent a null message?
BNE MWAITB ;No...loop to send another message.
.EXIT ;Yes...exit Program
1\$: PRINT #NDFG ;No FG !
.EXIT ;Exit Program
AREA: .BLKW 5 ;EMT Argument Block
BUFF: .BLKW 40, ;UP to 80 char message
PROMT: .ASCII /Enter message to be sent to FG Job/<15><12>/>/<200>
NOFG: .ASCIZ /?No FG?/
.END MWAITB

## 2.61 .PEEK/.POKE

The .PEEK programmed request returns in R0 the contents of a memory location; .POKE changes the contents of a memory location. The .POKE request also returns the old contents of the memory location in R0 to simplify the saving and restoring of a location. .PEEK and .POKE must be used in an XM environment to change memory locations that are not defined as monitor fixed offsets, and should be used with all RT-11 monitors for compatibility.

Although .PEEK and .POKE may seem very similar to .GVAL and .PVAL, respectively, they are different in the way they refer to locations. .GVAL and .PVAL access only monitor fixed offsets. All offsets used by .GVAL and .PVAL are calculated relative to the base of the resident monitor. Addresses used by .PEEK and .POKE, on the other hand, are simply memory addresses. Although .PEEK and .POKE can be used to access monitor fixed offsets, this requires that you find the base address of RMON, add the offset value, and use the resulting address as an argument to .PEEK or .POKE.

Macro Calls: .PEEK area,address

## .POKE area, address,value

where:

area is the address of a two- or three-word EMT argument block

address is the address of the location to examine or change

value is the new contents to place in the location

Request Format for .PEEK:

<table><tr><td rowspan="2">R0 → area:</td><td>34</td><td>1</td></tr><tr><td colspan="2">address</td></tr></table>

Request Format for .POKE:

<table><tr><td>34</td><td>3</td></tr><tr><td colspan="2">address</td></tr><tr><td colspan="2">value</td></tr></table>

Errors:

None.

## Example:

```asm
;Example of ,PEEK and ,POKE programmed requests.
;This example illustrates a way of reading and setting
;the default file size used by the .ENTER request.
;Normally, this would be done using the .GVAL and .PVAL programmed
;requests. (Refer to the example siven for the .PVAL request.) This
;example computes the address of the word in RMON containing the
;default file size used by the .ENTER request and uses .POKE
;both to change the default file size to 100, blocks and to return
;the old default file size in RO.
;
    .MCALL   .PEEK,   .POKE, .EXIT
    RMON=    54
    MAXBLK= 314

START:    .PEEK   #EMTBLK,#RMON          ;Pick up base of RMON from loc, 54
    ADD     #MAXBLK,RO           ;Add fixed offset of default file size,
    MOV     RO,      R1
    .POKE   #EMTBLK,R1,#NEWSIZ       ;Set a new default file size, return old
    MOV     RO,      OLDSIZ       ;default file size in RO and save the old size
    .EXIT                       ;We'll just exit now, but Presumably
                        ;in a real program we'd do more
                        ;processing, perhaps creating files
                        ;with the new default size we just set, then
                        ;before exiting we'd restore the old
                        ;default size.
                        ;EMT area

EMTBLK:   .BLKW   3                      ;EMT area
NEWSIZ:   .WORD   100..
OLDSIZ:   .WORD   0                      ;The old default size is saved here.

        .END     START
```

## 2.62 .POKE

Refer to .PEEK/.POKE (Section 2.61).

## 2.63 .PRINT

The .PRINT request causes output to be printed at the console terminal. The string to be printed can be terminated with either a null (0) byte or a 200 byte. If the null (ASCIZ) format is used, the output is automatically followed by a carriage return/line feed combination. If a 200 byte terminates the string, no carriage return/line feed combination is generated.

Control returns to the user program after all characters have been placed in the output buffer.

When a foreground job is running and the job that is producing output changes, a B> or F> appears. Any text following the message has been printed by the job indicated (foreground or background) until another B> or F> is printed.

When a system job prints a message to the terminal, the message is preceded by logical-job-name.

If the foreground job issues a message using .PRINT, the message is printed immediately, no matter what the state of the background job. Thus, for urgent messages, the .PRINT request should be used (rather than .TTYOUT or .TTOUTR). The .PRINT request forces a console switch and guarantees printing of the input line. If a background job is doing a prompt and has printed an asterisk but no carriage return/line feed combination, the console belongs to the background and .TTYOUTs from the foreground are not printed until a carriage return is typed to the background. A foreground job can force its message through by doing a .PRINT instead of the .TTYOUT.

Macro Call: .PRINT addr

where:

addr is the address of the string to be printed

Errors:

None.

Example:

```txt
,TITLE PRINT.MAC
;+
; .PRINT - This is an example in the use of the .PRINT request.
; The example merely accepts input from the console terminal and
; echoes it back.
;-
,MCALL ,GTLIN,,PRINT,,EXIT
START: .GTLIN #BUFF,#PROMT ;Get a line of input from keyboard
TSTB BUFF ;Nothing entered?
BEQ 1\$ ;Branch if nothing entered
.PRINT #BUFF ;Echo the input back
CLRB BUFF ;Clear first char of buffer
BR START ;Go back for more
1$: .EXIT ;Exit Program on null input
BUFF: .BLKW 41. ;80 character buffer (ASCIZ for .PRINT)
PROMT: .ASCII /Enter something/<15><12>/>/<200>
.END START
```

## 2.64 .PROTECT/.UNPROTECT (FB and XM Only)

.PROTECT

The .PROTECT request allows a job to obtain exclusive control of a vector (two words) in the region 0 to 474. If the request is successful, it indicates that the locations are not currently in use by another job or by the monitor. The job then can place an interrupt address and priority into the protected locations and begin using the associated device.

Macro Call: .PROTECT area,addr

## where:

area is the address of a two-word EMT argument block

addr is the address of the word pair to be protected

## NOTE

The argument addr must be a multiple of four, and must be less than or equal to 474(octal). The two words at addr and addr+2 are protected.

Request Format:

[figure omitted]

Errors:

Code Explanation

0 Protect failure; locations already in use.

1 Address (addr) is greater than 474 or is not a multiple of 4.

## Example:

```prolog
;+
; .PROTECT / .UNPROTECT - This is an example in the use of the .PROTECT
; and .UNPROTECT requests. The example illustrates how to protect the
; vectors of a device while an inline interrupt service routine does
; a data transfer (in this case the device is a DL11 Serial Line Interface),
; When the program is finished, the vectors are unprotected for possible
; use by another job.
;-
```

```asm
.MCALL .DEVICE,.EXIT,.PROTECT,.UNPROTECT,.PRINT
START: .DEVICE *AREA,*LIST iSetup to disable DL11 interrupts on
;EXIT or ^C^C
.PROTECT *AREA,*300 iProtect the DL11 vectors
BCS BUSY ;Branch if already protected
; . ;Set up data to transmit over DL11
; .
JSR R5,DL11 ;Use DL11 xfer routine (see ,INTEN
;example)
.WORD 128. ;Arguments...Word count
.WORD BUFFER ;Data buffer addr
; . ;Continue Processing...
; .
FINI: .UNPROTECT #AREA,*300 ;...eventually to exit Program
.EXIT
BUSY: .PRINT #NOVEC iPrint error message...
.EXIT ;then exit
AREA: .BLKW 3 ;EMT Argument block
LIST: .WORD 176500 ;CSR of DL11
.WORD 0 ;Stuff it with 'O'
.WORD 0 ;List terminator
BUFFER:
.BREPT 8. ;Data to send over DL11
.ASCIZ /Hello DL11... Are You There ??/
.ENDR
NOVEC: .ASCIZ /?Vector already protected?/ ;Error message text
.END START
```

## .UNPROTECT

The .UNPROTECT request is the complement of the .PROTECT request. It cancels any protected vectors in the 0 to 476 area. An attempt to unprotect a vector that a job has not protected is ignored.

Macro Call: .UNPROTECT area,addr

where:

area is the address of a two-word EMT argument block addr is the address of the protected vector pair that is going to be canceled. The argument addr must be a multiple of four, and must be less than or equal to 474(octal)

Request Format:

[figure omitted]

Errors:

## Explanation

1 Address (addr) is greater than 474(octal) or is not a multiple of four.

Example:

Refer to the example for the .PROTECT request.

## 2.65 .PURGE

The .PURGE request deactivates a channel without performing a .HRESET, .SRESET, .SAVESTATUS, or .CLOSE request. .PURGE frees a channel without taking any other action. If a tentative file has been entered on the channel, the file is discarded. An attempt to purge an inactive channel is ignored.

## NOTE

Do not purge channel 17(octal) if your program is overlaid because overlays are read on that channel.

Macro Call: .PURGE chan

where:

chan is the number of the channel to be freed

Request Format:

[figure omitted]

Errors:

None.

Example:

```csv
,TITLE PURGE.MAC
;+

; .PURGE - This is an example in the use of the PURGE request.
; This example merges 2-6 files into 1 file, making use of ,SAVESTATUS
; and .REOPEN to read all input files on one channel. The .PURGE request
; is used to free the input channel after each transfer,
;-

,MCALL CSIGEN,,SAVESTATUS,,REOPEN,,CLOSE,,EXIT
```

```asm
.MCALL
.READW,,WRITW,,PRINT,,PURGE
ERRBYT
= 52
;Error byte loc in SYSCOM

START:
.CSIGEN
#DSPACE,*DEFEXT
;Get file spec,open files,load handlers
MOV
*3,R4
;R4 = 1st input channel
MOV
*AREA,R3
;R3 => EMT Argument block
MOV
*SAVBLK,R5
;R5 => Channel savestatus blocks
1$:
.SAVEST
R3,R4,R5
;Save channel status
BCS
2$
;Branch if channel never opened
ADD
#12,R5
;Adjust R5 to Point to next status block
INC
R4
;Bump R4 to = next input channel
CMP
*8,,R4
;Done all input channels?
BGE
1$
;Branch if not
2$:
MOV
*SAVBLK,R5
;R5 => to 1st saved channel status
BEQ
7$
;Branch if no input files
4$:
.REOPEN
R3,#3,R5
;Re-open input channel on Ch 3
CLR
BLK
;Start readings with block O
5$:
.READW
R3,#3,*BUFFER,#256,,BLK
;Read a block
BCC
6$
;Branch if no error
TSTB
@*ERRBYT
;Check if error = EOF
BNE
8$
;Branch if not EOF
.PURGE
*3
;Clear input channel for re-use
ADD
#12,R5
;Point R5 to next saved ch status
TST
@R5
;Any more input channels?
BNE
4$
;Branch if yes
.CLOSE
*0
;We're done,,,close output channel
.PRINT
*DONE
;Announce merge complete
.EXIT

6$:
.WRITW
R3,#0,*BUFFER,#256,,WBLK
;Write block just read
INC
WBLK
;Bump to next output block
INC
BLK
;same for input blk (doesn't affect C bit)
BCC
5$
;Branch if no error on write
MOV
*WERR,RO
;Write error - RO => message
BR
9$
;merge...
7$:
MOVE
*NDINP,RO
;RO => No input files message
BR
9$
;merge...
8$:
MOV
*RERR,RO
;RO => Read error message
9$:
.PRINT
;
Report error
.EXIT

;then exit program

AREA:
.BLKW
5
;EMT Argument block
BLK:
.WORD
0
;Current read block
WBLK:
.WORD
0
;Current write block

SAVBLK:: BLKW 30,
;Saved channel status area
DEFEXT:
.WORD 0,0,0,0
;No default extensions for CSIGEN

NOINP:
.ASCIZ /?No input files?/
;Error messages
WERR:
.ASCIZ /?Write Error?/
RERR:
.ASCIZ /?Read Error?/
DONE:
.ASCIZ /I-O Transfer Completed/
.EVEN

BUFFER:
.BLKW 256,
;I/O buffer

DSPACE = .
;
Handlers start here...

.END START
```

## 2.66 .PVAL

See .GVAL/.PVAL (Section 2.41).

## 2.67 .QELDF (Device Handler Only)

The .QELDF macro symbolically defines queue element offsets for the specified set of system generation special features. The queue element offsets generated by this macro are as follows:

Q.LINK = 0 (Link to next queue element)

Q.CSW = 2. (Pointer to channel status word)

```txt
Since the handler usually deals with queue element offsets relative to Q.BLKN, the .QELDF macro also defines the following symbolic offsets:
    Q$LINK = -4
    Q$CSW = -2
    Q$BLKN = 0
    Q$FUNC = 2
    Q$JNUM = 3
    Q$UNIT = 3
    Q$BUFF = 4
    Q$WCNT = 6
    Q$COMP = ^O10

    For SJ and FB systems:
        Q.ELGH = ^O16 (End of queue element; used to find length)
        For XM systems:
            Q.PAR = ^O16 (PAR1 relocation bias)
            Q$PAR = ^O12
            Q.ELGH = ^O24 (End of queue element; used to find length)
Example:
    Refer to the example following the description of .DRAST.
```

```python
Q.FUNC = 6.          (Special function code)
Q.JNUM = 7.          (Job number)
Q.UNIT = 7.          (Device unit number)
Q.BUFF = ^O10      (User virtual memory buffer address)
Q.WCNT = ^O12      (Word count)
Q.COMP = ^O14      (Completion routine code)
```

## 2.68 .QSET

The .QSET request allows additional entries to be made to the RT-11 I/O queue. A general rule to follow is that each program should contain one more queue element than the total number of I/O requests that will be active simultaneously on different channels. Timing and message requests such as .MRKT, .TWAIT, .SDAT/C, and .RCVD/C also require queue elements and must be considered when allocating queue elements for a program. Note that if synchronous I/O is done (such as .READW/.WRITW) and no timing requests are done, no additional queue elements need be allocated.

Each time .QSET is called, a specified contiguous area of memory is divided into seven-word segments (10-word [decimal] segments for the XM monitor) and is added to the queue for that job. .QSET can be called as many times as required. The queue set up by multiple .QSET requests is a linked list. Thus, .QSET need not be called with strictly contiguous arguments. The space used for the new elements is allocated from your program space. Care must be taken so that the program in no way alters the elements once they are set up. The .SRESET and .HRESET requests discard all user-defined queue elements; therefore any previous .QSET requests must be reissued. However, you must not specify the same space in two separate .QSET requests if there has been no intervening .SRESET or .HRESET request.

Care should also be taken to allocate sufficient memory for the number of queue elements requested. The elements in the queue are altered asynchronously by the monitor; if enough space is not allocated, destructive references occur in an unexpected area of memory. The monitor returns the address of the first unused word beyond the queue elements. Other restrictions on the placement of queue elements are that the USR must not swap over them and they must not be in an overlay region. For jobs that run under the XM monitor, queue elements must be allocated in the lower 28K words of memory, since they must be accessible in kernel mapping. In addition, the elements must not be in the virtual address space mapped by kernel PAR1, specifically the area from 20000 to 37776(octal).

## NOTE

Programs that are to run in XM as well as SJ or FB environments should allocate 10(decimal) words for each queue element. Alternatively, a program can specify the start of a large area and use the returned value in R0 as the top of the queue element.

The following programmed requests require queue elements:

.TWAIT      .READW   .WRITE    .SDAT
.MRKT       .RCVD     .WRITC   .SDATC
.READ       .RCVDC   .WRITW   .SDATW
.READC       .RCVDW

Macro Call: .QSET addr,len

where:

addr is the address at which the new elements are to start

len is the number of entries to be added. In the SJ and FB monitor, each queue entry is seven words long; hence the space set aside for the queue should be len\*7 words. In the XM monitor, 10(decimal) words per queue element are required

On completion, R0 contains the address of the first word beyond the allocated queue elements.

## Errors:

In an extended memory environment, an attempt to violate the PAR1 restriction results in a ?MON-F-addr error, which can be intercepted with a .SERR programmed request.

Example:

,TITLE QSET.MAC
;+
; .QSET - This is an example in the use of the .QSET request.
; The example illustrates a user implemented "Timed Read" to cancel an

<table><tr><td colspan="4">; input request after a specified time interval.</td></tr><tr><td colspan="4">;-</td></tr><tr><td></td><td>.MCALL</td><td colspan="2">.MRKT,.TTINR,.EXIT,.PRINT,.TTYOUT,.CMKT,.TWAIT,.QSET</td></tr><tr><td></td><td>LF = 12</td><td></td><td>;Line Feed</td></tr><tr><td></td><td>JSW = 44</td><td></td><td>;Job Status Word location</td></tr><tr><td></td><td>TCBIT$ = 100</td><td></td><td>;Return C-bit bit in JSW</td></tr><tr><td></td><td>TTSPC$ = 10000</td><td></td><td>;TTY Special Mode bit in JSW</td></tr><tr><td>START:</td><td>.QSET</td><td>#XQUE,#1</td><td>;Need an extra Q-Elem for this</td></tr><tr><td>1$:</td><td>MOV</td><td>*PROMT,RO</td><td>;Mainline - RO =&gt; Prompt</td></tr><tr><td></td><td>MOV</td><td>*BUFFER,R1</td><td>;R1 =&gt; Input buffer</td></tr><tr><td></td><td>CALL</td><td>TREAD$</td><td>;Do a &quot;timed read&quot;</td></tr><tr><td></td><td>BCS</td><td>2$</td><td>;C-bit set = Timed out</td></tr><tr><td></td><td>.PRINT</td><td>*LINE</td><td>;&quot;Process&quot; data...</td></tr><tr><td></td><td>BR</td><td>1$</td><td>;Go back for more</td></tr><tr><td>2$:</td><td>.PRINT</td><td>*TIMOUT</td><td>;Read timed out - could process</td></tr><tr><td></td><td>.EXIT</td><td></td><td>;Partial data but we&#x27;ll just exit</td></tr><tr><td></td><td colspan="3">;* TREAD$ - &quot;Timed Read&quot; Subroutine</td></tr><tr><td></td><td>;* Input:</td><td colspan="2">RO =&gt; Prompt Strings / RO = 0 if no Prompt</td></tr><tr><td></td><td colspan="3">;* R1 =&gt; Input Buffer</td></tr><tr><td></td><td>;* Output:</td><td colspan="2">Buffer contains input chars,.if any, terminated</td></tr><tr><td></td><td colspan="3">;* by a null char. C-Bit set if timed out</td></tr><tr><td>TREAD$:</td><td>TST</td><td>RO</td><td>;See if we have to prompt</td></tr><tr><td></td><td>BEQ</td><td>1$</td><td>;Branch if no...</td></tr><tr><td></td><td>.PRINT</td><td></td><td>;Output Prompt</td></tr><tr><td>1$:</td><td>CLR</td><td>TBYT</td><td>;Clear time-out flag</td></tr><tr><td></td><td>.MRKT</td><td>*TAREA,#TIME,#TOUT,#1</td><td>;Issue a .MRKT for 10 sec</td></tr><tr><td></td><td>BIS</td><td>*TCBIT$,@*JSW</td><td>;Set C-Bit bit in JSW (for F/B)</td></tr><tr><td></td><td>CLRB</td><td>@R1</td><td>;Start with &quot;empty&quot; buffer</td></tr><tr><td>TTIN:</td><td>.TWAIT</td><td>*AREA</td><td>;Wait so we don&#x27;t lock out BG</td></tr><tr><td></td><td>.TTINR</td><td></td><td>;Look for a character</td></tr><tr><td></td><td>BIT</td><td>#1,(PC)+</td><td>;Timed out?</td></tr><tr><td>TBYT:</td><td>.WORD</td><td>O</td><td>;Time-out flag</td></tr><tr><td></td><td>BNE</td><td>2$</td><td>;Branch if yes</td></tr><tr><td></td><td>BCS</td><td>TTIN</td><td>;Branch if input not complete</td></tr><tr><td></td><td>MOVB</td><td>RO,(R1)+</td><td>;Xfer 1st character</td></tr><tr><td></td><td>.CMKT</td><td>*TAREA,*0</td><td>;Cancel .MRKT</td></tr><tr><td>2$:</td><td>BIS</td><td>*TTSPC$,@*JSW</td><td>;Turn on TT: Special mode</td></tr><tr><td>3$:</td><td>.TTINR</td><td></td><td>;Flush TT: ring buffer</td></tr><tr><td></td><td>MOVB</td><td>RO,(R1)+</td><td>;Putting characters in user buffer</td></tr><tr><td></td><td>BCC</td><td>3$</td><td>;If more char, so set &#x27;em</td></tr><tr><td></td><td>CLRB</td><td>-(R1)</td><td>;Terminate input with null byte</td></tr><tr><td></td><td>BIC</td><td>*TCBIT$!TTSPC$,@*JSW</td><td>;Clear bits in JSW</td></tr><tr><td></td><td>ROR</td><td>TBYT</td><td>;Set carry if timed out</td></tr><tr><td></td><td>RETURN</td><td></td><td>;Return to caller</td></tr><tr><td>TOUT:</td><td>INC</td><td>TBYT</td><td></td></tr><tr><td></td><td>RETURN</td><td></td><td>;Leave completion code</td></tr><tr><td>XQUE:</td><td>.BLKW</td><td>10.</td><td>;Extra Q-Element</td></tr><tr><td>AREA:</td><td>.WORD</td><td>0,WAIT</td><td>;EMT Argument block for .TWAIT</td></tr><tr><td>TAREA:</td><td>.BLKW</td><td>4</td><td>;EMT Argument block for .MRKT</td></tr><tr><td>TIME:</td><td>.WORD</td><td>0,600.</td><td>;Time-out interval (10 sec)</td></tr><tr><td>WAIT:</td><td>.WORD</td><td>0,1</td><td>;1/60 sec wait between .TTINRs</td></tr><tr><td>LINE:</td><td>.ASCI1</td><td>/Not in stock - Part # /</td><td>;Dummy response</td></tr><tr><td>BUFFER:</td><td>.BLKB</td><td>81.</td><td>;User input buffer</td></tr><tr><td>PROMT:</td><td>.ASCIZ</td><td>/Enter Part # &gt;/&lt;200&gt;</td><td>;Prompt</td></tr><tr><td>TIMOUT:</td><td>.ASCIZ</td><td>/Timed read expired!/</td><td>;Too bad message</td></tr><tr><td></td><td>.END</td><td>START</td><td></td></tr></table>

## 2.69 .RCTRLO

The .RCTRLO request makes sure that the console terminal is able to print by resetting the CTRL/O switch for the terminal. A CTRL/O typed while output is directed to the console terminal inhibits the output from printing until either another CTRL/O is struck or the program resets the CTRL/O switch. Therefore, a program with a message that must appear at the console should reset the CTRL/O switch.

A program should also issue a .RCTRLO request whenever it changes the contents of the job status word (JSW). Issuing a .RCTRLO request updates the monitor's internal status information to reflect the current contents of the JSW.

Macro Call: .RCTRLO

Errors:

None.

Example:

[figure omitted]

## 2.70 .RCVD/.RCVDC/.RCVDW (FB and XM Only)

The .RCVD (receive data) request allows a job to read messages or data sent by another job in an FB environment.

There are three forms of the .RCVD request, and they are used with the .SDAT (send data) request. The send data-receive data request combination provides a general data/message transfer system for communication between a foreground and a background job. .RCVD requests can be thought of as .READ requests where data transfer is not from a peripheral device but from the other job in the system. Additional queue elements should be allocated for buffered I/O operations in .RCVD and .RCVDC requests (see the .QSET request). Under an FB monitor with the system job feature, .RCVD/C/W requests and .SDAT/C/W requests remain valid for sending messages between background and foreground jobs in addition to the general read and write capability available to all jobs.

Be particularly careful if you use both synchronous (.RCVDW and .SDATW) and asynchronous (.RCVDC and .SDATC) requests in the same program. If you issue a mainline .SDATW while there is a pending .RCVDC, the .SDATW will wait until the .RCVDC is satisfied. If the completion routine for the .RCVDC issues another .RCVDC, the mainline .SDATW will never complete. In general, you should avoid the use of both synchronous and asynchronous message requests in the same program.

.RCVD

This request is used to receive data and continue execution. The request is posted and the issuing job continues execution. When the job needs to have the transmitted message, an .MWAIT should be executed. This causes the job to be suspended until all .SDATx and .RCVDx requests for the job are complete.

Macro Call: .RCVD area,buf,wcnt

where:

area is the address of a five-word EMT argument block

buf is the address of the buffer into which the message length/message data is to be placed

wcnt is the number of words to be transferred

Request Format:

<table><tr><td rowspan="5">R0 → area:</td><td>26</td><td>0</td></tr><tr><td colspan="2">reserved</td></tr><tr><td colspan="2">buf</td></tr><tr><td colspan="2">wcnt</td></tr><tr><td colspan="2">1</td></tr></table>

Upon completion of the .RCVD, the first word of the message buffer contains the number of words transmitted. Thus, the space allocated for the message should always be at least one word larger than the actual message size expected. If the sending job attempts to send more words than the receiver specified in the wcnt argument of the .RCVD request, the first word of the buffer will contain the number of words that the sender specified, but only wcnt words will be actually transferred. The rest of the sender's message will be ignored.

The word count is a variable number, and as such, the .SDAT/.RCVD combination can be used to transmit a few words or entire buffers. The .RCVD operation is only complete when a .SDAT is issued from the other job.

Programs using .RCVD/.SDAT must be carefully designed to either always transmit/receive data in a fixed format or to have the capability of handling variable formats. Messages are all processed in first-in first-out order. Thus, the receiver must be certain it is receiving the message it actually wants. Message handling in the FB monitor does not check for a word count of zero before queuing a send or receive data request. Since RT-11 distinguishes a send from a receive by complementing the word count, a .SDAT of zero words is treated as a .RCVD of zero words. Avoid a word count of zero at all times when using a .RCVD request.

[figure omitted]

Errors:

Code

## Explanation

0 No other job exists in the system. (A job exists as long as it is loaded, whether or not it is active.)

Example:

Refer to the example for the .SDAT request.

## .RCVDC

The .RCVDC request receives data and enters a completion routine when the message is received. The .RCVDC request is posted and the issuing job continues to execute. When the other job sends a message, the completion routine specified is entered.

Macro Call: .RCVDC area, buf, wcnt, crtn

where:

area is the address of a five-word EMT argument block

buf is the address of the buffer into which the message length/message data is to be placed

wcnt is the number of words to be transmitted

crtn is the address of a completion routine to be entered

As in the .RCVD request, word 0 of the buffer contains the number of words transmitted when the transfer is complete.

## Request Format:

R0 → area:

Errors:

Code

## Explanation

0 No other job exists in the system. (A job exists as long as it is loaded, whether or not it is active.)

Example:

,TITLE RCVDC.MAC

```prolog
;+
; ,RCVDC - This is an example of the ,RCVDC request, The example
; is a simulation of a mainline Foresround program which is currently
; suspended waiting for a message from the Background, but which needs
; to close a file (Perhaps opened by a ,ENTER ?) before aborting from
; CTRL-C action. A completion routine periodically inspects the CTRL-C
; status word and resumes the mainline if double CTRL-C is entered.
; NOTE: This example MUST be run as a FG Job under an FB monitor,
;-
```

<table><tr><td rowspan="2"></td><td>.MCALL</td><td colspan="2">.SCCA,,RCVDC,,EXIT,,PRINT,,MRKT</td></tr><tr><td>.MCALL</td><td colspan="2">.QSET,,SPND,,RSUM</td></tr><tr><td rowspan="2">START:</td><td>.QSET</td><td>#QELEM,#1</td><td>;Allocate another Q-Element</td></tr><tr><td>.SCCA</td><td>*MAREA,#SCCA</td><td>;Inhibit ^C^C action by monitor</td></tr><tr><td rowspan="13">1$:</td><td>CALL</td><td>CWATCH</td><td>;Start &quot;watchdos&quot; completion rtne</td></tr><tr><td>.RCVDC</td><td>*MAREA,#MBUFF,#40.,#MESG</td><td>;Look for a message</td></tr><tr><td>;</td><td>,</td><td>;No errors - there&#x27;s always BG</td></tr><tr><td>;</td><td>,</td><td>;Other processing here...</td></tr><tr><td>;</td><td>,</td><td>;</td></tr><tr><td>.PRINT</td><td>#SLEEP</td><td>;Announce we&#x27;re soing to suspend</td></tr><tr><td>.SPND</td><td></td><td>;Suspend to wait for message</td></tr><tr><td>TST</td><td>SCCA</td><td>;We&#x27;ve been ,RSUMed,...^C^C hit??</td></tr><tr><td>BNE</td><td>CLOSE</td><td>;Branch if yes</td></tr><tr><td>;</td><td>,</td><td>;otherwise assume message came in...</td></tr><tr><td colspan="3">;&lt;process message here&gt;</td></tr><tr><td>;</td><td>,</td><td></td></tr><tr><td>BR</td><td>1$</td><td>;Loop...</td></tr><tr><td rowspan="2">CWATCH:</td><td>TST</td><td>SCCA</td><td>;Check if ^C^C entered...</td></tr><tr><td>BEQ</td><td>MARK</td><td>;Branch if no</td></tr><tr><td rowspan="2">MESG:</td><td></td><td>,RSUM</td><td>;Yes...wake up the mainline</td></tr><tr><td>RETURN</td><td></td><td>;then leave completion code</td></tr><tr><td rowspan="2">MARK:</td><td>.MRKT</td><td>*CAREA,#TIME,#CWATCH,#1</td><td>;Schedule to run asain in 10 sec.</td></tr><tr><td>RETURN</td><td></td><td>;then leave completion code</td></tr><tr><td rowspan="5">CLOSE:</td><td>.PRINT</td><td>*ABORT</td><td>;Announce we&#x27;re abortins</td></tr><tr><td>;</td><td>,</td><td>;Proceed with &quot;orderly&quot; abort</td></tr><tr><td colspan="3">;&lt;Output file(s) closed here&gt;</td></tr><tr><td>;</td><td>,</td><td></td></tr><tr><td>.EXIT</td><td></td><td>;Exit the program</td></tr><tr><td>QELEM:</td><td>.BLKW</td><td>7</td><td>;Extra Q-Element</td></tr><tr><td>MBUFF:</td><td>.BLKW</td><td>41.</td><td>;Message buffer</td></tr><tr><td>MAREA:</td><td>.BLKW</td><td>5</td><td>;EMT Argument blocks</td></tr><tr><td>CAREA:</td><td>.BLKW</td><td>4</td><td>;</td></tr><tr><td>TIME:</td><td>.WORD</td><td>0,600.</td><td>;Time out in 10 seconds</td></tr><tr><td>SCCA:</td><td>.WORD</td><td>0</td><td>;^C^C Status word</td></tr><tr><td>ABORT:</td><td>.ASCIZ</td><td colspan="2">/?! Abort Acknowledged...Closing Output File(s) !?/</td></tr><tr><td>SLEEP:</td><td>.ASCIZ</td><td colspan="2">/! Mainline Suspendins !/</td></tr><tr><td></td><td>.END</td><td colspan="2">START</td></tr></table>

## .RCVDW

.RCVDW is used to receive data and wait. A message request is posted and the job issuing the request is suspended until all pending .SDATx and .RCVDx requests for the job are complete. When the issuing job runs again, the message has been received, and word 0 of the buffer indicates the number of words transmitted.

Macro Call: .RCVDW area,buf,wcnt

## where:

area is the address of a five-word EMT argument block

buf is the address of the buffer into which the message length/message data is to be placed

wcnt is the number of words to be transmitted

## Request Format:

<table><tr><td rowspan="5">R0 → area:</td><td>26</td><td>0</td></tr><tr><td colspan="2">reserved</td></tr><tr><td colspan="2">buf</td></tr><tr><td colspan="2">wcnt</td></tr><tr><td colspan="2">0</td></tr></table>

Errors:

0 No other job exists in the system. (A job exists as long as it is loaded, whether or not it is active.)

Example:

Refer to the example for the .SDATW request.

## 2.71 .RDBBK (XM Only)

The .RDBBK macro defines symbols for the region definition block and reserves space for it. The .RDBBK automatically invokes .RDBDF.

Macro Call: .RDBBK rgsiz

where:

rgsiz is the size of the dynamic region needed (expressed in 32-word units)

Example:

See Chapter 4 of the RT-11 Software Support Manual for an example that uses the .RDBBK macro and a detailed description of the extended memory feature.

## 2.72 .RDBDF (XM Only)

The .RDBDF macro defines the symbolic offset names for the region definition block and the names for the region status word bit patterns. In addition, this macro also defines the length of the region definition block by setting up the following symbol:

```txt
R.GLGH = 6
```

The .RDBDF macro does not reserve space for the region definition block.

Macro Call: .RDBDF

The .RDBDF macro expands as follows:

```lua
R.GID = 0
R.GSIZ = 2
R.GSTS = 4
R.GLGH = 6
RS.CRR = 100000
RS.UNM = 40000
RS.NAL = 20000
```

## 2.73 .READ/.READC/.READW

Read operations for the three modes of RT-11 I/O are done using the .READ, .READC, and READW programmed requests.

In the case of .READ and .READC, additional queue elements should be allocated for buffered I/O operations (see the .QSET request).

Upon return from any .READ, .READC, or .READW programmed request, R0 contains the number of words requested if the read is from a sequential-access device (for example, paper tape). If the read is from a random-access device (disk or DECtape), R0 contains the actual number of words that will be read (.READ or .READC) or have been read (.READW). This number is less than the requested word count if an attempt is made to read past end-of-file, but a partial transfer of one or more blocks is possible. In the case of a partial transfer, no error is indicated if a read request is shortened. Therefore, a program should always use the returned word count as the number of words available.

For example, suppose a file is five blocks long (it has block numbers 0 to 4) and a request is issued to read 512(decimal) words, starting at block 4. Since 512 words is two blocks, and block 4 is the last block of the file, this is an attempt to read past end-of-file. The monitor detects this and shortens the request to 256(decimal) words. On return from the request, R0 contains 256, indicating that a partial transfer occurred. Also, since the request is shortened to an exact number of blocks, a request for 256 words either succeeds or fails, but cannot be shortened.

An error is reported if a read is attempted starting with a block number that is beyond the end-of-file. The carry bit is set, and error code 0 appears in byte 52. No data is transferred in this case, and R0 contains a zero.

.READ

The .READ request transfers to memory a specified number of words from the device associated with the specified channel. The channel is associated with the device when a .LOOKUP or .ENTER request is executed. Control returns to the user program immediately after the .READ is initiated, possibly before the transfer is completed. No special action is taken by the monitor when the transfer is completed.

Macro Call: .READ area,chan,buf,wcnt,blk

where:

area is the address of a five-word EMT argument block

chan is a channel number in the range 0-376(octal)

buf is the address of the buffer to receive the data read

wcnt is the number of words to be read

blk is the block number to be read. For a file-structured .LOOKUP, the block number is relative to the start of the file. For a non-file-structured .LOOKUP, the block number is the absolute block number on the device. Note that the first block of a file or device is block number 0. The user program normally updates blk before it is used again. If input is from TT: and blk=0, TT: issues an uparrow (^) prompt (This is true for all .READ requests.)

## Notes:

1. .READ and .READC requests instruct the monitor to do a read from the device by queuing a request for the device and immediately returning control to your program.

2. .READ and .READC requests execute as soon as all previous I/O requests to the device handlers have been completed. Note that a read from RK1: must wait for a previous read from RK0: to complete. This is a hardware restriction common to most disks because the controller looks at all I/O operations sequentially.

3. Read errors are returned from the .READ and .READC or the .WAIT request. Errors can occur on the read or on the wait, but only one error is returned. Therefore, the program must check for an error when the read is complete (.READ/BCS) and after the wait (.WAIT/BCS). The wait request returns an error, but it does not indicate which read caused the error.

Errors reported on the return from the read request are as follows:

a. Nonexistent device/unit

b. Nonexistent block

c. In general, errors that do not require data transfers but are controller errors or EOF errors

4. During the .READ and .READC requests, the monitor keeps track of errors in the channel status word. If an error occurs before the monitor can return to the caller, the error is reported on the return from the read request with the carry bit set and the error value in R0. If the error occurs after return from the read request, the error is reported on return from the next .WAIT, or the next .READ/.READC. Some errors can be returned from .READ/.READC requests immediately, before any I/O operation takes place. One condition that causes an immediate error return is an attempt to read beyond end-of-file.

5. If .READ/C/W requests are used to receive messages under a system job monitor, the buffer must be one word longer than the number of words expected to be read. Upon completion of the data transfer, the first word of the buffer will contain a value equal to the number of words actually transferred (as for .RCVD/C/W).

Request Format:

<table><tr><td rowspan="5">R0 → area:</td><td>10</td><td>chan</td></tr><tr><td colspan="2">blk</td></tr><tr><td colspan="2">buf</td></tr><tr><td colspan="2">wcnt</td></tr><tr><td colspan="2">1</td></tr></table>

When the user program needs to access the data read on the specified channel, a .WAIT request should be issued as a check that the data has been read completely. If an error occurred during the transfer, the .WAIT request indicates the error.

<table><tr><td></td><td>ENABL</td><td>LSB</td><td>;Enable local symbol block</td></tr><tr><td rowspan="3">START:</td><td>.CSIGEN</td><td>#DSPACE,#DEFEXT</td><td>;Use CSIGEN to set handlers, files</td></tr><tr><td>MOV</td><td>*AREA,R5</td><td>;R5 =&gt; EMT Argument list</td></tr><tr><td>CLR</td><td>IOBLK</td><td>;Start reads with Block #0</td></tr><tr><td rowspan="7">1$:</td><td>.READ</td><td>R5,*3</td><td>;Read a block...</td></tr><tr><td>BCS</td><td>6$</td><td>;Branch on error</td></tr><tr><td>;</td><td>.</td><td>;Then simulate</td></tr><tr><td>BIT</td><td>*1,IOBLK</td><td>;some other</td></tr><tr><td>BNE</td><td>2$</td><td>;meaningful(?)</td></tr><tr><td>.PRINT</td><td>*MESSG</td><td>;process...</td></tr><tr><td>;</td><td>.</td><td></td></tr><tr><td rowspan="9">2$:</td><td>.WAIT</td><td>*3</td><td>;Did read finish OK?</td></tr><tr><td>BCS</td><td>5$</td><td>;Branch if not (must be hard error!)</td></tr><tr><td>.WRITE</td><td>R5,*0</td><td>;Now write the block just read</td></tr><tr><td>BCS</td><td>3$</td><td>;Branch on error</td></tr><tr><td>INC</td><td>IOBLK</td><td>;Bump Block #</td></tr><tr><td>;</td><td>.</td><td>;We could do some more Processing here</td></tr><tr><td>;</td><td>.</td><td></td></tr><tr><td>.WAIT</td><td>*0</td><td>;Wait for write to finish</td></tr><tr><td>BCC</td><td>1$</td><td>;Branch if write was successful</td></tr><tr><td>3$:</td><td>MOV</td><td>*WERR,RO</td><td>;RO =&gt; Write error msg</td></tr><tr><td rowspan="2">4$:</td><td>.PRINT</td><td></td><td>;Report error</td></tr><tr><td>BR</td><td>7$</td><td>;Merge to exit program</td></tr><tr><td rowspan="2">5$:</td><td>MOV</td><td>*RERR,RO</td><td>;RO =&gt; Read error msg</td></tr><tr><td>BR</td><td>4$</td><td>;Branch to report error</td></tr><tr><td rowspan="4">6$:</td><td>TSTB</td><td>@*ERRBYT</td><td>;Read error...EOF?</td></tr><tr><td>BNE</td><td>5$</td><td>;Branch if not</td></tr><tr><td>.PRINT</td><td>*DONE</td><td>;Yes...announce completion</td></tr><tr><td>.CLOSE</td><td>*0</td><td>;Make output file permanent</td></tr><tr><td rowspan="2">7$:</td><td>.SRESET</td><td></td><td>;Dismiss fetched handlers</td></tr><tr><td>.EXIT</td><td></td><td>;then exit program</td></tr><tr><td>AREA::</td><td>.WORD</td><td>0</td><td>;EMT Area block</td></tr><tr><td rowspan="4">IOBLK:</td><td>.WORD</td><td>0</td><td>;Block #,</td></tr><tr><td>.WORD</td><td>BUFF</td><td>;Buffer addr &amp; word count</td></tr><tr><td>.WORD</td><td>25G.</td><td>;already fixed in block...</td></tr><tr><td>.WORD</td><td>0</td><td>;</td></tr><tr><td>BUFF:</td><td>.BLKW</td><td>25G.</td><td>;I/O buffer</td></tr><tr><td>DEFEXT:</td><td>.WORD</td><td>0,0,0,0</td><td>;No default extensions for CSIGEN</td></tr><tr><td>DONE:</td><td>.ASCIZ</td><td colspan="2">/I-O Transfer Complete/ ;Messages...</td></tr><tr><td>MESSG:</td><td>.ASCIZ</td><td colspan="2">&lt;15&gt;&lt;12&gt;/&lt; Simulating Mainline Processing &gt;/</td></tr><tr><td>WERR:</td><td>.ASCIZ</td><td colspan="2">/?Write Error?/</td></tr><tr><td rowspan="2">RERR:</td><td>.ASCIZ</td><td colspan="2">/?Read Error?/</td></tr><tr><td>.EVEN</td><td colspan="2"></td></tr><tr><td>DSPACE:</td><td>= .</td><td></td><td>;Handlers may be loaded starting here</td></tr></table>

Errors:

Code Explanation
0 Attempt to read past end-of-file.
1 Hard error occurred on channel.
2 Channel is not open.

Example:

,TITLE READ.MAC
;+
; .READ / .WRITE - This is an example in the use of the .READ / .WRITE
; requests. The example demonstrates asynchronous I/O where a mainline
; Program initiates input via .READ requests, does some other processing
; makes sure input has completed via the .WAIT request, then outputs
; the block just read. Another .WAIT is issued before the next read
; is issued to make sure the Previous write has finished. This example
; is another single file copy program, utilizing .CSIGEN to input the
; file specs, load the required handlers and open the files,
;-

.MCALL          .READ,.WRITE,.CLOSE,.PRINT
.MCALL          .CSIGEN,.EXIT,.WAIT,.SRESET

## .READC

The .READC request transfers a specified number of words from the indicated channel to memory. Control returns to the user program immediately after the .READC is initiated. Attempting to read past end-of-file also causes an immediate return, in this case with the carry bit set and the error byte set to 0. Execution of the user program continues until the .READC is complete, then control passes to the routine specified in the request. When an RTS PC is executed in the completion routine, control returns to the user program.

Macro Call: .READC area,chan,buf,wcnt,crtn,blk

## where:

area is the address of a five-word EMT argument block

chan is a channel number in the range 0–376(octal)

buf      is the address of the buffer to receive the data read

wcnt is the number of words to be read

crtn is the address of the user's completion routine. The address of the completion routine must be above 500(octal)

blk is the block number to be read. For a file-structured .LOOKUP, the block number is relative to the start of the file. For a non-file-structured .LOOKUP, the block number is the absolute block number on the device. The user program normally updates blk before it is used again

When a completion routine is called, error or end-of-file information for a channel is not cleared. The next .WAIT or .READ/.READC on the channel (from either mainline code or a completion routine) produces an immediate return with the C bit set and the error code in byte 52. The completion routine will never be entered if the .READC request returns an error.

Request Format:

R0 → area:

<table><tr><td>10</td><td>chan</td></tr><tr><td colspan="2">blk</td></tr><tr><td colspan="2">buf</td></tr><tr><td colspan="2">wcnt</td></tr><tr><td colspan="2">crtn</td></tr></table>

When a .READC completion routine is entered, the following conditions are true:

1. R0 contains the contents of the channel status word for the operation. If bit 0 of R0 is set, a hardware error occurred during the transfer; consequently, the data may not be reliable. The end-of-file bit, bit 13, may be set.

2. R1 contains the channel number of the operation. This is useful when the same completion routine is to be used for transfers on different channels.

```csv
.MCALL READC,WRITC,CLOSE,PRINT,CSIGEN,EXIT,WAIT,SRESET
```

3. On a file-structured transfer, a shortened read is reported when the .READC request is returned, not when the completion routine is called.

4. Registers R0 and R1 can be used by the routine, but all other registers must be saved and restored. Data cannot be passed between the main program and completion routines in any register or on the stack.

Errors:

Code Explanation

0 Attempt to read past end-of-file; no data was read.

1 Hard error occurred on channel.

2 Channel is not open.

Example:

```prolog
,TITLE READC.MAC
;+
; ,READC / .WRITC - This is an example in the use of the .READC / .WRITC
; requests. The example demonstrates event-driven I/O where a mainline
; Program initiates a file transfer and completion routines continue it
; while the mainline Proceeds with other Processes. The example is another
; single file COPY Program, utilizing .CSIGEN to input the file specs, load
; the required handlers and open the files.
;-
```

<table><tr><td rowspan="2"></td><td>ERRBYT</td><td>= 52</td><td>;Error Byte location in SYSCOM</td></tr><tr><td>,ENABL</td><td>LSB</td><td></td></tr><tr><td rowspan="4">START:</td><td>,CSIGEN</td><td>#DSPACE,#DEFEXT</td><td>;Use CSIGEN to set handlers, files</td></tr><tr><td>CALL</td><td>IOXFER</td><td>;Start I/O</td></tr><tr><td>,PRINT</td><td>#MESSG</td><td>;Now simulate other mainline process</td></tr><tr><td>MOV</td><td>#-1,R5</td><td>;</td></tr><tr><td rowspan="10">1$:</td><td>DEC</td><td>R5</td><td>;(Kill some time)</td></tr><tr><td>BNE</td><td>1$</td><td>;</td></tr><tr><td>TSTB</td><td>EOF</td><td>;Did I/O complete?</td></tr><tr><td>BEQ</td><td>1$</td><td>;No...do some more mainline work</td></tr><tr><td>INCB</td><td>EOF</td><td>;Check for read/write error</td></tr><tr><td>BEQ</td><td>WERR</td><td>;EOF = 0 = Write error</td></tr><tr><td>BLT</td><td>RERR</td><td>;EOF &lt; 0 = Read error</td></tr><tr><td>,CLOSE</td><td>#0</td><td>;EOF &gt; 0 = End of File</td></tr><tr><td>MOV</td><td>#DONE,RO</td><td>;RO =&gt; We&#x27;re done messg</td></tr><tr><td>BR</td><td>GBYE</td><td>;Merse to exit Program</td></tr><tr><td rowspan="2">WERR:</td><td>MOV</td><td>#WRERR,RO</td><td>;Set up error messages here...</td></tr><tr><td>BR</td><td>GBYE</td><td></td></tr><tr><td>RERR:</td><td>MOV</td><td>#RDERR,RO</td><td></td></tr><tr><td rowspan="3">GBYE:</td><td>,PRINT</td><td></td><td>;Print message</td></tr><tr><td>,SRESET</td><td></td><td>;Dismiss fetched handlers</td></tr><tr><td>,EXIT</td><td></td><td>;Exit Program</td></tr><tr><td rowspan="2">WRDONE:</td><td>,WAIT</td><td>#0</td><td>;Write compl rtne...write successful?</td></tr><tr><td>BCS</td><td>3$</td><td>;Branch if not...</td></tr><tr><td rowspan="4">IOXFER:</td><td>,READC</td><td>#AREA,#3,,,#4$</td><td>;Queue up a read</td></tr><tr><td>BCC</td><td>7$</td><td>;Branch if ok...</td></tr><tr><td>TSTB</td><td>@#ERRBYT</td><td>;Error - is it EOF?</td></tr><tr><td>BEQ</td><td>6$</td><td>;Branch if yes</td></tr><tr><td>2$:</td><td>DECB</td><td>EOF</td><td>;User EOF Flag to indicate hard error</td></tr><tr><td rowspan="2">3$:</td><td>DECB</td><td>EOF</td><td>;EOF = -2 Read err / = -1 Write err</td></tr><tr><td>RETURN</td><td></td><td>;Leave completion code</td></tr><tr><td rowspan="2">4$:</td><td>,WAIT</td><td>#3</td><td>;Compl rtne #2 - was read ok?</td></tr><tr><td>BCS</td><td>2$</td><td>;Branch if not</td></tr></table>

```csv
,WRITC #AREA,#0,,,#WRDONE ;Queue up a write...
BCS 3$ ;Branch if error
5$: INC BLOK ;Bump block # for next read
RETURN ;Leave Completion code...
6$: INCB EOF ;Set EOF flag
7$: RETURN ;then return
AREA: .WORD O ;EMT Area block
BLOK: .WORD O ;Block #,
.WORD BUFF ;Buffer addr & word count
.WORD 256. ;already fixed in block...
.WORD O ;Completion rtne addr
BUFF: .BLKW 256. ;I/O buffer
DEFEXT: .WORD 0,0,0,0 ;No default extensions for CSIGEN
DONE: .ASCIZ /I-O Transfer Complete/ ;Messages...
MESSG: .ASCIZ /< Simulating Mainline Processing >/
WRERR: .ASCIZ /?Write Error?/
RDERR: .ASCIZ /?Read Error?/
EOF: .BYTE O ;EOF flag
.EVEN
DSPACE = , ;Handlers may be loaded starting here
.END START
```

## .READW

The .READW request transfers a specified number of words from the indicated channel to memory. When the .READW is complete or an error is detected, control returns to the user program.

Macro Call: .READW area,chan,buf,wcnt,blk

## where:

area is the address of a five-word EMT argument block

chan is a channel number in the range 0–376(octal)

buf is the address of the buffer to receive the data read

wcnt is the number of words to be read; each .READ request can transfer a maximum of 32K words

blk is the block number to be read. For a file-structured .LOOKUP, the block number is relative to the start of the file. For a non-file-structured .LOOKUP, the block number is the absolute block number on the device. The user program normally updates blk before it is used again

Request Format:

<table><tr><td rowspan="5">R0 → area:</td><td>10</td><td>chan</td></tr><tr><td colspan="2">blk</td></tr><tr><td colspan="2">buf</td></tr><tr><td colspan="2">wcnt</td></tr><tr><td colspan="2">0</td></tr></table>

If no error occurred, the data is in memory at the specified address. In an FB environment, the other job can be run while the issuing job is waiting for the I/O to complete.

If a volume is opened with a non-file-structured lookup and the word count specified is greater than the number of words left on the volume, .READW returns a hard error.

Errors:

0 Attempt to read past end-of-file.

1 Hard error occurred on channel.

2 Channel is not open.

## Example:

,TITLE READW.MAC
;+
;,READW / ,WRITW - This is an example in the use of the ,READW / ,WRITW
; requests. The example is a single file copy program. The file specs
; are input from the console terminal, and the input & output files opened
; via the general mode of the CSI. The file is copied using synchronous
; I/O, and the output file is made permanent via the ,CLOSE request,
;-
,MCALL CSIGEN,,READW,,PRINT,,EXIT,,WRITW,,CLOSE,,SRESET

START:        .CSIGEN      #DSPACE,#DEXT
            CLR              IOBLK
            MOV             \*AREA,R5
READ:        .READW       R5,#3

BCC          2\$
TSTB         @#ERRBYT
BEQ           3\$
MOV           #RERR ,RO

1\$ : PRINT BR 4\$

2\$:          .WRITW      R5 ,#0
          INC           IOBLK
          BCC           READ
          MOV           #WERR ,RO
          BR           1\$

3\$:          ,CLOSE      #0
            ,PRINT     #DONE
4\$:          ,SRESET
            ,EXIT

## 2.74 .RELEAS

See .FETCH/.RELEAS (Section 2.34).

## 2.75 .RENAME

The .RENAME request changes the name of the file specified.

Macro Call: .RENAME area,chan,dblk

where:

area is the address of a two-word EMT argument block

chan is an unused channel number in the range 0–376(octal)

dblk is the address of a block that specifies the file to be renamed followed by the new file name

Request Format:

$$
\mathrm{R0} \rightarrow \text {area:} \boxed {\begin{array}{c c}4&\text {chan}\\\hline \text {dblk}\end{array}}
$$

The dblk argument consists of two consecutive Radix-50 device and file specifications. For example:

```csv
,RENAME #AREA,#7,#DBLK ;USE CHANNEL 7
BCS RNMERR ;NOT FOUND
.
.
.
DBLK: RAD50 /DT3/
,RAD50 /OLDFIL/
,RAD50 /MAC/
,RAD50 /DT3/
,RAD50 /NEWFIL/
,RAD50 /MAC/
```

The first string represents the file to be renamed and the device where it is stored. The second represents the new file name. If a file with the same name as the new file name specified already exists on the indicated device, it is deleted. The second occurrence of the device name DT3 is necessary for proper operation and should not be omitted. The specified channel is left inactive when the .RENAME is complete. .RENAME requires that the handler to be used be resident at the time the .RENAME request is made. If it is not, a monitor error occurs. Note that .RENAME is legal only on files on block-replaceable devices (disks and DECTape). In magtape operations, the handler returns an illegal operation code in byte 52 if a .RENAME request is attempted. A .RENAME request to other devices is ignored.

Files cannot be protected or unprotected using the .RENAME request. To change the protection status of a file, use the .FPROT request or the PROTECT and UNPROTECT commands.

File dates can be changed using the .SFDAT request.

Errors:

Code Explanation
0 Channel open.
1 File not found.
2 Invalid operation.
3 A file by that name already exists and is protected.
A RENAME was not done.

## Example:

.TITLE RENAME.MAC

;+
; .RENAME - This is an example in the use of the .RENAME request.
; The example renames a file according to filespecs input thru the
; .CSISPC request.
;-

.MCALL          .RENAME,.PRINT,.EXIT
.MCALL          .CSISPC,.FETCH,.SRESET

START: .CSISPC #FILESP,#DEFEXT ;Use .CSISPC to set file specs
.FETCH #HANLOD,#FILESP ;Get Handler from outspec
BCS 2\$ ;Branch if failed
MOV #FILESP,R2 ;R2 => Outspec
MOV #FILESP+46,R3 ;R3 => Inspec
MOV @R2,FILESP+36 ;Copy device spec to inspec
.REPT 4 ;Copy outspec behind inspec
MOV (R2)+,(R3)+ ;for ,RENAME,...
.ENDR
.RENAME #AREA,#0,#FILESP+36 ;Rename input file
BCC 1\$ ;Operation successful
DECB @@ERRBYT ;Make error code -1,0 or +1
BEQ 3\$ ;Branch if File-Not-Found
MOV #ILLOP,RO ;Illegal operation-set up msg
BR 5\$ ;Branch to report error
1\$: .SRESET ;Dismiss handlers
.EXIT ;Exit Program
2\$: MOV #NOHAN,RO ;Fetch failed-set up message
BR 5\$ ;Branch to report error
3\$: MOV #NOFIL,RO ;File not found-setup message
5\$: .PRINT ;Print error message
BR 1\$ ;Then exit via ,SRESET
AREA: .BLKW 5 ;EMT Argument block
DEFEXT: .WORD 0,0,0,0 ;No default extensions
NOFIL: .ASCIZ /?File not found?/ ;Error message text
ILLOP: .ASCIZ /?Illegal Operation?/
NOHAN: .ASCIZ /?,FETCH Failed?/
.EVEN
FILESP: .BLKW 39,\*2 ;CSISPC Input Area
HANLOD = ,
.END START ;Handlers can load here...

## 2.76 .REOPEN

The .REOPEN request associates the channel that was specified with a file on which a .SAVESTATUS was performed. The .SAVESTATUS/.REOPEN combination is useful when a large number of files must be operated on at one time. As many files as are needed can be opened with .LOOKUP, and their status preserved with .SAVESTATUS. When data is required from a file, a .REOPEN enables the program to read from the file. The .REOPEN need not be done on the same channel as the original .LOOKUP and .SAVESTATUS.

Macro Call: .REOPEN area,chan,cblk

where:

area is the address of a two-word EMT argument block

chan is a channel number in the range 0–376(octal)

cblk is the address of the five-word block where the channel status information was stored

Request Format:

[figure omitted]

Errors:

Code

## Explanation

0 The specified channel is in use. The .REOPEN has not been done.

Example:

Refer to the example for the .SAVESTATUS request.

## 2.77 .RSUM (FB and XM Only)

See .SPND/.RSUM (Section 2.89).

## 2.78 .SAVESTATUS

The .SAVESTATUS request stores five words of channel status information into a user-specified area of memory. These words contain all the information RT-11 requires to completely define a file. When a .SAVESTATUS is done, the data words are placed in memory, the specified channel is freed, and the file is closed. When the saved channel data is required, the .REOPEN request is used.

.SAVESTATUS can only be used if a file has been opened with .LOOKUP. If .ENTER was used, .SAVESTATUS is invalid and returns an error. Note that .SAVESTATUS is not valid for magtape or cassette files.

The .SAVESTATUS/.REOPEN requests are used together to open many files on a limited number of channels or to allow all .LOOKUPs to be done at once to avoid USR swapping.

While the .SAVESTATUS/.REOPEN combination is useful, care must be observed when using it. In particular, the following cases should be avoided:

1. If a .SAVESTATUS is performed and the same file is then deleted before it is reopened, it becomes available as an empty space that could be used by the .ENTER command. If this sequence occurs, the contents of the file supposedly saved changes.

2. Although the device handler for the required peripheral need not be in memory for execution of a .REOPEN, the handler must be in memory when a .READ or .WRITE is executed, or a fatal error is generated.

One of the more common uses of .SAVESTATUS and .REOPEN is to consolidate all directory access motion and code at one place in the program. All files necessary are opened and their status saved, then they are re-opened one at a time as needed. USR swapping can be minimized by locking in the USR, doing .LOOKUP requests as needed, using .SAVESTATUS to save the file data, and then unlocking the USR. The user should be aware of the consequences of locking in the USR in a foreground/background environment. If the background job locks in the USR when the foreground job requires it, the foreground job is delayed until the background job unlocks the USR.

Macro Call: .SAVESTATUS area,chan,cblk

where:

area is the address of a two-word EMT argument block

chan is a channel number in the range 0–376(octal)

cblk is the address of the five-word user memory block where the channel status information is to be stored

Request Format:

<table><tr><td rowspan="2">R0 → area:</td><td>5</td><td>chan</td></tr><tr><td colspan="2">cblk</td></tr></table>

The five words returned by .SAVESTATUS contain the following information:

| Name | Offset | Contents |
| --- | --- | --- |
| C.CSW | 0 | Channel status word |
| C.SBLK | 2 | Starting block number of this file, or 0 if non-file-structured |
| C.LENG | 4 | Length of file |
| C.USED | 6 | Highest block written |
| C.DEVQ | 10 | Number of pending requests |
| C.UNIT | 11 | Device unit number |

Errors:

## Explanation

0 The channel specified is not currently associated with any files; that is, a previous .LOOKUP on the channel was never done.

# 1 The file was opened with an .ENTER request, or a .SAVE-STATUS request was performed for a magtape or cassette file.

Example:

;+
; .SAVESTATUS / .REOPEN - This is an example in the use of the .SAVESTATUS
; /.REOPEN requests. These requests are most commonly used together to
; consolidate access to the USR at one place in the Program or if the
; Program must access more files than there are I/O channels available.
; Once a channel has been opened, its status may be saved, to be re-opened
; and used later as needed. This example merges 2-6 files into 1 file,
;-reading all input files on one channel,

.MCALL          .CSIGEN,.SAVESTATUS,.REOPEN,.CLOSE,.EXIT
.MCALL          .READW,.WRITW,.PRINT,.PURGE

<table><tr><td></td><td>ERRDIT</td><td>= 32</td><td>ERROR BYTE 10c in SYSCOM</td></tr><tr><td rowspan="4">START:</td><td>.CSIGEN</td><td>#DSPACE,#DEFEXT</td><td>!Get file specs,open files,load handlers</td></tr><tr><td>MOV</td><td>#3,R4</td><td>!R4 = 1st input channel</td></tr><tr><td>MOV</td><td>#AREA,R3</td><td>!R3 =&gt; EMT Argument block</td></tr><tr><td>MOV</td><td>#SAVBLK,R5</td><td>!R5 =&gt; Channel savestatus blocks</td></tr><tr><td rowspan="6">1$:</td><td>.SAVEST</td><td>R3,R4,R5</td><td>!Save channel status</td></tr><tr><td>BCS</td><td>2$</td><td>!Branch if channel never opened</td></tr><tr><td>ADD</td><td>#12,R5</td><td>!Adjust R5 to Point to next status block</td></tr><tr><td>INC</td><td>R4</td><td>!Bump R4 to = next input channel</td></tr><tr><td>CMP</td><td>#8.,R4</td><td>!Done all input channels?</td></tr><tr><td>BGE</td><td>1$</td><td>!Branch if not</td></tr><tr><td rowspan="2">2$:</td><td>MOV</td><td>#SAVBLK,R5</td><td>!R5 =&gt; to 1st saved channel status</td></tr><tr><td>BEQ</td><td>7$</td><td>!Branch if no input files</td></tr><tr><td rowspan="2">4$:</td><td>.REOPEN</td><td>R3,#3,R5</td><td>!Re-open input channel on Ch 3</td></tr><tr><td>CLR</td><td>BLK</td><td>!Start readings with block 0</td></tr><tr><td rowspan="11">5$:</td><td>.READW</td><td>R3,#3,#BUFFER,#25G.,BLK</td><td>!Read a block</td></tr><tr><td>BCC</td><td>6$</td><td>!Branch if no error</td></tr><tr><td>TSTB</td><td>@#ERRBYT</td><td>!Check if error = EOF</td></tr><tr><td>BNE</td><td>8$</td><td>!Branch if not EOF</td></tr><tr><td>.PURGE</td><td>#3</td><td>!Clear input channel for re-use</td></tr><tr><td>ADD</td><td>#12,R5</td><td>!Point R5 to next saved ch status</td></tr><tr><td>TST</td><td>@R5</td><td>!Any more input channels?</td></tr><tr><td>BNE</td><td>4$</td><td>!Branch if yes</td></tr><tr><td>.CLOSE</td><td>#0</td><td>!We&#x27;re done...close output channel</td></tr><tr><td>.PRINT</td><td>#DONE</td><td>!Announce merge complete</td></tr><tr><td>.EXIT</td><td></td><td>!Exit program</td></tr><tr><td rowspan="6">6$:</td><td>.WRITW</td><td>R3,#0,#BUFFER,#25G.,WBLK</td><td>!Write block just read</td></tr><tr><td>INC</td><td>WBLK</td><td>!Bump to next output block</td></tr><tr><td>INC</td><td>BLK</td><td>!same for input blk (doesn&#x27;t affect C bit)</td></tr><tr><td>BCC</td><td>5$</td><td>!Branch if no error on write</td></tr><tr><td>MOV</td><td>#WERR,RO</td><td>!Write error - RO =&gt; message</td></tr><tr><td>BR</td><td>9$</td><td>!merge...</td></tr><tr><td rowspan="2">7$:</td><td>MOV</td><td>#NOINP,RO</td><td>!RO =&gt; No input files message</td></tr><tr><td>BR</td><td>9$</td><td>!merge...</td></tr><tr><td>8$:</td><td>MOV</td><td>#RERR,RO</td><td>!RO =&gt; Read error msg</td></tr><tr><td rowspan="2">9$:</td><td>.PRINT</td><td></td><td>!Report error</td></tr><tr><td>.EXIT</td><td></td><td>!then exit program</td></tr><tr><td>AREA:</td><td>.BLKW</td><td>5</td><td>!EMT Argument block</td></tr><tr><td>BLK:</td><td>.WORD</td><td>0</td><td>!Current read block</td></tr><tr><td>WBLK:</td><td>.WORD</td><td>0</td><td>!Current write block</td></tr><tr><td>SAVBLK::</td><td>.BLKW</td><td>30.</td><td>!Saved channel status area</td></tr><tr><td>DEFEXT:</td><td>.WORD</td><td>0,0,0,0</td><td>!No default extensions for CSIGEN</td></tr><tr><td>NOINP:</td><td>.ASCIZ</td><td>/?No input files?/</td><td>!Error messages</td></tr><tr><td>WERR:</td><td>.ASCIZ</td><td>/?Write Error?/</td><td></td></tr><tr><td>RERR:</td><td>.ASCIZ</td><td>/?Read Error?/</td><td></td></tr><tr><td rowspan="2">DONE:</td><td>.ASCIZ</td><td>/I-O Transfer Completed/</td><td></td></tr><tr><td>.EVEN</td><td></td><td></td></tr><tr><td>BUFFER:</td><td>.BLKW</td><td>256.</td><td>!I/O buffer</td></tr><tr><td>DSPACE</td><td>= ,</td><td></td><td>!Handlers start here...</td></tr><tr><td></td><td>.END</td><td>START</td><td></td></tr></table>

2-114 Programmed Request Description and Examples
