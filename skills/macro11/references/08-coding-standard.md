# MACRO-11 Reference: App.E DEC sample coding standard (line format, naming, module layout, forbidden/recommended practice)

Source: DEC PDP-11 MACRO-11 Language Reference Manual, AA-5075A-TC (Aug 1977). OCR-converted; code examples may have lost alignment, and a few table rows/headings were dropped by OCR.

Contents:
- APPENDIX E SAMPLE CODING STANDARD
- E.1 INTRODUCTION
- E.2 LINE FORMAT
- E.3 COMMENTS
- E.4 NAMING STANDARDS
- E.4.1 Register Standards
- E.4.2 Processor Priority
- E.4.3 Other Symbols
- E.4.4 Using the Standard Symbolics
- E.4.5 Symbols\*
- E.4.5.2 Symbol Examples
- E.5 PROGRAM MODULES
- E.5.1 General Comments on Programs
- E.5.2 The Module Preface
- E.5.3 Formatting the Module Preface
- E.5.4 Modularity
- E.6 FORMATTING STANDARDS
- E.6.1 Program Flow
- E.6.2 Common Exits
- E.6.3 Code with Interrupts Inhibited
- E.7 PROGRAM SOURCE FILES
- E.8 FORBIDDEN INSTRUCTION USAGE
- E.9 RECOMMENDED CODING PRACTICE
- E.9.1 Conditional Branches
- E.10 PDP-11 VERSION NUMBER STANDARD
- E.10.1 Displaying the Version Identifier
- E.10.2 Use of the Version Number in the Program

---

## APPENDIX E SAMPLE CODING STANDARD

### E.1 INTRODUCTION

Standards eliminate variability and the requirement to make a decision. Much of the difficulty in establishing standards stems from the notion that they should be optimal. However, to be successfully applied, standards must represent an agreement on certain aspects of the programming process.

This Appendix contains DIGITAL's PDP-11 Program Coding Standard. It is suggested that this be used as a model to assist users in preparing standards for their own installations.

### E.2 LINE FORMAT

All source lines shall consist of from one to a maximum of eighty characters (not including the audit trail added by SLIPR (SLP in RSX-11M) editor. This program is described in the applicable RSX-11M or RSX-11D Utilities Manual or in the IAS Editing Utilities Reference Manual (see Section 0.3 in the Preface).

Assembly language code lines shall have the following format:

1. Label Field - if present, the label shall start at tab stop 0 (column 1).

2. Operation field - the operation field shall start at tab stop 1 (column 9).

3. Operand field - the operand field shall start at tab stop 2 (column 17).

4. Comments field - the comments field shall start at tab stop 4 (column 33) and may continue to column 80.

Comment lines that are included in the code body shall be delimited by a line containing only a leading semicolon. The comment itself contains a leading semicolon and starts in column 3. Indents shall be 1 tab.

If the operand field extends beyond tab stop 4 (column 33) simply leave a space and start the comment. Comments which apply to an instruction but require continuation should always line up with the character position which started the comment.

```txt
E.4.1.1 General Purpose Registers - Only the following names are permitted as register names; and may not be used for any other purpose:
R0=%0                      ;REG 0
R1=%1                     ;REG 1
R2=%2                     ;REG 2
R3=%3                     ;REG 3
R4=%4                     ;REG 4
R5=%5                     ;REG 5
SP=%6                     ;STACK POINTER (REG 6)
PC=%7                     ;PROGRAM COUNTER (REG 7)
```

**SAMPLE CODING STANDARD**

### E.3 COMMENTS

Comment all coding to convey the global role of an instruction, rather than simply a literal translation of the instruction into English. In general this will consist of a comment per line of code. If a particularly difficult, obscure, or elegant instruction sequence is used, a paragraph of comments must immediately precede that section of code.

Preface text, which describes formats, algorithms, program-local variables, etc., will be delimited by the character sequence ;+ at the start of the text and ;- at the end; these delimiters facilitate automated extraction of narrative commentary. The comment itself will start in column 3.

For example:

```prolog
;+
; THE INVERT ROUTINE ACCEPTS
; A LIST OF RANDOM NUMBERS AND
; APPLIES THE KOLMOGOROV ALGORITHM
; TO ALPHABETIZE THEM.
;-
```

### E.4 NAMING STANDARDS

### E.4.1 Register Standards

E.4.1.2 Hardware Registers - These registers must be named identically to the hardware definition. For example, FS and SWR.

E.4.1.3 Device Registers - These are symbolically named identically to the hardware notation. For example, the control status register for the RK disk is RKCS. Only this symbolic name may be used to refer to this register.

### E.4.2 Processor Priority

Testing or altering the processor priority is done using the symbols

$$
\mathrm{PRU}, \mathrm{PR1}, \mathrm{PR2}, \dots \dots . \mathrm{PR7}
$$

which are equated to their corresponding priority bit pattern.

### E.4.3 Other Symbols

Frequently-used bit patterns such as CR and LF will be made conventional symbolics on an as-needed basis.

### E.4.4 Using the Standard Symbolics

The register standards will be defined within the assembler. All other standard symbols will appear in a file and will be linked prior to program execution.

### E.4.5 Symbols\*

E.4.5.1 Global Symbols - Global symbols should be easily recognized by their format. The following standards apply and completely define symbol standards for PDP-11 Medium/Large software products.

| symbol | pos-1 | pos-2 | pos-3 | pos-4 | pos-5 | pos-6 | length |
| --- | --- | --- | --- | --- | --- | --- | --- |
| non-glbl-sym | letter | a-num/null | a-num/null | a-num/null | a-num/null | a-num/null | >=1 |
| glbl-sym | $/. | a-num/null | a-num/null | a-num/null | a-num/null | a-num/null | >=1 |
| glbl-offset | letter | $/. | a-num | a-num/null | a-num/null | a-num/null | >=3 |
| glbl-bit-ptrn | letter | a-num | $/. | a-num/ | a-num/null | a-num/null | >=4 |
| local-sym | number* | $ |  |  |  |  | >=2 |

\* Symbols that are branch targets are also called labels, but we will always use the term "symbol".

\*\* Number is in the range 0<number<65535.

\*\*\* The use of \$ or . for global names is reserved for DEC-supplied software.

where:

a-num                  is an alphanumeric character.
non-glbl-sym       are non-global symbols.
local-sym             local symbols, as defined by
                    MACRO-11.
glbl-sym               are global symbols (addresses).
glbl-offset         are global offsets (absolute
                    quantities).
glbl-bit-ptrn       are global bit patterns.

A program never contains a .GLOBL statement without showing cause.

### E.4.5.2 Symbol Examples

Non-Global Symbols
    AlB
    ZXCJ1
    INSRT

Global Address Symbols
    \$JIM
    .VECTR
    \$SEC

Global Absolute Offset Symbols

A\$JIM
A\$XT
A.ENT

Global Bit Pattern Symbols
    A1\$20
    B3.6
    JI.M

Local Symbols
37\$
271\$
6\$

E.4.5.3 Program-Local Symbols - Self-relative address arithmetic (.+n) is absolutely forbidden in branch instructions; its use in other contexts must be avoided if at all possible and practical.

Target symbols for branches that exist solely for positional reference will use local symbols of the form

<num> \$ :

Use of non-local symbols is restricted, within reason, to those cases where reference to the code occurs external to the code. Local-symbols are formatted such that the numbers proceed sequentially down the page and from page to page.

E.4.5.4 Macro Names - The last two characters (with the last character possibly being null) have special significance. The next to last character is a \$, the last, a character specifying the mode of the macro.

For example, in the three macro forms in-line, stack, and p-section, the in-line form has no suffix, the stack has an <S>, and the p-section a <C>. Thus the RSX Queue I/O macro can be written as any of

QIO\$

QIO\$\$

QIO\$C

depending on the form required. These are not reserved letters. Only the form of the name is standard.

### E.5 PROGRAM MODULES

### E.5.1 General Comments on Programs

In our software, a program provides a single distinct function. No limits exist on size, but the single function limitation should make modules larger than 1K a rarity. Since any software may eventually exploit the virtual memory capacity of the 11/40 and 11/45, programs should make every attempt to maintain a dense reference locus (do not promiscuously branch over page boundaries or over a large absolute address distance).

All code is read-only. Code and data areas are distinct and each contains explanatory text. Read-only data should be segregated from read-write data.

### E.5.2 The Module Preface

Each program module in the system shall exist as a separate file. The file name will reflect the name of the module and the file type shall be of the form 'NNN'. The 'NNN' signifies the edit number or the version number. The version number shall be changed only when a new base level is created. Furthermore, if no corrections are made to a file from one base level to the next, the version number will not be changed. The availability of File Control Services and File Control Primitives will greatly simplify version number maintenance. Program modules adhere to a strict format. This format adds to the readability and understandability of the module. The following sections are included in each module:

    For the Code Section:

1. A .TITLE statement that specifies the name of the module. If a module contains more than one routine, subtitles may be used.

2. An .IDENT statement specifying the version number. The PDP-11 version number standard appears in section E.10.

3. A .PSECT statement that defines the program section in which the module resides.

    4. A copyright statement, and the disclaimer.

COPYRIGHT (C) 1976
DIGITAL EQUIPMENT CORPORATION, MAYNARD, MASS.

THIS SOFTWARE IS FURNISHED UNDER A LICENSE FOR USE ONLY ON A SINGLE COMPUTER SYSTEM AND MAY BE COPIED ONLY WITH THE INCLUSION OF THE ABOVE COPYRIGHT NOTICE. THIS SOFTWARE, OR ANY OTHER COPIES THEREOF, MAY NOT BE PROVIDED OR OTHERWISE MADE AVAILABLE TO ANY OTHER PERSON EXCEPT FOR USE ON SUCH SYSTEM AND TO ONE WHO AGREES TO THESE LICENSE TERMS. TITLE TO AND OWNERSHIP OF THE SOFTWARE SHALL AT ALL TIMES REMAIN IN DEC.

THE INFORMATION IN THIS DOCUMENT IS SUBJECT TO CHANGE WITHOUT NOTICE AND SHOULD NOT BE CONSTRUED AS A COMMITMENT BY DIGITAL EQUIPMENT CORPORATION.

DEC ASSUMES NO RESPONSIBILITY FOR THE USE OR RELIABILITY OF ITS SOFTWARE ON EQUIPMENT WHICH IS NOT SUPPLIED BY DEC.

5. The version number of the file.

The PDP-11 version number standard is described in section E.10.

6. The name of the principal author and the date on which the module was first created.

7. The name of each modifying author and the date of modification. Names and modification dates appear one per line and in chronological order.

8. A brief statement of the function of the module.

Note: Items 1-8 should appear on the same page.

9. A list of the definitions of all equated local symbols used in the module. These definitions appear one per line and in alphabetical order.

10. All local macro definitions, preferably in alphabetical order by name.

    11. All local data. The data should indicate

a. Description of each element (type, size, etc.)

b. Organization (functional, alpha, adjacent, etc.)

c. Adjacency requirements

12. A more detailed definition of the function of the module.

13. A list of the inputs expected by the module. This includes the calling sequence if non-standard, condition code settings, and global data settings.

14. A list of the outputs produced as a result of entering this module. These include delivered results, condition code settings, but not side effects. (All these outputs are visible to the caller.)

15. A list of all effects (including side effects) produced as a result of entering this module. Effects include alterations in the state of the system not explicitly expected in the calling sequence, or those not visible to the caller.

16. The module code.

### E.5.3 Formatting the Module Preface

Rules:

1. The first eight items appear on the same page and will not have explicit headings. Item 3 may be omitted if the blank p-section is being used.

2. Headings start at the left margin\*; descriptive text is indented 1 tab position.

3. Items 7-14 will have headings which start at the left margin, preceded and followed by lines containing only a leading <;>. Items which do not apply may be omitted.

A template for the module preface follows.

FILE-EXAMPL.S01

.TITLE      EXAMPLE
.IDENT     /01/
.PSECT     KERNEL

```txt
COPYRIGHT (C) 1976
DIGITAL EQUIPMENT COPORATION, MAYNARD, MASS.
```

THIS SOFTWARE IS FURNISHED UNDER A LICENSE FOR USE ONLY ON A SINGLE COMPUTER SYSTEM AND MAY BE COPIED ONLY WITH THE INCLUSION OF THE ABOVE COPYRIGHT NOTICE. THIS SOFTWARE, OR ANY OTHER COPIES THEREOF, MAY NOT BE PROVIDED OR OTHERWISE MADE AVAILABLE TO ANY OTHER PERSON EXCEPT FOR USE ON SUCH SYSTEM AND TO ONE WHO AGREES TO THESE LICENSE TERMS. TITLE TO AND OWNERSHIP OF THE SOFTWARE SHALL AT ALL TIMES REMAIN IN DEC.

THE INFORMATION IN THIS DOCUMENT IS SUBJECT TO CHANGE WITHOUT NOTICE AND SHOULD NOT BE CONSTRUED AS A COMMITMENT BY DIGITAL EQUIPMENT CORPORATION.

\*The left margin consists of a <;> a <space> then the heading, so the text of the heading begins in column 3.

```asm
; DEC ASSUMES NO RESPONSIBILITY FOR THE USE OR RELIABILITY OF
; ITS SOFTWARE ON EQUIPMENT WHICH IS NOT SUPPLIED BY DEC.
;
; VERSION 01
;
; JOE PASCUSNIK 1-JAN-72
;
; MODIFIED BY:
;
; RICHARD DOE 21-JAN-73
;
; SPENCER THOMAS 12-JUN-73
;
; Brief statement of the module's function
;
; EQUATED SYMBOLS
;
List equated symbols
;
; LOCAL MACROS
;
Local Macros
;
; LOCAL DATA
;
Local data
;+
; Module function-details
;
; INPUTS:
;
; Description of inputs
;
; OUTPUTS:
;
; Description of outputs
;
; EFFECTS:
;
; Description of effects
;-
Begin Module Code
```

### E.5.4 Modularity

No other characteristic has more impact on the ultimate engineering success of a system than does modularity. Modularity for PDP-11 Software Engineering's products consists of the application of the single-function philosophy described in section E.5.1, and adherence to a set of calling and return conventions.

E.5.4.1 Calling Conventions (Inter-Module) - The following calling conventions must be observed.

    Transfer of Control

Macros will exist for call and return. The actual transfer will be via a JSR PC instruction. For register save routines, a JSR Rn,SAVE will be permitted.

The CALL macro is:

CALL     subr-name

The RETURN macro is:

**RETURN**

Register Conventions

On entry, a subroutine minimally saves all registers it intends to alter except result registers. On exit it restores these registers. (State preservation is assumed across calls.)

    Argument Passing

Any registers may be used, but their use should follow a coherent pattern. For example, if passing three arguments, pass them in R0, R1 and R2 rather than R0, R2, R5. Saving and restoring occurs in one place.

E.5.4.2 Exiting - All subroutine exits occur through a single RETURN macro.

E.5.4.3 Intra-Module Calling Conventions - Designer optional, but consistency favors a calling sequence identical to that of the inter-module sequence.

E.5.4.4 Success/Failure Indication - The C bit will be used to return the success/failure indicator, where success equals 0, and failure equals 1. The argument registers can be used to return values or additional success/failure data.

E.5.4.5 Module Checking Routines - Modules are responsible for verifying the validity of arguments passed to them. The design of a module's calling sequence should aim at minimizing the validity checks by minimizing invalid combinations. Programmers may add test code to perform additional checks during checkout. All code should aim at discovering an error as close (in terms of instruction executions) to its occurrence as possible.

### E.6 FORMATTING STANDARDS

### E.6.1 Program Flow

Programs will be organized on the listing such that they flow down the page, even at the cost of an extra branch or jump.

For example:

[figure from original manual omitted]

shall appear on the listing as:

<table><tr><td rowspan="2"></td><td colspan="2">TST</td></tr><tr><td>BNE</td><td>BBB</td></tr><tr><td rowspan="5">AAA:</td><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td>BR</td><td>CMN</td></tr><tr><td rowspan="2">BBB:</td><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td rowspan="3">CMN:</td><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td> $\cdots$ </td><td> $\cdots$ </td></tr></table>

Rather than:

<table><tr><td rowspan="2"></td><td colspan="2">TST</td></tr><tr><td>BNE</td><td>BBB</td></tr><tr><td rowspan="3">AAA:</td><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td rowspan="3">CMN:</td><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td rowspan="5">BBB:</td><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td> $\cdots$ </td><td> $\cdots$ </td></tr><tr><td>BR</td><td>CMN</td></tr></table>

```txt
will appear on the listing as:
PR1: .... ....
.... ....
.... ....
BR EXIT
PR2: .... ....
.... ....
.... ....
BR EXIT
PR3: .... ....
.... ....
.... ....
BR EXIT
PR4: .... ....
.... ....
.... ....
.... ....
EXIT:
And not as:
PR1: .... ....
.... ....
.... ....
EXIT: .... ....
.... ....
.... ....
PR2: .... ....
.... ....
.... ....
BR EXIT
PR3: .... ....
.... ....
.... ....
BR EXIT
PR4: .... ....
.... ....
.... ....
BR EXIT
```

### E.6.2 Common Exits

A common exit appears as the last code sequence on the listing. Thus the flow chart:

[figure from original manual omitted]

### E.6.3 Code with Interrupts Inhibited

Code that is executed with interrupts inhibited, shall be flagged by a three semicolon (;;;) comment delimiter. For example:

```asm
..ERTZ:
;ENABLE BY RETURNING
;BY SYSTEM SUBROUTINES,
BIS #PR7,PS ;;; INHIBIT INTERRUPTS
BIT #PR7,+2 (SP) ;;; C
BEQ 10$ ;;; O
RTT ;;; M
10$: ;;; M
...... .... ;;; E
...... .... ;;; N
...... .... ;;; T
...... .... ;;; S
```

### E.7 PROGRAM SOURCE FILES

Source creation and maintenance shall be done in base levels. A base level is defined as a point at which the program source files have been frozen. From the freeze point to the next base level, corrections will not be made directly to the base level itself. Rather a file of corrections shall be accumulated for each file in the base level. Whenever an updated source file is desired, the correction file will be applied to the base file.

The accumulation of corrections shall proceed until a logical breaking point has occurred (i.e. a milestone or significant implementation point has been reached). At this time all accumulated corrections shall be applied to the previous base level to create a new base level. Correction files will then be started for the new base level.

### E.8 FORBIDDEN INSTRUCTION USAGE

1. The use of instructions or index words as literals of the previous instruction. For example:

    MOV @PC,Register

uses the bit clear instruction as a literal. This may seem to be a very "neat" way to save a word but what about maintaining a program using this trick? To compound the problem, it will not execute properly if I/D space is enabled on the 11/45. In this case @PC is a D bank reference.

2. The use of the MOV instruction instead of a JMP instruction to transfer program control to another location. For example:

    MOV #ALPHA,PC

transfers control to location ALPHA. Besides taking longer to execute (2.3 microseconds for MOV vs. 1.2 for JMP) the use of MOV instead of JMP makes it nearly impossible to pick up someone else's program and tell where transfers of control

take place. What if one would like to get a jump trace of the execution of a program (a move trace is unheard of)? As a more general issue, perhaps even other operations such as ADD and SUB from PC should be discouraged. Possibly one or two words can be saved by using these operations but how many such occurrences are there?

3. The seemingly "neat" use of all single word instructions where one double-word instruction could be used and would execute faster and would not consume additional memory. Consider the following instruction sequence:

$$
\mathrm{CMP} \quad - (\mathrm{R1}), (- \mathrm{R1})
$$

$$
\mathrm{CMP} \quad - (\mathrm{Rl}), - (\mathrm{Rl})
$$

The intent of this instruction sequence is to subtract 8 from register R1 (not to set condition codes). This can be accomplished in approximately 1/3 the time via a SUB instruction (9.4 vs. 3.8 microseconds) at no additional cost in memory space. Another question here is also, what if R1 is odd? SUB always wins since it will always execute properly and is always faster!

### E.9 RECOMMENDED CODING PRACTICE

### E.9.1 Conditional Branches

When using the PDP-11 conditional branch instructions, it is imperative that the correct choice be made between the signed and the unsigned branches.

| SIGNED | UNSIGNED |
| --- | --- |
| BGE | BHIS (BCC) |
| BLT | BLO |
| BGT | BHI |
| BLE | BLOS (BCS) |

A common pitfall is to use a signed branch (e.g. BGT) when comparing two memory addresses. All goes well until the two addresses have opposite signs; that is, one of them goes across the 16K (100000(8)) bound. This type of coding error usually shows itself as a result of re-linking at different addresses and/or a change in size of the program.

### E.10 PDP-11 VERSION NUMBER STANDARD

The PDP-11 Version Number Standard applies to all modules, parameter files, complete programs, and libraries which are written or caused to be written, as part of the PDP-11 Software Development effort. It is used to provide unique identification of all released, pre-released, and in-house software.

It is limited in that, as currently specified, only six characters of identification are used. Future implementations of the Macro Assembler, linker, and librarian should provide for at least nine

characters, and possibly twelve. It is expected that this standard will be enhanced as the need arises.

```txt
Version Identifier = <form> <version> <edit> <patch>
```

<form> Used to identify a particular form of a module or program, where applicable, as in the case of LINK-11. One alphabetic character, if used, and null (i.e., a binary 0) if not used.

<version> Used to identify the release, or generation, of a program. Two decimal digits, starting at 00, and incremented at the discretion of the project in order to reflect what, in their opinion, is a major change.

<edit> Used to identify the level to which a particular release, or generation, of a program or module has been edited. An edit is defined to be an alteration to the source form. Two decimal digits, beginning at 01, and incremented with each edit; null if no edits.

<patch> Used to identify the level to which a particular release, or generation, of a program or module has been patched. A patch is defined as an alteration to a binary form. One alphabetic character, starting at B, and running sequentially toward Z, each time a set of patches is released; null if no patches.

These fields are interrelated. When <version> is changed, then <patch> and <edit> must be reset to nulls. It is intended that when <edit> is incremented, then <patch> will be re-set to null, because the various bugs have been fixed.

### E.10.1 Displaying the Version Identifier

The visible output of the version identifier should appear as:

<key-letter> <form> <version> - <edit> <patch>,

where the following Key Letters have been identified:

```txt
V    released or frozen version
X    in-house experimental version
Y    field test, pre-release, or in-house release version
```

Note that 'X' corresponds roughly to individual support, 'Y' to group support, and 'V' to company support.

The dash which separates <version> from <edit> is used only if <edit> and/or <patch> is not null. When a version identifier is displayed as part of program identification, then the format is:

```html
Program
    <space><key-letter><form><version>-<edit><patch>
Name
```

Examples:

PIP X03
LINK VB04-C
MACRO Y05-01

### E.10.2 Use of the Version Number in the Program

All sources must contain the version number in an .IDENT directive. For programs (or libraries) which consist of more than one module, each individual module will follow this version number standard. The version number of the program or library is not necessarily related to the version numbers of the constituent modules; it is perfectly reasonable, for example, that the first version of a new FORTRAN library, V00, contain an existing SIN routine, say V05-01.

Parameter files are also required to contain the version number in an .IDENT directive. Because the assembler records the last .IDENT seen, parameter files must precede the program.

Entities which consist of a collection of modules or programs, e.g., the FORTRAN Library, will have an identification module in the first position. An identification module exists solely to provide identification, and normally consists of something like:

;OTS IDENTIFICATION

.TITLE FTNLIB

.IDENT /003010/

.END
