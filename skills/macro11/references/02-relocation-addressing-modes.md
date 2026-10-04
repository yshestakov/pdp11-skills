# MACRO-11 Reference: Ch.4 Relocation and Linking, Ch.5 Addressing Modes (incl. branch addressing, traps)

Source: DEC PDP-11 MACRO-11 Language Reference Manual, AA-5075A-TC (Aug 1977). OCR-converted; code examples may have lost alignment, and a few table rows/headings were dropped by OCR.

Contents:
- CHAPTER 4 RELOCATION AND LINKING
- CHAPTER 5
- 5.1 REGISTER MODE
- 5.2 REGISTER DEFERRED MODE
- 5.3 AUTOINCREMENT MODE
- 5.4 AUTOINCREMENT DEFERRED MODE
- 5.5 AUTODECREMENT MODE
- 5.6 AUTODECREMENT DEFERRED MODE
- 5.7 INDEX MODE
- 5.8 INDEX DEFERRED MODE
- 5.9 IMMEDIATE MODE
- 5.10 ABSOLUTE MODE
- 5.11 RELATIVE MODE
- 5.12 RELATIVE DEFERRED MODE
- 5.13 SUMMARY OF ADDRESSING FORMS
- 5.14 BRANCH INSTRUCTION ADDRESSING
- 5.15 USING TRAP INSTRUCTIONS

---

## CHAPTER 4 RELOCATION AND LINKING

The output of MACRO-11 is an object module that must be processed or linked before it can be loaded and executed. Essentially, linking fixes (i.e., makes absolute) the values of external or relocatable symbols in the object module, thus transforming the object module, or several such object modules, into an executable image.

To allow the value of an expression to be fixed at link time, MACRO-11 outputs certain directives in the object file, together with other required parameters. In the case of relocatable expressions in the object module, the base of the associated relocatable program section is added to the value of the relocatable expression provided by MACRO-11. In the case of external expression values, the value of the external term in the expression (since the external symbol must be defined in one of the other object modules being linked together) is determined and then added to the absolute portion of the external expression, as provided by MACRO-11.

All instructions that require modification at link time are flagged in the assembly listing, as illustrated in the example below. The apostrophe (') following the octal expansion of the instruction indicates that simple relocation is required; the letter G indicates that the value of an external symbol must be added to the absolute portion of an expression; and the letter C indicates that complex relocation analysis at link time is required in order to fix the value of the expression.

EXAMPLE:

005065 CLR EXTERN(R5) ;THE VALUE OF THE SYMBOL "EXTERN" IS
000000G ;ASSEMBLED AS ZERO AND IS
;RESOLVED AT LINK TIME.

005065 CLR EXTERN+6 (R5)

;THE VALUE OF THE SYMBOL "EXTERN"

;IS RESOLVED AT LINK TIME

;AND ADDED TO THE ABSOLUTE

;PORTION (+6) OF THE EXPRESSION.

005065 CLR RELOC(R5) ;ASSUMING THAT THE VALUE OF THE
000040' ;SYMBOL "RELOC" IS RELOCATABLE
;40, THE RELOCATION BIAS
;WILL BE ADDED TO THIS VALUE.

005065 CLR      -<EXTERN+RELOC>(R5) ;THIS EXPRESSION IS COMPLEX
000000C                      ;RELOCATABLE BECAUSE IT REQUIRES
                            ;THE NEGATION OF AN EXPRESSION
                            ;THAT CONTAINS A GLOBAL "EXTERN"
                            ;REFERENCE AND A RELOCATABLE TERM.

For a complete description of object records output by MACRO-11, refer to the applicable system manual (see Section 0.3 in the Preface).

## CHAPTER 5

**ADDRESSING MODES**

The program counter (PC) always contains the address of the next word to be fetched, i.e., the address of the next instruction to be executed, or the second or third word of the current instruction.

In order to understand how the address modes operate and how they assemble, the action of the program counter must be understood. The key rule to remember is:

"whenever the processor implicitly uses the program counter (PC) to fetch a word from memory, the program counter is automatically incremented by 2 after the fetch operation is completed."

In the case of 2- or 3-word instructions, the processor uses the PC to fetch the following words as well.

The following symbols are used in describing addressing modes throughout this chapter:

1. E is any expression, as defined in Chapter 3.

2. R is a register expression, i.e., any expression containing a term preceded by a percent sign (%) or a symbol previously equated to such a term, as shown in the examples below:

```matlab
R0=%0                      ;GENERAL REGISTER 0.
R1=R0+1                   ;GENERAL REGISTER 1.
R2=1+%1                   ;GENERAL REGISTER 2.
```

The symbol R may also represent any of the normal default register definitions (see Section 3.4).

3. ER is a register expression or an absolute expression in the range 0 to 7, inclusive.

4. A is a general addressing specification which produces a 6-bit mode address field, as described in the PDP-11 Processor Handbooks. The addressing specification, A, is described in terms of E, R, and ER, as defined above. Each addressing specification within this section is illustrated using either the single operand instruction CLR or the double operand instruction MOV.

### 5.1 REGISTER MODE

The register itself (R) contains the operand to be manipulated by the instruction.

Format for A: R

Example:

CLR       R3                  ;CLEARS REGISTER 3.

### 5.2 REGISTER DEFERRED MODE

The register (R) contains the address of the operand to be manipulated by the instruction.

Format for A: @R or (ER)

Examples:

CLR        @R1                  ;ALL THESE INSTRUCTIONS CLEAR
CLR        (R1)                 ;THE WORD AT THE ADDRESS
CLR        (1)                  ;CONTAINED IN REGISTER 1.

### 5.3 AUTOINCREMENT MODE

The contents of the register (ER) are incremented immediately after being used as the address of the operand (see Note below).

Format for A: (ER)+

Examples:

CLR          (R0) +
CLR          (R4) +
CLR          (R2) +
;EACH INSTRUCTION CLEARS
;THE WORD AT THE ADDRESS
;CONTAINED IN THE SPECIFIED
;REGISTER AND INCREMENTS
;THAT REGISTER'S CONTENTS
;BY TWO.

**NOTE:**

Certain special instruction/address mode combinations, which are rarely or never used, do not operate exactly the same on all PDP-11 processors, as described below.

In the autoincrement mode, both the JMP and JSR instructions autoincrement the register before its use on the PDP-11/40, but not on the PDP-11/45 or 11/10.

In double operand instructions having the addressing form Rn,(Rn)+ or Rn,-(Rn), where the source and destination registers are the same, the source operand is evaluated as the autoincremented or autodecremented value, but the destination register, at the time it is used, still contains the originally-intended effective address. In the following example, as executed on the PDP-11/40, Register 0 originally contains 100(8):

MOV R0, (R0) + ;THE QUANTITY 102 IS MOVED
;TO LOCATION 100.

MOV R0, -(R0) ;THE QUANTITY 76 IS MOVED
;TO LOCATION 100.

The use of these forms should be avoided, since they are not compatible with the entire family of PDP-11 processors.

An error code (Z) is printed in the assembly listing with each instruction which is not compatible among all members of the PDP-11 family.

### 5.4 AUTOINCREMENT DEFERRED MODE

The register (ER) contains a pointer to the address of the operand. The contents of the register are incremented after being used as a pointer.

```txt
Format for A: @(ER)+
```

Example:

```txt
CLR        @(R3) +
;THE CONTENTS OF REGISTER 3 POINT
;TO THE ADDRESS OF A WORD TO BE
;CLEARED BEFORE THE CONTENTS OF THE
;REGISTER ARE INCREMENTED BY TWO.
```

### 5.5 AUTODECREMENT MODE

The contents of the register (ER) are decremented before being used as the address of the operand (see Note above in Section 5.3).

```txt
Format for A: -(ER)
```

Examples:

```txt
CLR          - (RU)
CLR          - (R3)
CLR          - (R2)
```

```txt
;DECREMENT THE CONTENTS OF THE SPECI-
;FIED REGISTER (0, 3, OR 2) BY TWO
;BEFORE USING ITS CONTENTS
;AS THE ADDRESS OF THE WORD TO BE
;CLEARED.
```

### 5.6 AUTODECREMENT DEFERRED MODE

The contents of the register (ER) are decremented before being used as a pointer to the address of the operand.

```txt
Format for A: @-(ER)
```

Example:

```txt
CLR @-(R2) ;DECREMENT THE CONTENTS OF
;REGISTER 2 BY TWO BEFORE
;USING ITS CONTENTS AS A POINTER
;TO THE ADDRESS OF THE WORD TO BE
;CLEARED.
```

### 5.7 INDEX MODE

The value of an expression (E) is stored as the second or third word of the instruction. The effective address of the operand is calculated as the value of E, plus the contents of register ER. The value E is the offset of the instruction, and the contents of register ER form the base.

```txt
Format for A: E(ER)
```

Examples:

CLR       X+2(R1)          ;THE EFFECTIVE ADDRESS OF THE WORD
                        ;TO BE CLEARED IS X+2, PLUS THE
                        ;CONTENTS OF REGISTER 1.
MOV       R0,-2(R3)          ;THE EFFECTIVE ADDRESS OF THE
                        ;DESTINATION LOCATION IS -2, PLUS
                        ;THE CONTENTS OF REGISTER 3.

### 5.8 INDEX DEFERRED MODE

An expression (E), plus the contents of a register (ER), yields a pointer to the address of the operand. As in index mode above, the value E is the offset of the instruction, and the contents of register ER form the base.

Format for A: @E(ER)

Example:

CLR @114(R4) ;IF REGISTER 4 CONTAINS 100, THIS
;VALUE, PLUS THE OFFSET 114, YIELDS
;THE POINTER 214. IF LOCATION 214
;CONTAINS THE ADDRESS 2000, LOCATION
;2000 WOULD BE CLEARED.

### 5.9 IMMEDIATE MODE

Immediate mode allows the operand itself (E) to be stored as the second or third word of the instruction. This mode is assembled as an autoincrement of the PC.

```txt
Format for A: #E
```

Examples:

MOV          #100,R0                  ;MOVE THE VALUE 100 INTO REGISTER 0.
MOV          #X,R0                  ;MOVE THE VALUE OF SYMBOL X INTO
                                ;REGISTER 0.

The number sign (#) in the MACRO-11 character set has special significance as an addressing mode indicator. When this character appears in the operand field, as shown above, it specifies the immediate addressing mode, indicating to MACRO-11 that the operand itself immediately follows the instruction word.

The operation of this mode can be shown through the first example, MOV #100,R0, which assembles as two words:

Location 20: 0 1 2 7 0 0

Location 22: 0 0 0 1 0 0

Location 24: Next instruction

Note that the source operand (the value 100) is assembled immediately following the instruction word, i.e., as the second word in the instruction. Upon execution of the instruction, the processor fetches the first word (MOV) and increments the PC by 2 so that it points to location 22 (which contains the source operand).

After the next fetch and increment cycle, the source operand (100) is moved into register 0, leaving the PC pointing to location 24 (the next instruction).

### 5.10 ABSOLUTE MODE

Absolute mode is the equivalent of immediate mode deferred. The address expression @#E specifies an absolute address which is stored as the second or third word of the instruction. In other words, the value immediately following the instruction word is taken as the absolute address of the operand. Absolute mode is assembled as an autoincrement deferred of the PC.

Format for A: @#E

Examples:

MOV        @#100,R0          ;MOVE THE CONTENTS OF ABSOLUTE
                            ;LOCATION 100 INTO REGISTER R0.
CLR       @#X           ;CLEAR THE CONTENTS OF THE LOCATION
                            ;WHOSE ADDRESS IS SPECIFIED BY
                            ;THE SYMBOL X.

The operation of this mode can be shown through the first example, MOV @#100,R0, which assembles as two words:

Location 20: 0 1 3 7 0 0

Location 22: 0 0 0 1 0 0

Location 24: Next instruction

Note that the absolute address 100 is assembled immediately following the instruction word, i.e., as the second word in the instruction. Upon execution of the instruction, the processor fetches the first word (MOV) and increments the PC by 2 so that it points to location 22 (which contains the absolute address of the source operand). After the next fetch and increment cycle, the contents of absolute address 100 (the source operand) are moved into register 0, leaving the PC pointing to location 24 (the next instruction).

### 5.11 RELATIVE MODE

Relative mode is the normal mode for memory references within your program. It is assembled as index mode, using the PC as the index register.

Format for A: E

Examples:

CLR      100                  ;CLEAR ABSOLUTE LOCATION 100
MOV     R0,Y              ;MOVE THE CONTENTS OF REGISTER 0
                        ;TO LOCATION Y

In relative mode, the offset for the address calculation is assembled as the second or third word of the instruction. This value is added to the contents of the PC (the base register) to yield the address of the source operand.

The operation of relative mode can be shown with the statement MOV 100,R3, which assembles as two words:

Location 20: 0 1 6 7 0 3

Location 22: 0 0 0 0 5 4

Location 24: Next instruction

Note that the constant 54 is assembled immediately following the instruction word, i.e., as the second word in the instruction. Upon execution of the instruction, the processor fetches the first word (MOV) and increments the PC by 2 so that it points to location 22 (containing the value 54). After the next fetch and increment cycle, the processor calculates the effective address of the source operand by taking the contents of location 22 (the offset) and adding it to the current value of the PC, which now points to location 24 (the next instruction). Thus, the source operand address is the result of the calculation OFFSET+PC = 54+24 = 100(8), causing the contents of location 100 to be moved into register 3.

Since MACRO-11 considers the contents of the current location counter (.) as the address of the first word of the instruction, an equivalent index mode statement is shown below:

MOV 100-.-4(PC),R3

This instruction has a relative addressing mode because the operand address is calculated relative to the current value of the location counter. The offset is the distance (in bytes) between the operand and the current value of the location counter.

### 5.12 RELATIVE DEFERRED MODE

The relative deferred mode is similar in operation to the relative mode above, except that the expression E is used as a pointer to the address of the operand. In other words, the operand following the instruction word is added to the contents of the PC to yield a pointer to the address of the operand.

Format for A: @E

Example:

MOV @X,R0

;RELATIVE TO THE CURRENT VALUE OF
;THE PC, MOVE THE CONTENTS OF THE
;LOCATION WHOSE ADDRESS IS POINTED
;TO BY LOCATION X INTO REGISTER 0.

### 5.13 SUMMARY OF ADDRESSING FORMS

Each PDP-11 instruction takes at least one word. Operands of the form listed below do not increase the length of an instruction.

Form Meaning

R Register mode

@R or (ER) Register deferred mode (see Note below)

(ER) + Autoincrement mode

@(ER) + Autoincrement deferred mode

-(ER) Autodesk mode

@-(ER) Autodecrement deferred mode

Operands of the following forms add one word to the instruction length for each occurrence of an operand of that form:

Form Meaning

E (ER) Index mode

@E (ER) Index deferred mode

#E                  Immediate mode

@#E Absolute mode (see Note below)

E Relative mode

@E                  Relative deferred mode

The syntax of the addressing modes is summarized in Appendix B. Additional discussion of addressing modes is provided in the applicable PDP-11 Processor Handbook.

**NOTE:**

An alternate form for @R is (ER). However, the form @(ER) is only logically, but not physically equivalent to the expression @0(ER). The addressing form @#E differs from form E in that the second or third word of the instruction contains the absolute address of the operand, rather than the relative distance between the operand and the PC. Thus, the instruction CLR @#100 clears absolute location 100, even if the instruction is moved from the point at which it was assembled. See the description of the .ENABL AMA function in Section 6.2, which causes all relative mode addresses to be assembled as absolute mode addresses.

### 5.14 BRANCH INSTRUCTION ADDRESSING

The branch instructions are l-word instructions. The high-order byte contains the operator, and the low-order byte contains an 8-bit signed offset (seven bits, plus sign), which specifies the branch address relative to the current value of the PC. The hardware calculates the branch address as follows:

1. Extends the sign of the offset through bits 8-15.

2. Multiplies the result by 2, creating a byte offset rather than a word offset.

3. Adds the result to the current value of the PC to form the effective branch address.

MACRO-11 performs the reverse operation to form the word offset from the specified address. Remember that when the offset is added to the current value of the PC, the PC is pointing to the word following the branch instruction; hence, the factor -2 in the following calculation:

Word offset = (E-PC)/2 truncated to eight bits.

Since the value of the PC = .+2, we have:

Word offset = (E-.-2)/2 truncated to eight bits.

In using branch instructions, you must exercise care to avoid the following error conditions:

1. Branching from one program section to another;

2. Branching to a location that is defined as an external (global) symbol; or

3. Specifying a branch address that is out of range, i.e., the branch offset is a value that does not lie within the range -128(10) to +127(10).

The above conditions cause an error code (A) to be generated in the assembly listing for the statement in error.

### 5.15 USING TRAP INSTRUCTIONS

The EMT and TRAP instructions do not use the low-order byte of the instruction word, allowing information to be transferred to the trap handlers in the low-order byte. If the EMT or TRAP instruction is followed by an expression, the value of the expression is stored in the low-order byte of the word. However, if the expression is greater than 377(8), it is truncated to eight bits and an error code (T) is generated in the assembly listing.
