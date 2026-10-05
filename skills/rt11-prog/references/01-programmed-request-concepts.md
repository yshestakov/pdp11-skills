# RT-11 PRM reference: Ch.1.1 Programmed requests: EMT mechanism, request formats (FORMAT 1/2, area blocks), blank args, addressing modes, channels, device blocks, errors (C bit / byte 52), USR & swapping, using requests by category (init/control, I/O, files, CSI, timer, completion routines, F/B communication, XM, multiterminal, interrupt service, device handlers), V5 compatibility & conversion, summary tables 1-4..1-6

Source: RT-11 Programmer's Reference Manual AA-H378C-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' sometimes reads as ',' (`,MCALL` = `.MCALL`), 'R0' as 'RO', '#' as '\*' or '*'. Verify exact macro expansions against `sysmac_v53.mac`.

Contents:
- Chapter 1
- 1.1 Programmed Requests
- 1. Single-Job Monitor
- 2. Foreground/Background Monitor
- 3. Extended Memory Monitor
- 4. Multiterminal Feature
- 5. System Job Support
- 1.1.1 Programmed Request Implementation
- 1.1.2 System Conventions
- 1. The background job
- 2. The value of location 46
- 3. Monitor offset 374
- 4. Protecting program areas
- 1.1.3 Using Programmed Requests
- 1.1.4 Compatibility With Previous RT-11 Versions
- 1.1.5 Programmed Request Conversion
- 1.1.6 Programmed Request Summary

---

## Chapter 1

## Introduction to Advanced RT-11 Programming

Programmed requests and system subroutines are available as part of the RT-11 Operating System and can aid you in writing reliable and efficient programs.

Programmed requests provide a number of services to application programs. The requests function as calls to routines in the RT-11 monitor that perform these services. As system macros, they are defined in a system macro library that is stored on the system volume and named SYS-MAC.SML. In addition, macro routines are available in the system macro library that can help you write device handlers and interrupt service routines.

The file SYSMAC.MAC is not provided on the RT-11 distribution kit. However, you will need this file if you want to modify the system macro library.

You can create SYSMAC.MAC from the distributed file SYSMAC.SML by running the SPLIT utility. Type this CCL command:

.SPLIT ,SYSMAC.MAC=SYSMAC.SML/B:.,SYSM

This command creates the file SYSMAC.MAC on your default device. The variable ..SYSM represents the boundary along which to split SYSMAC.SML. Refer to the file CUSTOM.TXT on your distribution kit for the value to substitute for ..SYSM in the command line. Refer to the file UNSUP.TXT for more information on using the SPLIT utility.

If you are a FORTRAN programmer, you can access the RT-11 monitor services through calls to the system subroutine library called SYSLIB.OBJ, which is stored on the system volume. A character string manipulation package and two-word integer support routines are included in this library. The SYSLIB subroutines allow you to write almost all application programs in FORTRAN without having to do any assembly language coding.

This chapter tells you how to use programmed requests and subroutines effectively in your programs. Examples are provided to demonstrate their flexibility and value in working programs.

## 1.1 Programmed Requests

You issue a programmed request in your source program when a certain monitor service is required. The programmed request expands into the appropriate machine language code during assembly time. During program execution, this code requests the resident monitor to supply the service represented by the programmed request.

The services involve the following processes:

1. Initialization and control of operating system characteristics

2. Allocating system resources and reporting status

3. Command interpretation

4. File operations

5. Input/output operations

6. Foreground/background communications

7. Timer support

8. Program termination or suspension

9. System job communications

10. Extended memory functions

The system macro library (SYSMAC.SML) also contains several macros that are not programmed requests. These macros are provided to aid you in writing:

1. Interrupt service routines

2. Device handlers

3. Memory management control blocks

They are described in Chapter 2 along with the programmed requests.

Components of the RT-11 Operating System that support programmed requests are as follows:

## 1. Single-Job Monitor

The single-job (SJ) monitor supports most of the programmed requests. Table 1–4 lists the programmed requests that are supported by the SJ monitor. These programmed requests can manipulate files, perform input and output, set timer routines, check system resources and status, and terminate program operations.

## 2. Foreground/Background Monitor

Some programmed requests are provided for the foreground/background (FB) monitor only. Table 1–5 lists the programmed requests that are supported by the FB monitor in addition to those listed in Table 1–4. These programmed requests allow a program to set timer routines, suspend and resume jobs, and send messages and data between foreground and background jobs.

## 3. Extended Memory Monitor

The extended memory (XM) monitor provides additional programmed requests and features above those found in the FB monitor. The XM monitor extends the memory support capability of RT-11 beyond the

28K-word (plus I/O page) restriction imposed by the 16-bit address size. The XM monitor's programmed requests extend a program's effective logical addressing space (see Table 1–5).

## 4. Multiterminal Feature

The multiterminal feature of RT-11 allows your program to perform character input/output on up to 16 terminals. Programmed requests are available to perform input/output, attach and detach a terminal for your program, set terminal and line characteristics, and return system status information.

## 5. System Job Support

System job support allows users in a foreground/background or extended memory environment to extend the present standard foreground/background system to include up to eight jobs. Four system jobs are presently provided with the RT-11 system: the error logger, the device queue program (QUEUE), the transparent spooler package (SPOOL), and the communication package (VTCOM). Programmed requests allow programs to copy channels from other jobs, obtain job status information about jobs in the system, and send messages and data between any jobs in the system. The RT-11 Software Support Manual describes the system job feature in more detail.

Programmed requests perform most system resource control and interrogation functions. However, some communication is accomplished by directly accessing two memory areas: the system communication area and the monitor fixed-offset area.

The system communication area resides in locations 40 to 57(octal) and contains parameters that describe and control execution of the current job. This area holds information such as the Job Status Word, starting address of the job, User Service Routine (USR) swapping address, and the address of the start of the resident monitor. Some of this information is supplied by your program, while other data is supplied by the monitor and may not be changed.

The second memory communication area, the fixed-offset area, is accessed by a fixed-address offset from the start of the resident monitor. This area contains system values used to control monitor operation. Your program can examine or modify these values to determine the condition of the operating environment while a job is running. The RT-11 Software Support Manual describes in detail both the system communication area and the fixed-offset area.

This manual specifically describes programmed requests for RT-11 Version 5. Programmed requests for earlier versions of RT-11 and guidelines for their conversion are treated in Sections 1.1.4 and 1.1.5.

## 1.1.1 Programmed Request Implementation

1.1.1.1 EMT Instructions — A programmed request is a macro call followed by the necessary number of arguments. The macro code that corresponds to the macro call of a programmed request is expanded by the MACRO assembler when the programmed request appears in your program. The expansion arranges the arguments of the programmed request for the monitor and generates an EMT (emulator trap) instruction.

When an EMT instruction is executed, control passes to the monitor. The low-order byte of the EMT code provides the monitor with the information that tells it what monitor service is being requested.

The execution of the EMT generates a trap through vector location 30. This vector location is loaded at boot time with an address pointing to a location in the monitor. The monitor location contains the EMT processing code that services the interrupt caused by the EMT instruction.

Table 1–1 shows the codes that may appear in the low-order byte of an EMT instruction and the interpretation of these codes by the monitor.

Table 1-1: EMT Codes

| Low-Order Byte | Interpretation |
| --- | --- |
| 377 | Reserved; RT-11 ignores this EMT and returns control to the user program immediately. |
| 376 | Used internally by the RT-11 monitor; your programs should not use this EMT since its use would lead to unpredictable results. |
| 375 | Programmed request with several arguments; R0 points to a block of arguments that supports the user request. |
| 374 | Programmed request with one argument; R0 contains a function code in the high-order byte and a channel code in the low-order byte. |
| 360-373 | Used internally by the RT-11 monitor; your programs should never use these EMT codes since their use would lead to unpredictable results. |
| 340-357 | Programmed requests with the arguments on the stack and/or in R0. |
| 0-337 | Version 1 programmed requests with arguments both on the stack and in R0. They are supported for binary compatibility with Version 1 programs. |

EMT instructions should never appear in your programs except through programmed requests.

1.1.1.2 System Control Path Flow — Figure 1–1 shows system flow when a programmed request is executed.

In Figure 1-1, a programmed request in an application (or system utility) program is implemented with an EMT instruction. When your program is executed, the EMT instruction transfers control to the EMT processor code in the monitor. The user program counter (PC) and processor status word (PSW) are pushed onto the stack, and the contents of location 30 are placed in the program counter. Location 30 points to the EMT processor code in the monitor. Location 32 contains the PSW for the EMT trap. Byte 52 of the system communication area is loaded with an error code by the monitor if the monitor detects any errors during the EMT processing. In addition, the EMT processor uses R0 to pass back information to the program. All other registers except SP are preserved; .CSIGEN and .CSISPC return information on the stack.

The monitor either processes a programmed request entirely when it is issued or it performs partial processing and queues the request for further processing. The requests that require queued processing support completion routines (see Section 1.1.3.5). If a request results in an error prior to being queued, the completion routine is not entered, and the monitor returns to the user program with the carry bit set. If the request is queued, the completion routine is entered upon completion of further processing, regardless of the outcome.

Figure 1-1: System Flow During Programmed Request Execution

[figure omitted]

## 1.1.2 System Conventions

This section describes the system conventions that must be followed for the correct operation of programmed requests.

1.1.2.1 Programmed Request Format — To issue programmed requests from assembly language programs, you must set up the arguments in correct order and issue the appropriate EMT instruction. Macros have been created to help you do this. They are contained in the system macro library named SYSMAC.SML. Their use is recommended for maintaining program compatibility with future releases of RT-11 and for program readability. The macro names for all programmed requests except SOB start with a period (.) to distinguish them from symbols and macros you define.

Arguments supplied to a programmed request must be valid assembler expressions since the arguments are used as source fields in the instructions (such as a MOV instruction) when the macros are expanded at assembly time. All programmed requests that appear in your program must appear in a .MCALL directive to make the macro definition available from the system macro library, SYSMAC.SML. If the programmed request is specified by a .MCALL directive, the programmed request is obtained from the system macro library at assembly time. Alternatively, you can enable the automatic .MCALL feature of MACRO by using the .ENABL MCL directive.

Programmed requests have two formats that are accepted by the monitor. The first format specifies the programmed request followed by the arguments required by the request. The second format specifies the programmed request, the address of the argument block, and the arguments that will be contained in the argument block. Because the way you can set up the argument block and specify arguments to a programmed request can vary, read the sections on programmed request format and on blank arguments to be sure of correct programmed request operation.

## FORMAT 1

The first format for programmed requests is as follows:

    .PRGREQ Arg1,Arg2,...,Argn

where:

$$
\begin{array}{l l} \text {.PRGREQ} & \text {is the name of the programmed request} \\ \text {Arg1,Arg2,...,Argn} & \text {are the arguments used with the request} \end{array}
$$

Programmed requests using this format generate either an EMT 374 instruction or EMT 340 through 357 instructions.

Programmed requests that use an EMT 374 instruction set up R0 with the channel number in the even (low-order) byte and the function code in the odd (high-order) byte, as shown in Figure 1–2.

Figure 1-2: EMT 374 Argument

<table><tr><td></td><td>15</td><td>8</td><td>7</td><td>0</td></tr><tr><td>R0 =</td><td colspan="2">Function Code</td><td colspan="2">Channel Number(if applicable)</td></tr></table>

One programmed request that generates an EMT 374 is .DATE. The macro for this programmed request appears in the system macro library as:

```asm
.MACRO .DATE
MOV #10.*^0400,%0
EMT ^0374
.ENDM
```

The function code, which in this case is 10(decimal) is placed in the high-order byte of R0. A channel code of 0 is placed in the low-order byte.

For EMT 340 through 357, if there are arguments, they are placed either on the stack, in R0, or in R0 and on the stack.

The programmed request .CSIGEN is an example of a programmed request that generates an EMT 344. A simplified macro expansion of this programmed request is:

```asm
.MACRO ,CSIGEN DEVSPC,DEFEXT,CSTRNG,LINBUF
.IIF NB <LINBUF> MOV LINBUF,-(6.)
MOV DEVSPC,-(6.)
.IIF NB <LINBUF> INC (6.)
MOV DEFEXT,-(6.)
.IF B CSTRNG
CLR -(6.)
.IFF
.IF IDN CSTRNG,#0
CLR -(6.)
.IFF
MOV CSTRNG,-(6.)
.ENDC
.ENDC
EMT ^0344
.ENDM
```

When this programmed request is executed, all the specified arguments are placed on the user stack. Thus, the user stack would appear as shown in Figure 1-3.

Figure 1-3: Stack Set by .CSIGEN Programmed Request

[figure omitted]

The EMT processor then uses these arguments in performing the function of the programmed request .CSIGEN.

## FORMAT 2

The second format for programmed requests is as follows:

    .PRGREQ Area,Arg1,Arg2,...,Argn

where:

.PRGREQ is the name of the programmed request
Area is the address of an argument block
Arg1,Arg2,...,Argn are the arguments that will be contained in the
argument block

This format generates an EMT 375 instruction. Programmed requests that call the monitor via an EMT 375 use R0 as a pointer to an argument block. In general, the argument block appears as shown in Figure 1–4.

Figure 1-4: EMT 375 Argument Block

[figure omitted]

The programmed request format uses Area as a pointer to the argument block that contains the arguments Arg1 through Argn.

## .PRGREQ Area,Arg1,...,Argn

Blank fields are permitted. However, if the Area argument is empty, the macro assumes that R0 points to a valid argument block. If any of the fields Arg1 to Argn are empty, the corresponding entries in the argument list are left untouched. Thus,

## .PRGREQ Area,Arg1,Arg2

points R0 to the argument block at Area and fills in the first and second arguments, while

## .PRGREQ Area

points R0 to the block and fills in the first word — that is, the function code and channel number — without filling in any other arguments. Arguments that are left blank are discussed in the following section.

1.1.2.2 Blank Arguments — Any programmed request that uses an argument block assumes that any argument left blank has been previously loaded by your program into the appropriate memory location (exceptions to this are the .CHCOPY and .GTJB requests). For example, when the programmed request

## .PRGREQ Area, Arg1, Arg2

is assembled, R0 will point to the first word of the argument block. The first word has the function code in the high-order byte and the channel number in the low-order byte. Arg1 is in the second word of the argument block (that is, in address R0 plus 2), while Arg2 is in R0 plus 4.

There are two ways to account for arguments. You can let the MACRO assembler generate the instructions needed to fill up the argument block at run time, or you can write these instructions in your program, leaving the arguments in the programmed request blank for those that you have written in. DIGITAL recommends that you let MACRO generate the instructions, both for program clarity and for reduced chance of programming error.

The following examples are all equivalent in that the arguments have been accounted for either in the program instructions or in the programmed request.

MOV #ARG1,AREA+2

MOV #ARG2,AREA+4

, PRGREQ #AREA

is equivalent to

MOV #AREA,RO
,PRGREQ ,#ARG1,#ARG2

and also to

MOV #AREA,RO

MOV #ARG1,2(RO)

MOV \*ARG2,4(RO)

MOV #CODE\*400!CHANNEL,(RO)

, PRGREQ

This last example sets up all the arguments for the programmed request prior to executing the programmed request.

The following example shows how arguments are specified to the .TWAIT programmed request.

```asm
,TITLE     EXWAIT.MAC
,MCALL    .PRINT,.TWAIT
START:
WAIT:      .TWAIT   #EMTLST
        .PRINT   #MSG
        BR       WAIT
EMTLST:   .BYTE   0,24
        .WORD   TIME
TIME:   .WORD   0,10.*60
MSG:   .ASCIZ   /PRINT THIS EVERY TEN SECONDS/
        .END       START
```

The .TWAIT programmed request suspends a program and requires two arguments. The first argument is area, which points to the address of a two-word EMT argument block; the second argument is Time, which is a pointer to two words of time (high-order first, low-order second) expressed in ticks. In the example shown above, EMTLST is specified as an argument with the programmed request that points to the address of the EMT argument block. The first word of the argument block has a zero stored in the low-order byte representing the channel number and a function code of 24 stored in the high-order byte. The second word contains a symbolic pointer to the location (the second argument), which specifies the amount of time that the program will be suspended. It is defined as two words and, in this example, represents a 10-second interval. When run, the example program prints its message every ten seconds.

1.1.2.3 Addressing Modes — You must make certain that the arguments specified are valid source fields and that the address accurately represents the value desired. If the value is a constant or symbolic constant, use the immediate addressing mode [#]. If the value is in a register, use the register symbol [Rn]. If the value is in memory, use the label of the location whose value is the argument.

A common error is to use n rather than #n for numeric arguments. For example, when a direct numerical argument is required, the immediate mode causes the correct value to be put into the argument block. Thus

.PRGREQ #Area,#4

is correct, while

```csv
.PRGREQ #Area,4
```

is not correct since the contents of location 4 are placed into the argument block instead of the desired value 4.

However, the form

```csv
,PROREQ LIST,NUMBER
.
.
.
LIST: ,WORD AREA
NUMBER: ,WORD 4
```

is correct since the contents of LIST are the argument block pointer and the contents of NUMBER are the data value.

## NOTE

All registers except R0 are preserved across a programmed request. In certain cases, R0 contains information passed back by the monitor; however, unless the description of a request indicates that a specific value is returned in R0, the contents of R0 are unpredictable upon return from the request. Also, with the exception of calls to the Command String Interpreter, the position of the stack pointer is preserved across a programmed request.

You must be sure that the selected mode generates the correct value as a source operand in a MOV instruction. Check the programmed request-macro in the Macro Library (SYSMAC.SML) and expand the programmed request by hand or with the macro assembler (by using the .LIST MEB directive) to be sure of correct results.

1.1.2.4 Keyword Macro Arguments — The RT-11 MACRO assembler supports keyword macro arguments. All the arguments used in programmed request calls can be encoded in their keyword form (see the PDP-11 MACRO-11 Language Reference Manual for details).

In EMT 375 programmed requests, the high byte of the first word of the area (pointed to by R0) contains an identifying code for the request. Normally, this byte is set if the macro invocation of the programmed request specifies the area argument, and it remains unaffected if the programmed request omits the area argument. If the macro invocation contains CODE=SET, the high byte of the first word of the area is always set to the appropriate code, whether or not area is specified.

If CODE=NOSET is in the macro invocation, the high byte of the first word of area remains unaffected. This is true whether or not area is specified. This allows you to avoid setting the code when the programmed request is being set up. This might be done because it is known to be set correctly from an earlier invocation of the request using the same area, or because the code was statically set during the assembly process.

1.1.2.5 Channels and Channel Numbers — A channel is a data structure that is a logical connection between your program and a file on a mass storage device or on a serial device such as the line printer or terminal. The system provides 16(decimal) channels by default. When a file is opened on a particular device, a channel number is assigned to that file. The channel number can have an octal value from 0 to 376 (0 to 254 decimal). Thus, your program first opens a channel through a programmed request by specifying the device and/or file name, file type, and a channel number to the monitor. Your program refers to that file or device in all I/O operations thereafter by the assigned channel number. You can specify a device (non-file-structured) or a device and file name (file-structured).

Channel 255(decimal) is reserved for system use. Channel 15(decimal) is used by the system's overlay handler.

1.1.2.6 Device Blocks — A device block is a four-word block of Radix-50 information. You set up the block to specify a physical or logical device name, file name, and file type for use with a programmed request. This information is passed to the monitor when your program opens a file. The monitor uses the information to locate the referenced device and the file name in the corresponding directory.

For example, a device block representing the file FILE.TYP on device DK: could be written as

.RAD50 /DK /

.RAD50 /FIL/

.RAD50 /E /

.RAD50 /TYP/

The first word contains the device name, the second and third words contain the file name, and the fourth word contains the file type. Device, file name, and file type must each be left-justified in the appropriate field. This string could also have been written as

.RAD50 /DK FILE TYP/

Spaces must fill out each field. Also, the colon and period separators must not appear in the string since they are only used by the Command String Interpreter to delimit the various fields.

If the first word of a device block is the name of a mass-storage device such as a disk and the second word of the block is 0, the device block refers to an entire volume of the mass storage device in a non-file-structured manner.

1.1.2.7 Programmed Request Errors — Programmed requests use three methods of reporting errors detected by the monitor:

1. Setting the carry bit of the processor status word (PSW)

2. Reporting the error code in byte 52 of the system communications area

3. Generating a monitor error message

If a programmed request has been executed unsuccessfully, the monitor returns to your program with the carry bit set. The carry bit is returned clear after the normal termination of a programmed request. Almost all requests should be followed by a Branch Carry Set (BCS) or Branch Carry Clear (BCC) instruction to detect a possible error.

Because some programmed requests have several error codes — that is, errors can be generated for different reasons — byte 52 in the system communications area is used to receive the error code. Thus, when the carry bit is set, check byte 52 to find out the kind of error that occurred in the programmed request. The meanings of values in the error byte are described individually for each request. The error byte is always zero when the carry bit is clear. Your program should reference byte 52 with absolute addressing. Always address location 52 as a byte, never as a word, since byte 53 has a different usage. The following example shows how byte 52 can be tested for the error code.

Error messages generated by the monitor are caused by fatal errors, which cause your program to terminate immediately. Some fatal errors can be intercepted and have their values returned in byte 52 (see the .HERR/.SERR programmed requests).

1.1.2.8 User Service Routine (USR) Requirement — Many programmed requests require the USR to be in memory. Some of these requests always require a fresh copy of the USR to be read in because the code to execute them resides in the USR buffer area. Since the buffer area gets overlaid by data used to perform other system functions, the USR must be read in from the system device even if there is a copy of the USR presently in memory. Table 1–2 shows the programmed requests that require the USR.

Table 1-2: Programmed Requests Requiring the USR

<table><tr><td rowspan="2">Request</td><td colspan="3">Monitor</td></tr><tr><td>SJ</td><td>FB</td><td>XM</td></tr><tr><td>.CDFN</td><td>yes*</td><td>no</td><td>no</td></tr><tr><td>.CLOSE (see Note 1)</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.CSIGEN</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.CSISPC</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.DELETE</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.DSTATUS</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.ENTER</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.EXIT</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.FETCH</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.FPROT</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.GTLIN</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.HRESET</td><td>yes</td><td>no</td><td>no</td></tr><tr><td>.LOCK (see Note 2)</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.LOOKUP</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.QSET</td><td>yes*</td><td>yes*</td><td>yes</td></tr><tr><td>.RELEAS</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.RENAME</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.SFDAT</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>.SRESET</td><td>yes*</td><td>no</td><td>no</td></tr><tr><td>.TLOCK (see Note 3)</td><td>yes</td><td>yes</td><td>yes</td></tr></table>

Note 1: Only if channel was opened with an .ENTER programmed request

Note 2: Only if the USR is in a swapping state

Note 3: Only if the USR is not in use by another job

\* The requests marked with an asterisk always require a fresh copy of the USR to be read in before they can be executed.

USR requirements for programmed requests differ between the SJ and FB monitors as shown in the table. The .CLOSE programmed request on non-file-structured devices, such as a line printer or terminal, does not require the USR under any monitor.

The USR is not reentrant and cannot be shared by concurrent jobs. Thus, when the USR is in use by one job, another job requiring it must queue up for it. This is particularly important for concurrent jobs when devices such as magnetic tape or cassette are active. For example, USR file operations on tape devices require a sequential search of the tape. When a background program is running the USR, the foreground job is locked out until the tape operation is completed. You should be aware that this operation may take considerable time. The .SPFUN request can be used to perform asynchronous directory operations on tape. In the FB and XM monitors, the .TLOCK request can be used by a job to check USR availability.

Any request that requires the USR to be in memory can also require that a portion of your program be saved temporarily in the system device swap file (that is, "swapped out" and stored in the file SWAP.SYS to provide room for the USR). The USR is then read into memory. Although swapping is invisible to you in normal operation, you must be aware of it and take some care in your programming. For example, the argument block being passed to the USR must not be in the area that is swapped over. You can optimize programs so that they require little or no swapping, thereby saving time.

Consider the following items if a swap operation is necessary.

## 1. The background job

If a .SETTOP request in a background job specifies an address beyond the point at which the USR normally resides, a swap is required when the USR is called. Section 2.79 details the operation of the .SETTOP request. This case is not encountered in XM because the USR is always resident.

## 2. The value of location 46

If you assemble an address into word 46 or move a value there while the program is running, RT-11 uses the contents of that word as an alternate place to swap the USR. If location 46 is zero, this indicates that the USR will be at its normal location in high memory. If the USR does not require swapping, this value is ignored.

A foreground job must always have a value in location 46 unless it is certain that the USR will never be swapped. If the foreground job does not allow space for the USR and a swap is required, a fatal error occurs. The SET USR NOSWAP command makes the USR permanently resident.

If you specify an alternate address in location 46, the SJ monitor does not verify the validity of the USR swap address. Thus, if the area to be swapped overlays the resident monitor, the system is destroyed.

## 3. Monitor offset 374

The contents of monitor offset 374 indicate the size of the USR in bytes.

Programs should use this information to dynamically determine the size of the region needed to swap the USR.

## 4. Protecting program areas

Make sure that certain areas of your program do not get overlaid when you swap in the USR. These areas are the program stack, any parameter block for calls to the USR, the EMT instruction that invoked the USR, I/O buffers, device handlers, interrupt service routines, queue elements, defined channels, and completion routines in use when the USR is being called.

The RT-11 Software Support Manual provides additional information on the USR.

## 1.1.3 Using Programmed Requests

This section describes how to use and implement programmed requests to access the various monitor services. Chapter 2 contains, in alphabetical order, detailed descriptions of each request, including examples.

1.1.3.1 Initialization and Control — Typically, you use several programmed requests to control the operating environment in which your program is running. These requests can include control of memory allocation, I/O access, devices, and error processing.

## MEMORY ALLOCATION

The memory needs of a program are specified to the monitor by the .SETTOP request. When loaded, a program occupies the memory specified by its image created at link time. To obtain more memory, a .SETTOP request is executed, with R0 containing the highest address desired. The monitor returns the highest address available. Resident handlers or foreground jobs can prevent all the memory that is desired from being available to the program. If the memory requirements of the running program permit, the monitor retains the User Service Routine (USR) in memory, which reduces swapping. Otherwise, the monitor will automatically remove the USR from memory and then swap part of the user program to the swap file called SWAP.SYS on the system device whenever the USR must be reloaded to process a request. The .SETTOP request then allows you to determine how much memory is available and to control monitor swapping characteristics. See the .SETTOP programmed request in Chapter 2 for special optional features provided in an extended memory environment. Additional information on the .SETTOP request is also given in the RT-11 Software Support Manual.

If a program needs so much memory that the USR must swap, swapping will automatically occur whenever a USR call is made. However, if a program knows what file operations are necessary, and if these operations can be consolidated and performed at one time, the efficiency of the system can be enhanced in the following manner: request the USR to be swapped in, have it remain resident while a series of consecutive USR operations is performed, then swap the USR out when the sequence of operations is completed.

Three programmed requests control USR swapping. The request .LOCK causes the USR to be made resident for a series of file operations. It can operate by: (1) requiring a portion of your program to be written to the swap blocks prior to reading in the USR; (2) only requiring a fresh copy of the USR if the USR buffer is overwritten; or (3) not requiring the USR to be read in if it finds the USR intact. The request .UNLOCK swaps your program back in if it was swapped out, and the USR is overwritten; otherwise, no swapping occurs. The request .TLOCK makes the USR resident in foreground/background programs, but only if the USR is not currently servicing another job's file requests at the time the .TLOCK request is issued. This check prevents a job from becoming blocked while the USR is processing another job's request. When a .TLOCK succeeds, the USR is ready to perform an operation immediately. In a single-job environment, the .TLOCK request performs exactly like the .LOCK request.

RT-11 provides 16(decimal) channels as part of the job's impure area — that is, 16 files can be active at one time. Up to 255(decimal) channels can be activated with the .CDFN request. This request sets aside memory inside the job area to provide the storage required for the status information on the additional channels. Once the .CDFN request has been executed, as many channels as specified can be active simultaneously. Use the .CDFN request during the initialization phase of your program. The keyboard monitor command CLOSE does not work if you define new channels with the .CDFN programmed request.

The .CNTXSW request allows the job to add memory locations to the list of items to be context-switched. The request itself does not cause a context switch to occur.

## INPUT/OUTPUT ACCESS

Each pending I/O, message, or timer request must be placed into one of the monitor queues. These are then processed by the monitor on a first-in first-out basis, by job priority, or by time of expiration. In RT-11, all I/O transfers are queued to allow asynchronous processing of the request. A queue is a list of elements, each element being seven words long (ten words [decimal] long when using the extended memory monitor). When your program issues a data transfer programmed request, the information specifying the transfer is stored by the monitor in a queue element. This information is passed to the device handler, which then processes the I/O transfer.

Each job, whether background or foreground, initially has only a single queue element available. Additional queue elements may be set aside with a .QSET request. The .QSET request declares where in memory the additional queue elements will go and how many elements there will be. If you do not include a .QSET request in your program, the monitor uses the queue element set aside in the job's impure area. In this case, since only one element is available for each job, all operations would be synchronous. That is, any request issued when the available queue element list is empty has to wait for that element to become free. The number of queue elements necessary equals the number of asynchronous operations pending at any time.

## DEVICES

The .DEVICE request turns off any special devices that are being used by the running program upon program termination. This request (available only in FB or XM) allows you to specify a set of device control register addresses and a value to be set in each register on job exit. When a job is terminated — either normally, by an error condition, or by a CTRL/C — the specified values are set in the specified locations.

In SJ, a hard reset is done at .EXIT or CTRL/C. This clears all devices.

Loading a background job with a GET, R, or RUN command, or loading a foreground or system job with a FRUN and SRUN command, respectively, alters most locations in the vector area 0 to 476. RT-11 automatically prevents alteration of all locations used by the system, such as the clock, the console terminal, and all vectors used by handlers that are loaded. If a foreground job in a foreground/background environment accesses a device directly through an in-line interrupt service routine, the foreground job must notify the monitor that it must have exclusive use of the vectors. You use the .PROTECT programmed request to allow the foreground job to gain exclusive use of a vector. The .PROTECT request can also be used by either the foreground or background job, prior to setting the contents of a vector, to test whether the vectors are already controlled by a job. This serves as further protection against jobs interfering with each other. An .UNPROTECT programmed request relinquishes control of a vector, making the vector available to both the background and foreground jobs.

The request .SPFUN is available for performing special functions on devices such as magnetic tape. .SPFUN requests are used for such functions as rewind or space-forward operations.

## ERROR PROCESSING

During the course of program execution, errors can occur that cause the monitor to stop the program and print a MON-F error message. Examples include directory I/O errors, monitor I/O errors on the system device, or I/O requests to nonexistent devices. Some programs cannot afford to allow the monitor to abort the job because of such errors. For example, in the case of RT-11 multi-user BASIC, a directory I/O error affecting only one of the users should not cause the whole program to abort. For such applications, a pair of requests is provided, .HERR and .SERR. A .HERR request (normal default) indicates that the monitor will handle severe errors and stop the job. A .SERR request causes the monitor to return most errors to your program in byte 52 for appropriate action.

In addition to processing I/O errors through .HERR and .SERR requests, you can also handle certain fatal errors through the .TRPSET or .SFPA requests. You use these requests to prevent your program from aborting due to a trap to location 4 or 10(octal), or to the exception traps of the Floating Point Processor (FPP) or Floating Point Instruction Set (FIS). A .TRPSET request specifies the address of a routine that the monitor enters when a trap to location 4 or 10 occurs. A .SFPA request specifies the address of a floating-point exception routine that is called when an exception trap occurs.

1.1.3.2 Examining System Information and Reporting Status — Several programmed requests interrogate the system for specific details about a device or file that your program may be using.

The .DATE request obtains the system date, which then can be printed on a report or entered as a data record in a file. The time-of-day can be obtained with a .GTIM request and used in the same way. A program can set the system date and/or time by using the .SDTTM programmed request. Changing the date or time has no effect on any outstanding mark time or timed wait requests.

With a .GTJB request you can obtain information on whether the job is running in the foreground or background, the memory limits of the job, the virtual high limit for a job created with the linker /V option (XM only), the unit number of the job's console terminal (if you are using the multiterminal feature), the address of the job's channel area, the address of the job's impure area, and the job's logical job name (if you are using a monitor with the system job feature).

Status information on a file — such as its starting block, its length, and the device it is located on — can be obtained with a .CSTATUS request. Status information on a device — such as its block length and controller-assignment number — can be obtained with a .DSTATUS request.

The .MTGET and .MTSTAT programmed requests provide multiterminal status information when the multiterminal feature is being used.

The programmed requests .MFPS and .MTPS read the priority bits and set the priority and T-bits in the processor status word (PSW). These requests allow a program to run without change on any processor from an LSI-11 to a PDP-11/60.

1.1.3.3 Command Interpretation — Two of the most useful programmed requests are .CSIGEN and .CSISPC. These requests call the Command String Interpreter (CSI), which is part of the USR. They are used to process standard RT-11 command strings in the following general form:

\*Dev:Output/Option = Dev:Input/Option

The asterisk is printed on the terminal by the monitor. The RT-11 system programs use the same command string (see the RT-11 System Utilities Manual).

The .CSIGEN request analyzes the string for correct syntax, automatically loads the required device handlers into memory, opens the files specified in the command, and returns to your program with option information. Thus, with one request, a language processor such as the FORTRAN compiler is ready to input from the source files and output the listing and binary files. You can specify options in the command string to control the operation of the language processor. The .CSIGEN request uses channels 0 through 2 to accommodate three output file specifications and channels 3 through 10(oc-tal) to accommodate six input file specifications.

The .CSISPC request provides you with the services of the command processor, but allows you to do your own device and file manipulation. When you use .CSISPC, the CSI obtains a command string, analyzes it syntactically, places the results in a table, and passes the table to your program for appropriate action.

The .GTLIN request obtains one line of input at a time instead of one character. These three requests support the indirect file function and allow your program to obtain one line at a time from an indirect file. Thus, if your program was started through an indirect file, the line is taken from the indirect file and not the terminal. The .GTLIN request has an optional argument which forces input to come from the terminal. The feature is useful if your program requires information which can be supplied only at run time.

1.1.3.4 File Operations — A device handler is the normal RT-11 interface between the monitor and the peripheral device on which file operations are performed. The console terminal handlers (in FB and XM) and the interjob message handlers are part of the resident monitor and require no attention on your part. All other device handlers are loaded into memory with either a .FETCH request from the program or a LOAD command from the keyboard before any other request can access that device. Section 1.1.3.5 of this manual describes the use of programmed requests for performing I/O operations. The RT-11 Software Support Manual describes how to write device handlers for RT-11.

Once the handler is in memory, a .LOOKUP request can locate existing files and open them for access. New files are created with an .ENTER request. Space for the file can be defined and allocated as:

1. One-half the size of the largest unused space or all of the second largest space, whichever is larger (the default)

2. A space of a specific size

3. As much space as possible

The way the system allocates the space depends upon the parameter specified by you as the file size argument of the .ENTER request or specified in a .CSIGEN command string.

When file operations are completed, a .CLOSE request makes the new file permanent in the directory. A .PURGE request can free the channel without making the file permanent in the directory. Existing permanent files can be renamed with a .RENAME request or deleted with a .DELETE request.

Two other requests, .SAVESTATUS and .REOPEN, add to the flexibility of file operations. The .SAVESTATUS request stores the current status of a file that has been opened with a .LOOKUP request and makes the file temporarily inactive, thus freeing the channel for use by another file. The .REOPEN request causes the inactive file to be reactivated on the specified channel, and I/O continues on that channel. In this manner, you can open more files than there are channels. If, in addition, you lock the USR in memory, you can open all the files your job needs while maintaining system swapping efficiency. The procedure is:

1. Lock the USR in memory, and open the files that are needed.

2. Issue the .SAVESTATUS request.

3. Release the USR.

4. Issue a .REOPEN request each time a file is needed.

5. Lock USR, and use the .CLOSE request to make the files permanent.

Because a .REOPEN request does not require any I/O, all USR swapping and directory motion can be isolated in the initialization code for an application, improving program efficiency.

The creation date and protection status of a file can be modified by using the .SFDAT and .FPROT requests, respectively.

The .SFDAT request allows you to change the date that appears in a file's directory entry listing. You may want to do this for a file that you update in place, for example, or if the original creation date was in error.

The .FPROT request protects a file against deletion, or removes protection so that a file can be deleted by a .DELETE, .ENTER, or .RENAME request. The contents of a protected file are not protected against modification.

1.1.3.5 Input/Output Operations — You can perform I/O in three different modes:

• synchronous

\- asynchronous

\- event-driven

These modes allow you to optimize the overlap of CPU and I/O processing.

The programmed requests .READW and .WRITW perform synchronous I/O — that is, the instruction following the request is not executed until the I/O transfer is completely finished; thus the program and the I/O process are synchronized.

The program requests .READ, .WRITE, and .WAIT perform asynchronous I/O — that is, the .READ or .WRITE request adds the transfer request to the queue for the device; if the device is inactive, the transfer begins; control returns to the user program before the transfer is completed. The .WAIT programmed request, however, blocks the program until the transfer is completed. This allows the I/O operation to be completed before any further processing is done. Asynchronous I/O is most commonly used for double buffering.

Program requests such as .READC and .WRITC perform event-driven I/O — that is, they initiate a completion routine when the transfer is finished.

Event-driven I/O is practical for conditions where system throughput is important, where jobs are divided into overlapping processes, or where processing timings are random. The last condition is the most attractive case for using event-driven I/O because processor timing may range up to infinity in that a process is never completed.

Since the completion routine is essential to event-driven I/O, the next section presents general guidelines for writing completion routines.

## COMPLETION ROUTINES

Completion routines are part of your program. They execute following the completion of some external operation, interrupting the normal program flow. On entry to an I/O completion routine, Register 0 contains the contents of the Channel Status Word and Register 1 contains the channel number for the operation. The carry bit is not significant.

Completion routines are handled differently, depending on whether the program is being run under the SJ monitor or the FB and XM monitors. Under the SJ monitor, completion routines are totally asynchronous and can interrupt each other. An interrupted completion routine is resumed when the interrupting routine is finished. Unlike completion routines run under FB and XM monitors, which are serialized and run at priority 0, completion routines run under an SJ monitor are nested. In addition, they execute not at priority 0, but at the same priority as the device whose interrupt scheduled them. For example, the completion routine resulting from a .WRITC programmed request to device TT: runs at priority 4. Completion routines from timer requests run at the same priority as the system clock. This is particularly important on LSI-11 and PDP 11/03 systems that have only two interrupt levels, ON and OFF, because clock interrupts may be lost while lengthy completion routines execute. Under the FB and XM monitors, completion routines do not interrupt one another. Instead, they are queued, and the next routine is not entered until the first is completed.

If the foreground job is running and a foreground I/O transfer completes and wants a completion routine, that routine is entered immediately if the foreground job is not already executing a completion routine. If it is in a completion routine, that routine continues to termination, at which point other completion routines are entered in a first-in first-out order. If the background job is running (even in a completion routine) and a foreground I/O transfer completes with a specified completion routine, execution of the background job is suspended and the foreground routine is entered immediately.

Also under the FB and XM monitors, it is possible to request a completion routine from an in-line interrupt service routine through a .SYNCH programmed request. This allows the interrupt service routine to issue other programmed requests to the monitor.

Restrictions that must be observed when writing completion routines are as follows:

1. Requests that require the USR must not be issued within a completion routine. A fatal monitor error is generated if the USR is called from a completion routine.

2. Completion routines should never reside in memory space that is used for the USR, since the USR can be interrupted when I/O terminates and the completion routine is entered. If the USR has overlaid the routine, control passes to a random place in the USR, with a HALT or error trap being the likely result.

3. Registers other than R0 and R1 must be saved upon entry to completion routines and restored upon exiting. Registers cannot transfer data between the mainline program and the completion routine.

4. Under the XM monitor, completion routines must remain mapped while the request is active and the routine can be called.

5. The completion routine must exit with an RTS PC instruction because the routine was called from the monitor with a JSR PC,ADDR, where ADDR is the user-supplied entry point address. If you exit completion routines with an .EXIT request, your job will abort. An exit from a completion routine in FB or XM can be done by using an .SPCPS request to change the mainline PC to point to an .EXIT in the main code. As soon as all completion routines are done, the exit will be executed.

6. Under the XM monitor, completion routines scheduled as a result of a .SYNCH run in kernel mapping, not user mapping.

Frequently, a program's completion routine needs to change the flow of control of the mainline code. For example, you may wish to establish a schedule among the various tasks of an application program after a certain time has elapsed, or after an I/O operation is complete. Such an application needs to redirect the mainline code to a scheduling subroutine when the application's timer or read/write completion routine runs. The .SPCPS programmed request, which can only be used in a foreground/background or extended memory environment, saves the mainline code program counter and processor status word, and changes the mainline code program counter to a new value. If the mainline code is performing a monitor request, that request finishes before rerouting can occur.

## TERMINAL INPUT/OUTPUT

Several programmed requests are available to provide an I/O capability with the console terminal: a .TTYIN request obtains a character from the console; a .TTYOUT request prints a character on the terminal; long strings of characters — even multiple lines — are output with the .PRINT request. Programs can also issue .TTINR and .TTOUTR requests, which indicate that a character is not available or that the output buffer is full. The program can then resume operation and try again at a later time. A .RCTRO request forces the terminal output to be reactivated after a CTRL/O has been typed to suppress it, so that urgent messages will be printed.

You can use the .TTYIN/.TTINR requests in special (single-character) mode by setting bit 12 of the Job Status Word. See the .TTYIN programmed request for a description of special mode.

## MULTITERMINAL REQUESTS

The RT-11 multiterminal feature allows your program to perform input/output on up to 17 terminals. Several programmed requests allow you to perform I/O on these terminals. Before issuing any of these programmed requests to a terminal, you must issue the .MTATCH request, which reserves the specified terminal for exclusive use by your program. The terminal cannot then be used by any other job until you issue the .MTDTCH request to detach the terminal.

The .MTIN request returns to a program characters that are typed at the terminal, while the .MTOUT and .MTPRNT requests send characters to a terminal. These requests are analogous to the .TTYIN, .TTYOUT, and .PRINT requests. Note that the .TTYIN/.TTINR, .TTYOUT/.TTOUTR, and .PRINT requests can only be used with the console terminal.

You can set terminal and line characteristics with the .MTSET request. You provide a four-word status block that contains the terminal status word, the character of the terminal requiring fillers and the number of fillers required for this character, the width of the carriage (80 characters by default), and system terminal status. The status of a terminal can be obtained by issuing the .MTGET request. The .MTSTAT request provides multiterminal system status information.

1.1.3.6 Foreground/Background Communications — Communication between foreground and background jobs is obtained through the programmed requests .SDAT and .RCVD. These requests also have three modes (synchronous, asynchronous, and event driven) that allow transfer of buffers between the two jobs as if I/O were being done. The sending job treats a .SDAT request as a write, and the receiving job treats .RCVD as a read. In the case of .RCVD requests, the receiving buffer must be one word longer than the number of words expected. When the data transfer is completed, the first word of the buffer contains the number of words actually sent.

Jobs receiving messages can be activated when messages are sent through .RCVDC completion routines, while the sending jobs use .SDATC completion routines. The .MWAIT request is used for synchronizing message requests. It is similar to the .WAIT request that is used for normal I/O.

If you want one job in a foreground/background environment to read or write data in a file opened by the other job, use the .CHCOPY request. For example, when the background job is processing data that is being collected by the foreground job, the .CHCOPY request allows you to obtain channel information from the foreground job and to use that channel information to control a read or write request.

The foreground/background monitor always causes a context switch of critical items such as machine registers, the job status area, and floating-point processor registers when a different job is scheduled to run because it has a higher priority, or because the current job is blocked and a lower priority job is runnable. When the monitor saves a job's context, it saves the job-dependent information on the job's stack so that this information can be restored when the job is runnable again.

1.1.3.7 Timer Support — Timer support by the monitor is provided through the .MRKT request. With the .MRKT request, you specify the address of a routine that is to be entered after a specified number of clock ticks. Like I/O completion routines, .MRKT routines are asynchronous and independent of the main program. After the specified time elapses, the main program is interrupted, the timer completion routine executes, and control returns to the interrupted program.

Pending .MRKT requests — as many as the queue can hold — are identified by number. Pending timer requests can be canceled with a .CMKT request. .MRKT requests are normally used as a scheduling tool where jobs are scheduled on the basis of clock events, detected by timer completion routines.

The programmed requests .MRKT/.CMKT and .TIMIO/.CTIMIO require request identification words as an argument. Certain ranges of values are reserved for different uses as shown in the following table.

| Range | Use |
| --- | --- |
| 1-176777 | For user applications with .MRKT/.CMKT. Values in this range are canceled if a .CMKT request is issued with a value of 0. |
| 177000-177377 | For use in device handler .TIMIO/.CTIMIO requests. To ensure a unique value for each handler, DIGITAL suggests that the value be assigned as 177000 + devcod, where devcod represents the device identifier value used in the .DRDEF macro at the beginning of the handler. |
| 177400-177477 | Reserved for multiterminal support. |
| 177500-177677 | Reserved. |
| 177700 | Used by the .TWAIT request. |
| 177701-177766 | Reserved. |
| 177767-177777 | DECnet. |

Values in the range 177000 to 177677 must be canceled individually by the routine that issued the .TIMIO request. This would occur, for example, in handler abort code.

Values in the range 177700 to 177777 are automatically canceled whenever a program terminates or aborts.

A job can be suspended for a specified time interval with a .TWAIT request. For example, the .TWAIT request will allow a compute-bound job to relinquish CPU time to the rest of the system, permitting other jobs to run.

1.1.3.8 Program Termination or Suspension — Many jobs come to an execution point where there is no further processing necessary until an external event occurs. In the FB or XM environment such a job can issue a .SPND request to suspend the execution of that job. While the foreground job is suspended, the background job runs. When the desired external event occurs, it is detected by a previously requested completion routine, which executes a .RSUM request to continue the job at the point where it was suspended.

When a job is ready to terminate or reaches a serious error condition, it can reset the system with the .SRESET and .HRESET requests. .SRESET is a soft reset. That is, the monitor data base for the job is reinitialized, but queued I/O is allowed to run to completion. .HRESET is a hard reset where all I/O for the job is stopped (by a RESET instruction in the SJ monitor or by calls to the handlers in an FB environment).

Use the programmed request .EXIT in a background job to return control to the keyboard monitor by causing program termination. If Register 0 contains a zero upon execution of this request, a hard reset is performed, and the commands REENTER, CLOSE, and START are disabled. If Register 0 contains a non-zero value upon exit from your program, a soft reset is done, and these commands are not disabled. In a foreground job, an .EXIT programmed request stops the job but does not return control to the keyboard monitor. The job can be removed from memory by the UNLOAD command.

You may initiate the execution of another program with a .CHAIN request from a background job. Files remain open across a .CHAIN request and data is passed in memory to the chained job, so that it can adjust processing. In FORTRAN, channel information is stored in the job's impure area, and this information is not preserved across a .CHAIN request. Thus, close any channels in the first program, and reopen them in the program being chained to.

1.1.3.9 System Job Communications — System job support allows communications between any two jobs in the system. The background job, designated by the logical job name 'B', and the foreground job, designated by the logical job name 'F', can send and receive messages between each other by using the .RCVD and .SDAT programmed requests.

All jobs (that is, background, foreground, and system jobs) can communicate with each other by using the Message Handler (MQ). The MQ handler performs like an ordinary RT-11 device handler in the way it accepts and dispatches I/O requests from the queued I/O system. This permits .READ and .WRITE requests to send messages between any two jobs as if they were data transfers to files. Both the sending and receiving job must issue a .LOOKUP request on a channel and use 'MQ' as the device specification and the logical job name of the job with which they are communicating as the file specification. In the case of .READ requests, the receiving buffer must be one word longer than the number of words expected. When the data transfer is completed, the first word of the buffer contains the number of words actually sent (identical to the .RCVD requests). This does not apply to the .WRITE requests; the first word of the sending buffer is the first word of the message to be sent. Note that the Message Handler (MQ) can also be used under the distributed FB monitor; it does not require the system job special feature.

Care should be taken when assigning logical job names to system jobs. Programmed requests such as .LOOKUP, .CHCOPY, and .GTJB must use the job's current logical job name (see the RT-11 System User's Guide).

1.1.3.10 Extended Memory Functions — The RT-11 extended memory (XM) monitor permits MACRO programs to access extended memory by mapping their virtual addresses to physical locations in memory. This is done in conjunction with a hardware option called the Memory Management Unit that converts a 16-bit virtual address to an 18- or 22-bit physical address.

You access extended memory in a program through programmed requests. In accessing extended memory, you must first establish window and region definition blocks. Next, you must specify the amount of physical memory the program requires and describe the virtual addresses you plan to use. Do this by creating regions and windows. Then, associate virtual addresses with physical locations by mapping the windows to the regions. You can remap a window to another region or part of a region, or you can eliminate a window or a region. Once the initial data structures are set up, you can manipulate the mapping of windows to regions that best meet your requirements.

There are four types of extended memory programmed requests:

1. Window requests 3. Map requests

2. Region requests 4. Status requests

The window and region requests have their own data structures. RT-11 provides the macro .WDBBK to create a window definition block and the macro .RDBBK to create a region definition block. Both macros automatically define offsets and bit names. Two other macros, .WDBDF and .RDBDF, define only the offsets and bit names.

The programmed request .CRAW is used to create a window. To eliminate a window, use the .ELAW request. A region is created using the .CRRG request. You return a region to the free list of memory with the .ELRG request.

You map a window to a region with the .MAP request. If a window is already mapped to a region, this window is unmapped and the new one is mapped. Use the .UNMAP request to unmap a window. You obtain the mapping status of a window with the .GMCX request.

Certain programmed requests are restricted when they are in an extended memory environment. These programmed requests and their restrictions are as follows:

.CDFN All channels must be in the lower 28K of memory (but not in the PAR1 region, 20000–37776 octal).

.QSET All queue elements must be 10(decimal) words long and in the lower 28K of memory (but not in the PAR1 region, 20000–37776 octal).

.SETTOP Effective only in the virtual address space that is mapped at the time the request is issued, unless the job was linked with the /V option (see the RT-11 System Utilities Manual).

.CNTXSW Not usable in virtual jobs.

Detailed information on programmed requests in an extended memory environment is given in the RT-11 Software Support Manual.

1.1.3.11 Interrupt Service Routines — The system macro library (SYSMAC.SML) contains some macros that are not programmed requests, but are used like programmed requests in interrupt service communication to the monitor. The first macro call in every interrupt routine is .INTEN, which causes the system to use the system stack for interrupt service and allows the monitor scheduler to make note of the interrupt. If device service is all the routine does, .INTEN is the only call it need make. If you need to issue one or more programmed requests, such as .READ or .WRITE from the interrupt service routine, you must issue the .SYNCH call. The .INTEN call described above switches execution to the system state, and since programmed requests can only be made in the user state, the .SYNCH call handles the switch back to the user state. The code following the .SYNCH call executes as a completion routine. When the .SYNCH is finished, the completion routine can execute programmed requests, initiate I/O, and resume the mainline code. The first word after the .SYNCH call is the return address on error, while the second word is the return on success. The RT-11 Software Support Manual contains a detailed description of interrupt service routines.

1.1.3.12 Device Handlers — The system macro library (SYSMAC.SML) contains several macros that simplify the writing of a device handler. A device handler is divided into several sections. These sections are as follows:

\- Preamble section
- Interrupt service section

\- Header section
- I/O completion section

\- I/O initiation section
- Termination section

The .DRDEF macro is used near the beginning of your device handler, and performs much of the work in the preamble section. The .DRBEG macro sets up the first five words in the header section, stores information in block 0 of the handler file, and creates some global symbols. The .DRAST macro sets up the interrupt entry point and the abort entry point in the interrupt service section, and lowers the processor priority. The .DRFIN macro generates the instructions for the jump back to the monitor at the end of the handler I/O completion routine. The .DREND macro generates handler termination code. The .DRBOT macro sets up the primary driver. A primary driver must be added to a standard handler for a data device to create a system device handler. The .DRINS macro sets up the install code area by generating the CSR words used by INSTALL and RESORC. The .DRSET macro sets up the option table for the SET command in block 0 of the device handler file. The .DRVTB macro sets up a table of vectors for devices that require more than one vector.

Each of the device handler macros is described in Chapter 2. The RT-11 Software Support Manual details the use of these macros in writing a device handler.

## 1.1.4 Compatibility With Previous RT-11 Versions

Programmed requests were implemented differently in each major release of RT-11. The following sections outline the changes that were made to the programmed requests from version to version.

1.1.4.1 Version 1 Programmed Requests — Programmed requests provided with the first release of RT-11, such as .READ and .WRITE, were designed for a single-user, single-job environment. As such, they differ significantly from the programmed requests of the later versions. For Version 1 requests, arguments were pushed on the stack instead of being stored, as they are presently, in an argument block. The channel number was limited to the range 0 through 17(octal), while later versions can allocate an additional number of channels. Also, no arguments could be omitted in the macro call.

Programs written for use under Version 1 assemble and execute properly under Versions 3, 4, and 5 when the ..V1.. macro call is used. The ..V1.. macro call causes all Version 1 programmed requests to expand exactly as they did in Version 1. The ..V2.. macro call expands all requests in Version 2 format. However, it is to your advantage to convert Version 1 and Version 2 programs to the current format for programmed requests (see Section 2.7). Future versions of RT-11 may no longer support the older formats.

1.1.4.2 Version 2 Programmed Requests — The release of RT-11 Version 2 included new programmed requests and a different way of handling arguments. The new programmed requests reflected RT-11's ability to run a foreground job as well as a background job. They included requests to suspend/resume the foreground job and to share messages and data between the two jobs.

Arguments in Version 2 programmed requests were stored in an argument block instead of on the stack. Another difference in Version 2 was that arguments could be omitted from macro calls. If the Area argument — that is, the pointer to the argument block — was omitted, the macro assumed that R0 pointed to a valid argument block. If any of the optional arguments were not present, the macro placed a zero in the argument block for the corresponding argument. Version 1 programmed requests were modified to incorporate these changes, and the ..V1.. macro was provided to allow Version 1 programmed requests to execute under Version 2 without further modification.

Programs written for use under Version 2 assemble and execute properly under Versions 3 and 4 when the ..V2.. macro call is used. The ..V2.. macro call causes all programmed requests prior to Version 3 to expand in Version 2 format.

1.1.4.3 Version 3 Programmed Requests — The programmed requests for Version 3 provide means for user programs to access regions in extended memory and to use more than one terminal. The chief difference between Version 2 and Version 3 programmed requests is the way in which omitted arguments are handled. In Versions 3, 4, and 5, blank arguments in the macro calls do not cause zeros to be entered into the argument block, but leave the corresponding argument block entry for the missing argument untouched.

This change can have a significant impact on user programs. If an argument block within a program is to be used many times for similar calls, you can save instructions by setting up the argument block entries only once (at assembly or run time), and leaving the corresponding fields blank in the macro call.

However, you should keep in mind that you may not substitute zeroes for missing fields. Programs written with this assumption operate incorrectly and exhibit a wide range of symptoms that can be hard to diagnose. Therefore, you must write the necessary instructions to fill the argument block if a programmed request is issued with fields left blank in the argument list.

Programmed requests from previous versions were modified to incorporate this change, and the ..V2.. macro call was provided so that Version 2 programs could execute properly under Version 3 without further modification.

1.1.4.4 Version 4 Programmed Requests — Certain programmed requests have taken on additional functions to support the system job feature. These programmed requests and their additional functions follow:

| Programmed Request | Added Function |
| --- | --- |
| .GTJB | Returns logical job name. |
| .CHCOPY | May specify logical job name. |
| .LOOKUP | Opens message channel to any job; issues .READ/C/W, .WRITE/C/W, and .WAIT requests to communicate between jobs. |

1.1.4.5 Version 5 Programmed Requests — Version 5 added several new programmed requests and modified others. The requests added for Version 5 are .ABTIO, .FPROT, .PEEK, .POKE, .PVAL, and .SFDAT. Although the XM monitor was expanded to support 22-bit Q-bus addressing, from a program's point of view the extended memory programmed requests are unchanged from Version 4. Channel number 377 is now reserved for system use and is always unavailable to user programs. The programmed requests which have changed between Version 4 and Version 5 are summarized below:

| Programmed Request | Added Function |
| --- | --- |
| .CSTAT | Available under SJ monitor. |
| .TWAIT | Available under SJ monitor. |
| .FETCH | Available under XM monitor. |
| .GTLIN | Optional argument to force terminal input. |

## 1.1.5 Programmed Request Conversion

The previous sections describe the modified format of programmed requests that were developed after those of Version 1. This section describes the conversion process from the Version 1 format to Version 3.

1.1.5.1 Macro Calls Not Requiring Conversion — Version 1 macro calls that do not require any conversion are as follows:

| .CSIGEN | .LOCK | .SRESET |
| --- | --- | --- |
| .CSISPC | .PRINT | .TTINR (Note 2) |
| .DATE | .QSET | .TTOUTR (Note 2) |
| .DSTATUS | .RCTRLLO | .TTYIN |
| .EXIT | .RELEAS | .TTYOUT |
| .FETCH | .SETTOP (Note 1) | .UNLOCK |
| .HRESET |  |  |

Note 1: Provided that location 50 is examined for the maximum value.

Note 2: Except in FB or XM systems.

1.1.5.2 Macro Calls That Can Be Converted — Version 1 macro calls that can be converted are as follows:

| .CLOSE | .RENAME |
| --- | --- |
| .DELETE | .REOPEN |
| .ENTER | .SAVESTATUS |
| .LOOKUP | .WAIT |
| .READ | .WRITE |

The general format of the ..V1.. system macro is

## .PRGREQ Chan,Arg1,...,Argn

In this form, Chan is an integer between 0 and 17(octal) and is not a general assembler argument. The channel number is assembled into the EMT instruction itself. The arguments Arg1 through Argn are either moved into R0 or pushed on the stack.

The ..V2.. equivalent of the above call is

    .PRGREQ Area,Chan,Arg1,...,Argn

In this form, the Chan argument can be any legal assembler argument and can be in the range from 0 to 377(octal). Area points to an argument block where the arguments Arg1 through Argn will be placed.

For example, consider a .READ programmed request in both forms:

```asm
Version 1:      .READ 5 ,#BUFF ,#256 ,,BLOCK
Version 2:      .READ #AREA ,#5 ,#BUFF ,#256 ,,BLOCK
        .
        .
        .
AREA:      .WORD 0 ;CHANNEL/FUNCTION CODE HERE
        .WORD 0 ;BLOCK NUMBER HERE
        .WORD 0 ;BUFFER ADDRESS HERE
        .WORD 0 ;WORD COUNT HERE
        .WORD 0 ;A 1 GOES HERE
```

Thus, the difference in the two macro calls is that Version 2 declares the channel number as a legal assembler argument and adds an Area argument.

Table 1–3 shows a complete list of conversions for the programmed requests that can be converted. Version 1 and Version 2 formats are given. In Versions 3 and later, this function is performed automatically. The arguments shown inside the square brackets ([ ]) are optional. Refer to the appropriate section in Chapter 2 for more details on each request.

Table 1-3: Programmed Request Conversions (Version 1 to Version 2)

| Version | Programmed Request |
| --- | --- |
| V1: | .DELETE chan,dblk |
| V2: | .DELETE area,chan,dblk[,count] |
| V1: | .LOOKUP chan,dblk |
| V2: | .LOOKUP area,chan,dblk[,count] |
| V1: | .ENTER chan,dblk[,length] |
| V2: | .ENTER area,chan,dblk[,length[,count]] |
| V1: | .RENAME chan,dblk |
| V2: | .RENAME area,chan,dblk |
| V1: | .SAVESTAT chan,cblk |
| V2: | .SAVESTAT area,chan,cblk |
| V1: | .REOPEN chan,cblk |
| V2: | .REOPEN area,chan,cblk |
| V1: | .CLOSE chan |
| V2: | .CLOSE chan |
| V1: | .READ/.READW chan,buff,wcnt,blk |
| V2: | .READ/.READW area,chan,buff,wcnt,blk |
| V1: | .READC chan,buff,wcnt,crtn,blk |
| V2: | .READC area,chan,buff,wcnt,crtn,blk |
| V1: | .WRITE/.WRITW chan,buff,wcnt,blk |
| V2: | .WRITE/.WRITW area,chan,buff,wcnt,blk |
| V1: | .WRITC chan,buff,wcnt,crtn,blk |
| V2: | .WRITC area,chan,buff,wcnt,crtn,blk |
| V1: | .WAIT chan |
| V2: | .WAIT chan |

Several important features of Version 3 calls to be kept in mind when using them are as follows:

1. Version 3 calls require the area argument, which points to the area where the other arguments will be (unless R0 already points to it and the first word is set up).

2. Enough memory space must be allocated to hold all the required arguments.

3. The chan argument must be a legal assembler argument, not just an integer between 0 and 17(octal).

4. Blank fields are permitted in the Version 3 calls. Any field not specified (left blank) is not modified in the argument block.

## 1.1.6 Programmed Request Summary

Many programmed requests operate only in a specific RT-11 environment, such as under a foreground/background monitor or when using a special feature such as multiterminal operation. Table 1–4 lists the programmed requests that can be used in all RT-11 environments, including multiterminal operation. Table 1–5 lists the additional programmed requests that can be used under the foreground/background monitor and extended memory monitor. The EMT and function code for each request are shown in octal. Although only the first six characters of the programmed request are significant to the Macro assembler, the longer forms are shown to provide a better understanding of the request function. Also, the purpose of each request is described.

Macros that are used in interrupt service routines and in writing device handlers are listed since they are a part of the system macro library.

Table 1–4 summarizes the programmed requests that work in all RT-11 environments. The programmed requests followed by (MT) work only under the multiterminal feature of RT-11.

Table 1-4: Programmed Requests for All RT-11 Environments

| Name | EMT | Code | Purpose |
| --- | --- | --- | --- |
| .ABTIO | 374 | 13 | Aborts I/O in progress on the specified channel |
| .ADDR | — | — | Computes a specified address in a position-independent manner |
| .ASSUME | — | — | Tests for a specified condition; if test is false, generates assembly error and prints descriptive message |
| .BR | — | — | Warns if code which belongs together is separated during assembly |
| .CDFN | 375 | 15 | Defines additional channels for I/O |
| .CHAIN | 374 | 10 | Chains to another program (in background job only) |
| .CLOSE | 374 | 6 | Closes the specified channel |
| .CMKT | 375 | 23 | Cancels an unexpired mark time request (special feature in single-job environment) |
| .CSIGEN | 344 | — | Calls the Command String Interpreter (CSI) in general mode |
| .CSISPC | 345 | — | Calls the Command String Interpreter (CSI) in the special mode |
| .CSTAT | 375 | 27 | Returns the status of the specified channel |
| .CTIMIO | — | — | Used within a device handler as a macro call to cancel a mark time request (special feature) |
| .DATE | 374 | 12 | Moves the current date information into R0 |
| .DELETE | 375 | 0 | Deletes the file from the specified device |
| .DRAST | — | — | Used with device handlers to create the asynchronous entry points to the handler |
| .DRBEG | — | — | Used with device handlers to create a five-word header, and .ASECT locations 52 through 60 |
| .DRBOT | — | — | Used with system device handlers to set up the primary driver |
| .DRDEF | — | — | Used with device handlers to set up handler parameters, call driver macros from the library, and define useful symbols |
| .DREND | — | — | Used with device handlers to generate the table of pointers into the resident monitor |
| .DRFIN | — | — | Used with device handlers to generate the code required to exit to the completion code in the resident monitor |
| .DRINS | — | — | Sets up installation code area in block 0 of a device handler, and defines system and data device installation entry points |
| .DRSET | — | — | Used with device handlers to create the list of SET options for a device |
| .DRVTB | — | — | Used with multivector device handlers to generate a table that contains the vector location, interrupt entry point, and processor status word for each device vector |
| .DSTATUS | 342 | — | Returns the status of a particular device |
| .ENTER | 375 | 2 | Creates a new file for output |
| .EXIT | 350 | — | Exits the user program and optionally passes a command to KMON |
| .FETCH | 343 | — | Loads a device handler into memory |
| .FORK | — | — | Generates a subroutine call in an interrupt service routine that permits long but not critical processing to be postponed until all other interrupts are dismissed |
| .FPROT | 375 | 43 | Sets or removes a file's protection |
| .GTIM | 375 | 21 | Gets the time of day |
| .GTJB | 375 | 20 | Gets parameters of a job |
| .GTLIN | 345 | — | Accepts an input line from either an indirect command file or the console terminal |
| .GVAL | 375 | 34 | Returns contents of a monitor fixed offset |
| .HERR | 374 | 5 | Specifies termination of a job on fatal errors |
| .HRESET | 357 | — | Terminates I/O transfers and does a .SRESET operation |
| .INTEN | — | — | Generates a subroutine call to notify the monitor that an interrupt has occurred, requests system state, and sets processor priority to the specified value |
| .LOCK | 346 | — | Makes the monitor User Service Routine (USR) permanently resident until an .EXIT or .UN-LOCK is executed; the user program is swapped out, if necessary |
| .LOOKUP | 375 | 1 | Opens an existing file for input and/or output via the specified channel; opens a message channel to a specified job |
| .MFPS | — | — | Reads the priority bits in the processor status word, but does not read the condition codes |
| .MRKT | 375 | 22 | Marks time, that is, sets an asynchronous routine to be entered after specified interval (special feature in single-job environment) |
| .MTATCH (MT) | 375 | 37 | Attaches a terminal for exclusive use by the requesting job |
| .MTDTCH (MT) | 375 | 37 | Detaches a terminal from one job and frees it for use by other jobs |
| .MTGET (MT) | 375 | 37 | Returns the status of a specified terminal to the user |
| .MTIN (MT) | 375 | 37 | Operates as a .TTYIN request for a multiterminal configuration |
| .MTOUT (MT) | 375 | 37 | Operates as a .TTYOUT request for a multiterminal configuration |
| .MTPRNT (MT) | 375 | 37 | Operates as a .PRINT request for a multiterminal configuration |
| .MTPS | — | — | Sets the priority bits, condition codes, and T-bit in the processor status word |
| .MTRCTO (MT) | 375 | 37 | Resets the CTRL/O flag for the designated terminal |
| .MTSET (MT) | 375 | 37 | Modifies terminal status in a multiterminal configuration |
| .MTSTAT (MT) | 375 | 37 | Provides multiterminal system status |
| .PEEK | 375 | 34 | Examines memory locations |
| .POKE | 375 | 34 | Changes memory locations |
| .PRINT | 351 | — | Outputs an ASCII string terminated by a zero byte or a 200 byte |
| .PURGE | 374 | 3 | Clears out a channel for reuse |
| .PVAL | 375 | 34 | Replaces contents of a monitor fixed offset |
| .QELDF |  |  | Used with device handlers to define offsets in the I/O queue element |
| .QSET | 353 | — | Increases the size of the monitor I/O queue |
| .RCTRLO | 355 | — | Enables output to the terminal, overriding any previous CTRL/O |
| .READ | 375 | 10 | Transfers data on the specified channel to a memory buffer and returns control to the user program when the transfer request is entered in the I/O queue; no special action is taken upon completion of I/O |
| .READC | 375 | 10 | Transfers data on the specified channel to a memory buffer and returns control to the user program when the transfer request is entered in the I/O queue; upon completion of the read, control transfers asynchronously to the completion routine specified in the .READC request |
| .READW | 375 | 10 | Transfers data via the specified channel to a memory buffer and returns control to the user program only after the transfer is complete |
| .RELEASE | 343 | — | Removes a device handler from memory |
| .RENAME | 375 | 4 | Changes the name of the indicated file to a new name; if this request is attempted when using magtape, the handler returns an invalid operation code |
| .REOPEN | 375 | 6 | Restores the parameters stored via a .SAVE-STATUS request and reopens the channel for I/O |
| .SAVESTATUS | 375 | 5 | Saves the status parameters of an open file in user memory and frees the channel for use |
| .SCCA | 375 | 35 | Enables intercept of CTRL/C commands |

(continued on next page)

Table 1-4: Programmed Requests for All RT-11 Environments (Cont.)

| Name | EMT | Code | Purpose |
| --- | --- | --- | --- |
| .SDTTM | 375 | 40 | Sets the system date and/or time |
| .SERR | 374 | 4 | Inhibits most fatal errors from aborting the current job |
| .SETTOP | 354 | — | Specifies the highest memory location to be used by the user program |
| .SFDAT | 375 | 42 | Changes a file creation date in a directory entry |
| .SFPA | 375 | 30 | Sets user interrupt for floating-point processor exceptions |
| SOB | — | — | Simulates the SOB instruction |
| .SPFUN | 375 | 32 | Performs special functions on magtape, cassette, diskette, and some disk devices |
| .SRESET | 352 | — | Resets all channels and releases the device handlers from memory |
| .SYNCH | — | — | Generates a subroutine call that enables your program to perform programmed requests from within an interrupt service routine |
| .TIMIO | — | — | Generates a subroutine call in a handler to schedule a mark time request (special feature in all environments) |
| .TLOCK | 374 | 7 | Indicates if the USR is currently used by another job and performs exactly as a .LOCK request in a single-job environment |
| .TRPSET | 375 | 3 | Sets a user intercept for traps to monitor locations 4 and 10 |
| .TTINR.TTYIN | 340 | — | Reads one character from the keyboard buffer |
| .TTYOUT.TTOUTR | 341 | — | Transfers one character to the terminal input buffer |
| .TWAIT | 375 | 24 | Suspends the running job for a specified amount of time |
| .UNLOCK | 347 | — | Releases the USR after execution of a .LOCK and swaps in the user program, if required |
| ..V1.. | — | — | Provides compatibility with Version 1 format |
| ..V2.. | — | — | Provides compatibility with Version 2 format |
| .WAIT | 374 | 0 | Waits for completion of all I/O on a specified channel |
| .WRITC | 375 | 11 | Transfers data on the specified channel to a device and returns control to the user program when the transfer request is entered in the I/O queue; upon completion of the write, control transfers asynchronously to the completion routine specified in the .WRITC request |

(continued on next page)

Table 1-4: Programmed Requests for All RT-11 Environments (Cont.)

| Name | EMT | Code | Purpose |
| --- | --- | --- | --- |
| .WRITE | 375 | 11 | Transfers data on the specified channel to a device and returns control to the user program when the transfer request is entered in the I/O queue; no special action is taken upon completion of the I/O |
| .WRITW | 375 | 11 | Transfers data on the specified channel to a device and returns control to the user program only after the transfer is complete |

Table 1–5 lists the additional programmed requests that can be used only in a foreground/background and extended memory environment. The programmed requests followed by (XM) operate only in an extended memory environment.

Table 1-5: Foreground/Background and Extended Memory Programmed Requests

<table><tr><td>Name</td><td>EMT</td><td>Code</td><td>Purpose</td></tr><tr><td>.CHCOPY</td><td>375</td><td>13</td><td>Allows one job to access another job&#x27;s channel</td></tr><tr><td>.CNTXSW</td><td>375</td><td>33</td><td>Requests that the indicated memory locations be part of FB or XM context switch process</td></tr><tr><td>.CRAW (XM)</td><td>375</td><td>36</td><td>Creates a window in virtual memory</td></tr><tr><td>.CRRG (XM)</td><td>375</td><td>36</td><td>Creates a region in extended memory</td></tr><tr><td>DEVICE</td><td>375</td><td>14</td><td>Allows device interrupts in FB or XM to be disabled upon program termination</td></tr><tr><td>.ELAW (XM)</td><td>375</td><td>36</td><td>Eliminates an address window in virtual memory</td></tr><tr><td>.ELRG (XM)</td><td>375</td><td>36</td><td>Eliminates an allocated region in extended memory</td></tr><tr><td>.GMCX (XM)</td><td>375</td><td>36</td><td>Returns mapping status of a specified window</td></tr><tr><td>.MAP (XM)</td><td>375</td><td>36</td><td>Maps a virtual address window to extended memory</td></tr><tr><td>.MWAIT</td><td>374</td><td>11</td><td>Waits for messages to be processed</td></tr><tr><td>.PROTECT</td><td>375</td><td>31</td><td>Requests that specified vectors in the area from 0 to 476 be given exclusively to the current job</td></tr><tr><td>.RCVD</td><td rowspan="3">375</td><td rowspan="3">26</td><td rowspan="3">Receives data — allows a job to read messages or data sent by another job in an FB environment. The three modes correspond to the .READ, .READC, and .READW requests</td></tr><tr><td>.RCVDC</td></tr><tr><td>.RCVDW</td></tr><tr><td>.RDBBK (XM)</td><td>—</td><td>—</td><td>Reserves space in a program for a region definition block and sets up the region size and region status word</td></tr><tr><td>.RDBDF (XM)</td><td>—</td><td>—</td><td>Defines the offsets and bit names associated with a region definition block</td></tr></table>

(continued on next page)

Table 1-5: Foreground/Background and Extended Memory Programmed Requests (Cont.)

<table><tr><td>Name</td><td>EMT</td><td>Code</td><td>Purpose</td></tr><tr><td>.RSUM</td><td>374</td><td>2</td><td>Causes the mainline code of the job to be resumed after it was suspended by a .SPND request</td></tr><tr><td>.SDAT</td><td rowspan="3">375</td><td rowspan="3">25</td><td rowspan="3">Sends messages or data to the other job in an FB environment. The three modes correspond to the .WRITE, .WRITC, and .WRITW requests</td></tr><tr><td>.SDATC</td></tr><tr><td>.SDATW</td></tr><tr><td>.SPCPS</td><td>375</td><td>41</td><td>Used in a completion routine to change the flow of control of the mainline code (special feature)</td></tr><tr><td>.SPND</td><td>374</td><td>1</td><td>Causes the running job to be suspended</td></tr><tr><td>.UNMAP (XM)</td><td>375</td><td>36</td><td>Unmaps a virtual address memory window</td></tr><tr><td>.UNPROTECT</td><td>375</td><td>31</td><td>Cancels the .PROTECT vector protection request</td></tr><tr><td>.WDBBK (XM)</td><td>—</td><td>—</td><td>Reserves space in a program for a window definition block and sets up the associated data</td></tr><tr><td>.WDBDF (XM)</td><td>—</td><td>—</td><td>Defines the offsets and bit names associated with a window definition block</td></tr></table>
