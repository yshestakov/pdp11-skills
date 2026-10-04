# MACRO-11 Reference: Ch.6.6-6.10 .END/.EOT, .LIMIT, .PSECT/.ASECT/.CSECT, .GLOBL, conditional assembly (.IF/.IFF/.IFT/.IIF)

Source: DEC PDP-11 MACRO-11 Language Reference Manual, AA-5075A-TC (Aug 1977). OCR-converted; code examples may have lost alignment, and a few table rows/headings were dropped by OCR.

Contents:
- 6.6 TERMINATING DIRECTIVES
- 6.6.1 .END Directive
- 6.6.2 .EOT Directive
- 6.7 PROGRAM BOUNDARIES DIRECTIVE: .LIMIT
- 6.8 PROGRAM SECTIONING DIRECTIVES
- 6.8.1 .PSECT Directive
- 6.8.2 .ASECT and .CSECT Directives
- 6.9 SYMBOL CONTROL DIRECTIVE: .GLOBL
- 6.10 CONDITIONAL ASSEMBLY DIRECTIVES
- 6.10.1 Conditional Assembly Block Directives: .IF, .ENDC
- 6.10.2 Subconditional Assembly Block Directives: .IFF, .IFT, .IFTF
- 6.10.3 Immediate Conditional Assembly Directive: .IIF
- 6.10.4 PAL-11R Conditional Assembly Directives

---

### 6.6 TERMINATING DIRECTIVES

#### 6.6.1 .END Directive

The .END directive indicates the logical end of the source input, and takes the following form:

where: exp represents an optional expression value which, if present, indicates the program-entry point, i.e., the transfer address at which program execution is to begin.

When MACRO-11 encounters a valid occurrence of the .END directive, it terminates the current assembly pass. Any additional text beyond this point in the current source file, as well as in additional source files identified in the command line, will be ignored.

When creating an image consisting of several object modules, only one object module may be terminated with an .END exp statement specifying the starting address. All other object modules must be terminated with an .END statement without an address argument; otherwise, a diagnostic message will be issued at link time. If no starting address is specified in any of the object modules, image execution will begin at location 1 of the image and immediately fault because of an odd addressing error.

The .END statement must not be used within a macro expansion or a conditional assembly block; if it is so used, it is flagged with an error code (0) in the assembly listing. The .END statement may be used, however, in an immediate conditional statement (see Section 6.10.2).

If the source program input is not terminated with an .END directive, an error code (E) results in the assembly listing.

#### 6.6.2 .EOT Directive

Under RSX-11, RT-11, and IAS operating systems, the MACRO-11 .EOT directive is ignored and simply treated as a directive without effect, i.e., as a no-op.

### 6.7 PROGRAM BOUNDARIES DIRECTIVE: .LIMIT

It is often desirable to know the upper and lower address boundaries of the image. When the .LIMIT directive is specified in the source program, MACRO-11 effectively generates the following instruction:

    .BLKW 2

causing two storage words to be reserved in the object module. Later, at link time, the lowest address in the load image is inserted into the first reserved word, and the address of the first free word following the image is inserted into the second reserved word.

During linking, the size of the image is rounded upward to the nearest 2-word boundary.

**GENERAL ASSEMBLER DIRECTIVES**

For a discussion of memory allocation and mapping, refer to the applicable system manual (see Section 0.3 in the Preface).

### 6.8 PROGRAM SECTIONING DIRECTIVES

The MACRO-ll program sectioning directives are used to declare names for program sections and to establish certain program section attributes essential to the linking processing.

#### 6.8.1 .PSECT Directive

The .PSECT directive allows absolute control over the memory allocation of a program at link time, because any program attributes established through this directive are passed to the linker.

For example, if you are writing programs for a multi-user environment, a program section containing pure code (instructions only) or a program section containing impure code (data and instructions) may be explicitly declared through the .PSECT directive. Furthermore, these program sections may be explicitly declared as read-only code, qualifying them for use as protected, reentrant programs.

The advantages gained through sectioning programs in this manner therefore relate primarily to control of memory allocation, program modularity, and more effective partitioning of memory. Refer to the applicable system manual for a discussion of memory allocation (see Section 0.3 in the Preface).

The .PSECT directive is formatted as follows:

    .PSECT name,arg1,arg2,...argn

where: name represents the symbolic name of the program section, as described in Table 6-3.

, represents any legal separator (comma, tab and/or space).

arg1, represent one or more of the legal symbolic arguments defined for use with the .PSECT directive, as described in Table 6-3. The slash separating each pair of symbolic arguments listed in the table indicates that these optional arguments are mutually exclusive, i.e., one or the other, but not both, may be specified. Multiple arguments must be separated by a legal separating character. Any symbolic argument specified in the .PSECT directive other than those listed in Table 6-3 will cause that statement to be flagged with an error code (A) in the assembly listing.

Table 6-3
Symbolic Arguments of .PSECT Directive

| Argument | Default | Meaning |
| --- | --- | --- |
| NAME | Blank | Establishes the program section name, which is specified as one to six Radix-50 characters. If this argument is omitted, a comma must appear in place of the name parameter. The Radix-50 character set is listed in Section A.2 of Appendix A. |
| RO/RW | RW | Defines which type of access is permitted to the program section:RO=Read-Only AccessRW=Read/Write AccessNOTEIAS and RSX-11D set hardware protection for RO program sections. RSX-11M and RT-11 do not provide such protection. |
| I/D | I | Defines the program section as containing either instructions (I) or data (D). These attributes allow the linker to differentiate global symbols that are program entry-point instructions (I) from those that are data values (D). |
| GBL/LCL | LCL | Defines the scope of the program section, as subsequently interpreted at link time.In building single-segment nonoverlaid programs, the GBL/LCL arguments have no meaning, because the total memory allocation for the program will go into the root segment of the image. The GBL/LCL arguments apply only in the case of overlays.If an object module contains a local program section, then the storage allocation for that module will occur within the segment in which the module resides. Many modules can reference this same program section, and the memory allocation for each module is either concatenated or overlaid within the segment, depending on the argument of the program section (.PSECT) defining |

(continued on next page)

Table 6-3 (Cont.)
Symbolic Arguments of .PSECT Directive

| Argument | Default | Meaning |
| --- | --- | --- |
| GBL/LCL (cont'd) | LCL | its allocation requirements (see CON/OVR below). If an object module contains a global program section, the contributions to this program section are collected across segment boundaries, and the allocation of memory for that section will go into the segment nearest the root in which the first contribution to this program section appeared. (The term contribution implies an allocation of memory to the program section.) |
| ABS/REL | REL | Defines the relocatability attribute of the program section:ABS=Absolute (non-relocatable). When the ABS argument is specified, the program section is regarded at link time as an absolute module, thus requiring no relocation. The program section is assembled and loaded, starting at absolute virtual address 0.The location of data in absolute program sections must fall within the virtual memory limits of the segment containing the program section; otherwise, an error results at link time. For example, the following code, although valid at during assembly, may generate an error message if virtual location 100000 is outside the segment's virtual address space:.PSECT ALPHA,ABS.=.+100000.WORD XThe above coding assembles properly, but the resulting load address may be outside the respective segment's boundaries. In such cases, the linker recognizes this as an attempt to load data outside the image and responds with an error message.REL=Relocatable. When the REL argument is specified, the linker calculates a relocation bias and adds it to all references to locations within the program section, i.e., all references to the program section must have a relocation bias added to them to make them absolute. |

(Continued on next page)

    Table 6-3 (Cont.) Symbolic Arguments of .PSECT Directive

| Argument | Default | Meaning |
| --- | --- | --- |
| CON/OVR | CON | Defines the allocation requirements of the program section:CON=Concatenated. All program section contributions are to be concatenated with other references to this same program section in order to determine the total memory allocation requirement for this program section.OVR=Overlaid. All program section contributions are to be overlaid. Thus, the total allocation requirement for the program section is equal to the largest allocation request made by any individual contribution to this program section. |

The only argument in the .PSECT directive that is position-dependent is NAME. If it is omitted, a comma must be used in its place. For example, the directive:

    .PSECT ,GBL

shows a .PSECT directive with a blank name argument and the GBL argument. Default values (see Table 6-3) are assumed for all other unspecified arguments.

Once the attributes of a program section are declared through a .PSECT directive, MACRO-11 assumes that these attributes remain in effect for all subsequent .PSECT directives of the same name that are encountered within the module.

MACRO-11 provides for 256(10) program sections, as listed below:

1. One default absolute program section (. ABS.)

2. One default unnamed relocatable program section

3. Two-hundred-fifty-four named program sections.

The .PSECT directive enables the user to:

1. Create program sections (see Section 6.8.1.1)

2. Share code and data among program sections (see Section 6.8.1.2).

For each program section specified or implied, MACRO-11 maintains the following information:

1. Program section name

2. Contents of the current location counter

3. Maximum location counter value encountered

4. Program section attributes, i.e., the .PSECT arguments described in Table 6-3 above.

6.8.1.1 Creating Program Sections - MACRO-11 automatically begins assembling source statements at relocatable zero of the unnamed program section, i.e., the first statement of a source program is always an implied .PSECT directive.

The first occurrence of a .PSECT directive with a given name assumes that the current location counter is set at relocatable zero. The scope of this directive then extends until a directive declaring a different program section is specified. Further occurrences of a program section name in subsequent .PSECT statements cause the resumption of assembly where that section previously ended. For example:

D: .WORD 0 ;PROGRAM SECTION AND CONTINUES ASSEM-
;BLY AT RELOCATABLE ADDRESS 6.

A given program section may be defined completely upon encountering its first .PSECT directive. Thereafter, the section can be referenced by specifying its name only, or by completely respecifying its attributes. For example, a program section can be declared through the directive:

    .PSECT ALPHA,ABS,OVR

and later referenced through the equivalent directive:

    .PSECT ALPHA

which requires no arguments.

By maintaining separate location counters for each program section, MACRO-11 allows the user to write statements that are not physically contiguous within the program, but that can be loaded contiguously following assembly, as shown in the following example.

|  | .PSECT | SECL,REL,RO | ;START A RELOCATABLE PROGRAM SECTION |
| --- | --- | --- | --- |
| A: | .WORD | 0 | ;NAMED SECL ASSEMBLED AT RELOCATABLE |
| B: | .WORD | 0 | ;ADDRESSES 0, 2, AND 4. |
| C: | .WORD | 0 |  |
| ST: | CLR | A | ;ASSEMBLE CODE AT RELOCATABLE |
|  | CLR | B | ;ADDRESSES 6 THROUGH 12. |
|  | CLR | C |  |
|  | .PSECT | SECA,ABS | ;START AN ABSOLUTE PROGRAM SECTION |
|  |  |  | ;NAMED SECA. ASSEMBLE CODE AT |
|  | .WORD | .+2,A | ;ABSOLUTE ADDRESSES 0 AND 2. |
|  | .PSECT | SECL | ;RESUME RELOCATABLE PROGRAM SECTION |
|  | INC | A | ;SECL. ASSEMBLE CODE AT RELOCATABLE |
|  | BR | ST | ;ADDRESSES 14 AND 16. |

All labels in an absolute program section are absolute; likewise, all labels in a relocatable section are relocatable. The current location counter symbol (.) is also relocatable or absolute when referenced in a relocatable or absolute program section, respectively.

Any labels appearing on a line containing a .PSECT (or .ASECT or .CSECT) directive are assigned the value of the current location counter before the .PSECT (or other) directive takes effect. Thus, if the first statement of a program is:

    A: .PSECT ALT,REL

the label A is assigned to relocatable address zero of the unnamed (or blank) program section.

It is not known during assembly where relocatable program sections will be loaded, therefore all references between relocatable sections in a single assembly are translated by MACRO-11 to references relative to the base of the referenced section. Thus, MACRO-11 provides the linker with the necessary information to resolve the linkages between various program sections. Such information is not necessary, however, when referencing an absolute program section, because all instructions in an absolute program section are associated with an absolute virtual address.

In the following example, references to the symbols X and Y are translated into references relative to the base of the relocatable program section named SEN.

<table><tr><td></td><td>.PSECT</td><td>ENT,ABS</td><td></td></tr><tr><td colspan="4">.=.+1000</td></tr><tr><td>A:</td><td>CLR</td><td>X</td><td>;ASSEMBLED AS CLR BASE OF ;RELOCATABLE SECTION + 10.</td></tr><tr><td></td><td>JMP</td><td>Y</td><td>;ASSEMBLED AS JMP BASE OF ;RELOCATABLE SECTION + 6.</td></tr><tr><td></td><td>.PSECT</td><td>SEN,REL</td><td></td></tr><tr><td></td><td>MOV</td><td>R0,R1</td><td></td></tr><tr><td></td><td>JMP</td><td>A</td><td>;ASSEMBLED AS JMP 1000.</td></tr><tr><td>Y:</td><td>HALT</td><td></td><td></td></tr><tr><td>X:</td><td>.WORD</td><td>0</td><td></td></tr></table>

**NOTE:**

In the preceding example, using a constant in conjunction with the current location counter symbol (.) in the form .=1000 would result in an error, because constants are always absolute and are always associated with the program's .ASECT (. ABS.). If the form .=1000 were used, a program section incompatibility would be detected. See Section 3.6 for a discussion of the current location counter.

6.8.1.2 Code or Data Sharing - Named relocatable program sections with the arguments GBL and OVR operate in the same manner as FORTRAN COMMON, i.e., program sections of the same name with the arguments GBL and OVR from different assemblies are all loaded at the same location at link time. All other program sections, i.e., those with the argument CON, are concatenated.

Note that no conflict exists between internal symbolic names and program section names, i.e., it is legal to use the same symbolic name for both purposes. Considering FORTRAN again, using the same symbolic name is necessary to accommodate the following statement:

    COMMON /X/ A,B,C,X

where the symbol X represents the base of the program section and also the fourth element of that section.

6.8.1.3 Memory Allocation Considerations - The assembler does not generate an error when a module ends at an odd location. This allows you to place odd length data at the end of a module. However, when several modules contain object code contributions to the same program section having the concatenate attribute (see Table 6-3), odd length modules (except the last) may cause succeeding modules to be linked starting at odd locations, thereby making the linked program unexecutable. To avoid this problem, code and data should be separated from each other and be placed in separately named program sections. This permits the linker to automatically begin each program section on an even address. Refer to the applicable system manual for further information on memory allocation of tasks (see Section 0.3 in the Preface).

#### 6.8.2 .ASECT and .CSECT Directives

IAS and RSX-11 assembly-language programs use the .PSECT and .ASECT directives exclusively, since the .PSECT directive provides all the capabilities of the .CSECT directive defined for other PDP-11 assemblers. MACRO-11 will accept both .ASECT and .CSECT directives, but assembles them as though they were .PSECT directives with the default attributes listed in Table 6-4. Also, compatibility exists between other MACRO-11 programs and the IAS/RSX-11 Task Builders, since the respective Task Builders recognize the .ASECT and .CSECT directives that appear in such programs and likewise assign the default values listed in Table 6-4.

Table 6-4
Non-IAS/RSX-11 Program Section Default Values

<table><tr><td rowspan="2">Attribute</td><td colspan="3">Default Value</td></tr><tr><td>.ASECT</td><td>.CSECT (named)</td><td>.CSECT (unnamed)</td></tr><tr><td>Name</td><td>.ABS.</td><td>name</td><td>Blank</td></tr><tr><td>Access</td><td>RW</td><td>RW</td><td>RW</td></tr><tr><td>Type</td><td>I</td><td>I</td><td>I</td></tr><tr><td>Scope</td><td>GBL</td><td>GBL</td><td>LCL</td></tr><tr><td>Relocation</td><td>ABS</td><td>REL</td><td>REL</td></tr><tr><td>Allocation</td><td>OVR</td><td>OVR</td><td>CON</td></tr></table>

The allowable syntactical forms of the .ASECT and .CSECT directives are:

.ASECT
.CSECT
.CSECT symbol

Note that the statement:

.CSECT JIM

is identical to the statement:

.PSECT JIM,GBL,OVR

because the .CSECT default values GBL and OVR are assumed for the named program section.

### 6.9 SYMBOL CONTROL DIRECTIVE: .GLOBL

MACRO-11 produces a relocatable object module and a listing file containing the assembly listing and symbol table. The linker joins separately-assembled object modules into a single executable image. During linking, object modules are relocated as a program function of the specified base of the module. The object modules are then linked via global symbols, such that a global symbol in one module, defined either by a global assignment operator (==), a global label operator (::), or the .GLOBL directive can be referenced from another module. Thus, all symbols which will be referenced by other program modules must be singled out as global symbols in the defining modules.

The .GLOBL directive is provided to define (and thus provide linkage to) symbols not otherwise defined as global symbols within a module. For example, if the .DSABL GBL directive is in effect (see Section 6.2), .GLOBL directives might be included in a source program to effect linkage to library routines. For a global symbol definition, the directive .GLOBL A,B,C is equivalent to:

A==expression (or A::)
B==expression (or B::)
C==expression (or C::)

Thus, the general form of the .GLOBL directive is:

.GLOBL sym1,sym2,...symn

where: sym1, represent legal symbolic names. When multiple sym2,... symbols are specified, they are separated by any symn legal separator (comma, space, and/or tab).

A .GLOBL directive may also embody a label field and/or a comment field.

At the end of assembly pass 1, MACRO-11 determines whether a given global symbol is defined within the current program module or whether it is to be treated as an external symbol. All internal symbols appearing within a given program must be defined at the end of assembly pass 1 or they will be assumed to be default global references. Refer to Section 6.2 for a description of enabling/disabling of global references.

In the example below, A and B are entry-point symbols. The symbol A has been explicitly defined as a global symbol by means of the .GLOBL directive, and the symbol B has been explicitly defined as a global label by means of the double colon (::). Since the symbol C is not defined as a label within the current assembly, it is an external (global) reference if .ENABL GBL is in effect.

; DEFINE A SUBROUTINE WITH 2 ENTRY POINTS WHICH CALLS AN
; EXTERNAL SUBROUTINE

.PSECT
.GLOBL A
MOV @(R5)+,R0
MOV #X,R1
JSR PC,C
RTS R5
MOV (R5)+,R1
CLR R2
BR X

External symbols can appear in the operand field of an instruction or MACRO-11 directive as a direct reference, as shown in the examples below:

CLR        EXT
.WORD    EXT
CLR        @EXT

External symbols may also appear as a term within an expression, as shown below:

CLR        EXT+A
.WORD     EXT-2
CLR        @EXT+A (R1)

It should be noted that an undefined external symbol cannot be used in the evaluation of a direct assignment statement or as an argument in a conditional assembly directive (see Sections 6.10.1 and 6.10.3).

### 6.10 CONDITIONAL ASSEMBLY DIRECTIVES

Conditional assembly directives allow you to include or exclude blocks of source code during the assembly process, based on the evaluation of stated condition tests within the body of the program. This capability allows several variations of a program to be generated from the same source code.

#### 6.10.1 Conditional Assembly Block Directives: .IF, .ENDC

The general form of a conditional assembly block is as follows:

.IF cond,argument(s) ;START CONDITIONAL ASSEMBLY BLOCK.
:

;RANGE OF CONDITIONAL ASSEMBLY BLOCK.

;END OF CONDITIONAL ASSEMBLY BLOCK.

where: cond represents a specified condition that must be met if the block is to be included in the assembly. The conditions that may be tested by the conditional assembly directives are defined in Table 6-5.

, represents any legal separator (comma, space, and/or tab).

argument(s) represent(s) the symbolic argument(s) or expression(s) of the specified conditional test. These arguments are thus a function of the specified condition to be tested (see Table 6-5).

range represents the body of code that is either included in the assembly or excluded, depending upon whether the specified condition is met.

.ENDC terminates the conditional assembly block. This directive must be present to end the conditional assembly block.

A condition test other than those listed in Table 6-5, an illegal argument, or a null argument specified in an .IF directive causes that line to be flagged with an error code (A) in the assembly listing.

Table 6-5

Legal Condition Tests for Conditional Assembly Directives

<table><tr><td colspan="2">Conditions</td><td rowspan="2">Arguments</td><td rowspan="2">Assemble Block If:</td></tr><tr><td>Positive</td><td>Complement</td></tr><tr><td>EQ</td><td>NE</td><td>Expression</td><td>Expression is equal to 0 (or not equal to 0).</td></tr><tr><td>GT</td><td>LE</td><td>Expression</td><td>Expression is greater than 0 (or less than or equal to 0).</td></tr></table>

Table 6-5 (Cont.)
Legal Condition Tests for Conditional Assembly Directives

<table><tr><td colspan="2">Conditions</td><td rowspan="2">Arguments</td><td rowspan="2">Assemble Block If:</td></tr><tr><td>Positive</td><td>Complement</td></tr><tr><td>LT</td><td>GE</td><td>Expression</td><td>Expression is less than 0 (or greater than or equal to 0).</td></tr><tr><td>DF</td><td>NDF</td><td>Symbolic argument</td><td>Symbol is defined (or not defined).</td></tr><tr><td>B</td><td>NB</td><td>Macro-type argument</td><td>Argument is blank (or non-blank).</td></tr><tr><td>IDN</td><td>DIF</td><td>Two macro-type arguments</td><td>Arguments are identical (or different).</td></tr><tr><td>Z</td><td>NZ</td><td>Expression</td><td>Same as EQ/NE.</td></tr><tr><td>G</td><td>L</td><td>Expression</td><td>Same as GT/LT.</td></tr></table>

NOTE

A macro-type argument (which is a form of symbolic argument), as shown below, is enclosed within angle brackets or denoted with an up-arrow construction (as described in Section 7.3.1).

<A,B,C>
^/124/

An example of a conditional assembly directive follows:

.IF EQ ALPHA+1 ;ASSEMBLE BLOCK IF ALPHA+1=0.
.
.
.ENDC

The two operators & and ! have special meaning within DF and NDF conditions, in that they are allowed in grouping symbolic arguments.

& Logical AND operator

! Logical inclusive OR operator

For example, the conditional assembly statement:

.IF DF SYM1 & SYM2
.
.
.
.ENDC

results in the assembly of the conditional block if the symbols SYM1 and SYM2 are both defined.

Nested conditional directives take the form:

```txt
Conditional Assembly Directive
Conditional Assembly Directive
.
.
.
.ENDC
.ENDC
```

For example, the following conditional directives:

```asm
.IF DF SYM1
.IF DF SYM2
.
.
.
.ENDC
.ENDC
```

can govern whether assembly is to occur. In the example above, if the outermost condition is unsatisfied, no deeper level of evaluation of nested conditional statements within the program occurs.

Each conditional assembly block must be terminated with an .ENDC directive. An .ENDC directive encountered outside a conditional assembly block is flagged with an error code (0) in the assembly listing.

MACRO-11 permits a nesting depth of 16(10) conditional assembly levels. Any statement that attempts to exceed this nesting level depth is flagged with an error code (O) in the assembly listing.

#### 6.10.2 Subconditional Assembly Block Directives: .IFF, .IFT, .IFTF

Subconditional directives may be placed within conditional assembly blocks to indicate:

1. The assembly of an alternate body of code when the condition of the block tests false.

2. The assembly of a non-contiguous body of code within the conditional assembly block, depending upon the result of the conditional test in entering the block.

3. The unconditional assembly of a body of code within a conditional assembly block.

The subconditional directives are described in detail in Table 6-6. If a subconditional directive appears outside a conditional assembly block, an error code (O) is generated in the assembly listing.

Table 6-6
Subconditional Assembly Block Directives

| Subconditional Directive | Function |
| --- | --- |
| .IFF | If the condition tested upon entering the conditional assembly block is false, the code following this directive, and continuing up to the next occurrence of a subconditional directive or to the end of the conditional assembly block, is to be included in the program. |
| .IFT | If the condition tested upon entering the conditional assembly block is true, the code following this directive, and continuing up to the next occurrence of a subconditional directive or to the end of the conditional assembly block, is to be included in the program. |
| .IFTF | The code following this directive, and continuing up to the next occurrence of a subconditional directive or to the end of the conditional assembly block, is to be included in the program, regardless of the result of the condition tested upon entering the conditional assembly block. |

EXAMPLE 1: Assume that symbol SYM is defined.

| .IF DF SYM | ;TESTS TRUE, SYM IS DEFINED. ASSEMBLE |
| --- | --- |
| . | ;THE FOLLOWING CODE. |
| . |  |
| .IFF | ;TESTS FALSE. SYM IS DEFINED. DO NOT |
| . | ;ASSEMBLE THE FOLLOWING CODE. |
| . |  |
| .IFT | ;TESTS TRUE. SYM IS DEFINED. ASSEM- |
| . | ;BLE THE FOLLOWING CODE. |
| . |  |
| .IFTF | ;ASSEMBLE FOLLOWING CODE UNCONDITION- |
| . | ;ALLY. |
| . |  |
| .IFT | ;TESTS TRUE. SYM IS DEFINED. ASSEM- |
| . | ;BLE REMAINDER OF CONDITIONAL ASSEM- |
| . | ;BLY BLOCK. |
| . |  |
| .ENDC |  |

EXAMPLE 2: Assume that symbol X is defined and that symbol Y is not defined.
    .IF DF X                      ;TESTS TRUE, SYMBOL X IS DEFINED.
    .IF DF Y                       ;TESTS FALSE, SYMBOL Y IS NOT DEFINED.
    .IFF                          ;TESTS TRUE, SYMBOL Y IS NOT DEFINED,
        .                           ;ASSEMBLE THE FOLLOWING CODE.
        .
        .
        .IFT                          ;TESTS FALSE, SYMBOL Y IS NOT DEFINED.
        .                           ;DO NOT ASSEMBLE THE FOLLOWING CODE.
        .
        .
    .ENDC
ENDC

EXAMPLE 3: Assume that symbol A is defined and that symbol B is not defined.
    .IF DF A                      ;TESTS TRUE. A IS DEFINED.
                   ;ASSEMBLE THE FOLLOWING CODE.
    MOV     A,R1
        .
        .
        .
    .IFF                          ;TESTS FALSE. A IS DEFINED. DO NOT
                   ;ASSEMBLE THE FOLLOWING CODE.
    MOV     R1,R0
        .
        .
        .
    .IF NDF B                      ;NESTED CONDITIONAL DIRECTIVE IS NOT
        .
        ;
    .
ENDC
ENDC

EXAMPLE 4: Assume that symbol X is not defined and that symbol Y is defined.
    .IF DF X                      ;TESTS FALSE. SYMBOL X IS NOT DEFINED.
                   ;DO NOT ASSEMBLE THE FOLLOWING CODE.
    .IF DF Y                      ;NESTED CONDITIONAL DIRECTIVE IS NOT
        .                     ;EVALUATED.
        .
        .
        .
    .IFF                          ;NESTED SUBCONDITIONAL DIRECTIVE IS
        .                     ;NOT EVALUATED.
        .
        .
    .IFT                          ;NESTED SUBCONDITIONAL DIRECTIVE IS
        .                     ;NOT EVALUATED.
        .
        .
    .ENDC
ENDC

#### 6.10.3 Immediate Conditional Assembly Directive: .IIF

An immediate conditional assembly directive provides a means for writing a l-line conditional assembly block. In using this directive, no terminating .ENDC statement is required, and the condition to be tested is completely expressed within the line containing the directive. Immediate conditional assembly directives are of the form:

.IIF cond, arg, statement

where: cond represents one of the legal condition tests defined for conditional assembly blocks in Table 6-5.

, represents any legal separator (comma, space, and/or tab).

arg represents the argument associated with the immediate conditional directive, i.e., an expression, symbolic argument, or macro-type argument, as described in Table 6-5.

' represents the separator between the conditional argument and the statement field. If the preceding argument is an expression, then a comma must be used; otherwise, a comma, space, and/or tab may be used.

statement represents the specified statement to be assembled if the condition is satisfied.

For example, the immediate conditional statement:

.IIF DF FOO,BEQ ALPHA

generates the code

BEQ ALPHA

if the symbol FOO is defined within the source program.

As with the .IF directive, a condition test other than those listed in Table 6-5, an illegal argument, or a null argument specified in an .IIF directive results in an error code (A) in the assembly listing.

#### 6.10.4 PAL-11R Conditional Assembly Directives

In order to maintain compatibility with programs developed under PAL-llR, the following conditionals remain permissible under MACRO-ll. It is advisable, however, to develop future programs using the format for MACRO-ll conditional assembly directives.

Directive     Arguments     Assemble Block if

.IFZ or .IFEQ expression expression=0
.IFNZ or .IFNE expression expression not equal 0
.IFL or .IFLT expression expression<0
.IFG or .IFGT expression expression>0
.IFLE expression expression is < or =0
.IFDF symbolic argument symbol is defined
.IFNDF symbolic argument symbol is undefined

The rules governing these directives are the same as for the MACRO-11 conditional assembly directives previously described.
