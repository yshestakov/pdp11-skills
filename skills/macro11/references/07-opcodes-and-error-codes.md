# MACRO-11 Reference: App.C Permanent symbol table (op codes with octal values, directives), App.D Assembly error codes

Source: DEC PDP-11 MACRO-11 Language Reference Manual, AA-5075A-TC (Aug 1977). OCR-converted; code examples may have lost alignment, and a few table rows/headings were dropped by OCR.

## APPENDIX C

    PERMANENT SYMBOL TABLE (PST)

The permanent symbol table (PST) contains those symbols which are automatically recognized by MACRO-11. These symbols consist of both op codes and assembler directives. The op codes (i.e., the instruction set) are listed first, followed by the directives which cause specific actions during assembly.

For a detailed description of the instruction set, see the appropriate PDP-11 Processor Handbook.

### C.1 OP CODES

| MNEMONIC | OCTAL VALUE | FUNCTIONAL NAME |
| --- | --- | --- |
| ADC | 005500 | Add Carry |
| ADCB | 105500 | Add Carry (Byte) |
| ADD | 060000 | Add Source To Destination |
| ASH | 072000 | Shift Arithmetically |
| ASHC | 073000 | Arithmetic Shift Combined |
| ASL | 006300 | Arithmetic Shift Left |
| ASLB | 106300 | Arithmetic Shift Left (Byte) |
| ASR | 006200 | Arithmetic Shift Right |
| ASRB | 106200 | Arithmetic Shift Right (Byte) |
| BCC | 103000 | Branch If Carry Is Clear |
| BCS | 103400 | Branch If Carry Is Set |
| BEQ | 001400 | Branch If Equal |
| BGE | 002000 | Branch If Greater Than Or Equal |
| BGT | 003000 | Branch If Greater Than |
| BHI | 101000 | Branch If Higher |
| BHIS | 103000 | Branch If Higher Or Same |
| BIC | 040000 | Bit Clear |
| BICB | 140000 | Bit Clear (Byte) |
| BIS | 050000 | Bit Set |
| BISB | 150000 | Bit Set (Byte) |
| BIT | 030000 | Bit Test |
| BITB | 130000 | Bit Test (Byte) |
| BLE | 003400 | Branch If Less Than Or Equal |
| BLO | 103400 | Branch If Lower |
| BLOS | 101400 | Branch If Lower Or Same |
| BLT | 002400 | Branch If Less Than |
| BMI | 100400 | Branch If Minus |
| BNE | 001000 | Branch If Not Equal |
| BPL | 100000 | Branch If Plus |
| BPT | 000003 | Breakpoint Trap |
| BR | 000400 | Branch Unconditional |
| BVC | 102000 | Branch If Overflow Is Clear |
| BVS | 102400 | Branch If Overflow Is Set |
| CALL | 004700 | Jump To Subroutine (JSR PC,xxx) |
| CCC | 000257 | Clear All Condition Codes |
| CLC | 000241 | Clear C Condition Code Bit |
| CLN | 000250 | Clear N Condition Code Bit |
| CLR | 005000 | Clear Destination |
| CLRB | 105000 | Clear Destination (Byte) |
| CLV | 000242 | Clear V Condition Code Bit |
| CLZ | 000244 | Clear Z Condition Code Bit |
| CMP | 020000 | Compare Source To Destination |
| CMPB | 120000 | Compare Source To Destination (Byte) |
| COM | 005100 | Complement Destination |
| COMB | 105100 | Complement Destination (Byte) |
| DEC | 005300 | Decrement Destination |
| DECB | 105300 | Decrement Destination (Byte) |
| DIV | 071000 | Divide |
| EMT | 104000 | Emulator Trap |
| FADD | 075000 | Floating Add |
| FDIV | 075030 | Floating Divide |
| FMUL | 075020 | Floating Multiply |
| FSUB | 075010 | Floating Subtract |
| HALT | 000000 | Halt |
| INC | 005200 | Increment Destination |
| INCB | 105200 | Increment Destination (Byte) |
| IOT | 000004 | Input/Output Trap |
| JMP | 000100 | Jump |
| JSR | 004000 | Jump To Subroutine |
| MARK | 006400 | Mark |
| MFPI | 006500 | Move From Previous Instruction Space |
| MFPS | 106700 | Move from PS (LSI-ll) |
| MOV | 010000 | Move Source To Destination |
| MOVB | 110000 | Move Source To Destination (Byte) |
| MTPI | 006600 | Move To Previous Instruction Space |
| MTPS | 106400 | Move to PS (LSI-ll) |
| MUL | 070000 | Multiply |
| NEG | 005400 | Negate Destination |
| NEGB | 105400 | Negate Destination (Byte) |
| NOP | 000240 | No Operation |
| RESET | 000005 | Reset External Bus |
| RETURN | 000207 | Return From Subroutine (RTS PC) |
| ROL | 006100 | Rotate Left |
| ROLB | 106100 | Rotate Left (Byte) |
| ROR | 006000 | Rotate Right |

PERMANENT SYMBOL TABLE (PST)

| MNEMONIC | OCTAL VALUE | FUNCTIONAL NAME |
| --- | --- | --- |
| RORB | 106000 | Rotate Right (Byte) |
| RTI | 000002 | Return From Interrupt(Permits a trace trap) |
| RTS | 000200 | Return From Subroutine |
| RTT | 000006 | Return From Interrupt(inhibits trace trap) |
| SBC | 005600 | Subtract Carry |
| SBCB | 105600 | Subtract Carry (Byte) |
| SCC | 000277 | Set All Condition Code Bits |
| SEC | 000261 | Set C Condition Code Bit |
| SEN | 000270 | Set N Condition Code Bit |
| SEV | 000262 | Set V Condition Code Bit |
| SEZ | 000264 | Set Z Condition Code Bit |
| SOB | 077000 | Subtract One And Branch |
| SUB | 160000 | Subtract Source From Destination |
| SWAB | 000300 | Swap Bytes |
| SXT | 006700 | Sign Extend |
| TRAP | 104400 | Trap |
| TST | 005700 | Test Destination |
| TSTB | 105700 | Test Destination (Byte) |
| WAIT | 000001 | Wait For Interrupt |
| XOR | 074000 | Exclusive OR |

OP CODES FLOATING POINT PROCESSOR ONLY

| MNEMONIC | OCTAL VALUE | FUNCTIONAL NAME |
| --- | --- | --- |
| ABSD | 170600 | Make Absolute Double |
| ABSF | 170600 | Make Absolute Floating |
| ADDD | 172000 | Add Double |
| ADDF | 172000 | Add Floating |
| CFCC | 170000 | Copy Floating Condition Codes |
| CLRD | 170400 | Clear Double |
| CLRF | 170400 | Clear Floating |
| CMPD | 173400 | Compare Double |
| CMPF | 173400 | Compare Floating |
| DIVD | 174400 | Divide Double |
| DIVF | 174400 | Divide Floating |
| LDCDF | 177400 | Load And Convert From Double To Floating |
| LDCFD | 177400 | Load And Convert From Floating To Double |
| LDCID | 177000 | Load And Convert Integer To Double |
| LDCIF | 177000 | Load And Convert Integer To Floating |
| LDCLD | 177000 | Load And Convert Long integer To Double |
| LDCLF | 177000 | Load And Convert Long Integer To Floating |
| LDD | 172400 | Load Double |
| LDEXP | 176400 | Load Exponent |
| LDF | 172400 | Load Floating |
| LDFPS | 170100 | Load FPPs Program Status |
| MFPD | 106500 | Move From Previous Data Space |
| MODD | 171400 | Multiply And Integerize Double |
| MODF | 171400 | Multiply And Integerize Floating |
| MTPD | 106600 | Move To Previous Data Space |
| MULD | 171000 | Multiply Double |
| MULF | 171000 | Multiply Floating |
| NEGD | 170700 | Negate Double |
| NEGF | 170700 | Negate Floating |
| SETD | 170011 | Set Double Mode |
| SETF | 170001 | Set Floating Mode |
| SETI | 170002 | Set Integer Mode |
| SETL | 170012 | Set Long Integer Mode |
| SPL | 000230 | Set Priority Level |
| STCDF | 176000 | Store And Convert From Double To Floating |
| STCDI | 175400 | Store And Convert From Double To Integer |
| STCDL | 175400 | Store And Convert From Double To Long Integer |
| STCFD | 176000 | Store And Convert From Floating To Double |
| STCFI | 175400 | Store And Convert From Floating To Integer |
| STCFL | 175400 | Store And Convert From Floating To Long Integer |
| STD | 174000 | Store Double |
| STEXP | 175000 | Store Exponent |
| STF | 174000 | Store Floating |
| STFPS | 170200 | Store FPPs Program Status |
| STST | 170300 | Store FPPs Status |
| SUBD | 173000 | Subtract Double |
| SUBF | 173000 | Subtract Floating |
| TSTD | 170500 | Test Double |
| TSTF | 170500 | Test Floating |

### C.2 MACRO-11 DIRECTIVES

| DIRECTIVE | FUNCTIONAL SIGNIFICANCE |
| --- | --- |
| .ASCIII | Translates character string to ASCII equivalents. |
| .ASCIZ | Translates character string to ASCII equivalents; inserts zero byte as last character. |
| .ASECT | Begins absolute program section (provided for compatibility with other PDP-11 assemblers). |
| .BLKB | Reserves byte block in accordance with value of specified argument. |
| .BLKW | Reserves word block in accordance with value of specified argument. |
| .BYTE | Generates successive byte data in accordance with specified arguments. |
| .CSECT | Begins relocatable program section (provided for compatibility with other PDP-11 assemblers). |

PERMANENT SYMBOL TABLE (PST)

| DIRECTIVE | FUNCTIONAL SIGNIFICANCE |
| --- | --- |
| .DSABL | Disables specified function. |
| .ENABL | Enables specified function. |
| .END | Defines logical end of source program. |
| .ENDC | Defines end of conditional assembly block. |
| .ENDM | Defines end of macro definition, repeat block, or indefinite repeat block. |
| .ENDR | Defines end of current repeat block (provided for compatibility with other PDP-11 assemblers). |
| .EOT | Define End of Tape condition (ignored). |
| .ERROR | Outputs diagnostic message to listing file or command output device. |
| .EVEN | Word-aligns the current location counter. |

| .GLOBL | Declares global attribute for specified symbol(s). |
| --- | --- |
| .IDENT | Labels object module with specified program version number. |
| .IF | Begins conditional assembly block. |
| .IFF | Begins subconditional assembly block (if conditional assembly block test is false). |
| .IFT | Begins subconditional assembly block (if conditional assembly block test is true). |
| .IFTF | Begins subconditional assembly block (whether conditional assembly block test is true or false). |
| .IIF | Assembles immediate conditional assembly statement (if specified condition is satisfied). |
| .IRP | Begins indefinite repeat block; replaces specified symbol with specified successive real arguments. |
| .IRPC | Begins indefinite repeat block; replaces specified symbol with value of successive characters in specified string. |
| .LIMIT | Reserves two words of storage for high and low addresses of task image. |
| .LIST | Controls listing level count and format of assembly listing. .MACRO Denotes start of macro definition. |
| .MCALL | Identifies required macro definition(s) for assembly. |
| .MEXIT | Exit from current macro definition or indefinite repeat block. |
| .NARG | Equates specified symbol to the number of arguments in the macro expansion. |
| .NCHR | Equates specified symbol to the number of characters in the specified character string. |
| .NLIST | Controls listing level count and suppresses specified portions of the assembly listing. |
| .NTYPE | Equates specified symbols to the addressing mode of the specified argument. |
| .ODD | Byte-aligns the current location counter. |
| .PAGE | Advances form to top of next page. |
| .PRINT | Prints specified message on command output device. |
| .PSECT | Begins specified program section having specified attributes. |
| .RADIX | Changes current program radix to specified radix. |
| .RAD50 | Generates data block having Radix-50 equivalents of specified character string. |
| .REPT | Begins repeat block and replicates it according to the value of the specified expression. |

PERMANENT SYMBOL TABLE (PST)

| DIRECTIVE | FUNCTIONAL SIGNIFICANCE |
| --- | --- |
| .SBTTL. TITLE.WORD | Prints specified subtitle text as the second line of the assembly listing page header.Prints specified title text as object module name in the first line of the assembly listing page header.Generates successive word data in accordance with specified arguments. |

The MACRO-11 directives listed above are summarized in greater detail in Appendix B.

## APPENDIX D DIAGNOSTIC ERROR MESSAGE SUMMARY

### D.1 MACRO-11 ERROR CODES

A diagnostic error code is printed as the first character in a source line which contains an error detected by MACRO-11. This error code identifies a syntactical problem or some other type of error condition detected during the processing of a source line. An example of such a source line is shown below:

Q 26 000236 010102 MOV R1,R2,A

The extraneous argument A in the MOV instruction above causes the line to be flagged with a Q (syntax) error.

| Error Code | Meaning |
| --- | --- |
| A | Assembly error. Because many different types of error conditions produce this diagnostic message, all the possible directives which may yield a general assembly error have been categorized below to reflect specific classes of error conditions:CATEGORY 1: ILLEGAL ARGUMENT SPECIFIED.RADIX -- A value other than 2, 8, or 10 is specified as a new radix.LIST/.NLIST -- Other than a legally defined argument (see Table 6-1) is specified with the directive.ENABL/.DSABL -- Other than a legally defined argument (see Table 6-2) is specified with the directive.PSECT -- Other than a legally-defined argument (see Table 6-3) is specified with the directive.IF/.IIF -- Other than a legally defined conditional test (see Table 6-5) or an illegal argument expression value is specified with the directive.MACRO -- An illegal or duplicate symbol found in dummy argument list. |

DIAGNOSTIC ERROR MESSAGE SUMMARY

| Error Code | Meaning |
| --- | --- |
| P | Phase error. A label's definition of value varies from one assembly pass to another or a multiple definition of a local symbol has occurred within a local symbol block. Also, when in a local symbol block defined by the .ENABL LSB directive, an attempt has occurred to define a local symbol in a program section other than that which was in effect when the block was entered. A P error code also appears if an .ERROR directive is assembled. |
| Q | Questionable syntax. Arguments are missing, too many arguments are specified, or the instruction scan was not completed. |
| R | Register-type error. An invalid use of or reference to a register has been made, or an attempt has been made to redefine a standard register symbol without first issuing the .DSABL REG directive. |
| T | Truncation error. A number generated more than 16 bits in a word, or an expression generated more than 8 significant bits during the use of the .BYTE directive or trap (EMT or TRAP) instruction. |
| U | Undefined symbol. An undefined symbol was encountered during the evaluation of an expression; such an undefined symbol is assigned a value of zero. Other possible conditions which result in this error code include unsatisfied macro names in the list of .MCALL arguments and a direct assignment (symbol=expression) statement which contains a forward reference to a symbol whose definition also contains a forward reference; also, a local symbol may have been referenced that does not exist in the current local symbol block. |
| Z | Instruction error. The instruction so flagged is not compatible among all members of the PDP-11 family. See Section 5.3 for details. |

---

### D.1 supplement — error codes lost in OCR

The OCR conversion dropped several rows of the error-code table (and most of the A-error category list). The full standard MACRO-11 single-letter error set is listed here for completeness (wording paraphrased, not quoted from the manual):

| Code | Meaning |
| --- | --- |
| A | Assembly error — illegal argument to a directive, bad relocation, branch out of range, etc. (see category text above) |
| B | Bounding error — instruction or word data at an odd address; location counter is bumped to even |
| D | Doubly-defined symbol referenced |
| E | End-of-source reached without .END; .END assumed |
| I | Illegal character in source |
| L | Line too long (input line > 132 characters) |
| M | Multiple definition of a label (first six characters collide) |
| N | Number contains 8 or 9 without a trailing decimal point |
| O | Op-code error — directive out of context (e.g. .ENDC/.ENDM without opener), nesting too deep |
| P | Phase error (see above) |
| Q | Questionable syntax (see above) |
| R | Register-type error (see above) |
| T | Truncation (see above) |
| U | Undefined symbol (see above) |
| Z | Instruction not compatible across all PDP-11 models |
