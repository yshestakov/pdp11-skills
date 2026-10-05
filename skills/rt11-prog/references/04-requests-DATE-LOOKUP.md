# RT-11 PRM reference: Ch.2 programmed requests .DATE through .LOOKUP: .DELETE .DEVICE .DRAST .DRBEG .DRBOT .DRDEF .DREND .DRFIN .DRINS .DRSET .DRVTB .DSTATUS .ELAW .ELRG .ENTER .EXIT .FETCH/.RELEAS .FORK .FPROT .GMCX .GTIM .GTJB .GTLIN .GVAL/.PVAL .HERR/.SERR .HRESET .INTEN .LOCK/.UNLOCK .LOOKUP

Source: RT-11 Programmer's Reference Manual AA-H378C-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' sometimes reads as ',' (`,MCALL` = `.MCALL`), 'R0' as 'RO', '#' as '\*' or '*'. Verify exact macro expansions against `sysmac_v53.mac`.

Contents:
- 2.17 .DATE
- 2.18 .DELETE
- 2.19 .DEVICE (FB and XM Only)
- 2.20 .DRAST (Device Handler Only)
- 2.21 .DRBEG (Device Handler Only)
- 2.22 .DRBOT (Device Handler Only)
- 2.23 .DRDEF (Device Handler Only)
- 2.24 .DREND (Device Handler Only)
- 2.25 .DRFIN (Device Handler Only)
- 2.26 .DRINS
- 2.27 .DRSET (Device Handler Only)
- 2.28 .DRVTB (Device Handler Only)
- 2.29 .DSTATUS
- 2.30 .ELAW (XM Only)
- 2.31 .ELRG (XM Only)
- 2.32 .ENTER
- 2.33 .EXIT
- 2.34 .FETCH/.RELEAS
- 2.35 .FORK (Device Handler and Interrupt Service Routine Only)
- 2.36 .FPROT
- 2.37 .GMCX (XM Only)
- 2.38 .GTIM
- 2.39 .GTJB
- 2.41 .GVAL/.PVAL
- 2.42 .HERR/.SERR
- 2.43 .HRESET
- 2.44 .INTEN
- 2.45 .LOCK/.UNLOCK
- 2.46 .LOOKUP
- 2.46.1 Standard Lookup
- 2.46.2 System Job Lookup

---

## 2.17 .DATE

This request returns the current date information from the system date word in R0. The date word returned is in the following format:

```txt
BIT: 15 14 13 ... 10 9 ... 5 4 ... 0
0 0 MONTH DAY YEAR
```

The year value in bits 4–0 is the actual year minus 1972. The day in bits 9 to 5 is a number from 1 to the length of the month. The month in bits 13 to 10 is a number from 1 to 12.

## NOTE

RT-11 support of month and year rollover is a system generation special feature; otherwise, the keyboard monitor DATE command must be issued to change the month and year.

Macro Call: .DATE

Request Format:

```txt
R0 = 12 0
```

Errors:

No errors are returned. A zero result in R0 indicates that the user has not entered a date.

Example:

```txt
,TITLE DATE.MAC

;+
; .DATE - This is an example in the use of the .DATE request,
; This example may be assembled separately and linked with
; user written Programs

;
; INPUT:                 none
;
; OUTPUT:               R0 = MONTH (1-12)
;                      R1 = DAY (1-31)
;                      R2 = YEAR (Last two digits)
;
```

<table><tr><td rowspan="15">DATE::</td><td>.DATE</td><td></td><td>;Get date in RO via ,DATE request</td></tr><tr><td>MOV</td><td>RO,R2</td><td>;Copy RO</td></tr><tr><td>BEQ</td><td>1$</td><td>;If zero, no date was entered</td></tr><tr><td>BIC</td><td>#^C37,R2</td><td>;Clear all but year bits</td></tr><tr><td>ADD</td><td>#72.,,R2</td><td>;Make it current year</td></tr><tr><td>MOV</td><td>RO,R1</td><td>;Copy date word again</td></tr><tr><td>ASL</td><td>R1</td><td>;Get day bits</td></tr><tr><td>ASL</td><td>R1</td><td>;on a byte boundary...</td></tr><tr><td>ASL</td><td>R1</td><td>;</td></tr><tr><td>SWAB</td><td>R1</td><td>;Put day bits in low order byte</td></tr><tr><td>BIC</td><td>#^C37,R1</td><td>;Clear all but day bits</td></tr><tr><td>SWAB</td><td>RO</td><td>;Put month bits in low byte</td></tr><tr><td>ASR</td><td>RO</td><td>;Right adjust</td></tr><tr><td>ASR</td><td>RO</td><td>;month bits...</td></tr><tr><td>BIC</td><td>#^C17,RO</td><td>;Clear all but month bits</td></tr><tr><td>1$:</td><td>RETURN</td><td></td><td>;Return to calling program</td></tr><tr><td></td><td>.END</td><td></td><td></td></tr></table>

## 2.18 .DELETE

The .DELETE request deletes a named file from an indicated device. The .DELETE request is invalid for magtapes. The .SERR programmed request can be used to allow the program to process any errors.

Macro Call: .DELETE area,chan,dblk[,seqnum]

where:

area is the address of a three-word EMT argument block

chan is the device channel number in the range 0-376(octal)

dblk is the address of a four-word Radix-50 descriptor of the file to be deleted

seqnum file number for cassette operations: if this argument is blank, a value of 0 is assumed

Request Format:

<table><tr><td>0</td><td>chan</td></tr><tr><td colspan="2">dblk</td></tr><tr><td colspan="2">seqnum</td></tr></table>

Notes:

The channel specified in the .DELETE request must not be open when the request is made, or an error will occur. The file is deleted from the device, and an empty (UNUSED) entry of the same size is put in its place. A .DELETE issued to a non-file-structured device is ignored. .DELETE requires that the handler to be used be in memory at the time the request is made. When the .DELETE is complete, the specified channel is left inactive.

0 Channel is active.

1 File was not found in the device directory.

2 Invalid operation.

3 The file is protected and cannot be deleted.

## Example:

```asm
,TITLE DELETE.MAC
;+
; .DELETE - This is an example in the use of the .DELETE request.
; The example uses the "special" mode of CSI to set an input
; specification from the console terminal, then uses the .DSTATUS
; request to determine if the output device's handler is loaded;
; if not, a .FETCH request is issued to load the handler into
; memory. Finally a .DELETE request is issued to delete the specified
; file.
;-
.MCALL .DSTATUS,.PRINT,.EXIT,.FETCH,.CSISPC,.DELETE
START: MOV SP, R5 ;Save current stack pointer
.CSISPC *OUTSP,#DEFEXT ;Use .CSISPC to set output spec
MOV R5, SP ;Restore SP to clear any CSI options
.DSTAT *STAT,#OUTSP ;Check on the output device
;(CSISPC catches illegal devices!)
TST STAT+4 ;See if the device is resident
BNE 2$ ;Branch if already loaded
.FETCH *HANLOD,#INSPEC ;It's not loaded...bring it into memory
BCC 2$ ;Branch if successful
.PRINT *FEFAIL ;Fetch failed...Print error message
.EXIT ;then exit program
2$: .DELETE *AREA,#0,#INSPEC ;Now delete the file
BCC 3$ ;Branch if successful
.PRINT *NOFIL ;Print error message
BR START ;Then try again
3$: .PRINT *FILDEL ;Acknowledge successful deletion
.EXIT ;then exit program
AREA: .BLKW 2 ;EMT Argument block
STAT: .BLKW 4 ;Block for status
DEFEXT: .WORD 0,0,0,0 ;No default extensions
FEFAIL: .ASCIZ /?,FETCH Failed?/ ;Fetch failed message
NOFIL: .ASCIZ /?File Not Found?/ ;File not found
FILDEL: .ASCIZ /!File Deleted!/ ;Delete acknowledgment
.EVEN ;Fix boundary
OUTSP: .BLKW 5*3 ;Output specs go here
INSPEC: .BLKW 4*6 ;Input specs go here
HANLOD: .BLKW 1 ;Handlers begin loading here (if necessary)
.END START
```

## 2.19 .DEVICE (FB and XM Only)

This request allows your program to load device registers with any necessary values when the program is terminated. You set up the list of addresses with the specified values. Upon issuing an .EXIT request or a CTRL/C from the terminal, this list is picked up by the system and the designated addresses are loaded with the corresponding values. This function is primarily designed to allow your program to turn off a device's interrupt enable bit when the program servicing the device terminates.

Successive calls to .DEVICE are allowed when you need to link requested tables. When the job is terminated for any reason, the list is scanned once. At that point, the monitor disables the feature until another .DEVICE call is executed. Thus, background programs that are reenterable should include .DEVICE as a part of the reenter code.

The .DEVICE request is ignored when it is issued by a virtual job running under the XM monitor.

Macro Call: .DEVICE area,addr[,link]

where:

area is the address of a two-word EMT argument block

addr is the address of a list of two-word elements, each composed of a one-word address and a one-word value to be put at that address. If addr is #0, any previous list is discarded; in this form, the argument link must be omitted

link is an optional argument that, if present, specifies linking of tables on successive calls to .DEVICE. If the argument is omitted, the list referenced in the previous .DEVICE request is replaced by the new list. The argument must be supplied to cause linking of lists; however, linked and unlinked list types cannot be mixed

Request Format:

NOTE

[figure omitted]

The list referenced by addr must be in either linking or non-linking format. The different formats are shown below. Both formats must be terminated with a separate, zero-value word. Linking format must also have a zero-value word as its first word.

[figure omitted]

Example:

```asm
;+
; .DEVICE - This is an example in the use of the .DEVICE request.
; The example shows how .DEVICE is used to disable interrupts from
; a device upon termination of the program. In this case the device
; is a DL11 Serial Line Interface.
;-

        .MCALL      .DEVICE,,EXIT,,PROTECT,,UNPROTECT,,PRINT
        .GLOBL      DL11
START:    .DEVICE     *AREA,*LIST          ;Setup to disable DL11 interrupts on
                                   ;.EXIT or ^C^C
        .PROTECT   *AREA,*300         ;Protect the DL11 vectors
        BCS       BUSY               ;Branch if already protected
        ;          .                       ;Set up data to transmit over DL11
        ;          .
        JSR           R5,DL11             ;Use DL11 xfer routine (see .INTEN example)
        .WORD      128.                 ;Arguments...Word count
        .WORD      BUFFER              ;Data buffer addr
        ;          .                       ;Continue processing,...
        ;          .
FINI:    .UNPROTECT *AREA,*300         ;...eventually to exit program
        .EXIT
BUSY:    .PRINT     *NOVEC            ;Print error message...
        .EXIT                     ;then exit
AREA:    .BLKW     3             ;EMT Argument block
LIST:    .WORD      176500         ;CSR of DL11
        .WORD      0                   ;Fill it with 'O'
        .WORD      0                   ;List terminator
BUFFER:                ;Data to send over DL11
        .REPT      8.                 ;8 lines of 32 characters...
        .ASCIZ     /Hello DL11... Are You There ??/
        .ENDR

NOVEC:    .ASCIZ     /?Vector already protected?/ ;Error message text
        .END      START
```

## 2.20 .DRAST (Device Handler Only)

The .DRAST macro sets up the interrupt and abort entry points, lowers the processor priority, and references a global symbol \$INPTR, which contains a pointer to the \$INTEN routine in the resident monitor. This pointer is filled in by the bootstrap (for a system device) or at .FETCH time (for a data device).

Macro Call: .DRAST name,pri[,abo]

where:

name is the two-character device name

pri is the priority of the device, and also the priority at which the interrupt service code is to execute

abo is an optional argument that represents the label of an abort entry point. If you omit this argument, the macro generates an RTS PC instruction at the abort entry point, which is the word immediately preceding the interrupt entry point

```prolog
.TITLE SP.MAC
;+
; SP.MAC - This is an example of a simple, RT-11 device driver to illustrate
; the use of the .DRBEG, .DRAST, .DRFIN, .DREND, .FORK & .QELDF requests.
; This driver could be used to output to a serial ASCII Printer-terminal
; over a DL11 Serial Line Interface. To use this driver as an RT-11 device
; handler, simply install it via the INSTALL command (es, 'INSTALL SP'),
;-
```

## Example:

## ; INTERRUPT SERVICE ROUTINE

.DRAST SP,SP\$PRI ;Use .DRAST to define Int Svc Sect,
; ;MACRO expansion...
; RTS PC ;Abort Entry Point
;SPINT::JSR R5,@\$INPTR ;Do a .INTEN to alert monitor
; .WORD ^C&lt;SP$PRI*^040&gt;&^0340 ;and drop processor priority
MOV SPCQE,R4 ;R4 => Q-Element
TST @\*SP\$CSR ;Error?
BMI SPRET ;Yes...'hans' until read>
BIC \*100,@\*SP\$CSR ;Disable interrupts
.FORK SPFORK ;Continue at FORK level
SPNXT: TSTB @\*SP\$CSR ;Is device ready?
BPL SPRET ;No...so wait 'till it is
MOVB @Q\$BUFF(R4),@\*SP\$CSR+2 ;Xfer byte from buffer to DL-11
INC Q\$BUFF(R4) ;Bump the buffer Pointer
INC Q\$WCNT(R4) ;and the word count (it's negative!)
BEQ SPDUN ;Branch if done
BR SPNXT ;Try to output another character
SPERR: BIS \*IOERR,@Q\$CSW(R4) ;Set error bit in CSW
SPDUN: .DRFIN SP ;Use .DRFIN to return to Monitor
; ;MACRO expansion...

```asm
;     MOV     PC,R4          iCalculate PIC addr of current
;     ADD     *SPCQE-.,,R4         ;queue element pointer
;     MOV     @*54,R5          ;Put addr of base of RMON in R5
;     JMP     @^0270(R5)       ;Jump to handler completion in monitor

SPFORK:  .WORD      0,0,0,0           ;Fork Queue Element

    .DREND     SP              ;Use ,DREND to end code
                                      ;MACRO expansion...
;$INPTR::.WORD      0             ;Addr of .INTEN code in RMON
;$FKPTR::.WORD      0             ;Addr of .FORK processor in RMON
;$PEND ==  .
                                      ;End of driver

    .END
```

## 2.21 .DRBEG (Device Handler Only)

The .DRBEG macro sets up the information in block 0 and the first five words of the handler. This macro also generates the appropriate global symbols for your handler. Before you use .DRBEG, invoke .DRDEF to define xx\$CSR, xx\$VEC, xxDSIZ, and xxSTS (see Section 2.23).

Macro Call: .DRBEG name

where:

name is a two-character device name

Example:

Refer to the example for .DRAST.

## 2.22 .DRBOT (Device Handler Only)

The .DRBOT macro sets up the primary driver. A primary driver must be added to a standard handler for a data device to create a system device handler. The .DRBOT macro invokes the .DREND macro (see Section 2.24) to mark the end of the handler so that the primary driver is not loaded into memory during normal operations.

Macro Call: .DRBOT name,entry,read[,CONTROL = arg...,arg][,SIDES = n]

where:

name is the two-character device name

entry is the entry point of the software bootstrap routine

read is the entry point of the bootstrap read routine

CONTROL defines the types of controllers supported by this handler. The values for arg can be UBUS or QBUS. If CONTROL is omitted, both Unibus and Q-bus are assumed. This is correct for all supported handlers

SIDES specifies single- or double-sided diskettes. If omitted, single-sided diskettes are assumed. This is correct for all supported handlers

The .DRBOT macro puts a pointer to the start of the primary driver into location 62 of the handler file. It puts the length (in bytes) of the primary driver into location 64. Location 66 of the handler file contains the offset from the start of the primary driver to the start of the bootstrap read routine. The .DRBOT macro is called before the .DREND macro that you issue. The code for the primary driver is placed between the .DRBOT and .DREND calls.

Example:

Refer to the RT-11 Software Support Manual for an example showing the use of .DRBOT.

## 2.23 .DRDEF (Device Handler Only)

The .DRDEF macro sets up handler parameters, calls the driver macros from the library, and defines useful symbols.

Macro Call: .DRDEF name,code,stat,size,csr,vec

where:

name is the two-character device name

code is the numeric code that is the device identifier value for the device

stat is the device status bit pattern. The value for stat may use the following symbols:

FILST\$ = 100000 SPECL\$ = 10000 ABTIO\$ = 1000

size is the size of the device in 256-word blocks

csr is the default value for the device's control and status regis-
ter

vec is the default value for the device's vector

The .DRDEF macro performs the following operations:

1. A .MCALL is done for the following macros: .DRAST; .DRBEG; .DRBOT; .DREND; .DRFIN; .DRINS; .DRSET; .DRVTB; .FORK; .QELDF.

2. If the system generation conditionals TIM\$IT, MMG\$T, or ERL\$G are undefined in your program, they are defined as zero. If time-out support is selected, the .DRDEF macro does a .MCALL for the .TIMIO and .CTIMIO macros.

3. The .QELDF macro is invoked to define symbolic offsets within a queue element.

4. The symbols listed above are defined for the device status bits.

5. The following symbols are defined:

```txt
HDERR$=1                      ;HARD ERROR BIT IN THE CSW
EOF$=20000               ;END OF FILE BIT IN THE CSW
```

6. The symbol xxDSIZ is set to the value specified in size.

7. The symbol xx\$COD is set to the specified device identifier code.

8. The symbol xxSTS is set to the value of the device identifier code plus the status bits.

9. If the symbol xx\$CSR is not defined, it is set to the default csr value.

10. If the symbol xx\$VEC is not defined, it is set to the default vector value.

11. The symbols xx\$CSR and xx\$VEC are made global.

You should invoke the .DRDEF macro near the beginning of your handler, after all handler specific conditionals are defined.

Example:

Refer to the RT-11 Software Support Manual for an example showing the use of .DRDEF.

## 2.24 .DREND (Device Handler Only)

The .DREND macro generates the termination table for the termination section of the device handler.

Macro Call: .DREND name

where:

name is the two-character device name

The generation of the termination table, dependent upon certain conditions, is as follows:

<table><tr><td>Label</td><td colspan="2">Addresses</td></tr><tr><td>$RLPTR:</td><td>.WORD 0</td><td>($RELOC)</td></tr><tr><td>$MPPTR:</td><td>.WORD 0</td><td>($MPPHY)</td></tr><tr><td>$GTBYT:</td><td>.WORD 0</td><td>($GETBYT)</td></tr><tr><td>$PTBYT:</td><td>.WORD 0</td><td>($PUTBYT)</td></tr><tr><td>$PTWRD:</td><td>.WORD 0</td><td>($PUTWRD)</td></tr><tr><td>$ELPTR:</td><td>.WORD 0</td><td>($ERLOG)</td></tr><tr><td>$TIMIT:</td><td>.WORD 0</td><td>($TIMIO)</td></tr><tr><td>$INPTR:</td><td>.WORD 0</td><td>($INTEN)</td></tr><tr><td>$FKPTR:</td><td>.WORD 0</td><td>($FORK)</td></tr></table>

The generation of the labels depends upon the special features chosen during the system generation process. All the pointers in the termination section are initialized when the handler is loaded into memory with the .FETCH request. If the device handler is a system device, the pointers are initialized at boot time with the addresses shown in the address column.

The addresses are located within the monitor. The first five addresses are the locations of subroutines in the resident monitor that are available to device handlers in an extended memory environment. Device I/O time-out service is provided by \$TIMIO and error logging is provided by \$ERLOG. The \$INPTR and \$FKPTR labels are always filled in by a .FETCH or LOAD command.

Example:

Refer to the example for .DRAST.

## 2.25 .DRFIN (Device Handler Only)

The .DRFIN macro generates the instructions for the jump back to the monitor at the end of the handler I/O completion section. The macro makes the pointer to the current queue element a global symbol, and it generates position-independent code for the jump to the monitor. When control passes to the monitor after the jump, the monitor releases the current queue element.

Macro Call: .DRFIN name

where:

name is the two-character device name

Example:

Refer to the example for .DRAST.

## 2.26 .DRINS

The .DRINS macro sets up the installation code area in block 0 of a device handler. The .DRINS macro defines addresses that contain the CSR addresses listed by RESORC (display CSRs) and the CSR checked by the INSTALL keyboard command. The .DRINS macro also defines the system and data device installation entry points.

The .DRINS macro has the following syntax:

.DRINS name,&lt;csr,csr,...&gt;

where:

name represents the two-letter device mnemonic for the device whose handler installation code you are setting up.

csr represents a symbolic CSR address for that device. If more than one display CSR exists, separate them with commas and enclose the list in angle brackets (<>). With multiple display CSRs, you do not have to list the first CSR.

When the .DRINS macro is processed, the following addresses are defined based on the CSR addresses you supply.

INSCSR Installation check CSR

DISCSR First display CSR

DISCSn Subsequent display CSRs if any exist (n begins at 2 and is incremented by 1 for each subsequent display CSR)

In addition, the .DRINS macro sets the location counter to 200 (INSDAT =: 200) for the data device installation entry point, and defines the label INSSYS as 202 (INSSYS =: 202), the system device installation entry point.

The following example shows the installation code generated by a .DRINS macro used for a DX handler with two controllers.

```asm
.DRINS      DX,<DX$CS2>          ;GENERATE INSTALLATION CODE
                                ;FOR TWO-CONTROLLER RX01
.=172
        .WORD       O                  ;END OF LIST
DISCS2:   .WORD      DX$CS2           ;SECONDARY DISPLAY CSR
DISCSR:   .WORD      DX$CSR           ;PRIMARY DISPLAY CSR
INSCSR:   .WORD      DX$CSR           ;INSTALL CSR
INSDAT:
.=202
INSSYS:
.=200
```

The next example shows the installation code generated by a .DRINS macro used for a DU handler with three controllers.

```asm
,DRINS DU,<DU$CS2,DU$CS3> ;GENERATE INSTALLATION CODE
;FOR THREE-CONTROLLER
;MSCP DEVICE
.=170
,WORD 0 ;END OF LIST
DISCS3: ,WORD DU$CS3 ;THIRD DISPLAY CSR
DISCS2: ,WORD DU$CS2 ;SECONDARY DISPLAY CSR
DISCSR: ,WORD DU$CSR ;FIRST DISPLAY CSR
INSCSR: ,WORD DU$CSR ;INSTALL CSR
INSDAT:
.=202
INSSYS:
.=200
```

## 2.27 .DRSET (Device Handler Only)

The .DRSET macro sets up the option table for the SET command in block 0 of the device handler file. The option table consists of a series of four-word entries, one entry per option. Use this macro once for each SET option that is used. When used a number of times, the macro calls must appear one after another.

Macro Call: .DRSET option,val,rtn[,mode]

where:

option is the name of the SET option, such as WIDTH or CR. The name can be up to six alphanumeric characters long and should not contain any embedded spaces or tabs

val is a parameter that is passed to the routine in Register R3. It can be a numeric constant, such as minimum column width, or any one-word instruction that is substituted for an existing one in block 1 of the handler. It must not be a zero

rtn is the name of the routine that modifies the code in block 1 of the handler. The routine must follow the option table in block 0 and must not go above address 776

mode is an optional argument to indicate the type of SET parameter. A NO indicates that a NO prefix is valid for the option. NUM indicates that a decimal numeric value is required. OCT indicates that an octal numeric value is required. Omitting this argument indicates that the option takes neither a NO prefix nor a numeric argument

The .DRSET macro does an .ASECT and sets the location counter to 400 for the start of the table. The macro also generates a zero word for the end of the table and leaves the location counter there. Thus routines to modify codes are placed immediately after the .DRSET calls in the handler, and their location in block 0 of the handler file is made certain.

Example:

Refer to the RT-11 Software Support Manual for an example of .DRSET.

## 2.28 .DRVTB (Device Handler Only)

The .DRVTB macro sets up a table of three-word entries for each vector of a multivector device. The table entries contain the vector location, interrupt entry point, and processor status word. You must use this macro once for each device vector. The .DRVTB macros must be placed consecutively in the device handler between the .DRBEG macro and the .DREND macro. They must not interfere with the flow of control within the handler.

Macro Call: .DRVTB name,vec,int[,ps]

where:

name is the two-character device name. This argument must be blank except for the first-time use of .DRVTB

vec is the location of the vector, and must be between 0 and 474

int is the symbolic name of the interrupt handling routine. It must appear elsewhere in the handler code. It generally takes the form ddINT, where dd represents the two-character device name

ps is an optional value that specifies the low-order four bits of the new Processor Status Word in the interrupt vector. This argument defaults to zero if omitted. The priority bits of the PSW are set to 7 even if you omit this argument

## Example:

Refer to the RT-11 Software Support Manual for an example of .DRVTB.

## 2.29 .DSTATUS

This .DSTATUS request obtains information about a particular device.

Macro Call: .DSTATUS retspc,dnam

where:

retspc is the address of a four-word block that stores the status information

dnam is the address of a word containing the Radix-50 device name

.DSTATUS looks for the device specified by dnam and, if successful, returns four words of status starting at the address specified by retspc. The four words returned are as follows:

## Word 1 Status Word

Bits 0–7: The low-order byte contains a number that identifies the device in the system. The values are currently defined in octal as follows:

0 = RK05 Disk
1 = TC11 DECtape
2 = Error Logger
3 = Line Printer
4 = Console Terminal or Batch Handler
5 = RL01/RL02 Disk
6 = RX02 Diskette
7 = PC11 High-speed Paper Tape Reader and Punch
10 = Reserved (V2 PP handler)
11 = TU10 Magtape
12 = RF11 Disk
13 = TA11 Cassette
14 = Card Reader (CR11,CM11)
15 = Reserved
16 = RJS03/RJS04 Fixed-head Disk
17 = Reserved
20 = TJU16 Magtape
21 = RP02/RP03 Disk
22 = RX01 Diskette
23 = RK06/RK07 Disk
24 = Reserved
25 = Null Handler
26-30 = Reserved (DECnet)
31-33 = Reserved (CTS-300,LQ,LR,LS)
34 = TU58 DECtape II
35 = TS11 Magtape
36 = PDT-11/130
37 = PDT-11/150

41 = Serial Line Printer Handler (LS)

42 = Message Queue Handler (MQ)

44 = Down-line Load Handler (XT) (MRRT-11 only)

46 = Logical Disk Handler

50 = MSCP Class Disk Handler

52 = RX50 Diskette (Professional 325/350)

53 = RD50/RD51 Disk (Professional 350)

54 = Professional Interface (PI)

55 = Transparent Spooler (SP)

57 = Communication Port (Professional 325/350 or DL(V)-11)

Bit 8: 1 = Handler can access variable-sized volumes and supports .SPFUN 373

0 = All volumes used by this device are the same size

Bit 9: $1 =$ Enter handler at abort entry whenever program terminates for any reason

0 = Do not enter at abort entry point unless conditions for bit 11 are satisfied

Bit 10: 1 = Handler accepts .SPFUN requests (for example, MT, CT, DX)

0 = No .SPFUN requests accepted

Bit 11: 1 = Enter handler abort entry every time a job is aborted

0 = Handler abort entry taken only if there is an active queue element belonging to aborted job

Bit 12: $1 =$ Non RT-11 directory-structured device (magtape, cassette)

Bit 13: $1 =$ Write-only device (line printer, serial line printer)

Bit 14: 1 = Read-only device (card reader, paper tape reader)

Bit 15: 1 = Random-access device (disk, DECtape)

0 = Sequential-access device (line printer, paper tape, card reader, magtape, cassette, terminal)

## Word 2 Handler Size

The size of the device handler in bytes.

## Word 3 Load Address +6

Non-zero implies the handler is now in memory: zero implies that it must be fetched before it can be used. The address returned is the load address of the handler +6.

Word 4 Device Size
The size of the device (in 256-word blocks) for block-replaceable devices; 0 for sequential-access devices, the smallest-sized volume for variable-sized devices. The last block on the device is the device size -1.

The device name can be a user-assigned name. .DSTATUS information is extracted from the device handler. Therefore, this request requires the handler for the device to be present on the system device and installed on the system.

## Errors:

## Code Explanation

0 Device not found in tables.

## Example:

```asm
,TITLE  DSTAT.MAC
;+
; ,DSTATUS - This is an example in the use of the ,DSTATUS request.
; The example uses the "special" mode of CSI to get an input
; specification from the console terminal, then uses the ,DSTATUS
; request to determine if the output device's handler is loaded;
; if not, a .FETCH request is issued to load the handler into
; memory. Finally a .DELETE request is issued to delete the specified
; file.
;-

    ,MCALL      .DSTATUS,.PRINT,.EXIT,.FETCH,.CSISPC,.DELETE

START:     .CSISPC     #OUTSP,#DEFEXT       ;Use ,CSISPC to set output spec
        .DSTAT       #STAT,#OUTSP         ;Check on the output device
                                    ;(CSISPC catches illegal devices!)
        TST          STAT+4           ;See if the device is resident
        BNE            2$               ;Branch if already loaded
        .FETCH       #HANLOD,#INSPEC       ;It's not loaded...bring it into memory
        BCC            2$               ;Branch if successful
        .PRINT       #FEFAIL           ;Fetch failed...Print error message
        .EXIT                       ;then exit program
2$:       .DELETE     #AREA,#0,#INSPEC       ;Now delete the file
        BCC            3$               ;Branch if successful
        .PRINT       #NOFIL           ;Print error message
        BR            START           ;Then try again
3$:       .PRINT     #FILDEL           ;Acknowledge successful deletion
        .EXIT                       ;then exit program

AREA:     .BLKW      2               ;EMT Argument block
STAT:     .BLKW      4               ;Block for status
DEFEXT:     .WORD   0,0,0,0           ;No default extensions

FEFAIL:     .ASCIZ     /?,FETCH Failed?/       ;Fetch failed message
NOFIL:     .ASCIZ     /?File Not Found?/       ;File not found
FILDEL:     .ASCIZ     /!File Deleted!/       ;Delete acknowledgment
        .EVEN                       ;Fix boundary

OUTSP:     .BLKW      5*3               ;Output specs so here
INSPEC:     .BLKW      4*6               ;Input specs so here
HANLOD:     .BLKW      1               ;Handlers begin loading here (if necessary)
        .END       START
```

## 2.30 .ELAW (XM Only)

The .ELAW request eliminates a virtual address window. An implied unmapping of the window occurs when its definition block is eliminated.

Macro Call: .ELAW area[,addr]

where:

area is the address of a two-word EMT argument block

addr is the address of the window definition block for the window to be eliminated

Request Format:

[figure omitted]

Errors:

Code Explanation

3 An invalid window identifier was specified.

Example:

Refer to the example for the .CRAW request.

## 2.31 .ELRG (XM Only)

The .ELRG request directs the monitor to eliminate a dynamic region in physical memory and return it to the free list where it can be used by other jobs.

Macro Call: .ELRG area [,addr]

where:

area is the address of a two-word EMT argument block

addr is the address of the region definition block for the region to be eliminated. Windows mapped to this region are unmapped. The static region cannot be eliminated

## Request Format:

[figure omitted]

Errors:

Code Explanation

2 An invalid region identifier was specified.

Example:

Refer to the example for the .CRAW request.

## 2.32 .ENTER

The .ENTER request allocates space on the specified device and creates a tentative entry in the directory for the named file. The channel number specified is associated with the file.

<table><tr><td colspan="2">Macro Call: .ENTER area,chan,dblk,len[,seqnum]</td></tr><tr><td colspan="2">where:</td></tr><tr><td>area</td><td>is the address of a four-word EMT argument block</td></tr><tr><td>chan</td><td>is a channel number in the range 0-376(octal)</td></tr><tr><td>dblk</td><td>is the address of a four-word Radix-50 descriptor of the file to be operated upon</td></tr><tr><td>len</td><td>is the file size specification. If the argument is omitted, it is not set to 0 in area. An argument of #0 must be specified to accomplish this. If an argument is left blank, the corresponding location in area is assumed to be setThe value of this argument determines the file length allocation as follows:0 either half the largest empty entry or the entire second-largest empty entry, whichever is larger. (A maximum size for nonspecific .ENTER requests can be patched in the monitor by changing resident monitor offset 314; refer to the example for .PVAL)m a file of m blocks. The size, m, can exceed the maximum mentioned above-1 the largest empty entry on the device</td></tr><tr><td>seqnum</td><td>is a file number for magtape or cassette. Programming for specific devices such as magtape or cassettes is discussed in detail in Chapter 10 of the RT-11 Software Support Manual. For cassette operation, if this argument is blank, a value of 0 is assumedFor magtape, seqnum describes a file sequence number. The action taken depends on whether the file name is given or is null. The sequence number can have the following values:0 rewind the magtape and space forward until the file name is found or until logical end-of-tape is detected. If the file name is found, an error is generated. If the file name is not found, then enter file. If the file name is a null, a non-file-structured lookup is done (tape is rewound)n position magtape at file sequence number n if n is greater than zero and the file name is not null-1 space to the logical end-of-tape and enter file-2 rewind the magtape and space forward until the file name is found, or until logical end-of-tape is detected. The magtape is now positioned correctly. A new logical end-of-tape is implied</td></tr></table>

Request Format:

<table><tr><td rowspan="4">R0 → area:</td><td>2 chan</td></tr><tr><td>dblk</td></tr><tr><td>len</td></tr><tr><td>seqnum</td></tr></table>

On return from this call, R0 contains the size of the area actually allocated for use.

The file created with an .ENTER request is not a permanent file until a .CLOSE request is given on that channel. Thus, the newly created file is not available to .LOOKUP, and the channel cannot be used by .SAVE-STATUS requests. However, it is possible to read data that has just been written into the file by referencing the appropriate block number. When the .CLOSE to the channel is given, any existing permanent unprotected file of the same name on the same device is deleted and the new file becomes permanent. Although space is allocated to a file during the .ENTER operation, the actual length of the file is determined when .CLOSE is requested.

Each job can have up to 255 files open on the system at any time. If required, all 255 can be opened for output with the .ENTER function.

When an .ENTER request is made, the device handler must be in memory. Thus, a .FETCH should normally be executed before an .ENTER can be done.

## Notes:

When using the zero-length feature of .ENTER, keep in mind that the space allocated is less than the largest empty space. This can have an important effect in transferring files between devices (particularly DECTape and diskette) that have a relatively small capacity. For example, transferring a 200-block file to a diskette, on which the largest available empty space is 300 blocks, does not work with a zero-length .ENTER. Since the .ENTER allocates half the largest space, only 150 blocks are really allocated and an output error occurs during the transfer. When transferring from A to B, with the length of A unknown, do a .LOOKUP first. This request returns the length so that value can be used to do a fixed-length .ENTER. The .ENTER request generates hard errors when problems are encountered during directory operations. These errors can be detected after the operation with the .SERR request.

Errors:

Code Explanation

0 Channel is in use.

1 In a fixed-length request, no space greater than or equal to $m$ was found; or the device or the directory was found to be full.

3 A file by that name already exists and is protected. A new file was not opened.

## Example:

; .ENTER - This is an example in the use of the .ENTER request.

; The example makes a copy of the file 'TECO.SAV' on device DK:

<table><tr><td rowspan="3"></td><td>.MCALL</td><td colspan="2">LOOKUP,,ENTER,,WRITW,,READW,,CLOSE</td></tr><tr><td>.MCALL</td><td colspan="2">.PRINT,,EXIT</td></tr><tr><td colspan="3">ERRBYT=52</td></tr><tr><td rowspan="6">START:</td><td>.LOOKUP</td><td>*AREA,*,0,*TECO</td><td>!Lookup file TECO.SAV</td></tr><tr><td>BCS</td><td>5$</td><td>!Branch if not there!</td></tr><tr><td>MOV</td><td>RO,R3</td><td>!Copy size of file to R3</td></tr><tr><td>.ENTER</td><td>*AREA,*,1,*TFILE,R3</td><td>!Enter a new file of same size</td></tr><tr><td>BCS</td><td>6$</td><td>!Branch if failed</td></tr><tr><td>CLR</td><td>BLK</td><td>!Initialize block * to zero</td></tr><tr><td rowspan="6">1$:</td><td>.READW</td><td>*AREA,*,0,*BUFFER,#25G,,BLK</td><td>!Read a block</td></tr><tr><td>BCC</td><td>2$</td><td>!Branch if successful</td></tr><tr><td>TSTB</td><td>@#ERRBYT</td><td>!Was error EOF?</td></tr><tr><td>BEQ</td><td>3$</td><td>!Branch if yes</td></tr><tr><td>MOV</td><td>*RERR,RO</td><td>!Hard read error message to RO</td></tr><tr><td>BR</td><td>7$</td><td>!Branch to print message</td></tr><tr><td rowspan="5">2$:</td><td>.WRITW</td><td>*AREA,*,1,*BUFFER,#25G,,BLK</td><td>!Write a block</td></tr><tr><td>INC</td><td>BLK</td><td>!Bump block # (doesn&#x27;t affect C bit)</td></tr><tr><td>BCC</td><td>1$</td><td>!Branch if write was ok</td></tr><tr><td>MOV</td><td>*WERR,RO</td><td>!RO =&gt; Write error message</td></tr><tr><td>BR</td><td>7$</td><td>!Branch to print message</td></tr><tr><td rowspan="3">3$:</td><td>.CLOSE</td><td>#1</td><td>!Make new file permanent</td></tr><tr><td>MOV</td><td>*DONE,RO</td><td>!RO =&gt; Done message</td></tr><tr><td>BR</td><td>7$</td><td>!Branch to print message</td></tr><tr><td rowspan="2">5$:</td><td>MOV</td><td>*NOFIL,RO</td><td>!RO =&gt; File not found message</td></tr><tr><td>BR</td><td>7$</td><td>!Branch to print it</td></tr><tr><td>6$:</td><td>MOV</td><td>*NDENT,RO</td><td>!RO =&gt; Enter Failed message</td></tr><tr><td rowspan="2">7$:</td><td>.PRINT</td><td></td><td>!Print message on console terminal</td></tr><tr><td>.EXIT</td><td></td><td>!the exit program</td></tr><tr><td>AREA:</td><td>.WORD</td><td>0</td><td>!EMT Argument block</td></tr><tr><td>BLK:</td><td>.WORD</td><td>0,0,0,0</td><td>;</td></tr><tr><td>BUFFER:</td><td>.BLKW</td><td>25G.</td><td>!I/O Buffer</td></tr><tr><td rowspan="3">TECO:</td><td>.RAD50</td><td>/DK/</td><td>!File descriptors...</td></tr><tr><td>.RAD50</td><td>/TECO/</td><td></td></tr><tr><td>.RAD50</td><td>/SAV/</td><td></td></tr><tr><td rowspan="3">TFILE:</td><td>.RAD50</td><td>/DK/</td><td></td></tr><tr><td>.RAD50</td><td>/OLDTEC/</td><td></td></tr><tr><td>.RAD50</td><td>/SAV/</td><td></td></tr><tr><td>NOFIL:</td><td>.ASCIZ</td><td>/?File not found?/</td><td>!Message text...</td></tr><tr><td>NOENT:</td><td>.ASCIZ</td><td>/?,ENTER Failed?/</td><td></td></tr><tr><td>WERR:</td><td>.ASCIZ</td><td>/?Write Error?/</td><td></td></tr><tr><td>RERR:</td><td>.ASCIZ</td><td>/?Read Error?/</td><td></td></tr><tr><td rowspan="2">DONE:</td><td>.ASCIZ</td><td>/TECO Copy Complete/</td><td></td></tr><tr><td>.END</td><td>START</td><td></td></tr></table>

## 2.33 .EXIT

The .EXIT request causes the user program to terminate. When used from a background job under the FB monitor or XM monitor, or in SJ, .EXIT causes KMON to run in the background area. All outstanding mark time requests are canceled. Any I/O requests and/or completion routines pending for that job are allowed to complete. If part of the background job resides where KMON and USR are to be read and SET EXIT SWAP is in effect, the user job is written onto the system swap blocks (the file SWAP.SYS). KMON and USR are then loaded and control goes to KMON in the background area. If SET EXIT NOSWAP is in effect, the user program is simply overwritten when a .EXIT is done. If R0 = 0 when the .EXIT is done, an implicit .HRESET is executed when KMON is entered, disabling the subsequent use of REENTER, START, or CLOSE.

```asm
.=510
    .WORD B-A
A:   .ASCIZ /COPY A,MAC B,MAC/
    .ASCIZ /DELETE A,MAC/
```

The .EXIT request allows a user program to pass command lines to KMON in the chain information area (locations 500–777octal) for execution after the job exits. This is performed under the following conditions:

1. The word (not byte) location 510 must contain the total number of bytes of command lines to be passed to KMON.

2. The command lines are stored beginning at location 512. The lines must be .ASCIZ strings with no embedded carriage return or line feed. For example:

3. The user program must set bit 5 or bit 11 in the Job Status Word immediately before doing an .EXIT, which must be issued with R0 = 0.

When the .EXIT request is used to pass command lines to KMON, the following restrictions are in effect:

1. If bit 11 of the JSW is set and if the feature is used by a program that is invoked through an indirect file, the indirect file context is aborted before executing the supplied command lines. Any unexecuted lines in the indirect file are never executed.

2. If bit 5 of the JSW is set and the feature is used by a program invoked through an indirect file, the indirect file context is preserved across the .EXIT request.

3. An indirect file can be invoked, using the steps described above, only if a single line containing the indirect file specification is passed to KMON. Attempts to pass multiple indirect files or combinations of indirect command files and other KMON commands yield incorrect results. An indirect file must be the last item on a KMON command line.

The .EXIT request also resets any .CDFN and .QSET calls that were done and executes an .UNLOCK if a .LOCK has been done. Thus, the CLOSE command from the keyboard monitor does not operate for programs that perform .CDFN requests.

An attempt to use a .EXIT from a completion routine aborts the running job.

## NOTE

You must make sure that the data being passed to KMON is not destroyed during the .EXIT request. Extreme care should be exercised so that the user stack does not overwrite this data area. If the user passes command lines to KMON, the stack pointer should be reset to 1000(octal) or above before an exit is made.

Macro Call: .EXIT

Example:

;Chain bit in JSW
;JSW location
;RO => Communication area
;R1 => Command strings
;Make sure that the stack is
;not in the communication area...
;Copy command strings
;Done?
;Branch if not
;Set the "chain" bit to alert KMON that
;there's a command in the communication area
;RO must be zero !
;Exit the program

## 2.34 .FETCH/.RELEAS

The .FETCH request loads device handlers into memory from the system device.

Macro Call: .FETCH addr,dnam

where:

addr      is the address where the device handler is to be loaded

dnam is the pointer to the Radix-50 device name

The storage address for the device handler is passed on the stack. When the .FETCH is complete, R0 points to the first available location above the handler. If the handler is already in memory, R0 contains the same value that was initially specified in the argument addr. If the argument on the stack is less than 400(octal), it is assumed that a handler .RELEAS is being done. (.RELEAS does not dismiss a handler that was loaded from the KMON; an UNLOAD must be done.) After a .RELEAS, a .FETCH must be issued in order to use the device again.

Several requests require a device handler to be in memory for successful operation. These include:

| .CLOSE | .READC | .READ | .SFDAT |
| --- | --- | --- | --- |
| .LOOKUP | .WRITC | .WRITE | .FPROT |
| .ENTER | .READW | .SPFUN |  |
| .RENAME | .WRITW | .DELETE |  |

When running under the foreground/background monitor, handlers for the foreground program or a system job must be loaded with the LOAD command before execution.

## NOTE

I/O operations cannot be executed on devices unless the handler for that device is in memory.

Errors:

Code

## Explanation

0 The device name specified is not installed in the system, or there is no handler for that device in the system.

Example:

```asm
,TITLE  FETCH.MAC
;+
; .FETCH - This is an example in the use of the .FETCH request,
; The example uses the "special" mode of CSI to set an input
; specification from the console terminal, then uses the .DSTATUS
; request to determine if the output device's handler is loaded;
; if not, a .FETCH request is issued to load the handler into
; memory. Finally a .DELETE request is issued to delete the specified
; file.
;-

    .MCALL      .DSTATUS,.PRINT,.EXIT,.FETCH,.CSISPC,.DELETE

START:     .CSISPC   #OUTSP,#DEFEXT       #Use .CSISPC to set output spec
        .DSTAT     #STAT,#OUTSP          #Check on the output device
                                    #(CSISPC catches illegal devices!)
        TST         STAT+4              #See if the device is resident
        BNE         2$                    #Branch if already loaded
        .FETCH     #HANLOD,#INSPEC     #It's not loaded...bring it into memory
        BCC         2$                    #Branch if successful
        .PRINT     #FEFAIL             #Fetch failed...Print error message
        .EXIT                     #then exit Program
2$:     .DELETE   #AREA,#0,#INSPEC     #Now delete the file
        BCC         3$                    #Branch if successful
        .PRINT     #NOFIL            #Print error message
        BR         START           #Then try again
3$:     .PRINT   #FILDEL             #Acknowledge successful deletion
        .EXIT                     #then exit Program

AREA:     .BLKW      2                   #EMT Argument block
STAT:     .BLKW      4                   #Block for status
DEFEXT:     .WORD      0,0,0,0               #No default extensions

FEFAIL:     .ASCIZ   /?,FETCH Failed?/   #Fetch failed message
NOFIL:     .ASCIZ   /?File Not Found?/   #File not found
FILDEL:     .ASCIZ   /!File Deleted!/   #Delete acknowledgment
        .EVEN                     #Fix boundary

OUTSP:     = .BLKW    5*3                  #Output specs so here
INSPEC:    = .BLKW    4*6                  #Input specs so here
HANLOD:    = .BLKW    1                   #Handlers begin loading here (if necessary)
        .END      START
```

The .RELEAS request notifies the monitor that a fetched device handler is no longer needed. The .RELEAS is ignored if the handler is (1) the system device, (2) not currently resident, (3) resident because of a LOAD command

```asm
.TITLE    RELEAS.MAC
;In this example, the DECTape handler (DT) is loaded into memory,
;used, then released. If the system device is DECTape, the handler is
;always resident, and ,FETCH will return HSPACE in RO.

        .MCALL    ,FETCH,,RELEAS,,EXIT,,PRINT

START:    ,FETCH   #HSPACE,#DTNAME   ;Load DT handler
        BCS       FERR                  ;Not available

; Use handler

        ,RELEAS  #DTNAME               ;Mark DT no lonser in
                                ;memory

        BR      START
FERR:    ,PRINT   *NODT                 ;DT not available
DTNAME:   ,RAD50   /DT /                ;Name for DT handler
NODT:    ,ASCIZ   /?DT HANDLER NOT AVAILABLE/
        .EVEN

HSPACE:                                      ;Beginning of handler
                                ;area

        .END     START
```

None.

to the keyboard monitor. .RELEAS from the foreground or system job under the FB monitor or the XM monitor is always ignored, since the foreground job in a FB environment or extended memory environment can only use handlers that have been loaded by the LOAD command.

Macro Call: .RELEAS dnam

## where:

```txt
dnam is the address of the Radix-50 device name
```

## Errors:

## Code Explanation

0 Device name is invalid.

## Example:

## 2.35 .FORK (Device Handler and Interrupt Service Routine Only)

The .FORK call is used when access to a shared resource must be serialized or when a lengthy but non-time-critical section of code must be executed. .FORK issues a subroutine call to the monitor and does not use an EMT instruction request.

Macro Call: .FORK fkblk

where:

fkblk is a four-word block of memory allocated within the driver
Errors:

The .FORK macro expands as follows:

```csv
.FORK fkb1k
JSR %5,@$FKPTR
.WORD fkb1k-
```

The .FORK call must be preceded by an .INTEN call, and the address of a four-word block must be supplied with the request. Your program must not have left any information on the stack between the .INTEN and the .FORK call. The contents of registers R4 and R5 are preserved through the call, and on return registers R0 through R3 are available for use.

If you are using a .FORK call from a device handler, it is assumed that you are also using the other macros (.QELDF, .DRBEG, .DRAST, .DRFIN, and .DREND) provided for handlers.

The .DREND macro allocates a word for \$FKPTR. This word is filled in at bootstrap time for a system device or at LOAD or .FETCH time for a non-system device.

If you want to use the .FORK macro in an in-line interrupt service routine rather than in a device handler, you must set up \$FKPTR. The recommended way to do this is as follows:

```asm
SYSPTR=54
    FORK=402
        .GVAL      #AREA, #FORK
        ADD       @*SYSPTR, RO
        MOVE      RO, $FKPTR
    .
    .
    .
AREA:   .BLKW 2
$FKPTR:   .WORD 0
```

Once the pointer is set up, use the macro in the usual way as follows:

## .FORK fkblk

This method permits you to preserve both R4 and R5 across the fork.

The .FORK request is linked into a queue and serviced on a first-in first-out basis. On return to the driver or interrupt service routine following the call, the interrupt has been dismissed and the processor is executing at priority 0. Therefore, the .FORK request must not be used where it can be reentered using the same fork block by another interrupt. It also should not be used with devices that have continuous interrupts that cannot be disabled. The RT-11 Software Support Manual gives additional information on the .FORK request.

## Notes:

For use within a user interrupt service routine, monitor fixed offset 402 (FORK) contains the offset from the start of the resident monitor to the .FORK request processor. A .FORK can be done by computing the address of the .FORK request processor and using a subroutine instruction. (Under the XM monitor, only privileged jobs can contain user interrupt service routines.) For example:

```asm
SYSPTR=54
    FORK=402
        .GVAL      *AREA, *FORK
        ADD       @*SYSPTR, RO
        MOV       RO, R4
        JSR       R5, (R4)
        .WORD      BLOCK-.
        .
        .
        .
AREA:   .BLKW 2
BLOCK:   .BLKW 4
```

This method destroys the contents of R4.

Example:

Refer to the example following the description of .DRAST.

## 2.36 .FPROT

The .FPROT programmed request sets or removes file protection on individual RT-11 files. A file marked as protected cannot be deleted by .CLOSE, .DELETE, .ENTER, or .RENAME requests. However, the contents of a protected file are not protected against modification. For example, a .LOOKUP of a protected file followed by a .WRITE to the file is permitted.

Protection is enabled by setting bit 15 of a file's directory entry status word.

Macro Call: .FPROT area, chan, dblk, prot

where:

area is the address of a four-word EMT argument block

chan is a channel number in the range 0–376(octal)

dblk is the address of a four-word block containing the filespec in Radix-50 of the file

prot = #1 — to protect the file from deletion

= #0 — to remove protection so that the file can be deleted

Request Format:

R0 area

<table><tr><td>43</td><td>chan</td></tr><tr><td colspan="2">dblk</td></tr><tr><td colspan="2">prot</td></tr></table>

Errors:

Code         Explanation
0       Channel in use
1       File not found
2       Invalid operation
3       Invalid value for PROT

## Example:

;.FPROT, .SFDAT example.
;This is an example of the use of the .FPROT and .SFDAT
;programmed requests. It uses the "special" mode of the CSI to
;set an input filespec from the console terminal. .DSTATUS is
;used to determine if the device handler is loaded. If not, a
;.FETCH request is used to load the handler into memory. Finally,
;the file is marked as protected using the .FPROT request and
;the file date is changed to the current system date using the
;.SFDAT request.
;
;MCALL : .FPROT , .FETCH , .CSISRC , .DSTATUS , .SFDAT , .PRINT , .EXIT

```asm
START: .CSISPC #OUTSP, #DEFEXT ;Use CSI to set input filespec
.DSTAT *STAT,*INSPEC ;Check the device
TST STAT+4 ;to see if the handler is resident
BNE 1\$ ;Branch if it is
.FETCH #INSPEC ;Otherwise, load that handler
BCC 1\$ ;ok
.PRINT *LOFAIL ;Otherwise, Print load error message
BR START ;and try again
1\$: .FPROT #EMTBLK, #0, #INSPEC, #1 ;Mark file as protected
BCC 2\$ ;and branch if okay
.PRINT *PRFAIL ;Otherwise, Print Protect error message
BR START ;and try again
2\$: .SFDAT #EMTBLK, #0, #INSPEC, #0 ;Finally, set current date
;A date of 0 means "use current system date"
BCC 10\$ ;Branch if everything is okay
.PRINT *SDFAIL ;Otherwise, Print date error message
BR START ;and try again
10\$: .EXIT ;Everythings okay - exit to KMON
EMTBLK: .BLKW 4 ;The EMT argument block is built here
DEFEXT: .WORD 0,0,0,0 ;No default extensions
STAT: .BLKW 4 ;Block for ,DSTATUS to use
LOFAIL: .ASCIZ /Error in ,LOAD request/
PRFAIL: .ASCIZ /Error in ,FPROT request/
SOFAIL: .ASCIZ /Error in ,SFDAT request/
.EVEN
OUTSP: .BLKW 5*3 ;Output specs so here
INSPEC: .BLKW 4*6 ;Input specs so here
HANLOD: .BLKW 1 ;Handlers begin loading here (if necessary)
.END START
```

## 2.37 .GMCX (XM Only)

The .GMCX request returns the mapping status of a specified window. Status is returned in the window definition block and can be used in a subsequent mapping operation. Since the .CRAW request permits combined window creation and mapping operations, entire windows can be changed by modifying certain fields of the window definition block.

The .GMCX request modifies the following fields of the window definition block:

W.NAPR base page address register of the window

W.NBAS window virtual address

W.NSIZ window size in 32-word blocks

W.RID region identifier

If the window whose status is requested is mapped to a region, the .GMCX request loads the following additional fields in the window definition block:

W.NOFF offset value into the region

W.NLEN length of the mapped window

W.NSTS state of the WS.MAP bit is set to 1 in the window status word

Otherwise, these locations are zeroed.

Macro Call: .GMCX area[,addr]

where:

area is the address of a two-word EMT argument block

addr is the address of the window definition block where the specified window's status is returned

Request Format:

R0 → area:

Errors:

Code Explanation

3 An illegal window identifier was specified.

Example:

Refer to the example for the .CRAW request.

## 2.38 .GTIM

.GTIM allows user programs to access the current time of day. The time is returned in two words and given in terms of clock ticks past midnight.

Macro Call: .GTIM area,addr

where:

area is the address of a two-word EMT argument block

addr is the address of the two-word area where the time is to be returned

Request Format:

```txt
R0 → area: 21 0
addr
```

The high-order time is returned in the first word, the low-order time in the second word. Your program must perform the conversion from clock ticks to hours, minutes, and seconds.

The basic clock frequency (50 or 60 Hz) can be determined from the configuration word in the monitor (offset 300 relative to the start of the resident monitor). In the FB monitor, the time of day is automatically reset after 24:00, when a .GTIM request is done and the date is changed if necessary. In the SJ monitor, the time of day is not reset unless SJ timer support was selected during the system generation process. The month is not automatically updated in either monitor. (Proper month and year rollover is a special feature that you enable through the system generation process.)

The default clock rate is 60 cycles, that is, 60 ticks per second. Consult the RT-11 System Generation Guide if conversion to a 50-cycle rate is necessary.

Because day rollover is done only through a .GTIM request, make sure that your program receives the correct time and day by issuing a .GTIM request before using the .DATE request. Nearly all RT-11 system utility programs issue a .GTIM request to make sure that rollover occurs daily. If you do not use a system utility program regularly, issue a .GTIM request at least once during a 24-hour period.

## NOTE

There are also several SYSLIB routines that perform time conversion (see Chapter 3). They are CVTTIM, TIMASC, TIME, and SECNDS.

Errors:

None.

```prolog
Example:
,TITLE GTIM.MAC
;+
; .GTIM - This is an example in the use of the .GTIM request.
; This example is a subroutine that can be assembled separately
; and linked with a user program.
;
; CALLING SEQUENCE: CALL TIME
;
; INPUT: none
;
; OUTPUT: R4 = Minutes in hi byte / hours in lo byte
; R5 = Ticks in hi byte / seconds in lo byte
; (in that order for ease of removal !)
;
; ERRORS: none Possible
;
; NOTE: This example calls SYSLIB functions '$DIVTK' & '$DIV60'
;-
.GLOBL $DIVTK,$DIV60
.MCALL ,GTIM
```

<table><tr><td rowspan="14">TIME::</td><td>MOV</td><td>*TICKS,R1</td><td>;R1 Points to where to Put time</td></tr><tr><td>.GTIM</td><td>*AREA,R1</td><td>;Get ticks since midnight via ,GTIM</td></tr><tr><td>MOV</td><td>(R1)+,RO</td><td>;RO = lo order time</td></tr><tr><td>MOV</td><td>@R1,R1</td><td>;R1 = hi order time</td></tr><tr><td>CALL</td><td>$DIVTK</td><td>;Call SYSLIB 32 bit divide by clk freq</td></tr><tr><td>MOV</td><td>R3,R5</td><td>;Save ticks</td></tr><tr><td>SWAB</td><td>R5</td><td>;Put them in hi byte</td></tr><tr><td>CALL</td><td>$DIV60</td><td>;Call SYSLIB divide by 60, routine</td></tr><tr><td>BISB</td><td>R3,R5</td><td>;Put seconds in lo byte</td></tr><tr><td>CALL</td><td>$DIV60</td><td>;Divide by 60, once again</td></tr><tr><td>MOV</td><td>R3,R4</td><td>;Put minutes in R4</td></tr><tr><td>SWAB</td><td>R4</td><td>;Move them to hi byte</td></tr><tr><td>BISB</td><td>R1,R4</td><td>;Put hours in lo byte</td></tr><tr><td>RETURN</td><td></td><td>;and return</td></tr><tr><td>AREA:</td><td>.BLKW</td><td>2</td><td>;EMT argument area</td></tr><tr><td rowspan="2">TICKS:</td><td>.WORD</td><td>0,0</td><td>;Ticks since midnight returned here</td></tr><tr><td>.END</td><td></td><td></td></tr></table>

## 2.39 .GTJB

The .GTJB request returns information about a job in the system.

Macro Call: .GTJB area,addr[,jobblk]

where:

area is the address of a three-word EMT argument block

addr is the address of an eight-word or twelve-word block into which the parameters are passed. The values returned are:

Word 1 Job Number = priority level \*2 (background job is 0; system jobs are 2, 4, 6, 10, 12, 14; and foreground job is 16 in system job monitors; background job is 0 and foreground job is 2 in FB and XM monitors; job number is 0 in a SJ monitor)

2 High-memory limit of job partition (highest location available to a job in low memory if the job executes a privileged .SETTOP #-2 request)

3 Low-memory limit of job partition (first location)

4 Pointer to I/O channel space

5 Address of job's impure area in FB and XM monitors

6 Low byte: unit number of job's console terminal (used only with multiterminal option; 0 when multiterminal feature is not used)
High byte: reserved for future use

7 Virtual high limit for a job created with the linker /V option (XM only; 0 when not running under the XM monitor or if /V option is not used)

8-9 Reserved for future use

10–12 ASCII logical job name (system job monitors only; contains zeroes for non-system jobs in FB and XM, not defined in SJ)

jobblk is a pointer to a three-word ASCII logical job name for which data is being requested

```asm
;+
; .GTJB - This is an example of the .GTJB request. The
; example issues the request to determine if there is a loaded
; Foresground Job in the system. This Program will execute properly
; with either a normal FB monitor or an FB monitor that includes
; System Job support.
;-
    .MCALL   .GVAL, .GTJB, .PRINT, .EXIT
    SYSGEN= 372                  ;Fixed offset to SYSGEN word
    SYSJOB= 40000                   ;System Job option bit
START: MOV     #2,      R1          ;Assume FG job number = 2
    .GVAL     #LIST,   #SYSGEN       ;Get SYSGEN option word
    BIT     #SYSJOB, RO           ;System job monitor?
    BEQ     1$                    ;Branch if not
    MOV     #16,      R1          ;If so, FG job number = 16
1$: .GTJB     #LIST, #JOBARG, R1   ;Find out if FG loaded
    BCS     2$                    ;Branch if no active FG job
    .PRINT   #FGLOAD             ;Announce that FG job is loaded
    .EXIT                     ;and exit from Program.
2$: .PRINT   #NOFG              ;Announce that there's no FG job
    .EXIT                     ;and exit from Program.
LIST: .BLKW   3                       ;EMT Argument block
JOBARG: .BLKW   12.                 ;Job Parameters Passed back here
FGLOAD: .ASCIZ   /!FG Loaded!/        ;FG loaded message
NOFG: .ASCIZ   /?No FG Job?/        ;No FG message
    .END     START
```

Word 4 of addr, which describes where the I/O channel words begin, normally indicates an address within the job's impure area. However, when a .CDFN is executed, the start of the I/O channel area changes to the user-specified area.

If the jobblk argument to the .GTJB request is between 0 and 16 when the status of a job is requested, it is interpreted as a job number. If the jobblk argument is 'ME', or equals -1, information about the current job is returned. If the jobblk argument is omitted, or equals -3 (a V03B-compatible parameter block), only eight words of information (corresponding to words 1–8 of addr) are returned.

In an F/B environment without the system job feature, you can get another job's status only by specifying its job number (0 or 2).

## Request Format:

[figure omitted]

Errors:

Code Explanation
0 No such job currently running.

Example:
    See the program GTJB.MAC in the example listing.

The .GTLIN request collects a line of input from either the console terminal or an indirect command file, if one is active. This request is similar to .CSIGEN and .CSISPC in that it requires the USR, but no format checking is done on the input line. Because the .GTLIN command is implemented in the USR, the CSI will generate an error message if you attempt to input more than 80 characters to a .GTLIN request. Normally, .GTLIN collects a line of input from the console terminal and returns it in the buffer specified by you. However, if there is an indirect command file active, .GTLIN collects the line of input from the indirect command file just as though it were coming from the terminal.

When bit 3 of the Job Status Word is set and your program encounters a CTRL/C in an indirect command file, the .GTLIN request collects subsequent lines from the terminal. Note that if you then clear bit 3 of the Job Status Word, the next line collected by the .GTLIN request is the CTRL/C in the indirect command file; this causes the program to abort. Further input will come from the indirect command file, if there are any more lines in it. When bit 14 of the Job Status Word is set, the .GTLIN request passes lowercase letters.

An optional prompt string argument (similar to the CSI asterisk) allows your program to query for input at the terminal. The prompt string argument is an ASCIZ character string in the same format as that used by the .PRINT request. If input is from an indirect command file and the SET TT QUIET option is in effect, this prompt is suppressed. If SET TT QUIET is not in effect, the prompt is printed before the line is collected, regardless of whether the input comes from the terminal or an indirect file. The prompt appears only once. It is not reissued if an input line is canceled from the terminal by CTRL/U or multiple DELETE characters, unless the single-line editor is running.

If your program requires a nonstandard command format, such as the user identification code (UIC) specification for FILEX, you can use the .GTLIN request to accept the command string input line. .GTLIN tracks indirect command files and your program can do a pre-pass of the input line to remove the nonstandard syntax before passing the edited line to .CSIGEN or .CSISPC.

## NOTE

In an F/B environment, .GTLIN performs a temporary implicit unlock while the line is being read from the console.

Macro Call: .GTLIN linbuf[,prompt][,type]

where:

linbuf is the address of the buffer to receive the input line. This area must be at least 81 bytes in length. The input line is stored in this area and is terminated with a zero byte

prompt is an optional argument and is the address of a prompt string to be printed on the console terminal. The prompt string has the same format as the argument of a .PRINT request. Usually, the prompt string ends with an octal 200 byte to suppress printing the carriage return/line feed at the end of the prompt

type is an optional argument which forces .GTLIN to take its input from the terminal rather than from an indirect file

## NOTE

The only requests that can take their input from an indirect command file are .CSIGEN, .CSISPC, and .GTLIN. The .TTYIN and .TTINR requests cannot get characters from an indirect command file. They get their input from the console terminal (or from a BATCH file if BATCH is running). The .TTYIN and .TTINR requests and the .GTLIN request with the optional type argument are useful for information that is dynamic in nature — for example, when all files with a .MAC file type need to be deleted or when a disk needs to be initialized. In these circumstances, the response to a system query should be collected through a .TTYIN or a .GTLIN with the type argument so that confirmation can be done interactively, even though the process may have been invoked through an indirect command file. However, the response to the linker's Transfer Symbol? query would normally be collected through a .GTLIN, so that the LINK command could be invoked and the start address specified from an indirect file. Also, if there is no active indirect command file, .GTLIN simply collects an input line from the console terminal by using .TTYIN requests.

Errors:

None.

Example:

.TITLE GTLIN.MAC

;+
; .GTLIN - This is an example in the use of the .GTLIN request.
; The example merely accepts input from the console terminal and
; echoes it back,
;-

START: .GTLIN #BUFF, \*PROMT ;Get a line of input from Keyboard
TSTB BUFF ;Nothing entered?
BEQ 1\$ ;Branch if nothing entered
.PRINT #BUFF ;Echo the input back
CLRB BUFF ;Clear first char of buffer
BR START ;Go back for more

BUFF: BLKW 41.

PROMT:        ,ASCII       /Enter somethings>/<200>
        ,END          START

## 2.41 .GVAL/.PVAL

The .GVAL request returns in R0 the contents of a monitor fixed offset; the .PVAL request changes the contents of a monitor offset. The .PVAL request also returns the old contents of an offset in R0 to simplify saving and restoring an offset value. .GVAL and .PVAL must be used in an XM environment to read or change any fixed offset, and should be used with other RT-11 monitors for compatibility with XM and possible future releases of RT-11.

Chapter 3 of the RT-11 Software Support Manual contains a table of the monitor's fixed offset locations.

Macro Calls: .GVAL area, offset

.PVAL area, offset, value

where:

area is the address of a two- or three-word EMT argument block

offset is the displacement from the beginning of the resident monitor to the word to be returned in R0

value is the new value to be placed in the fixed offset location

Request Format for .GVAL:

<table><tr><td rowspan="2">R0 → area:</td><td>34</td><td>0</td></tr><tr><td colspan="2">offset</td></tr></table>

Request format for .PVAL:

<table><tr><td>34</td><td>2</td></tr><tr><td colspan="2">offset</td></tr><tr><td colspan="2">value</td></tr></table>

Errors:

Code

## Explanation

0 The offset requested is beyond the limits of the resident monitor.

Example:

```matlab
,TITLE .GVAL.MAC
;+
; .GVAL - This is an example of the .GVAL request. It finds out
; if the foreground job is active. Compare this example with the
; .GTJB example.
;-
.MCALL .GVAL, .PRINT, .EXIT
CONFIG= 300      ;Offset in monitor of configuration word
FJOB$= 200      ;Bit in config word is on if FG active
```

```asm
START:    .GVAL   #AREA, #CONFIG    ;Get monitor CONFIG word in RO
        BIT     #FJOB$,RO      ;See if FG Active bit is on
        BEQ    1$               ;Branch if not
        .PRINT   #FGACT          ;Announce FG is active
        .EXIT                     ;then exit Program
1$:    .PRINT   #NOFG          ;Announce there's no FG job
        .EXIT                     ;then exit Program

AREA:    .BLKW   2              ;EMT argument block
FGACT:    .ASCIZ  /! FG is active !/      ;FG active message
NOFG:    .ASCIZ  /? No FG Job ?/       ;No FG message
        .EVEN
        .END    START

;       .TITLE  .PVAL.MAC

;+
; .PVAL - This is an example of the .PVAL request. The example
; illustrates a way of changing the default file size created
; by the .ENTER request. Compare this example with the .PEEK/.POKE
; example. .PVAL is used both to change the default file size and
; to read the old default file size, returning the old value in RO.
;-

        .MCALL  .PVAL, .EXIT

        MAXBLK= 314             ;Monitor offset of default file size

START:    .PVAL   #EMTBLK,#MAXBLK,#NEWSIZ ;Change default file size to 100. blocks
        MOV     RO,   OLDSIZ     ;Save the old default
        .EXIT                 ;We'll just exit now, but Presumably
                ;in a real program we'd do more
                ;processins, perhaps creating files
                ;with the new default size we just
                ;set, then before exiting we'd restore
                ;the old default size.

EMTBLK:    .BLKW   3              ;EMT argument block
NEWSIZ:    .WORD   100,
OLDSIZ:    .WORD   0              ;Old default size is saved here
        .END    START
```

## 2.42 .HERR/.SERR

.HERR and .SERR are complementary requests used to govern monitor behavior for serious error conditions. During program execution, certain error conditions can arise that cause the executing program to be aborted (see Table 2–2).

Normally, these errors cause program termination with one of the ?MON-F-error messages. However, in certain cases it is not feasible to abort the program because of these errors. For example, a multi-user program must be able to retain control and merely abort the user who generated the error. .SERR accomplishes this by inhibiting the monitor from aborting the job and causing an error return to the offending EMT. On return from that request, the carry bit is set and byte 52 contains a negative value indicating the error condition that occurred. In some cases (such as the .LOOKUP and .ENTER requests), the .SERR request leaves channels open. It is your responsibility to perform .PURGE or .CLOSE requests for these channels, otherwise subsequent .LOOKUP/.ENTER requests will fail.

.HERR turns off user error interception. It allows the system to abort the job on fatal errors and generate an error message. (.HERR is the default case.)

Macro Calls: .HERR
.SERR

Request Formats:

```txt
.HERR Request R0 = 5 0
.SERR Request R0 = 4 0
```

Errors:

Table 2–2 contains a list of the errors that are returned if soft error recovery is in effect. Traps to locations 4 and 10, floating-point exception traps, and CTRL/C aborts are not inhibited. These errors have their own recovery mechanism.

Table 2-2: Soft Error Codes (.SERR)

| Code | Explanation |
| --- | --- |
| -1 | Called USR from completion routine. |
| -2 | No device handler; this operation needs one. |
| -3 | Error doing directory I/O. |
| -4 | .FETCH error. Either an I/O error occurred while the handler was being used, or an attempt was made to load the handler over USR or RMON. |
| -5 | Error reading an overlay. |
| -6 | No more room for files in the directory. |
| -7 | Invalid address (FB only); tried to perform a monitor operation outside the job partition. |
| -10 | Invalid channel number; number is greater than actual number of channels that exist. |
| -11 | Invalid EMT; an invalid function code has been decoded. |
| -12 | Reserved for monitor internal use. |
| -13 | Reserved for monitor internal use. |
| -14 | Invalid directory. |
| -15 | Unloaded XM handler. |
| -16 | Reserved for monitor internal use. |
| -17 | Reserved for monitor internal use. |
| -20 | Reserved for monitor internal use. |
| -21 | Reserved for monitor internal use. |
| -22 | Reserved for monitor internal use. |

;+
; .HERR / .SERR - This is an example in the use of the .HERR & .SERR
; requests. Normally fatal errors will cause a return to the user
; Program for Processing and Printing of an appropriate error message,
;-

.MCALL          .HERR , .SERR , .LOOKUP , .PURGE
.MCALL          .EXIT , .PRINT , .CSISPC

        BR      START          #Try again...
FTLERR:    NEG     RO           #Make error # positive
        DEC     RO           #Adjust by one
        ASL     RO           #Multiply by 2 to make an index
        MOV     TBL(RO),RO   #Put message address into RO
        .PRINT                  #and Print it.
        BR      START          #Go try some more errors

TBL: M1
M1
M2
M3
M4
M5
M6
M7
M10
M11
M12
M13
M14
M15
M16
M17
M20
M21
M22

M2: .ASCIZ /?Invalid Device -or- No Handler?/
M3: .ASCIZ /?Directory I-O.Error?/
M7: .ASCIZ /?Address Check Error?/
M10: .ASCIZ /?Invalid Channel?/
M11: .ASCIZ /?Invalid EMT?/
M12: .ASCIZ /?Trap to 4?/
M13: .ASCIZ /?Trap to 10?/
M14: .ASCIZ /?Invalid directory?/
M17: .ASCIZ /?Memory error?/
M1: Not Possible in this Program
M4: Not Possible in this Program
M5: Not Possible in this Program
M6: Not Possible in this Program
M15: Not Possible in this Program
M16: Not Possible in this Program
M20: Not Possible in this Program
M21: Not Possible in this Program
M22: .ASCIZ /?Not Possible?/ Not Possible in this Program

| NOFIL: | .ASCIZ | /?File Not Found?/ |  |
| --- | --- | --- | --- |
| LUPOK: | .ASCIZ | /LookUP succeeded/ |  |
|  | .EVEN |  | ;Fix boundary |
| AREA: | .BLKW | 4 | ;EMT Argument block |
| DEFEXT: | .WORD | 0,0,0,0 | ;No default extensions |
| OUTSP: | .BLKW | 5*3 | ;Output specs so here |
| INSPEC: | .BLKW | 4*6 | ;Input specs so here |
| HANLOD: | .BLKW | 1 | ;Handlers begin loading here (if necessary) |
|  | .END | START |  |

## 2.43 .HRESET

The .HRESET request stops all I/O transfers in progress for the issuing job, and then performs an .SRESET request. (.HRESET is not used to clear a hard-error condition.) In an SJ environment, a hardware RESET instruction is used to terminate I/O. In an FB or XM environment, only the I/O associated with the job that issued the .HRESET is affected by entering active handlers at the abort entry point of the handler. All other transfers continue.

Macro Call: .HRESET

Errors:

None.

Example:

Refer to the example for .SRESET for format.

## 2.44 .INTEN

.INTEN is used by interrupt service routines to:

1. Notify the monitor that an interrupt has occurred and to switch to system state.

2. Set the processor priority to the correct value.

3. Save the contents of R4 and R5 before returning to the Interrupt Service Routine. Any other registers must be saved by you.

.INTEN issues a subroutine call to the monitor and does not use an EMT instruction request.

All external interrupts must cause the processor to go to priority level 7. .INTEN is used to lower the priority to the value at which the device should be run. On return from .INTEN, the device interrupt can be serviced, at which point the interrupt routine returns with an RTS PC.

## NOTE

An RTI instruction does not return correctly from an interrupt routine that specifies an .INTEN.

Macro Call: .INTEN prio[,pic]

where:

prio is the processor priority at which to run the interrupt routine, normally the priority at which the device requests an interrupt

pic is an optional argument that should be non-blank if the interrupt routine is written as a PIC (position-independent code) routine. Any interrupt routine written as a device handler must be a PIC routine and must specify this argument

Errors:

None.

Example:

.TITLE SL11.MAC

```csv
SL11.MAC - This is an example in the use of the .INTEN request.
The example is an in-line, interrupt service routine, which may
be assembled separately and linked with a mainline program.
The routine transfers data from a user specified buffer to a DL11
Serial Line Interface.
CALLING FORMAT:
JSR R5,SL11 #Initiate Output
WORD wordcount #words to transfer
WORD BUFFER #Address of Data Buffer
BUFFER: BLKW wordcount
MCALL .INTEN
DLVEC = 304 #DL11 Vector ***
DLCSR = 176504 #DL11 Output CSR ***
DLPRI = 4 #DL11 Priority for RT-11
SL11:: MOV (R5)+,(PC)+ #I/O Initiation - Get word count
WCNT: ,WORD 0
MOV (R5)+,(PC)+ #Get address of Data Buffer
BUFAD: ,WORD 0
ASL WCNT #Make word count byte count
BEQ 1$ #Just leave if zero word count
MOV *DLINT,@*DLVEC #Initialize DL11 interrupt vector
BIS *100,@*DLCSR #Enable interrupts
RETURN #Return to caller
DLINT: ,INTEN DLPRI. #Interrupt service - Notify RT-11
MOVB @BUFAD,@*DLCSR+2 #and drop priority to that of DL11
INC BUFAD #Transfer a byte
DEC WCNT #Bump buffer pointer
BEQ DLDUN #All bytes transferred?
RETURN #Branch if yes #No return from interrupt thru RT-11
DLDUN: BIC *100,@*DLCSR #All done - disable DL11 interrupts
RETURN #Return thru RT-11
.END
```

## 2.45 .LOCK/.UNLOCK

.LOCK

The .LOCK request keeps the USR in memory to provide any of its services required by your program. If all the conditions that cause swapping are satisfied, the part of the user program over which the USR swaps is written into the system swap blocks (the file SWAP.SYS) and the USR is loaded. Otherwise, the copy of the USR in memory is used, and no swapping occurs. (Note that certain calls always require a fresh copy of the USR.) A .LOCK request always causes the USR to be loaded in memory if it is not already in memory. The USR is not released until an .UNLOCK request is given. (Note that under an FB monitor, calling the CSI or using a .GTLIN request can also perform an implicit and temporary .UNLOCK.) A program that has many USR requests to make can .LOCK the USR in memory, make all the requests, and then .UNLOCK the USR.

In an FB environment, a .LOCK inhibits the other job from using the USR. Note that the .LOCK request reduces time spent in file handling by eliminating the swapping of the USR in and out of memory. .LOCK causes the USR to be read into memory or swapped into memory. After a .LOCK has been executed, an .UNLOCK request must be executed to release the USR from memory. The .LOCK/.UNLOCK requests are complementary and must be matched. That is, if three .LOCK requests are issued, at least three .UNLOCK requests must be done, otherwise the USR is not released. More .UNLOCK than .LOCK requests can be issued without error.

Macro Call: .LOCK

## Notes:

1. It is vital that the .LOCK call not come from within the area into which the USR will be swapped. If this should occur, the return from the .LOCK request would not be to the user program, but to the USR itself, since the .LOCK function inhibits the user program from being re-read. Also, none of the executable code should be in the area or reference anything in the area that the USR will occupy while it is locked.

2. Once a .LOCK has been performed, it is not advisable for the program to destroy the area the USR is in, even if no further use of the USR is required, because this causes unpredictable results when an .UNLOCK is done.

3. If a foreground job performs a .LOCK request while the background job owns the USR, foreground execution is suspended until the USR is available. In this case, it is possible for the background to lock out the foreground (see the .TLOCK request).

Errors:

None.

Example:

Refer to the example for the .UNLOCK request.

.UNLOCK

The .UNLOCK request releases the User Service Routine (USR) from memory if it was placed there with a .LOCK request. If the .LOCK required a swap, the .UNLOCK loads the user program back into memory. There is a .LOCK count. Each time the user does a .LOCK, the lock count is incremented. When the user does an .UNLOCK, the lock count is decremented. When the lock count goes to 0, the user program is swapped back in (see Note 1).

Macro Call: .UNLOCK

Notes:

1. The number of .UNLOCK requests must at least match the number of .LOCK requests that were issued. If more .LOCK requests are done, the USR remains locked in memory. Extra .UNLOCK requests in your program do no harm since they are ignored.

2. With two running jobs in an FB environment use .LOCK/.UNLOCK pairs only where absolutely necessary. When a job locks the USR, the other job cannot use it until it is unlocked, which can degrade performance in some cases.

3. In an FB environment, calling the CSI with input coming from the console terminal results in an implicit (though temporary). UNLOCK.

4. Make sure that the .UNLOCK request is not in the area that the USR swaps into. Otherwise, the request can never be executed.

Errors:

None.

Example:

```asm
,TITLE LOCK.MAC
;+
; ,LOCK / ,UNLOCK - This is an example in the use of the ,LOCK and ,UNLOCK
; requests, This example tries to obtain as much memory as possible (using
; the ,SETTOP request), which will force the USR into a swapping mode. The
; ,LOCK request will bring the USR into memory (over the high 2k of our little
; program !) and force it to remain there until an ,UNLOCK is issued,
;-
.MCALL ,LOCK,,UNLOCK,,LOOKUP
.MCALL ,SETTOP,,PRINT,,EXIT
SYSPTR=54 ;Pointer to beginnings of RMON
START: .SETTOP @#SYSPTR ;Try to allocate all of memory (up to RMON)
.LOCK ;bring USR into memory
.LOOKUP #AREA,#0,#FILE1 ;LOOKUP a file on channel 0
BCC 1\$ ;Branch if successful
2\$: .PRINT #LMSG ;Print Error Message
.EXIT ;then exit program
1\$: .PRINT #F1FND ;Announce our success
MOV #AREA,RO ;RO => EMT Argument Block
INC @RO ;Increment low byte of 1st arg (chan #)
MOV #FILE2,2(RO) ;Fill in pointer to new filespec
.LOOKUP ;Do the ,LOOKUP from filled in arg block
.BCS 2\$ ;Pointed to by RO.
.PRINT #F2FND ;Branch on error
.UNLOCK ;Say we found it
.EXIT ;now release the USR
.AEXIT ;and exit program
AREA: .BLKW 3 ;EMT Argument Block
FILE1: .RAD50 /DK/ ;A File we're sure to find
.RAD50 /PIP /
.RAD50 /SAV/
FILE2: .RAD50 /DK/ ;Another file we might find
.RAD50 /TECO /
.RAD50 /SAV/
LMSG: .ASCIZ /?Error on ,LOOKUP?/ ;Error message
F1FND: .ASCIZ /...Found PIP.SAV/
F2FND: .ASCIZ /...Found TECO.SAV/
.EVEN
.END START
```

## 2.46 .LOOKUP

A .LOOKUP request can be used in two different ways. The first way is to use the request as a standard lookup, which occurs under the SJ, FB, and XM monitors. The second way is to use the request when the system job feature is implemented. Both ways are described in this section.

## 2.46.1 Standard Lookup

The .LOOKUP request associates a specified channel with a device and existing file for the purpose of performing I/O operations. The channel used is then busy until one of the following requests is executed:

.CLOSE

.SAVESTATUS

.SRESET

.HRESET

.PURGE

.CSIGEN (if the channel is in the range 0–10 octal)

Note that if the program is overlaid, channel 17(octal) is used by the overlay handler and should not be modified.

If the first word of the file name (the second word of dblk) is 0 and the device is a file-structured device, absolute block 0 of the device is designated as the beginning of the file. This technique is called a non-file-structured .LOOKUP and allows I/O operations to access any physical block on the device. If a file name is specified for a device that is not file structured (such as LP:FILE.TYP), the name is ignored.

The handler for the selected device must be in memory for a .LOOKUP. On return from the .LOOKUP, R0 contains the length in blocks of the file just opened. On a return from a .LOOKUP for a non-directory, file-structured device (typically magtape), R0 contains 0 for the length.

## NOTE

Care should be exercised when doing a non-file-structured .LOOKUP on a file-structured device, since if your program writes data, corruption of the device directory can occur and effectively destroy the disk. (The RT-11 directory starts in absolute block 6.)

In particular, avoid doing a .LOOKUP or .ENTER with a file specification where the file value is missing. If the device type is not known in advance and is to be entered from the keyboard, include a dummy file name with the .LOOKUP or .ENTER, even when it is assumed that the device is always non-file structured.

Macro Call: .LOOKUP area,chan,dblk[,seqnum]

where:

area is the address of a three-word EMT argument block

chan is a channel number in the range 0–377(octal)

dblk is the address of a four-word Radix-50 descriptor of the file to be operated upon

seqnum is a file number for magtape and cassette

If this argument is blank, a value of 0 is assumed.

For magtape, it describes a file sequence number. The action taken depends on whether the file name is given or is null. The sequence number can have the following values:

-1 means suppress rewind and search for a file name from the current tape position. If a file name is given, a file-structured lookup is performed (do not rewind). It is important that only -1 be specified and not any other negative number. If the file name is null, a non-file-structured lookup is done (tape is not moved).

0 means rewind to the beginning of the tape and do a non-file-structured lookup.

n where n is any positive number. This means position the tape at file sequence number n and check that the file names match. If the file names do not match, an error is generated. If the file name is null, a file-structured lookup is done on the file designated by seqnum.

## Request Format:

[figure omitted]

## Errors:

Code Explanation

0 Channel already open.

1 File indicated was not found on the device.

## Example:

.TITLE LOOKUP.MAC

; ,LOOKUP - This is an example in the use of the ,LOOKUP request.

; This example determines whether or not the RT-11 Device Queue

```asm
START:      .LOOKUP     #AREA,#0,#QUSPEC       ;See if there's a DK:QUFILE.TMP
                        BCC         1$                   ;Branch if there is
                        .PRINT     #NOFIL              ;Print 'File Not Found' message
                        .EXIT                     ;then exit Program
1$:      MOV     #SIZE,R1           ;R1 => where to Put ASCII size
                        CALL     CNV10            ;Convert size (in R0) to ASCII
                        .PRINT     #BUFF             ;Print size of QUFILE.TMP on console
                        .EXIT                     ;then exit Program
CNV10:      MOV     R0,-(SP)          ;Subroutine to convert Binary # in R0
                        CLR         R0                   ;to Decimal ASCII by repetitive
1$:      INC     R0                   ;subtraction. The remainder for each
                        SUB     #10.,@SP          ;radix is made into ASCII and pushed
                        BGE     1$                   ;on the stack, then the routine calls
                        ADD     #72,@SP          ;itself. The code at 2$ pops the ASCII
                        DEC     R0                   ;digits off the stack and into the out-
                        BEQ     2$                   ;put buffer, eventually returning to
                        CALL     CNV10            ;the calling Program. This is a VERY
2$:      MOVB     (SP)+,(R1)+       ;useful routine, is short and is
        RETURN                 ;memory efficient,
AREA:      .BLKW     3                  ;EMT Argument Block
QUSPEC:      .RAD50    /DK QUFILE/
                        .RAD50    /TMP/
BUFF:      .ASCII     /DK:QUFILE.TMP = /
SIZE:      .ASCIZ    /   Blocks/
NOFIL:      .ASCIZ    /?File Not Found DK:QUFILE.TMP ?/
                        .EVEN
                        .END     START
```

## 2.46.2 System Job Lookup

The foreground and background jobs can send messages to each other via the existing .SDAT/.RCVD/.MWAIT facility. A more general message facility is available to all jobs through the message queue (MQ) handler. By turning message handling into a formal "device" handler, and treating messages as I/O to jobs, the existing .READ/C/W-.WRITE/C/W-.WAIT mechanism can be used to transmit messages. A channel is opened to a job via a .LOOKUP request, after which standard I/O requests are issued to that channel.

Macro Call: .LOOKUP area,chan,jobdes

where:

area is the address of a two-word EMT argument block

chan is the number of the channel to open

jobdes is the address of a four-word descriptor of the job to which messages will be sent or received

jobdes → .RAD50 /MQ/
        .ASCII /logical-job-name/

where logical-job-name can be from one to six characters long. It must be padded with nulls if less than six characters long. If logical-job-name is zero, the channel will be opened for .READ/C/W requests only and such requests will accept messages from any job

Request Format:

```txt
R0 → area: 1 | chan
    jobdes
```

The .LOOKUP request associates a channel with a specified job for the purposes of sending inter-task messages. R0 is undefined on return from the .LOOKUP.

Errors:

Code Explanation

0 Channel already open.

1 No such job.

Example:

```txt
,TITLE SJLOOK.MAC
;+
; ,LOOKUP - This is an example in the use of the ,LOOKUP request
; to open a message channel to a System Job, specifically, the
; RT-11 Device Queue Foresround Program. NOTE: This example assumes
; it will be run under an FB Monitor generated with System Job
; Support and that QUEUE.REL has been successfully FRUN/SRUN !!!
;-
.MCALL .LOOKUP,.PRINT,.EXIT,.WRITW,.READW
START: .LOOKUP *AREA,*,0,*,QMSG Try to open a channel to QUEUE
BCC 1$ Branch if successful
.PRINT #NOJOB Error...Print error message
.EXIT then exit Program
1$: .WRITW *AREA,*,0,*,RMSG,*,G Send a meaningless message to QUEUE
BCS 2$ Branch if error
.READW #AREA,*,0,*,RMSG,*,G Wait for an acknowledgment message
BCS 2$ Branch if error
.PRINT #QRUN Announce QUEUE alive and well
.EXIT then exit
2$: .PRINT #MSGERR Print error message
.EXIT then exit
AREA: .BLKW 5 EMT Argument Block
QMSG: .RADSO /MQ/ Job Descriptor Block for ,LOOKUP
.ASCIZ /QUEUE/
.WORD 0,0
RMSG: .WORD 0 Dummy message...
.ASCI I /SJLOOK/
MSGERR: .ASCIZ /?Message Error?/ Error Messages, etc.
NOJOB: .ASCIZ /?QUEUE is not running?/
QRUN: .ASCIZ /! QUEUE is alive and running !/
.EVEN
.END START
```
