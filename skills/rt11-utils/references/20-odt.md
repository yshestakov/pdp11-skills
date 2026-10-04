# RT-11 System Utilities Manual: Part III, Ch.20 ODT on-line debugging technique: commands, breakpoints, single step, relocation registers, searches

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 20.1 Calling and Using ODT
- 20.2 Relocation
- 20.3 Commands and Functions
- 20.3.1 Printout Formats
- 20.3.2 Opening, Changing, and Closing Locations
- 20.3.3 Accessing General Registers 0–7
- 20.3.4 Accessing Internal Registers
- 20.3.5 Radix-50 Mode (X)
- 20.3.6 Breakpoints
- 20.3.7 Running the Program (r;G and r;P)
- 20.3.8 Single-Instruction Mode
- 20.3.9 Searches
- 20.3.10 Constant Register (r;C)
- 20.3.11 Memory Block Initialization (;F and ;I)
- 20.3.12 Calculating Offsets (r;O)
- 20.3.13 Relocation Register Commands
- 20.3.14 The Relocation Calculators, n! and nR
- 20.3.15 ODT Priority Level (\$P)
- 20.3.16 ASCII Input and Output (r;nA)
- 20.4 Programming Considerations
- 20.4.1 Using ODT with Foreground/Background Jobs
- 20.4.2 Functional Organization
- 20.4.3 Breakpoints
- 20.4.4 Searches
- 20.4.5 Terminal Interrupt
- 20.5 Error Detection

---

## Part III

# Debugging and Altering Programs

Part III of this manual consists of the following four topics: on-line debugging technique (ODT), object module patch program (PAT), save image patch program (SIPP), and source language patch program (SLP). The four programs that these chapters describe can help you debug programs, examine or change assembled programs, and patch source programs.

Chapter 18 describes ODT. This program aids you in debugging assembly language programs. With ODT, you can control your program's execution, examine locations in memory and alter their contents, and search the object program for specific words.

Chapter 19 describes PAT, which patches or updates code in a relocatable binary object module. PAT accepts a file containing corrections or additional instructions and applies these corrections and additions to the original object module.

Chapter 20 describes SIPP. You can use SIPP to examine or modify individual locations within programs linked with the RT-11 V04 or later linker. Using SIPP, you can also create an indirect command file that contains a patch and the commands necessary to install it.

Chapter 21 describes SLP. SLP provides an easy way to make changes to source files. This program can accept an indirect command file created by the DIFFERENCES/SLP:filespec command (or by specifying a SLP-filespec to SRCCOM) to make two source programs match.

(1)

# Chapter 20 On-Line Debugging Technique (ODT)

On-line debugging technique (ODT) is a program that aids in debugging assembly language programs. ODT performs the following tasks:

\- Prints the contents of any location for examination or alteration

\- Runs all or any portion of an object program using the breakpoint feature

\- Searches the object program for specific bit patterns

\- Searches the object program for words that reference a specific word

\- Calculates offsets for relative addresses

\- Fills a single word, block of words, byte, or block of bytes with a designated value

Make sure you have an assembly listing and a link map available for the program you want to debug with ODT. You can make minor corrections to the program on line during the debugging session, and you can then execute the program under the control of ODT to verify the corrections. If you need to make major changes, such as adding a missing subroutine, note them on the assembly listing and incorporate them in a new assembly.

See the RT-11 Software Support Manual for debugging the following routines and jobs: interrupt service routines, device handlers, multiterminal jobs, extended memory and virtual jobs.

## 20.1 Calling and Using ODT

ODT is supplied as a relocatable object module. You can link ODT with your program (using the RT-11 linker) for an absolute area in memory and load it with your program. When you link ODT with your program, it is a good idea to link ODT low in memory relative to the program. If you do link ODT high in memory, be sure that the buffer space for your program is contained within program bounds. Otherwise, if your program uses dynamic buffering, program execution may destroy ODT in memory. Figure 20-1 shows the relationship between ODT and the program MYPROG in memory.

To link ODT low in memory relative to your program, the program must declare a named p-sect by using the .PSECT directive. Since the linker orders blank p-sects below named p-sects in memory, your program should declare a named p-sect so that ODT will be linked lower in memory than your program.

For example, if you include the directive .PSECT MYPROG in the program MYPROG, the following command will cause the linker to link ODT low in memory relative to MYPROG, and create the executable module MYPROG.SAV:

. LINK/DEBUG/MAP:TT:MYPROG RET

Figure 20-1: Linking ODT with a Program.

[figure omitted]

Once loaded in memory with your program, ODT has three legal start or restart addresses. Use the lowest (O.ODT) for normal entry, retaining the current breakpoints. The next (O.ODT+2) is a restart address that clears all breakpoints and reinitializes ODT, thus saving the general registers and clearing the relocation registers. Use the last address (O.ODT+4) to reenter ODT. A reenter saves the processor status and general registers, and removes the breakpoint instructions from your program. ODT prints the bad entry (BE) error message. Breakpoints that were set are reset by the next ;G command. (;P is invalid after a BE message.) The ;G and ;P commands control program execution and are explained in Section 20.3.7.

The system uses as an absolute address the address of the entry point O.ODT shown in the linker load map.

## NOTE

If you link ODT with an overlay-structured file, it should reside in the root segment so that it will always be in memory. Remove all breakpoints from the current overlay segment before execution proceeds to another overlay segment. A breakpoint inserted in an overlay is destroyed if it is overlaid during program execution.

The following example links ODT low in memory relative to MYPROG, creating the executable module MYPROG.SAV. Running MYPROG causes ODT to start automatically.

```txt
LINK/MAP:TT:/DEBUG MYPROG
RT-11 LINK V08.00 Load Map Thursday 04-Nov-82 14:15 Page
MYPROG .SAV Title: ODT Ident: 05.00
Section Addr Size Global Value Global Value Global Value
.ABS. 000000 001000 = 256. words (RW,I,GBL,ABS,OVR)
$ODT$ 001000 006152 = 1589. words (RW,I,LCL,REL,CON)
0.ODT 001232
PROG 007152 002052 = 533. words (RW,I,LCL,REL,CON)
START 007152
Transfer address = 001232, High limit = 011222 = 2377. words
.
.R MYPROG
.ODT V05.00
*
```

The following example links MYPROG low in memory relative to ODT and specifies O.ODT as the transfer address. Running MYPROG causes ODT to start automatically. The advantage to this method is that MYPROG is loaded at its normal, execution-time address.

```asm
LINK/MAP:TT: MYPROG,ODT/TRANSFER
Transfer symbol? 0.0DT

RT-11 LINK V08.00 Load Map Thursday 04-Nov-82 14:15 Page 1
MYPROG .SAV Title: ODT Ident: 05.00

Section Addr Size Global Value Global Value Global Value
.ABS. 000000 001000 = 256. words (RW,I,GBL,ABS,OVR)
PROG 001000 002052 = 533. words (RW,I,LCL,REL,CON)
START 001000
$ODT$ 003052 006152 = 1589. words (RW,I,LCL,REL,CON)
0.0DT 003304

Transfer address = 003304, High limit = 011222 = 2377. words

.
R MYPROG
ODT ¥05.00
*
```

The following example is similar to the previous example, except that execution does not automatically begin with ODT. When you start the program (MYPROG in this case), you must specify the address of O.ODT as shown in the link map.

```csv
, LINK/MAP:TT: MYPROG,ODT
RT-11 LINK V08.00 Load Map Thursday 04-Nov-82 14:15
Page 1
MYPROG .SAV Title: ODT Ident: 05.00
Section Addr Size Global Value Global Value Global Value
, ABS. 000000 001000 = 256. words (RW,I,GBL,ABS,OVR)
PROG 001000 002052 = 533. words (RW,I,LCL,REL,CON)
START 001000
$ODT$ 003052 006152 = 1589. words (RW,I,LCL,REL,CON)
0.ODT 003304
Transfer address = 003304, High limit = 011222 = 2377. words
, GET MYPROG
, START 3304
ODT V05.00
*
```

The next example links ODT with a bottom address of 4000, then loads ODT.SAV and MYPROG.SAV into memory. As in the example above, when you start the program, you must specify the address of O.ODT as shown in the link map.

```asm
. LINK/MAP:TT: ODT/BOTTOM:4000
RT-11 LINK V08.00 Load Map Thursday 04-Nov-82 14:15
Page 1
ODT .SAV Title: ODT Ident: 05.00 /B:004000
Section Addr Size Global Value Global Value Global Value
. ABS. 000000 004000 = 1024. words (RW,I,GBL,ABS,DVR)
$ODT$ 004000 006152 = 1589. words (RW,I,LCL,REL,CON)
0.ODT 004232
Transfer address = 004232, High limit = 012150 = 2612. words
. GET ODT.SAV
. GET MYPROG.SAV
. START 004232
ODT V05.00
*
```

You can restart ODT by specifying O.ODT+2 as the start address. This reinitializes ODT and clears all breakpoints. For example:

```txt
. START 4234
*
```

You can reenter ODT by specifying O.ODT+4 as the start address. For example:

If ODT is waiting for a command, a CTRL/C from the keyboard calls the keyboard monitor. The monitor responds with a ^C on the terminal and waits for a command. (You can use the REENTER command to reenter ODT only if your program has set the reenter bit and ODT is linked high in memory relative to the program; otherwise, ODT is reentered at address O.ODT + 6.)

If you type CTRL/U during a search printout, the search terminates and ODT prints an asterisk.

## 20.2 Relocation

When the assembler produces a relocatable object module, the base address of the module is assumed to be location 000000. The addresses of all program locations, as shown in the assembly listing, are relative to this base address. After you link the module, many of the values and all of the addresses in the program will be incremented by a constant whose value is the actual absolute base address of the module after it has been relocated. This constant is called the relocation bias for the module. Since a linked program may contain several relocated modules, each with its own relocation bias, and since, in the process of debugging, these biases will have to be subtracted from absolute addresses continually in order to relate relocated code to assembly listings, ODT provides automatic relocation.

The basis of automatic relocation is the eight relocation registers, numbered 0 through 7. You can set them to the values of the relocation biases at different times during debugging. Obtain relocation biases by consulting the link map. Once you set a relocation register, ODT uses it to relate relative addresses to absolute addresses. For more information on the relocation process, see Chapter 11.

ODT evaluates a relocatable expression as a 16-bit, six-digit (octal) number. You can type an expression in any one of the three forms presented in Table 20-1. In this table, the symbol n stands for an integer in the range 0 to 7 inclusive, and the symbol k stands for an octal number up to six digits long, with a maximum value of 177777. If you type more than six digits, ODT takes the last six digits typed, truncated to the low-order 16 bits. The symbol k may be preceded by a minus sign, in which case its value is the two's complement of the number typed. For example:

| k (number typed) | Values |
| --- | --- |
| 1 | 000001 |
| -1 | 177777 |
| 400 | 000400 |
| -177730 | 000050 |
| 1234567 | 034567 |

Table 20-1: Forms of Relocatable Expressions (r)

| Form | Expression | Value of r |
| --- | --- | --- |
| A | k | The value of k. |
| B | n,k | The value of k plus the contents of relocation register n.(If the n part of this expression is greater than 7, ODT uses only the last octal digit of n.) |
| C | C or C,k or n,C or C,C | Whenever you type the letter C, ODT replaces C with the contents of a special register called the constant register. (This value has the same role as the k or n that it replaces. The constant register is designated by the symbol $C and may be set to any value, as indicated below.) |

Section 20.3.13 describes the relocation register commands in greater detail.

## 20.3 Commands and Functions

When ODT starts it indicates its readiness to accept commands by printing an asterisk at the left margin of the terminal. You can issue most of the ODT commands in response to the asterisk. You can examine a word and change it; you can run the object program in its entirety or in segments; you can search memory for specific words or references to them. The discussion below explains these features.

## 20.3.1 Printout Formats

Normally, when ODT prints addresses it attempts to print them in relative form (Form B in Table 20–1). ODT looks for the relocation register whose value is closest to, but less than or equal to, the address to be printed. It then represents the address relative to the contents of the relocation register. However, if no relocation register fits the requirement, the address prints in absolute form. Since the relocation registers are initialized to -1 (the highest number), the addresses initially print in absolute form. If you change the contents of any relocation register, it can then, depending on the command, qualify for relative form.

For example, suppose relocation registers 1 and 2 contain 1000 and 1004 respectively, and all other relocation registers contain much higher numbers. In this case, the following sequence might occur (the slash command causes the contents of the location to be printed; the line feed command, LF, accesses the next sequential location):

```csv
* 1000;1R
* 1,4;2R
* 774/000000 LF
000776 /000000 <LF>
1,000000 /000000 <LF>
1,000002 /000000 <LF>
2,000000 /000000
```

The printout format is controlled by the format register, \$F. Normally this register contains 0, in which case ODT prints relative addresses whenever possible. You can open \$F and change its contents to a nonzero value, however. In that case all addresses will print in absolute form (see Section 20.3.4, Accessing Internal Registers).

## 20.3.2 Opening, Changing, and Closing Locations

An open location is one whose contents ODT prints for examination, making those contents available for change. In a closed location, the contents are no longer available for change. Several commands are used for opening and closing locations.

Any command (except for the slash and backslash commands) that opens a location when another location is already open causes the currently open location to be closed. You can change the contents of an open location by typing the new contents followed by a single-character command that requires no argument (that is, LF, ^, RET, ←, (a, >, <).

20.3.2.1 Slash (/) — One way to open a location is to type its address followed by a slash. For example:

\*1000/012746

This command opens location 1000 for examination and makes it ready to be changed.

If you do not want to change the contents of an open location, press the RETURN key to close the location. ODT prints an asterisk and waits for another command. However, to change the word, simply type the new contents before giving a command to close the location. For example:

\*1000/012746 012345 RET
\*

This command inserts the new value, 012345, in location 1000 and closes the location. ODT prints another asterisk, indicating its readiness to accept another command.

Used alone, the slash reopens the last location opened. For example:

```txt
* 1000/012345 2340 RET
*/002340
```

This command opens location 1000, changes its address to 002340, and then closes the location. ODT prints an asterisk, indicating its readiness to accept another command. The / character reopens the last location opened and verifies its value.

Note again that opening a location while another is open automatically closes the currently open location before opening the new location.

Also note that if you specify an odd numbered address with a slash, ODT opens the location as a byte, and subsequently behaves as if you had typed a backslash (see Section 20.3.2.2).

20.3.2.2 Backslash (\) — ODT operates on bytes, as well as on words. Typing the address of the byte followed by a backslash character opens the byte. This causes ODT to print the byte value at the specified address, to interpret the value as ASCII code, and to print the corresponding character (if possible) on the terminal. (ODT prints a ? when it cannot interpret the ASCII value as a printable character.)

```txt
*1001\101 =A
```

A backslash typed alone reopens the last open byte. If a word was previously open, the backslash reopens its even byte:

\*1002/000004 \004 =?

20.3.2.3 LINE FEED Key (LF) — If you type the LINE FEED key when a location is open, ODT closes the open location and opens the next sequential location:

```txt
*1000/002340 LF
001002 /012740
```

In this example, the LINE FEED key caused ODT to print the address of the next location along with its contents and to wait for further instructions. After the above operation, location 1000 is closed and 1002 is open. You may modify the open location by typing the new contents.

If a byte location was open, typing a line feed opens the next byte location.

20.3.2.4 Circumflex or Up-Arrow ( $^{or}$   $\uparrow$ ) — If you type the circumflex (or up-arrow) when a location is open, ODT closes the open location and opens the previous location. To continue from the example above:

```csv
*001002/012740
001000 /002340
```

This command closes location 1002 and opens location 1000. You may modify the open location by typing the new contents.

If the opened location was a byte, then the circumflex opens the previous byte.

20.3.2.5 Underline or Back-Arrow (\_ or $\leftarrow$) — If you type the underline (or back-arrow) to an open word, ODT interprets the contents of the currently open word as an address indexed by the program counter (PC) and opens the addressed location:

\*1006/000006\_
001016 /000405

Notice in this example that the open location, 1006, is indexed by the PC as if it were the operand of an instruction with addressing mode 67 (PC relative mode).

You can make a modification to the opened location before you type a line feed, circumflex, or underline. Also, the new contents of the location will be used for address calculations using the underline command. For example:

```txt
*100/000222 4LF                  ;modifies to 4 and open next location
000102 /000111 6^                 ;modifies to 6 and open previous location
000100 /000004 200_               ;changes to 200 and open location indexed
000302 /123456                   ;by PC
```

20.3.2.6 Open the Addressed Location (@) — You can use the at (@) symbol to optionally modify a location, close it, and then use its contents as the address of the location to open next. For example:

```asm
*1006/001044 @                      ;opens location 1044 next
001044 /000500

*1006/001044 2100@                 ;modifies to 2100 and opens location
002100 /000167                          ;2100
```

20.3.2.7 Relative Branch Offset (>) — The right-angle bracket (>) optionally modifies a location, closes it, and then uses its low-order byte as a relative branch offset to the next word to be opened. For example:

```txt
*1032/000407 301>          ;modifies to 301 and interprets as a
000636 /000010           ;relative branch
```

Note that 301 is a negative offset (-77). ODT doubles the offset before it adds it to the PC; therefore,  $1034 + (-176) = 636$ .

20.3.2.8 Return to Previous Sequence (<) — The left-angle bracket (<) lets you optionally modify a location, close it, and then open the next location of the previous sequence that was interrupted by an underline, @, or right-angle bracket command. Note that underline, @, or right-angle bracket causes a sequence change to the open word. If a sequence change has not occurred, the left-angle bracket simply opens the next location as a LINE FEED does. This command operates on both words and bytes.

```txt
*1032/000407 301> ;> causes a sequence change
000636 /000010 < ;returns to original sequence
001034 /001040 @ ;@ causes a sequence.change
001040 /000405 \005 = < ;< now operates on byte
001035 \002 =? < ;< acts like <LF>
001036 \004 =?
```

## 20.3.3 Accessing General Registers 0–7

Open the program's general registers 0–7 with a command in the following format:

\$n/

The symbol, n, is an integer in the range 0–7 that represents the desired register. When you open these registers, you can examine them or change their contents by typing in new data, as with any addressable location. For example:

```txt
* 000033$0/    [RET] ;examines register 0 then closes it
*
* 000474$4/    [464RET];opens register 4, changes its contents
*          ;to 000464, then closes the register
```

The example above can be verified by typing a slash in response to ODT's asterisk:

```txt
* 000464 /.
```

You can use the LINE FEED, circumflex, or @ command when a register is open.

## 20.3.4 Accessing Internal Registers

The program's status register contains the condition codes of the most recent operational results and the interrupt priority level of the object program. Open it by typing \$S. For example:

```txt
* 000311$S/
```

$S$ represents the address of the status register. In response to $S$ in the example above, ODT prints the 16-bit word, of which only the low-order eight bits are meaningful. Bits 0–3 indicate whether a carry, overflow, zero, or negative (in that order) has resulted, and bits 5–7 indicate the interrupt priority level (in the range 0–7) of the object program. (Refer to the PDP-11 Processor Handbook for the Status Register format.)

You can also use the \$ to open certain other internal locations listed in Table 20-2.

Table 20-2: Internal Registers

| Register | Section | Contents |
| --- | --- | --- |
| $B | 20.3.6 | First word of the breakpoint table |
| $M | 20.3.9 | Mask location for specifying which bits are to be examined during a bit pattern search |
| $P | 20.3.15 | Defines the operating priority of ODT |
| $S | 20.3.4 | Condition codes (bits 0–3) and interrupt priority level (bits 5–7) |
| $C | 20.3.10 | Constant register |
| $R | 20.3.13 | Relocation register 0, the base of the Relocation Register table |
| $F | 20.3.1 | Format register |

## 20.3.5 Radix-50 Mode (X)

Many PDP-11 system programs employ the Radix-50 mode of packing certain ASCII characters three to a word. You can use Radix-50 mode by specifying the MACRO .RAD50 directive. ODT provides a method for examining and changing memory words packed in this way with the X command.

When you open a word and type the X command, ODT converts the contents of the opened word to its three-character Radix-50 equivalent and prints these characters on the terminal. You can then type one of the responses from Table 20–3.

Table 20-3: Radix-50 Terminators

| Response | Effect |
| --- | --- |
| RETURN key (RET) | Closes the currently open location. |
| LINE FEED key (LF) | Closes the currently open location and opens the next one in sequence. |
| Circumflex (^) | Closes the currently open location and opens the previous one in sequence. |
| Any three characters whose octal code is 040 (space) or greater | Converts the three characters into packed Radix-50 format. Valid Radix-50 characters for this response are: .$Space0 through 9A through Z |

If you type any other characters, the resulting binary number is unspecified (that is, no error message prints and the result is unpredictable). You must type exactly three characters before ODT resumes its normal mode of operation. After you type the third character, the resulting binary number is available to be stored in the opened location. Do this by closing the location in any one of the ways listed in Table 20–3. For example:

\*1000/042431 X =KBI CBA RET

\*1000/011421 X = CBA

## NOTE

After ODT converts the three characters to binary, the binary number can be interpreted in one of many different ways, depending on the command that follows. For example:

## \*1234/063337 X=PRO XIT/013704

Since the Radix--50 equivalent of XIT is 113574, the final slash in the example will cause ODT to open location 113574 if it is a valid address.

## 20.3.6 Breakpoints

The breakpoint feature helps you monitor the progress of program execution. You can set a breakpoint at any instruction that is not referenced by the program for data. When a breakpoint is set, ODT replaces the contents of the breakpoint location with a BPT trap instruction so that program execution is suspended when a breakpoint is encountered. Then the original contents of the breakpoint location are restored, and ODT regains control.

With ODT you can set up to eight breakpoints, numbered 0 through 7, at any one time. Set a breakpoint by typing the address of the desired location of the breakpoint followed by ;B. Thus, r;B sets the next available breakpoint at location r. (If all eight breakpoints have been set, ODT ignores the r;B command.) You may set or change specific breakpoints by the r;nB command, where n is the number of the breakpoint. For example:

```c
* 1020;B    ;sets breakpoint 0
* 1030;B    ;sets breakpoint 1
* 1040;B    ;sets breakpoint 2
* 1032;1B   ;resets breakpoint 1
*
```

The ;B command removes all breakpoints. Use the ;nB command to remove only one of the breakpoints, where n is the number that identifies the breakpoint. For example:

```c
* ;2B          ;removes breakpoint 2
*
```

ODT keeps a table of breakpoints that you can access. The \$B/ command opens the location containing the address of breakpoint 0. The next seven locations contain the addresses of the other breakpoints in order. You can sequentially open them by using the LINE FEED key. For example:

```shell
* $B/001020 LF
001136 /001032 LF
001140 /007070 LF
001142 /007070 LF
001144 /007070 LF
001146 /001046 LF
001150 /001066 LF
001152 /007070
```

In this example, breakpoint 0 is set to 1020, breakpoint 1 is set to 1032, breakpoint 5 is set to 1046, and breakpoint 6 is set to 1066. The other breakpoints are not set.

Note that a repeat count in a proceed command (;P) refers only to the breakpoint that ODT most recently encountered. Execution of other breakpoints is determined by their own repeat counts. See Section 20.3.7.

## 20.3.7 Running the Program (r;G and r;P)

ODT controls program execution. There are two commands for running the program: r;G and r;P. The r;G command starts execution (go) and r;P continues (proceed) execution after halting at a breakpoint. For example:

```txt
* 1000;G
```

This command starts execution at location 1000. The program runs until it encounters a breakpoint or until it completes. If it gets caught in an infinite loop, it must be either restarted or reentered as explained in Section 20.1.

On execution of either the r;G or r;P command, the general registers 0–6 are set to the values in the locations specified as \$0–\$6. The processor status register is set to the value in the location specified as \$S.

When ODT encounters a breakpoint, execution stops and ODT prints Bn; (where n is the breakpoint number), followed by the address of the breakpoint. You can then examine locations for expected data. For example:

```txt
* 1010;3B          ;sets breakpoint 3 at location 1010
* 1000;G           ;starts execution at location 1000
B3;001010       ;stops execution at location 1010
*
```

To continue program execution from the breakpoint, type ;P in response to ODT's last prompt (\*).

When you set a breakpoint in a loop, you can allow the program to execute a specified number of times through the loop before ODT recognizes the breakpoint. Set a proceed count by using the r;P command. This command specifies the number of times the breakpoint is to be encountered before ODT suspends program execution (on the kth encounter). The count k refers only to the numbered breakpoint that most recently occurred. You can specify a different proceed count for the breakpoint when it is encountered. Thus:

```txt
B3;001010          ;halts execution at breakpoint 3
* 1026;3B       ;resets breakpoint 3 at location 1026
* 4;P               ;sets proceed count to 4 and
B3;001026         ;continues execution; the program loops
*                       ;through the breakpoint three times and halts on
                       ;the fourth occurrence of the breakpoint
```

Following the table of breakpoints (as explained in Section 20.3.6) is a table of proceed command repeat counts for each breakpoint. You can inspect these repeat counts by typing \$B/ and nine line feeds. The repeat count for breakpoint 0 prints (the first seven line feeds cause the table of breakpoints to be printed; the eighth types the single-instruction mode, explained in the next section, and the ninth line feed begins the table of proceed command repeat counts). The repeat counts for breakpoints 1 through 7 and the repeat count for the single-instruction trap follow in sequence. ODT initializes a proceed count to 0 before you assign it a value. After the command has been executed, it is set to -1. Opening any one of these provides an alternative way of changing the count. Once the location is open, you can modify its contents in the usual manner by typing the new contents followed by the RETURN key. For example:

[figure omitted]

Both the address indicated as the single-instruction address and the repeat count for single-instruction mode are explained in the following section.

## 20.3.8 Single-Instruction Mode

With this mode, you specify the number of instructions to be executed before ODT suspends the program run. The proceed command, instead of specifying a repeat count for a breakpoint encounter, specifies the number of succeeding instructions to be executed. Note that breakpoints are disabled in single-instruction mode. Table 20–4 lists the single-instruction mode commands.

Table 20-4: Single-Instruction Mode Commands

| Command | Function |
| --- | --- |
| ;nS | Enables single-instruction mode (n can be any digit and serves only to distinguish this form from the form ;S, which disables single-instruction mode). Breakpoints are disabled. |
| n;P | Proceeds with program run for next n instructions before reentering ODT. (If n is missing, it is assumed to be 1.) Trapping instructions and associated handlers can affect the proceed repeat count (see Section 20.4.2). |
| ;S | Disables single-instruction mode. |

When the repeat count for single-instruction mode is exhausted and the program suspends execution, ODT prints:

## B8 ;nnnnnnn

where nnnnnn is the address of the next instruction to be executed. The \$B breakpoint table contains this address following that of breakpoint 7. However, unlike the table entries for breakpoints 0–7, direct modification has no effect.

Similarly, following the repeat count for breakpoint 7 is the repeat count for single-instruction mode. You can modify this table entry directly. This is an alternative way of setting the single-instruction mode repeat count. In such a case, ;P implies the argument set in the \$B repeat count table rather than an assumed 1.

## 20.3.9 Searches

With ODT you can search any specific portion of memory for bit patterns or references to a particular location.

20.3.9.1 Word Search (r;W) — Before initiating a word search, you must specify the mask and search limits. The location represented by \$M specifies the mask of the search. \$M/ opens the mask register. The next two sequential locations (opened by LINE FEEDs) initially contain the lower and upper limits of the search. ODT examines in the search all bits set to 1 in the mask and ignores other bits.

You must then give the search object and the initiating command, using the r;W command, where r is the search object. When ODT finds a match (that is, each bit set to 1 in the search object is set to 1 in the word ODT searches over the mask range), the matching word prints. For example:

```csv
* $M/000000 177400 LF
r,nnnnnn—/000000 1000 LF
r,nnnnnn—/000000 1040 RET
* 400 ;W
001010 /000770
001034 /000404
*
```

In the above example, nnnnnn is an address internal to ODT; this location varies and is meaningful only for reference purposes. In the first line above, the slash was used to open \$M, which now contains 177400; the LINE FEEDs open the next two sequential locations, which now contain the upper and lower limits of the search.

In the search process, ODT performs an exclusive OR (XOR) with the word currently being examined and the search object; the result is ANDed to the mask. If this result is 0, a match has been found and ODT reports it on the terminal. Note that if the mask is 0, all locations within the limits print. This provides a convenient method for dumping all memory locations within given limits using ODT.

Typing CTRL/U during a search printout terminates the search.

20.3.9.2 Effective Address Search (r;E) — ODT provides a search for words that reference a specific location. Open the mask register only to gain access to the low- and high-limit registers. After specifying the search limits (as explained for the word search), type the command r;E (where r is the effective address) to initiate the search.

Words that are an absolute address (argument r itself), a relative address offset, or a relative branch to the effective address print after their addresses. For example:

```csv
*\$M/177400 LP ;opens mask register only to gain
r,nnnnnn /001000 1010 LP ;access to search limits
r,nnnnnn /001040 1060 RET
*1034;E ;initiates search
001016 /001006 ;relative branch
001054 /002767 ;relative branch
*1020;E ;initiates a new search
001022 /177774 ;relative address offset
001030 /001020 ;absolute address
```

Pay particular attention to the reported effective address references. A word can have the specified bit pattern of an effective address without actually being used as one. ODT reports all possible references whether they are actually used or not.

Typing CTRL/U during a search printout terminates the search.

## 20.3.10 Constant Register (r;C)

It is often desirable to convert a relocatable address into its value after relocation, or to convert a number into its two's complement and then to store the converted value into one or more places in a program. Use the constant register to perform this and other useful functions.

Typing r;C evaluates the relocatable expression to its six-digit octal value, prints the value on the terminal, and stores it in the constant register. Invoke the contents of the constant register in subsequent relocatable expressions by typing the letter C. Examples follow:

\*-4432;C=173346;places the two's complement of 4432 in the
;constant register

\*6632/062701 C RET;stores the contents of the constant
;register in location 6632

\*1000;1R

;sets relocation register 1 to 1000

\*1,4272;C=005272;reprints relative location 4272 as an
;absolute location and stores it in the
;constant register

## 20.3.11 Memory Block Initialization (;F and ;I)

Use the constant register with the commands ;F and ;I to set a block of memory to a specific value. While the most common value required is 0, other possibilities are +1, -1, ASCII space, etc.

When you type the command ;F, ODT stores the contents of the constant register in successive memory words, starting at the memory word address you specify in the lower search limit and ending with the address you specify in the upper search limit.

Typing the command ;I stores the low-order eight bits in the constant register in successive bytes of memory, starting at the byte address you specify in the lower search limit and ending with the byte address you specify in the upper search limit.

For example, assume relocation register 1 contains 7000, 2 contains 10000, and 3 contains 15000. The following sequence sets word locations 7000–7776 to 0, and byte locations 10000–14777 to ASCII spaces:

```csv
* \$M/000000 LF
r,nnnnnn /000000 1,0 LF
r,nnnnnn /000000 2,-2 RET
* 0;C=000000
* ;F

* \$M/000000 LF
r,nnnnnn /007000 2,0 LF
r,nnnnnn /007776 3,-1 RET
* 40;C=000040

* ;I

*
;opens the mask register to gain
;access to search limits
;sets the lower limit to 7000
;sets the upper limit to 7776
;sets the constant register to zero
;sets locations 7000-7776 to zero
;
;sets the lower limit to 10000
;sets the upper limit to 14777
;sets the constant register to 40
;(space)
;sets the byte locations
;10000-14777
;to the value in the low-order
;eight bits of the constant
;register
```

## 20.3.12 Calculating Offsets (r;O)

Relative addressing and branching involve the use of an offset. An offset is the number of words or bytes forward or backward from the current location to the effective address. During the debugging session it is sometimes necessary to change a relative address or branch reference by replacing one instruction offset with another. ODT calculates the offsets in response to the r;O command.

The command r;O causes ODT to print the 16-bit and 8-bit offsets from the currently open location to address r. For example:

```txt
*346/000034 414;0 000044 022 22 RET
*/000022
```

This command opens location 346, calculates and prints the offsets from location 346 to location 414, changes the contents of location 346 to 22 (the 8-bit offset), and verifies the contents of location 346.

The 8-bit offset prints only if it is in the range -128(decimal) to 127(decimal) and the 16-bit offset is even, as was the case above. In the next example, the offset of a relative branch is calculated and modified so that it branches to itself.

```txt
*1034/103421 1034;0 177776 377 \021 =? 377RET
*/103777
```

Note that the modified low-order byte 377 must be combined with the unmodified high-order byte.

## 20.3.13 Relocation Register Commands

The use of the relocation registers is described briefly in Section 20.2. At the beginning of a debugging session it is desirable to preset the registers to the relocation biases of those relocatable modules that will be receiving the most attention. Do this by typing the relocation bias, followed by a semicolon and the specification of relocation registers, using the following syntax:

r;nR

The symbol r may be any relocatable expression, and n is an integer in the range 0–7. If you omit n, it is assumed to be 0. For example:

```txt
*1000;5R          ;puts 1000 into relocation register 5
*5,100;5R       ;adds 100 to the contents
*                       ;of relocation register 5
```

Once a relocation register is defined, you can use it to reference relocatable values. For example:

```txt
*2000;1R          ;puts 2000 into relocation register 1
*1,2176/002466 ;examines the contents of location 4176
*1,3712;0B         ;sets a breakpoint at location 5712
```

Sometimes programs may be relocated to an address below the one at which they were assembled. This could occur with PIC code (position-independent code), which is moved without using the linker. In this case, the appropriate relocation bias would be the two's complement of the actual downward displacement. One method for easily evaluating the bias and putting it in the relocation register is illustrated in the following example.

Assume a program was assembled at location 5000 and was moved to location 1000. Then the following sequence enters the two's complement of 4000 in relocation register 1.

```csv
*1000;1R
*1,-5000;1R
*
```

Relocation registers are initialized to -1 so that unwanted relocation registers never enter into the selection process when ODT searches for the most appropriate register.

To set a relocation register to -1, type ;nR. To set all relocation registers to -1, type ;R.

ODT maintains a table of relocation registers, beginning at the address specified by \$R. Opening \$R (\$R/) opens relocation register 0. Successively typing a LINE FEED opens the other relocation registers in sequence. When a relocation register is opened in this way, you can modify it as you would any other memory location.

## 20.3.14 The Relocation Calculators, n! and nR

When a location has been opened, it is often desirable to relate the relocated address and the contents of the location back to their relocatable values. To calculate the relocatable address of the opened location relative to a particular relocation bias, use the following syntax:

## n!

The symbol n specifies the relocation register. This calculator works with opened bytes and words. If you omit n, the relocation register whose contents are closest to, but less than or equal to, the opened location is selected automatically by ODT. In the following example, assume that these conditions are fulfilled by relocation register 3, which contains 2000. Use the following command to find the most likely module that a given opened byte is in:

\*2500\011 = !=3,000500

To calculate the difference between the contents of the opened location and a relocation register, use the following syntax:

## nR

The symbol n represents the relocation register. If you omit n, ODT selects the relocation register whose contents are closest to, but less than or equal to, the contents of the opened location. For example, assume the relocation bias stored in relocation register 1 is 7000:

```csv
*1,500/011032 1R=1,002032
```

The value 2032 is the content of 1,500, relative to the base 7000. The next example shows the use of both relocation calculators.

If relocation register 1 contains 1000, and relocation register 2 contains 2000, use the following command to calculate the relocatable addresses of location 3000 and its contents, relative to 1000 and 2000:

\*3000/006410 1!=1,002000 2!=2,001000 1R=1,005410 2R=2,00410

## 20.3.15 ODT Priority Level (\$P)

\$P represents a location in ODT that contains the interrupt (or processor) priority level at which ODT operates. If \$P contains the value 377, ODT operates at the priority level of the processor at the time ODT is entered. Otherwise \$P may contain a value between 0 and 7 corresponding to the fixed priority at which ODT operates.

To set ODT to the desired priority level, open \$P. ODT prints the present contents, which you can then change:

\*\$P / 000006 4 RET
\*

;lowers the priority to allow interrupts
;from the terminal

If you do not change \$P, its value is seven.

You must set ODT's priority to 0 if you are using ODT in a foreground/background environment while another job is running.

ODT may not always service breakpoints that are set in routines that run at different priority levels. For example, a program running at a low priority can use a device service routine that operates at a higher priority level. If you set \$P low, ODT waits for terminal input at a low priority. If an interrupt occurs from a high-priority routine, the breakpoints in the high-priority routine will not be recognized because they were removed when the earlier breakpoint occurred. Thus, interrupts that are set at a priority higher than the one at which ODT is running will be serviced, but any breakpoints will not be recognized. To avoid this problem, set breakpoints at one priority level at a time. That is, set breakpoints within an interrupt service routine, but not at mainline code level. For a more complete discussion of how the PDP-11 handles priority and interrupts, refer to the processor handbook for your particular machine. ODT disables all breakpoints in the program whenever it gains control. Breakpoints are enabled when ;P and ;G commands are executed. For example:

```txt
*\$P/00007 5
*1000;B
*2000;B
*1000;G
BO:001000
* ;an interrupt occurs and is serviced
```

If a higher-level interrupt occurs while ODT is waiting for input, the interrupt is serviced, and no breakpoints are recognized.

## 20.3.16 ASCII Input and Output (r;nA)

Inspect and change ASCII text by using a command of this syntax:

## r;nA

The symbol r represents a relocatable expression, and n is a character count. If you omit n, it is assumed to be 1. ODT prints n characters starting at location r and followed by a carriage return/line feed combination. Table 20–5 lists responses and their effect.

Table 20-5: ASCII Terminators

| Response | Effect |
| --- | --- |
| RETURN Key() | ODT outputs a carriage return/ line feed combination followed by an asterisk, and waits for another command. |
| LINE FEED Key() | ODT opens the byte following the last byte that was output. |
| Up to n characters of text | ODT inserts the text into memory, starting at location r. If you type exactly n characters, ODT responds withaddress*. If you type fewer than n characters, terminate that string with CTRL/U. ODT responds with ?^Uaddress. |

## 20.4 Programming Considerations

Information in this section is not necessary for normal use of ODT. However, it does provide a better understanding of how ODT performs some of its functions. In certain difficult debugging situations, this understanding is necessary.

## 20.4.1 Using ODT with Foreground/Background Jobs

It is possible to use ODT to debug programs written as either background or foreground jobs. In the background or under the SJ monitor, you can link ODT with the program as described in the first example in Section 20.1. To debug a program in the foreground area, DIGITAL recommends that you run ODT in the background while the program to be debugged is in the foreground. The sequence of commands to do this is:

| ,FRUN PROG/P | ;loads the foreground program |
| --- | --- |
| LOADED AT nnnnnn | ;the first address of the job prints |
| ,RUN ODT | ;runs ODT in the background |
| ODT V01.01 | ;and sets a relocation register |
| *nnnnnn;OR | ;to the start of the job |
| *$F/000000 0 | ;clears the format register to enable |
| *0 ,nnnnnn;OB | ;proper address printing |
|  | ;sets a breakpoint |
| *0 ;G | ;starts the keyboard monitor again |
| ,RESUME | ;starts the foreground job |

The copy of ODT used must be linked low enough so that it fits in memory along with the foreground job.

## NOTE

Since ODT uses its own terminal handler, it cannot be used with the display hardware. If GT ON is in effect, ODT ignores it and directs its input and output only to the console terminal.

If you use ODT in a foreground/background environment while another job is running, set ODT's priority bit to 0 as follows:

\* \$P/000007 0 RET

This puts ODT into the wait state at level 0, not at level 7. If you leave ODT's priority at 7, all interrupts (including clock) are locked out while ODT is waiting for terminal input.

## 20.4.2 Functional Organization

The internal organization of ODT is almost totally modularized into independent subroutines. The internal structure consists of three major functions: command decoding, command execution, and utility routines.

The command decoder interprets the individual commands, checks for command errors, saves input parameters for use in command execution, and sends control to the appropriate command execution routine.

The command execution routines take parameters saved by the command decoder and use the utility routines to execute the specified command. Command execution routines either return to the command decoder or transfer control to your program.

The utility routines are common routines such as SAVE-RESTORE and I/O. They are used by both the command decoder and the command executers.

## 20.4.3 Breakpoints

The function of a breakpoint is to give control to ODT whenever a program tries to execute the instruction at the selected address.

When a breakpoint is executed, ODT removes all the breakpoint instructions from the code so that you can examine and alter the locations. ODT then types a message on the terminal in the form Bn;r, where r is the breakpoint address and n is the breakpoint number. ODT restores the breakpoints when execution resumes.

There is a major restriction in the use of breakpoints: the program must not reference the word where a breakpoint was set since ODT altered the word. You should also avoid setting a breakpoint at the location of any instruction that clears the T-bit. For example:

MOV #240,177776

;SET PRIORITY TO LEVEL 5

## NOTE

Instructions that cause traps or returns from them (for example, EMT, RTI) are likely to clear the T-bit, because a new word from the trap vector or the stack is loaded into the status register.

A breakpoint occurs when a trace trap instruction (placed in your program by ODT) is executed. When a breakpoint occurs, ODT operates according to the following algorithm:

1. Sets processor priority to seven (automatically set by trap instruction).

2. Saves registers and sets up stack.

3. If internal T-bit trap flag is set, goes to step 13.

4. Removes breakpoints.

5. Resets processor priority to ODT's priority or user's priority.

6. Makes sure a breakpoint or single-instruction mode caused the interrupt.

7. If the breakpoint did not cause the interrupt, goes to step 15.

8. Decrements repeat count.

9. Goes to step 18 if nonzero; otherwise resets count to one.

10. Saves terminal status.

11. Types message about the breakpoint or single-instruction mode interrupt.

12. Goes to command decoder.

13. Clears T-bit in stack and internal T-bit flag.

14. Jumps to the go processor.

15. Saves terminal status.

16. Types BE (bad entry), followed by the address.

17. Clears the T-bit, if set, in the user status and proceeds to the command decoder.

18. Goes to the proceed processor, bypassing the TT restore routine.

Note that steps 1–5 inclusive take approximately 100 microseconds. Interrupts are not permitted at this time, because ODT is running at priority level 7.

ODT processes a proceed (;P) command according to the following algorithm:

1. Checks the proceed for validity.

2. Sets the processor priority to seven.

3. Sets the T-bit flags (internal and user status).

4. Restores the user registers, status, and program counter.

5. Returns control to the user.

6. When the T-bit trap occurs, executes steps 1, 2, 3, 13, and 14 of the breakpoint sequence, restores breakpoints, and resumes normal program execution.

When a breakpoint is placed on an IOT, EMT, TRAP, or any instruction causing a trap, ODT follows this algorithm:

1. When the breakpoint occurs as described above, enters ODT.

2. When ;P is typed, sets the T-bit and executes the IOT, EMT, TRAP, or other trapping instruction.

3. Pushes the current PC and status (with the T-bit included) on the stack.

4. Obtains the new PC and status (no T-bit set) from the respective trap vector.

5. Executes the whole trap service routine without any breakpoints.

6. When an RTI is executed, restores the saved PC and PS (including the T-bit). Executes the instruction following the trap-causing instruction. If this instruction is not another trap-causing instruction, the T-bit trap occurs; reinserts the breakpoints in the user program, or decrements the single-instruction mode repeat count. If the following instruction is a trap-causing instruction, repeats this sequence starting at step 3.

## NOTE

Exit from the trap handler must be by means of the RTI instruction. Otherwise, the T-bit is lost. ODT cannot regain control because the breakpoints have not yet been reinserted.

Note that the ;P command is invalid if a breakpoint has not occurred (ODT responds with ?). ;P is valid, however, after any trace trap entry.

The internal breakpoint status words have the following format:

1. The first eight words contain the breakpoint addresses for breakpoints 0–7. (The ninth word contains the address of the next instruction to be executed in single-instruction mode.)

2. The next eight words contain the respective repeat counts. (The following word contains the repeat count for single-instruction mode.)

You may change these words at will, either by using the breakpoint commands or by directly manipulating \$B.

When program runaway occurs (that is, when the program is no longer under ODT control, perhaps executing an unexpected part of the program where you did not place a breakpoint), give control to ODT by pressing the HALT key to stop the computer and then restarting ODT (see Section 20.1). ODT prints an asterisk, indicating that it is ready to accept a command.

If the program you are debugging uses the console terminal for input or output, the program can interact with ODT to cause an error because ODT uses the console terminal as well. This interactive error does not occur when you run the program without ODT.

Note the following rules concerning the ODT break routine:

1. If the console terminal interrupt is enabled upon entry to the ODT break routine, and no output interrupt is pending when ODT is entered, ODT generates an unexpected interrupt when returning control to the program.

2. If the interrupt of the console terminal reader (the keyboard) is enabled upon entry to the ODT break routine, and the program is expecting to receive an interrupt to input a character, both the expected interrupt and the character are lost.

3. If the console terminal reader (keyboard) has just read a character into the reader data buffer when the ODT break routine is entered, the expected character in the reader data buffer is lost.

## 20.4.4 Searches

The word search lets you search for bit patterns in specified sections of memory. Using the \$M/ command, specify a mask, a lower search limit (\$M + 2), and an upper search limit (\$M + 4). Specify the search object in the search command itself.

The word search compares selected bits (where 1s appear in the mask) in the word and search object. If all of the selected bits are equal, the unmasked word prints.

The following shows the search algorithm.

1. Fetches a word at the current address.

2. XORs (exclusive OR) the word and search object.

3. ANDs the result of step 2 with the mask.

4. If the result of step 3 is zero, types the address of the unmasked word and its contents; otherwise, proceeds to step 5.

5. Adds two to the current address. If the current address is greater than the upper limit, types \* and returns to the command decoder; otherwise, goes to step 1.

Note that if the mask is 0, ODT prints every word between the limits, since a match occurs every time (that is, the result of step 3 is always 0).

In the effective address search, ODT interprets every word in the search range as an instruction that is interrogated for a possible direct relationship to the search object. The mask register is opened only to gain access to the search limit registers.

The algorithm for the effective address search is as follows ((X) denotes contents of X, and K denotes the search object):

1. Fetches a word at the current address X.

2. If  $(\mathbf{X})=\mathbf{K}$  [direct reference], prints contents and goes to step 5.

3. If $(\mathbf{X}) + \mathbf{X} + 2 = \mathbf{K}$ [indexed by PC], prints contents and goes to step 5.

4. If (X) is a relative branch to K, prints contents.

5. Adds 2 to the current address. If the current address is greater than the upper limit, performs a carriage return/line feed combination and returns to the command decoder; otherwise, goes to step 1.

## 20.4.5 Terminal Interrupt

When entering the TT SAVE routine, ODT follows these steps:

1. Saves the LSR status register (TKS).

2. Clears interrupt enable and maintenance bits in the TKS.

3. Saves the TT status register (TPS).

4. Clears interrupt enable and maintenance bits in the TPS.

To restore the TT:

1. Wait for completion of any I/O from ODT.

2. Restore the TKS.

3. Restore the TPS.

## NOTE

If the TT printer interrupt is enabled upon entry to the ODT break routine, the following can occur:

1. If no output interrupt is pending when ODT is entered, an additional interrupt always occurs when ODT returns control to the user.

2. If an output interrupt is pending upon entry, the expected interrupt occurs when the user regains control.

If the TT reader (keyboard) is busy or done, the expected character in the reader data buffer is lost.

If the TT reader (keyboard) interrupt is enabled upon entry to the ODT break routine, and a character is pending, the interrupt (as well as the character) is lost.

## 20.5 Error Detection

ODT detects two types of error: invalid or unrecognizable command and bad breakpoint entry. ODT does not check for the validity of an address when you command it to open a location for examination or modification. Thus in the following example, the command references nonexistent memory, thereby causing a trap through the vector at location 4.

177774/

?MON-F-Trap to 4 003362

If the program you are debugging with ODT has requested traps through location 4 with the .TRPSET EMT, the program receives control at its TRPSET address.

If something other than a valid command is typed, ODT ignores the command and prints:

(echoes invalid command)?

ODT then waits for another command. Therefore, to cause ODT to ignore a command that has just been typed, type any invalid character (such as 9 or RUBOUT), and the command will be treated as an error and ignored.

ODT suspends program execution whenever it encounters a breakpoint (that is, traps to its breakpoint routine). If the breakpoint routine is entered and no known breakpoint caused the entry, ODT prints:

## BEnnnnnn \*

and waits for another command. BEnnnnnn denotes bad entry from location nnnnnn. A bad entry may be caused by an invalid trace trap instruction, by a T-bit set in the status register, or by a jump to some random location within ODT.

(1)
