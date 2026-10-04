# MACRO-11 Reference: App.F Assembler virtual memory hints, App.G Writing position-independent code

Source: DEC PDP-11 MACRO-11 Language Reference Manual, AA-5075A-TC (Aug 1977). OCR-converted; code examples may have lost alignment, and a few table rows/headings were dropped by OCR.

## APPENDIX F ALLOCATING VIRTUAL MEMORY

This appendix is intended for the MACRO-11 user who wants to avoid the problem of thrashing, by optimizing the allocation of virtual memory. Users of smaller systems, particularly those with the 8K subset version of MACRO-11, should become thoroughly familiar with the conventions discussed herein. In this regard, Appendix F addresses the following topics:

1. General hints and space-saving guidelines

2. Macro definitions and expansions

3. Operational techniques.

The user is assumed to have pursued a policy of modular programming, as advised in Appendix E. In addition to the obvious advantages accruing from small, distinct, highly-functional bodies of code, one can usually avoid the problem of insufficient dynamic memory during assembly by practicing such a policy. Other suggestions as to how available memory can be best utilized are discussed in the following sections.

### F.1 GENERAL HINTS AND SPACE-SAVING GUIDELINES

Work-file memory is shared by a number of MACRO-11's tables, each of which is allocated space on demand (64K words of dynamically pageable storage are available to the assembler). The tables and their corresponding entry sizes are as follows:

1. User-defined symbols - five words.

2. Local symbols - four words.

3. Program sections - six words.

4. Macro names - four words.

5. Macro text - nine words.

6. Source files - six words.

In addition, several scratch pad tables are used during the assembly process, as follows:

1. Expression analysis - five words.

2. Object code generation - five words.

**ALLOCATING VIRTUAL MEMORY**

3. Macro argument processing - three words.

4. .MCALL argument processing - five words.

The above information can serve as a guide for estimating dynamic storage requirements and for determining ways to reduce such requirements.

For example, the use of local symbols whenever possible is highly encouraged, since their internal representation requires 25% less dynamic storage than that required for regular user-defined symbols. The usage of local symbols can often be maximized by extending the scope of local symbol blocks through the .ENABL LSB/.DSABL LSB MACRO-11 directives (see Sections 3.5 and 6.2).

Since MACRO-11 does not support a purge function, once a symbol is defined, it permanently occupies its dynamic memory allocation. Numerous instances occur during conditional assemblies and repeat loops when a temporarily assigned symbol is used as a count or offset indicator. If possible, the symbols so used should be re-used.

In keeping with the same principle, special treatment should be given to the definition of commonly-used symbols. Instead of simply appending a prefix file which defines all possibly-used symbols for each assembly, users are encouraged to group symbols into logical classes. Each class so grouped can then become a shortened prefix file or a macro in a library (see Section F.2 below). In either case, selective definition of symbolic assignments is achieved, resulting in fewer defined (but unreferenced) symbols.

An appropriate example of this idea is seen in the definition of standard symbols. The system macro library, for example, supplies several macros used to define distinct classes of symbols. These groupings and associated macro names are, as follows:

DRERR\$ - Directive return status codes

IOERR\$ - I/O return status codes

FILIO\$ - File-related I/O function codes

SPCIO\$ - Special I/O function codes

### F.2 MACRO DEFINITIONS AND EXPANSIONS

By far, dynamic storage is used most heavily for the storage of macro text. Upon macro definition or the issuance of an .MCALL directive, the entire macro body is stored, including all comments appearing in the macro definition. For this reason, comments should not be included as part of the macro text. An RSX-11 utility program (called SQZ for RSX-11D only) and a Librarian function switch (/SZ) are available to compress macro source text by removing all trailing blanks and tabs, blank lines, and comments. The system macro library (RSXMAC.SML) has already been compressed. User-supplied macro libraries (.MLB) and macro definition prefix files should also be compressed. For additional information regarding these two utility tasks, consult the applicable RSX-11M or RSX-11D Utilities Manual (see Section 0.3 in the Preface).

It often seems expedient to append a macro definition prefix file to each assembly to provide commonly-used macros. This practice, however, may produce the undesirable allocation of valuable dynamic

storage for unnecessary macros. This side effect can be avoided by specifying that the prefix file containing the macros is a user-supplied macro library file (see Table 8-1). This action imposes the stipulation that the names of all desired macros must be listed as arguments in the .MCALL directive (see Section 7.8).

Storage for macro text can be re-used effectively by redefining certain types of macros to null after they have been invoked. This practice releases their dynamic memory for the storage of later macro text and also eliminates the overhead and the need for dynamic memory which would otherwise be required during the subsequent invocation and expansion of such non-redefined macros. The practice of redefining macros to null applies mainly to those that only define symbolic assignments, as shown in the example below. The redefinition process may be accomplished as follows:

```asm
.MACRO DEFIN
SYM1 = VAL1                      ;DEFINE SYMBOLIC ASSIGNMENTS.
SYM2 = VAL2
.
.
.
OFF1 = SYMBOL                     ;DEFINE SYMBOLIC OFFSETS.
OFF2 = OFF1+SIZE1
OFF3 = OFF2+SIZE2
.
.
.
OFFN = OFFM+SIZEM
.
.
.
.MACRO DEFIN          ;MACRO NULL REDEFINITION.
.ENDM
```

.ENDM DEFIN

Macros exhibiting this redefinition property should be defined (or read via the .MCALL directive) and invoked before all other macro definition and/or .MCALL processing. So doing ensures more efficient use of dynamic memory.

The following system macros have the automatic null redefinition property after once being invoked:

DRERR\$ - Directive return status codes

IOERR\$ - I/O return status codes

FILIO\$ - File-related I/O function codes

SPCIO\$ - Special I/O function codes

CSI\$ - Command String Interpreter codes and offsets

GCMLD\$ - Get Command Line codes and offsets

BDOFF\$ - FCS buffer descriptor offsets

FCSBT\$ - FCS bit value codes

FDOFF\$ - FCS file descriptor block offsets

FSROF\$ - FCS file storage region (FSR) offsets

NBOFF\$ - FCS filename block offsets

### F.3 OPERATIONAL TECHNIQUES

When, despite adhering to the guidelines discussed above, performance still falls below expectations, several additional measures may be taken to improve performance.

The first measure involves shifting the burden of symbol definition from MACRO-11 to the linker. In most cases, the definition of system I/O and FCS symbols (and user-defined symbols of the same nature) is not necessary during the assembly process, since such symbols are defaulted to global references (see Section 3.9 and Section D.1, category 4 of error code A). The linker attempts to resolve all global references from user-specified default libraries and/or the system object library (SYSLIB). Furthermore, by applying the selective search option for object modules consisting only of global symbol definitions, the actual additional burden to the linker is minimal.

A second way of making more dynamic memory available is to produce only one output file (either object or listing), as opposed to two. The additional file descriptor block (FDB) and file storage region (FSR) required to support the second output file are allocated from available dynamic memory at the start of each assembly. Furthermore, the size of the file storage region allocated is the minimum required for the second (listing) output file. For disk files, this is 264(10) words, and for direct line printer output, it is 74(10) words.

The final way of increasing available dynamic memory is related only to the operating environment. Under RSX-11M, MACRO-11 allocates all storage between its highest address and the end of its partition as dynamic memory. Consequently, the amount of working storage can be increased by installing and running MACRO-11 in a larger partition.

In IAS and RSX-11D, the assembler's dynamic memory is fixed at link time. If a larger assembler is not available, you may build one by increasing the size of the task's stack. This is accomplished by altering the STACK= option in the command file to build MACRO-11.

## APPENDIX G WRITING POSITION INDEPENDENT CODE

### G.1 INTRODUCTION TO POSITION INDEPENDENT CODE

The output of a MACRO-11 assembly is a relocatable object module. The Task Builder binds one or more modules together to create an executable task image. Once built, a task can generally be loaded and executed only at the virtual address specified at link time. This is because the linker has had to modify some instructions to reflect the memory locations in which the program is to run. Such a body of code is considered position-dependent (i.e., dependent on the virtual addresses to which it was bound).

All PDP-11 processors offer addressing modes that make it possible to write instructions that are not dependent on the virtual addresses to which they are bound. A body of such code is termed position-independent and can be loaded and executed at any virtual address. Position-independent code can improve system efficiency, both in use of virtual address space and in conservation of physical memory.

In multiprogramming systems like IAS, RSX-11D and RSX-11M, it is important that many tasks be able to share a single physical copy of common code; for example a library routine. To make the optimum use of a task's virtual address space, shared code should be position-independent. Code that is not position-independent can also be shared, but it must appear in the same virtual locations in every task using it. This restricts the placement of such code by the Task Builder and can result in the loss of virtual addressing space.

The construction of position-independent code is closely linked to the proper usage of PDP-11 addressing modes. The remainder of this Appendix assumes you are familiar with the addressing modes described in Chapter 5.

All addressing modes involving only register references are position-independent. These modes are as follows:

R register mode

(R) deferred register mode

(R) + autoincrement mode

@ (R) + deferred autoincrement mode

-(R) autodecrement mode

@-(R) deferred autodecrement mode

When using these addressing modes, you are guaranteed position-independence, providing the contents of the registers have been supplied such that they are not dependent upon a particular virtual memory location.

**WRITING POSITION INDEPENDENT CODE**

The relative addressing modes are position-independent when a relocatable address is referenced from a relocatable instruction. These modes are as follows:

    A           relative mode
@a           relative deferred mode

Relative modes are not position-independent when an absolute address (that is a non-relocatable address) is referenced from a relocatable instruction. In this case, absolute addressing (i.e., @#A) may be employed to make the reference position-independent.

Index modes can be either position-independent or position-dependent, according to their use in the program. These modes are as follows:

X(R)         index mode
@X(R)         index deferred mode

If the base, X, is an absolute value (e.g., a control block offset), the reference is position-independent. For example:

N=4
        MOV     2(SP),R0          ;POSITION-INDEPENDENT
        MOV     N(SP),R0          ;POSITION-INDEPENDENT

If, however, X is a relocatable address, the reference is position-dependent. For example:

CLR        ADDR(R1)          ;POSITION-DEPENDENT

Immediate mode can be either position-independent or not, according to its usage. Immediate mode references are formatted as follows:

    #N immediate mode

When an absolute expression defines the value of N, the code is position-independent. When a relocatable expression defines N, the code is position-dependent. That is, immediate mode references are position-independent only when N is an absolute value.

Absolute mode addressing is position-independent only in those cases where an absolute virtual location is being referenced. Absolute mode addressing references are formatted as follows:

@#A absolute mode

An example of a position-independent absolute reference is a reference to the directive status word (\$DSW) from a relocatable instruction. For example:

MOV @#\$DSW,RO ;RETRIEVE DIRECTIVE STATUS

### G.2 EXAMPLES

The RSX-11 library routine, PWRUP, is a FORTRAN callable subroutine to establish or remove a user power failure AST entry point address. Imbedded within the routine is the actual AST entry point which saves all registers, effects a call to the user-specified entry point, restores all registers on return, and executes an AST exit directive. The following examples are excerpts from this routine. The first example has been modified to illustrate position-dependent references, (see Figure G-1). The second example, Figure G-2, is the position-independent version.

10\$:                  ;
        MOV     R2,F.PF(R4)      ;SET AST ENTRY POINT
        MOV     #BA,-(SP)          ;PUSH AST SERVICE ADDRESS

BA:        MOV     R0,-(SP)          ;PUSH (SAVE) R0
        MOV     R1,-(SP)          ;PUSH (SAVE) R1
        MOV     R2,-(SP)          ;PUSH (SAVE) R2

Figure G-1 Position-Dependent Code

PWRUP::
    CLR     -(SP)          ;ASSUME SUCCESS
    CALL     .X.PAA         ;PUSH ARGUMENT ADDRESSES ONTO STACK
    .WORD   1.,\$DSW           ;CLEAR DSW, AND SET R1=R2=SP.
    MOV     @#\$OTSV,R4      ;GET OTS IMPURE AREA POINTER
    MOV     (SP)+,R2       ;GET AST ENTRY POINT ADDRESS
    BNE     10\$               ;IF NONE SPECIFIED, SPECIFY NO POWER
    CLR     -(SP)          ;RECOVERY AST SERVICE
    BR     20\$

10\$:                     ;
        MOV     R2,F.PF(R4)      ;SET AST ENTRY POINT
        MOV     PC,-(SP)          ;PUSH CURRENT LOCATION
        ADD     #BA-.,(SP)      ;COMPUTE ACTUAL LOCATION OF AST

20\$: CALL .X.EXT ;ISSUE DIRECTIVE, EXIT.
.BYTE 109.,2.

BA:        MOV     R0,-(SP)          ;PUSH (SAVE) R0
        MOV     R1,-(SP)          ;PUSH (SAVE) R1
        MOV     R2,-(SP)          ;PUSH (SAVE) R2

    Figure G-2 Position-Independent Code

The position-dependent version of the subroutine contains a relative reference to an absolute symbol (\$OTSV) and a literal reference to a relocatable symbol (BA). Both references are bound by the Task Builder to fixed memory locations. Therefore, the routine will not execute properly as part of a resident library if its location in virtual memory is not the same as the location specified at link time.

In the position-independent version, the reference to \$OTSV has been changed to an absolute reference. In addition, the necessary code has been added to compute the virtual location of BA based upon the value of the program counter. In this case, the value is obtained by adding the value of the program counter to the fixed displacement between the current location and the specified symbol. Thus, execution of the modified routine is not affected by its location in the image's virtual address space.

The MACRO-11 Assembler provides a way of checking the position-independence of code. In an assembly listing, MACRO-11 inserts a ' character following the contents of any word which requires the linker to perform a relocation operation. In some cases this character indicates a position-dependent instruction; in other cases, it merely draws the user's attention to the use of a symbol which may or may not be position-independent. The cases which cause a ' character to be inserted in the assembly listing are as follows:

1. Absolute mode references are flagged with a ' character when the reference is relocatable. References are not flagged when they are position-independent (i.e., absolute). For example:

MOV  @#ADDR,RL      ;PIC ONLY IF ADDR IS ABSOLUTE.

2. Index and index deferred mode references are flagged with a 'character when the offset is relocatable. For example:

MOV ADDR(R1),R5 ;NON-PIC IF ADDR IS RELOCATABLE.
MOV @ADDR(R1),R5 ;NON-PIC IF ADDR IS RELOCATABLE.

3. Relative and relative deferred mode references are flagged with a ' character when the address specified is relocatable with respect to another program section. For example:

MOV  ADDR1,R1          ;NON-PIC WHEN ADDR1 IS BOUND
MOV  @ADDR1,R1         ;TO ANOTHER PROGRAM SECTION

4. Immediate mode references to relocatable addresses are always flagged with a ' character.

MOV #3,R0          ;ALWAYS POSITION-INDEPENDENT.
MOV #ADDR,R1       ;NON-PIC WHEN ADDR IS RELOCATABLE.

There is one case in which the MACRO-11 assembler does not flag a potential position-dependent reference. This occurs where a relative reference is made to an absolute virtual location from a relocatable instruction (i.e., MOV \$OTSV,R4 in Figure F-1).

Those references requiring more than simple relocation at link time are also indicated in the assembly listing. Simple global references are flagged with the letter G. Those which contain multiple global references or complex relocation, are flagged with the letter C (see Section 3.9 and Chapter 4). In such cases, it is difficult to positively state which are or are not position-independent. However, in general, it is safe to apply the guidelines discussed earlier in this Appendix to the resulting address value produced at link time.
