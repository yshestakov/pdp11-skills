# RT-11 PRM reference: Ch.2 programmed requests .ABTIO through .CTIMIO (alphabetical): .ADDR .ASSUME .BR .CDFN .CHAIN .CHCOPY .CLOSE .CMKT .CNTXSW .CRAW .CRRG .CSIGEN .CSISPC .CSTAT

Source: RT-11 Programmer's Reference Manual AA-H378C-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' sometimes reads as ',' (`,MCALL` = `.MCALL`), 'R0' as 'RO', '#' as '\*' or '*'. Verify exact macro expansions against `sysmac_v53.mac`.

Contents:
- Chapter 2
- 2.1 .ABTIO
- 2.2 .ADDR
- 2.3 .ASSUME
- 2.4 .BR
- 2.5 .CDFN
- 2.6 .CHAIN
- 2.7 .CHCOPY (FB and XM Only)
- 2.8 .CLOSE
- 2.9 .CMKT (FB and XM; SJ Monitor Special Feature)
- 2.10 .CNTXSW (FB and XM Only)
- 2.11 .CRAW (XM Only)
- 2.12 .CRRG (XM Only)
- 2.13 .CSIGEN
- 2.13.1 Passing Option Information
- 2.14 .CSISPC
- 2.15 .CSTAT
- 2.16 .CTIMIO (Device Handler Only)

---

## Chapter 2

# ) Programmed Request Description and Examples

This chapter presents the programmed requests alphabetically, describing each one in detail and providing an example of its use in a program. Also described are macros and subroutines that are used to implement device handlers and interrupt service routines. The following parameters are commonly used as arguments in the various calls:

addr an address, the meaning of which depends on the request being used.

area a pointer to the EMT argument block for those requests that require a block.

blk a block number specifying the relative block in a file or device where an I/O transfer is to begin.

buf a buffer address specifying a memory location into which or from which an I/O transfer will be performed; this address has to be word-aligned — that is, located at an even address and not a byte or odd address.

cblk the address of the five-word block where channel status information is stored.

chan a channel number in the range 0–376(octal).

chrcnt a character count in the range 1–255(decimal).

code a flag used to indicate whether the code is to be set in an EMT 375 programmed request.

crtn the entry point of a completion routine.

dblk a four-word Radix-50 descriptor block that specifies the physical device, file name, and file type to be operated upon (see Section 1.1.2.6).

func a numerical code indicating the function to be performed.

jobblk a pointer to a three-word ASCII system job name.

jobdev a pointer to a four-word system-job descriptor where the first word is a Radix-50 device name and the next three words contain an ASCII system-job name (for keyword argument use, refer to this as a "dblk").

num a number, the value of which depends on the request.

seqnum a file number.

For cassette operation, a value of 0 is assumed if this argument is blank.

For magtape operation, this argument describes a file sequence number. The values that the argument can have are described under the applicable programmed requests.

unit the logical unit number of a particular terminal in a multiterminal system.

wcnt a word count specifying the number of words to be transferred to or from the buffer during an I/O operation.

Many programmed requests are qualified as special features. These requests are enabled only if you performed a system generation process, that is, they are not available in a distributed monitor.

## 2.1 .ABTIO

The .ABTIO programmed request allows a running job to stop all outstanding I/O operations on a channel without terminating the program.

When .ABTIO is issued, the handler for the device opened on the specified channel is entered at its abort entry point. After the handler abort code is executed, control returns to the user program.

This request cannot be issued from a completion routine.

Macro Call: .ABTIO chan

where:

chan is the channel number for which to abort I/O

Request Format:

| R0 = | 13 | chan |
| --- | --- | --- |

Errors:

none

Example:

```asm
.TITLE ABTIO.MAC
\$This is an example of the .ABTIO request. The .ABTIO request
\$is useful for immediately terminating .READC/.WRITC or .READ/
;WRITE I/O on a Particular channel without issuins a .EXIT or
;HRESET, which would terminate the Program or stop I/O on all
\$channels.

.MCALL .ABTIO, .ENTER, .SCCA

START: .SCCA #AREA,#CTCWRD ;Inhibit CTRL/C
.ENTER *AREA,#1,#FILNAM ;Open channel 1 as output file
IOLOOP:
;
;
;Perform I/O to the file...
```

<table><tr><td rowspan="6"></td><td>TST</td><td>CTCWRD</td><td>;Has CTRL/C been typed?</td></tr><tr><td>BPL</td><td>IOLOOP</td><td>;No, continue file I/O</td></tr><tr><td>.ABTIO</td><td>#1</td><td>;Yes, stop I/O on channel 1</td></tr><tr><td>.</td><td></td><td rowspan="3">;Continue other processing</td></tr><tr><td>.</td><td></td></tr><tr><td>.</td><td></td></tr><tr><td>AREA:</td><td>.BLKW</td><td>4</td><td>;EMT argument block</td></tr><tr><td rowspan="2">CTCWRD:</td><td>.WORD</td><td>0</td><td>;Terminal status word</td></tr><tr><td>.END</td><td></td><td></td></tr></table>

## 2.2 .ADDR

The .ADDR macro computes the address you specify in a position-independent manner.

The .ADDR macro has the following syntax:

.ADDR addr,reg,push

where:

addr is the label of the address to compute, expressed as an immediate value with a number sign (#) before the label.

reg is the register in which to store the computed address, expressed as a register reference Rn or @Rn. To store the address on the stack, use @SP or -(SP). The following register references are valid:

| R1 | @R1 | @SP |
| --- | --- | --- |
| R2 | @R2 | -(SP) |
| R3 | @R3 |  |
| R4 | @R4 |  |
| R5 | @R5 |  |
|  | @R6 |  |

push determines what to do with the original contents of the register. If you omit push, the computed address overwrites the register contents. If you use ADD for the push argument, the computed address is added to the original contents of the register. If you use PUSH for the push argument, the register contents are pushed onto the stack before the computed address is stored in the register.

If you use -(SP) for the argument reg and you omit the push argument, PUSH is automatically used.

The following sample lines from a program show all three uses of the .ADDR macro.

| .ADDR | #ABC,RO | ;LOAD ADDRESS OF ABC IN RO |
| --- | --- | --- |
| .ADDR | #ABC,RO,ADD | ;ADD ADDRESS OF LABEL TO CONTENTS;OF RO |
| .ADDR | #ABC,RO,PUSH | ;PUSH CONTENTS OF RO ONTO STACK,;THEN LOAD ADDRESS OF ABC IN RO |

## 2.3 .ASSUME

The .ASSUME macro tests for a condition you specify. If the test is false, MACRO generates an assembly error and prints a descriptive message.

The .ASSUME macro has the following syntax:

.ASSUME a rel c [message=text]

where:

a is an expression.

c is an expression.

rel is the relationship between a and c you want to test.

text is the message you want MACRO to print if the condition you specified in the relationship between a and c is false. To specify your own error message, start the message with a semicolon (;), or start with a valid assembly expression followed by a semicolon (;) and the message. If you omit the message argument, the error message "a REL c" IS NOT TRUE prints; the expressions you used appear in the message in place of a and c.

In the following example, if the location counter (.) is less than 1000, MACRO generates an assembly error and prints the message 1000 - .; LOCATION TOO HIGH.

## , ASSUME      , LT 1000 MESSAGE=<1000-.; LOCATION TOO HIGH>

## 2.4 .BR

The .BR macro warns you if code that belongs together is separated during assembly. When you call the .BR macro, you specify an address as an argument. .BR checks that the next address matches the address you specified in the .BR macro. If it does not, MACRO prints the error message Error; not at location "addr". The location you specified in the .BR macro appears in place of addr in the message.

The .BR macro has the following syntax:

.BR addr

where addr is the address you want to test.

In the following example, MACRO tests the location that follows the .BR macro. Since the address does not match the address ABC, MACRO prints an error message.

|  | .BR | ABC | ;TEST THE NEXT ADDRESS FOR ABC |
| --- | --- | --- | --- |
| FOO: |  |  |  |
|  | . |  |  |
|  | . |  |  |
|  | . |  |  |
| ABC: |  |  |  |

In the next example, no error occurs:

## 2.5 .CDFN

The .CDFN request redefines the number of I/O channels. Each job, whether foreground or background, is initially provided with 16(decimal) I/O channels numbered 0–15. .CDFN allows the number to be expanded to as many as 255(decimal) channels (0–254 decimal, or 0–376 octal). Channel 377 is reserved for use by the monitor.

The space for the new channels is taken from within the user program. Each I/O channel requires five words of memory. Therefore, you must allocate 5\*n words of memory, where n is the number of channels to be defined.

It is recommended that you use the .CDFN request at the beginning of a program before any I/O operations have been initiated. If more than one .CDFN request is used, the channel areas must either start at the same location or not overlap at all. The two requests .SRESET and .HRESET cause the channels to revert to the original 16 channels defined at program initiation. Hence, you must reissue any .CDFNs after using .SRESET or .HRESET. The keyboard monitor command CLOSE does not work if your program defines new channels with the .CDFN request.

The .CDFN request defines new channels so that the space for the previously defined channels cannot be used. Thus, a .CDFN for 20(decimal) channels (while 16 original channels are defined) creates 20 new I/O channels; the space for the original 16 is unused, but the contents of the old channel set are copied to the new channel set.

If a program is overlaid, the overlay handler uses channel 17(octal) and this channel should not be modified. (Other channels can be defined and used as usual.)

In an XM monitor environment, the area supplied for additional channels specified by the .CDFN request must lie in the lower 28K words of memory. In addition, it must not be in the virtual address space mapped by Kernel PAR1, specifically the area from 20000 to 37776(octal). If you supply an invalid area, the system generates an error message.

Macro Call: .CDFN area,addr,num

where:

area is the address of a three-word EMT argument block

addr is the address where the I/O channels begin

num is the number of I/O channels to be created

```txt
R0 = 10 0
```

Request Format:

[figure omitted]

## Errors:

## Explanation

0 An attempt was made to define fewer than or the same number of channels that already exist. In an XM environment, an attempt to violate the PAR1 restriction sets the carry bit and returns error code 0 in byte 52.

Example:

```asm
.TITLE CDFN.MAC
+.
; .CDFN - This is an example in the use of the .CDFN request. The
; example defines 32 new channels to reside in the body of the
; program.
;-
.MCALL .CDFN,.PRINT,.EXIT
START: .CDFN *AREA,*CHANL,#32, ;Use .CDFN to define 32. new channels
BCC 1$ ;Branch if successful
.PRINT *BADCD ;Print failure message on console
.EXIT ;Exit Program
1$: .PRINT *GOODCD ;Print success message
.EXIT ;Then exit
AREA: .BLKW 3 ;EMT Argument Block
CHANL: .BLKW 5*32, ;Space for new channels
BADCD: .ASCIZ /? ,CDFN Failed ?/ ;Failure message
GOODCD: .ASCIZ /,CDFN Successful/ ;Success message
.END START
```

## 2.6 .CHAIN

The .CHAIN request allows a background program to pass control directly to another background program without operator intervention. Since this process can be repeated, a long "chain" of programs can be strung together.

The area in low memory from locations 500–507 contains the device name and file name (in Radix–50) to be chained to. The area from locations 510–777 is used to pass information between the chained programs.

Macro Call: .CHAIN

Request Format:

Notes:

1. Make no assumptions about which areas of memory remain intact across a .CHAIN. In general, only the resident monitor and locations

500–777 are preserved across a .CHAIN. In a .CHAIN to or from a virtual job, locations 500–777 are not preserved.

2. I/O channels are left open across a .CHAIN for use by the new program. However, new I/O channels opened with a .CDFN request are not available in this way. Since the monitor reverts to the original 16 channels during a .CHAIN, programs that leave files open across a .CHAIN should not use .CDFN. Furthermore, nonresident device handlers are released during a .CHAIN request and must be fetched again by the new program. Note that FORTRAN logical units do not stay open across a .CHAIN.

3. An executing program determines whether it was chained to or RUN from the keyboard by examining bit 8 of the Job Status Word. The monitor sets this bit if the program was invoked with .CHAIN request. If the program was invoked with R or RUN command, this bit remains cleared. If bit 8 is set, the information in locations 500–777 is preserved from the program that issued the .CHAIN and is available for the currently executing program to use. Again, locations 500–777 are not preserved in a .CHAIN to or from a virtual job.

An example of a calling and a called program is MACRO and CREF. MACRO places information in the chain area, locations 500–777, then chains to CREF. CREF tests bit 8 of the JSW. If it is clear, it means that CREF was invoked with the R or RUN command and the chain area does not contain useful information. CREF aborts itself immediately. If bit 8 is set, it means that CREF was invoked with .CHAIN and the chain area contains information placed there by MACRO. In this case, CREF executes properly.

## Errors:

.CHAIN is implemented by simulating the monitor RUN command and can produce any errors that RUN can produce. If an error occurs, the .CHAIN is abandoned and the keyboard monitor is entered.

When using .CHAIN, be careful with initial stack placement. The linker normally defaults the initial stack to 1000(octal); if caution is not observed, the stack can destroy chain data before it can be used.

## Example:

```asm
.TITLE CHAIN.MAC
;+
; .CHAIN - This example demonstrates the use of the .CHAIN
; Program request. It chains to Program 'CTEST.SAY' and passes it
; a command line typed in at the console terminal. As an exercise
; write the Program 'CTEST' - in it, check to see if it was chained
; to, and if so, echo the data passed to it, otherwise Print the
; message "Was not chained to".
;-
.MCALL .CHAIN,,TTYIN,,PRINT

START: MOV #500,R1 ;R1 => Chain area
MOV #CHPTR,R2 ;R2 => RAD50 Program FileSpec
.REPT 4 ;Move the Program FileSpec
MOV (R2)+,(R1)+ ;into the Chain area,...
.ENDR ;
.PRINT #PROMT ;Ask for the data to be passed
```

```asm
LOOP: .TTYIN
        MOVB     RO,(R1)+
        CMPB     RO,*12
        BNE     LOOP
        CLR8    @R1
        .CHAIN
CHPTR: .RAD50    /DK/
        .RAD50    /CTEST /
        .RAD50    /SAV/
PROMT: .ASCII    /Enter data to be passed to CTEST >/<200>
        .END    START

;
; IN CASE YOU DON'T HAVE TIME HERE'S AN EXAMPLE *
; 'CTEST.MAC' PROGRAM...
;
.TITLE  CTEST.MAC
.MCALL  .PRINT,,EXIT
JSW = 44
CHAIN$ = 400
CTEST: BIT      *CHAIN$,@*JSW      ;Were we chained to?
BEQ      1$
.PRINT     *CHAIND          ;Branch if not
MOV       *510,RO          ;Say we were...
.PRINT
.EXIT
1$: .PRINT     *NOCHN          ;Get addr of start of data
.EXIT
CHAIND: ,ASCIZ    /CTEST was chained to - and here's the data passed.../
NOCHN: .ASCIZ    /CTEST was not chained to/
.END    CTEST
```

## 2.7 .CHCOPY (FB and XM Only)

The .CHCOPY request opens a channel for input, logically connecting it to a file that is currently open by another job for either input or output. This request can be used by a foreground, background, or system job and must be issued before the first .READ or .WRITE request on that channel.

.CHCOPY is valid only on files on disk (including diskette) or DECtape. However, no errors are detected by the system if another device is used. (To close a channel following use of .CHCOPY, use either the .CLOSE or .PURGE request.)

Macro Call: .CHCOPY area,chan,ochan [,jobblk]

where:

area is the address of a three-word EMT argument block

chan is the channel the current job will use to read the data

ochan is the channel number of the other job's channel to be copied

jobblk is a pointer to a three-word ASCII logical job name that represents a system job (see the RT-11 System Utilities Manual)

Request Format:

<table><tr><td>13</td><td>chan</td></tr><tr><td colspan="2">ochan</td></tr><tr><td colspan="2">jobblk</td></tr></table>

## Notes:

1. If the other job's channel was opened with .ENTER in order to create a file, the copier's channel indicates a file that extends to the highest block that the creator of the file had written at the time the .CHCOPY was executed.

2. A channel open on a non-file-structured device should not be copied, because intermixture of buffer requests can result.

3. A program can write to a file (that is being created by the other job) on a copied channel just as it could if it were the creator. When the copier's channel is closed, however, no directory update takes place.

4. Foreground and background jobs may optionally leave the jobblk argument blank or set it to zero. This causes the job name to default to F if the background job issued the request, or to B if the foreground job issued the request.

Errors:

Code

## Explanation

0 Other job does not exist, does not have enough channels defined, or does not have the specified channel (ochan) open.

1 Channel (chan) already open.

## Example:

```prolog
;+
; .CHCOPY - This is an example in the use of the .CHCOPY request.
; The example consists of two programs; a Foresround job which
; creates a file and sends a message to a Background Program
; which copies the FG channel and reads a record from the file.
; Both Programs must be assembled and linked separately.
;-
    .TITLE CHCOPF.MAC
;+
; This is the Foresround program ...
;-
    .MCALL     .ENTER,.PRINT,.SDATW,.EXIT,.RCVDW,.CLOSE,.WRITW

STARTF:   MOV     #AREA,R5          ;R5 => EMT argument block
    .ENTER     R5,*,0,*FILE,*,5       ;Create a 5 block file
    .WRITW     R5,*,0,*RECD,#256,*,4      ;Write a record BG is interested in
    BCS         ENTERR             ;Branch on error
    .SDATW     R5,*,BUFR,*,2       ;Send message with info to BG
    ;           .                       ;Do some other processing
    .RCVDW     R5,*,BUFR,*,1       ;When it's time to exit, make sure
    .CLOSE     *0               ;BG is done with the file
    .PRINT     *FEXIT             ;Tell user we're exiting
    .EXIT                     ;Exit the Program
ENTERR:   .PRINT     *ERMSG       ;Print error message
    .EXIT                     ;then exit
```

```asm
FILE:        .RAD50      /DK QUFILE/          #File spec for .ENTER
                   .RAD50       /TMP/
AREA:        .BLKW         5                          #EMT argument block
BUFR:        .WORD         0                          #Channel #
                   .WORD         4                          #Block #
RECRD:        .BLKW         25G.                  #File record
ERMSG:        .ASCIZ       /?Enter Error?/     #Error message text
FEXIT:        .ASCIZ       /FG Job exiting/     #Exit message
                   .END             STARTF
```

```txt
;+
; This is the Background Program ...
;-
.MCALL ,CHCOPY,,RCVDW,,READW,,EXIT,,PRINT,,SDATW
```

```asm
STARTB:    MOV     *AREA,R5          ;R5 => EMT ars block
        .RCVDW    R5,*MSG,#2         ;Wait for message from FG
        BCS       1$               ;Branch if no FG
        .CHCOPY    R5,*0,MSG+2      ;Channel # is 1st word of message
        BCS       2$               ;Branch if FG channel not open
        .READW    R5,*0,#BUFF,*25G.,MSG+4 ;Read block which is 2nd word of msg
        BCS       3$               ;Branch if read error
        ;                  ;Continue Processing...
        .SDATW    R5,*MSG,#1       ;Tell FG we're thru with file
        .PRINT     *BEXIT           ;Tell user we're thru
        .EXIT                   ;then exit Program
1$:    MOV     *NOJOB,RO          ;RO => No FG error msg
        BR       4$               ;Branch to print msg
2$:    MOV     *NOCH,RO          ;RO => FG ch not open msg
        BR       4$               ;Branch...
3$:    MOV     *RDERR,RO          ;RO => Read err msg
4$:    .PRINT                 ;Print proper error msg
        .EXIT                   ;then exit.
AREA:    .BLKW     5              ;EMT argument blk
MSG:    .BLKW     3              ;Message buffer
BUFF:    .BLKW     25G.          ;File buffer
BEXIT:    .ASCIZ     /Channel-Record copy successful/
NOJOB:    .ASCIZ     /?No FG Job?/      ;Error messages...
NOCH:    .ASCIZ     /?FG channel not open?/
RDERR:    .ASCIZ     /?Read Error?/
        .END     STARTB
```

## 2.8 .CLOSE

The .CLOSE request terminates activity on the specified channel and frees it for use in another operation. The handler for the associated device must be in memory if the file was created with a .ENTER programmed request.

Macro Call: .CLOSE chan

Request Format:

| R0 = | 6 | chan |
| --- | --- | --- |

A .CLOSE request specifying a channel that is not open is ignored.

A file opened with .LOOKUP does not require any directory operations when a .CLOSE is issued, and the USR does not have to be in memory for such a .CLOSE. The USR is required if, while the channel is open, a request was issued that required directory operations. The USR is always required for special structured devices such as magtape.

A .CLOSE is required on any channel opened with .ENTER if the associated file is to become permanent.

## NOTE

Do not close channel 17(octal) if your program is overlaid, because overlays are read on that channel.

A .CLOSE performed on a file opened with .ENTER causes the device directory to be updated to make that file permanent. The first permanent file in the directory with the same name, if one exists, is deleted, provided that it is not protected. When a file that is opened with an .ENTER request is closed, its permanent length reflects the highest block written since it was entered. For example, if the highest block written is block number 0, the file is given a length of 1; if the file was never written, it is given a length of 0. If this length is less than the size of the area allocated at .ENTER time, the unused blocks are reclaimed as an empty area on the device.

In magtape operations, the .CLOSE request causes the handler to write an ANSI EOF1 label in software mode (using MM.SYS, MT.SYS, or MS.SYS) and to close the channel in hardware mode (using MMHD.SYS, MTHD.SYS, or MSHD.SYS).

Errors:

Code

## Explanation

3 A protected file with the same name already exists on the device. The .CLOSE is performed anyway, resulting in two files with the same name on the device.

.CLOSE does not return any other errors unless the .SERR request has been issued. If the device handler for the operation is not in memory, and the .CLOSE request requires updating of the device directory, a fatal monitor error is generated.

Example:

Refer to the examples for the .CSISPC and .WRITW requests, which show typical uses for .CLOSE.

## 2.9 .CMKT (FB and XM; SJ Monitor Special Feature)

The .CMKT request causes one or more outstanding mark time requests to be canceled (see the .MRKT programmed request). The .CMKT request is a special feature in the SJ monitor, and is selected with the timer support during the system generation process.

Macro Call: .CMKT area,id[,time]

where:

area is the address of a three-word EMT argument block

id is a number that identifies the mark time request to be canceled. If more than one mark time request has the same id, the request with the earliest expiration time is canceled. If id = 0, all non-system mark time requests (those in the range 1 to 176777) for the issuing job are canceled

time is the address of a two-word area in which the monitor returns the amount of time (clock ticks) remaining in the canceled request. The first word contains the high-order time, the second contains the low-order. If an address of 0 is specified, no value is returned. If id = 0, the time parameter is ignored and need not be indicated

Request Format:

<table><tr><td rowspan="3">R0 → area:</td><td>23</td><td>0</td></tr><tr><td colspan="2">id</td></tr><tr><td colspan="2">time</td></tr></table>

## Notes:

1. Canceling a mark time request frees the associated queue element.

2. A mark time request can be converted into a timed wait by issuing a .CMKT followed by a .TWAIT, and by specifying the same time area.

3. If the mark time request to be canceled has already expired and is waiting in the job's completion queue, .CMKT returns an error code of 0. It does not remove the expired request from the completion queue. The completion routine will eventually be run.

Errors:

Code

## Explanation

0 The id was not zero and a mark time request with the specified identification number could not be found (implying that the request was never issued or that it has already expired).

Example:

Refer to the example for the .MRKT request.

## 2.10 .CNTXSW (FB and XM Only)

A context switch is an operation performed when a transition is made from running one job to running another. The .CNTXSW request is used to specify locations to be included in a list when jobs are switched. Refer to the RT-11 Software Support Manual for further details.

The system always saves the parameters it needs to uniquely identify and execute a job. These parameters include all registers and the following locations:

34,36 Vector for TRAP instruction

40-52 System Communication Area

If an .SFPA request has been executed with a non-zero address, all floating-point registers and the floating-point status are also saved.

It is possible that both jobs want to share the use of a particular location not included in normal context switch operations. For example, if a program uses the IOT instruction to perform an internal user function (such as printing error messages), the program must set up the vector at 20 and 22 to point to an internal IOT trap handling routine. If both foreground and background wish to use IOT, the IOT vector must always point to the proper location for the job that is executing. Including locations 20 and 22 in the .CNTXSW list for both jobs before loading these locations accomplishes this. This procedure is not necessary for jobs running under the XM monitor. In the XM monitor, both IOT and BPT vectors are automatically context switched.

If .CNTXSW is issued more than once, only the latest list is used; the previous address list is discarded. Thus, all addresses to be switched must be included in one list. If the address (addr) is 0, no extra locations are switched. The list cannot be in an area into which the USR swaps, nor can it be modified while a job is running.

In the XM monitor, the .CNTXSW request is ignored for virtual jobs, since they do not share memory with other jobs. For virtual jobs, the IOT, BPT, and TRAP vectors are simulated by the monitor. The virtual job sets up the vector in its own virtual space by any of the usual methods (such as a direct move or an .ASECT). When the monitor receives a synchronous trap from a virtual job that was caused by an IOT, BPT, or TRAP instruction, it checks for a valid trap vector and dispatches the trap to the user program in user mapping mode. An invalid trap vector address will abort the job with the following fatal error message:

## ?MON-F-Inv SST (invalid synchronous system trap)

## Macro Call: .CNTXSW area,addr

where:

area is the address of a two-word EMT argument block

addr is a pointer to a list of addresses terminated by a zero word. The addresses in the list must be even and be one of the following:

a. in the range 2–476

b. in the user job area

c. in the I/O page (addresses

160000-177776)

Request Format:

<table><tr><td rowspan="2">R0 → area:</td><td>33</td><td>0</td></tr><tr><td colspan="2">addr</td></tr></table>

Errors:

| Code | Explanation |
| --- | --- |

0 One or more of the conditions specified by addr was violated.

## Example:

```asm
.TITLE CNTXSW.MAC
;+
; .CNTXSW - This is an example in the use of the .CNTXSW request.
; In this example, a .CNTXSW request is used to specify that location 20
; and 22 (IOT vectors) and certain necessary EAE registers be context
; switched. This allows both jobs to use IOT and the EAE simultaneously
; yet independently.
;-
.MCALL .CNTXSW,.PRINT,.EXIT

START: .CNTXSW *AREA,*SWLIST ;Issue the .CNTXSW request
BCC 1$ ;Branch if successful
.PRINT *ADDERR ;Address error (should not occur)
.EXIT ;Exit the program
1$: .PRINT *CNTOK ;Acknowledge success with a message
.EXIT ;then exit the program

SWLIST: .WORD 20 ;Addresses to include in context switch
.WORD 22 ;IOT & EAE vectors...
.WORD 177302 ;EAE registers...
.WORD 177304 ;
.WORD 177310 ;
.WORD 0 ;List terminator !!!

AREA: .BLKW 2 ;EMT argument block

ADDERR: .ASCIZ /? .CNTXSW Addressing Error ?/
CNTOK: .ASCIZ /.CNTXSW Successful/

.END START
```

## 2.11 .CRAW (XM Only)

The .CRAW request defines a virtual address window and optionally maps it into a physical memory region. Mapping occurs if you set the WS.MAP bit in the last word of the window definition block before you issue .CRAW. Since the window must start on a 4K word boundary, the program only has to specify which page address register to use and the window size in 32-word increments. If the new window overlaps previously defined windows, those windows are eliminated before the new window is created (except the static window reserved for a virtual program's base segment).

Macro Call: .CRAW area,addr

where:

area is the address of a two-word EMT argument block

addr is the address of the window definition block

The window status word (W.NSTS) of the window definition block may have one or more of the following bits set on return from the request:

WS.CRW set if address window was successfully created
WS.VNM set if one or more windows were unmapped to create and map this window
WS.ELW set if one or more windows were eliminated

## Request Format:

```txt
R0 → area: 36 2
addr
```

Errors:

Code

## Explanation

0 Window alignment error: the new window overlaps the static window for a virtual job. The window is too large or W.NAPR is greater than 7.

1 An attempt was made to define more than seven windows in your program. You should eliminate a window first (.ELAW), or redefine your virtual address space into fewer windows.

If the WS.MAP bit was set in the window definition block status word, the following errors can also occur:

Code

## Explanation

2 An invalid region identifier was specified.

4 The combination of the offset into the region and the size of the window to be mapped into the region is invalid.

## Example:

```asm
.TITLE XMCOPY
;+
; This is an example in the use of the RT-11 Extended Memory requests.
; The program is a file copy with verify utility that uses extended
; memory to implement 4k transfer buffers. The example utilizes most of
; the Extended Memory requests and demonstrates other programming
; techniques useful in utilizing the requests.
;-
.NLIST BEX
.MCALL .UNMAP,.ELRG,.ELAW,.CRRG,.CRAW,.MAP,.PRINT,.EXIT,.CLOSE
.MCALL .RDBBK,.WDBBK,.TTYOUT,.WDBDF,.RDBDF,.CSIGEN,.READW,.WRITW
JSW = 44 iJSW location
J.VIRT = 2000 ;Virtual Job bit in JSW
ERRBYT = 52 ;Error byte location
APR = 2 ;PAR/PDR for 1st window
APR1 = 4 ; " " 2nd "
BUF = WDB+W.NBAS ;Virtual addr of 1st buffer
BUF1 = WDB1+W.NBAS ; " " " 2nd "
CORSIZ = 4096. ;Size of buffer in words
PAGSIZ = CORSIZ/256. ;Pase size in blocks
WRNID = WDB+W.NRID ;Region ID addr of 1st region
WRNID1 = WDB1+W.NRID ; " " " " 2nd "
.ASECT ;Assemble in the Virt Job Bit
. = JSW
.WORD J.VIRT ;Make this a "virtual" Job
.PSECT ;Start code now
.WDBDF ;Create Window Def Blk Symbols
.RDBDF ; " Region " " "
START:: .CSIGEN *ENDCRE,*DEFLT,#0 ;Get filespecs, handlers, open files
BCS START ;Branch if error
```

INCB ERRNO
.CRRG \*CAREA, \*RDB
BCC 10\$
JMP ERROR
10\$: MOV RDB, WRNID
INCB ERRNO
.CRAW \*CAREA, \*WDB
BCC 20\$
JMP ERROR
20\$: INCB ERRNO
.MAP \*CAREA, \*WDB
BCC 30\$
JMP ERROR
30\$: CLR R1
MOV \*CORSIZ, R2
INCB ERRNO
READ: .READW \*RAREA, \*3, BUF, R2, R1
BCC WRITE
TSTB @@ERRBYT
BEQ PASS2
JMP ERROR
WRITE: MOV RO, R2
.WRITW \*RAREA, \*0, BUF, R2, R1
BCC ADDIT
INCB ERRNO
JMP ERROR
ADDIT: ADD \*PAGSIZ, R1
BR READ
PASS2: INCB ERRNO
.CRRG \*CAREA, \*RDB1
BCC 35\$
JMP ERROR
35\$: MOV RDB1, WRNID1

;\* EXAMPLE USING THE .CRAW REQUEST DOING \*
;\* IMPLIED .MAP REQUEST.

GETBLK:    MOV     \*CORSIZ,R2
        ,READW   \*RAREA,\*3,BUF1,R2,R1
        BCC       40\$
        TSTB   @\*ERRBYT
        BEQ       ENDIT
        JMP       ERROR
40\$:    MOV     R0,R2

70\$: CMP (R4)+,(R3)+
BNE ERRDAT
DEC R2
BNE 70\$
ADD \*PAGSIZ,R1
BR GETBLK

ENDIT:          .PRINT     \*ENDPRG
XCLOS:         .CLOSE       \*0
               .UNMAP        \*CAREA ,\*WDB
               .ELAW       \*CAREA ,\*WDB
               .ELRG         \*CAREA ,\*RDB
               .ELRG         \*CAREA ,\*ROB1
               .EXIT

\$ERR = 1x
\$Create a region
\$Branch if successful
\$Report error (JMP due to range!)
\$Move region id to Window Def BLK
\$ERR = 2x
\$Create window...
\$Branch if no error
\$Report error...
\$ERR = 3x
\$Explicitly map window...
\$Branch if no error
\$Report error
\$R1 = RT11 Block \* for I/O
\$R2 = \* of words to read
\$ERR = 4x
\$Try to read 4K worth of blocks
\$Branch if no error
\$EOF?
\$Branch if yes
\$Must be hard error, report it
\$R2 = size of buffer just read
.Write out the buffer
\$Branch if no error
\$ERR = 5x
\$Report error
\$Adjust block \*
\$Then so set another buffer
\$ERR = 6x
\$Create a region
\$Branch if no error
\$Report error
\$Get region id to window def BLK

;ERR = 7x
;Create window using implied .MAP
;Branch if no error
;Report error
;ERR = 8x
;R1 = RT11 block # again
;R2 = 4K buffer size
;Try to set 4K worth of input file
;Branch if no error
;EOF?
;Branch if yes
;Report hard error
;R2 = size of buffer read
;Try to set same size from output file
;Branch if no error
;ERR = 9x
;Report error
;Get output buffer address
;Get input buffer address
;Verify that data is the same
;It's not, report error
;Are we finished?
;Branch if we aren't
;Adjust block # for page size
;Go set another buffer pair

;Announce we're finished
;Close output file
;Explicitly unmap 1st window
;Explicitly eliminate 1st window
;Eliminate 1st region
;Unmap,eliminate 2nd window & region
;Exit Program

| Code | Explanation |
| --- | --- |

```asm
ERROR:     MOVB    @*ERRBYT,RO          #Make error byte code 2nd digit
        ADD       *'0,RO              #of error code...
        MOVB     RO,ERRNO+1         #Put it in error message
        .PRINT   #ERR                   #Print it...
        BR      XCLOS                  #Go close output file
ERRDAT:    .PRINT   #ERRBUF           #Report verify failed...
        BR      XCLOS                  #Go close output file

RDB:     .RDBBK   CORSIZ/32,          #,RDDBK defines Region Def Blk
WDB:     .WDBBK   APR,CORSIZ/32,       #,WDDBK defines Window Def Blk
RDB1:    .RDBBK   CORSIZ/32,       #Define 2nd region same way
WDB1:    .WDBBK   APR1,CORSIZ/32.,0,0,CORSIZ/32.,WS,MAP i and 2nd Window
                                #(but with mappins status set!)
CAREA:    .BLKW    2                    #EMT argument blocks
RAREA:    .BLKW    6
DEFLT:    .WORD   0,0,0,0             #No default extensions
ENDPRG:    .ASCIZ   / * End of XM Example Program */
ERR:     .ASCII   /?XM Request or I-O Error # /
ERRNO:    .ASCIZ.   /00/
ERRBUF:    .ASCIZ   /?Data Verification Error?/
ENDCRE = .                              #For CSIGEN - XM handlers loaded !
        .END    START
```

## 2.12 .CRRG (XM Only)

The .CRRG request directs the monitor to allocate a dynamic region in physical memory for use by the current requesting program.

Macro Call: .CRRG area,addr

where:

area is the address of a two-word EMT argument block

addr is the address of the region definition block for the region to be created

## Request Format:

[figure omitted]

Errors:

6 No region control blocks are available. You eliminate a region to obtain a region control block (.ELRG), or you can redefine your physical address space into fewer regions.

7 A region of the requested size cannot be created because not enough memory is available. The size of the largest available region is returned in R0.

10 An invalid region size was specified. A value of 0, or a value greater than the available amount of contiguous extended memory, is invalid.

## Example:

Refer to example for the .CRAW request.

## 2.13 .CSIGEN

The .CSIGEN request calls the Command String Interpreter (CSI) in general mode to process a standard RT-11 command string. In general mode, file .LOOKUP and .ENTER requests as well as handler .FETCH requests are performed.

The .CSIGEN request accepts a command string of the form dev:output-filespec = dev:input-filespec/options, and the following operations occur:

1. The handlers for devices specified in the command line are fetched.

2. .LOOKUP and/or .ENTER requests on the files are performed.

3. The option information is placed on the stack. See the end of this section for a description of the way option information is passed. Note that this call always puts at least one word of information on the stack.

When called in general mode, the CSI closes channels 0 through 10(octal).

.CSIGEN loads all necessary handlers and opens the files as specified. The area specified for the device handlers must be large enough to hold all the necessary handlers simultaneously. If the device handlers exceed the area available, your program can be destroyed. (The system, however, is protected.)

The three possible output files are assigned to channels 0, 1, and 2, and the six possible input files are assigned to channels 3 through 10(octal). A null specification causes the associated channel to remain inactive. For example, the following string

\*,LP:=F1,F2

causes channel 0 to be inactive since the first specification is null. Channel 1 is associated with the line printer, and channel 2 is inactive. Channels 3 and 4 are associated with two files on DK:, while channels 5 through 10 are inactive. Your program can determine whether a channel is inactive by issuing a .WAIT request on the associated channel, which returns an error if the channel is not open.

Macro Call: .CSIGEN devspc,defext[,cstrng][,linbuf]

## where:

devspc is the address of the memory area where the device handlers (if any) are to be loaded

defext is the address of a four-word block that contains the Radix-50 default file types. These file types are used when a file is specified without a file type (see Note 1)

cstrng is the address of the ASCIZ command string or a 0 if input is to come from the console terminal. (In an FB or XM environment, if the input is from the console terminal, an .UNLOCK of the USR is automatically performed while the string is being read, even if the USR is locked at the time.)

If the string is in memory, it must not contain a RET LF (octal 15 and 12), and must terminate with a zero byte. If the cstrng field is blank, input is automatically taken from the console terminal. This string, whether in memory or entered at the console, must obey all the rules for a standard RT-11 command string

linbuf is the storage address of the original command string. This is a user-supplied area, 81 decimal bytes in length. The command string is terminated with a zero byte. If this argument is omitted, the input command string is not copied to user memory

On return, R0 points to the first available location above the handlers, the stack contains the option information, and all the specified files have been opened.

## Note:

1. The four-word block pointed to by defext is arranged as:

Word 1: default file type for all input channels (3–10)

Words 2,3,4: default file types for output channels 0, 1, and 2, respectively

If there is no default for a particular channel, the associated word must contain 0. All file types are expressed in Radix-50. For example, the following block can be used to set up default file types for a macro assembler:

```txt
DEFEXT: .RAD50      "MAC"
        .RAD50      "OBJ"
        .RAD50      "LST"
        .WORD       0
```

In the command string:

```txt
*DTO:ALPHA,DT1:BETA=DT2:INPUT
```

the default file type for input is MAC; for output, OBJ and LST. The following cases are valid:

```txt
*DTO:OUTPUT=
*DT2:INPUT
```

In other words, the equal sign is not necessary if only input files are specified.

2. An optional argument (linbuf) is available in the .CSIGEN format that provides the user with an area to receive the original input string. The input string is returned as an ASCIZ string and can be printed through a .PRINT request.

3. The .CSIGEN request automatically takes its input line from an indirect command file if console terminal input is specified (cstrng = #0) and the program issuing the .CSIGEN is invoked through an indirect command file.

## Errors:

If CSI errors occur and input was from the console terminal, an error message describing the fault is printed on the terminal and the CSI retries the command. If the input was from a string, the carry bit is set and byte 52 contains the error code. In either case, the options and option-count are purged from the stack. These errors are:

## Code

## Explanation

0 Invalid command (such as bad separators, invalid file names, and commands that are too long).

1 A device specified is not found in the system tables.

2 A protected file of the same name already exists. A new file was not opened.

3 Device full.

4 An input file was not found in a .LOOKUP.

## Example:

```asm
.TITLE CSIGEN.MAC
;+
; .CSIGEN - This is an example in the use of the .CSIGEN request.
; The example is a single file copy program. The file specs are
; input from the console terminal, and the input & output files opened
; via the general mode of the CSI. The file is copied using synchronous
; I/O, and the output file is made permanent via the .CLOSE request.
;-
.MCALL .CSIGEN,.READW,.EXIT,.WRITW,.CLOSE,.SRESET
```

## ERRBYT=52

## 2.13.1 Passing Option Information

In both general and special modes of the CSI, options and their associated values are returned on the stack. A CSI option is a slash (/) followed by any character. The CSI does not restrict the option to printing characters, although you should use printing characters to avoid confusion. The option can be followed by a value, which is indicated by a : separator. The : separator is followed by an octal number, a decimal number, or by one to three alphanumeric characters, the first of which must be alphabetic. Decimal values are indicated by terminating the number with a decimal point (/N:14.). If no decimal point is present, the number is assumed to be octal. Options can be associated with files. For example, the command string

\*DK:FOO/A,DT4:FILE,OBJ/A:100

has two A options. The first is associated with the input file DK:FOO. The second is associated with the input file DT4:FILE.OBJ and has a value of 100(octal). The format of the stack output of the CSI for options is as follows:

<table><tr><td>Word #</td><td>Value</td><td>Meaning</td></tr><tr><td>1 (top of stack)</td><td>N</td><td>Number of options found in command string. If N=0, no options were found.</td></tr><tr><td rowspan="3">2</td><td rowspan="3">Option character and file number</td><td>Even byte = seven-bit ASCII option character</td></tr><tr><td>Bits 8-14 = number (0-10) of the file with which the option is associated</td></tr><tr><td>Bit 15 = 1 if the option had a value = 0 if the option had no value</td></tr><tr><td>3</td><td>Option value or next option</td><td>If bit 15 of word 2 is set, word 3 contains the option value. If bit 15 is not set, word 3 contains the next option character and file number, if any.</td></tr></table>

For example, if the input line to the CSI is

\*FILE/B:20.,FIL2/E=DT3:INPUT/X:SY:20

## on return, the stack is:

| Stack Pointer → | 4 | Three options appeared (X option has two values and is treated as two options). |
| --- | --- | --- |
|  | 101530 | Last option = X; with file 3, has a value. |
|  | 20 | Value of option X = 20(octal). |
|  | 101530 | Next option = X; with file 3, has a value. |
|  | 075250 | Next value of option X = RAD50 code for SY. |
|  | 505 | Next option = E; associated with file 1, no value. |
|  | 100102 | Option = B; associated with file 0 and has a value of 24. |
|  | 24 | (octal). |

As an extended example, assume the following string was input for the CSI in general mode:

```csv
*FILE[8,],LP:,SY:FILE2[20,]=PC:,DT1:IN1/B,DT2:IN2/M:7
```

Assume also that the default file type block is:

```asm
DEFEXT:     .RAD50      'MAC'          ;INPUT FILE TYPE
                   .RAD50      'OP1'          ;FIRST OUTPUT FILE TYPE
                   .RAD50      'OP2'          ;SECOND OUTPUT FILE TYPE
                   .RAD50      'OP3'          ;THIRD OUTPUT FILE TYPE
```

The results of the above CSI call are as follows:

1. An eight-block file named FILE.OP1 is entered on channel 0 on device DK;; channel 1 is open for output to the device LP;; a 20-block file named FILE2.OP3 is entered on the system device on channel 2.

2. Channel 3 is open for input from device PC;; channel 4 is open for input from a file IN1.MAC on device DT1;; channel 5 is open for input from IN2.MAC on device DT2:.

3. The stack contains options and values as follows:

## Contents

## Explanation

2 Two options found in string.

102515 Second option is M, associated with channel 5; has a value.

7 Numeric value is 7(octal).

2102 Option is B, associated with channel 4; has no value.

If the CSI were called in special mode, the stack would be the same as for the general mode call, and the descriptor table would contain:

```txt
OUTSPC: 15270 ;.RAD50 'DK'
23364 ;.RAD50 'FIL'
17500 ;.RAD50 'E'
60137 ;.RAD50 'OP1'
10 ;LENGTH OF 8 BLOCKS (DECIMAL)
46600 ;.RAD50 'LP'
```

| 0 | ;NO NAME OR LENGTH SPECIFIED |
| --- | --- |
| 0 |  |
| 0 |  |
| 0 |  |
| 75250 | ;.RAD50 'SY' |
| 23364 | ;.RAD50 'FIL' |
| 22100 | ;.RAD50 'E2' |
| 60141 | ;.RAD50 'OP3' |
| 24 | ;LENGTH OF 20 (DECIMAL) |
| 62170 | ;.RAD50 'PC' |
| 0 | ;NO NAME SPECIFIED |
| 0 |  |
| 0 |  |
| 16077 | ;.RAD50 'DT1' |
| 35217 | ;.RAD50 'IN1' |
| 0 | ;.RAD50 ' ' |
| 50553 | ;.RAD50 'MAC' |
| 16100 | ;.RAD50 'DT2' |
| 35220 | ;.RAD50 'IN2' |
| 0 | ;.RAD50 ' ' |
| 50553 | ;.RAD50 'MAC' |
| 0 |  |
| . |  |
| . |  |
| . |  |
| 0 | (12 more zero words are returned) |

Keyboard error messages that can occur when input is from the console keyboard include:

| Message | Meaning |
| --- | --- |
| ?CSI-F-Invalid command | Syntax error. |
| ?CSI-F-file not found | Input file was not found. |
| ?CSI-F-Device full | Output file does not fit. |
| ?CSI-F-Invalid device | Device specified does not exist. |
| ?CSI-F-Protected file | Output file specified already exists and is protected. |

## Notes:

1. In many cases, your program does not need to process options in CSI calls. However, you could inadvertently enter options at the console. In this case, it is wise to save the value of the stack pointer before the call to the CSI, and restore it after the call, so that no extraneous values are left on the stack. Note that even a command string with no options causes a word to be pushed onto the stack. This word indicates the number of options to follow.

2. Under an FB monitor, calls to the CSI that require console terminal input always do an implicit .UNLOCK of the USR while the string is being gathered. This should be kept in mind when using .LOCK calls.

## 2.14 .CSISPC

The .CSISPC request calls the Command String Interpreter in special mode to parse the command string and return file descriptors and options to the program. In this mode, the CSI does not perform any .CLOSE, .ENTER, .LOOKUP, or handler .FETCH requests.

Options and their associated values are returned on the stack. The optional argument (linbuf) can provide your program with the original command string.

.CSISPC automatically takes its input line from an indirect command file if console terminal input is specified (cstrng = #0) and the program issuing the .CSISPC is invoked through an indirect command file.

Note that in a foreground/background environment, calling the CSI performs a temporary and implicit .UNLOCK while the command line is being read.

Macro Call: .CSISPC outspc,defext[,cstrng][,linbuf]

## where:

outspc is the address of the 39-word block to contain the file descriptors produced by .CSISPC. This area can overlay the space allocated to cstrng, if desired

defext is the address of a four-word block that contains the Radix-50 default file types. These file types are used when a file is specified without a file type

cstrng is the address of the ASCIZ input string or a #0 if input is to come from the console terminal. If the string is in memory, it must not contain a RET LF (octal 15 and 12), and must terminate with a zero byte. If cstrng is blank, input is automatically taken from the console terminal or indirect file, if one is active

linbuf is the storage address of the original command string. This is a user-specified area, 81 bytes in length. The command string is terminated with a zero byte instead of RET LF (octal 15 and 12)

## Notes:

1. The file description consists of 39 words, comprising nine file descriptor blocks (five words for each of three possible output files; four words for each of six possible input files), which correspond to the nine possible files (three output, six input). If any of the nine possible file names are not specified, the corresponding descriptor block is filled with zeroes.

2. The five-word blocks hold four words of Radix-50 representing dev:file.type, and one word representing the size specification given in the string. (A size specification is a decimal number enclosed in square brackets ([ ]) that follows the output file descriptor.) For example:

\*DT3:LIST.MAC[15]=PC:

Using special mode, the CSI returns in the first five-word slot:

16101 Radix-50 for DT3

46173 Radix-50 for LIS

76400 Radix-50 for T

50553 Radix-50 for MAC

00017 Octal value of size request

```txt
AREA: .BLKW 2 ;EMT Argument block
STAT: .BLKW 4 ;Block for status
DEFEXT: .WORD 0,0,0,0 ;No default extensions
FEFAIL: .ASCIZ /?,FETCH Failed?/ ;Fetch failed message
NOFIL: .ASCIZ /?File Not Found?/ ;File not found
FILDEL: .ASCIZ /!File Deleted!/ ;Delete acknowledgment
.EVEN ;Fix boundary
OUTSP: .BLKW 5*3 ;Output specs so here
INSPEC: .BLKW 4*6 ;Input specs so here
HANLOD: .BLKW 1 ;Handlers begin loading here (if necessary)
.END START
```

In the fourth slot (starting at an offset of 36 bytes [octal] into outspc), the CSI returns:

| 62170 | Radix-50 for PC |
| --- | --- |
| 0 | No file name |
| 0 | specified |
| 0 | No file type given |

Since this is an input file, only four words are returned.

## Errors:

Errors are the same as in general mode except that invalid device specifications are checked only for output file specifications with null file names. Since .LOOKUP and .ENTER requests are not done, the valid error codes are:

Code Explanation

0 Invalid command line.
1 Invalid device.

## Example:

```asm
.TITLE CSISPC.MAC
;+
; .CSISPC - This is an example in the use of the .CSISPC request,
; The example uses the "special" mode of CSI to set an input
; specification from the console terminal, then uses the ,DSTATUS
; request to determine if the output device's handler is loaded;
; if not, a .FETCH request is issued to load the handler into
; memory. Finally a .DELETE request is issued to delete the specified
; file.
;-
```

```txt
.MCALL        .DSTATUS,.PRINT,.EXIT,.FETCH,.CSISPC,.DELETE
```

## 2.15 .CSTAT

This request furnishes you with information about a channel.

Macro Call: .CSTAT area,chan,addr

where:

area is the address of a two-word EMT argument block

chan is the number of the channel about which information is desired

addr is the address of a six-word block to contain the status

Request Format:

```txt
R0 → area: 27 chan
addr
```

## Notes:

The six words passed back to the user correspond to the following six points of information:

1. Channel status word (see the RT-11 Software Support Manual for details)

2. Starting block number of file (0 if sequential-access device, or if channel was opened with a non-file-structured .LOOKUP or .ENTER)

3. Length of file (0 if non-file-structured device, or if channel was opened with a non-file-structured .LOOKUP or .ENTER)

4. Highest relative block written since file was opened (no information if non-file-structured device). This word is maintained by the .WRITE/.WRITC/.WRITW requests

5. Unit number of device with which this channel is associated

6. Radix-50 of the device name with which the channel is associated (this is a physical device name, unaffected by any user name assignment in effect).

Errors:

Code Explanation

0 The channel is not open.

## Example:

```asm
,TITLE CSTAT.MAC
;+
; .CSTAT - This is an example in the use of the .CSTAT request.
; In this example, .CSTAT is used to determine the .RAD50
; representation of the device with which the channel is associated.
;-
    .MCALL      .CSTAT,.CSIGEN,.PRINT,.EXIT

START:    MOV     SP, R5          iSave current stack Pointer
        .CSIGEN   *DEVSDC,#DEFEXT       iOpen files
        MOV     R5, SP           iRestore SP to clear any CSI options
        .CSTAT    *AREA,#0,#ADDR       iGet the status
        BCS      NOCHAN           iChannel O not open
        MOV     *ADDR+10,R5         iPoint to unit #
```

```asm
MOV          (R5)+,RO          ;Unit * to RO
ADD          (PC)+,RO          ;Make it RAD50
.RAD50     / 0/
ADD          (R5),RO          ;Get device name
MOV          RO,DEVNAM      ;'DEVNAM' has RAD50 device name
.EXIT                   ;Exit the program

NOCHAN:   .PRINT    #MSG           ;Print error message
.EXIT                   ;then exit program

MSG:   .ASCIZ    /?No Output File?/       ;Error message
.EVEN                   ;Fix boundary
AREA:   .BLKW    5               ;EMT ars list
ADDR:   .BLKW    6               ;Area for channel status
DEVNAM:   .WORD    0               ;Storage for device name
DEFEXT:   .WORD    0,0,0,0             ;No default extensions

DEVSDC=.                                       ;Start CSI tables here...
```

## 2.16 .CTIMIO (Device Handler Only)

The .CTIMIO macro cancels the device time-out request in the handler interrupt service section. It is used when an interrupt occurs to disable the completion routine (see .TIMIO).

If the time interval has already elapsed and the device has, therefore, timed out, the .CTIMIO request fails. The completion routine has already been placed in the queue. The .CTIMIO call returns with the C bit set when it fails because the completion routine was already queued.

The device time-out feature must have been selected during the system generation process.

Macro Call: .CTIMIO tbk

where:

tbk is the address of the seven-word timer block shown in Table 2-1

Table 2-1: Timer Block Format

| Offset | Filled in By | Contents |
| --- | --- | --- |
| 0 | .TIMIO | High-order time word (expressed in ticks). |
| 2 | .TIMIO | Low-order time word (expressed in ticks). |
| 4 | monitor | Link to next queue element; 0 indicates none. |
| 6 | user | Owner's job number; 0 for background job, MAXJOB for fore-ground job, and job priority *2 for system jobs. MAXJOB is equal to (the number of jobs in the system * 2)-2. The job number for the foreground job is 2 in a system without system jobs, and 16 for a system with system jobs. The job number is set from the queue element. |
| 10 | user | Sequence number of timer request. The valid range of sequence numbers is from 177000 to 177377. |
| 12 | monitor | -1 |
| 14 | user | Address of the completion routine to execute if timeout occurs. The monitor zeroes this word when it calls the completion routine, indicating that the timer block is available for reuse. |

The .CTIMIO macro expands as follows:

```txt
.CTIMIO tbk
JSR R5,@$TIMIT ;POINTER AT END OF HANDLER
.WORD tbK - ,
.WORD 1 ;CODE FOR .CTIMIO
```

Example:

Refer to the example for the .TIMIO request.
