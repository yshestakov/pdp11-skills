# RT-11 PRM reference: Ch.1.2 SYSLIB (FORTRAN-callable library): conventions, calling, FORTRAN/MACRO interface, F/B FORTRAN, linking with FORLIB, services, character-string functions, subroutine summary table

Source: RT-11 Programmer's Reference Manual AA-H378C-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' sometimes reads as ',' (`,MCALL` = `.MCALL`), 'R0' as 'RO', '#' as '\*' or '*'. Verify exact macro expansions against `sysmac_v53.mac`.

Contents:
- 1.2 Using the System Subroutine Library
- 1.2.1 System Conventions
- 1.2.2 Calling SYSLIB Subroutines
- 1.2.3 FORTRAN/MACRO Interface
- 1.2.4 FORTRAN Programs in a Foreground/Background Environment
- 1.2.5 Linking with FORLIB
- 1.2.6 SYSLIB Services Not Provided by Programmed Requests
- 1.2.7 Character String Functions
- 1.2.8 System Subroutine Summary

---

## 1.2 Using the System Subroutine Library

The system subroutine library is a collection of FORTRAN-callable routines that allow various RT-11 system features to be used by a FORTRAN programmer. There are no FORTRAN routines in SYSLIB to access extended memory under the extended memory (XM) monitor.

This collection of subroutines is placed in a system library called SYS-LIB.OBJ. This library file also contains the overlay handlers, utility functions, a character string manipulation package, and two-word integer support routines. The linker uses this library to resolve undefined globals. It is resident on the system device (SY:).

You should be familiar with the PDP-11 FORTRAN Language Reference Manual and the RT-11/RSTS/E FORTRAN IV User's Guide before using the material in this chapter.

The system subroutine library provides the following capabilities:

1. Complete RT-11 I/O facilities, including synchronous, asynchronous, and event-driven modes of operation. FORTRAN subroutines can be activated upon completion of an input/output operation.

2. Timed scheduling of completion routines. This feature is standard in the FB and XM monitors, and is a special feature in the SJ monitor.

3. Facilities for communication between foreground and background jobs.

4. FORTRAN language interrupt service routines for user devices.

5. Complete timer support facilities, including timed suspension of execution in a FB or XM environment, conversion of different time formats, and time-of-day information. The timer support facilities can use either 50- or 60-cycle clocks.

6. All RT-11 auxiliary input/output functions, including the capabilities of opening, closing, renaming, and creating or deleting files on any device.

7. All monitor-level information functions, such as job partition parameters, device statistics, and input/output channel statistics.

8. Access to the RT-11 command string interpreter (CSI).

9. A character string manipulation package supporting variable-length character strings.

10. INTEGER\*4 support routines that allow two-word integer computations.

## NOTE

When variables are described or mentioned, and unless otherwise specified, INTEGER means INTEGER\*2, (16-bit integer) and REAL means REAL\*4 (single-precision floating point). Integer and real arguments to subprograms are indicated in this section as follows:

i = INTEGER\*2 arguments

j = INTEGER\*4 arguments

a = REAL\*4 arguments

$\mathrm{d} = \mathrm{REAL}^{*}8$ arguments

In general, the routines in SYSLIB were written for use with RT-11 V2 or later and FORTRAN IV V1B or later versions. The use of SYSLIB with prior versions of RT-11 or FORTRAN may lead to unpredictable results.

## 1.2.1 System Conventions

This section describes system conventions that must be followed for proper operation of calls to the system subroutine library. Certain restrictions that apply are described in Section 1.2.1.7.

1.2.1.1 Channel Numbers — A channel number is a logical identifier for a file used by FORTRAN. Thus, when you open a file on a particular device, you assign a channel number to that file. To refer to an open file, it is only necessary to refer to the appropriate channel number.

The FORTRAN system has 16(decimal) channels available for your use. The call IGETC assigns a channel to your program and notifies the FORTRAN I/O system, which also uses these channels, that the channel is in use. When there is no longer need for a channel, the program should close the channel with a CLOSEC, ICLOSE or a PURGE SYSLIB call. The channel should also be freed and returned to the FORTRAN I/O system with a IFREEC call.

Up to 254(decimal) channels can be activated with the ICDFN call. This function sets aside memory in the job area to accommodate status information for the extra channels. Use the ICDFN call during the initialization phase of your program. You can use all channels numbered higher than 15(decimal). The FORTRAN I/O system uses channels 0 through 15(decimal).

Channels must be allocated in the main program routine or its subprograms. Do not allocate channels in routines that are activated as the result of I/O completion events or ISCHED or ITIMER calls.

1.2.1.2 Completion Routines — Completion routines can be written in FORTRAN or assembly language, depending upon the function called.

A completion routine is a subprogram that executes asynchronously with a main program and is scheduled to run as soon as possible after the completion of an associated event, such as an I/O transfer or the passing of a specified time interval. All completion routines of the current job have higher priority than other parts of the job. Therefore, once a completion routine becomes runnable because of its associated event, it interrupts execution of the job and continues to execute until it relinquishes control.

Completion routines are handled differently in the SJ and the FB and XM monitors. In the SJ monitor, these routines are totally asynchronous and can interrupt one another. Unlike completion routines run under FB and XM monitors, which are serialized and run at priority 0, completion routines run under an SJ monitor are nested and can interrupt each other. In addition, they execute not at priority 0, but at the same priority as the device whose interrupt scheduled them. For example, the completion routine resulting from a .WRITC programmed request to device TT: runs at priority 4. Completion routines from timer requests run at the same priority as the system clock. This is particularly important on LSI-11 and PDP/03 systems that have only two interrupt levels, ON and OFF, because clock interrupts may be lost while lengthy completion routines execute. In the FB and XM monitors, completion routines do not interrupt each other but are queued and have to wait until the correct job is running. They are then scheduled on a first-in first-out basis.

Assembly language completion routines exit with an RTS PC instruction. FORTRAN completion routines exit by the execution of a RETURN or END statement in the subroutine. All names of completion routines external to the routine being coded that are passed to scheduling calls must be specified in an EXTERNAL statement in the FORTRAN program unit issuing the call.

A completion routine written in FORTRAN can have a maximum of two arguments as follows:

Form: SUBROUTINE crtn [(iarg1,iarg2)]

where:

crtn is the name of the completion routine iarg1 is equivalent to R0 on entry to an assembly language completion routine

iarg2 is equivalent to R1 on entry to an assembly language completion routine

If an error occurs in a completion routine or in a subroutine at completion level, the error handler traces back through to the original interruption of the main program. Thus, the traceback is shown as though the completion routine were called from the main program. This lets you know where the main program was executing, so that when an error is fatal, it can be diagnosed and corrected.

Certain restrictions apply to completion routines that are activated by the following calls:

| INTSET | IREADF | ISPFNC | IWRITC |
| --- | --- | --- | --- |
| IRCVDC | ISCHED | ISPFNF | IWRITF |
| IRCVDF | ISDATC | ITIMER | MRKT |
| IREADC | ISDATF |  |  |

The restrictions that apply when using these calls are as follows:

\- No channels can be allocated by calls to IGETC or freed by calls to IFREEC from a completion routine. Channels to be used by completion routines should be allocated and placed in a COMMON block for use by the routine.

\- The completion routine cannot perform any call that requires the use of the USR, such as LOOKUP and IENTER. See Section 1.2.1.5 for a list of the SYSLIB functions that call the USR.

\- Files that are used by the completion routine must be opened and closed by the main program. There are, however, no restrictions on the input or output operations that can be performed in the completion routine. If many files must be made available to the completion routine, they can be opened by the main program and saved for later use (without tying up RT-11 channels) by an ISAVES call. The completion routine can later make them available by reattaching the file to a channel with an IRE-OPN call.

Even if the completion routine itself does not issue any programmed requests, but does perform I/O to a logical unit number through the OTS, that logical unit number must be opened from the main level. To accomplish this, either the first I/O access or an OPEN statement must be issued from main level. A completion routine may not call CLOSE to close a logical unit.

\- FORTRAN subroutines are reusable but not reentrant. That is, a given subroutine can be used many times as a completion routine or as a routine in the main program, but a subroutine executing as main program code does not work properly if it is interrupted and then called again at the completion level. This restriction applies to all subroutines that can be invoked at the completion level while they are active in the main program.

\- FORTRAN completion routines can be called only by SYSLIB functions that end in F. Conversely, MACRO completion routines cannot be called by SYSLIB functions that end in F. Refer to Section 1.1.3.5 for details of other restrictions on MACRO completion routines.

\- Under the SJ monitor, only one completion function should be active at any time.

1.2.1.3 Device Blocks — A device block is a four-word block of Radix-50 information that specifies a physical device and a file name. In FORTRAN, you can use one of three different methods to set up this block as follows:

1. You can use the DIMENSION and DATA statements. For example,

```csv
DIMENSION IFILE (4)
DATA IFILE/3RSY ,3RFIL,3RE ,3RXYZ/
```

2. You can translate the available ASCII file description string into Radix-50 format, using the SYSLIB calls IRAD50, R50ASC, and RAD50. For example,

```csv
REAL*8 FSPEC
CALL IRAD50 (12,'SY FILE XYZ',FSPEC)
```

3. You can use the SYSLIB call ICSI to call the Command String Interpreter (CSI) to accept and parse standard RT-11 command strings.

1.2.1.4 INTEGER\*4 Support Functions — This section discusses the initialization of INTEGER\*4 variables for the FORTRAN programmer. Section 1.2.6.3 describes the use of INTEGER\*4 functions for use by the MACRO programmer.

When the DATA statement is used to initialize INTEGER\*4 variables, it must specify both the low- and high-order parts. For example, the code

```txt
INTEGER*4 J
DATA J/3/
```

Initializes only the first word. The correct way to initialize an INTEGER\*4 variable to a constant such as 3 is as follows:

```txt
INTEGER*4 J
INTEGER*2 I(2)
EQUIVALENCE (J,I)
DATA I/3,0/      !INITIALIZE J TO 3
```

If you are initializing an INTEGER\*4 variable to a negative value such as -4, the high-order (second word) part must be the continuation of the two's complement of the low-order part. For example,

```csv
INTEGER*4 J
INTEGER*2 I(2)
EQUIVALENCE (J,I)
DATA I/-4,-1/ !INITIALIZE J TO -4
```

The following example is suitable for initializing INTEGER\*4 arguments to subprograms:

```txt
INTEGER*2 J(2)
DATA J/3,0/      !LOW ORDER,HIGH ORDER
```

1.2.1.5 User Service Routine (USR) Requirements — User-written routines that interface to the FORTRAN Object Time System (OTS) must account for the location of the RT-11 User Service Routine (USR). The USR occupies 2K words. When your program calls a SYSLIB routine that requests a USR function (such as IENTER or LOOKUP), or when the USR is invoked by the FORTRAN OTS, the USR is swapped into memory if it is nonresident. The FORTRAN OTS is designed so that the USR can swap over it.

If you permit the USR to swap over certain kinds of data and code, you will obtain unpredictable results. In particular, you should restrict interrupt service routines and completion routines to locations outside the USR swapping area. To find the limits of this swapping area, examine the link map and, if necessary, change the order of object modules and libraries as specified to the Linker.

Subroutines that require the USR are as follows:

CLOSEC,ICLOSE
GETSTR (only if first I/O operation on logical unit)
ICDFN (single job only)
GTLIN
ICSI
IDELET
IDSTAT
IENTER
IFETCH
IQSET
IRENAM
ITLOCK (only if USR is not in use by another job)
LOCK (only if USR is in a swapping state)
LOOKUP
PUTSTR (only if first I/O operation on logical unit)

CONTROLLING USR SWAPPING

You can control USR swapping by using the KMON commands SET USR NOSWAP and SET USR SWAP. The SET USR NOSWAP command prevents swapping and freezes the USR in memory. The command SET USR SWAP reverses this, allowing the USR to swap under program control.

Alternatively, you can compile your FORTRAN main program with the /NOSWAP option if you are sure that there is space just below the foreground partition or RMON to make the USR permanent for the duration of your program. Use this option if your program does not need the 2K words of memory that the USR occupies. If the /NOSWAP option is not specified, the USR swaps over the 2K words of your program above the base address — that is, from location 1000(octal) to 11000(octal), which is the part of a FORTRAN program least likely to violate the USR restrictions.

To prevent USR swapping for part of the program execution time and allow the USR to swap out at other times, use the LOCK, UNLOCK, and ITLOCK calls.

The LOCK call locks the USR into main memory and attaches it to the requesting job. The UNLOCK call allows the USR to swap again and to be used by another job. The ITLOCK call is used to determine whether another job is already using the USR. If so, the ITLOCK call returns immediately with an error code. This allows the program to try for a lock, but to continue with other action if it fails. The LOCK and UNLOCK calls are used in a foreground program to prevent interference from the background during initialization and completion phases and to minimize the number of swaps.

## STRATEGIES IN USR SWAPPING

If you decide to change the position of code or data to avoid the USR swapping area, or if you want to move the USR itself, you must consider the concept of PSECT (program section) ordering.

PSECTs contain code and data and are identified by names as segments of the object program. The attributes associated with each PSECT direct the Linker to combine several separately compiled FORTRAN program units, assembly language modules, and library routines into an executable program.

The order in which program sections are allocated in the executable program is the order that they are presented to the Linker. Applications that are sensitive to this ordering typically separate those sections containing read-only information (such as executable code and pure data) from impure sections containing variables.

The main program unit of a FORTRAN program (normally the first object module in sequence presented to LINK) declares PSECT ordering as shown in Table 1–6.

The USR can swap over pure code, but must not be loaded over constants or impure data that can be used as arguments to the USR. The ordering shown in Table 1–6 collects all pure sections before impure data in memory. The USR can safely swap over sections OTS\$I, OTS\$P, SYS\$I, USER\$I, and \$CODE. When a FORTRAN program is running, the USR will normally swap starting at the base of section OTS\$I. Location 46 of the System Communication Area contains the address where the USR will swap. If location 46 is zero, the USR will swap at its default location, below RMON and any handlers.

See the RT-11/RSTS/E FORTRAN IV User's Guide for more information on program sections. The RT-11 Software Support Manual also contains information on USR swapping and PSECT ordering.

Table 1-6: FORTRAN Program PSECT Ordering

| Section Name | Attributes |
| --- | --- |
| OTS$I | RW,I,LCL,REL,CON |
| OTS$P | RW,D,GBL,REL,OVR |
| SYS$I | RW,I,LCL,REL,CON |
| USER$I | RW,I,LCL,REL,CON |
| $CODE | RW,I,LCL,REL,CON |
| OTS$O | RW,I,LCL,REL,CON |
| SYS$O | RW,I,LCL,REL,CON |
| $DATAP | RW,D,LCL,REL,CON |
| OTS$D | RW,D,LCL,REL,CON |
| OTS$S | RW,D,LCL,REL,CON |
| SYS$S | RW,D,LCL,REL,CON |
| $DATA | RW,D,LCL,REL,CON |
| USER$D | RW,D,LCL,REL,CON |
| .$$$$$. | RW,D,GBL,REL,OVR |
| Other COMMON Blocks | RW,D,GBL,REL,OVR |

USR LOCKOUT AND TIMING

If one job is using the USR and another job requests it, the second job will become blocked until the first job releases the USR. The second job may be locked out for seconds or minutes at a time. Interrupt service and completion routines can run, but not the mainline code. The timing problems that arise as a result can be eliminated, or minimized, in one of the following four ways:

1. Do not use devices with slow directory operations, such as cassettes and magtapes.

2. Code real-time operations as completion and interrupt service routines in your foreground job so that a locked out mainline program does not impact real-time operations.

3. Separate USR and real-time operations.

4. Use the ITLOCK call and avoid SYSLIB calls that request the USR while the USR is owned by another job.

Typically, a real-time foreground job can be constructed of (1) an initialization phase that opens all required channels and begins a real-time operation, (2) a real-time phase that performs interrupt service and I/O operations, and (3) a completion phase that halts real-time activity and then closes the channels. Maintaining this structure in the foreground allows the background task to do USR operations during the real-time phase without locking out the foreground. This also simplifies USR swapping since the USR can swap over the interrupt routines and I/O buffers as long as they are inactive.

1.2.1.6 Subroutines Requiring Additional Queue Elements — Certain sub-routines require queue elements for their proper operation. These sub-routines are as follows:

## IRCVD/IRCVDC/IRCVDF/IRCVDW IREAD/IREADC/IREADF/IREADW ISCHED ISDAT/ISDATC/ISDATF/ISDATW ISLEEP ISPFN/ISPFNC/ISPFNF/ISPFNW ITIMER ITWAIT IUNTIL IWRITC/IWRITE/IWRITF/IWRITW MRKT MWAIT

One queue element per job is automatically allocated. Issuing more than one request from the list requires extra queue elements. Additional queue elements can be allocated through a call to the IQSET function.

1.2.1.7 System Restriction — The following restrictions must be considered when coding a FORTRAN program that uses SYSLIB.

1. Programs using IPEEK, IPOKE, IPEEKB, IPOKEB, or ISPY to access system-specific addresses, such as FORTRAN, monitor, or hardware addresses, are not guaranteed to run under future releases or on different configurations. When using these functions, you should document their use precisely so that you can check your references against the current documentation. Also, these routines may act differently under the XM monitor. NOTE: IPEEK and IPOKE are not equivalent to the programmed requests .PEEK and .POKE.

2. Various functions in SYSLIB return values that are of type integer, real, and double precision. If you specify an implicit statement that changes the defaults for external function types, you must explicitly declare the type of those SYSLIB functions that return integer or real results. You must also be sure that the arguments to the SYSLIB routines are the correct type for the routine. Double-precision functions must always be declared to be type DOUBLE PRECISION (or REAL\*8). Failure to observe this restriction leads to unpredictable results.

3. All names of completion routines external to the routine being coded that are passed to scheduling calls (such as ISCHED, ITIMER, and IREADC) must be specified in an EXTERNAL statement in the FORTRAN program issuing the call.

4. Certain arguments to SYSLIB calls must be located in such a manner as to prohibit the RT-11 User Service Routine (USR) from swapping over them at execution time. This kind of swapping can occur when the OTS\$I section (which contains the all-pure code and data for the module) is less than 2K words in length. Swapping in this uncommon situation can be avoided either by typing the SET USR NOSWAP command to make the USR resident before starting the job, or by compiling the mainline routine with a /NOSWAP option. You can also use the linker /BOUNDARY option to make OTS\$O start at word boundary 11000(oc-tal). (This problem generally occurs only with small FORTRAN programs.)

In FORTRAN IV, program sections (PSECTs) are used to collect code and data into appropriate areas of memory. If the RT-11 USR is needed and is not resident, it swaps over a FORTRAN program starting at the symbol OTS\$I for 2K words of memory.

5. Certain restrictions apply when using completion or interrupt routines. See Section 1.2.1.2 for a description of these restrictions.

6. Unless explicitly stated, null arguments should not be used in calls to SYSLIB routines.

7. If several arguments to a call are listed as being optional, they must either be all present or all omitted.

## 1.2.2 Calling SYSLIB Subroutines

SYSLIB includes both function subprograms and callable subroutines, which are called in the same manner as user-written subroutines.

Function subprograms receive control by means of a function reference as follows:

i = function name ([arguments])

The returned function value may be an error code, or it may be information that is useful to the calling routine. See the description of the particular function for the meaning of the returned function value.

Call subroutines are invoked by means of a CALL statement as follows:

CALL subroutine name [(arguments)]

All subroutines in SYSLIB can be called as FUNCTION programs if a return value is desired, or as SUBROUTINE programs if no return value is desired. For example, the LOCK subroutine can be referenced as either

CALL LOCK

or

I = LOCK()

Some subroutines have two acceptable formats. For example, the subroutine CLOSEC can also be specified as ICLOSE because error codes are returned by the subroutine and require an integer return to be useful.

Quoted-string literals are useful as arguments of calls to routines in SYS-LIB, notably the character string routines. These literals are allowed in subroutine and function calls (see Section 1.2.7.3).

## 1.2.3 FORTRAN/MACRO Interface

FORTRAN calling routines and subroutines follow a well-defined set of conventions regarding transfer of control, transfer of information, memory usage, and register usage. By adhering to these conventions a MACRO programmer can write FORTRAN-callable routines such as those in SYS-LIB.

Control is transferred to a subroutine by

JSR PC, SUBR

When control passes to the subroutine SUBR, Register 5 (R5) points to an argument block that has the format shown in Figure 1–5.

Figure 1-5: Subroutine Argument Block

[figure omitted]

Null arguments in CALL statements must be entered with successive commas, for example, CALL SUBR (A,,B). The value -1 is stored in the argument block as the address of a null argument.

The lower byte of the first word of the argument block contains the number of arguments that are passed to the subroutine. The rest of the argument block contains the addresses of those arguments. The argument block is  $n+1$  words long for n arguments.

The program counter is the linkage register. The subroutine obtains its arguments through R5. In FORTRAN, the calling program saves the registers, and the subroutine leaves the contents of the stack pointer intact before returning to the calling program. The RETURN statement of the subroutine is replaced by

The name of the subroutine must be declared global with the .GLOBL directive in the calling program or with the double colon (::) construction in the called program.

## NOTE

You must make sure that the called program does not modify the argument block passed by the calling program to a sub-program.

1.2.3.1 Subroutine Register Usage — A subroutine that is called by a FORTRAN program does not have to preserve any registers. However, each push onto the stack must be matched by a pop off the stack before exiting from the routine.

User-written assembly language programs must preserve any pertinent registers before calling FORTRAN subprograms or SYSLIB routines. They must then restore registers after the subroutine returns.

Function subroutines return a single result in a register. Table 1–7 shows the register assignments for returning the different variable types.

Table 1-7: Return Value Conventions for Function Subroutines

<table><tr><td>Type</td><td>Result Placed In</td></tr><tr><td>INTEGER*2</td><td>R0</td></tr><tr><td>LOGICAL*1</td><td></td></tr><tr><td>INTEGER*4</td><td>R0 low-order result</td></tr><tr><td>LOGICAL*4</td><td>R1 high-order result</td></tr><tr><td rowspan="2">REAL</td><td>R0 high-order result (including sign and exponent)</td></tr><tr><td>R1 low-order result</td></tr><tr><td rowspan="4">DOUBLE PRECISION</td><td>R0 highest-order result (including sign and exponent)</td></tr><tr><td>R1 next higher order</td></tr><tr><td>R2 next higher order</td></tr><tr><td>R3 lowest-order result</td></tr><tr><td rowspan="4">COMPLEX</td><td>R0 high-order real result</td></tr><tr><td>R1 low-order real result</td></tr><tr><td>R2 high-order imaginary result</td></tr><tr><td>R3 low-order imaginary result</td></tr></table>

Note that floating-point results are returned in the general purpose registers and not in the FPU registers. Assembly language subprograms that use the FP11 Floating Point Unit may be required to save and restore the FPU status.

1.2.3.2 FORTRAN Programs Calling MACRO Subroutines — FORTRAN programs can call MACRO subroutines, but several rules must be followed. For example, the following program named INIARR is a MACRO subroutine that can be called from a FORTRAN program.

[figure omitted]

## A FORTRAN program calls the preceding routine with

## CALL INIARR (IAR,IVAL,N)

where:

INIARR is the name of the subroutine

IAR is the name of the array to initialize

IVAL is the value the array is initialized to

N is the number of elements to initialize

This program illustrates the rules that must be observed when calling a MACRO program. The name of the subroutine is made global by using the .GLOBL directive.

Register 5 (R5) is used to pass the arguments. Thus, in the program INIARR, the argument block would appear as shown in Figure 1–6.

Figure 1-6: Argument Block for Program INIARR

[figure omitted]

Registers R0 through R4 can be freely used since the calling program saves them. Once the arguments are retrieved, you can also use R5.

On completion, the subroutine returns to the calling program through an RTS PC. If your MACRO program pushes data on the stack, you must make sure that all data is popped off the stack before the RTS PC is executed.

The following FORTRAN program named DOFOR calls the subroutine INIARR.

```fortran
PROGRAM DOFOR
C
      INTEGER*2 ARRAY
      DIMENSION ARRAY(10)
      N=2
      DO 20 IVAL=1,10
      CALL INIARR (ARRAY,IVAL,N)
      WRITE (5,100) (ARRAY(I),I=1,N)
20     CONTINUE
100    FORMAT (I3)
      STOP
      END
```

After you compile and link both programs, run the program by typing
, RUN DOFOR RET

The initialized array will be output to the terminal as follows:

1.2.3.3 MACRO Routines Calling FORTRAN Programs — If you want to call FORTRAN subroutines from a MACRO program, create a dummy main program such as

```prolog
PROGRAM FORINT
CALL CALMAC
STOP
END
```

where CALMAC is the name of a MACRO program that can call FORTRAN or MACRO routines.

Creating a dummy program causes the FORTRAN main program to perform the initialization necessary for FORTRAN subroutines.

The following MACRO program named CALMAC calls a FORTRAN subroutine named MAXMIN.

```asm
,TITLE CALMAC
,GLOBL MAXMIN

CALMAC::
    MOV     #ARGBLK,R5          ;POINT R5 TO ARGUMENT BLOCK
    JSR       PC,MAXMIN         ;CALL MAXMIN
    RTS PC
I:        .WORD 28,                  ;VALUE OF FIRST ARGUMENT
J:        .WORD 76,                  ;VALUE OF SECOND ARGUMENT
ARGBLK:   .WORD   2                   ;NUMBER OF ARGUMENTS
        .WORD   I                    ;ADDRESS OF FIRST ARGUMENT
        .WORD   J                    ;ADDRESS OF SECOND ARGUMENT
        .END
```

You must set up the argument block either on the stack or in a separate area in your MACRO program. You then point R5 to the top of the argument block prior to calling the FORTRAN subroutine with a JSR PC, MAX-MIN. In the above program, the argument block is set up in a area of your program.

The following program named STAKEM performs the same operation as the program CALMAC, except that it places the arguments on the stack.

```csv
,TITLE STAKEM
,GLOBL MAXMIN,STAKEM
STAKEM: MOV #J,-(SP)
MOV #I,-(SP)
MOV #2,-(SP)
MOV SP,R5
JSR PC,MAXMIN
ADD #6,SP
RTS PC
I: .WORD 28,
J: .WORD 76,
.END
```

If the argument block is set up on the stack, be sure that you remove the arguments from the stack prior to the execution of the RTS PC. In general, before calling the FORTRAN subroutine, you must save all pertinent registers. You do not know which registers the FORTRAN subroutine is using. The stack pointer remains unchanged across the call.

The name of the FORTRAN subroutine that the MACRO program calls must be defined as a global. In the FORTRAN subroutine, execute normal FORTRAN statements and return to the MACRO program with a RETURN statement.

The following program is the FORTRAN subroutine MAXMIN.

```fortran
SUBROUTINE MAXMIN(IN1,IN2)
      INTEGER BIG,SMALL
      IF (IN1,LT,IN2) GO TO 10
      BIG=IN1
      SMALL=IN2
      TYPE 20,BIG
      TYPE 30,SMALL
      RETURN
10     BIG=IN2
      SMALL=IN1
      TYPE 20,BIG
      TYPE 30,SMALL
20     FORMAT (' THE BIGGER NUMBER IS ',I2)
30     FORMAT (' THE SMALLER NUMBER IS ',I2)
      RETURN
      END
```

After assembling and linking the programs, using either the program CALMAC or STAKEM, type

```txt
. RUN FORINT RET
```

The program executes as follows:

```txt
THE BIGGER NUMBER IS 76
THE SMALLER NUMBER IS 28
STOP --
```

## 1.2.4 FORTRAN Programs in a Foreground/Background Environment

FORTRAN programs can be run in a foreground/background environment, which permits efficient use of CPU execution time. (See Chapter 15 of Introduction to RT-11 for a description of running in an FB environment.) The basic steps in running FORTRAN programs that use the FB monitor are described in this section.

Before running your foreground program, you must use the LOAD command to load the device handlers required by the foreground job. The device handlers are placed in memory between RMON and the USR and KMON, which causes USR and KMON to move down in memory.

Next, you use the FRUN command to load your foreground program in memory between the device handlers and the USR, which causes the USR and KMON to move further down in memory. It is important that you allocate workspace when running a FORTRAN program in the foreground. You do this with the /BUFFER:n option of the FRUN command. Also make sure that any FORTRAN program you run in the foreground has adequate stack space. You can use one of the options supported by the linker (see the RT-11 System Utilities Manual).

The background area must be at least 4K words long to accommodate the USR and KMON. Until you run a background job with the RUN command, KMON is the background job.

When the USR is required, a 2K-word area must be set up in each job for the swapping to occur correctly — that is, there must be space for 2K words in the background area and 2K words in the foreground area. USR swapping is explained in Section 1.2.1.5.

1.2.4.1 Calculating Workspace for a FORTRAN Foreground Program — Additional workspace must be allocated in memory when running a FORTRAN program in the foreground of a foreground/background environment. For a foreground job, the space is allocated by the /BUFFER:n option of the FRUN command. (A background job uses whatever space is available between its high limit and the system's low limit.) When you allocate additional workspace in memory to run a FORTRAN program in the foreground, calculate the space required by using the following formula:

$$
\mathrm{n} = [ 1 / 2 [ 5 0 4 + (3 5 ^ {*} \mathrm{N}) + (\mathrm{R} - 1 3 6) + \mathrm{A} ^ {*} 5 1 2 ] ]
$$

where:

n = number of decimal words

A = the maximum number of files open at any one time. If double buffering is used, A should be multiplied by 2

N = the maximum number of simultaneously open channels (logical unit numbers); the default is 6

R = maximum formatted record length; the default is 136 characters

This formula must be modified for certain SYSLIB functions.

The IQSET function requires the formula to include additional space for queue elements (qcount) as follows:

$$
\mathrm{n} = [ 1 / 2 [ 5 0 4 + (3 5 ^ {*} \mathrm{N}) + (\mathrm{R} - 1 3 6) + \mathrm{A} ^ {*} 5 1 2 ] ] + [ 1 0 ^ {*} \mathrm{qcount} ]
$$

The ICDFN function requires the formula to include additional space for the integer number of channels (num) as follows:

$$
\mathrm{n} = [ 1 / 2 [ 5 0 4 + (3 5 ^ {*} \mathrm{N}) + (\mathrm{R} - 1 3 6) + \mathrm{A} ^ {*} 5 1 2 ] ] + [ 6 ^ {*} \mathrm{num} ]
$$

The INTSET function requires the formula to include additional space for the number of INTSET calls issued in the program as follows:

$$
\mathrm{n} = [ 1 / 2 [ 5 0 4 + (3 5 ^ {*} \mathrm{N}) + (\mathrm{R} - 1 3 6) + \mathrm{A} ^ {*} 5 1 2 ] ] + [ 2 5 ^ {*} \text {INTSET} ]
$$

Any calls, including INTSET, that invoke completion routines must include 64(decimal) words plus the number of words needed to allocate the second record buffer (default is 68[decimal] words). The length of the record buffer is controlled by the /RECORD option to the FORTRAN compiler. If the /RECORD option is not used, the allocation in the formula must be 136(decimal) bytes, or the length that was set at FORTRAN installation time. This modifies the formula as follows:

$$
\mathrm{n} = [ 1 / 2 [ 5 0 4 + (3 5 ^ {*} \mathrm{N}) + (\mathrm{R} - 1 3 6) + \mathrm{A} ^ {*} 5 1 2 ] ] + [ 6 4 + \mathrm{R} / 2 ]
$$

If the /BUFFER option does not allocate enough space in the foreground on the initial call to a completion routine, the following message appears:

```batch
?Err O Non-FORTRAN error call
```

This message also appears if there is not enough free memory for the background job or if a completion routine in the single-job monitor is activated during another completion routine. In the latter case, the job aborts; you should use the FB monitor to run multiple active completion routines.

1.2.4.2 Running a FORTRAN Program in a Foreground/Background Environment — This section briefly describes the procedure for running two FORTRAN programs, one in the background and one in the foreground.

The background program named BACK is as follows:

```fortran
PROGRAM BACKGROUND
IMPLICIT INTEGER(0)
CALL IPOKE("44,"10000,OR,IPEEK("44))
100 CALL PRINT('HELLO FROM THE BACKGROUND')
ICCHAR=ITTINR()
OCHAR=ITTOUR(ICCHAR)
GO TO 100
END
```

This program prints the message "HELLO FROM THE BACKGROUND" and will print the message each time you input a character at the terminal.

The foreground program named FORE is as follows:

```fortran
PROGRAM FOREGROUND
IMPLICIT INTEGER(0)
CALL IPOKE("44,"10000,OR,IPEEK("44))
100 CALL PRINT('HELLO FROM THE FOREGROUND')
ICHAR=ITTINR()
OCHAR=ITTOUR(ICHAR)
GO TO 100
END
```

After compiling both programs, link them. Link the foreground program using the LINK command with the /FOREGROUND option. This option produces a relocatable load module with a .REL file type. For example,

```txt
LINK/FOREGROUND FORE RET
```

Then you can assign the device that will be used for the output of the foreground program. You must also load into memory the peripheral device handlers needed by the foreground program.

The command FRUN loads and starts execution of a .REL program as the foreground job. If the command

.FRUN FORE RET

is typed at this point, the error message

```batch
?Err G2 FORTRAN start fail
```

will be displayed. This message indicates that additional workspace allocation is required and that the /BUFFER option must be used. (Refer to the previous section for the formula to calculate the additional space needed.) Thus, the command would be typed as follows:

```txt
.FRUN FORE/BUFFER:760 RET
```

Execution of this command results in the following output at the terminal:

```txt
F>
HELLO FROM THE FOREGROUND
```

The system first identifies the message as foreground output. Then the foreground job executes and outputs its message. The background monitor next prprints the characters B> and a period, indicating that control has returned to monitor command mode. Command input remains directed to the background job. By typing

```txt
• RUN BACK RET
```

the message from the background job will be displayed

```txt
HELLO FROM THE BACKGROUND
```

Each time a character is input to the terminal, say an "L", the message will be repeated.

```txt
LHELLO FROM THE BACKGROUND
```

Use the CTRL/F command to direct terminal input to the foreground job. The system prints F> to remind you that you are now directing input to the foreground job. When you type a character, such as "Y", the foreground job message will be displayed.

```txt
F>
YHELLO FROM THE FOREGROUND
```

Type a CTRL/B to return to the background job or a CTRL/C to return to monitor command mode. If you are returning to a background environment, you should unload the foreground job and any handlers to reclaim memory space for background use.

## 1.2.5 Linking with FORLIB

Normally, the default system library file (SYSLIB.OBJ) also includes the overlay handlers and the appropriate FORTRAN run-time system routines.

To add FORLIB.OBJ modules to the default library SYSLIB.OBJ, use the following command:

```txt
,LIBRARY/INSERT/REMOVE SYSLIB FORLIB RET
Global? $OVRH RET
Global? RET
```

## 1.2.6 SYSLIB Services Not Provided by Programmed Requests

SYSLIB provides many services that are not provided by programmed requests. Such services are as follows:

• Time conversion and date access

\- Program suspension

\- Two-word integer support (INTEGER\*4)

\- Radix–50 conversion

\- Character string manipulation

1.2.6.1 Time Conversion and Date Access — Several calls allow you to perform time conversions and access the system date.

You use the CVTTIM call to convert a two-word internal format time to hours, minutes, seconds, and ticks. The JTIME call converts a time given in hours, minutes, seconds, and ticks into the internal two-word time format.

If you need to print out the time, the TIMASC call converts the time returned by the .GTIM programmed request into an eight-character ASCII string; the TIME call returns the current time of day as an eight-character ASCII string.

The current system date can be accessed by your program with a DATE call. The date is returned as a string value. IDATE performs similarly, but returns an integer value. DATE and IDATE are part of FORLIB.OBJ.

1.2.6.2 Program Suspension — You suspend execution of a running program for a specified number of ticks with the ITWAIT call. You use the ISLEEP call to suspend a running program for a specified number of hours, minutes, seconds, and ticks. The IUNTIL call allows you to suspend job execution until a specific time of day, which is given to the routine in hours, minutes, seconds, and ticks. You can use this function to periodically collect data and to stop processing between acquisitions.

1.2.6.3 Two-Word Integer Support (INTEGER\*4) — You can make calls to SYS-LIB to manipulate a 32-bit integer that uses two words of storage. The first word contains the low-order part of the value and the second word contains the sign and the high-order part of the value. The range of numbers that is represented is -2(31) to 2(31)-1. This format differs from the two-word internal time format that stores the high-order part of the value in the first word and the low-order part in the second word. Table 1–8 shows the calls that you can use to convert from one format to another.

Table 1-8: SYSLIB Conversion Calls

| From | To | Call |
| --- | --- | --- |
| INTEGER*2 (16-bit integer) | INTEGER*4 | JICVT |
| INTEGER*4 (32-bit integer) | INTEGER*2 | IJCVT |
| INTEGER*4 | REAL*4 | AJFLT/IAJFLT |
| INTEGER*4 | REAL*8 | DJFLT/IDJFLT |
| REAL*4 (2-word floating point) | INTEGER*2 | JAFIX |
| REAL*8 (4-word floating point) | INTEGER*4 | JDFIX |

Calls are also available for you to perform arithmetic operations on INTEGER\*4 values, move a value to a variable, and convert a two-word internal time format to and from an INTEGER\*4 value.

1.2.6.4 Radix-50 Conversion — You can convert ASCII characters to or from Radix-50.

IRAD50 converts a specified number of characters of Radix-50 and returns the number of characters converted as a function result. RAD50 encodes RT-11 file descriptors in Radix-50 notation. R50ASC converts a specified number of Radix-50 characters to ASCII.

1.2.6.5 Character String Operations — SYSLIB provides character string functions that perform string operations such as concatenation, comparison, copying, replacing, and computing the number of characters in a string. For example, the following program will concatenate two character strings.

.TITLE GETTOO
.GLOBL CONCAT
.MCALL .PRINT,.EXIT

START: MOV #ARGBLK,R5
JSR PC,CONCAT
.PRINT #STRCON
.EXIT

ARGBLK: .WORD 3
.WORD STRNG1
.WORD STRNG2
.WORD STRCON

STRING1: .ASCIZ /RESEARCH AND/
STRING2: .ASCIZ / DEVELOPMENT/
STRING: .BLKB 31
.EVEN
.END START

Running this program results in the concatenation of string 1 and string 2, and the output at the terminal is

RESEARCH AND DEVELOPMENT

The following section describes character string functions in detail.

## 1.2.7 Character String Functions

The SYSLIB character string functions and routines provide variable-length string support for RT-11 FORTRAN and for MACRO programs. SYSLIB calls perform the following character string operations:

| Call | Operation |
| --- | --- |
| GETSTR | Reads character strings from a specified FORTRAN logical unit |
| PUTSTR | Writes character strings to a specified FORTRAN logical unit |
| CONCAT | Concatenates variable-length strings |

INDEX Returns the position of one string in another

INSERT Inserts one string into another

LEN Returns the length of a string

REPEAT    Repeats a character string

SCOMP Compares two strings

SCOPY Copies a character string

STRPAD Pads a string with blanks on the right

SUBSTR Copies a substring from a string

TRANSL Performs character modification

TRIM Removes trailing blanks

VERIFY Verifies the presence of characters in a string

Strings are stored in LOGICAL\*1 arrays that you define and dimension. These arrays store strings in ASCII format as one character per array element plus a zero element to indicate the current end of the string.

The length of a string can vary at execution time from zero characters to one less than the size of the array that stores the string. The maximum size of any string is 32767 characters. Strings can contain any of the seven-bit ASCII characters except null(0), since the null character is used to mark the end of the string. The inclusion of a terminating zero byte constitutes an "ASCIZ" format, which is the format set up by a MACRO assembler directive .ASCIZ. This directive automatically sets up strings with a terminating zero byte. Bit 7 of each character must be cleared. Therefore, the valid characters are those whose decimal representations range from 1 to 127, inclusive.

The ASCII code used in this string package is the same as that employed by FORTRAN for A-type FORMAT items, ENCODE/DECODE strings, and object-time format strings. Whenever quoted strings are used as arguments in the CALL statement, ASCIZ strings are generated for these routines by the FORTRAN compiler. Note that a null string (a string containing no characters) can be represented in FORTRAN by a variable or constant of any type that contains the value zero, or by a LOGICAL variable or constant with the .FALSE. value.

In many routines, it is difficult to predict the length of the string produced. To prevent a string from overflowing the array that contains it, you can specify an optional integer argument to the subroutine. This argument, called len, limits the length of an output string to the value specified for len plus one (for the null terminator), so that the array receiving the result must be at least len plus one elements in size.

## NOTE

If the string is larger than the array, other data may be destroyed and cause unpredictable results.

When len is specified, you can also include the optional argument called err. Err is a logical variable that should be initialized by the FORTRAN program to the .FALSE. value. If a string function is given the arguments len and err, and len is actually used to limit the length of the string result, then err is set to the .TRUE. value. If len is not used to truncate the string, err is unchanged — that is, it retains a .FALSE. value.

The argument len can appear alone. However, len must appear if err is specified. The err argument should be used for GETSTR and PUTSTR.

Several routines use the concept of character position. Each character in a string is assigned a position number. The first character in a string is in position one. Each subsequent character has a position number one greater than the character that precedes it.

1.2.7.1 Allocating Character String Variables — A one-dimensional LOGICAL\*1 array can contain a single string whose length can vary from zero characters to one fewer than the dimensioned length of the array. For example,

LOGICAL\*1 A(45)

## !ALLOCATE SPACE FOR STRING VARIABLE A

allows array A to be used as a string variable that can contain a string of 44 or fewer characters. Similarly, a two-dimensional LOGICAL\*1 array can be used to contain a one-dimensional array of strings. Each string in the array can have a length up to one less than the first dimension of the LOGICAL\*1 array. There can be as many strings as the number specified for the second dimension of the LOGICAL\*1 array. For example,

LOGICAL\*1 W(21,10)

!ALLOCATE AN ARRAY OF STRINGS

creates string array W that has ten string elements, each of which can contain up to 20 characters. String I in array W is referenced in subroutine or function calls as W(1,I).

The following example allocates a two-dimensional string array.

LOGICAL\*1 T(14,5,7)

!ALLOCATE A 5 BY 7 ARRAY OF 13-CHARACTER
!STRINGS

Each string in array T may vary in length to a maximum of 13 characters. String I,J of the array can be referenced as T(1,I,J). Note that T is the same as T(1,1,1). This dimensioning process can create string arrays of up to six dimensions (represented by LOGICAL\*1 arrays of up to seven dimensions).

1.2.7.2 Passing Strings to Subprograms — There are three ways to pass strings to subprograms.

1. LOGICAL\*1 arrays that contain strings can be placed in a COMMON block and referenced by any or all routines with a similar common declaration. However, when you place a LOGICAL\*1 array in a common block, make sure that the array is even in length, that odd-length arrays are paired to result in an overall even length, or that the strings are together as the last elements in the COMMON block. Otherwise, all succeeding variables in the COMMON block may be assigned odd addresses.

```txt
LOGICAL*1 A(21) !STRING VARIABLE A, 20 CHARACTERS MAXIMUM
CALL SUBR(A)
passes string A to subroutine SUBR.
```

A LOGICAL\*1 array has an odd length only if the product of its dimensions is odd. For example,

```c
LOGICAL*1 B(10,7)          !(10*7) = 70; EVEN LENGTH
LOGICAL*1 H (21)           !21 IS AN ODD LENGTH
```

These might be handled as follows:

```csv
COMMON A1,A2,A3(10),H(21) !PLACE ODD-SIZED ARRAY AT END
or
COMMON A1,A2,H(21),H1(7),A3(10) !PAIR ODD-SIZE ARRAYS H AND H1
```

These restrictions apply only to LOGICAL\*1 variables and arrays.

2. A single string can be passed by using its array name as an argument. For example,

3. If the calling program has declared a multidimensional array, and only one string of that array is to be passed to a subroutine, then the subroutine call should specify the first element of the string to be passed (this requires that the first dimension of the array equals the maximum length of each string).

```txt
For example,
    LOGICAL*1 NAMES (81,20) !20 NAMES, 80 CHARACTERS EACH
    LOGICAL*1 ERR
    .
    .
    .
    DO 10 NAMNUM=1,20 !GET ALL 20 NAMES
10 CALL GETSTR (5,NAMES(1,NAMNUM),80,ERR) !FROM TT
```

If the maximum length of a string argument is unknown in a subroutine or function, or if the routine is used to handle many different lengths, the dummy argument in the routine should be declared as a LOGICAL\*1 array with a dimension of one, such as LOGICAL\*1 ARG(1). In this case, the string routines correctly determine the length of ARG whenever it is used, but it is not possible to determine the maximum size of any string that can be stored in ARG. If a multidimensional array of strings is passed to a routine, it must be declared in the called program with the same dimensions that were specified in the calling program.

## NOTE

The length argument specified in many of the character string functions refers to the maximum length of the string excluding the necessary null byte terminator. The length of the LOGICAL\*1 array to receive the string must be at least one greater than the length argument.

1.2.7.3 Using Quoted-String Literals — You can use quoted strings as arguments to any of the string routines that are invoked as functions or with the CALL statement. For example,

```txt
CALL SCOMP(NAME, 'SMYTHE, R', M)
```

compares the string in the array NAME to the constant string SMYTHE, R and sets the value of the integer variable accordingly.

## 1.2.8 System Subroutine Summary

Table 1–9 lists the SYSLIB subroutines alphabetically within categories, the sections in which they are located, and a brief description of each subroutine. Those subroutines prefaced with an asterisk (\*) are allowed only in a foreground/background environment, under either the FB or XM monitor. The SYSLIB subroutines do not support the XM monitor mapping programmed requests. Use FORTRAN virtual arrays to access extended memory.

Table 1-9: Summary of SYSLIB Subroutines

<table><tr><td>Name</td><td>Section</td><td>Description</td></tr><tr><td colspan="3">File-Oriented Operations</td></tr><tr><td>CLOSEC,ICLOSE</td><td>3.3</td><td>Closes the specified channel.</td></tr><tr><td>IDELET</td><td>3.22</td><td>Deletes a file from the specified device.</td></tr><tr><td>IENTER</td><td>3.25</td><td>Creates a new file for output.</td></tr><tr><td>IFPROT</td><td>3.27</td><td>Changes the file&#x27;s protection.</td></tr><tr><td>IRENAM</td><td>3.46</td><td>Changes the name of the indicated file.</td></tr><tr><td>ISFDAT</td><td>3.53</td><td>Changes the file&#x27;s creation date.</td></tr><tr><td>LOOKUP</td><td>3.79</td><td>Opens an existing file for input and/or output via the specified channel.</td></tr><tr><td colspan="3">Data Transfer Operations</td></tr><tr><td>IABTIO</td><td>3.12</td><td>Aborts I/O operations on a specified channel.</td></tr><tr><td>GTLIN</td><td>3.11</td><td>Transfers a line of input from the console terminal or indirect file (if active) to the user program.</td></tr><tr><td>*IRCVD*IRCVDC*IRCVDF*IRCVDW</td><td>3.44</td><td>Receives data. Allows a job to read messages or data sent by another job in an FB environment. The four modes correspond to the IREAD, IREADC, IREADF, and IREADW modes.</td></tr><tr><td>IREAD</td><td>3.45</td><td>Transfers data from a file to a memory buffer and returns control to the user program when the request is entered in the I/O queue. No special action is taken upon completion of I/O.</td></tr></table>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">\* FB and XM monitors only.</span></small>

(continued on next page)

Table 1-9: Summary of SYSLIB Subroutines (Cont.)

| Name | Section | Description |
| --- | --- | --- |
| IREADC | 3.45 | Transfers data from a file to a memory buffer and returns control to the user program when the request is entered in the I/O queue. Upon completion of the read, control transfers to the assembly language routine specified in the IREADC function call. |
| IREADF | 3.45 | Transfers data from a file to a memory buffer and returns control to the user program when the request is entered in the I/O queue. Upon completion of the read, control transfers to the FORTRAN subroutine specified in the IREADF function call. |
| IREADW | 3.45 | Transfers data from a file to a memory buffer and returns control to the program only after the transfer is complete. |
| *ISDAT*ISDATC*ISDATF*ISDATW | 3.51 | Allows the user to send messages or data to the other job in an FB environment. The four functions correspond to the IWRITE, IWRITC, IWRITF, and IWRITW modes. |
| ITTINR | 3.59 | Gets one character from the console keyboard. |
| ITTOUR | 3.60 | Transfers one character to the console terminal. |
| IWAIT | 3.64 | Waits for completion of all I/O on a specified channel (commonly used with the IREAD and IWRITE functions). |
| IWRITC | 3.65 | Transfers data to a file and returns control to the user program when the request is entered in the I/O queue. Upon completion of the write, control transfers to the assembly language routine specified in the IWRITC function call. |
| IWRITE | 3.65 | Transfers data to a file and returns control to the user program when the request is entered in the I/O queue. No special action is taken upon completion of the I/O. |
| IWRITF | 3.65 | Transfers data to a file and returns control to the user program when the request is entered in the I/O queue. Upon completion of the write, control transfers to the FORTRAN subroutine specified in the IWRITF function call. |
| IWRITW | 3.65 | Transfers data to a file and returns control to the user program only after the transfer is complete. |
| †MTATCH | 3.81 | Attaches a particular terminal in a multiterminal environment. |
| †MTDTCH | 3.82 | Detaches a particular terminal in a multiterminal environment. |
| †MTGET | 3.83 | Provides information about a particular terminal in a multi-terminal system. |
| †MTIN | 3.84 | Transfers characters from a specific terminal to the user program in a multiterminal system. |
| †MTOUT | 3.85 | Transfers characters to a specific terminal in a multiterminal system. |
| †MTPRNT | 3.86 | Prints a message to a specific terminal in a multiterminal system. |

$^{\dagger}$  With multiterminal support only.

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">\* FB and XM monitors only.</span></small>

(continued on next page)

Table 1-9: Summary of SYSLIB Subroutines (Cont.)

<table><tr><td>Name</td><td>Section</td><td>Description</td></tr><tr><td>†MTRCTO</td><td>3.87</td><td>Enables output to terminal by canceling the effect of a previously typed CTRL/O.</td></tr><tr><td>†MTSET</td><td>3.88</td><td>Sets terminal and line characteristics in a multiterminal system.</td></tr><tr><td>†MTSTAT</td><td>3.89</td><td>Returns multiterminal system status.</td></tr><tr><td>*MWAIT</td><td>3.90</td><td>Waits for messages to be processed.</td></tr><tr><td>PRINT</td><td>3.91</td><td>Outputs an ASCII string to the console terminal.</td></tr><tr><td colspan="3">Channel-Oriented Operations</td></tr><tr><td>ICDFN</td><td>3.16</td><td>Defines additional I/O channels.</td></tr><tr><td>*ICHCPY</td><td>3.17</td><td>Allows access to files currently open in another job&#x27;s environment.</td></tr><tr><td>ICSTAT</td><td>3.21</td><td>Returns the status of a specified channel.</td></tr><tr><td>IFREEC</td><td>3.28</td><td>Returns the specified RT-11 channel to the available pool of channels for the FORTRAN I/O system.</td></tr><tr><td>IGETC</td><td>3.29</td><td>Allocates an RT-11 channel and informs the FORTRAN I/O system of its use.</td></tr><tr><td>ILUN</td><td>3.33</td><td>Returns the RT-11 channel number with which a FORTRAN logical unit is associated.</td></tr><tr><td>IREOPN</td><td>3.47</td><td>Restores the parameters stored via an ISAVES function and reopens the channel for I/O.</td></tr><tr><td>ISAVES</td><td>3.48</td><td>Stores five words of channel status information into a user-specified array and deactivates the channel.</td></tr><tr><td>PURGE</td><td>3.92</td><td>Deactivates a channel.</td></tr><tr><td colspan="3">Device and File Specifications</td></tr><tr><td>IASIGN</td><td>3.15</td><td>Sets information in the FORTRAN logical unit table.</td></tr><tr><td>ICSI</td><td>3.20</td><td>Calls the RT-11 CSI in special mode to decode file specifications and options.</td></tr><tr><td colspan="3">Timer Support Operations</td></tr><tr><td>CVTTIM</td><td>3.5</td><td>Converts a two-word internal format time to hours, minutes, seconds, and ticks.</td></tr><tr><td>GTIM</td><td>3.9</td><td>Gets time of day.</td></tr><tr><td>ICMKT</td><td>3.19</td><td>Cancels an unexpired ISCHED, ITIMER, or MRKT request (valid under FB and XM, and for SJ monitors with timer support, a SYSGEN option).</td></tr><tr><td>ISCHED</td><td>3.49</td><td>Schedules the specified FORTRAN subroutine to be entered at the specified time of day as an asynchronous completion routine (valid under FB and XM, and for SJ monitors with timer support, a special feature).</td></tr><tr><td>ISDTTM</td><td>3.52</td><td>Changes the system date and time.</td></tr></table>

$^{\dagger}$  With multiterminal support only.

\* FB and XM monitors only.

(continued on next page)

Table 1-9: Summary of SYSLIB Subroutines (Cont.)

<table><tr><td>Name</td><td>Section</td><td>Description</td></tr><tr><td>‡ISLEEP</td><td>3.54</td><td>Suspends main program execution of the running job for a specified amount of time; completion routines continue to run.</td></tr><tr><td>ITIMER</td><td>3.57</td><td>Schedules the specified FORTRAN subroutine to be entered as an asynchronous completion routine when the time interval specified has elapsed (valid under FB and XM, and for SJ monitors with timer support, a special feature).</td></tr><tr><td>‡ITWAIT</td><td>3.61</td><td>Suspends the running job for a specified amount of time; completion routines continue to run.</td></tr><tr><td>‡IUNTIL</td><td>3.62</td><td>Suspends the main program execution of the running job until a specified time of day; completion routines continue to run.</td></tr><tr><td>JTIME</td><td>3.76</td><td>Converts hours, minutes, seconds, and ticks into two-word internal format time.</td></tr><tr><td>MRKT</td><td>3.80</td><td>Schedules an assembly language routine to be activated as an asynchronous completion routine after a specified interval (valid under FB and XM, and for SJ monitors with timer support, a special feature).</td></tr><tr><td>SECNDS</td><td>3.103</td><td>Returns the current system time in seconds past midnight minus the value of a specified argument.</td></tr><tr><td>TIMASC</td><td>3.108</td><td>Converts a specified two-word internal format time into an eight-character ASCII string.</td></tr><tr><td>TIME</td><td>3.109</td><td>Returns the current system time of day as an eight-character ASCII string.</td></tr><tr><td colspan="3">RT-11 Services</td></tr><tr><td>CHAIN</td><td>3.2</td><td>Chains to another program (from the background job only).</td></tr><tr><td>*DEVICE</td><td>3.6</td><td>Specifies actions to be taken on normal or abnormal program termination, such as turning off interrupt enable on user-programmed devices.</td></tr><tr><td>GTJB,IGTJB</td><td>3.10</td><td>Returns the parameters of the specified job.</td></tr><tr><td>IDSTAT</td><td>3.24</td><td>Returns the status of the specified device.</td></tr><tr><td>IFETCH</td><td>3.26</td><td>Loads a device handler into memory.</td></tr><tr><td>IQSET</td><td>3.42</td><td>Expands the size of the RT-11 monitor queue from the free space managed by the FORTRAN system.</td></tr><tr><td>ISPFN</td><td>3.55</td><td>Issues special function requests to various handlers, such as magtape. The four modes correspond to the IWRITE, IWRITC, IWRITF, and IWRITW modes.</td></tr><tr><td>ISPFCN</td><td></td><td></td></tr><tr><td>ISPFNF</td><td></td><td></td></tr><tr><td>ISPFNW</td><td></td><td></td></tr><tr><td>*ITLOCK</td><td>3.58</td><td>Indicates whether the USR is currently in use by another job and performs a LOCK if the USR is available.</td></tr><tr><td>LOCK</td><td>3.78</td><td>Makes the RT-11 monitor User Service Routine (USR) permanently resident until an UNLOCK function is executed. If necessary, a portion of the user&#x27;s program is swapped out to make room for the USR.</td></tr></table>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">$^{\ddagger}$  SYSGEN option in SJ monitor.</span></small>

(continued on next page)

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">\* FB and XM monitors only.</span></small>

Table 1-9: Summary of SYSLIB Subroutines (Cont.)

<table><tr><td>Name</td><td>Section</td><td>Description</td></tr><tr><td>RCHAIN</td><td>3.96</td><td>Allows a program to access variables passed across a chain.</td></tr><tr><td>RCTRLO</td><td>3.97</td><td>Enables output to the terminal by canceling the effect of a previously typed CTRL/O.</td></tr><tr><td>*RESUME</td><td>3.99</td><td>Causes the main program execution of a job to resume at the point it was suspended by a SUSPND function call.</td></tr><tr><td>SCCA</td><td>3.100</td><td>Intercepts a CTRL/C command initiated at the console terminal.</td></tr><tr><td>SETCMD</td><td>3.104</td><td>Passes command lines to the keyboard monitor for execution after the program exits.</td></tr><tr><td>*SUSPND</td><td>3.107</td><td>Suspends main program execution of the running job; completion routines continue to execute.</td></tr><tr><td>UNLOCK</td><td>3.112</td><td>Releases the USR if a LOCK was performed; the user program is swapped in if required.</td></tr><tr><td colspan="3">INTEGER*4 Support Functions</td></tr><tr><td>AJFLT</td><td>3.1</td><td>Converts a specified INTEGER*4 value to REAL*4 and returns the result as the function value.</td></tr><tr><td>DJFLT</td><td>3.7</td><td>Converts a specified INTEGER*4 value to REAL*8 and returns the result as the function value.</td></tr><tr><td>IAJFLT</td><td>3.14</td><td>Converts a specified INTEGER*4 value to REAL*4 and stores the result.</td></tr><tr><td>IDJFLT</td><td>3.23</td><td>Converts a specified INTEGER*4 value to REAL*8 and stores the result.</td></tr><tr><td>IJCVT</td><td>3.32</td><td>Converts a specified INTEGER*4 value to INTEGER*2.</td></tr><tr><td>JADD</td><td>3.66</td><td>Computes the sum of two INTEGER*4 values.</td></tr><tr><td>JAFIX</td><td>3.67</td><td>Converts a REAL*4 value to INTEGER*4.</td></tr><tr><td>JCMP</td><td>3.68</td><td>Compares two INTEGER*4 values and returns an INTEGER*2 value that reflects the signed comparison result.</td></tr><tr><td>JDFIX</td><td>3.69</td><td>Converts a REAL*8 value to INTEGER*4.</td></tr><tr><td>JDIV</td><td>3.70</td><td>Computes the quotient and remainder of two INTEGER*4 values.</td></tr><tr><td>JICVT</td><td>3.71</td><td>Converts an INTEGER*2 value to INTEGER*4.</td></tr><tr><td>JJCVT</td><td>3.72</td><td>Converts the two-word internal time format to INTEGER*4 format, and vice versa.</td></tr><tr><td>JMOV</td><td>3.73</td><td>Assigns an INTEGER*4 value to a variable.</td></tr><tr><td>JMUL</td><td>3.74</td><td>Computes the product of two INTEGER*4 values.</td></tr><tr><td>JSUB</td><td>3.75</td><td>Computes the difference between two INTEGER*4 values.</td></tr></table>

\* FB and XM monitors only.

(continued on next page)

Table 1-9: Summary of SYSLIB Subroutines (Cont.)

<table><tr><td>Name</td><td>Section</td><td>Description</td></tr><tr><td colspan="3">Character String Functions</td></tr><tr><td>CONCAT</td><td>3.4</td><td>Concatenates two variable-length strings.</td></tr><tr><td>GETSTR</td><td>3.8</td><td>Reads a character string from a specified FORTRAN logical unit.</td></tr><tr><td>INDEX</td><td>3.34</td><td>Returns the location in one string of the first occurrence of another string</td></tr><tr><td>INSERT</td><td>3.35</td><td>Replaces a portion of one string with another string.</td></tr><tr><td>ISCOMP</td><td>3.50</td><td>Compares two character strings.</td></tr><tr><td>IVERIF</td><td>3.63</td><td>Indicates whether characters in one string appear in another.</td></tr><tr><td>LEN</td><td>3.77</td><td>Returns the number of characters in a specified string.</td></tr><tr><td>PUTSTR</td><td>3.93</td><td>Writes a variable-length character string on a specified FORTRAN logical unit.</td></tr><tr><td>REPEAT</td><td>3.98</td><td>Concatenates a specified string with itself to provide an indicated number of copies and stores the resultant string.</td></tr><tr><td>SCOMP</td><td>3.101</td><td>Compares two character strings.</td></tr><tr><td>SCOPY</td><td>3.102</td><td>Copies a character string from one array to another.</td></tr><tr><td>STRPAD</td><td>3.105</td><td>Pads a variable-length string on the right with blanks to create a new string of a specified length.</td></tr><tr><td>SUBSTR</td><td>3.106</td><td>Copies a substring from a specified string.</td></tr><tr><td>TRANSL</td><td>3.110</td><td>Replaces one string with another after performing character modification.</td></tr><tr><td>TRIM</td><td>3.111</td><td>Removes trailing blanks from a character string.</td></tr><tr><td>VERIFY</td><td>3.113</td><td>Indicates whether characters in one string appear in another.</td></tr><tr><td colspan="3">Radix-50 Conversion Operations</td></tr><tr><td>IRAD50</td><td>3.43</td><td>Converts characters in ASCII format to Radix-50, returning the number of characters converted.</td></tr><tr><td>R50ASC</td><td>3.94</td><td>Converts characters in Radix-50 format to ASCII.</td></tr><tr><td>RAD50</td><td>3.95</td><td>Converts six ASCII characters, returning a REAL*4 result that is the two-word Radix-50 value.</td></tr><tr><td colspan="3">Miscellaneous Services</td></tr><tr><td>IADDR</td><td>3.13</td><td>Obtains the memory address of a specified entity.</td></tr><tr><td>IGETSP</td><td>3.30</td><td>Returns the address and size (in words) of free space obtained from the FORTRAN system.</td></tr><tr><td>INTSET</td><td>3.36</td><td>Establishes a specified FORTRAN subroutine as an interrupt service routine with a specified priority.</td></tr><tr><td>IPEEK</td><td>3.37</td><td>Returns the value of a word located at a specified absolute memory address.</td></tr><tr><td>IPEEKB</td><td>3.38</td><td>Returns the value of a byte located at a specified byte address.</td></tr><tr><td>IPOKE</td><td>3.39</td><td>Stores an integer value in an absolute memory location.</td></tr><tr><td>IPOKEB</td><td>3.40</td><td>Stores an integer value in a specified byte location.</td></tr><tr><td>IPUT</td><td>3.41</td><td>Changes the value of the word located at an offset specified from the beginning of the RT-11 monitor.</td></tr><tr><td>ISPY</td><td>3.56</td><td>Returns the integer value of the word located at a specified offset from the beginning of the RT-11 resident monitor.</td></tr></table>
