# RT-11 System Utilities Manual: Ch.23 SLP source language patch program (command file syntax)

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 23.1 Calling and Terminating SLP
- 23.2 SLP Command String Syntax
- 23.3 Options
- 21.4 Example
- 23.5 Creating and Maintaining a Command File
- 23.5.1 Update Line Format
- 23.5.2 Creating a Numbered Listing
- 23.5.3 Adding Lines to a File
- 23.5.4 Deleting Lines in a File
- 23.5.5 Replacing Lines in a File
- 23.5.6 Determining and Validating the Contents of a File

---

# Chapter 23 Source Language Patch Program (SLP)

The source language patch program (SLP), is a patching tool you can use for maintaining source files that exist on any RT-11 device.

SLP accepts as input a source file you wish to patch and a command file that you create when you compare two source programs using the source compare program, SRCCOM, described in Chapter 15. When you use SLP along with the SRCCOM command file, you can quickly and easily patch one version of a source program to match another version.

Chapter 15, Source Compare Program (SRCCOM), describes the procedure you can use to create a patch command file that is suitable for input to SLP.

## 23.1 Calling and Terminating SLP

To call SLP from the system device, type the following in response to the keyboard monitor dot (.):

•R SLPRET

The Command String Interpreter (CSI) prints an asterisk (\*) at the left margin of the terminal and waits for a command string. If you enter only a carriage return in response to the asterisk, SLP prints its current version number. You can type CTRL/C to halt SLP and return control to the monitor when SLP is waiting for input from the console terminal. To restart SLP, type R SLP or REENTER in response to the monitor's dot.

## 23.2 SLP Command String Syntax

Chapter 1, Command String Interpreter, describes the general syntax of the command line that SLP accepts.

Enter a command line according to this general syntax:

$$
[ \text {outfil} ] [, \text {listfil} ] = \text {infil,comfil / [option...]}
$$

where:

outfil represents the updated source file. The default file type is .MAC.

listfil represents the listing file. When you specify this file, SLP creates a numbered listing of the updates SLP made to the source file. The default file type is .LST.

infil represents the source file you want SLP to update. The default file type is .MAC.

comfil represents the command file that contains the commands for updating the source file. The default file type is .MAC. You can create this file by specifying a SLP-filespec in a SRCCOM command line. A SLP input file created by SRCCOM has the file type .SLP.

/option represents one of the options listed in Table 23-1.

Although either output files can be omitted, you must use one or both.

## 23.3 Options

Table 23-1 lists the options you can use in the command line.

## 21.4 Example

This section uses SLP to patch the source file, ANTONY.MAC, so that it matches the source file CAESAR.MAC. CAESAR.MAC consists of the following lines.

```txt
FRIENDS, ROMANS, COUNTRYMEN!
LEND ME YOUR EARS!
I COME TO BURY CAESAR,
NOT TO PRAISE HIM.
THE EVIL THAT MEN DO
LIVES AFTER THEM.
THE GOOD IS OFT INTERRED
WITH THEIR BONES;
SO LET IT BE WITH CAESAR!
```

The file this example will patch, ANTONY.MAC, follows.

```csv
FRIENDS, ROMANS, COUNTRYMEN!
LEN ME YOUR EARS!
I COME TO BURY CAESAR,
NOT TO PRAISE HIM.
THE EVIL THAT MAN DO
LIVES AFTER THEM.
THE GOOD IS OFT ENTERED
WIT THEIR HOMES;
SO LET IT BE WITH CAESAR!
```

Table 23-1: SLP Options

| Option | Function |
| --- | --- |
| /A | Disables audit trail generation. The audit trail is a string of characters that SLP appends to the end of each updated line in the output files. The audit trail keeps track of the update status of each line in the output file. You can use the /A option if you do not want SLP to use the audit trail in both the updated source file and the listing file. |
| /B | Inserts spaces instead of tabs between the source line and the audit trail. |
| /C[:n] | Determines or validates the contents of the SLP input file, SLP command file, or both by using checksums. Use /C to determine the checksum of a file. Use /C:n to verify the contents of a file. SLP computes the checksum for the file, and compares the result to the value you specify with n. |
| /D | Creates a double-spaced listing. When you use this option, SLP double-spaces between the lines in a listing file. |
| /L:n | Specifies the size of the source line, where n represents the maximum number of characters you want in the source line. The default buffer size for formatting lines is 200(decimal) bytes. If you expect the size of the command lines or source lines to be greater than what can fit in the line buffer, you can use this option to change the buffer size. SLP interprets the number you specify for n as an octal number; if you enter a decimal number, use a decimal point. The line buffer must be at least as long as the sum of the column number where the audit trail begins and the number of characters in the audit trail. |
| /N | Suppresses the creation of a backup file when SLP updates the input file. |
| /P:n | Specifies the start column of the audit trail, where n represents the column number in which you want the audit trail to start. If the number you specify for n is decimal, be sure to use a decimal point after the number. By default, SLP starts the audit trail in column 73 (decimal). If a source line extends beyond the column where the audit trail begins, the audit trail can overstrike the source line. If you use the /P:n option, you start the audit trail in any tab stop column. SLP rounds up the number you specify to the nearest tab stop column. If, for example, you specify 46 for n, SLP rounds this number to 49. |
| /S:n | Specifies size of the audit trail, where n represents the number of characters you want in the audit trail. If the number you specify is decimal, be sure to use a decimal point after the number. The default number of characters in the audit trail is 12(decimal). The maximum number of characters you can specify for the audit trail is 16(decimal). |
| /T | Retains trailing blanks and tabs in the input source file. By default, SLP removes spaces and tabs that appear at the end of lines in the input source file. |

By specifying a SLP-filespec in a SRCCOM command line, this example obtains a command file, CAESAR.SLP. CAESAR.SLP contains the necessary commands to make ANTONY.MAC match CAESAR.MAC. The following command line directs SLP to patch ANTONY.MAC so that it matches CAESAR.MAC.

• R SLP

\* ANTONY, ANTONY = ANTONY, CAESAR, SLP

After executing the command above, SLP assigns a .BAK file type to the input file ANTONY.MAC. It assigns .MAC file type to the updated source file. SLP has also created a listing of ANTONY.MAC that lists each line by number and appends an audit trail to each new line. The updated file, ANTONY.MAC, is now identical to CAESAR.MAC. ANTONY.LST appears below.

ANTONY, ANTONY = ANTONY, MAC, CAESAR, SLP

```csv
V05.00 ANTONY,ANTONY=ANTONY.MAC:
1. FRIENDS, ROMANS, COUNTRYMEN! ;**NEW**
2. LEND ME YOUR EARS! ;**-1
3. I COME TO BURY CAESAR,
4. NOT TO PRAISE HIM. ;**NEW**
5. THE EVIL THAT MEN DO ;**-1
6. LIVES AFTER THEM. ;**NEW**
7. THE GOOD IS OFT INTERRED ;**NEW**
8. WITH THEIR BONES; ;**-2
9. SO LET IT BE WITH CAESAR!
```

Note that when SLP updates a line, it appends an additional audit trail below the audit trail of the updated line. The additional audit trail keeps track of the number of consecutive lines that have been updated. In ANTONY.LST, above, note the audit trails;\*\*-1 and;\*\*-2.

## 23.5 Creating and Maintaining a Command File

SLP is a line-oriented patching tool. That is, you make changes to entire lines, and not to individual characters or strings of characters within a line. If you want to change only a few characters within a line, it will be necessary for you to enter a new line.

Although DIGITAL recommends that you create the SLP input command file by specifying a SLP-filespec in a SRCCOM command line, you can use any RT-11 editor to create it yourself. The section that follows describes the commands, or operators, you use to create the command file. This procedure is tedious, however, and in most cases unnecessary. But for completeness, this procedure is included with this chapter. Table 23–2 lists the commands, or operators, you enter into the command file.

The section ends with a description of various line manipulations that SLP can effect.

## 23.5.1 Update Line Format

The general format of the SLP command file update line follows.

-locator1,[locator2],[/audit trail/][;]
inputline

Table 23-2: SLP Command File Operators

<table><tr><td>Operator</td><td>Function</td></tr><tr><td></td><td>Indicates the start of an update. SLP ignores any data that precedes this operator in a SLP command file. If SLP finds characters before this operator in a command file, SLP prints a warning and the characters are ignored. If no operator of this type is found in a command file, SLP prints an error message and the CSI prompt (*) appears.</td></tr><tr><td>\</td><td>Disables the audit trail. Note that this operator must appear on a line by itself. If it appears in the first column of a line with additional information following it, the audit trail will be disabled, but the rest of the command line will be ignored. If used in any column other than column one, a syntax error occurs.</td></tr><tr><td>%</td><td>Enables the audit trail.</td></tr><tr><td>/</td><td>Indicates the end of an update or a series of updates; it appears as the last character in the command file.</td></tr><tr><td>//</td><td>Indicates the end of one of a series of update texts in a single command file; each text updates one input file. This operator is used when you want to include updates for more than one file in a single command file. Type the double slash (//) on a line by itself after each update text in the series. Then type on the next line the command line that specifies the next input file to be updated, and on the succeeding lines the update text for that file. Note that the command file specified in each command line must be the same as the command file specified on the first command line.</td></tr><tr><td>&lt;</td><td>Serves as an escape character for characters SLP would otherwise interpret as operators. For example, if you want to include a slash (/) in a source file, type the less-than character (&lt;) before the slash. Then, SLP will not interpret the slash as an operator. You can use the less-than character as an escape character for all SLP command file operators.</td></tr><tr><td colspan="2">where:</td></tr><tr><td>-</td><td>indicates that this is an update line.</td></tr><tr><td>locator1</td><td>represents a character string that serves as a line locator.SLP moves the line pointer to the line specified by the line locator. You can specify this line locator with any of the locator forms described below.</td></tr><tr><td>locator2</td><td>represents a character string that, when used with locator1, defines the end of a range of lines you want to delete or replace. You can specify this line locator with any of the locator forms described below. You cannot define a range of lines in a backwards direction; the line referenced by locator2 must occur in the source file after the line referenced by locator1.</td></tr><tr><td>/audit trail/</td><td>represents a character string you use as an audit trail.SLP appends the audit trail to the right of each updated line. You must delimit the audit trail with slashes (/).</td></tr></table>

inputline represents a line of new text that SLP inserts into the file immediately following the current line. You can enter as many input lines as you want.

```txt
; is an optional command line terminator.
```

All fields in the update line are positional. That is, if you specify only locator1 and an audit trail, you must use two commas between those two fields. If you want to specify only the audit trail, you must precede the audit trail with two commas.

The update lines in a command file must edit the source file in a forwards direction, from beginning to end. Each locator1 must point to a line that appears in the source file before the lines pointed to by any succeeding locator1.

The line locators can take one of the following forms:

```txt
/string/[(+n]
/string...string/[(+n]
number[+n]
.+n
```

where:

/string/[( + n] represents an ASCII character string. You must delimit any string you enter with slashes. SLP locates the first occurrence of this string, and moves the line pointer to the line that contains that string. + n represents the offset from the line that contains the string. You must use the plus character (+) with the n notation.

/string...string/[( + n] represents an ASCII character string. SLP locates the line in which the two strings delimit a larger string. Use the ellipsis (...) in this locator form to separate the two strings. +n represents the offset from the line specified by the string...string locator.

number[ + n] represents the line number to which SLP is to move the line pointer. +n represents the offset from the line specified by number.

.+ n represents the offset from the current line pointer. SLP interprets the period (.) as the current line pointer location, and the +n as the offset from it. You must use the plus character (+).

## 23.5.2 Creating a Numbered Listing

You can use SLP to create a numbered listing of the input source file. In creating a command file, you should use a numbered listing when you prepare command input. To generate a numbered listing, enter the following lines:

```txt
• R SLP
* ,listfile=infile
```

```json
-.[ + n],,[/audittrail/]
```

Listfile represents the listing file SLP produces, and infile represents the input source file. Here is a file, PROG.MAC, from which SLP is to create a numbered listing:

```asm
.TITLE  PROG.MAC     VERSION 1
        .MCALL   .TTYOUT, .EXIT, .PRINT

EXP:      .PRINT    #MESSAGE
        MOV         #N,R5
FIRST:   MOV         #N+1,RO
        MOV         #A,R1
```

The following command line creates a numbered listing, PROG.LST of the file above, PROG.MAC:

```txt
*,PROG=PROG
```

After SLP processes the command above, it produces the following listing of PROG.MAC:

```asm
SLP    V05.00
,PROG=PROG.MAC

1.                      .TITLE  PROG.MAC     VERSION 1
2.
3.                      .MCALL   .TTYOUT, .EXIT, .PRINT
4.
5.      EXP:     .PRINT  #MESSAGE
6.                      MOV     #N,R5
7.      FIRST:   MOV     #N+1,RO
8.                      MOV     #A,R1
```

## 23.5.3 Adding Lines to a File

To add lines to a file, enter in the command file one of the three locator forms below:

-number

Notice in the second locator form the two commas between the locator and the audit trail. You do not have to insert these commas if you are not specifying an audit trail.

Below is a file, NUMBER.PAS, to which SLP is to add new lines.

```txt
PROGRAM NUMBER;

TYPE     TEXT      =FILE OF CHAR;
        PTR       =^WORDNODE;
        WORDNODE=RECORD
                WORD:ARRAY[1.,30] OF CHAR;
                NEXT:PTR;
                END;

VAR     P,TOP    :PTR;
        INTEXT   :TEXT;
        I          :INTEGER;
```

SLP is to insert the following line between the fourth and fifth lines of NUMBER.PAS.

The command file, OMEGA.MAC, contains the following update 1 to perform this procedure.

```txt
- / PTR /
(*POINTER TO NODE*)
/
```

When SLP processes OMEGA.MAC with NUMBER.PAS, it produces the following updated listing file.

```txt
SLP V05.00 NUMBER.PAS,NUMBER=NUMBER.PAS,OMEGA.MAC
PROGRAM NUMBER;
TYPE TEXT =FILE OF CHAR;
PTR =^WORDNODE;
(*POINTER TO NODE*) ;**NEW**
WORDNODE=RECORD
WORD:ARRAY[1..30] OF CHAR;
NEXT:PTR;
END;
VAR P,TOP :PTR;
INTEXT :TEXT;
I :INTEGER;
```

SLP has numbered the lines, inserted the new text, and appended the default audit trail ( $;^{**}NEW^{**}$ ) to the new line.

The next example uses the same source file, but uses this command in the command file, SIGMA.MAC:

```txt
- /WORDNODE = / + 2
ID : INTEGER;
/
```

When SLP processes SIGMA.MAC with the source file NUMBER.PAS, it generates the following listing file:

```txt
SLP V05.00 NUMBER.PAS,NUMBER=NUMBER.PAS,SIGMA.MAC
PROGRAM NUMBER;
TYPE TEXT =FILE OF CHAR;
PTR =^WORDNODE;
WORDNODE=RECORD
WORD:ARRAY[1..30] OF CHAR;
NEXT:PTR;
ID :INTEGER;
END; ;**NEW**
VAR P,TOP :PTR;
INTEXT :TEXT;
I :INTEGER;
```

Again, SLP has numbered the lines, and this time it skips two lines after the first occurrence of string WORDNODE before inserting the new input line.

You can include in one command file update text for several input files. Type a double slash (//) on a line by itself at the end of the update text for each file. Begin the update text for the next file with a line containing only the command line that specifies the input file to be updated by the next text. Then type the update text on the lines that follow the command line. Type a slash (/) at the end of the command file.

For example, the command file MTST.MAC contains update text to patch the files NUMBER.PAS and GTMSG.MAC, in that order.

```txt
- /WORDNODE = / + 2
        ID    : INTEGER;
// 
DYO: NEWMSG = GTMSG, MAC, MTST, MAC
-2, 2
      , IDENT     /01, 01/
-7
      ADD       A, B
-14
B:   , WORD     0
/
```

## 23.5.4 Deleting Lines in a File

The SLP command file command syntax for deleting lines from a file is:

-locator1,locator2,[/audittrail/][;]

where locator1 and locator2 can be any of the forms of the locator fields described earlier. locator1 specifies the line where SLP is to begin deleting lines. locator2 specifies the last line SLP is to delete.

If you want to delete lines five through eight in file NUMBER.PAS, it will be helpful to look at a numbered listing of NUMBER.PAS.

```txt
SLP  V05,00
,NUMBER=NUMBER,PAS

1. PROGRAM NUMBER;
2.
3. TYPE TEXT =FILE OF CHAR;
4. PTR =^WORDNODE;
5. WORDNODE=RECORD
6. WORD:ARRAY[1..30] OF CHAR;
7. NEXT:PTR;
8. END;
9.
10. VAR P,TOP :PTR;
11. INTEXT :TEXT;
12. I :INTEGER;
```

In the command file, GAMMA.MAC, the command for deleting lines five through eight follows.

```txt
- /WORDNODE = / , /END /
/
```

When SLP processes GAMMA.MAC with NUMBER.PAS, it produces this listing file of NUMBER.PAS.

```txt
SLP  V05.00
NUMBER, PAS, NUMBER=NUMBER, PAS, GAMMA, MAC
PROGRAM NUMBER;
TYPE
    TEXT
    =FILE OF CHAR;
    PTR
    =^WORDNODE;
VAR
    P,TOP
    :PTR;
    INTEXT
    :TEXT;
    I
    :INTEGER;
```

## 23.5.5 Replacing Lines in a File

When you replace lines, you delete and then add new text. To replace lines in a file, first enter the full SLP edit command for the delete operation. The first line locator specifies the first line to be deleted. The second line locator specifies both the last line to be deleted and the location where SLP is to insert new text. For example, the command file command instructs SLP to move the line pointer to line 4.

```txt
-4, +4
```

Then, SLP is to delete the next four lines (represented by +4), including line 4. Finally, SLP is to insert input lines that follow in the command file. SLP inserts the new lines, beginning at the line pointer's current location.

The following example illustrates replacing lines in a file. The source file, BETA.MAC, consists of the following lines:

```csv
,TITLE BETA,MAC
,MCALL ,TTYOUT, ,PRINT, ,EXIT
START: ,PRINT #MESSAG
MOV #5,RO
```

The command file, DELTA.MAC, contains:

```csv
-6,6, /; AUDIT TRAIL/
BNE START:
MOVB (R2), -(R3)
/
```

When SLP processes DELTA.MAC with BETA.MAC, it produces the following listing file:

```asm
SLP  V05.00    BETA,BETA=BETA,DELTA.MAC
1.          .TITLE   BETA.MAC
2.          .
3.          .MCALL   .TTYOUT, .PRINT, .EXIT
4.          .
5. START:   .PRINT #MESSAGE
6.          BNE     START:                  ;AUDIT TRAIL
7.          MOVB      (R2),-(R3)               ;AUDIT TRAIL
```

## 23.5.6 Determining and Validating the Contents of a File

Use the checksum option (/C[:n]) to determine or validate the contents of a file. The checksum option directs SLP to compute the sum of all ASCII data in a file. If you specify the command in the form /C:n, /C directs SLP to compute the checksum and compare that checksum to the value you specify as n.

To determine the checksum of a file, enter the SLP command line with the /C option applied to the appropriate file (the file whose checksum you want to determine). For example, SLP responds to the command

INFILE, INFILE=INFILE, MAC/C, INFILE, SLP

with the message

```txt
?SLP-I-DEV:FILNAM,TYP checksum is n
```

SLP generates a similar message when you request the checksum for the command file.

To validate the changes made to a file, enter the checksum option in the form /C:n. SLP compares the value it computes for the checksum with the value you specify as n. If the two values do not match, SLP enters no changes and displays a message reporting the checksum error as either a source file or a correction file checksum error, whichever is appropriate.

```txt
?SLP-F-Source file checksum error
```

or

?SLP-F-Correction file checksum error

Checksum processing always results in a nonzero value.

Do not confuse this checksum with the record checksum byte.

(1)
