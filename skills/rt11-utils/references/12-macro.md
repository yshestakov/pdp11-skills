# RT-11 System Utilities Manual: Ch.12 MACRO assembler program: command string, options, listing/cross reference (CREF), macro libraries, errors

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 12.1 Calling the MACRO-11 Assembler
- 12.2 MACRO-11 Assembler Command String Syntax
- 12.3 Terminating the MACRO-11 Assembler
- 12.4 Assigning the Temporary Work File
- 12.5 File Specification Options
- 12.5.1 Listing Control Options (/L:arg and /N:arg)
- 12.5.2 Function Control Options (/D:arg and /E:arg)
- 12.5.3 Macro Library File Designation Option (/M)
- 12.5.4 Cross-Reference (CREF) Table Generation Option (/C:arg)
- 12.6 MACRO-11 Error Codes

---

## Chapter 12

# MACRO-11 Assembler Program (MACRO)

This chapter describes how to assemble MACRO-11 programs under the RT-11 operating system.

Output from the MACRO-11 assembler includes any or all of the following:

1. A binary object file — the machine-readable logical equivalent of the MACRO-11 assembly language source code

2. A listing of the source input file

3. A cross-reference file listing

4. A table of contents listing

5. A symbol table listing

To use the MACRO-11 assembler, you should understand how to:

1. Initiate and terminate the MACRO-11 assembler (including how to format command strings to specify files MACRO-11 uses during assembly)

2. Assign temporary work files to nondefault devices, if necessary

3. Use file specification options to override file control directives in the source program

4. Interpret error codes

The following sections describe these topics.

## 12.1 Calling the MACRO-11 Assembler

To call the MACRO-11 assembler from the system device, respond to the system prompt (a dot printed by the keyboard monitor) by typing:

• R MACRO RET

When the assembler responds with an asterisk (\*), it is ready to accept command string input. (You can also call the assembler using the keyboard monitor MACRO command; see Chapter 4 of the RT-11 System User's Guide for a description of this command.)

## 12.2 MACRO-11 Assembler Command String Syntax

The assembler expects a command string consisting of the following items, in sequence:

1. Output file specifications

2. An equal sign $(=)$

3. Input file specifications

Format this command string as follows (punctuation is required where shown):

dev:obj,dev:list,dev:cref/s:arg = dev:sourcei,...,dev:sourcen/s:arg

where:

dev is any valid RT-11 device for output; any file-structured device for input.

obj is the file specification of the binary object file that the assembly process produces; the dev for this file should not be TT or LP.

list is the file specification of the assembly and symbol listing that the assembly process produces.

cref is the file specification of the CREF temporary cross-reference file that the assembly process produces. (Omission of dev:cref does not preclude a cross-reference listing, however.)

/s:arg is a set of file specification options and arguments. (Section 12.5 describes these options and associated arguments.)

sourcei is a file specification for MACRO-11 source files or MACRO library files. (These files contain the MACRO language programs to be assembled. You can specify as many as six source files.)

The following command string calls for an assembly that uses one source file plus the system MACRO library to produce an object file BINF.OBJ and a listing. The listing goes directly to the line printer.

\* DK:BINF.OBJ,LP:=DK:SRC.MAC

All output file specifications are optional. The system does not produce an output file unless the command string contains a specification for that file.

The system determines the file type of an output file specification by its position in the command string. Use commas in place of files you wish to omit. For example, to omit the object file, you must begin the command string with a comma. The following command produces a listing, including cross-reference tables, but not binary object files.

\* ,LP:/C=(source file specification)

You need not include a comma after the final output file specification in the command string.

Table 12-1 lists the default values for each file specification.

Table 12-1: Default File Specification Values

| File | Default Device | Default File Name | Default File Type |
| --- | --- | --- | --- |
| Object | DK: | Must specify | .OBJ |
| Listing | Same as for object file | Must specify | .LST |
| Cref | DK: | Must specify | .TMP |
| First source | DK: | Must specify | .MAC |
| Additional source | Same as for preceding source file | Must specify | .MAC |
| System MACRO library | System device SY: | SYSMAC | .SML |
| User MACRO library | DK: if first file, otherwise same as for preceding source file | Must specify | .MLB |

## 12.3 Terminating the MACRO-11 Assembler

If you have typed R MACRO and received the asterisk prompt but have not yet entered the command string, you can terminate MACRO-11 control by typing CTRL/C once. After you have completed the command string (thus beginning an assembly) you can halt the assembly process at any time by typing CTRL/C twice. This returns control to the system monitor, and a system monitor dot prompt appears on the terminal.

To restart the assembly process, type R MACRO in response to the system monitor prompt.

## 12.4 Assigning the Temporary Work File

Some assemblies need more symbol table space than available memory can contain. When this occurs the system automatically creates a temporary work file called WRK.TMP to provide extended symbol table space.

The default device for WRK.TMP is DK. To cause the system to assign a different device, enter the following command:

• ASSIGN dev: WF

The dev parameter is the physical name of a file-structured device. The system assigns WRK.TMP to this device.

## 12.5 File Specification Options

At assembly time you may need to override certain MACRO directives appearing in the source programs. You may also need to direct MACRO-11 on the handling of certain files during assembly. You can satisfy these needs by including special options in the MACRO-11 command string in addition to the file specifications. Table 12-2 lists the options and describes the effect of each.

The general format of the MACRO-11 command string is repeated below for your convenience:

$$
\text {dev:obj,dev:list,dev:cref/s:arg = dev:sourcei,...,dev:sourcen / s:arg}
$$

Table 12-2: File Specification Options

| Option | Function |
| --- | --- |
| /C:arg | Control contents of cross-reference listing |
| /D:arg | Object file function disabling; overrides source program directive .DSABL |
| /E:arg | Object file function enabling; overrides source program directive .ENABL/L:arg listing control, overrides source program directive .LIST |
| /L:arg | Listing control; overrides source program directive .LIST |
| /M | Indicates input file is MACRO library file : |
| /N:arg | Listing control; overrides source program directive .NLIST |

The /M option affects only the particular source file specification to which it is directly appended in the command string.

Other options are unaffected by their placement in the command string. The /L option, for example, affects the listing file, regardless of where you place it in the command string.

The following subsections describe how to use the file specification options.

## 12.5.1 Listing Control Options (/L:arg and /N:arg)

Two options, /L:arg and /N:arg, pertain to listing control. By specifying these options with a set of selected arguments (see Table 12–3) you can control the content and format of assembly listings. You can override at assembly time the arguments of .LIST and .NLIST directives in the source program.

Figure 12–1 shows an assembly listing of a small program. This illustration shows the more important listing features. It labels each feature with the mnemonic ASCII argument that determines its appearance on the listing; the argument SEQ, for instance, controls the appearance of the source line sequence numbers.

Figure 12-1: Sample Assembly Listing

<table><tr><td colspan="6">MAIN. MACRO V04.00 6-JUN-79 00:03:57 PAGE 1</td></tr><tr><td>SEQ</td><td></td><td colspan="2">BIN</td><td colspan="2">SRC</td></tr><tr><td>1</td><td rowspan="5">LOC</td><td rowspan="5" colspan="2">000012</td><td rowspan="5">LF=</td><td>v12</td></tr><tr><td>2</td><td>.MCALL .TTYIN, .EXIT</td></tr><tr><td>3</td><td>.MACRO CALL NAME;DEFINE A USER MACRO</td></tr><tr><td>4</td><td>.JSR PC,NAME</td></tr><tr><td>5</td><td>.ENDM</td></tr><tr><td rowspan="3">AU</td><td>6 000000</td><td rowspan="2">000000</td><td rowspan="2">000000 R00000</td><td rowspan="3">START:</td><td>MOV #BUFFER,R2;TWO EXTERNAL SUBROUTINES</td></tr><tr><td>7 000000</td><td>.CSECT PROG;DEFINE A CSRCT</td></tr><tr><td>8 000000</td><td>012702</td><td>000050°</td><td>MOV8 R0,(R2)+;READ A CHAF INTO RM;AND STORE IN BUFFER</td></tr><tr><td rowspan="3">AU</td><td>9 000004</td><td>000000</td><td>000003</td><td rowspan="6">1$</td><td>CMPB RM,#LF;WAS II A LINE FEED?</td></tr><tr><td>10 000013</td><td>110022</td><td></td><td>BNE 1$;NUFE = KEEP READING</td></tr><tr><td>11 000012</td><td>120027</td><td>000012</td><td>CLKB (R2)+;ELSE FLAG END OF LINE WITH ZERO</td></tr><tr><td rowspan="4">AU</td><td>12 000016</td><td>001377</td><td></td><td>MOV #BUFFER,R3;R3 = ADRS(BUFFER) FOR SUBR1</td></tr><tr><td>13 000020</td><td>105022</td><td></td><td>CALL SUBR1;INVOLVE CALL MACRO</td></tr><tr><td>14 000022</td><td>012703</td><td>000050°</td><td>JSR PC,SURR1</td></tr><tr><td>15 000026</td><td></td><td></td><td rowspan="8">MC</td><td>BCS START;GET A NEW LINE IF CARRY SET</td></tr><tr><td rowspan="3">U</td><td>000026</td><td>004767</td><td>000000</td><td>CALL SUBR2;ELSE CALL OTHER SUBR.</td></tr><tr><td>16 000032</td><td>103762</td><td></td><td>JSH PC,SURR2</td></tr><tr><td>17 000034</td><td></td><td></td><td>MOV R0,ANSWER;AND STORE IN ANSWER</td></tr><tr><td rowspan="7">U</td><td>000034</td><td>004767</td><td>000000</td><td>.EXIT</td></tr><tr><td>18 000040</td><td>010067</td><td>000002</td><td>EMT *035N;RETURN TO RI-11</td></tr><tr><td>19 000044</td><td></td><td></td><td>.BLKW;DEFINE ANSWER STORAGE</td></tr><tr><td>000044</td><td>104350</td><td></td><td>.BLKB 72;INPUT LINE BUFFER</td></tr><tr><td>20 000046</td><td></td><td></td><td>ANSWER:</td><td rowspan="3">.BLKB START</td></tr><tr><td>21 000050</td><td></td><td></td><td rowspan="2">BUFFER:</td></tr><tr><td>22</td><td>000000°</td><td></td></tr><tr><td colspan="6">SYMBOL TABLE</td></tr><tr><td>ANSWER</td><td>000046R</td><td colspan="2">002 LF = 000012</td><td>SUBR1 = *****</td><td rowspan="5">.GLOBA= ***** .TTYIN= *****</td></tr><tr><td>BUFFER</td><td>000050R</td><td>002 START</td><td>000000R 002</td><td>SUBR2 = *****</td></tr><tr><td rowspan="2">ABS.</td><td>030630</td><td colspan="2">000</td><td></td></tr><tr><td>000006</td><td colspan="2">001</td><td></td></tr><tr><td>PROG</td><td>030160</td><td colspan="2">002</td><td></td></tr><tr><td colspan="6">ERRORS DETECTED: 5</td></tr></table>

Specifying the /N option with no argument causes the system to list only the symbol table, table of contents, and error messages.

Specifying the /L option with no arguments causes the system to ignore .LIST and .NLIST directives that have no arguments.

The following example lists binary code throughout the assembly using the 132-column line printer format, and suppresses the symbol table listing.

.\* I ,LP : /L :MEB /N :SYM=FILE

Table 12-3: Arguments for /L and /N Listing Control Options

| Argument | Default | Listing Control |
| --- | --- | --- |
| BEX | List | Binary extensions |
| BIN | List | Generated binary code |
| CND | List | Unsatisfied conditionals, .IF and .ENDC statements |
| COM | List | Comments |
| LD | No list | List control directives with no arguments |
| LOC | List | Address location counter |
| MC | List | Macro calls, repeat range expansion |
| MD | List | Macro definitions, repeat range expansion |
| ME | No list | Macro expansions |
| MEB | No list | Macro expansion binary code |
| SEQ | List | Source line sequence numbers |
| SRC | List | Source code |
| SYM | List | Symbol table |
| TOC | List | Table of contents |
| TTM | No list | 132-column line printer format when not specified, terminal mode when specified |

## 12.5.2 Function Control Options (/D:arg and /E:arg)

Two options, /E:arg and /D:arg, allow you to enable or disable functions at assembly time, and thus influence the form and content of the binary object file. These functions can override .ENABLE and .DSABL directives in the source program.

Table 12–4 summarizes the acceptable /E and /D function arguments, their normal default status, and the functions they control.

```txt
• R PIP
* SRCPRG.MAC=CR:/A
* CTRL/C
• R MACRO
* ,LP:=SRCPRG.MAC/E:CDR
```

Table 12-4: Arguments for /E and /D Function Control Options

| Argument | Default Mode | Function |
| --- | --- | --- |
| ABS | Disable | Allows absolute binary output |
| AMA | Disable | Assembles all absolute addresses as relative addresses |
| CDR | Disable | Treats all source information beyond column 72 as commentary |
| CRF | Enable | Allows cross-reference listing; disabling this function inhibits CREF output if option /C is active |
| FPT | Disable | Truncates floating point values (instead of rounding) |
| GBL | Enable | Treats undefined symbols as globals |
| LC | Enable | Allows lowercase ASCII source input |
| LCM | Disable | Causes the MACRO-11 conditional assembly directives .IF IDN and .IF DIF to sense differences between uppercase and lowercase letters. |
| LSB | Disable | Allows local symbol block |
| MCL | Disable | Causes MACRO to search all MACRO libraries for a MACRO definition if an undefined op code is found |
| PNC | Enable | Allows binary output |
| REG | Enable | Allows mnemonic definitions of registers |

For example, if you type the following commands the system assembles a file while treating columns 73 through 80 of each source line as commentary.

Because MACRO-11 is a two-pass assembler, you cannot read directly from any non-file-structured device. You must use PIP (or the keyboard monitor COPY command) to transfer input to a file-structured device before beginning the assembly.

Use either the function control or listing control option and arguments at assembly time to override corresponding listing or function control directives in the source program. For example, assume that the source program contains the following sequence:

.NLIST MEB

∴ (MACRO references)

.LIST MEB

In this example, you disable the listing of macro expansion binary code for some portion of the code and subsequently resume MEB listing. However, if you indicate /L:MEB in the assembly command string, the system ignores both the .NLIST MEB and the .LIST MEB directives. This enables MEB listing throughout the program.

## 12.5.3 Macro Library File Designation Option (/M)

The /M option is meaningful only if appended to a source file specification. It designates its associated source file as a macro library.

If the command string does not include the standard system macro library SYSMAC.SML, the system automatically includes it as the first source file in the command string.

When the assembler encounters an .MCALL directive in the source code, it searches macro libraries according to their order of appearance in the command string. When it locates a macro record whose name matches that given in the .MCALL,,it assembles the macro as indicated by that definition. Thus if two or more macro libraries contain definitions of the same macro name, the macro library that appears rightmost in the command string takes precedence.

Consider the following command string:

\* (output file specification)=ALIB,MLB/M,BLIB,MLB/M,XIZ

Assume that each of the two macro libraries, ALIB and BLIB, contain a macro called .BIG, but with different definitions. Then, if source file XIZ contains a macro call .MCALL .BIG, the system includes the definition of .BIG in the program as it appears in the macro library BLIB.

Moreover, if macro library ALIB contains a definition of a macro called .READ, that definition of .READ overrides the standard .READ macro definition in SYSMAC.SML.

## 12.5.4 Cross-Reference (CREF) Table Generation Option (/C:arg)

A cross-reference (CREF) table lists all or a subset of the symbols in a source program, identifying the statements that define and use the symbols.

12.5.4.1 Obtaining a Cross-Reference Table — To obtain a CREF table you must include the /C:arg option in the command string. Usually you include the /C:arg option with the assembly listing file specification. You can in fact place it anywhere in the command string.

If the command string does not include a CREF file specification, the system automatically generates a temporary file on device DK:. If you need to have a device other than DK: contain the temporary CREF file, you must include the dev:cref field in the command string.

If the listing device is magtape, load the handler for that device before issuing the command string, using the monitor LOAD command (described in Chapter 4 of the RT-11 System User's Guide).

A complete CREF listing contains the following six sections:

1. A cross-reference of program symbols; that is, labels used in the program and symbols defined by a direct assignment statement.

2. A cross-reference of register equate symbols. These normally include the symbols R0, R1, R2, R3, R4, R5, SP, and PC, unless the REG function has been disabled through a .DSABL REG directive or the /D:REG option. Also included are any other symbols that are defined in the program by the construct:

symbol = %n

where  $0^{<n^{<7}}$  and n represents the register number.

3. A cross-reference of MACRO symbols; that is, those symbols defined by .MACRO and .MCALL directives.

4. A cross-reference of permanent symbols, that is, all operation mnemonics and assembler directives.

5. A cross-reference of program sections. These symbols include the names you specify as operands of .CSECT or .PSECT directives. Also included are the default program sections produced by the assembler, the blank p-sect, and the absolute p-sect, .ABS.

6. A cross-reference of errors. The system groups and lists all flagged errors from the assembly by error type.

You can include any or all of these six sections in the cross-reference listing by specifying the appropriate arguments with the /C option. These arguments are listed and described in Table 12–5.

Table 12-5: /C Option Arguments

| Argument | CREF Section |
| --- | --- |
| C | Control and program sections |
| E | Error code grouping |
| M | MACRO symbolic names |
| P | Permanent symbols including instructions and directives |
| R | Register symbols |
| S | User-defined symbols |

## NOTE

Specifying /C with no argument is equivalent to specifying /C:S:M:E. That special case excepted, you must explicitly request each CREF section by including its arguments. No cross-reference file occurs if the /C option is not specified, even if the command string includes a CREF file specification.

12.5.4.2 Handling Cross-Reference Table Files — When you request a cross-reference listing by means of the /C option, you cause the system to generate a temporary file, DK: CREF.TMP.

If device DK: is write-locked or if it contains insufficient free space for the temporary file, you can allocate another device for the file. To allocate another device, specify a third output file in the command string; that is, include a dev:cref specification. (You must still include the /C option to control the form and content of the listing. The dev:cref specification is ignored if the /C option is not also present in the command string.)

The system then uses the dev:cref file instead of DK:CREF.TMP and deletes it automatically after producing the CREF listing.

The following command string causes the system to use RK2:TEMP.TMP as the temporary CREF file.

\* ,LP: ,RK2:TEMP, TMP=SOURCE/C

Another way to assign an alternate device for the CREF.TMP file is to enter the following command prior to entering R MACRO:

, ASSIGN dev: CF

This method is preferred if you intend to do several assemblies, because it relieves you from having to include the dev:cref specification in each command string. If you enter the ASSIGN dev: CF command, and later include a CREF specification in a command string, the specification in the command string prevails for that assembly only.

If you assign CF to a physical device, that device also becomes the default device for the LINK temporary file CREF.TMP created when you use the LINK/GLOBAL (/N) option.

The system lists requested cross-reference tables following the MACRO assembly listing. Each table begins on a new page. (Figure 12-2 combines the tables to save space, however.)

The system prints symbols and also symbol values, control sections, and error codes, if applicable, beginning at the left margin of the page. References to each symbol are listed on the same line, left-to-right across the page. The system lists references in the form p-l, where p is the page in which the symbol, control section, or error code appears, and l is the line number on the page.

A number sign (#) next to a reference indicates a symbol definition. An asterisk (\*) next to a reference indicates a destructive reference — that is, an operation that alters the contents of the addressed location.

## Figure 12-2: Cross-Reference Table

.MAIN, MACPO VM4.20 6-JUN-79 00:03157 PAGE S-1
CROSS REFERENCE TABLE (CREF V01-05)

$$
1 = 1 4
$$

$$
1 = 2 1 *
$$

$$
1 = 1 1
$$

$$
1 \cdot 1 6
$$

$$
1 = 2 2
$$

$$
1 \cdot 1 5
$$

$$
1 = 1 7
$$

,MAIN, MACRO V03.00 6-JUN-77 M1:V3:57 PAGE H-1
CROSS REFERENCE TABLE (CREF V01-05)

$$
\begin{array}{l} 1 = 1 5 \\ 1 = 1 2 \\ 1 = 9 \\ 1 = 1 4 \end{array}
$$

$$
\begin{array}{l} 1 = 1 7 \\ 1 = 1 1 \\ 1 = 1 2 \end{array}
$$

$$
\begin{array}{l} 1 = 1 8 \\ 1 = 1 3 \end{array} *
$$

MAIN. MACRO VE3,00 6-JUN-77 00:03:57 PAGE M-1
CROSS REFERENCE TABLE (CREF V:1-05)

$$
\begin{array}{c} \bullet E X J T \\ \bullet T T Y 1 N \\ C A L I. \end{array}
$$

$$
\begin{array}{l} 1 = 2 \\ 1 = 2 \\ 1 = 3 \end{array}
$$

$$
\begin{array}{c} 1 \cdot 1 9 \\ 1 \cdot 1 5 \end{array}
$$

$$
1 = 1 7
$$

MAIN. MACRO V04.00 6-JUN-79 001:03:57 PAGE P-1 CROSS REFERENCE TABLE (CREF V01-05)

$$
1 \cdot 3
$$

$$
1 = 1 6
$$

$$
1 \cdot 1 3
$$

$$
1 = 1 1
$$

$$
1 \cdot 1 9
$$

$$
1 = 1 5
$$

$$
\begin{array}{l} 1 = 1 7 \\ 1 = 1 4 \end{array}
$$

$$
1 = 1 6
$$

$$
1 = 1 8
$$

,MAIN, MACRO V23.02 6-JUN-77 02:03:57 PAGE C-1
CROSS REFERENCE TABLE (CREF V01-05)

$$
\begin{array}{c} \text {ABS.} \\ \text {PPOG} \end{array}
$$

$$
\begin{array}{c} \partial = \partial \\ \partial = \partial \\ 1 = 7 \end{array}
$$

,MAIN, MACPO V04.00 6-JUN-79 001:3157 PAGE F-1 CROSS REFERENCE TABLE (CREF V01-PS)

$$
1 \circ 6   1 \circ 6
$$

$$
\begin{array}{c} 1 = 9 \\ 1 = 9 \end{array}
$$

$$
\begin{array}{c} 1 \div 1 2 \\ 1 \div 1 2 \end{array}
$$

$$
1 - 1 5
$$

$$
1 = 1 7
$$

## 12.6 MACRO-11 Error Codes

The MACRO-11 system prints diagnostic error codes as the first character of a source line on which the assembler detects an error. This error code identifies the type of error; for example, a code of M indicates a multiple definition of a label. Table 12-6 shows the error codes that might appear on an assembly listing. For detailed information on error code interpretation and debugging, see the PDP-11 MACRO-11 Language Reference Manual.

## Table 12-6: MACRO-11 Error Codes

<table><tr><td>Error Code</td><td>Meaning</td></tr><tr><td rowspan="10">A</td><td>Addressing or relocation error. This code can be generated by any of the following:</td></tr><tr><td>1. A conditional branch instruction target that is too far above or below the current statement. Conditional branch targets must be within -128 to -127 (decimal) words of the instruction.</td></tr><tr><td>2. A statement that makes an invalid change to the current location counter. For example, a statement that forces the current location counter to cross a .PSECT boundary can generate this code.</td></tr><tr><td>3. A statement that contains an invalid address expression. For example, an absolute address expression that has a global symbol, relocatable value, or complex relocatable value can generate this code. The directives .BLKB, .BLKW, and .REPT must have an absolute value or an expression that reduces to an absolute value.</td></tr><tr><td>4. Separate expressions in the statement that are not separated by commas.</td></tr><tr><td>5. A global definition error. If .ENABL GBL is set, MACRO-11 scans the symbol table at the end of the first pass and marks any undefined symbols as global references. If one of these symbols is subsequently defined in the second pass, a general addressing error occurs.</td></tr><tr><td>6. A global assignment statement that contains a forward reference to another symbol.</td></tr><tr><td>7. An expression that defines the value of the current location counter and contains a forward reference.</td></tr><tr><td>8. An invalid argument for an assembler directive</td></tr><tr><td>9. An unmatched delimiter or invalid argument construction.</td></tr><tr><td>B</td><td>Instruction or word data is being assembled at an odd address. The system increments the location counter by 1, and continues.</td></tr><tr><td>D</td><td>A nonlocal label is defined more than once, specifically in an earlier statement.</td></tr><tr><td>E</td><td>The .END assembler directive at the end of the source input is missing. The system supplies an .END statement and completes the current assembly pass.</td></tr><tr><td>I</td><td>MACRO-11 has detected one or more invalid characters. A question mark (?) replaces each invalid character on the assembly listing, and MACRO-11 continues after ignoring the character.</td></tr><tr><td>L</td><td>An input line is longer than 132 characters. In particular, this error occurs when the expansion of a macro causes excessive substitution of real arguments for dummy arguments.</td></tr><tr><td>M</td><td>A label is the same as an earlier label (multiple definition of a label). For example, two labels whose first six characters are identical can generate this error.</td></tr><tr><td>N</td><td>A number is not in the current program radix. MACRO-11 processes this number as a decimal value.</td></tr><tr><td>O</td><td>Op-code error. Exceeding the permitted nesting level for conditional assemblies causes this error. Attempting to expand a macro that remains unidentified after an .MCALL search can also generate this code.</td></tr><tr><td>P</td><td>Phase error. The definition or value of a label differs from one assembler pass to the next, or a local symbol occurs more than once in a local symbol block.</td></tr><tr><td>Q</td><td>Questionable syntax. For example, missing arguments, too many arguments, or an incomplete instruction scan can generate this error code.</td></tr><tr><td>R</td><td>Register-type error. For example, if the source program attempts an invalid reference to a register, the assembler can gene rate this error code.</td></tr><tr><td>T</td><td>Truncation error. A number that generates more than 16 bits in a word, or an expression in a .BYTE directive or trap instruction, can cause this error code.</td></tr><tr><td>U</td><td>Undefined symbol. The assembler assigns the undefined symbol a constant zero value.</td></tr><tr><td>Z</td><td>Incompatible instruction. This code is a warning that the instruction is not defined for all PDP-11 hardware configurations.</td></tr></table>
