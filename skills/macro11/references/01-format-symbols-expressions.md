# MACRO-11 Reference: Preface, Ch.1 Features, Ch.2 Source Program Format, Ch.3 Symbols and Expressions

Source: DEC PDP-11 MACRO-11 Language Reference Manual, AA-5075A-TC (Aug 1977). OCR-converted; code examples may have lost alignment, and a few table rows/headings were dropped by OCR.

Contents:
- PREFACE
- 0.1 MANUAL OBJECTIVES AND READER ASSUMPTIONS
- 0.2 STRUCTURE OF THE DOCUMENT
- 0.3 ASSOCIATED DOCUMENTS
- 0.4 DOCUMENT CONVENTIONS
- CHAPTER 1
- 1.1 OVERVIEW OF MACRO-11
- 1.1.1 Assembly Pass 1
- 1.1.2 Assembly Pass 2
- CHAPTER 2
- 2.1 PROGRAMMING STANDARDS AND CONVENTIONS
- 2.2 STATEMENT FORMAT
- 2.2.1 Label Field
- 2.2.2 Operator Field
- 2.2.3 Operand Field
- 2.2.4 Comment Field
- 2.3 FORMAT CONTROL
- CHAPTER 3
- 3.1 CHARACTER SET
- 3.1.1 Separating and Delimiting Characters
- 3.1.2 Illegal Characters
- 3.1.3 Unary and Binary Operators
- 3.2 MACRO-11 SYMBOLS
- 3.2.1 Permanent Symbols
- 3.2.2 User-Defined and Macro Symbols
- 3.3 DIRECT ASSIGNMENT STATEMENTS
- 3.4 REGISTER SYMBOLS
- 3.5 LOCAL SYMBOLS
- 3.6 CURRENT LOCATION COUNTER
- 3.7 NUMBERS
- 3.8 TERMS
- 3.9 EXPRESSIONS

---

### PREFACE

### 0.1 MANUAL OBJECTIVES AND READER ASSUMPTIONS

The intent of this manual is to enable users to develop programs coded in the MACRO-11 assembly language. No prior knowledge of the MACRO-11 Relocatable Assembler is assumed.

Although the description of the assembly language is wholly self-contained within this manual, the reader is assumed to be familiar with the PDP-11 processors and related terminology, as presented in the PDP-11 Processor Handbooks. No attempt is made in this document to describe the PDP-11 hardware or the functions of the various PDP-11 instructions.

Since the development of programs necessarily involves linking to create an executable image, the reader is encouraged to become familiar with this process, as presented in the applicable system manual (see Section 0.3).

In presenting MACRO-11, a tutorial bias has been adopted to enlarge upon the reference material. This posture is reflected in the examples and the accompanying commentary describing MACRO-11 language elements in typical applications. Portions of text that are shaded indicate that a particular MACRO-11 feature is not available in the 8K version of MACRO-11.

### 0.2 STRUCTURE OF THE DOCUMENT

This manual contains three parts. Part I, consisting of two chapters, briefly introduces MACRO-11. Chapter 1 lists the key features of MACRO-11, and Chapter 2 identifies the advantages of following programming standards and conventions. Also described is the format used in coding MACRO-11 source programs.

Part II, consisting of three chapters, presents general information essential to programming with the MACRO-11 assembly language. Chapter 3 describes the symbols, terms, and expressions that form the elements of MACRO-11 instructions. The character set is listed, and the types of programming symbols that may be defined by the user are discussed. Chapter 4 describes the output of MACRO-11 and presents concepts essential to the proper relocation and linking of object modules. Chapter 5 briefly describes how data stored in memory can be accessed and manipulated using the addressing modes recognized by the PDP-11 hardware.

Part III, consisting of two chapters, describes the MACRO-11 directives that control the processing of source statements during assembly. Chapter 6 discusses directives which accomplish generalized MACRO-11 functions, while Chapter 7 deals with directives used in the definition and expansion of macros.

```txt
Finally, several appendixes are provided, supplying additional information of interest to the MACRO-11 programmer.
```

Appendix A lists the ASCII and Radix-50 character sets that may be used in MACRO-11 programs. Appendix B lists the special characters recognized by MACRO-11, summarizes the syntax of the various addressing modes used in PDP-11 processors, and briefly describes the MACRO-11 directives in alphabetical order. The permanent symbols that have been defined for use with MACRO-11 are listed alphabetically in Appendix C.

The diagnostic error codes produced by MACRO-11 to identify various types of errors detected during the assembly process are listed alphabetically in Appendix D. Appendix E contains a sample coding standard that is recommended practice in preparing MACRO-11 programs. Appendix F discusses several methods of conserving dynamic memory space for users of small systems who may experience difficulty in assembling MACRO-11 programs.

Appendix G is a discussion of position independent code (PIC).

### 0.3 ASSOCIATED DOCUMENTS

The reader should refer to the applicable documentation directory listed below for descriptions of documents associated with this manual.

IAS Documentation Directory

RSX-11D Documentation Directory

```txt
RSX-11M/RSX-11S Documentation Directory
```

```txt
RT-11 Documentation Directory
```

### 0.4 DOCUMENT CONVENTIONS

The symbols defined below are used throughout this manual.

```txt
Symbol    Definition
[]        Brackets indicate that the enclosed argument is optional.
||        Vertical bars indicate that a single choice must be made from a list of arguments.
...        Ellipsis indicates optional continuation of an argument list in the form of the last specified argument.
```

UPPER-CASE Upper-case characters indicate elements of the language CHARACTERS that must be used exactly as shown.

lower-case characters    Lower-case characters indicate elements of the language that are supplied by the programmer.

(n)

In some instances the symbol (n) is used following a number to indicate the radix. For example, 100(8) indicates that 100 is an octal value, while 100(10) indicates a decimal value.

PART I

INTRODUCTION TO MACRO-11

## CHAPTER 1

**MACRO-11 FEATURES**

The MACRO-11 Assembler provides the following features:

1. Source and command string control of assembly functions

2. Device and filename specifications for input and output files

3. Error listing on command output device

4. Alphabetized, formatted symbol table listing; optional cross-reference listing of symbols

5. Relocatable object modules

6. Global symbols for linking object modules

7. Conditional assembly directives

8. Program sectioning directives

9. User-defined macros and macro libraries

10. Comprehensive system macro library

11. Extensive source and command string control of listing functions.

### 1.1 OVERVIEW OF MACRO-11

MACRO-11 is a 2-pass assembler. The functions and operations relevant to each assembly pass are described in the following sections.

#### 1.1.1 Assembly Pass 1

The main purpose of assembly pass 1 is to locate and read all required macros from libraries; to build symbol tables and program section tables for the program; while also performing a rudimentary assembly of each source statement.

The first stage of assembly pass l is the initialization of all impure data areas that MACRO-11 uses internally for the assembly process. These areas include all dynamic storage areas and buffer areas used as file storage regions.

After initializing memory areas, MACRO-ll issues a call to a system subroutine which transfers a command line into memory. This command line contains the specifications of the files to be used during assembly. After scanning the command line for proper syntax, MACRO-11 initializes the specified output files. These files are opened to determine if valid output file specifications have been passed in the command line. They are then closed to minimize requirements for active file space.

As the assembly process begins, MACRO-11 initiates a routine which retrieves source lines from the input file. If no such file is currently open, as is the case at the beginning of assembly, MACRO-11 opens the next input file specified in the command line previously read and begins to assemble the source statements. MACRO-11 determines the length of each instruction and assembles it accordingly as one word, two words, or three words.

At the end of assembly pass 1, MACRO-11 reopens the output files described above and writes out information that is to be used later in linking the object modules. Such information as the object module name, the program version number, and the global symbol directory (GSD) entries for each program section are output to the object file. After writing out the GSD entries for a given program section, MACRO-11 scans through the symbol tables to find all the global symbols that are bound to that particular program section. MACRO-11 then writes out GSD records to the object file for these symbols. This process continues for each program section, bringing to a close assembly pass 1.

#### 1.1.2 Assembly Pass 2

As an integral part of pass 2, MACRO-11 simultaneously writes the object records to the output file and generates the assembly listing, followed by the symbol table listing for the program. A cross-reference listing may also be generated.

Basically, assembly pass 2 consists of the same steps performed in assembly pass 1, except that all source statements containing MACRO-ll-detected errors are flagged with an error code as the assembly listing file is created. The object file that is created as the final consequence of pass 2 contains all the object records, together with relocation records containing information necessary for subsequent linking of the object file.

The information thus passed enables the global symbols in the object modules to be associated with absolute or virtual memory addresses, thereby forming an executable body of code.

The user may wish to become familiar with the macro object file format and description. This information is presented in the applicable system manual (see Section 0.3 in the Preface).

## CHAPTER 2

**SOURCE PROGRAM FORMAT**

### 2.1 PROGRAMMING STANDARDS AND CONVENTIONS

Assembly level programming deals directly with the host hardware. Hence, great care must be exercised in establishing programming standards and conventions to enable code written by one group to be interchanged easily with another group. Standards provide a number of advantages. When applied to the program development process, standards make the programming effort easier to:

```ignorefile
Plan
Comprehend
Test
Modify
Convert
```

Even though standards must accommodate local requirements, many aspects of the program development process have universal applicability. The standards common to all of DIGITAL's PDP-11 software products are presented in Appendix E as a model for users. Observance of these standards is beneficial to DIGITAL and its users, by simplifying both communications and the continuing task of software maintenance and enhancement.

### 2.2 STATEMENT FORMAT

A source program is composed of a sequence of source coding lines. Each line contains a single assembly-language statement. MACRO-11 will accept a source line of 132 characters, but 80 characters is the recommended length, because of constraints imposed by listing format and terminal line size.

A MACRO-11 statement may consist of as many as four fields. These fields are identified by their order of appearance within the statement and/or by specified separating characters between fields. The general format of a MACRO-11 statement is:

Label: Operator Operand ;Comment(s)

The label and comment fields are optional. The operator and operand fields are interdependent, i.e., when both fields are present in a source statement, each field is evaluated by MACRO-11 in the context of the other.

A statement may contain an operator field and no operand field, but the reverse is not true. A statement containing an operand with no operator does not conform to established MACRO-11 coding conventions; such a statement is currently interpreted by MACRO-11 during assembly as an implicit .WORD directive (see Section 6.3.2).

MACRO-11 interprets and processes source program statements one by one, generating one or more binary instructions or data words, or performing a specified assembly process. Blank lines, although legal, have no significance in the source program.

An assembly-language statement must be completed on one source line; no continuation lines are allowed in MACRO-11.

The tab character can be used in the source statement to format the fields into aligned columns in accordance with DIGITAL's standard source program format, as shown below:

Label - begins in column 1

Operator - begins in column 9

Operand(s) - begin(s) in column 17

Comment(s) - begin(s) in column 33.

For example, the following statement should be formatted in the source program into specific columns, increasing its readability in the assembly listing:

REGTST:BIT#MASK,VALUE;COMPARES BITS IN OPERANDS.

1 9 17 33 (columns)

REGTST: BIT #MASK,VALUE ;COMPARES BITS IN OPERANDS.

The above formatting conventions are not mandatory in coding MACRO-11 programs (free-field coding is permissible). However, it is recommended that source programs be prepared in accordance with these conventions for consistency and clarity.

#### 2.2.1 Label Field

A label is a means of symbolically referring to a location in a program.

A label is a user-defined symbol which is assigned the value of the current location counter and entered into the user-defined symbol table. The current location counter is the means by which MACRO-11 assigns memory addresses to the source program statements as they are encountered during the assembly process. The address value of the label is absolute or relocatable, depending on whether the current program section being assembled is absolute or relocatable. (The concept of program sections and the attributes that may be specified for them are discussed in detail in Section 6.8.)

In the case of an absolute program section, the value of the current location counter is likewise absolute, i.e., its value references an absolute virtual memory address (such as location 100). Similarly, the value of the current location counter in a relocatable program section is also relocatable; however, a relocation bias calculated at link time will be added to the apparent value of the current location counter to establish its effective absolute virtual address at execution time.

If present, a label always appears as the first field in a source statement and must be terminated by a colon. For example, if the current location counter value is absolute 100(8), the statement:

    ABCD: MOV A,B

assigns the value 100(8) to the label ABCD. Subsequent references to this label would then yield a value of absolute 100(8). In this example, if the location counter value were relocatable, the final value of ABCD would be 100(8)+K, where K represents the relocation bias of the program section, as calculated by the Task Builder at link time.

More than one label may appear within a single label field. Each label so specified is assigned the same address value. For example, if the current location counter value is 100(8), the multiple labels in the following statement:

ABC: \$DD: A7.7: MOV A,B

are each assignet uhe value 100(8).

Multiple labels may also appear on successive lines. For example, the statements

ABC:
\$DD:
A7.7:    MOV     A,B

likewise cause the same current location counter value to be assigned to all three labels.

Of the two methods of assigning multiple labels shown above, the second is preferred, because consistency of field positioning within the source program improves readability.

A double colon (::) defines the label as a global symbol. Such a label can be referenced by independently-assembled object modules. References to this label in other modules will be resolved when the modules are linked as a composite executable image. For example, the statement

    ABCD:: MOV A,B

establishes the label ABCD as a global symbol. The distinguishing attribute of a global symbol is that it can be referenced from within an object module other than the module in which the symbol is defined (see Section 6.9).

The legal characters for defining labels are:

A through Z
U through 9
. (Period)
\$ (Dollar Sign)

**NOTE:**

By convention, the dollar sign (\$) and period (.) are reserved for use in defining DIGITAL system software symbols. Therefore these characters should not be used in defining labels in MACRO-ll source programs.

A label may be any length; however, only the first six characters are significant and, therefore, must be unique among all the labels in the source program. All labels are terminated by a colon (:), which is not considered part of the label. It is a mandatory delimiter. An error code (M) is generated in the assembly listing if the first six characters in two or more labels are the same (see Appendix D).

A symbol used as a label must not be redefined within the source program. If the symbol is redefined, a label with a multiple definition results, causing MACRO-11 to generate an error code (M) in the assembly listing (see Appendix D). Furthermore, any statement in the source program which references a multi-defined label results in an additional diagnostic message; in this case, an error code (D) is generated in the assembly listing (see Appendix D).

#### 2.2.2 Operator Field

The operator field specifies the action to be performed. It may consist of an instruction mnemonic (op code), an assembler directive, or a macro call.

The operator field follows the label field in a source statement. Chapters 6 and 7 describe these three types of operator field entries.

When the operator is an instruction mnemonic, the mnemonic op code specifies the machine instruction to be generated. MACRO-11 then continues with the evaluation of the address(es) of the operand(s) which follow(s). When the operator is a directive, the directive causes MACRO-11 to perform certain control actions or processing operations during the assembly of the source program. When the operator is a macro call, MACRO-11 inserts the code generated by the macro expansion.

The operator field need not be preceded by a label; but it may be preceded by one or more labels and followed by one or more operands and/or a comment. Furthermore, leading and trailing spaces or tabs in the operator field have no significance; such characters serve only to separate the operator field from the preceding and following fields.

An operator is terminated by a space, tab, or any non-RAD50 character, as in the following examples:

MOV A,B ;THE SPACE TERMINATES THE OPERATOR
;MOV.

MOV A,B ;THE TAB TERMINATES THE OPERATOR MOV.

MOV@A,B                      ;THE @ CHARACTER TERMINATES THE
                     ;OPERATOR MOV.

Although the statements above are all equivalent in function, the second statement is the recommended form because it conforms to MACRO-11 coding conventions.

#### 2.2.3 Operand Field

When the operator field contains an instruction mnemonic (op code), the operand field specifies those program variables that are to be

evaluated/manipulated by the operator. The operand field may also be used to supply arguments to MACRO-11 directives and macro calls, as described in Chapters 6 and 7, respectively.

Operands may be expressions or symbolic arguments (within the context of the specified operation). Multiple expressions used in the operand field of a MACRO-ll statement must be separated by a comma; multiple symbolic arguments similarly used may be delimited by any legal separator, i.e., a comma, tab, and/or space. An operand should be preceded by an operator field; if it is not, the statement is treated by MACRO-ll as an implicit .WORD directive (see Section 6.3.2).

When the operator field contains an op code, associated operands are always expressions, as shown in the following statement:

$$
\text {MOV} \quad \mathrm{R0,A+2(R1)}
$$

On the other hand, when the operator field contains a MACRO-11 directive or a macro call, associated operands are normally symbolic arguments, as shown in the following statement:

    .MACRO ALPHA ARG1,ARG2

Refer to the description of each MACRO-11 directive to determine the type and number of operands required in issuing the directive.

The operand field is terminated by a semicolon when the field is followed by a comment. For example, in the following statement:

the tab between MOV and A terminates the operator field and defines the beginning of the operand field; a comma separates the operands A and B; and a semicolon terminates the operand field and defines the beginning of the comment field. When no comment field follows, the operand field is terminated by the end of the source line.

#### 2.2.4 Comment Field

The comment field normally begins in column 33 and extends through the end of the line. This field is optional and may contain any ASCII characters except null, RUBOUT, carriage-return, line-feed, vertical-tab or form-feed. All other characters appearing in the comment field, even special characters reserved for use in MACRO-11, are checked only for ASCII legality and then included in the assembly listing as they appear in the source text.

All comment fields must begin with the semicolon character(); When lengthy comments extend beyond the end of the source line (column 80), the comment may be resumed in a following line. Such a line must contain a leading semicolon, and it is suggested that the body of the comment be continued in the same columnar position in which the comment began. A comment line can also be included as an entirely separate line within the code body.

Comments do not affect assembly processing or program execution. However, comments are useful in source listings for later analysis, debugging, or documentation purposes.

### 2.3 FORMAT CONTROL

Horizontal formatting of the source program is controlled by the space and tab characters. These characters have no effect on the assembly process unless they are embedded within a symbol, number, or ASCII text string, or unless they are used as the operator field terminator. Thus, the space and tab characters can be used to provide an orderly and readable source program, as reflected by the following statements:

LABEL:MOV(SP)+,TAG;POP VALUE OFF STACK.

No spaces or tabs have been used to separate the fields in this statement. Note the difficulty in recognizing where one field ends and the next begins.

LABEL: MOV (SP)+,TAG ;POP VALUE OFF STACK.

This statement conforms to the standard horizontal formatting conventions, i.e., the statement elements are separated into four distinct fields and are therefore easily discernible.

Page formatting and assembly listing considerations are discussed in Chapter 6 in the context of MACRO-11 directives that may be specified to accomplish desired formatting operations. Appendix E describes the coding conventions used in all DIGITAL PDP-11 operating system software.

PART II

PROGRAMMING
IN MACRO-11 ASSEMBLY
LANGUAGE

## CHAPTER 3

**SYMBOLS AND EXPRESSIONS**

This chapter describes the components of MACRO-11 instructions. The character set, the conventions observed in constructing symbols, and the use of numbers, operators, terms and expressions are discussed as they relate to MACRO-11 programming.

### 3.1 CHARACTER SET

The following characters are legal in MACRO-11 source programs:

1. The letters A through Z. Both upper- and lower-case letters are acceptable, although, upon input, lower-case letters are converted to upper-case (see Section 6.2, .ENABL LC).

2. The digits 0 through 9.

3. The characters . (period) and \$ (dollar sign). These characters are reserved for use as Digital Equipment Corporation system program symbols.

4. The special characters listed in Table 3-1.

Table 3-1
Special Characters Used in MACRO-11

| Character | Designation | Function |
| --- | --- | --- |
| : | Colon | Label terminator. |
| :: | Double colon | Label terminator; defines the label as a global label. |
| = | Equal sign | Direct assignment operator; and macro keyword indicator. |
| == | Double equal sign | Direct assignment operator; defines the symbol as a global symbol. |
| % | Percent sign | Register term indicator. |
|  | Tab | Item or field terminator. |
|  | Space | Item or field terminator. |

(Continued on next page)

Table 3-1 (Cont.)
Special Characters Used in MACRO-11

| Character | Designation | Function |
| --- | --- | --- |
| # | Number sign | Immediate expression indicator. |
| @ | At sign | Deferred addressing indicator. |
| ( | Left parenthesis | Initial register indicator. |
| ) | Right parenthesis | Terminal register indicator. |
| . | Period | Current location counter |
| , | Comma | Operand field separator. |
| ; | Semicolon | Comment field indicator. |
| < | Left angle bracket | Initial argument or expression indicator. |
| > | Right angle bracket | Terminal argument or expres-sion indicator. |
| + | Plus sign | Arithmetic addition operator or autoincrement indicator. |
| - | Minus sign | Arithmetic subtraction operator or autodecrement indica-tor. |
| * | Asterisk | Arithmetic multiplication op-erator. |
| / | Slash | Arithmetic division operator. |
| & | Ampersand | Logical AND operator. |
| ! | Exclamation point | Logical inclusive OR operator. |
| " | Double quote | Double ASCII character indica-tor. |
| ' | Single quote | Single ASCII character indica-tor; or concatenation indicator. |
| ^ | Up arrow or circumflex | Universal unary operator or argument indicator. |
| \\ | Backslash | Macro call numeric argument indicator. |

#### 3.1.1 Separating and Delimiting Characters

Legal separating characters and legal argument delimiters are defined below in Tables 3-2 and 3-3 respectively.

Table 3-2

Legal Separating Characters

| Character | Definition | Usage |
| --- | --- | --- |
| Space | One or more spaces and/or tabs | A space is a legal separator between instruction fields and between symbolic arguments within the operand field. Spaces within expressions are ignored (see Section 3.9). |
| , | Comma | A comma is a legal separator between symbolic arguments within the operand field. Multiple expressions used in the operand field must be separated by a comma. |

Table 3-3

Legal Argument Delimiters

| Character | Definition | Usage |
| --- | --- | --- |
|  | Paired angle brackets | Paired angle brackets may be used anywhere in a program to enclose an expression for treatment as a single term. Paired angle brackets are also used to enclose a macro argument, particularly when that argument contains separating characters (see Section 7.3). |
| ^x...x | Up-arrow (unary operator) construction, where the up-arrow is followed by an argument that is bracketed by any paired printing characters (x). | This construction is equivalent in function to the paired angle brackets described above and is generally used only where the argument itself contains angle brackets. |

#### 3.1.2 Illegal Characters

A character is determined to be illegal for one of two reasons:

1. A character is not an element of the recognized MACRO-ll character set. A character of this kind is replaced in the listing by a question mark, and an error code (I) is printed in the assembly listing (see Appendix D). The exception to this is an embedded null which, when detected, terminates the scan of the current line.

2. A legal MACRO-11 character is illegal in the context of its usage within the source statement, i.e., its syntax is illegal or questionable. Such a character causes an error code (Q) to be printed in the assembly listing.

#### 3.1.3 Unary and Binary Operators

Legal MACRO-11 unary operators are described in Table 3-4. Unary operators are used in connection with single terms (arguments or operands) to indicate an action to be performed on that term during assembly. A term preceded by a unary operator is considered to contain that operator. The term so specified thus becomes a value which can be used alone or as an element of an expression.

Table 3-4

Legal Unary Operators

<table><tr><td>Unary Operator</td><td>Explanation</td><td>Example</td><td>Effect</td></tr><tr><td>+</td><td>Plus sign</td><td>+A</td><td>Produces the positive value of A.</td></tr><tr><td>-</td><td>Minus sign</td><td>-A</td><td>Produces the negative (2's complement) value of A.</td></tr><tr><td rowspan="6">^</td><td rowspan="6">Up-arrow, universal unary operator.(This usage is described in detail in Section 6.4.)</td><td>^C24</td><td>Produces the l's complement value of 24(8).</td></tr><tr><td>^D127</td><td>Interprets 127 as a decimal number.</td></tr><tr><td colspan="2"></td></tr><tr><td>^034</td><td>Interprets 34 as an octal number.</td></tr><tr><td>^B11000111</td><td>Interprets 11000111 as a binary number.</td></tr><tr><td>^RABC</td><td>Evaluates ABC in Radix-50 form.</td></tr></table>

Unary operators can be used adjacent to each other or in constructions involving multiple terms, as shown below:

$$
\begin{array}{l l} - ^ {\wedge} \mathrm{D} 5 0 & (\text {Equivalent to} - <   ^ {\wedge} \mathrm{D} 5 0 >) \\ ^ {\wedge} \mathrm{C} ^ {\wedge} \mathrm{O} 1 2 & (\text {Equivalent to} ^ {\wedge} \mathrm{C} <   ^ {\wedge} \mathrm{O} 1 2 >) \end{array}
$$

Legal MACRO-11 binary operators are described in Table 3-5. In contrast to unary operators, binary operators specify actions to be performed on multiple items or terms within an expression. Table 3-5 shows the relationships that can be established between expression terms through the use of binary operators.

Table 3-5
Legal Binary Operators

| Binary Operator | Explanation | Example |
| --- | --- | --- |
| + | Addition | A+B |
| - | Subtraction | A-B |
| * | Multiplication | A*B (16-bit product returned) |
| / | Division | A/B (16-bit quotient returned) |
| & | Logical AND | A&B |
| ! | Logical inclusive OR | A!B |

All binary operators have equal priority. Items or terms can be grouped for evaluation within an expression by enclosing them within angle brackets. Terms so enclosed are evaluated first, and remaining operations are performed from left to right, as shown in the examples below:

| .WORD | 1+2*3 | ;EQUALS 11(8). |
| --- | --- | --- |
| .WORD | 1+<2*3> | ;EQUALS 7(8). |

### 3.2 MACRO-11 SYMBOLS

Three types of symbols may be defined for use within MACRO-11 source programs: permanent symbols, user-defined symbols, and macro symbols. MACRO-11 maintains three types of symbol tables: the Permanent Symbol Table (PST), the User Symbol Table (UST), and the Macro Symbol Table (MST). The PST contains all the permanent symbols defined within (and thus automatically recognized by) MACRO-11 and is part of the MACRO-11 image. The UST and MST are constructed as the source program is assembled.

#### 3.2.1 Permanent Symbols

Permanent symbols consist of the instruction mnemonics (see Appendix C) and MACRO-11 directives (see Chapters 6 and 7 and Appendix B). These symbols are a permanent part of the MACRO-11 image and need not be defined before being used in the operator field of a MACRO-11 source statement (see Section 2.2.2).

#### 3.2.2 User-Defined and Macro Symbols

User-defined symbols are those symbols treated by the programmer as labels (see Section 2.2.1) or that are equated to a specific value through a direct assignment statement (see Section 3.3) or appear as macro names or dummy arguments. These symbols are added to the User Symbol Table as they are encountered during assembly. Macro symbols are those symbols used as macro names (see Section 7.1). Similarly, these symbols are added to the Macro Symbol Table as they are encountered during assembly.

User-defined and macro symbols can be composed of alphanumeric characters, dollar signs (\$), and periods (.) only; any other character is illegal.

**NOTE:**

The dollar sign (\$) and period (.) characters are reserved for use in defining Digital Equipment Corporation system software symbols. For example, READ\$ is a file-processing system macro. The user is cautioned not to employ these characters in constructing user-defined symbols or macro symbols in order to avoid possible conflicts with existing or future Digital Equipment Corporation system software symbols.

The following rules govern the creation of user-defined and macro symbols:

1. The first character of a symbol must not be a number (except in the case of local symbols; see Section 3.5).

2. The first six characters of a symbol must be unique.

3. A symbol can be written with more than six legal characters, but the seventh and subsequent characters are checked only for ASCII legality and are not otherwise evaluated or recognized by MACRO-11.

4. Spaces, tabs, and illegal characters must not be embedded within a symbol. The legal MACRO-11 character set is defined in Section 3.1.

The value of a symbol depends upon its use in the program. When a symbol appears in the operator field, it may be any one of the three symbol types described above i.e., permanent, user-defined, macro. To determine the value of an operator-field symbol, MACRO-11 searches the symbol tables in the following order:

1. Macro Symbol Table

2. Permanent Symbol Table

3. User-Defined Symbol Table

This search order allows redefinition of Permanent Symbol Table entries as macro symbols. That is, permanent symbols may be used as macro symbols. But the user must keep in mind the sequence in which the search for symbols is performed in order to avoid incorrect interpretation of the symbol's use.

When a symbol appears in the operand field, the User-Defined Symbol Table is searched first, then the Permanent Symbol Table is searched.

Depending on their use in the source program, user-defined symbols have either a local (internal) attribute or a global (external) attribute.

Normally, MACRO-11 treats all user-defined symbols as local, that is, their definition is limited to the module in which they appear. However, symbols can be explicitly declared to be global symbols through one of three methods:

1. Use of the .GLOBL directive (see Section 6.9).

2. Use of the double colon (::) in defining a label (see Section 2.2.1).

3. Use of the double equal (==) sign in a direct assignment statement (see Section 3.3).

All symbols within a module that remain undefined at the end of assembly are treated as default global references.

**NOTE:**

Undefined symbols at the end of assembly are assigned a value of 0 and placed into the user-defined symbol table as undefined default global references. If the .DSABL GBL directive is in effect, however, (see Section 6.2), the automatic global reference default function of MACRO-11 is inhibited, causing the statement containing the undefined symbol to be flagged with an error code (U) in the assembly listing (see Appendix D).

Global symbols provide linkages between independently-assembled object modules within the task image. A global symbol defined as a label, for example, may serve as an entry-point address to another section of code within the image. Such symbols are referenced from other source modules in order to transfer control throughout execution. These global symbols are resolved at link time, ensuring that the resulting image is a logically coherent and complete body of code.

### 3.3 DIRECT ASSIGNMENT STATEMENTS

A direct assignment statement allows you to equate a symbol to a specific value. When a direct assignment statement is first used to define a symbol, that symbol is entered into the User-Defined Symbol Table. A symbol defined in this manner may be redefined in a subsequent direct assignment statement by assigning a new value to the previously-defined symbol.

The general format for a direct assignment statement is:

symbol=expression

or

symbol==expression

where: expression - can have only one level of forward reference (see 5. below).

\- cannot contain an undefined global reference.

A direct assignment statement embodying the double equal (==) sign, as shown above, defines the symbol as global (see Section 6.9).

The following examples illustrate the coding of direct assignment statements:

A=1
;THE SYMBOL A IS EQUATED TO THE
;VALUE 1.

B=A-1&MASKLOW
;THE SYMBOL B IS EQUATED TO THE
;VALUE OF THE ENTIRE EXPRESSION
;WHICH FOLLOWS.

C:
D=.
E:        MOV     #1,ABLE
;THE SYMBOL D IS EQUATED TO ., AND
;THE LABELS C AND E ARE ASSIGNED A
;VALUE THAT IS EQUAL TO THE LOCATION
;OF THE MOV INSTRUCTION.

The last of the three examples above is provided only to illustrate the performance of MACRO-11 in such situations. See Section 3.6 for a description of the period (.) as the current location counter symbol.

The following conventions apply to the coding of direct assignment statements:

1. An equal sign (=) or double equal sign (==) must separate the symbol from the expression defining the symbol's value. Spaces preceding and/or following the direct assignment operators, although permissible, have no significance in the resulting value.

2. The symbol being assigned in a direct assignment statement is placed in the label field.

3. Only one symbol can be defined in a single direct assignment statement.

4. A direct assignment statement may be followed only by a comment field.

5. Only one level of forward referencing is allowed, as shown in the following example:

X=Y (Illegal forward reference)

y=z (Legal forward reference)

The above example would result in the generation of an error code (U) in the assembly listing on the line containing the illegal forward reference.

Although one level of forward referencing is allowed for local symbols, a global symbol defined in a direct assignment statement must not contain a forward reference, i.e., the global assignment expression must not itself contain an undefined reference to another symbol. Such a forward reference is illegal, causing an error code (A) to be generated in the assembly listing.

### 3.4 REGISTER SYMBOLS

The eight general registers of the PDP-11 processor are numbered 0 through 7 and can be expressed in the source program in the following manner:

where & indicates a reference to a register rather than a location. The digit specifying the register can be replaced by any legal, absolute term that can be evaluated during the first assembly pass. Use standard symbolic names for all register references.

The register definitions listed below are automatically assigned by MACRO-11, i.e., these definitions are the normal default values and remain valid for all register references within the source program.

R0=%0                      ;REGISTER 0 DEFINITION.
R1=%1                     ;REGISTER 1 DEFINITION.
R2=%2                     ;REGISTER 2 DEFINITION.
R3=%3                     ;REGISTER 3 DEFINITION.
R4=%4                     ;REGISTER 4 DEFINITION.
R5=%5                     ;REGISTER 5 DEFINITION.
SP=%6                     ;STACK POINTER DEFINITION.
PC=%7                     ;PROGRAM COUNTER DEFINITION.

Note that registers 6 and 7 are given special names because of their unique system functions.

A register symbol may be defined in a direct assignment statement appearing in the program. The defining expression of a register symbol must be a legal, absolute value. Although you can reassign the standard register symbols through the use of the .DSABL REG directive (see Section 6.2), this practice is not recommended. An attempt to redefine a default register symbol without first specifying the .DSABL REG directive to override the normal register definitions causes that assignment statement to be flagged with an error code (R) in the assembly listing. The symbolic default names assigned to the registers, as listed above, are the conventional names used in all DIGITAL-supplied PDP-11 system programs. For this reason, you are well advised to follow these conventions.

All non-standard register symbols must be defined before they are referenced in the source program. A register expression less than 0 or greater than 7 is flagged with an error code (R) in the assembly listing.

The % character may be used with any legal term or expression to specify a register. For example, the statement

CLR 83+1

is equivalent in function to the statement

CLR 84

and clears the contents of register 4.

In contrast, the statement

CLR 4

clears the contents of virtual memory location 4.

### 3.5 LOCAL SYMBOLS

Local symbols are specially formatted symbols used as labels within a block of coding that has been delimited as a local symbol block. Local symbols are of the form n\$, where n is a decimal integer from 1 to 65535, inclusive. Examples of local symbols are:

1\$
27\$
59\$
104\$

A local symbol block is delimited in one of three ways:

1. The range of a local symbol block usually consists of those statements between two normally-constructed symbolic labels (see Figure 3-1). Note that a statement of the form:

ALPHA=expression

is a direct assignment statement (see Section 3.3), but does not create a label and thus does not delimit the range of a local symbol block.

2. The range of a local symbol block is normally terminated upon encountering a .PSECT, .CSECT, or .ASECT directive in the source program (see Figure 3-1).

3. The range of a local symbol block is delimited through MACRO-11 directives, as follows:

Starting delimiter: .ENABL LSB (see Section 6.2)

Ending delimiter: .ENABL LSB

or

.DSABL LSB (see Section 6.2)

followed by one of: Symbolic label

.PSECT (see Section 6.8.1)
.CSECT (see Section 6.8.2)
.ASECT (see Section 6.8.2)

Local symbols provide a convenient means of generating labels for branch instructions and other such references within a local symbol block. Using local symbols reduces the possibility of symbols with multiple definitions appearing within a user program. In addition, the use of local symbols differentiates entry-point labels from local labels, since local symbols cannot be referenced from outside their respective local symbol block. Thus, local symbols of the same name can appear in other local symbol blocks without conflict. Local symbols do not appear in cross-reference listings.

Local symbols require less symbol table space than other types of symbols. Their use is recommended. When defining local symbols, use the range from 1\$ to 63\$ first, then the range from 128\$ to 65535\$. Local symbols within the range 64\$ through 127\$, inclusive, can be generated automatically as a feature of MACRO-11. Such local symbols are useful in the expansion of macros during assembly and are described in detail in this context in Section 7.3.5.

Be sure to avoid multiple definitions of local symbols within the same local symbol block. For example, if the local symbol 10\$ is defined two or more times within the same local symbol block, each symbol represents a different address value. Such a multi-defined symbol causes an error code (P) to be generated in the assembly listing.

For examples of local symbols and local symbol blocks as they appear in a source program, see Figure 3-1.

[figure from original manual omitted]

Figure 3-1 Assembly Listing Showing Local Symbol Block

### 3.6 CURRENT LOCATION COUNTER

The period (.) is the symbol for the current location counter. When used in the operand field of an instruction, it represents the address of the first word of the instruction, as shown in the first example below. When used in the operand field of a MACRO-11 directive, it represents the address of the current byte or word, as shown in the second example below.

A: MOV #.,RU ;THE PERIOD (.) REFERS TO THE ADDRESS ;OF THE MOV INSTRUCTION.

(The function of the # symbol is explained in Section 5.9.)

SAL=0
        .WORD    177535,.+4,SAL   ;THE OPERAND .+4 IN THE .WORD
            ;DIRECTIVE REPRESENTS A VALUE
            ;THAT IS STORED AS THE SECOND
            ;OF THREE WORDS DURING
            ;ASSEMBLY.

Assume that the current value of the location counter is 500. During assembly, MACRO-11 reserves storage in response to the .WORD directive (see Section 6.3.2), beginning with location 500. The operands accompanying the .WORD directive determine the values so stored. The

value 177535 is thus stored in location 500. The value represented by .+4 is stored in location 502; this value is derived as the current value of the location counter (which is now 502), plus the absolute value 4, thereby depositing the value 506 in location 502. Finally, the value of SAL, previously equated to 0, is deposited in location 504.

Figure 3-2 illustrates the result of the example.

| LOCATION | CONTENTS |
| --- | --- |
| 500 | 177535 |
| 502 | 506 |
| 504 | 0 |

Figure 3-2 Sample Assembly Results

At the beginning of each assembly pass, MACRO-11 resets the location counter. Normally, consecutive memory locations are assigned to each byte of object data generated. However, the value of the location counter can be changed through a direct assignment statement of the following form:

    .=expression

Similar to other MACRO-11 symbols, the current location counter symbol (.) has an attribute of relocatability associated with it: it is either absolute or relocatable, depending on the specific such attribute of the current program section. (A program section and its attributes are defined through the use of the .PSECT directive described in Section 6.8.1.) The existing attribute (or mode) of the current location counter cannot be changed by specifying a defining expression having a different attribute.

Furthermore, such a defining expression must not force the location counter into another program section (.PSECT area), even though the program sections so involved may both be absolute or relocatable. The expression defining the location counter value must not contain a forward reference, i.e., the expression must not contain a reference to a symbol that is not previously defined. Such violations constitute a general assembly error, resulting in an error code (A) in the assembly listing.

Thus, the attribute (or mode) of the current location counter takes on the attribute of the current program section. Therefore, its attribute from program section to program section can be changed only through the program sectioning directives (.PSECT, .ASECT, and .CSECT), as described in Section 6.8.

The following coding illustrates the use of the current location counter:

.ASECT
.=500
FIRST: MOV .+10,COUNT
.=520
SECOND: MOV .,INDEX
;SET LOCATION COUNTER TO
;ABSOLUTE 500(OCTAL).
;THE LABEL "FIRST" HAS THE VALUE
;500(OCTAL).
;.+10 EQUALS 510(OCTAL). THE
;CONTENTS OF THE LOCATION
;510(OCTAL) WILL BE DEPOSITED
;IN THE LOCATION "COUNT."
;THE ASSEMBLY LOCATION COUNTER
;NOW HAS A VALUE OF
;ABSOLUTE 520(OCTAL).
;THE LABEL SECOND HAS THE
;VALUE 520(OCTAL).
;THE CONTENTS OF LOCATION
;520(OCTAL), THAT IS, THE BINARY
;CODE FOR THE INSTRUCTION
;ITSELF, WILL BE DEPOSITED IN THE
;LOCATION "INDEX."

.PSECT
.=.+20
;SET LOCATION COUNTER TO
;RELOCATABLE 20 OF THE
;UNNAMED PROGRAM SECTION.
THIRD: .WORD 0
;THE LABEL THIRD HAS THE
;VALUE OF RELOCATABLE 20.

Storage areas may be reserved in the program by advancing the location counter. For example, if the current value of the location counter is 1000, each of the following statements:

$. = . + 40$

or

.BLKB 40

.BLKW 20

reserves 40(8) bytes of storage space in the source program. The .BLKB and .BLKW directives, however, are recommended as the preferred ways to reserve storage space (see Section 6.5.3).

### 3.7 NUMBERS

MACRO-11 assumes that all numbers in the source program are to be interpreted in octal radix, unless otherwise specified. An exception to this is that operands associated with Floating Point Processor instructions and Floating Point Data directives are treated as decimal (see Section 6.4.2). This default radix can be altered with the .RADIX directive (see Section 6.4.1.1). Also, individual numbers can be designated as decimal, binary, or octal numbers through temporary radix control operators (see Section 6.4.1.2).

For every statement in the source program that contains a digit that is not in the current radix, an error code (N) is generated in the assembly listing. However, MACRO-11 continues with the scan of the statement and evaluates each such number encountered as a decimal value.

Negative numbers must be preceded by a minus sign; MACRO-11 translates such numbers into two's complement form. Positive numbers may (but need not) be preceded by a plus sign.

A number containing more than 16 significant bits, i.e., greater than 177777(8), is truncated from the left and flagged with an error code (T) in the assembly listing.

Numbers are always considered to be absolute values, i.e., they are not relocatable.

Single-word floating-point numbers may be generated with the ^F operator (see Section 6.4.2.2) and are stored in the following format:

Refer to the appropriate PDP-11 Processor Handbook for details of the floating-point number format.

### 3.8 TERMS

A term is a component of an expression and may be one of the following:

1. A number, as defined in Section 3.7, whose 16-bit value is used.

2. A symbol, as defined in Section 3.2. Symbols are evaluated as follows:

a. A period (.) specified in an expression causes the value of the current location counter to be used.

b. A defined symbol is located in the User-Defined Symbol Table (UST) and its value is used.

c. A permanent symbol's basic value is used, with zero substituted for the addressing modes. (Appendix C lists all op codes and their values.)

d. An undefined symbol is assigned a value of zero and inserted in the User-Defined Symbol Table as an undefined default global reference. If the .DSABL GBL directive (see Section 6.2) is in effect, the automatic global reference default function of MACRO-ll is inhibited, in which case, the statement containing the undefined symbol is flagged with an error code (U) in the assembly listing.

3. A single quote followed by a single ASCII character, or a double quote followed by two ASCII characters. This type of expression construction is explained in detail in Section 6.3.3.

4. A term may also be an expression enclosed in angle brackets (<>). Any expression so enclosed is evaluated and reduced to a single term before the remainder of the expression in which it appears is evaluated. Angle brackets, for example, may be used to alter the left-to-right evaluation of expressions (as in A\*B+C versus A\*<B+C>), or to apply a unary operator to an entire expression (as in -<A+B>).

5. A unary operator followed by a symbol or number.

### 3.9 EXPRESSIONS

Expressions are combinations of terms joined together by binary operators (see Table 3-5) and which reduce to a 16-bit expression value. The evaluation of an expression includes the determination of its attributes. A resultant expression value may be any one of four types (as described later in this section): absolute, relocatable, external, or complex relocatable.

Expressions are evaluated from left to right with no operator hierarchy rules, except that unary operators take precedence over binary operators. A term preceded by a unary operator is considered to contain that operator. (Terms are evaluated, where necessary, before their use in expressions.) Multiple unary operators are valid and are treated as follows:

-+-A

is equivalent to:

    -<+<-A>>

A missing term, expression, or external symbol is interpreted as a zero. A missing or illegal operator terminates the expression analysis, causing an error code (A) or (Q), or both, to be generated in the assembly listing, depending on the context of the expression itself. For example, the expression:

    TAG ! LA 177777

is evaluated as

    TAG ! LA

because the first non-blank character following the symbol LA is not a legal binary operator, an expression separator (i.e., a comma), or an operand field terminator (i.e., a semicolon or the end of the source line). It should be noted that spaces within expressions are ignored.

The value of an external expression is equal to the value of the absolute part of that expression. For example, the expression EXTERN+A, where "EXTERN" is an external symbol, has a value at assembly-time that is equal to the value of the internal symbol A. This expression, however, when evaluated at link time takes on the resolved value of the symbol EXTERN, plus the value of symbol A.

Expressions, when evaluated by MACRO-11, are determined to be one of four types: absolute, relocatable, external (or global), or complex relocatable. The following distinctions are important:

1. An expression is absolute if its value is fixed. An expression whose terms are numbers and ASCII conversion characters will reduce to an absolute value. A relocatable expression or term minus a relocatable term, where both elements being evaluated belong to the same program section, are also absolute, since such an expression is reduced to a single term by MACRO-11 upon completion of the expression scan. For example, the expression TAG2-TAG1, where both TAG1 and TAG2 are defined in the same program section, is an absolute expression. Terms that contain labels defined in an absolute section will have an absolute value.

2. An expression is relocatable if its value is fixed relative to the base address of the program section in which it appears, but it will have an offset value added at link time. Terms that contain labels defined in relocatable program sections will have a relocatable value; similarly, a period (.) in a relocatable program section, representing the value of the current location counter, will also have a relocatable value.

3. An expression is external (or global) if it contains a single global reference (plus or minus an absolute expression value) that is not defined within the current program. Thus, an external expression is only partially defined following assembly and must be resolved at link time.

4. An expression is complex relocatable if any of the following conditions applies:

\- It contains a global reference and a relocatable symbol.

\- It contains more than one global reference.

\- It contains relocatable terms belonging to different program sections.

\- The value resulting from the expression has more than one level of relocation. For example, if the relocatable symbols TAG1 and TAG2 associated with the same program section are specified in an expression construction in the form TAG1+TAG2, two levels of relocation would be introduced, since each symbol is evaluated in terms of the relocation bias in effect for the program section.

\- An operation other than addition is specified on an undefined global symbol.

\- An operation other than addition, subtraction, negation, or complementation is specified for a relocatable value.

The evaluation of relocatable, external, and complex relocatable expressions is completed at link time.
