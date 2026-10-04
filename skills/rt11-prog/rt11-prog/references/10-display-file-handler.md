# RT-11 PRM reference: App.A VT11/VS60 display file handler: graphics macros (.INSRT .REMOV .BLANK .LPEN .SCROL...), extended display instructions, display file structure, VTMAC, examples

Source: RT-11 Programmer's Reference Manual AA-H378C-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' sometimes reads as ',' (`,MCALL` = `.MCALL`), 'R0' as 'RO', '#' as '\*' or '*'. Verify exact macro expansions against `sysmac_v53.mac`.

Contents:
- Appendix A Display File Handler
- A.1 Description
- A.1.1 Assembly Language Display Support
- A.1.2 Monitor Display Support
- A.2 Description of Graphics Macros
- A.2.1 .BLANK
- A.2.2 .CLEAR
- A.2.3 .INSRT
- A.2.4 .LNKRT
- A.2.5 .LPEN
- A.2.6 .NAME
- A.2.7 .REMOV
- A.2.8 .RESTR
- A.2.9 .SCROL
- A.2.10 .START
- A.2.11 .STAT
- A.2.12 .STOP
- A.2.13 .SYNC/.NOSYN
- A.2.14 .TRACK
- A.2.15 .UNLNK
- A.3 Extended Display Instructions
- A.3.1 DJSR Subroutine Call Instruction
- A.3.2 DRET Subroutine Return Instruction
- A.3.3 DSTAT Display Status Instruction
- A.3.4 DHALT Display Halt Instruction
- A.3.5 DNAME Load Name Register Instruction
- A.4 Using the Display File Handler
- A.4.1 Assembling Graphics Programs
- A.4.2 Linking Graphics Programs
- A.5 Display File Structure
- A.5.1 Subroutine Calls
- A.5.2 Main File/Subroutine Structure
- A.5.3 BASIC-11 Graphic Software Subroutine Structure
- A.6 Summary of Graphics MACRO Calls
- A.7 Display Processor Mnemonics
- A.8 Assembly Instructions
- A.8.1 General Instructions
- A.8.2 VTBASE
- A.8.3 VTCAL1 - VTCAL4
- A.8.4 VTHDLR
- A.8.5 Building VTLIB.OBJ
- A.9 VTMAC

---

## Appendix A Display File Handler

This appendix describes the assembly language support provided under RT-11 for the VT11 graphic display hardware systems.

The following manuals are suggested for additional reference:

GT40/GT42 User's Guide
EK-GT40-OP-002

GT44 User's Guide
EK-GT44-OP-001

VT11 Graphic Display Processor
EK-VT11-TM-001

DECGRAPHIC-11 GT Series Reference Card
EH-02784-73

DECGraphic-11 FORTRAN Reference Manual
DEC-11-GFRMA-A-D

BASIC-11 Graphics Extensions User's Guide
DEC-11-LBGEA-A-D

## A.1 Description

The graphics display terminals have hardware configurations that include a display processor and CRT (cathode ray tube) display. All systems are equipped with light pens and hardware character and vector generators, and are capable of high-quality graphics. The Display File Handler supports this graphics hardware at the assembly language level under the RT-11 monitor.

## A.1.1 Assembly Language Display Support

The Display File Handler is not an RT-11 device handler, since it does not use the I/O structure of the RT-11 monitor. For example, it is not possible to use a utility program to transfer a text file to the display through the Display File Handler. Rather, the Display File Handler provides the graphics programmer the means for the display of graphics files and the easy management of the display processor. Included in its capabilities are such services as interrupt handling, light pen support, tracking object, and starting and stopping of the display processor.

The Display File Handler manages the display processor by means of a base segment (called VTBASE) which contains interrupt handlers, an internal display file and some pointers and flags. The display processor cycles through the internal display file; any user graphics files to be displayed are accessed by display subroutine calls from the Handler's display file. In this way, the Display File Handler exerts control over the display processor, relieving the assembly language user of the task.

Through the Display File Handler, the programmer can insert and remove calls to display files from the Handler's internal display file. Up to two user files may be inserted at one time, and that number may be increased by re-assembling the Handler. Any user file inserted for display may be blanked (the subroutine call to it bypassed) and unblanked by macro calls to the Display File Handler.

Since the Handler treats all user display files as graphics subroutines to its internal display file, a display processor subroutine call is required. This is implemented with software, using the display stop instruction, and is available for user programs. This instruction and several other extended instructions implemented with the display stop instruction are described in Section A.3.

The facilities of the Display File Handler are accessed through a file of macro definitions (VTMAC) which generate calls to a set of subroutines in VTLIB. VTMAC's call protocol is similar to that of the RT-11 macros. The expansion of the macros is shown in Section A.6. VTMAC also contains, for convenience in programming, the set of recommended display processor instruction mnemonics and their values. The mnemonics are listed in Section A.7 and are used in the examples throughout this appendix.

VTCAL1 through VTCAL4 are the set of subroutines which service the VTMAC calls. They include functions for display file and display processor management. These are described in detail in Section A.2. VTCAL1 through VTCAL4 are distributed, along with the base segment VTBASE, as a file of five object modules called VTHDLR.OBJ. VTHDLR is built into the graphics library VTLIB by using the monitor LIBRARY command. VTHDLR only supports VT11 hardware. Section A.4.2 shows an example.

## A.1.2 Monitor Display Support

The RT-11 monitor, under Version 03 and later, directly supports the display as a console device. A keyboard monitor command, GT ON (GT OFF) permits the selection of the display as console device. Selection results in the allocation of approximately 1.25K words of memory for text buffer and code. The buffer holds approximately 2000 characters.

The text display includes a blinking cursor to indicate the position in the text where a character is added. The cursor initially appears at the top left corner of the text area. As lines are added to the text the cursor moves down the screen. When the maximum number of lines are on the screen, the top line is deleted from the text buffer when the line feed terminating a new line is received. This causes the appearance of “scrolling,” as the text disappears off the top of the display.

When the maximum number of characters have been inserted in the text buffer, the scroller logic deletes a line from the top of the screen to make room for additional characters. Text may appear to move (scroll) off the top of the screen while the cursor is in the middle of a line.

The Display File Handler can operate simultaneously with the scroller program, permitting graphic displays and monitor dialogue to appear on the screen at the same time. It does this by inserting its internal display file into the display processor loop through the text buffer. However, the following should be noted. Under the SJ Monitor, if a program using the display for graphics is running with the scroller in use (that is, GT ON is in effect), and the program does a soft exit (.EXIT with R0 not equal to 0) with the display stopped, the display remains stopped until a CTRL/C is typed at the keyboard.

This can be recognized by failure of the monitor to echo on the screen when expected. If the scroller text display disappears after a program exit, always type CTRL/C to restore. If CTRL/C fails to restore the display, the running program probably has an error.

Four scroller control characters provide the user with the capability of halting the scroller, advancing the scrolling in page sections, and printing hard copy from the scroller.

## NOTE

The scroller logic does not limit the length of a line, but the length of text lines affects the number of lines which may be displayed, since the text buffer is finite. As text lines become longer, the scroller logic may delete extra lines to make room for new text, temporarily decreasing the number of lines displayed.

## A.2 Description of Graphics Macros

The facilities of the Display File Handler are accessed through a set of macros, contained in VTMAC, which generate assembly language calls to the Handler at assembly time. The calls take the form of subroutine calls to the sub-routines in VTLIB. Arguments are passed to the subroutines through register 0 and, in the case of the .TRACK call, through both register 0 and the stack.

This call convention is similar to Version 1 RT-11 I/O macro calls, except that the subroutine call instruction is used instead of the EMT instruction. If a macro requires an argument but none is specified, it is assumed that the address of the argument has already been placed in register 0. The programmer should not assume that R0 is preserved through the call.

## A.2.1 .BLANK

The .BLANK request temporarily blanks the user display file specified in the request. It does this by bypassing the call to the user display file, which prevents the display processor from cycling through the user file, effectively blanking it. This effect can later be canceled by the .RESTR request, which restores the user file. When the call returns, the user is assured the display processor is not in the file that was blanked.

Macro Call: .BLANK faddr

where:

faddr is the address of the user display file to be blanked

Errors:

No error is returned. If the file specified was not found in the Handler file or has already been blanked, the request is ignored.

## A.2.2 .CLEAR

The .CLEAR request initializes the Display File Handler, clearing out any calls to user display files and resetting all of the internal flags and pointers.

After initialization with .LNKRT (Section A.2.4), the .CLEAR request can be used any time in a program to clear the display and to reset pointers. All calls to user files are deleted and all pointers to status buffers are reset. They must be re-inserted if they are to be used again.

Macro Call: .CLEAR

Errors:
    None.

Example:

This example uses a .CLEAR request to initialize the Handler then later uses the .CLEAR to re-initialize the display. The first .CLEAR is used for the case when a program may be restarted after a CTRL C or other exit.

BR RSTRT

EX1: BIS #20000,@#44 ;SET REENTER BIT IN JSW
RSTRT: .UNLNK ;CLEARS LINK FLAG FOR RESTART
.LNKRT ;SET UP VECTORS, START DISPLAY
.CLEAR ;INITIALIZE HANDLER
.INSRT #FILE1 ;DISPLAY A PICTURE
1\$: .TTYIN ;WAIT FOR A KEY STRIKE
CMPB #12,RO ;LINE FEED?
BNE 1\$ ;NO,' LOOP
.CLEAR ;YES, CLEAR DISPLAY
.INSRT #FILE2 ;DISPLAY NEW PICTURE
.
.
.
FILE1: POINT ;AT POINT (0,500)
0
500
LONGV ;DRAW A LINE
500!INTX ;TO (500,500)
0
DRET
0

FILE2: POINT          ;AT POINT (500,0)
        500
        0
        LONGV            ;DRAW A LINE
        0! INTX         ;TO (500,500)
        500
        DRET
        0

        .END EX1

## A.2.3 .INSRT

The .INSRT request inserts a call to the user display file specified in the request into the Display File Handler's internal display file. .INSRT causes the display processor to cycle through the user file as a subroutine to the internal file. The handler permits two user files at one time. The call inserted in the handler looks like the following:

DJSR                      #DISPLAY SUBROUTINE
.+4                       #RETURN ADDRESS
.faddr                   #SUBROUTINE ADDRESS

The call to the user file is removed by replacing its address with the address of a null display file. The user file is blanked by replacing the DJSR with a DJMP instruction, bypassing the user file.

Macro Call: .INSRT faddr

where:

faddr is the address of the user display file to be inserted

Errors:

The .INSRT request returns with the C bit set if there was an error in processing the request. An error occurs only when the Handler's display file is full and cannot accept another file. If the user file specified exists, the request is not processed. Two display files with the same starting address cannot be inserted.

Example:

See the examples in Sections A.2.2 and A.2.4.

## A.2.4 .LNKRT

The .LNKRT request sets up the display interrupt vectors and possibly links the Display File Handler to the scroll text buffer in the RT-11 monitor. It must be the first call to the Handler, and is used whether or not the RT-11 monitor is using the display for console output (that is, the KMON command GT ON has been entered).

The .LNKRT request used with Version 03 and later RT-11 monitors enables a display application program to determine the environment in which it is operating. Error codes are provided for the situations where there is no display hardware present on the system or the display hardware is already being used by another task (for example, a foreground job in the foreground/background version).

The existence of the monitor scroller and the size of the Handler's subpicture stack are also returned to the caller. If a previous call to .LNKRT was made without a subsequent .UNLNK, the .LNKRT call is ignored and an error code is returned.

Macro Call: .LNKRT

## Errors:

Error codes are returned in R0, with the N condition bit set.

## Code Meaning

-1 No VT11 display hardware is present on this system.

-2 VT11 hardware is presently in use.

-3 Handler has already been linked.

On completion of a successful .LNKRT request, R0 will contain the display subroutine stack size, indicating the depth to which display subroutines may be nested. The N bit will be zero.

If the RT-11 monitor scroll text buffer was not in memory at the time of the .LNKRT, the C bit will be returned set. The KMON commands GT ON and GT OFF cannot be issued while a task is using the display.

## Example:

START:      .LNKRT
        BMI          ERROR       ;LINK TO MONITOR
        BCS          CONT     ;ERROR DOING LINK
        .SCROL   #SBUF     ;NO SCROLL IF C SET
    CONT:      .INSRT  #FILE1   ;ADJUST SCROLL PARAMETERS
1\$:      .TTYIN
        CMPB     #12,RO   ;DISPLAY A PICTURE
        BNE      1\$           ;WAIT FOR KEY STRIKE
        .UNLNK
        .EXIT

SBUF: .BYTE 5 ;LINE COUNT OF 5
.BYTE 7 ;INTENSITY 7 (SCALE OF 1-8)
.WORD 1000 ;POSITION OF TOP LINE

FILE1: POINT ;AT POINT (500,500)
500
500
CHAR ;DISPLAY SOME TEXT
.ASCI I /FILE1 THIS IS FILE1. TYPE CR TO EXIT/
.EVEN
DRET
O

ERROR: Error routine

## A.2.5 .LPEN

The .LPEN request transfers the address of a light pen status data buffer to VTBASE. Once the buffer pointer has been passed to the Handler, the light pen interrupt handler in VTBASE will transfer display processor status data to the buffer, depending on the state of the buffer flag.

The buffer must have seven contiguous words of storage. The first word is the buffer flag, and it is initially cleared (set to zero) by the .LPEN request. When a light pen interrupt occurs, the interrupt handler transfers status data to the buffer and then sets the buffer flag non-zero. The program can loop on the buffer flag when waiting for a light pen hit (although doing this will tie up the processor; in a foreground/background environment, timed waits would be more desirable). No further data transfers take place, despite the occurrence of numerous light pen interrupts, until the buffer flag is again cleared to zero. This permits the program to process the data before it is destroyed by another interrupt.

The buffer structure looks like this:

Buffer Flag
Name
Subpicture Tag
Display Program Counter (DPC)
Display Status Register (DSR)
X Status Register (XSR)
Y Status Register (YSR)

The Name value is the contents of the software Name Register (described in A.3.5) at the time of interrupt. The Tag value is the tag of the subpicture being displayed at the time of interrupt. The last four data items are the contents of the display processor status registers at the time of interrupt. They are described in detail in Table A-1.

Macro Call: .LPEN baddr

where:

baddr is the address of the 7-word light pen status data buffer

Errors:

None.

If a .LPEN was already issued and a buffer specified, the new buffer address replaces the previous buffer address. Only one light pen buffer can be in use at a time.

Example:

#L.FILE
#L.BUF
L.BUF
LOOP

\$DISPLAY LFILE
\$SET UP LPEN BUFFER
\$TEST LBUF FLAG, WHICH
\$WILL BE SET NON-ZERO
\$ON LIGHT PEN HIT.

; PROCESS DATA IN LBUF HERE.

<table><tr><td rowspan="4"></td><td rowspan="3">CLR</td><td rowspan="3">LBUF</td><td>DATA IN LBUF</td></tr><tr><td>CLEAR THE BUFFER FLAG</td></tr><tr><td>PERMITTING ANOTHER &quot;HIT&quot;</td></tr><tr><td>BR</td><td>LOOP</td><td>GO WAIT FOR IT</td></tr><tr><td>LBUF:</td><td>BLKW</td><td>7</td><td>SEVEN WORD LPEN BUFFER</td></tr><tr><td>LFILE:</td><td></td><td></td><td></td></tr></table>

Table A-1: Description of Display Status Words

<table><tr><td>Bits</td><td>Significance</td></tr><tr><td colspan="2">Display Program Counter (DPC=172000)</td></tr><tr><td>0-15</td><td>Address of display processor program counter at time of interrupt.</td></tr><tr><td colspan="2">Display Status Register (DSR=172002)</td></tr><tr><td>0-1</td><td>Line Type</td></tr><tr><td>2</td><td>Spare</td></tr><tr><td>3</td><td>Blink</td></tr><tr><td>4</td><td>Italics</td></tr><tr><td>5</td><td>Edge Indicator</td></tr><tr><td>6</td><td>Shift Out</td></tr><tr><td>7</td><td>Light Pen Flag</td></tr><tr><td>8-10</td><td>Intensity</td></tr><tr><td>11-14</td><td>Mode</td></tr><tr><td>15</td><td>Stop Flag</td></tr><tr><td colspan="2">X Status Register (XSR=172004)</td></tr><tr><td>0-9</td><td>X Position</td></tr><tr><td>10-15</td><td>Graphplot Increment</td></tr><tr><td colspan="2">Y Status Register (YSR=172006)</td></tr><tr><td>0-9</td><td>Y Position</td></tr><tr><td>10-15</td><td>Character Register</td></tr></table>

## A.2.6 .NAME

The .NAME request has been added to the Version 03 and later Display File Handler. The contents of the name register are now stacked when a subpicture call is made. When a light pen interrupt occurs, the contents of the name register stack may be recovered if the user program has supplied the address of a buffer through the .NAME request.

The buffer must have a size equal to the stack depth (default is 10) plus one word for the flag. When the .NAME request is entered, the address of the buffer is passed to the Handler and the first word (the flag word) is cleared. When a light pen hit occurs, the stack's contents are transferred and the flag is set non-zero.

Macro Call: .NAME baddr

where:

baddr is the address of the name register buffer

Errors:

None.

If a .NAME request has been previously issued, the new buffer address replaces the previous buffer address.

## A.2.7 .REMOV

The .REMOV request removes the call to a user display file previously inserted in the handler's display file by the .INSRT request. All reference to the user file is removed, unlike the .BLANK request, which merely bypasses the call while leaving it intact.

Macro Call: .REMOV faddr

where:

faddr is the address of the display file to be removed

Errors:

No errors are returned. If the file address given cannot be found, the request is ignored.

## A.2.8 .RESTR

The .RESTR request restores a user display file that was previously blanked by a .BLANK request. It removes the by-pass of the call to the user file, so that the display processor once again cycles through the user file.

Macro Call: .RESTR faddr

where:

faddr is the address of the user file that is to be restored to view
Errors:

No errors are returned. If the file specified cannot be found, the request is ignored.

## A.2.9 .SCROL

This request is used to modify the appearance of the Display Monitor's text display. The .SCROL request permits the programmer to change the maximum line count, intensity and the position of the top line of text of the scroller. The request passes the address of a two-word buffer which contains the parameter specifications. The first byte is the line count, the second byte is the intensity, and the second word is the Y position. Line count, intensity and Y position must all be octal numbers. The intensity may be any number from 0 to 7, ranging from dimmest to brightest. (If an intensity of 0 is specified, the scroller text will be almost unnoticeable at a BRIGHTNESS knob setting less than one-half.) The scroller parameter change is temporary, since an .UNLNK or CTRL/C restores the previous values.

Macro Call: .SCROL baddr

where:

baddr is the address of the two-word scroll parameters buffer

Errors:

No errors are returned. No checking is done on the values of the parameters. A zero argument is interpreted to mean that the parameter value is not to be changed. A negative argument causes the default parameter value to be restored.

Example:

SCBUF: .BYTE 5 #DECREASE #LINES TO 5.
.BYTE 0 #LEAVE INTENSITY UNCHANGED.
.WORD 300 #TOP LINE AT Y=300.

## A.2.10 .START

The .START request starts the display processor if it was stopped by a .STOP directive. If the display processor is running, it is stopped first, then restarted. In either case, the subpicture stack is cleared and the display processor is started at the top of the handler's internal display file.

Macro Call: .START

Errors:
    None.

## A.2.11 .STAT

The .STAT request transfers the address of a seven-word status buffer to the display stop interrupt routine in VTBASE. Once the transfer has been made, display processor status data is transferred to the buffer by the display stop interrupt routine in VTBASE whenever a .DSTAT or .DHALT instruction is encountered (see Sections A.3.3 and A.3.4). The transfer is made only when the buffer flag is clear (zero). After the transfer is made, the buffer flag is set non-zero and the .DSTAT or .DHALT instruction is replaced by a .DNOP (Display NOP) instruction.

The status buffer must be a seven-word, contiguous block of memory. Its contents are the same as the light pen status buffer. For a detailed description of the buffer and an explanation of the status words, see Section A.2.5 and Table A-1.

Macro Call: .STAT baddr

where:

baddr is the address of the status buffer receiving the data

Errors:

No errors are indicated. If a buffer was previously set up, the new buffer address is replaced as the old buffer address.

## A.2.12 .STOP

The .STOP request “stops” the display processor. It actually effects a stop by preventing the DPU from cycling through any user display files. It is useful for stopping the display during modification of a display file, a risky task when the display processor is running. However, a .BLANK could be equally useful for this purpose, since the .BLANK request does not return until the display processor has been removed from the user display file being blanked.

Macro Call: .STOP

Errors:

None.

## NOTE

Since the display processor must cycle through the text buffer in the Display Monitor in order for console output to be processed, the text buffer remains visible after a .STOP request is processed, but all user files disappear.

## A.2.13 .SYNC/.NOSYN

The .SYNC and .NOSYN requests provide program access to the power line synchronization feature of the display processor. The .SYNC request enables synchronization and the .NOSYN request disables it (the default case).

Synchronization is achieved by stopping the display and restarting it when the power line frequency reaches a trigger point, e.g., a peak or zero-crossing. Synchronization has the effect of fixing the display refresh time. This may be useful in some cases where small amounts of material are displayed but the amount frequently changes, causing changes in intensity. In most cases, however, using synchronization increases flicker.

Macro Calls: .SYNC
.NOSYN

Errors:

None.

## A.2.14 .TRACK

The .TRACK request causes the tracking object to appear on the display CRT at the position specified in the request. The tracking object is a diamond-shaped display figure which is light-pen sensitive. If the light pen is placed over the tracking object and then moved, the tracking object follows the light pen, trying to center itself on the pen.

The tracking object first appears at a position specified in a two-word buffer whose address was supplied with the .TRACK request. As the tracking object moves to keep centered on the light pen, the new center position is returned to the buffer. A new set of X and Y values is returned for each light pen interrupt.

The tracking object cannot be lost by moving it off the visible portion of the display CRT. When the edge flag is set, indicating a side of the tracking object is crossing the edge of the display area, the tracking object stops until moved toward the center. To remove the tracking object from the screen, repeat the .TRACK request without arguments.

The .TRACK request may also include the address of a completion routine as the second argument. If a .TRACK completion routine is specified, the light pen interrupt handler passes control to the completion routine at interrupt level. The completion routine is called as a subroutine and the exit statement must be an RTS PC. The completion routine must also preserve any registers it may use.

Macro Call: .TRACK baddr, croutine

where:

baddr is the address of the two-word buffer containing the X and Y position for the track object

croutine is the address of the completion routine

Errors:

None.

Example:

See Section A.10.

## A.2.15 .UNLNK

The .UNLNK request is used before exiting from a program. In the case where the scroller is present, .UNLNK breaks the link, established by .LNKRT, between the Display File Handler's internal display file and the scroll file in the Display Monitor. The display processor is started cycling in the scroll text buffer, and no further graphics may be done until the link is established again. In the case where no scroller exists, the display processor is simply left stopped.

Macro Call: .UNLNK

Errors:

No errors are returned. An internal link flag is checked to determine if the link exists. If it does not exist, the request is ignored.

## A.3 Extended Display Instructions

The Display File Handler offers the assembly language graphics programmer an extended display processor instruction set, implemented in software through the use of the Load Status Register A (LSRA) instruction. The extended instruction set includes: subroutine call, subroutine return, display status return, display halt, and load name register.

## A.3.1 DJSR Subroutine Call Instruction

The DJSR instruction (octal code is 173400) simulates a display subroutine call instruction by using the display stop instruction (LSRA instruction with interrupt bits set). The display stop interrupt handler interprets the non-zero word following the DJSR as the subroutine return address, and the second word following the DJSR as the address of the subroutine to be called. The instruction sequence is:

DJSR
Return address
Subroutine address

Example:

To call a subroutine SQUARE:

POINT                      #POSITION BEAM
100                          #AT (100,100)
100
DJSR                          #THEN CALL SUBROUTINE
.+4
SQUARE                   #TO DRAW A SQUARE
DRET
0

The use of the return address preceding the subroutine address offers several advantages. For example, the BASIC-11 graphics software uses the return address to branch around subpicture tag data stored following the subpicture address. This structure is described in Section A.5.3. In addition, a subroutine may be temporarily bypassed by replacing the DJSR code with a DJMP instruction, without the need to stop the display processor to make the by-pass.

The address of the return address is stacked by the display stop interrupt handler on an internal subpicture stack. The stack depth is conditionalized and has a default depth of 10. If the stack bottom is reached, the display stop interrupt handler attempts to protect the system by rejecting additional subroutine calls. In that case, the portions of the display exceeding the legal stack depth will not be displayed.

## A.3.2 DRET Subroutine Return Instruction

The DRET instruction provides the means for returning from a display file subroutine. It uses the same octal code as DJSR, but with a single argument of zero. The DRET instruction causes the display stop interrupt handler to pop its subpicture stack and fetch the subroutine return address.

```csv
SQUARE: LONGV ;DRAW A SQUARE
100!INTX
0
0!INTX
100
100!INTX!MINUSX
0
0!INTX
100!MINUSX
DRET ;RETURN FROM SUBPICTURE
0
```

## A.3.3 DSTAT Display Status Instruction

The DSTAT instruction (octal code is 173420) uses the LSRA instruction to produce a display stop interrupt, causing the display stop interrupt handler to return display status data to a seven-word user status buffer. The status buffer must first have been set up with a .STAT macro call (if not, the DSTAT is ignored and the display is resumed). The first word of the buffer is set non-zero to indicate the transfer has taken place, and the DSTAT is replaced with a DNOP (display NOP). The first word is the buffer flag and the next six words contain name register contents, current subpicture tag, display program counter, display status register, display X register, and display Y register. After transfer of status data, the display is resumed.

## A.3.4 DHALT Display Halt Instruction

The DHALT instruction (octal code is 173500) operates similarly to the DSTAT instruction. The difference between the two instructions is that the DHALT instruction leaves the display processor stopped when exiting from the interrupt. A status data transfer takes place provided the buffer was initialized with a .STAT call. If not, the DHALT is ignored.

Example:

```asm
. STAT      #SBUF          ;INIT BUFFER
MOV         #DHALT,STPLOC   ;INSERT DHALT
.INSRT     #DFILE          ;DISPLAY THE PICTURE
TST        SBUF          ;DHALT PROCESSED?
BEQ         1$           ;NO, WAIT
.
.
SBUF:      .BLKW 7                  ;STATUS BUFFER
DFILE: POINT            ;POSITION NEAR TOP OF 12" TUBE
.WORD       500,1350
LONGV
.WORD       0,400          ;DRAW A LINE, MAYBE OVER EDGE
STPLOC: DNOP             ;IF IT IS A 12" SCOPE.
DRET
O
```

## A.3.5 DNAME Load Name Register Instruction

The Display File Handler provides a name register capability through the use of the display stop interrupt. When a DNAME instruction (octal code is 173520) is encountered, a display stop interrupt is generated. The display stop handler stores the argument following the DNAME instruction in an internal software register called the “name register.” The current name register contents are returned whenever a DSTAT or DHALT is encountered, and more importantly, whenever a light pen interrupt occurs. The use of a “name” (with a valid range from 1 to 77777) enables the programmer to label each element of the display file with a unique name, permitting the easy identification of the particular display element selected by the light pen.

The name register contents are stacked on a subpicture call and restored on return from the subpicture.

## Example:

The SQUARE subroutine with "named" sides.

SQUARE: DNAME ;NAME IS
10 ;10
LONGV ;DRAW A SIDE
100!INTX
0
DNAME ;THIS SIDE IS NAMED
11 ;11
0!INTX ;STILL IS LONG VECTOR MODE
100
DNAME
12
100!INTX!MINUSX
0
DNAME
13
0!INTX
100!MINUSX
DRET ;RETURN FROM SUBPICTURE
0

## A.4 Using the Display File Handler

Graphics programs which intend to use the Display File Handler for display processor management can be written in MACRO assembly language. The display code portions of the program may use the mnemonics described in Section A.7. Calls to the Handler should have the format described in Section A.6.

The Display File Handler is supplied in two pieces, a file of MACRO definitions and a library containing the Display File Handler modules.

MACRO Definition File: VTMAC.MAC

| Display File Handler: | VTLIB.OBJ | (consisting of:) |
| --- | --- | --- |
|  |  | VTBASE.OBJ |
|  |  | VTCAL1.OBJ |
|  |  | VTCAL2.OBJ |
|  |  | VTCAL3.OBJ |
|  |  | VTCAL4.OBJ |

## A.4.1 Assembling Graphics Programs

To assemble a graphics program using the display processor mnemonics or the Display Handler macro calls, the file VTMAC.MAC must be assembled with the program, and must precede the program in the assembler command string.

## Example:

Assume PICTUR.MAC is a user graphics program to be assembled. An assembler command string would look like this:

MACRO VTMAC+PICTUR/OBJECT

## A.4.2 Linking Graphics Programs

Once assembled with VTMAC, the graphics program must be linked with the Display File Handler, which is supplied as a single concatenated object module, VTHDLR.OBJ. The Handler may optionally be built as a library, following the directions in A.8.5. The advantage of using the library when linking is that the Linker will select from the library only those modules actually used. Linking with VTHDLR.OBJ results in all modules being included in the link.

To link a user program called PICTUR.OBJ using the concatenated object module supplied with RT-11:

LINK PICTUR, VTHOLR

To link a program called PICTUR.OBJ using the VTLIB library built by following the directions in A.8.5, be sure to use the Version 03 Linker:

LINK PICTUR, VTLIB

VTLIB (Handler Modules):

<table><tr><td>Module</td><td>CSECT</td><td>Contains</td><td>Globals</td></tr><tr><td rowspan="5">VTCAL1</td><td rowspan="2">$GT1</td><td>.CLEAR</td><td>$VINIT</td></tr><tr><td>.START</td><td>$VSTRT</td></tr><tr><td rowspan="3">.STOP</td><td>$VSTOP</td><td></td></tr><tr><td>.INSRT</td><td>$VNSRT</td></tr><tr><td>.REMOV</td><td>$VRMOV</td></tr><tr><td rowspan="2">VTCAL2</td><td rowspan="2">$GT2</td><td>.BLANK</td><td>$VBLNK</td></tr><tr><td>.RESTR</td><td>$VRSTR</td></tr><tr><td rowspan="6">VTCAL3</td><td rowspan="6">$GT3</td><td>.LPEN</td><td>$VLPEN</td></tr><tr><td>.NAME</td><td>$NAME</td></tr><tr><td>.STAT</td><td>$VSTPM</td></tr><tr><td>.SYNC</td><td>$SYNC</td></tr><tr><td>.NOSYN</td><td>$NOSYN</td></tr><tr><td>.TRACK</td><td>$VTRAK</td></tr><tr><td rowspan="3">VTCAL4</td><td rowspan="3">$GT4</td><td>.LNKRT</td><td>$VRTLK</td></tr><tr><td>.UNLNK</td><td>$VUNLK</td></tr><tr><td>.SCROL</td><td>$VSCRL</td></tr><tr><td>VTBASE</td><td>$GTB</td><td>Interrupt handlers and internal display file</td><td>$DFILE</td></tr></table>

The file modules in VTHDLR can be used in three different ways. When space is not critical, the most straightforward way is to link VTHDLR directly with a display program. The following command is an example.

## LINK PICTUR, VTHOLR

It is often necessary to conserve space, however, and selective loading of modules is possible by first creating an indexed object module library from VTHDLR and then by making global calls within the display program. The following command creates an indexed object module library.

## LIBRARY/CREATE VTLIB VTHDLR

To further conserve space with overlays, it is also possible to extract individual object modules from a library and create separate object module files. For example, to link a display program using overlays, the following statements are a typical sequence of creating, extracting and linking commands. (NOTE: the modules VTCAL1 and VTCAL2 must be in the same overlay if any global in either one is used.)

.
.
.
.LIBRARY/CREATE VTLIB VTHDLR
.
.
.
.LIBRARY/EXTRACT VTLIB VTCAL1
GLOBAL? \$VSTRT !moves entire module with \$VSTRT to VTCAL1
GLOBAL? !Terminates prompting sequence
.LIBRARY/EXTRACT VTLIB VTCAL2
GLOBAL? \$VBLNK !Moves the entire module to VTCAL2
GLOBAL?
.LIBRARY/EXTRACT VTLIB VTCAL3
GLOBAL? \$VLPEN !Moves the entire module
GLOBAL?
.LIBRARY/EXTRACT VTLIB VTCAL4
GLOBAL? \$VRTLK !Moves the entire module
GLOBAL?
.LIBRARY/EXTRACT VTLIB VTBASE
GLOBAL? \$DFILE !Moves the entire module
GLOBAL?
.
.
.
.LINK/PROMPT PICTUR,VTBASE
\*VTCAL1,VTCAL2,VTCAL3/0:1
\*VTCAL4/0:1
\*//

## A.5 Display File Structure

The Display File Handler supports a variety of display file structures, takes over the job of display processor management for the programmer, and may be used for both assembly language graphics programming and for systems program development. For example, the Handler supports the tagged subpicture file structure used by the BASIC-11 graphics software, as well as simple file structures. These are discussed in this section.

## A.5.1 Subroutine Calls

A subroutine call instruction, with the mnemonic DJSR, is implemented using the display stop (DSTOP) instruction with an interrupt. The display stop interrupt routine in the Display File Handler simulates the DJSR instruction, and this allows great flexibility in choosing the characteristics of the DJSR instruction.

The DJSR instruction stops the display processor and requests an interrupt. The DJSR instruction may be followed by two or more words, and in this implementation the exact number may be varied by the programmer at any time. The basic subroutine call has this form:

DJSR
Return Address
Subroutine Address

In practice, simple calls to subroutines could look like:
    DJSR
    .WORD      +4
    .WORD      SUB

where SUB is the address of the subroutine. Control will return to the display instruction following the last word of the subroutine call. This structure permits a call to the subroutine to be easily by-passed without stopping the display processor, by replacing the DJSR with a display jump (DJMP) instruction:

```asm
DJMF
.WORD          .+4
.WORD          SUB
```

A more complex display file structure is possible if the return address is generalized:

```txt
• IJSR
• WORD NEXT
• WORD SUB
```

where NEXT is the generalized return address. This is equivalent to the sequence:

DJSR
.WORD          .+4
.WORD          SUB
DJMP
.WORD          NEXT

It is also possible to store non-graphic data such as tags and pointers in the subroutine call sequence, such as is done in the tagged subpicture display file structure of the BASIC-11 graphics software. This technique looks like:

        DJSR
        .WORD     NEXT
        .WORD     SUB
      DATA
NEXT:    .
          .
          .

For simple applications where the flexibility of the DJSR instruction described above is not needed and the resultant overhead is not desired, the

Display File Handler (VTBASE.MAC and VTCALL.MAC) can be conditionally re-assembled to produce a simple DJSR call. If NOTAG is defined during the assembly, the Handler will be configured to support this simple DJSR call:

```txt
DJSR
.WORD SUB
```

where SUB is the address of the subroutine. Defining NOTAG will eliminate the subpicture tag capability, and with it the tracking object, which uses the tag feature to identify itself to the light pen interrupt handler.

Whatever the DJSR format used, all subroutines and the user main file must be terminated with a subroutine return instruction. This is implemented as a display stop instruction (given the mnemonic DRET) with an argument of zero. A subroutine then has the form:

```txt
SUB:      Display Code
        DRET
        .WORD 0
```

## A.5.2 Main File/Subroutine Structure

A common method of structuring display files is to have a main file which calls a series of display subroutines. Each subroutine will produce a picture element and may be called many times to build up a picture, producing economy of code. If the following macros are defined:

.MACRO     CALL &lt;ARG&gt;
DJSR
.WORD       .+4
.WORD       ARG
.ENDM
.MACRO     RETURN
DRET
.WORD       0
.ENDM

then a main file/subroutine file structure would look like:

;MAIN DISPLAY FILE
;
MAIN:      Display Code
        CALL SUB1     ;CALL SUBROUTINE 1
        Display Code
        CALL SUB2     ;CALL SUBROUTINE 2
          .                 ;ETC
          .
          .

;DISPLAY SUBROUTINES
;
SUB1: Display Code ;SUBROUTINE 1
RETURN
;
SUB2: Display Code ;SUBROUTINE 2
RETURN
:
;
ETC.

## A.5.3 BASIC-11 Graphic Software Subroutine Structure

An example of another method of structuring display files is the tagged sub-picture structure used by BASIC-11 graphic software. The display file is divided into distinguishable elements called subpictures, each of which has its own unique tag.

The subpicture is constructed as a subroutine call followed by the subroutine. It is essentially a merger of the main file/subroutine structure into an in-line sequence of calls and subroutines. As such, it facilitates the construction of display files in real time, one of the important advantages of BASIC-11 graphic software.

The following is an example of the subpicture structure. Each subpicture has a call to a subroutine with the return address set to be the address of the next subpicture. The subroutine called may either immediately follow the call, or may be a subroutine defined as part of a subpicture created earlier in the display file. This permits a subroutine to be used by several subpictures without duplication of code. Each subpicture has a tag to identify it, and it is this tag which is returned by the light pen interrupt routine. To facilitate finding subpictures in the display file, they are made into a linked list by inserting a forward pointer to the next tag.

SUB1:       DJSR                  ;START OF SUBPICTURE 1
        .WORD      SUB2          ;NEXT SUBPICTURE
        .WORD      SUB1+12   ;JUMP TO THIS SUBPICTURE
        .WORD      1           ;TAG = 1
        .WORD      SUB2+6   ;POINTER TO NEXT TAG

BODY OF SUBPICTURE 1

DRET
O

SUB2:        DJSR
            .WORD      SUB3
            .WORD      SUB2+12
            .WORD      2
            .WORD      SUB3+6
;BODY OF SUBPICTURE 2

\*RETURN FROM
\*SUBPICTURE 1

\$START SUBPICTURE 2
\$NEXT SUBPICTURE
\$JUMP TO THIS SUBPICTURE
\$TAG 2
\$PTR TO NEXT TAG

DRET
•WORD    O \$RETURN FROM
\$SUBPICTURE 2

SUB3:        DJSR
        .WORD      SUB4
        .WORD      SUB1+12

.WORD          3
.WORD          SUB4+6;START SUBPICTURE 3
;NEXT SUBPICTURE
;COPY SUBPICTURE 1
;FOR THIS SUBPICTURE
;BUT TAG IT 3.
;PTR TO NEXT TAG

SUB4: DIJSR
    :
    :
    :

;START SUBPICTURE 4
;ETC.

## A.6 Summary of Graphics MACRO Calls

| Mnemonic | Function | MACRO Call(see Note 1) | Assembly Language Expansion(see Note 2) |
| --- | --- | --- | --- |
| .BLANK | Temporarily blanks a user display file. | .BLANK faddr | .GLOBL $VBLNK.IF NB, faddrMOV faddr, ^100.ENDCJSR ^O7, $VBLNK |
| .CLEAR | Initializes handler. | .CLEAR | .GLOBL $VINITJSR ^O7, $VINIT |
| .INSRT | Inserts a call to user display file in handler's master display file. | .INSRT faddr | .GLOBL $VNSRT.IF NB, faddrMOV faddr, ^O0.ENDCJSR ^O7, $VNSRT |
| .LNKRT | Sets up vectors and links display file handler to RT-11 scroller. | .LNKRT | .GLOBL $VRTLKJSR ^O7, $VRTLK |
| .LPEN | Sets up light pen status buffer. | .LPEN baddr | .GLOBL $VLPEN.IF NB, baddrMOV baddr, ^O0.ENDCJSR ^O7, $VLPEN |
| .NAME | Sets up buffer to receive name register stack contents. | .\\NAME \\baddr | .GLOBL $NAME.IF NB, baddrMOV .BEDDR, ^O0.ENDCJSR ^O7, $NAME |
| .NOSYN | Disables power line synchronization. | .NOSYN | .GLOBL $NOSYNJSR ^O7, $NOSYN |
| .REMOV | Removes the call to a user display file. | .REMOV faddr | .GLOBL $VRMOV.IF NB, faddrMOV faddr, ^O0.ENDCJSR ^O7, $VRMOV |
| .RESTR | Unblanks the user display file. | .RESTR faddr | .GLOBL $VRSTRIF NB, faddrMOV faddr, ^O0ENDCJSR ^O7, $VRSTR |
| .SCROL | Adjusts monitor scroller parameters. | .SCROL baddr | .GLOBL $VSCRL.IF NB, baddrMOV baddr, ^O0.ENDCJSR ^O7, $VSCRL |
| .START | Starts the display. | .START | .GLOBL $VSTRTJSR ^07, $VSTRT |
| .STAT | Sets up status buffer. | .STAT baddr | .GLOBL $VSTPM.IF NB, baddrMOV baddr, ^00.ENDCJSR ^07, $VSTPM |
| .STOP | Stops the display. | .STOP | .GLOBL $VSTOPJSR ^07, $VSTOP |
| .SYNC | Enables power line synchronization. | .SYNC | .GLOBL $SYNCJSR ^07, $SYNC |
| .TRACK | Enables the track object. | .TRACK baddr, croutine | .GLOBL $VTRAKIF NB, baddrMOV baddr, ^00.ENDC.IF NB, croutineMOV croutine,-(`06).IFFCLR-(`06).ENDC.NARG T.IF EQ, TCLR ^00.ENDCJSR ^07, $VTRAK |
| .UNLNK | Unlinks display handler from RT-11 if linked (otherwise leaves display stopped). | .UNLNK | .GLOBL $VUNLKJSR ^07, $VUNLK |

## NOTE 1

baddr Address of data buffer.

faddr Address of start of user display file.

croutine Address of .TRACK completion routine.

## NOTE 2

The lines preceded by a dot will not be assembled. The code they enclose may or may not be assembled depending on the conditionals.

## A.7 Display Processor Mnemonics

<table><tr><td>Mnemonic</td><td></td><td>Value</td><td>Function</td></tr><tr><td>CHAR</td><td>-</td><td>100000</td><td>Character Mode</td></tr><tr><td>SHORTV</td><td>=</td><td>104000</td><td>Short Vector Mode</td></tr><tr><td>LONGV</td><td>-</td><td>110000</td><td>Long Vector Mode</td></tr><tr><td>POINT</td><td>-</td><td>114000</td><td>Point Mode</td></tr><tr><td>GRAPHX</td><td>-</td><td>120000</td><td>Graphplot X Mode</td></tr><tr><td>GRAPHY</td><td>-</td><td>124000</td><td>Graphplot Y Mode</td></tr><tr><td>RELATV</td><td>-</td><td>130000</td><td>Relative Point Mode</td></tr><tr><td>INT0</td><td>-</td><td>2000</td><td>Intensity 0 (Dim)</td></tr><tr><td>INT1</td><td>-</td><td>2200</td><td>Intensity 1</td></tr><tr><td>INT2</td><td>-</td><td>2400</td><td>Intensity 2</td></tr><tr><td>INT3</td><td>-</td><td>2600</td><td>Intensity 3</td></tr><tr><td>INT4</td><td>-</td><td>3000</td><td>Intensity 4</td></tr><tr><td>INT5</td><td>-</td><td>3200</td><td>Intensity 5</td></tr><tr><td>INT6</td><td>-</td><td>3400</td><td>Intensity 6</td></tr><tr><td>INT7</td><td>-</td><td>3600</td><td>Intensity 7 (Bright)</td></tr><tr><td>LPOFF</td><td>-</td><td>100</td><td>Light Pen Off</td></tr><tr><td>LPON</td><td>-</td><td>140</td><td>Light Pen On</td></tr><tr><td>BLKOFF</td><td>-</td><td>20</td><td>Blink Off</td></tr><tr><td>BLKON</td><td>-</td><td>30</td><td>Blink On</td></tr><tr><td>LINE0</td><td>-</td><td>4</td><td>Solid Line</td></tr><tr><td>LINE1</td><td>-</td><td>5</td><td>Long Dash</td></tr><tr><td>LINE2</td><td>-</td><td>6</td><td>Short Dash</td></tr><tr><td>LINE3</td><td>-</td><td>7</td><td>Dot Dash</td></tr><tr><td>DJMP</td><td>-</td><td>160000</td><td>Display Jump</td></tr><tr><td>DNOP</td><td>-</td><td>164000</td><td>Display No Operation</td></tr><tr><td>STATSA</td><td>-</td><td>170000</td><td>Load Status A Instruction</td></tr><tr><td>LPLITE</td><td>-</td><td>200</td><td>Light Pen Hit On</td></tr><tr><td>LPDARK</td><td>-</td><td>300</td><td>Light Pen Hit Off</td></tr><tr><td>ITAL0</td><td>-</td><td>40</td><td>Italics Off</td></tr><tr><td>ITAL1</td><td>-</td><td>60</td><td>Italics On</td></tr><tr><td>SYNC</td><td>-</td><td>4</td><td>Halt and Resume Synchronized</td></tr><tr><td>STATSB</td><td>-</td><td>174000</td><td>Load Status B Instruction</td></tr><tr><td>INCR</td><td>-</td><td>100</td><td>Graphplot Increment</td></tr><tr><td colspan="4">Vector/Point Mode</td></tr><tr><td>INTX</td><td>-</td><td>40000</td><td>Intensity Vector or Point</td></tr><tr><td>MAXX</td><td>-</td><td>1777</td><td>Maximum X Component</td></tr><tr><td>MAXY</td><td>-</td><td>1377</td><td>Maximum Y Component</td></tr><tr><td>MINUSX</td><td>-</td><td>20000</td><td>Negative X Component</td></tr><tr><td>MINUSY</td><td>-</td><td>20000</td><td>Negative Y Component</td></tr><tr><td colspan="2">Mnemonic</td><td>Value</td><td>Function</td></tr><tr><td colspan="2">Short Vector Mode</td><td></td><td></td></tr><tr><td>SHIFTX</td><td>=</td><td>200</td><td></td></tr><tr><td>MAXSX</td><td>=</td><td>17600</td><td>Maximum X Component</td></tr><tr><td>MAXSY</td><td>=</td><td>77</td><td>Maximum Y Component</td></tr><tr><td>MISVX</td><td>=</td><td>20000</td><td>Negative X Component</td></tr><tr><td>MISVY</td><td>=</td><td>100</td><td>Negative Y Component</td></tr></table>

## A.8 Assembly Instructions

## A.8.1 General Instructions

All programs can be assembled in 16K, using RT-11 MACRO. All assemblies and all links should be error free. The following conventions are assumed:

Default file types are not explicitly typed. These are .MAC for source files, .OBJ for assembler output, and .SAV for Linker output.

2. The default device (DK) is used for all files in the example command strings.

3. Listings and link maps are not generated in the example command strings.

## A.8.2 VTBASE

To assemble VTBASE with RT-11 link-up capability.
MACRO VTBASE

## A.8.3 VTCAL1 - VTCAL4

To assemble the modules VTCAL1 through VTCAL4:
MACRO VTCAL1, VTCAL2, VTCAL3, VTCAL4

## A.8.4 VTHDLR

To create the concatenated handler module:
COPY/BINARY VTCAL1.OBJ, VTCAL2.OBJ, VTCAL3.OBJ,
VTCAL4.OBJ, VTBASE.OBJ VTHDLR.OBJ

## A.8.5 Building VTLIB.OBJ

To build the VTLIB library:
LIBRARY/CREATE VTLIB VTHDLR

## A.9 VTMAC

.TITLE VTMAC
; THIS SOFTWARE IS FURNISHED UNDER A LICENSE AND MAY ONLY BE USED
; OR COPIED IN ACCORDANCE WITH THE TERMS OF SUCH LICENSE.
;
; COPYRIGHT (C) 1978, DIGITAL EQUIPMENT CORPORATION.
;
; VTMAC IS A LIBRARY OF MACRO CALLS AND MNEMONIC DEFINITIONS WHICH
; PROVIDE SUPPORT OF THE VT11 DISPLAY PROCESSOR. THE MACROS PRODUCE
; CALLS TO THE VT11 DEVICE SUPPORT PACKAGE, USING GLOBAL REFERENCES.

; MACRO TO GENERATE A MACRO WITH ZERO ARGUMENTS.
.MACRO MACO NAME,CALL
.MACRO NAME
.GLOBL CALL
JSR PC,CALL
.ENDM

## ; MACRO TO GENERATE A MACRO WITH ONE ARGUMENT

.MACRO MAC1 NAME,CALL
    .MACRO NAME ARG
    .IF NB,ARG
    MOV     ARG,%^00
    .ENDC
    .GLOBL CALL
    JSR      FC,CALL
    .ENDM

## ; MACRO TO GENERATE A MACRO WITH TWO OPTIONAL ARGUMENTS

.MACRO MAC2 NAME, CALL
    .MACRO NAME ARG1,ARG2
    .GLOBL CALL
    .IF NB,ARG1

MOV        ARG1, %^00
.ENDC
.IF NB,ARG2
MOV        ARG2, -(SP)
.IFF
CLR       -(SP)
.NARG     T
.IF EQ,T
CLR       %^00
.ENDC
.ENDC
JSR       PC,CALL
.ENDM

## ; MACRO LIBRARY FOR VT11:

MAC0     <.CLEAR>,<\$VINIT>
MAC0     <.STOP>,<\$VSTOP>
MAC0     <.START>,<\$VSTRT>
MAC1     <.INSRT>,<\$VNSRT>
MAC1     <.REMOV>,<\$VRMOV>
MAC1     <.BLANK>,<\$VBLNK>
MAC1     <.RESTR>,<\$VRSTR>
MAC1     <.STAT>,<\$VSTPM>
MAC1     <.LPEN>,<\$VLPEN>

```txt
MAC1     <.SCROL>,<$VSCRL>
MAC2     <.TRACK>,<$VTRAK>
MAC0     <.LNKRT>,<$VRTLK>
MAC0     <.UNLNK>,<$VUNLK>

; MNEMONIC DEFINITIONS FOR THE VT11 DISPLAY PROCESSOR

DJMP=160000          ;DISPLAY JUMP
DNOP=164000          ;DISPLAY NOP
DJSR=173400          ;DISPLAY SUBROUTINE CALL
DRET=173400          ;DISPLAY SUBROUTINE RETURN
DNAME=173520          ;SET NAME REGISTER
DSTAT=173420          ;RETURN STATUS DATA
DHALT=173500          ;STOP DISPLAY AND RETURN STATUS DATA

CHAR=100000          ;CHARACTER .MODE
SHORTV=104000          ;SHORT VECTOR MODE
LONGV=110000          ;LONG VECTOR MODE
POINT=114000          ;POINT MODE
GRAPHX=120000          ;GRAPH X MODE
GRAPHY=124000          ;GRAPH Y MODE
RELATV=130000          ;RELATIVE VECTOR MODE

INTO=2000            ;INTENSITY O
INT1=2200
INT2=2400
INT3=2600
INT4=3000
INT5=3200
INT6=3400
INT7=3600

LPOFF=100           ;LIGHT PEN OFF
LPON=140           ;LIGHT PEN ON
BLKOFF=20           ;BLINK OFF
BLKON=30           ;BLINK ON
LINE0=4           ;SOLID LINE
LINE1=5           ;LONG DASH
LINE2=6           ;SHORT DASH
LINE3=7           ;DOT DASH

STATSA=170000      ;LOAD STATUS REG A
LPLITE=200       ;INTENSIFY ON LPEN HIT
LPDARK=300       ;DON'T INTENSIFY
ITAL0=40           ;ITALICS OFF
ITAL1=60           ;ITALICS ON
SYNC=4               ;POWER LINE SYNC

STATSB=174000      ;LOAD STATUS REG B
INCR=100             ;GRAPH PLOT INCREMENT
INTX=40000       ;INTENSIFY VECTOR OR POINT
MAXX=1777           ;MAXIMUM X INCR. = LONGV
MAXY=1377           ;MAXIMUM Y INCR. = LONGV
MINUSX=20000       ;NEGATIVE X INCREMENT
MINUSY=20000       ;NEGATIVE Y INCREMENT
MAXSX=17600         ;MAXIMUM X INCR. = SHORTV
MAXSY=77           ;MAXIMUM Y INCR. = SHORTV
MISVX=20000       ;NEGATIVE X INCR. = SHORTV
MISVY=100           ;NEGATIVE Y INCR. = SHORTV
```

<table><tr><td colspan="7">A.10 Examples Using GTON</td></tr><tr><td>EXAMPLE #1</td><td>MACRO X03.04 18-MAY-77</td><td>14:49:44</td><td>PAGE 5</td><td></td><td></td><td></td></tr><tr><td>1</td><td></td><td></td><td>-TITLE EXAMPLE #1</td><td></td><td></td><td></td></tr><tr><td>2</td><td></td><td></td><td>; THIS EXAMPLE USES THE .LPEN STATUS BUFFER AND THE</td><td></td><td></td><td></td></tr><tr><td>3</td><td></td><td></td><td>; NAME REGISTER TO MODIFY A DISPLAY FILE WITH THE LIGHT PEN.</td><td></td><td></td><td></td></tr><tr><td>4</td><td></td><td></td><td>;</td><td></td><td></td><td></td></tr><tr><td>5</td><td></td><td></td><td>;</td><td></td><td></td><td></td></tr><tr><td>6</td><td>000000</td><td></td><td>R0=X0</td><td></td><td></td><td></td></tr><tr><td>7</td><td>000001</td><td></td><td>R1=X1</td><td></td><td></td><td></td></tr><tr><td>8</td><td>000007</td><td></td><td>PC=X7</td><td></td><td></td><td></td></tr><tr><td>9</td><td>000044</td><td></td><td>JSW=40</td><td></td><td></td><td>;JOB STATUS WORD</td></tr><tr><td>10</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>11</td><td></td><td></td><td>.MCALL</td><td>.TTINR,.EXIT,.PRINT</td><td></td><td></td></tr><tr><td>12</td><td>000000</td><td></td><td>.LNKRT</td><td></td><td></td><td>;LINK TO MONITOR</td></tr><tr><td>13</td><td>000004</td><td>100004</td><td>BPL</td><td>1$</td><td></td><td>;LINK UP ERROR?</td></tr><tr><td>14</td><td>000006</td><td></td><td>.PRINT</td><td>#EMSG</td><td></td><td>;YES, PRINT MESSAGE</td></tr><tr><td>15</td><td>000014</td><td></td><td>.EXIT</td><td></td><td></td><td>;AND EXIT.</td></tr><tr><td>16</td><td>000016</td><td></td><td>.SCPOL</td><td>#SCBUF</td><td></td><td>;ADJUST SCROLL</td></tr><tr><td>17</td><td>000026</td><td></td><td>.PRINT</td><td>#MSG</td><td></td><td></td></tr><tr><td>18</td><td>000034</td><td></td><td>.INSRT</td><td>#DFILE</td><td></td><td>;INSERT DISPLAY FILE</td></tr><tr><td>19</td><td>000044</td><td></td><td>.LPEN</td><td>#LBUF</td><td></td><td>;SET UP LPEN BUFFER</td></tr><tr><td>20</td><td>000054</td><td>052737</td><td>BIS</td><td>#100,@JSW</td><td></td><td>;SET JSW FOR TTINR</td></tr><tr><td>21</td><td>000062</td><td>005767</td><td>TST</td><td>LBUF</td><td></td><td>;LIGHT PEN HIT?</td></tr><tr><td>22</td><td>000066</td><td>001003</td><td>BNE</td><td>1$</td><td></td><td>;YES</td></tr><tr><td>23</td><td>000070</td><td></td><td></td><td>.TTINR</td><td></td><td>;NO, ANY TT INPUT?</td></tr><tr><td>24</td><td>000072</td><td>103023</td><td></td><td>BCC</td><td>EXIT</td><td>;YES, EXIT</td></tr><tr><td>25</td><td>000074</td><td>000772</td><td></td><td>BR</td><td>LTST</td><td>;NO, LOOP AGAIN</td></tr><tr><td>26</td><td>000076</td><td>016777</td><td>000102</td><td>MOV</td><td>I2,@IPTR</td><td>;RESTOPE PREVIOUS CODE</td></tr><tr><td>27</td><td>000104</td><td>016701</td><td>000050</td><td>MOV</td><td>LBUF+2,R1</td><td>;GET NAME VALUE</td></tr><tr><td>28</td><td>000110</td><td>005301</td><td></td><td>DEC</td><td>R1</td><td>;SUBTRACT ONE</td></tr><tr><td>29</td><td>000112</td><td>006301</td><td></td><td>ASL</td><td>R1</td><td>;MULTIPLY BY TWO</td></tr><tr><td>30</td><td>000114</td><td>060701</td><td></td><td>ADD</td><td>PC,R1</td><td>;USE TO INDEX</td></tr><tr><td>31</td><td>000116</td><td>062701</td><td>000062</td><td>ADD</td><td>#DTABL=.,R1</td><td>;OFF TABLE DTABL.</td></tr><tr><td>32</td><td>000122</td><td>011167</td><td>000060</td><td>MOV</td><td>(R1),IPTR</td><td>;MOVE ADDR INTO IPTR</td></tr><tr><td>33</td><td>000126</td><td>016777</td><td>000042</td><td>MOV</td><td>I1,@IPTR</td><td>;MODIFY THAT CODE</td></tr><tr><td>34</td><td>000134</td><td>005067</td><td>000016</td><td>CLR</td><td>LBUF</td><td></td></tr><tr><td>35</td><td></td><td></td><td></td><td></td><td></td><td>;CLEAR BUFFER FLAG TO</td></tr><tr><td>36</td><td>000140</td><td>000750</td><td></td><td></td><td>BR</td><td>;ENABLE ANOTHER LP HIT.</td></tr><tr><td>37</td><td>000142</td><td>022700</td><td>000012</td><td>EXIT:</td><td>CMP</td><td>;LOOP AGAIN</td></tr><tr><td>38</td><td>000146</td><td>001345</td><td></td><td></td><td>BNE</td><td>;LINE FEED?</td></tr><tr><td>39</td><td>000150</td><td></td><td></td><td></td><td>.UNLNK</td><td>;NO, GET ANOTHER</td></tr><tr><td>40</td><td>000154</td><td></td><td></td><td></td><td>.EXEIT</td><td>;UNLINK FROM MONITOR</td></tr><tr><td>41</td><td>000156</td><td></td><td></td><td>LBUF:</td><td>BLKW</td><td>;LPEN STATUS BUFFER</td></tr><tr><td>42</td><td>000174</td><td>103370</td><td></td><td>I1:</td><td>.WORD</td><td>CHARINTSIBLKONILPON</td></tr><tr><td>43</td><td>000176</td><td>103160</td><td></td><td>I2:</td><td>.WORD</td><td>CHARINT4!BLKOFFILPON</td></tr></table>

| 44 | 000200 | 000252° | 000272° | 000312° | DTABL: | .WORD | D1,02,D3 | ;TABLE OF DISPLAY FILE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 45 |  |  |  |  |  |  |  | ;LOCATIONS TO BE MODIFIED |
| 46 | 000206 | 000252° |  |  | IPTR: | .WORD | D1 | ;PREVIOUS LOCATION MODIFIED |
| 47 | 000210 | 000002 |  |  | SCBUF: | .WORD | 2 | ;SCROLL LINE COUNT |
| 48 | 000212 | 000100 |  |  |  | .WORD | 1RAD | ;SCROLL TCP Y POS. |
| 49 | 000214 | 041 | 105 | 122 | EMSG: | .ASCIZ | /!ERROR!/ | ;ERROR MESSAGE |
|  | 000217 | 122 | 117 | 122 |  |  |  |  |
|  | 000222 | 041 | 000 |  |  |  |  |  |
| 50 |  |  |  |  | .EVEN |  |  |  |
| 51 | 000224 | 105 | 130 | 101 | MSG: | .ASCIZ | /EXAMPLE #1/ | ;I.D. MESSAGE |
|  | 000227 | 115 | 120 | 114 |  |  |  |  |
|  | 000232 | 105 | 040 | 043 |  |  |  |  |
|  | 000235 | 061 | 000 |  |  |  |  |  |
| 52 |  |  |  |  |  | .EVEN |  |  |

<table><tr><td colspan="3">78 000324 000000</td><td rowspan="2" colspan="3">0END START</td></tr><tr><td colspan="3">79 000000°</td></tr><tr><td colspan="6">EXAMPLE #1 MACRO X03.04 18-MAY-77 14:49:44 PAGE 5-2</td></tr><tr><td colspan="6">SYMBOL TABLE</td></tr><tr><td>D2 000272R</td><td>INTX = 040000</td><td>INT4 = 003000</td><td>ITAL1 = 000060</td><td>DFILE 000240R</td><td></td></tr><tr><td>EXIT 000142R</td><td>INT2 = 002400</td><td>LPON = 000140</td><td>LTST 000062R</td><td>INT7 = 003600</td><td></td></tr><tr><td>INT0 = 002000</td><td>LINE1 = 000005</td><td>MINUSX= 020000</td><td>INT5 = 003200</td><td>MAXY = 021377</td><td></td></tr><tr><td>MAXSX = 017600</td><td>DJMP = 160000</td><td>MINUSY= 020000</td><td>I2 000176R</td><td>SHORTV= 124000</td><td></td></tr><tr><td>D3 000312R</td><td>LONGV = 110000</td><td>POINT = 114000</td><td>IPTR 000206R</td><td>D1 000252R</td><td></td></tr><tr><td>MAXSY = 000077</td><td>LPDARK= 000300</td><td>EMSG 000214R</td><td>DSTAT = 173424</td><td>STATSA= 170000</td><td></td></tr><tr><td>MISVY = 000100</td><td>LINE2 = 000006</td><td>ITAL0 = 000040</td><td>SCRUF 000210R</td><td>STATSB= 174000</td><td></td></tr><tr><td>MSG 000224R</td><td>INT3 = 002600</td><td>I1 0001/4R</td><td>SYNC = 000004</td><td>$VSCRL= ***** G</td><td></td></tr><tr><td>INT1 = 002200</td><td>RELATV= 130000</td><td>$VLPEN= ***** G</td><td>INT6 = 003400</td><td>GRAPHX= 120000</td><td></td></tr><tr><td>BLKON = 000030</td><td>DRET = 173400</td><td>MLKOFF= 000020</td><td>JSW = 000044</td><td>GRAPHY= 124000</td><td></td></tr><tr><td>DHALT = 173500</td><td>LINE3 = 000007</td><td>DJSR = 173400</td><td>MAYX = 001777</td><td>$VASHT= ***** G</td><td></td></tr><tr><td>LINE0 = 170004</td><td>LBUF 200156R</td><td>$VRTLK= ***** G</td><td>START 000000R</td><td>LPCFF = 020100</td><td></td></tr><tr><td>CHAR = 100000</td><td>INCR = 000100</td><td>DNAME = 173520</td><td>$VINLK= ***** G</td><td>MISVX = 220000</td><td></td></tr><tr><td>DTABL 000200R</td><td>LPLITE= 000200</td><td>DNOP = 164000</td><td></td><td></td><td></td></tr><tr><td colspan="6">. ABS. 000003 000</td></tr><tr><td colspan="6">000326 001</td></tr><tr><td colspan="6">ERRORS DETECTED: 0</td></tr><tr><td colspan="6">VIRTUAL MEMORY USED: 3564 WORDS (14 PAGES)</td></tr><tr><td colspan="6">DYNAMIC MEMORY AVAILABLE FOR 64 PAGES</td></tr><tr><td colspan="6">.LP:=VTMAC.MANEX1</td></tr><tr><td colspan="6">EXAMPLE #2 MACRO X03.04 18-MAY-77 14:49:57 PAGE 5</td></tr><tr><td colspan="6">1 .TITLE EXAMPLE #2</td></tr><tr><td colspan="6">2 ; THIS EXAMPLE USES THE TRACKING OBJECT AND THE TRACK</td></tr><tr><td colspan="6">3 ; COMPLETION ROUTINE TO CAUSE A VECTOR TO FOLLOW</td></tr><tr><td colspan="6">4 ; THE LIGHT PEN FROM A SET POINT AT (500,500).</td></tr><tr><td colspan="6">5 ; R0:%0</td></tr><tr><td colspan="6">6 ; R1:%1</td></tr><tr><td colspan="6">7 ; SP:%6</td></tr><tr><td colspan="6">8 ; PC:%7</td></tr><tr><td colspan="6">9 ; .MCALL .EXIT,.TTYIN,.PRINT</td></tr><tr><td colspan="6">10 START: .LNKRT ;LINK TO MONITOR</td></tr><tr><td colspan="6">11 BPL 10 ;LINK UP ERROR?</td></tr></table>

<table><tr><td>14</td><td>000006</td><td></td><td></td><td></td><td>.PRINT #EMSG</td><td>;YES, INFORM USER</td></tr><tr><td>15</td><td>000014</td><td></td><td></td><td></td><td>.EXIT</td><td>;AND EXIT</td></tr><tr><td>16</td><td>000016</td><td></td><td></td><td>1$:</td><td>.INSRT #DFILE</td><td>;INSERT DISPLAY FILE</td></tr><tr><td>17</td><td>000026</td><td></td><td></td><td></td><td>.TRACK #IBUF,#TCCM</td><td>;DISPLAY TRACK OBJECT</td></tr><tr><td>18</td><td>000042</td><td>004767</td><td>000006</td><td></td><td>JSR PC,WAIT</td><td>;WAIT FOR &lt;CR&gt;</td></tr><tr><td>19</td><td>000046</td><td></td><td></td><td></td><td>.UNLNK</td><td></td></tr><tr><td>20</td><td>000052</td><td></td><td></td><td></td><td>.EXIT</td><td></td></tr><tr><td>21</td><td>000054</td><td></td><td></td><td>WAIT:</td><td>.TTYIN</td><td>;GFT CHAR, FROM TTY</td></tr><tr><td>22</td><td>000060</td><td>022700</td><td>000012</td><td></td><td>CMP #12,R0</td><td>;LINE FEED?</td></tr><tr><td>23</td><td>000064</td><td>001373</td><td></td><td></td><td>BNE WAIT</td><td>;NO, GET ANOTHER</td></tr><tr><td>24</td><td>000066</td><td>000207</td><td></td><td></td><td>RTS PC</td><td></td></tr><tr><td>25</td><td>000070</td><td>000500</td><td>000500</td><td>TBUF:</td><td>.WORD 500,500</td><td>;TRACK BUFFER INITED TO</td></tr><tr><td>26</td><td></td><td></td><td></td><td></td><td></td><td>;START TRACK AT (500,500)</td></tr><tr><td>27</td><td></td><td></td><td></td><td>;</td><td></td><td></td></tr><tr><td>28</td><td></td><td></td><td></td><td colspan="3">; TRACK COMPLETION ROUTINE ENTERED AT INTERRUPT LEVEL</td></tr><tr><td>29</td><td></td><td></td><td></td><td colspan="3">; FROM DISPLAY FILE HANDLER WITH DISPLAY STOPPED.</td></tr><tr><td>30</td><td></td><td></td><td></td><td colspan="3">; USED TO UPDATE DISPLAY FILE WITH DATA FROM TRUF.</td></tr><tr><td>31</td><td></td><td></td><td></td><td>;</td><td></td><td></td></tr><tr><td>32</td><td>000074</td><td>010146</td><td></td><td>TCOM:</td><td>MOV R1,(SP)</td><td>;SAVE R1</td></tr><tr><td>33</td><td>000076</td><td>016701</td><td>177766</td><td></td><td>MOV TBUF,R1</td><td>;NEW X</td></tr><tr><td>34</td><td>000102</td><td>166701</td><td>000052</td><td></td><td>SUB OX,R1</td><td>;NEW X = OLD X</td></tr><tr><td>35</td><td>000106</td><td>100003</td><td></td><td></td><td>BPL 1$</td><td>;POSITIVE DIFFERENCE?</td></tr><tr><td>36</td><td>000110</td><td>005401</td><td></td><td></td><td>NEG R1</td><td>;NO&#x27; SO MAKE POSITIVE</td></tr><tr><td>37</td><td>000112</td><td>052701</td><td>020000</td><td></td><td>BIS #MINUSX,R1</td><td>;BUT SET MINUS BIT</td></tr><tr><td>38</td><td>000116</td><td>052701</td><td>040000</td><td>1$:</td><td>BIS #INTX,R1</td><td>;ALSO SET INTENSIFY BIT</td></tr><tr><td>39</td><td>000122</td><td>010167</td><td>000040</td><td></td><td>MOV R1,DX</td><td>;THEN STORE IN DFILE.</td></tr><tr><td>40</td><td>000126</td><td>016701</td><td>177740</td><td></td><td>MOV TBUF+2,R1</td><td>;NEW Y</td></tr><tr><td>41</td><td>000132</td><td>166701</td><td>000024</td><td></td><td>SUB OY,R1</td><td>;NEW Y = OLD Y</td></tr><tr><td>42</td><td>000136</td><td>100003</td><td></td><td></td><td>BPL 2$</td><td>;POSITIVE DIFFERENCE?</td></tr><tr><td>43</td><td>000140</td><td>005401</td><td></td><td></td><td>NEG R1</td><td>;NO, SO MAKE POSITIVE</td></tr><tr><td>44</td><td>000142</td><td>052701</td><td>020000</td><td></td><td>BIS #MINUSX,R1</td><td>;AND SET MINUS BIT</td></tr><tr><td>45</td><td>000146</td><td>010167</td><td>000016</td><td>2$:</td><td>MOV R1,DY</td><td>;THEN STORE IN DFILE</td></tr><tr><td>46</td><td>000152</td><td>012601</td><td></td><td></td><td>MOV (SP)+,R1</td><td>;RESTORE R1</td></tr><tr><td>47</td><td>000154</td><td>000207</td><td></td><td></td><td>RTS PC</td><td>;EXIT FROM COMPLETION ROUTINE</td></tr><tr><td>48</td><td></td><td></td><td></td><td>;</td><td></td><td></td></tr><tr><td>49</td><td></td><td></td><td></td><td colspan="3">; DISPLAY FILE FOR EXAMPLE #2</td></tr><tr><td>50</td><td></td><td></td><td></td><td>;</td><td></td><td></td></tr><tr><td>51</td><td>000156</td><td>114000</td><td></td><td>UFILE:</td><td>POINT</td><td>;SET POINT AT</td></tr><tr><td>52</td><td>000160</td><td>000500</td><td></td><td>OX:</td><td>500</td><td></td></tr><tr><td>53</td><td>000162</td><td>000500</td><td></td><td>OY:</td><td>500</td><td>;(500,500)</td></tr><tr><td>54</td><td>000164</td><td>113000</td><td></td><td></td><td>LONGVIINT4</td><td>;DRAW A VECTOR</td></tr><tr><td>55</td><td>000166</td><td>000000</td><td></td><td>DX:</td><td>.WORD 0</td><td>;INITIALLY NOWHERE</td></tr><tr><td>56</td><td>000170</td><td>000000</td><td></td><td>DY:</td><td>.WORD 0</td><td></td></tr><tr><td>57</td><td>000172</td><td>173400</td><td></td><td></td><td>DRET</td><td>;DISPLAY FILE END</td></tr></table>

<table><tr><td colspan="8">EXAMPLE #2 MACRO X03.04 18-MAY-77 14:49:57 PAGE 5-1</td></tr><tr><td>58</td><td>000174</td><td>000000</td><td></td><td></td><td>0</td><td></td><td></td></tr><tr><td>59</td><td>000176</td><td>123</td><td>117</td><td>122</td><td>EMSG:</td><td>.ASCIZ /SORRY, THERE SEEMS TO BE A PROBLEM/</td><td></td></tr><tr><td></td><td>000201</td><td>122</td><td>131</td><td>054</td><td></td><td></td><td></td></tr><tr><td></td><td>000204</td><td>040</td><td>124</td><td>110</td><td></td><td></td><td></td></tr><tr><td></td><td>000207</td><td>105</td><td>122</td><td>105</td><td></td><td></td><td></td></tr><tr><td></td><td>000212</td><td>040</td><td>123</td><td>105</td><td></td><td></td><td></td></tr><tr><td></td><td>000215</td><td>105</td><td>115</td><td>123</td><td></td><td></td><td></td></tr><tr><td></td><td>000220</td><td>040</td><td>124</td><td>117</td><td></td><td></td><td></td></tr><tr><td></td><td>000223</td><td>040</td><td>102</td><td>105</td><td></td><td></td><td></td></tr><tr><td></td><td>000226</td><td>040</td><td>101</td><td>040</td><td></td><td></td><td></td></tr><tr><td></td><td>000231</td><td>120</td><td>122</td><td>117</td><td></td><td></td><td></td></tr><tr><td></td><td>000234</td><td>102</td><td>114</td><td>105</td><td></td><td></td><td></td></tr><tr><td></td><td>000237</td><td>115</td><td>000</td><td></td><td></td><td></td><td></td></tr><tr><td>60</td><td></td><td></td><td></td><td></td><td>.EVEN</td><td></td><td></td></tr><tr><td>61</td><td></td><td>000000°</td><td></td><td></td><td></td><td>.END START</td><td></td></tr><tr><td colspan="8">EXAMPLE #2 MACRO X03.04 18-MAY-77 14:49:57 PAGE 5-2 SYMBOL TABLE</td></tr><tr><td colspan="2">INT0 = 002000</td><td colspan="2">LONGV = 110000</td><td colspan="2">LPLITE= 000200</td><td>$VRTLK= ***** G</td><td>$VUNLK= ***** G</td></tr><tr><td colspan="2">MAXSX = 017600</td><td colspan="2">LPDARK= 000300</td><td colspan="2">WAIT 000054R</td><td>ONAME = 173528</td><td>DFILE 000156R</td></tr><tr><td colspan="2">MAXSY = 000077</td><td colspan="2">LINE2 = 000006</td><td colspan="2">$XTRAK= ***** G</td><td>DNUP = 164900</td><td>INT7 = 003600</td></tr><tr><td colspan="2">MISVY = 000100</td><td colspan="2">DX 000166R</td><td colspan="2">INT4 = 003000</td><td>ITAL1 = 000060</td><td>MAXY = 291377</td></tr><tr><td colspan="2">INT1 = 002200</td><td colspan="2">INT3 = 002600</td><td colspan="2">LPON = 000140</td><td>INTS = 003200</td><td>SHORTV= 194000</td></tr><tr><td colspan="2">BLKON = 000030</td><td colspan="2">RELATV= 130000</td><td colspan="2">MINUSX= 020000</td><td>DSTAT = 173420</td><td>STATSA= 172000</td></tr><tr><td colspan="2">DHALT = 173500</td><td colspan="2">TCOM 000074R</td><td colspan="2">MINUSY= 020000</td><td>SYNC = 000284</td><td>STATSE= 174400</td></tr><tr><td colspan="2">LINE0 = 000004</td><td colspan="2">DRET = 173400</td><td colspan="2">POINT = 114000</td><td>INT6 = 003400</td><td>GRAPHX= 121800</td></tr><tr><td colspan="2">CHAR = 100000</td><td colspan="2">LINE3 = 000007</td><td colspan="2">EMSG 000176R</td><td>MAXX = 001777</td><td>GRAPHY= 124300</td></tr><tr><td colspan="2">INTX = 040000</td><td colspan="2">DY 000170R</td><td colspan="2">ITAL0 = 000040</td><td>OX 000160R</td><td>$VNSXT= ***** G</td></tr><tr><td colspan="2">INT2 = 002400</td><td colspan="2">TBUF 000070R</td><td colspan="2">BLKOFF= 000120</td><td>START 000000R</td><td>LPOFF = 000120</td></tr><tr><td colspan="2">LINE1 = 000005</td><td colspan="2">INCR = 000100</td><td colspan="2">DJSP = 173400</td><td>CY 000162R</td><td>*MISVX = 028700</td></tr><tr><td colspan="2">DJMP = 160000</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td colspan="2">.ABS. 000000 000</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td colspan="2">.000242 001</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td colspan="8">ERRORS DETECTED: 0</td></tr><tr><td colspan="8">VIRTUAL MEMORY USED: 3717 WORDS (15 PAGES) DYNAMIC MEMORY AVAILABLE FOR 64 PAGES .LP:=VTMAC.MANEX2</td></tr></table>
