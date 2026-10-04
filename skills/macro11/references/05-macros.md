# MACRO-11 Reference: Ch.7 Macros: .MACRO/.ENDM, arguments, .NARG/.NCHR/.NTYPE, .ERROR/.PRINT, .IRP/.IRPC, .REPT, .MCALL

Source: DEC PDP-11 MACRO-11 Language Reference Manual, AA-5075A-TC (Aug 1977). OCR-converted; code examples may have lost alignment, and a few table rows/headings were dropped by OCR.

Contents:
- CHAPTER 7
- 7.1 DEFINING MACROS
- 7.1.1 .MACRO Directive
- 7.1.2 .ENDM Directive
- NOTES
- 7.1.3 .MEXIT Directive
- 7.1.4 MACRO Definition Formatting
- 7.2 CALLING MACROS
- 7.3 ARGUMENTS IN MACRO DEFINITIONS AND MACRO CALLS
- 7.3.1 Macro Nesting
- 7.3.2 Special Characters in Macro Arguments
- 7.3.3 Passing Numeric Arguments as Symbols
- 7.3.4 Number of Arguments in Macro Calls
- 7.3.5 Creating Local Symbols Automatically
- 7.3.6 Keyword Arguments
- 7.3.7 Concatenation of Macro Arguments
- 7.4 MACRO ATTRIBUTE DIRECTIVES: .NARG, .NCHR, AND .NTYPE
- 7.4.1 .NARG Directive
- 7.4.2 .NCHR Directive
- 7.4.3 .NTYPE Directive
- 7.5 .ERROR AND .PRINT DIRECTIVES
- 7.6 INDEFINITE REPEAT BLOCK DIRECTIVES: .IRP AND .IRPC
- 7.6.1 .IRP Directive
- 7.6.2 .IRPC Directive
- 7.7 REPEAT BLOCK DIRECTIVE: .REPT, .ENDR
- 7.8 MACRO LIBRARY DIRECTIVE: .MCALL

---

## CHAPTER 7

**MACRO DIRECTIVES**

### 7.1 DEFINING MACROS

In assembly-language programming, it is often convenient and desirable to generate a recurring coding sequence by invoking a single statement within the program. In order to do this, the desired coding sequence is first established with dummy arguments as a macro definition. Once a macro has been defined, a single statement calling the macro by name with a list of real arguments (replacing the corresponding dummy arguments in the macro definition) generates the desired coding sequence. This sequence is called the macro expansion.

#### 7.1.1 .MACRO Directive

The first statement of a macro definition must be a .MACRO directive.
This directive takes the form:

label: .MACRO name, dummy argument list

where: label represents an optional statement label.

name represents the programmer-assigned symbolic name of the macro. This name may be any legal symbol and may be used as a label elsewhere in the program.

' represents any legal separator (comma, space, and/or tab).

dummy represents a number of legal symbols (see 3.2.2) that may appear anywhere in the body of the macro definition, even as a label. These dummy symbols can be used elsewhere in the program with no conflict of definition. Multiple dummy arguments specified in this directive may be separated by any legal separator. The detection of a duplicate or an illegal symbol in a dummy argument list terminates the scan and causes an error code to be generated.

A comment may follow the dummy argument list in a .MACRO directive, as shown below:

.MACRO ABS A,B ;DEFINES MACRO ABS WITH TWO ARGUMENTS.

**NOTE:**

Although it is legal for a label to appear on a .MACRO directive, this practice is discouraged, especially in the case of nested macro definitions, because invalid labels or labels constructed with the concatenation character will cause the macro directive to be ignored. This may result in improper termination of the macro definition. This NOTE also applied to .IRP, .IRPC, and .REPT.

#### 7.1.2 .ENDM Directive

The final statement of every macro definition must be an .ENDM directive of the form:

.ENDM name

where: name represents an optional argument specifying the symbolic name of the macro being terminated by the directive, as shown in the following example:

. ENDM

;TERMINATES THE CURRENT
;MACRO DEFINITION.

.ENDM ABS

;TERMINATES THE CURRENT
;MACRO DEFINITION NAMED ABS.

If specified, the symbolic name in the .ENDM statement must match the name specified in the corresponding .MACRO directive. Otherwise, the statement is flagged with an error code (A) in the assembly listing (see Appendix D). In either case, the current macro definition is terminated. Specifying the macro name in the .ENDM statement thus permits MACRO-11 to detect missing .ENDM statements or improperly-nested macro definitions.

The .ENDM directive may be followed by a comment field, but must not contain a label, as shown below:

.MACRO TYPMSG MESSAGE ;TYPE A MESSAGE.
JSR R5,TYPMSG
.WORD MESSAGE
.ENDM ;END OF TYPMSG MACRO.

An .ENDM statement encountered by MACRO-11 outside a macro definition is flagged with an error code (0) in the assembly listing (see Appendix D).

### NOTES

1. Labels on .ENDM directives are ignored.

2. Illegal labels will cause the directive to be bypassed.

#### 7.1.3 .MEXIT Directive

The .MEXIT directive may be used to terminate a macro expansion before the end of the macro is encountered. This directive is also legal within repeat blocks (see Sections 7.6 and 7.7). It is most useful in the context of nested macros. The .MEXIT directive terminates the current macro as though an .ENDM directive had been encountered. Using the .MEXIT directive bypasses the complexities of nested conditional directives and alternate assembly paths, as shown in the following example:

```asm
.MACRO ALTR N,A,B
.
.
.
.IF EQ N ;START CONDITIONAL ASSEMBLY BLOCK.
.
.
.
.MEXIT ;TERMINATE MACRO EXPANSION.
.ENDC ;END CONDITIONAL ASSEMBLY BLOCK.
.
.
.
.ENDM ;NORMAL END OF MACRO.
```

Considering the above macro, in an assembly where the real argument for the dummy symbol N is equal to zero (see Table 6-5), the conditional block would be assembled, and the macro expansion would be terminated by the .MEXIT directive. When macros are nested, a .MEXIT directive causes an exit to the next higher level of macro expansion.

A .MEXIT directive encountered outside a macro definition is flagged with an error code (0) in the assembly listing.

#### 7.1.4 MACRO Definition Formatting

A form-feed character used within a macro definition causes a page eject during the assembly of the macro definition. A page eject, however, is not performed when the macro is expanded.

Conversely, when the .PAGE directive is specified within a macro definition, it is ignored during the assembly of the macro definition, but a page eject is performed when that macro is expanded.

### 7.2 CALLING MACROS

A macro definition must be established by means of the .MACRO directive (see Section 7.1.1) before the macro can be expanded within the source program. Macro calls are of the general form:

label: name real arguments

where: label represents an optional statement label.

name represents the name of the macro, as specified in the .MACRO directive (see Section 7.1.1).

real arguments represent symbolic arguments which replace the dummy arguments specified in the .MACRO directive. When multiple arguments are specified, they are separated by any legal separator. Arguments to the macro call are treated as character strings whose usage is determined by the macro definition. Note that MACRO-ll accepts the ASCII value of lower-case alphabetic characters when .ENABL LC has been specified.

When a macro name is the same as a user label, the appearance of the symbol in the operator field designates the symbol as a macro call; the appearance of the symbol in the operand field designates it as a label, as shown below:

ABS:     MOV     (R0),R1          ;ABS IS DEFINED AS A LABEL.
        .
        .
        .
BR       ABS           ;ABS IS CONSIDERED TO BE A LABEL.
        .
        .
ABS       #4,ENT,LAR      ;ABS IS A MACRO CALL.

### 7.3 ARGUMENTS IN MACRO DEFINITIONS AND MACRO CALLS

Arguments within a macro definition or macro call are separated from other arguments by any of the legal separating characters described in Section 3.1.1.

Macro definition arguments (dummy) and macro call arguments (real) normally maintain a strict positional relationship. That is, the first real argument in a macro call corresponds with the first dummy argument in a macro definition. Only the use of keyword arguments in a macro call can override this correspondence (see Section 7.3.6).

For example, the following macro definition and its associated macro expansion contain multiple arguments:

.MACRO REN A,B,C
.
.
REN ALPHA,BETA,<C1,C2>

Arguments which themselves contain separating characters must be enclosed in paired angle brackets, as shown above. For example, the macro call:

REN <MOV X,Y>,#44,WEV

causes the entire expression

MOV X,Y

to replace all occurrences of the symbol A in the macro definition. Real arguments within a macro call are considered to be character strings and are treated as a single entity during the macro expansion.

The up-arrow ( $^{\wedge}$ ) construction is provided to allow angle brackets to be passed as part of the argument. This construction, for example, could have been used in the above macro call, as follows:

    REN      ^//<MOV X,Y>/,#44,WEV

causing the entire character string <MOV X,Y> to be passed as an argument.

The following macro call:

```csv
REN #44,WEV^/MOV X,Y/
```

however, contains only two arguments (#44 and WEV^/MOV X,Y/), because the up-arrow is a unary operator (see Section 3.1.3) and it is not preceded by an argument separator.

As shown in the examples above, spaces can be used within bracketed argument constructions to increase the legibility of such expressions.

#### 7.3.1 Macro Nesting

The nesting of macros, where the expansion of one macro includes a call to another, causes one set of angle brackets in the macro definition to be removed from an argument with each nested call. The depth of nesting allowed is dependent upon the amount of dynamic memory used by the source program being assembled.

To pass an argument containing legal argument delimiters to nested macros, the argument in the macro definition should be enclosed within one set of angle brackets for each level of nesting, as shown in the coding sequence below. It should be noted that this extra set of angle brackets for each level of nesting is required in the macro definition, not in the macro call.

```asm
.MACRO LEVEL1 DUM1,DUM2
LEVEL2 <DUM1>
LEVEL2 <DUM2>
.ENDM
```

.MACRO LEVEL2 DUM3
DUM3
ADD #10,R0
MOV R0,(R1)+
.ENDM

A call to the LEVEL1 macro, as shown below, for example:

```txt
LEVEL1 <MOV X,R0>,<MOV R2,R0>
```

causes the following macro expansion to occur:

MOV         X,R0
ADD       #10,R0
MOV       R0,(R1)+
MOV       R2,R0
ADD       #10,R0
MOV       R0,(R1)+

When macro definitions are nested, i.e., when a macro definition is contained entirely within the definition of another macro, the inner definition is not a callable macro until the outer macro has been called and expanded. For example, in the following coding:

```txt
.MACRO LV1 A,B
.
.
.
.MACRO LV2 C
.
.
.ENDM
.ENDM
```

the LV2 macro cannot be called and expanded until the LV1 macro has been so invoked. Likewise, any macro defined within the LV2 macro definition cannot be called and expanded until LV2 has also been invoked.

#### 7.3.2 Special Characters in Macro Arguments

An argument may include special characters without enclosing them in a bracketed construction if that argument does not contain spaces, tabs, semicolons, or commas. For example, the macro definition:

.MACRO PUSH ARG
MOV ARG, -(SP)
.ENDM
.
.
.
PUSH X+3 (%2)

causes the following code to be generated:

```csv
MOV X+3(82),-(SP)
```

#### 7.3.3 Passing Numeric Arguments as Symbols

When macro arguments are passed, an absolute symbol value can be passed which is treated by the macro as a numeric string. An argument preceded by the unary operator backslash (\) is treated as a numeric value in the current program radix. The ASCII characters representing this value are inserted in the macro expansion, and their function is defined in the context of the resulting code, as shown in the following example:

.B=B+1
.A'B:
.C=0
.MACRO INC A,B
CON A,\B
.ENDM
.MACRO CON A,B
.WORD 4
.ENDM
.
.
.
INC X,C

;B IS TREATED AS A NUMBER IN CURRENT
;PROGRAM RADIX.

The above macro call (INC) would thus expand to:

X0: .WORD 4

Note in this expanded code that the label X0: is the result of the concatenation of two real arguments. The single quote (') character in the label A'B: causes the real arguments X and 0 to be concatenated as they are passed during the expansion of the macro. This type of argument construction is described in further detail in Section 7.3.6.

A subsequent call to the same macro would generate the following code:

X1: .WORD 4

and so on, for later calls. The two macro definitions are necessary because the symbol associated with dummy argument B (i.e., C) cannot be updated in the CON macro definition, because its numeric value has already been substituted for its symbolic name, i.e., the character 0 has replaced C in the argument string. In the CON macro definition, the number passed is treated as a string argument. (Where the value of the real argument is 0, only a single 0 character is passed to the macro expansion.)

Passing numeric values in this manner is useful in identifying source listings. For example, versions of programs created through conditional assemblies of a single source program can be identified through such coding as that shown below. Assume, for example, that the symbol ID in the macro call (IDT) has been equated elsewhere in the source program to the value 6.

.MACRO IDT SYM          ;ASSUME THAT THE SYMBOL ID TAKES
.IDENT /V05A'SYM/       ;ON A UNIQUE 2-DIGIT VALUE.
.ENDM                    ;WHERE V05A IS THE UPDATE
.                                       ;VERSION OF THE PROGRAM.
.
.
IDT     \ID

The above macro call would then expand to:

.IDENT /V05A6/

where 6 is the numeric value of the symbol ID.

#### 7.3.4 Number of Arguments in Macro Calls

If more arguments appear in the macro call than in the macro definition, an error code (Q) is generated in the assembly listing. If fewer arguments appear in the macro call than in the macro definition, missing arguments are assumed to be null values. The conditional directives .IF B and .IF NB (see Table 6-5) can be used within the macro to detect missing arguments. The number of arguments can also be specified using the .NARG directive (Section 7.4.1). Note that a macro can be defined with no arguments.

#### 7.3.5 Creating Local Symbols Automatically

A label is often required in an expanded macro. In the conventional macro facilities thus far described, such a label must be explicitly

specified as an argument with each macro call. Be careful in issuing subsequent calls to the same macro, to avoid specifying a duplicate label as a real argument. This concern can be eliminated through a feature of MACRO-11 which creates a unique symbol where a label is required in an expanded macro.

As noted in Section 3.5, MACRO-11 can automatically create local symbols of the form n\$, where n is a decimal integer within the range 64 through 127, inclusive. Such local symbols are created by MACRO-11 in numerical order, as shown below:

This automatic facility is invoked on each call of a macro whose definition contains a dummy argument preceded by the question mark (?) character, as shown in the macro definition below:

.MACRO ALPHA, A, ?B ;CONTAINS DUMMY ARGUMENT B PRECEDED BY
;QUESTION MARK.
TST A
BEQ B
ADD #5, A
.ENDM

A local symbol is generated automatically by MACRO-11 only when a real argument of the macro call is either null or missing, as shown in Example 1 below, which reflects the expansion of the ALPHA macro defined above.

If the real argument is specified in the macro call, however, MACRO-11 inhibits the generation of a local symbol and normal argument replacement occurs, as shown in Example 2 below.

EXAMPLE 1: Generate a Local Symbol for the Missing Argument:

ALPHA    R1                     ;SECOND ARGUMENT IS MISSING.
TST       R1
BEQ       64\$                   ;LOCAL SYMBOL IS GENERATED.
ADD       #5,R1

64\$:

EXAMPLE 2: Do Not Generate a Local Symbol:

ALPHA    R2,XYZ          ;SECOND ARGUMENT XYZ IS SPECIFIED.
TST       R2
BEQ       XYZ           ;NORMAL ARGUMENT REPLACEMENT OCCURS.
ADD      #5,R2

XYZ:

Automatically-generated local symbols are restricted to the first 16(10) arguments of a macro definition.

Note that automatically-created local symbols resulting from the expansion of a macro, as described above, do not in any way influence local symbol block boundaries. In other words, such automatically-created local symbols do not establish a local symbol block in their own right.

However, when a macro has several arguments earmarked for automatic local symbol generation, substituting a specific label for one such argument introduces a risk that assembly errors will result. This is because MACRO-11 constructs its argument substitution list at the point of macro invocation. Therefore, the appearance of any label, the .ENABL LSB directive, or the .PSECT directive, in the macro expansion will create a new local symbol block. This could leave local symbol references in the previous block and the symbol definitions in the new one, resulting in error codes in the assembly listing (see Appendix D). Furthermore, a subsequent macro expansion that generates local symbols in the new block may duplicate one of the symbols in question, resulting in an additional error code (P) in the assembly listing.

#### 7.3.6 Keyword Arguments

Macros may be defined with and/or invoked with keyword arguments. A keyword argument has the following form:

name=string

where

name represents the dummy argument,

string represents the real symbolic argument.

The keyword argument may not contain embedded argument separators unless properly delimited as described in section 7.3.

When a keyword argument appears in the dummy argument list of a macro definition, the specified string becomes the default real argument at macro call.

When a keyword argument appears in the real argument list of a macro call, the specified string becomes the real argument for the dummy argument that exactly matches the specified name, whether or not the dummy argument was defined with a keyword. If a match fails, the entire argument specification is treated as the next positional real argument. A keyword argument may be specified anywhere in the dummy argument list of a macro definition and is part of the positional ordering of argument. On the other hand, a keyword argument may be specified anywhere in the real argument list of a macro call but does not affect the positional correspondence of the remaining arguments.

    .LIST ME

; DEFINE A MACRO HAVING KEYWORDS IN DUMMY ARGUMENT LIST
;

.MACRO TEST CONTROL=1,BLOCK,ADDRESS=TEMP

.WORD CONTROL

.WORD ADDRES

; NOW INVOKE SEVERAL TIMES
;

000000
000000 000000G
.WORD A
000002 000000G
.WORD B
000004 000000G
.WORD C
000006
000006 000040
TEST ADDRES=20,BLOCK=30,CONTRL=40
.WORD 40
000010 000030
.WORD 30
000012 000020
.WORD 20
000014
000014 000001
TEST BLOCK=5
.WORD 1
000016 000005
.WORD 5
.WORD TEMP
000020 000000G
TEST CONTROL=5,ADDRES=VARIAB
.WORD 5
.WORD
.WORD VARIAB
000022
000022 000005
TEST
.WORD 1
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD
.WORD

#### 7.3.7 Concatenation of Macro Arguments

The apostrophe or single quote character (') operates as a legal delimiting character in macro definitions. A single quote that precedes and/or follows a dummy argument in a macro definition is removed, and the substitution of the real argument occurs at that point. For example, in the following statements:

        .MACRO  DEF A,B,C
    .ASCIZ   /C/
    .BYTE    '''A,''B
    .ENDM

when the macro DEF is called through the statement:

DEF       X,Y,<MACRO-11>

it is expanded, as follows:

XY: .ASCIZ /MACRO-11/
.BYTE 'X,'Y

In expanding the first line, the scan for the first argument terminates upon finding the first ' character. Since A is a dummy argument, the ' is removed. The scan then resumes with B; B is also noted as another dummy argument. The two real arguments X and Y are then concatenated to form the label XY:. The third dummy argument is noted in the operand field of the .ASCIZ directive, causing the real argument MACRO-11 to be substituted in this field.

When evaluating the arguments to the .BYTE directive during expansion of the second line, the scan begins with the first ' character. Since it is neither preceded nor followed by a dummy argument, this ' character remains in the macro expansion. The scan then encounters the second ' character, which is followed by a dummy argument and is therefore discarded. The scan of argument A is terminated upon encountering the comma (,). The third ' character is neither preceded nor followed by a dummy argument and again remains in the macro expansion. The fourth (and last) ' character is followed by another dummy argument and is likewise discarded. (Note that four ' characters were necessary in the macro definition to generate two ' characters in the macro expansion.)

### 7.4 MACRO ATTRIBUTE DIRECTIVES: .NARG, .NCHR, AND .NTYPE

Three directives are available in MACRO-11 which allow the user to determine certain attributes of macro arguments. The use of these directives permits selective modifications of a macro expansion, depending on the nature of the arguments being passed. These directives are described separately below.

#### 7.4.1 .NARG Directive

The .NARG directive is used to determine the number of arguments in the macro call currently being expanded. Hence, the .NARG directive can appear only within a macro definition; if it does not, an error code (0) is generated in the assembly listing. This directive takes the form:

label: .NARG symbol

where: label represents an optional statement label.

represents any legal symbol. This symbol is equated to the number of arguments in the macro call currently being expanded. If a symbol is not specified, the .NARG directive is flagged with an error code (A) in the assembly listing.

An example of the .NARG directive follows:

15 000000
000000
NOPP
.NARG SYM
.IF EQ, SYM
.MEXIT
.IFF
.REPT
NOP
.ENDM
.ENDC

#### 7.4.2 .NCHR Directive

The .NCHR directive, which can appear anywhere in a MACRO-11 program, is used to determine the number of characters in a specified character string. This directive, which is useful in calculating the length of macro arguments, takes the following form:

label: .NCHR symbol,<string>

where: label represents an optional statement label.

symbol represents any legal symbol. This symbol is equated to the number of characters in the specified character string. If a symbol is not specified, the .NCHR directive is flagged with an error code (A) in the assembly listing (see Appendix D).

, represents any legal separator (comma, space, and/or tab).

<string> represents a string of printable characters. The character string need be enclosed within angle brackets (<>) or up-arrows (^) only if the specified character string contains a legal separator (comma, space, and/or tab). If the delimiting characters do not match or if the ending delimiter cannot be detected because of a syntactical error in the character string (thus prematurely terminating its evaluation), the .NCHR directive is flagged with an error code (A) in the assembly listing.

An example of the .NCHR directive follows:

[figure from original manual omitted]

#### 7.4.3 .NTYPE Directive

The .NTYPE directive is used to determine the addressing mode of a specified macro argument. Hence, the .NTYPE directive can appear only within a macro definition; if it appears elsewhere, it is flagged with an error code (0) in the assembly listing. This directive takes the form:

label: .NTYPE symbol,aexp

where: label represents an optional statement label.

symbol represents any legal symbol. This symbol is equated to the 6-bit addressing mode of the following argument. If a symbol is not specified, the .NTYPE directive is flagged with an error code (A) in the assembly listing.

, represents any legal separator (comma, space, and/or tab).

aexp represents any legal address expression, as used with an opcode. If no argument is specified, the result will be zero.

An example of the use of an .NTYPE directive in a macro definition is shown below:

| 1 |  |  |  | .TITLE | NTYPE |  |
| --- | --- | --- | --- | --- | --- | --- |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  | .MACRO | SAVE,ARG |  |
| 4 |  |  |  | .NTYPE | SYM,ARG |  |
| 5 |  |  |  | .IF | FQ,SYM&7A |  |
| 6 |  |  |  | MOV | ARG,(SP) | ;REGISTER MODE |
| 7 |  |  |  | .IFF |  |  |
| 8 |  |  |  | MOV | #ARG,(SP) | ;NON-REGISTER MODE |
| 9 |  |  |  | .ENDC |  |  |
| 10 |  |  |  | .ENDM |  |  |
| 11 |  |  |  |  |  |  |
| 12 |  |  |  |  |  |  |
| 13 | 000000 | 000000 | TEMP: | .WORD | P |  |
| 14 |  |  |  |  |  |  |
| 15 |  |  |  |  |  |  |
| 16 | 000002 |  |  | SAVE | R1 |  |
|  |  | 000001 |  | .NTYPE | SYM,R1 |  |
|  |  |  |  | .IF | EQ,SYM&7A |  |
|  | 000002 | 010146 |  | MOV | R1,(SP) | ;REGISTER MODE |
|  |  |  |  | .IFF |  |  |
|  |  |  |  | MOV | #R1,(SP) | ;NON-REGISTER MODE |
|  |  |  |  | .ENDC |  |  |
| 17 |  |  |  |  |  |  |
| 18 |  |  |  |  |  |  |
| 19 | 000004 |  |  | SAVE | TEMP |  |
|  |  | 000067 |  | .NTYPE | SYM,TEMP |  |
|  |  |  |  | .IF | EQ,SYM&7A |  |
|  |  |  |  | MOV | TEMP,(SP) | ;REGISTER MODE |
|  |  |  |  | .IFF |  |  |
|  | 000004 | 012746 |  | MOV | #TEMP,(SP) | ;NON-REGISTER MODE |
|  |  | 000000' |  |  |  |  |
|  |  |  |  | .ENDC |  |  |
| 20 |  |  |  |  |  |  |
| 21 |  |  |  |  |  |  |
| 22 |  | 000001 |  | .END |  |  |

For additional information concerning addressing modes, refer to Chapter 5 and Appendix B, Section B.2.

### 7.5 .ERROR AND .PRINT DIRECTIVES

The .ERROR directive is used to output messages to the listing file during assembly pass 2. A common use of this directive is to provide a diagnostic announcement of a rejected or erroneous macro call or to alert the user to the existence of an illegal set of conditions specified in a conditional assembly. If the listing file is not specified, the .ERROR messages are output to the command output device. The .ERROR directive takes the form:

label: .ERROR expr ;text

where: label represents an optional statement label.

expr represents an optional expression whose value is output when the .ERROR directive is encountered during assembly.

; denotes the beginning of the text string.

text represents the specified message associated with
the .ERROR directive.

Upon encountering an .ERROR directive anywhere in a source program, MACRO-11 outputs a single line containing:

1. An error code (P)

2. The sequence number of the .ERROR directive statement

3. The value of the current location counter

4. The value of the expression, if one is specified

5. The source line containing the .ERROR directive.

For example, the following directive:

    .ERROR A ;INVALID MACRO ARGUMENT

causes a line in the following form to be output to the listing file:

Seq. Loc. Exp.
No. No. Value

Text

P 512 005642 000076 .ERROR A ;INVALID MACRO ARGUMENT

The .PRINT directive is identical in function to the .ERROR directive, except that it is not flagged with the P error code.

### 7.6 INDEFINITE REPEAT BLOCK DIRECTIVES: .IRP AND .IRPC

An indefinite repeat block is a structure that is similar to a macro definition; essentially a macro definition that has only one dummy argument. At each expansion of the indefinite repeat range, this dummy argument is replaced with successive elements of a specified real argument list. An indefinite repeat block directive and its associated repeat range are coded in-line within the source program. This type of macro definition and expansion does not require calling the macro by name, as required in the expansion of conventional macros previously described in this section.

An indefinite repeat block can appear either within or outside another macro definition, indefinite repeat block, or repeat block (see Section 7.7). The rules for specifying indefinite repeat block arguments are the same as for specifying macro arguments (see Section 7.3).

#### 7.6.1 .IRP Directive

The .IRP directive is used to replace a dummy argument with successive real arguments specified in an argument string. This replacement process occurs during the expansion of an indefinite repeat block range. This directive takes the following form:

label: .IRP sym,<argument list>
.
.
.
(range of indefinite repeat block)
.
.
.
.ENDM

where: label represents an optional statement label.

sym represents a dummy argument that is successively replaced with the specified real arguments enclosed within the angle brackets. If no dummy argument is specified, the .IRP directive is flagged with an error code (A) in the assembly listing.

, represents any legal separator (comma, space, and/or tab).

<argument list> represents a list of real arguments enclosed within angle brackets that is to be used in the expansion of the indefinite repeat range. A real argument may consist of one or more characters; multiple arguments must be separated by any legal separator (comma, space, and/or tab). If no real arguments are specified, no action is taken.

range represents the block of code to be repeated once for each occurrence of a real argument in the list. The range may contain other macro definitions and repeat ranges. The .MEXIT directive (see Section 7.1.3) is legal within the range of an indefinite repeat block.

.ENDM indicates the end of the indefinite repeat block range.

An example of the use of the .IRP directive is shown in Figure 7-1.

#### 7.6.2 .IRPC Directive

The .IRPC directive is available to permit single character substitution, rather than argument substitution. On each iteration of the indefinite repeat range, the dummy argument is replaced with each successive character in the specified string. The .IRPC directive is specified as follows:

```txt
label: .IRPC sym,<string>
.
.
.
(range of indefinite repeat block)
.
.
.
.ENDM
where: label represents an optional statement label.
```

sym represents a dummy argument that is successively replaced with the specified real arguments enclosed within the angle brackets. If no dummy argument is specified, the .IRPC directive is flagged with an error code (A) in the assembly listing.

, represents any legal separator (comma, space, and/or tab).

<string> represents a list of characters enclosed within angle brackets to be used in the expansion of the indefinite repeat range. Although the angle brackets are required only when the string contains separating characters, their use is recommended for legibility.

range represents the block of code to be repeated once for each occurrence of a character in the list. The range may contain macro definitions and repeat ranges. The .MEXIT directive (see Section 7.1.3) is legal within the range of an indefinite repeat block.

.ENDM indicates the end of the indefinite repeat block range.

An example of the use of the .IRPC directive is shown in Figure 7-1.

[figure from original manual omitted]

Figure 7-1 Example of .IRP and .IRPC Directives

### 7.7 REPEAT BLOCK DIRECTIVE: .REPT, .ENDR

It is sometimes useful to duplicate a block of code a number of times in-line with other source code. This duplication of code is accomplished by creating a repeat block, using a directive in the form:

label: .REPT exp
.
.
.
(range of repeat block)
.
.
.
.ENDM

where: label represents an optional statement label.

exp represents any legal expression whose value controls the number of times the block of code is to be assembled within the program. When the expression value is less than or equal to zero (0), the repeat block is not assembled. If this expression is not an absolute value, the .REPT statement is flagged with an error code (A) in the assembly listing.

range represents the block of code to be repeated the number of times determined by the specified expression value. The repeat block may contain macro definitions, indefinite repeat blocks, or other repeat blocks. The .MEXIT directive is legal within the range of a repeat block.

.ENDM indicates the end of the repeat block range. The
or terminating statement in a repeat block can be
.ENDR either an .ENDM directive or an .ENDR directive.

### 7.8 MACRO LIBRARY DIRECTIVE: .MCALL

The .MCALL directive allows you to indicate in advance those system and/or user-defined macro definitions that are required in the assembly of the source program. The .MCALL directive allows you to specify the names of all system or user macro definitions not defined within the source program but which are required to assemble the program. The .MCALL directive must appear before the first occurrence of a call to any externally-defined macro. The .MCALL directive is of the form:

    .MCALL arg1,arg2,...argn

where: arg1, represent the symbolic names of the macro
arg2,... definitions required in the assembly of the source
argn program. The symbolic macro names may be
separated by any legal separator (comma, space,
and/or tab).

The .MCALL directive thus provides the means to access both user-defined and system macro libraries during assembly.

The /ML switch under RSX-11 and the /LIBRARY qualifier under IAS and RT-11, specified in connection with an input file specification, indicate to MACRO-11 that the file is a macro library. When a macro call is encountered in the source program, MACRO-11 first searches the user macro library for the named macro definitions, and, if necessary, continues the search with the system macro library.

Any number of such user-supplied macro files may be designated. In cases of multiple library files, the search for the named macros begins with the last such file specified. The search continues in reverse order until the required macro definitions are found, terminating again, if necessary, with a search of the system macro library.

If any named macro is not found upon completion of the search, i.e., if the macro is not defined, the .MCALL statement is flagged with an error code (U) in the assembly listing. Furthermore, a statement elsewhere in the source program which attempts to expand such an undefined macro is flagged with an error code (O) in the assembly listing.

The command strings to MACRO-11, through which file specifications are supplied, are described in detail in the appropriate system manual (see Section 0.3 in the Preface).
