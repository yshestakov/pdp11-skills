# RT-11 System Utilities Manual: App.A BATCH: batch control language, $JOB/$MACRO/$LINK/$RUN..., BATCH compiler/run-time handler

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- A.1 Hardware and Software Requirements
- A.2 Control Statement Format
- A.3 General Rules and Conventions
- A.4 Commands
- A.5 RT-11 MODE
- A.6 Creating BATCH Programs on Punched Cards
- A.7 Operating Procedures
- A.8 Differences Between RT-11 BATCH and RSX-11D BATCH

---

## Appendix A BATCH

RT-11 BATCH is a complete job control language that allows RT-11 to operate unattended. BATCH processing is ideally suited to frequently run production jobs, large and long-running programs, and programs that require little or no interaction with you, the user. With BATCH, you can prepare your job on any RT-11 input device and leave it for the operator to start and run.

RT-11 BATCH permits you to:

\- Execute an RT-11 BATCH stream from any RT-11 input device

\- Output a log file to any RT-11 output device (except magtape or cassette)

\- Execute the BATCH stream with the SJ monitor or in the background with the FB monitor or XM monitor

\- Generate and support system-independent BATCH language jobs

\- Execute RT-11 monitor commands from the BATCH stream

RT-11 BATCH consists of the BATCH compiler and the BATCH run-time handler. The BATCH compiler reads the batch input stream you create, translates it into a format suitable for the RT-11 BATCH run-time handler, and stores it in a file. The BATCH run-time handler executes this file with the RT-11 monitor. As each command in the batch stream executes, BATCH lists the command, along with any terminal output generated, by executing the command on the BATCH log device.

## A.1 Hardware and Software Requirements

You can run RT-11 BATCH on any single-job foreground/background or extended memory system that is configured with at least 16K words of memory. A line printer, although optional, is highly desirable as the log device.

BATCH uses certain RT-11 system programs to perform its operations. For example, the \$BASIC command executes the file BASIC.SAV. Make sure that the following RT-11 programs are on the system device, with exactly the following names, before you run BATCH:

BASIC.SAV (BASIC users only)

SYSLIB.OBJ (FORTRAN and MACRO users)

## A.2 Control Statement Format

For input to RT-11 BATCH, you can generate a file with the RT-11 editor and use any RT-11 input device, or you can use punched cards from the card reader. In both cases, the input consists of BATCH control statements. A BATCH control statement is divided into three fields, separated from one another by spaces: command fields, specification fields, and comment fields. The control statement has the syntax:

\$command/option specification/option [!comment]

Each control statement requires a specific combination of command and specification fields and options (see Section A.4). Control statements cannot be longer than 80 characters, excluding multiple spaces, tabs, and comments. You can use a hyphen (-) as a line continuation character to indicate that the control statement is continued on the next line (see Table A-4). Even if you use the line continuation character, the maximum control statement length is still 80 characters.

The following example of a \$FORTRAN command illustrates the various fields in a control statement.

\$FORTRAN/LIST/RUN PROGA/LIBRARY PROGB/EXE !RUN FORTRAN

command/options     spec fields/options     comment field

## A.2.1 Command Fields

The command field in a BATCH control statement indicates the operation to be performed. It consists of a command name and certain command field options. Indicate the command field with a \$ in the first character position and terminate it with a space, tab, blank, or carriage return.

A.2.1.1 Command Names – The command name must appear first in a BATCH control statement and have a dollar sign (\$) in the first position of the command (for example, \$JOB). No intervening spaces are allowed in the command name. BATCH recognizes only two forms of a command name: the full name, and an abbreviation consisting of \$ and the first three characters of the command name. For example, you can enter the \$FORTRAN command as:

\$FORTRAN

or

\$FOR

You cannot enter it as:

\$FORT

or

\$FORTR

A.2.1.2 Command Field Options – Options that appear in a command field are command qualifiers. Their functions apply to the entire control statement. All option names must begin with a slash (/) that immediately follows the command name. Table A-1 describes the command field options for BATCH and indicates the commands on which you can use them. Those option characters that appear in square brackets are optional. The command field options are described in greater detail in the sections dealing with the appropriate commands.

## NOTE

All /NO options are the defaults, except the /WAIT option in the \$MOUNT and \$DISMOUNT commands and the /OBJECT option in the \$LINK command.

## A.2.2 Specification Fields

Specification fields immediately follow command fields in a BATCH control statement and apply only to the fields they follow. Use them to name the devices and files involved in the command. You must separate these fields from the command field, and from each other, by blanks or spaces.

If a specification field contains more than one file to be used in the same operation, separate the files by a plus (+) sign. For example, to assemble files F1 and F2 to produce an object file F3 and a temporary listing file, type:

\$MACRO/LIST F1+F2/SOURCE F3/OBJECT

Table A-1: Command Field Options

| Option | Function |
| --- | --- |
| /BAN[NER] | Prints the header of the job on the log file. BATCH allows this option only on the $JOB command. Note that BATCH outputs the $JOB command line to the log device sixty times. |
| /NOBAN[NER] | Does not print a job header. |
| /CRE[F] | Produces a cross-reference listing during compilation. BATCH allows this option only on the $MACRO command. |
| /NOCRE[F] | Does not create a cross-reference listing. |
| /DEL[ETE] | Deletes input files after the operation completes. BATCH allows this option on the $COPY and $PRINT commands. |
| /NODEL[ETE] | Does not delete input files after operation completes. |
| /DOL[LARS] | The data following this command can have a $ in the first character position of a line. BATCH allows this option on the $CREATE, $DATA, $FORTRAN, and $MACRO commands. BATCH terminates reading data when you use one of the following commands or when it encounters a physical end-of-file on the BATCH input stream: |
|  | $ JOB $EOD$SEQUENCE $EOJ |
| /NODOL[LARS] | The data following this command cannot have a $ in the first character position; a $ in the first character position means a BATCH control command. |
| /LIB[RARY] | Includes the default library in the link operation. BATCH allows this option on the $LINK and $MACRO commands. |
| /NOLIB[RARY] | Does not include the default library in the link operation. |
| /LIS[T] | Produces a temporary listing file (see Section A.2.5) on the listing device (LST:) or writes data images on the log device (LOG:). BATCH allows this option on the $BASIC, $CREATE, $DATA, $FORTRAN, $JOB, and $MACRO commands. When you use /LIST on the $JOB command, /LIST sends data lines in the job stream to the log device (LOG:). |
| /NOLIS[T] | Does not produce a temporary listing file. |
| /MAP | Produces a temporary link map on the listing device (LST:). BATCH allows this option on the $FORTRAN, $LINK, and $MACRO commands. |
| /NOMAP | Does not create a MAP file. |
| /OBJ[ECT] | Produces a temporary object file as output from compilation or assembly (see Section A.2.5). BATCH allows this option on the $FORTRAN, $LINK, and $MACRO commands. When you use /OBJECT on $LINK, BATCH includes temporary files in the link operation. |

\$MACRO/LIST F1/SOURCE F2/OBJECT F3/MAP,F4+F5/SOURCE-F6/OBJECT

Table A-1: Command Field Options (Cont.)

| Option | Function |
| --- | --- |
| /NOOBJ[ECT] | Does not produce an object file as output of compilation; with $LINK, does not include temporary files in the link operation. |
| /RT11 | Sets BATCH to operate in RT-11 mode (see Section A.5). BATCH allows this option only on the $JOB command. |
| /NORT11 | Does not set BATCH to operate in RT-11 mode. |
| /RUN | Links (if necessary) and executes programs compiled since the last link-and-go operation or start of job. BATCH allows this option on the $BASIC, $FORTRAN, $LINK, and $MACRO commands. |
| /NORUN | Does not execute or link and execute the program after performing the specified command. |
| /TIM[E] | Writes the time of day to the log file when BATCH executes. BATCH allows this option only on the $JOB command. This command writes the time after each command that begins with a dollar sign ($). |
| /NOTIM[E] | Does not write the time of day to the log file. |
| /UNI[QUE] | Checks for unique spelling of options and keynames (see Section A.4.13). BATCH allows this option only on the $JOB command. |
| /NOUNI[QUE] | Does not check for unique spelling. |
| /WAI[T] | Pauses for operator action. BATCH allows this option on the $DISMOUNT, $MESSAGE, and $MOUNT commands. |
| /NOWAI[T] | Does not pause for operator action. |
| /WRI[TE] | Indicates that the operator is to WRITE-ENABLE a specified device or volume. BATCH allows this option only on the $MOUNT command. |
| /NOWRI[TE] | Indicates that no writes are allowed or that the specified volume is read-only; informs the operator, who must WRITE-LOCK the appropriate device. |

If you need to repeat a command for more than one field specification, separate the files by a comma (),. For example, the following command assembles F1 to produce F2, a temporary listing file, and a map file F3. It then assembles F4 and F5 to produce F6 and a temporary listing file.

Depending on the command you use, specification fields can contain a device specification, file specification, or an arbitrary ASCII string. You can use an appropriate specification field option (see Table A-3) with any of these three items.

[figure omitted]

A.2.2.1 Physical Device Names — Represent each device in an RT-11 BATCH specification field with a standard two- or three-character device name. Table 3-1 in Chapter 3 of the RT-11 System User's Guide lists each name and its related device. If you do not specify a unit number for devices that have more than one unit, BATCH assumes unit 0.

In addition to the permanent names shown in Table 3-1, you can assign logical device names to devices. A logical device name takes precedence over a physical name, thus providing device independence. With this feature, you do not need to rewrite a program that is coded to use a specific device if the device is unavailable. For example, DK: is initially assigned to the system device, but you can assign that name to diskette unit 1 (DX1:) with an RT-11 monitor ASSIGN command.

You must assign certain logical names prior to running any BATCH job. BATCH uses these logical names as default devices. These names are:

LOG: BATCH log device (cannot be magtape or cassette)
LST: Default for listing files generated by BATCH stream

The following are not legal device names in RT-11; if you use them, the operator must assign them as logical names with the ASSIGN command. You can use these names in BATCH streams written for other DIGITAL systems.

DF: Fixed-head disk (RF)

LL: Line printer with uppercase and lowercase characters

M7: 7-track magtape

M9: 9-track magtape

PS: Public storage (DK: as assigned by RT-11)

Refer to the ASSIGN keyboard command in the RT-11 System User's Guide and Section A.7.1 in this manual for instructions on assigning logical names to devices.

A.2.2.2 File Specifications — You can reference files symbolically in a BATCH control statement with a name of up to six alphanumeric characters followed, optionally, by a period and a file type of three alphanumeric characters. Tabs and embedded spaces are not allowed in either the file name or file type. The file type generally indicates the format of a file. It is good practice to conform to the standard file types for RT-11 BATCH. If you do not specify a file type for an output file, BATCH and most other RT-11 system programs assign appropriate default file types. If you do not specify a file type for an input file, the system searches for that file name with a default file type. Table A-2 lists the standard file types used in RT-11 BATCH.

A.2.2.3 Wildcard Construction – You may use wildcards in certain BATCH control statements (such as, \$COPY, \$CREATE, \$DELETE, \$DIRECTORY, \$PRINT). You can use the asterisk as a wildcard to designate the entire file name or file type. See Chapter 4 of the RT-11 System User's Guide for a complete description of the wildcard construction.

Table A-2: BATCH File Types

| File Type | Explanation |
| --- | --- |
| .BAS | BASIC source file (BASIC input) |
| .BAT | BATCH command file |
| .CTL | BATCH control file generated by the BATCH compiler |
| .CTT | BATCH temporary file generated by the BATCH compiler |
| .DAT | BASIC or FORTRAN data file |
| .DIR | Directory listing file |
| .FOR | FORTRAN IV source file (FORTRAN input) |
| .LST | Listing file |
| .LOG | BATCH log file |
| .MAC | MACRO source file (MACRO or SRCCOM input) |
| .MAP | Link map output from $LINK operation |
| .OBJ | Object file output from compilation or assembly |
| .SOU | Temporary source file |
| .SAV | Runnable file or program image output from $LINK |

## NOTE

You cannot use embedded wild cards (\* or %) in BATCH control statements. However, you can use them in the keyboard monitor commands if you use the RT-11 mode of BATCH.

A.2.2.4 Specification Field Options – Specification field options follow file specifications in a BATCH control statement and designate how the file will be used. These options apply only to the field in which they appear. Option names begin with a slash. The specification field options for RT-11 BATCH are listed in Table A-3. Optional characters in the option names are in square brackets.

## A.2.3 Comment Fields

Comment fields, which document a BATCH stream, are identified by an exclamation point (!) appearing anywhere except in the first character position of the control statement. BATCH treats any character following the ! and preceding the carriage return/line feed combination as a comment. For example:

\$RUN PIP !DELETE FILES ON DK:

This command runs the RT-11 system program PIP. BATCH ignores the comment.

Table A-3: Specification Field Options

| Option | Explanation |
| --- | --- |
| /BAS[IC] | BASIC source file |
| /EXE[CUTABLE] | Indicates the executable program image file to be created as the result of a link operation |
| /FOR[TRAN] | FORTRAN source file |
| /INP[UT] | Input file; default if you specify no options |
| /LIB[RARY] | Library file to be included in link operation (prior to default library) |
| /LIS[T] | Listing file |
| /LOG[ICAL] | Indicates that the device is a logical device name; use in $DISMOUNT and $MOUNT commands |
| /MAC[RO] | MACRO source file |
| /MAP | Linker map file |
| /OBJ[ECT] | Object file (output of assembly or compilation) |
| /OUT[PUT] | Output file |
| /PHY[SICAL] | Indicates physical device name |
| /SOU[RCE] | Indicates source file |
| /VID | Volume identification |

You can also include comments as separate comment lines by typing a \$ in character position 1, followed immediately by the ! operator and the comment. For example:

\$!DELETE FILES ON DK:

## A.2.4 BATCH Character Set

The RT-11 BATCH character set is limited to the 64 uppercase characters (ASCII 40 through 137). The current ASCII set is assumed (character 137 is underscore and not left-arrow, and character 136 is circumflex, not up-arrow). The BATCH job control language does not support any control characters other than tab, carriage return, and line feed.

Table A-4 shows how BATCH normally interprets certain characters. Character interpretations are different if you use RT-11 mode (see Section A.5).

Table A-4: Character Explanation

| Character | Explanation |
| --- | --- |
| space | Specification field delimiter. It separates arguments in control statements. BATCH considers any string of consecutive spaces and tabs (except in quoted strings) as a blank (that is, equivalent to a single space). |
| ! | Comment delimiter. The input routine ignores all characters after the exclamation point, up to the carriage return/line-feed combination. |
| " | Passes a text string containing delimiting characters where the normal precedence rules would create the wrong action. For example, use it to include a space in a volume identification (/VID). |
| $ | BATCH control statement recognition character. A dollar sign ($) in the first character position of a BATCH input stream line indicates that the line is a control statement. |
| . | Delimiter for file type. |
| - | Indicates line continuation if the character after the hyphen is one of the following:● A carriage return/line feed● Any number of spaces or tabs followed by a carriage return/line feed● A comment delimiter (!)● Spaces followed by a comment delimiter (!)If any other character follows the hyphen, the hyphen is assumed to be a minus sign indicating a negative value in an option |
| / | Precedes an option name. An alphanumeric string must immediately follow it. |
| 0-9 | Numeric string components. |
| : | Immediately follows a device name. You can also use it to separate an option name from its value or to separate an option value from its sub-value (you can use : interchangeably with = for this purpose). |
| A-Z | Alphabetic string components. |
| = | Separates an option name from a value. |
| \\ | Illegal character except when it precedes a directive to the BATCH run-time handler from the operator (see Section A.7.3): (To include \\ in an RT-11 mode command, use \\ .) |
| + | File delimiter. Separates multiple files in a single specification field. Also indicates a positive value in options. |
| , | Separates sets of arguments for which the command is to be repeated. |
| * | A wildcard in utility command file specifications. |
| CR/LF | Carriage return/line feed. It indicates end-of-line (or end of logical record) for records in the BATCH input stream. |

## A.2.5 Temporary Files

When you do not include field specifications in a BATCH command line, BATCH sometimes generates temporary files. For example, you can enter a \$FORTRAN command that is followed in the BATCH stream by the FORTRAN source program as:

\$FORTRAN/RUN/OBJECT/LIST
FORTRAN source Program
\$EOD

This command generates a temporary source file from the source statements that follow, a temporary object file, a temporary listing file, and a temporary memory image file.

BATCH sends temporary files to the default device (DK:) or the listing device (LST:) according to their type. If the device is file-structured, BATCH assigns file names and file types as follows:

nnnmmm.LST for temporary listing files (sent to LST:)

nnnmmm.MAP for temporary map files (sent to LST:)

nnnppp.OBJ for temporary object files (sent to DK:)

000000.SAV for temporary memory image files (sent to DK:)

nnnppp.SOU for temporary source files (sent to DK:)

## where:

nnn represents the last three digits of the sequence number assigned to the job by the \$SEQUENCE command (see Section A.4.22). Thus, a sequence number of 12345 produces a file name beginning 345. If you do not use the \$SEQUENCE command, BATCH sets nnn to 000.

mmm represents the number of listing (or map) files BATCH generated since the BATCH run-time handler (BA.SYS) was loaded. The first such file, listing or map, is 000. Each time BATCH generates a new temporary file, it increments the file name by 1. Thus, the second listing file produced under job sequence number 12345 is 345001.LST, and the first map file produced is 345000.MAP.

ppp represents the number of object or source files in the current BATCH run. The first such file (object or source) is 000. Each time BATCH generates a new temporary file, it increments the file name by 1. BATCH resets these file names to 000 every time you run BATCH and after every \$LINK, \$MACRO, or \$FORTRAN command that uses the temporary files.

## A.3 General Rules and Conventions

You must adhere to the following general rules and conventions associated with RT-11 BATCH processing.

1. Always place a dollar sign (\$) in the first character position of a command line.

2. Each job must have a \$JOB and \$EOJ command (or card).

3. You can spell out command and option names entirely or you can specify only the first three characters of the command and required characters of the option.

4. Specify wildcard construction (\*) only for the utility commands (\$COPY, \$CREATE, \$DELETE, \$DIRECTORY, and \$PRINT) and for commands that normally accept wildcards in RT–11 mode.

5. Include comments at the end of command lines or in a separate comment line. When you include comments in a command line, place them after the command but precede them by an exclamation mark.

6. Include only 80 characters per control statement (card record), excluding multiple spaces, tabs, and comments.

7. When you omit file specifications from BATCH commands and supply data in the BATCH stream, the system creates a temporary file with a default name (see Section A.2.5).

8. You can use the RT-11 monitor type-ahead feature only with BATCH handler directives (see Section A.7.3) to be inserted into a BATCH program. No other terminal input (except input to a foreground program) can be entered while a BATCH stream is executing.

9. You cannot use an indirect command file to call BATCH.

## A.4 Commands

Place BATCH commands in the input stream to indicate to the system which functions to perform in the job. All BATCH commands have a dollar sign (\$) in the first character position (for example, \$JOB). Intervening spaces are not allowed in command names. The command name must always start in the first character position of the line (card column 1).

BATCH commands are presented in alphabetical order in this chapter for ease of reference. However, if you are not familiar with BATCH, read the commands in a functional order as listed in Table A–5. The characters shown in square brackets are optional.

Table A-5: BATCH Commands

| Command | Section | Function |
| --- | --- | --- |
| $SEQ[UENCE] | A.4.22 | Assigns an arbitrary identification number to a job. |
| $JOB | A.4.13 | Indicates the start of a job. |
| $EOJ | A.4.11 | Indicates the end of a job. |
| $MOU[NT] | A.4.18 | Signals the operator to mount a volume on a device and optionally assigns a logical device name. |
| $DIS[MOUNT] | A.4.9 | Signals the operator to dismount a volume from a device and deassigns a logical device name. |
| $FOR[TRAN] | A.4.12 | Compiles a FORTRAN source program. |
| $BAS[IC] | A.4.1 | Compiles a BASIC source program. |
| $MAC[RO] | A.4.16 | Assembles a MACRO source program. |
| $LIB[RARY] | A.4.14 | Specifies libraries for BATCH to use in link operations. |
| $LIN[K] | A.4.15 | Links modules for execution. |
| $RUN | A.4.21 | Causes a program to execute. |
| $CAL[L] | A.4.2 | Transfers control to another BATCH file, executes that BATCH file, and returns to the calling BATCH stream. |
| $CHA[IN] | A.4.3 | Passes control to another BATCH file. |
| $DAT[A] | A.4.6 | Indicates the start of data. |
| $EOD | A.4.10 | Indicates the end of data. |
| $MES[SAGE] | A.4.17 | Issues a message to the operator. |
| $COP[Y] | A.4.4 | Copies files. |
| $CRE[ATE] | A.4.5 | Creates new files from data included in the BATCH stream. |
| $DEL[ETE] | A.4.7 | Deletes files. |
| $DIR[ECTORY] | A.4.8 | Provides a directory of the specified device. |
| $PRI[NT] | A.4.19 | Prints files. |
| $RT[11] | A.4.20 | Specifies that the following lines are RT-11 mode commands. |

For each command listed below, the term filespec represents a device name, or file name, and a file type. Filespec has this form:

dev:filnam.typ

As a general rule, BATCH assumes device DK: if you omit a device specification.

## A.4.1 \$BASIC

The \$BASIC command calls RT-11 single-user BASIC to execute a BASIC source program. The \$BASIC command has the following syntax:

\$BASIC[/option...] [filespec/option]] [!comments]

/option indicates an option you can append to the \$BASIC command. The options are as follows:

/RUN indicates that BATCH should execute the source program.

/NORUN indicates that BATCH should only compile the program and send error messages to the log file.

/LIST writes data images that are contained in the job stream to the log file (LOG:).

/NOLIST writes data images to the log file only if you specify \$JOB/LIST.

filespec indicates the name and type of the source file and the device on which it resides. If you omit the file type, BATCH assumes .BAS. If you omit this specification, the source statements must immediately follow the \$BASIC command in the input stream.

Terminate the source program after a \$BASIC statement with either a \$EOD command or with any other BATCH command that starts with a \$ in the first position.

/option indicates an option that can follow the source file name. BATCH assumes any file name with no option appended is the name of a source file. This option can have one of the following values (or you can omit it):

/BASIC indicates that the file name you specify is a BASIC source program.

/SOURCE performs the same function as /BASIC.

/INPUT performs the same function as /BASIC.

You can follow the \$BASIC command with the source program, BASIC commands (such as RUN), or data. The following two BATCH streams, for example, produce the same results (but BATCH does not echo the same output format for both streams).

\$BASIC \$BASIC/RUN
10 INPUT A 10 INPUT A
20 PRINT A 20 PRINT A
30 END 30 END
RUN \$DATA
123 123
\$EOD \$EOD

## A.4.2 \$CALL

The \$CALL command transfers control to another BATCH control file, temporarily suspending execution of the current control file. BATCH executes the called file until it reaches \$EOJ or until the job aborts; control then returns to the statement following the \$CALL in the originating BATCH control file. You can nest calls up to 31 levels. BATCH includes the log file for the called file in the log file for the originating BATCH program. (See NOTE following the \$EOJ command.)

The syntax of the \$CALL command is:

## \$CALL filespec[!comments]

Options are not allowed in the \$CALL command. BATCH saves \$JOB command options across a \$CALL; however, they do not apply to the called BATCH file. If you specify .CTL as the file type, BATCH assumes a precompiled BATCH control file. If you do not specify a file type, BATCH assumes .BAT and compiles the called BATCH stream before execution.

## NOTE

If the called program generates temporary files, those files can supersede existing temporary files if the two jobs have the same sequence number. For example, consider the following two BATCH streams:

\$FOR/OBJ A          \$FOR/OBJ A
\$FOR/OBJ B          \$CALL C
\$LINK/RUN         \$FOR/OBJ B

The called BATCH file (C.BAT) contains the following:

```txt
$JOB
$FOR/OBJ A1
$FOR/OBJ B1
$LINK/RUN
$EOJ
```

The temporary object files C.BAT generates change the behavior of the previous two BATCH statement sequences. The first temporary file created by C.BAT (000000.OBJ) supersedes the temporary file produced by the first \$FORTRAN command (000000.OBJ). You can avoid this situation by giving the BATCH job C.BAT a unique sequence number (see Section A.4.22).

## A.4.3 \$CHAIN

The \$CHAIN command transfers control to a named BATCH control file but does not return to the input stream that executed the \$CHAIN command. The syntax of the \$CHAIN command is:

\$CHAIN filespec[!comments]

BATCH does not permit options in the \$CHAIN command. If you specify .CTL as the file type, BATCH assumes a precompiled BATCH control file. If you do not specify a file type, BATCH assumes .BAT and compiles the chained BATCH stream before execution.

A \$EOJ command should always follow the \$CHAIN command in the BATCH stream.

## NOTE

The values of BATCH run-time variables remain constant across a \$CALL, \$CHAIN, or return from call. See Section A.5.2.2 for a description of these variables.

Use the \$CHAIN command to transfer control to programs that you need to run only once at the end of a BATCH stream. For example, you could use the following BATCH program (PRINT.BAT) to print and then delete all temporary listing files generated during the current BATCH job.

\$JOB
\$PRINT/DELETE \*.LST
\$EOJ

## You could then run PRINT.BAT with the \$CHAIN command as follows:

\$JOB
\$MACRO/RUN                      A ALST/LIST
\$MACRO/RUN                      B BLST/LIST
\$CHAIN PRINT .
\$EOJ

## A.4.4 \$COPY

The \$COPY command copies files in image mode from one device to another. You can use the wild card construction (see Section A.2.2.3) in the input and output file specifications. You can concatenate several input files to form one output file (as long as the output specification does not contain a wild card). The \$COPY command has the following syntax:

\$COPY[/option] output-filespec[...,output-filespec]/OUTPUT-input-filespec[...,input-filespec][/INPUT][!comments]

where:

/option indicates options that you can append to the \$COPY command.

/DELETE deletes input files after the copy operation.

/NODELETE does not delete input files after the copy operation.

output-filespec represents an output file; you must specify a file type.

/OUTPUT indicates that a file specification is for an output file.

input-filespec represents a file to be copied. (BATCH copies files to the output file in the order that you list them, except when you use wildcards.)

/INPUT indicates that a file specification is for an input file; if you do not specify an option, BATCH assumes INPUT.

The following are examples of the \$COPY command:

```txt
$COPY *.BAS/OUTPUT DT1:*.BAS
```

This command copies all files with the file type .BAS from the DECtape on unit 1 to the default storage device DK:.

\$COPY FILE2.FOR/OUTPUT FILE0.FOR+FILE1.FOR

This command merges the input files FILE0.FOR and FILE1.FOR to form one file called FILE2.FOR and stores FILE2.FOR on device DK:.

```scss
$COPY *.*/OUT DTO:*.FOR, DT1:*.*/OUT DTO:*.*
```

This command copies all files with the file type .FOR from DT0: to DK: and all files on DT0: to DT1:.

## A.4.5 \$CREATE

The \$CREATE command generates a file from data records that follow the \$CREATE command in the input stream. An error occurs if the data does not immediately follow the \$CREATE command. You cannot precede the data records with a \$DATA command.

You can follow the \$CREATE data with a \$EOD command to signify the end of data, or you can use any other BATCH control statement to indicate end of data and initiate a new function. The \$CREATE command has the following syntax:

\$CREATE[/option...] filespec [!comments]

where:

/option indicates an option you can append to the \$CREATE command. The options are:

/DOLLARS indicates that the data following this command can have a \$ in the first character position of a line.

/NODOLLARS indicates that a \$ cannot be in the first character position of a line.

/LIST writes data image lines to the log file.

does not write data image lines to the log file. If you specify \$JOB/LIST, BATCH ignores this option.

filespec represents the file you want to create.

## NOTE

If you use the /DOLLARS option, you must follow the last data record with a \$EOD command (see Table A-1).

The following is an example of the \$CREATE command:

\$CREATE/LIST PROG.FOR
FORTRAN source file
\$EOD

The data records following the \$CREATE command become a new file (PROG.FOR) on the default device (DK:). BATCH generates a listing on logical device LOG:.

## A.4.6 \$DATA

Use the \$DATA command to include data records in the input stream. Data you include in this manner needs no file name. BATCH transfers the data to the appropriate program as though it were input from the console terminal. For example, you can follow the \$RUN command for a particular program by a \$DATA command and the data records for the program to process. The data records must be valid data for the program that is to use them.

The \$DATA command has the following syntax:

\$DATA[/option...] [!comments]

Four options that you can use with the \$DATA command are as follows:

/DOLLARS Indicates that the data following this command can have a \$ in the first character position of a line.

/NODOLLARS. Indicates that a \$ cannot be in the first character position of a line.

/LIST Writes data image lines to the log file.

/NOLIST Does not write data images to the log file. If you specify \$JOB/LIST, BATCH ignores this option.

## NOTE

Any command beginning with a \$ normally follows the last data record. However, if you specify \$DATA/DOLLARS, you must follow the last data record with \$EOD.

The following example shows data entered into a BASIC program (TEST1.BAS).

```csv
$BASIC/RUN TEST1,BAS
$DATA
25,75,125,146
180,210,520,874
$EOD
```

A.4.6.1 Using \$DATA with FORTRAN Programs — When you use the \$DATA command to provide input to a FORTRAN program, you must insert a CTRL/Z into the BATCH file after the last data line and before \$EOD (or before the next BATCH command if you do not use \$EOD). This procedure permits FORTRAN to properly detect an end-of-file after it reads the last data line. For example:

```csv
$FORTRAN/RUN A, FOR
$DATA
1
2
3 .
^Z RET LF
$EOD
$RUN PIP
```

The above program reads three numbers from the input stream and then detects an end-of-file when it attempts to read a fourth number. If you include an END=n statement in your FORTRAN program, statement n gets control when the end-of-file is detected. If the CTRL/Z &lt;RET&gt; &lt;LF&gt; is not present, the program aborts when it reaches \$EOD and never executes the END=n statement.

## A.4.7 \$DELETE

Use the \$DELETE command to delete files from the device you specify. This command has the syntax:

\$DELETE filespec[...,filespec][!comments]

filespec represents the name of a file to be deleted

The following example deletes all files named TEST1 on the default device DK:.

\$DELETE TEST1.\*

The following example deletes all files with .FOR file types on DT1:, then deletes all files with .MAC file types on DK:.

```csv
$DELETE DT1:*,FOR,*,MAC
```

## A.4.8 \$DIRECTORY

The \$DIRECTORY command outputs a directory of the device you specify to a listing file. If you do not specify a listing file, the listing goes to the BATCH log file. This command has the syntax:

\$DIRECTORY [filespec/LIST] [filespec[...,filespec]][/INPUT]
[!comments]

where:

filespec/LIST indicates the name of the directory listing file

filespec/INPUT indicates the input files to be included in the directory (default)

The following command outputs a directory of the device DK: to the BATCH log file.

## \$DIRECTORY

This next command creates on the device DK: a directory file (FOR.DIR) that contains the names, lengths, and dates of creation of all FORTRAN source files on that device.

\$DIRECTORY FOR.DIR/LIST \*.FOR

## A.4.9 \$DISMOUNT

The \$DISMOUNT command removes the logical device name assigned by a \$MOUNT command. When BATCH encounters \$DISMOUNT while executing a job, it prints the entire \$DISMOUNT command line on the console terminal. This message tells the operator which device to unload. This command has the syntax:

\$DISMOUNT[/option] logical-device-name:[/LOGICAL] [!comments] where:

/option indicates an option you can append to the \$DISMOUNT command. The options are:

/WAIT indicates that the job must pause until the operator enters a response. If you do not specify either /WAIT or /NOWAIT, BATCH assumes /WAIT. BATCH rings a bell at the terminal, prints the physical device name to be dismounted followed by a question mark (?), and waits for a response. (At this point you can enter input to the BATCH handler. See Section A.7.3.)

/NOWAIT does not pause for operator response; BATCH prints the physical device name to be dismounted.

logical-device-name: is the logical device name to be deassigned from the physical device.

/LOGICAL identifies the device specification as a logical device name.

The following example instructs the operator to dismount the physical device with the logical device name OUT: and removes the logical assignment of device OUT:. In this example, OUT: is DT0:. The operator dismounts DT0: and then types a carriage return.

\$DISMOUNT/WAIT OUT:/LOGICAL
DTO?

## A.4.10 \$EOD

The \$EOD command indicates the end-of-data record or the end of a source program in the job stream. The syntax of this command is:

\$EOD [!comments]

The \$EOD command can signal the end of data associated with any of the following commands:

\$BASIC \$FORTRAN
\$CREATE \$MACRO
\$DATA

In the following example, the \$EOD command indicates the end of a source program that is to be compiled, linked, and executed.

\$FORTRAN/RUN
source program
\$EOD

## A.4.11 \$EOJ

The \$EOJ command indicates the end of a job. This command must be the last statement in every BATCH job. The command has the following syntax:

## \$EOJ [!comments]

If BATCH encounters a \$JOB command, a \$SEQUENCE command, or a physical end-of-file in the input stream before \$EOJ, an error message appears in the log file.

## NOTE

Make sure that the \$EOJ command is the last line in a BATCH file.

## A.4.12 \$FORTRAN

The \$FORTRAN command calls the FORTRAN compiler to compile a source program. Optionally, this command can provide printed listings or list files and can produce a link map in the listing. The \$FORTRAN command has the following syntax:

\$FORTRAN[/option...] [source-filespec[/option]] [filespec/OBJECT]-

[filespec/LIST] [filespec/EXECUTE]-

[filespec/MAP] [filespec/LIBRARY] [!comments]

where:

/option indicates an option you can append to the \$FORTRAN command. The options are as follows:

/RUN indicates that FORTRAN is to compile the source program, link it with the default library, and execute it. The default library is SYSLIB.OBJ. You can change it with the \$LIBRARY command.

/NORUN compiles the program only.

/OBJECT produces a temporary object file.

/NOOBJECT does not produce a temporary object file.

/LIST produces a list file on the listing device (LST:).

/NOLIST does not produce a list file.

/MAP produces a link map on the listing device (LST:).

/NOMAP does not create a MAP file.

/DOLLARS indicates that the data following this command can have a \$ in the first character position of a line.

/NODOLLARS indicates that a \$ cannot be in the first character position of a line.

source-filespec indicates the device, file name, and file type of the FORTRAN source file. If you do not specify the file name, the \$FORTRAN source statements must immediately follow the \$FORTRAN command in the input stream; BATCH generates a temporary source file that it deletes after FORTRAN compiles the temporary source file (see Section A.2.5).

## filespec/OBJECT

You can terminate the source program included after a \$FORTRAN statement by either a \$EOD command or by any other BATCH command. If, however, you use dollar signs in the first position in the source program, you must enter the source program with \$CREATE/DOLLARS. In this case, you cannot use \$FORTRAN/DOLLARS.

represents an option that can have one of the following values:

/FORTRAN indicates that the file name you specify is a FORTRAN source program. BATCH assumes that any file name with no option appended is the name of a source file.

/SOURCE performs the same function as /FORTRAN.

/INPUT performs the same function as /FORTRAN.

indicates the device, file name, and file type of the object file produced by compilation. The object file remains on the device you specify after the job finishes. You must follow the object file specification, if you include it, with the /OBJECT option.

If you omit the object file specification but specify \$FORTRAN/OBJECT, BATCH creates a temporary object file. BATCH includes this temporary file in any \$LINK operations that follow it in the job, and deletes it after the link operation.

indicates the name you assign to the list file created by the compiler. BATCH does not automatically print the list file if you assign LST: to a file-structured device, but you can list it using the \$PRINT command. Follow the list file specification with the /LIST option.

filespec/EXECUTE indicates the name you assign to a memory image file. Follow the memory image file specification with the /EXECUTE option. If you do not include this field, BATCH generates a temporary memory image file (see Section A.2.5) and then deletes the temporary file.

espec/MAP indicates the name you assign to the link map file created by the linker. Follow the map specification with the /MAP option.

filespec/LIBRARY indicates that BATCH must include the file you specify in the link procedure as a library before SYSLIB.OBJ. The file must be a library file (produced by the RT-11 librarian). Follow the library specification with the /LIBRARY option.

The following command calls FORTRAN to compile and execute a source program named PROGA.FOR.

\$FORTRAN/RUN PROGA.FOR

The next command sequence compiles the FORTRAN program but does not produce an object file. BATCH creates a temporary listing file on LST:.

\$FORTRAN/NOOBJ/LIST

source program

\$EOD

## NOTE

See Section A.4.6.1 for instructions on using the \$DATA command with FORTRAN programs.

A.4.13 \$JOB

The \$JOB command indicates the beginning of a job. Each job must have its own \$JOB command. This command has the following syntax:

\$JOB[/option...] [!comments]

BATCH allows the following options in the \$JOB command:

/BANNER Prints a header (a repetition of the \$JOB line or card) on the log file.

/NOBANNER Does not print a job header.

/LIST Writes data image lines that are contained in the job stream to the log file.

/NOLIST Writes data image lines to the log file only when a /LIST option exists on a \$BASIC, \$CREATE, or \$DATA command that has data lines following it.

/RT11 If no \$ appears in column 1 when BATCH expects one, BATCH assumes that the line or card is an RT-11 mode command (see Section A.5).

/NORT11 Does not process RT-11 mode commands.

/TIME Writes the time of day to the log file when BATCH executes command lines (except \$DATA command lines).

/NOTIME Does not write the time of day.

/UNIQUE Checks for unique spelling of options and keynames. When you use this option, you can abbreviate commands and options to the fewest number of characters that still make their names unique. For example, you can abbreviate the /DOLLARS option to /DO since no other option begins with the characters DO.

/NOUNIQUE Checks only for normal option and keyname spellings.

End each job with a \$EOJ command if you want to run it. If an input stream consists of more than one job, BATCH automatically terminates one job when it encounters the \$JOB command for the next job. BATCH will never run a job terminated with another \$JOB command; instead, an error message will appear in the log.

The following \$JOB command writes the time of day to the log file before BATCH executes each command beginning with a \$. It also accepts unique abbreviations of BATCH commands and options.

\$JOB/TIME/UNIQUE

## A.4.14 \$LIBRARY

The \$LIBRARY command lets you specify a list of library files for inclusion in FORTRAN links or other link operations that have the /LIBRARY option. By default, the list of libraries contains only SYSLIB.OBJ, the RT-11 system library. This command has the syntax:

\$LIBRARY filespec [!comments]

or

\$LIBRARY filespec + SYSLIB [!comments]

where:

filespec represents a library file; the default file type is .OBJ

SYSLIB is the RT-11 system library that you create at system generation

Libraries are linked in order of their appearance in the \$LIBRARY command.

The following example shows two libraries (LIB1.OBJ and LIB2.OBJ) that are included in FORTRAN links before SYSLIB.OBJ.

\$LIBRARY LIB1.OBJ+LIB2.OBJ+SYSLIB.OBJ

## A.4.15 \$LINK

Use the \$LINK command to produce memory image files from object files. This command links any files you may specify with any temporary object files created since the last link or link-and-go operation.

Temporary object files are those files you create as a result of a \$FORTRAN or \$MACRO command without naming an object file (with the /OBJECT option) by suppressing an object file (with the /NOOBJECT option). Create permanent object files by using the /OBJECT option on a \$FORTRAN or \$MACRO file descriptor.

BATCH links files in the following order:

1. Temporary files — in the order in which they were compiled

2. Permanent files — in the order in which they are specified in the \$LINK command

3. Any library specified by the \$LINK command — provided that unresolved references remain

4. The default library list — if you specified \$LINK/LIBRARY

The syntax for this command is:

\$LINK[/option...] [filespec/OBJECT] [filespec/LIBRARY]-[filespec/MAP] [filespec/EXECUTE] [!comments]

where:

/option indicates an option that you can append to the \$LINK command. The options are as follows:

/LIBRARY includes the RT-11 system library (SYSLIB.OBJ) and any default libraries specified in the \$LIBRARY command in this \$LINK operation. Use this option when the files being linked do not include any temporary FORTRAN object files. You can also use it when you specify \$FORTRAN without the /RUN or /MAP option, but want to search the default library list for unresolved references.

/NOLIBRARY does not include the default libraries.

/MAP produces a temporary load map on the listing device (LST:).

/NOMAP does not produce a map file.

/OBJECT includes temporary object files in the link. If you specify neither /OBJECT nor /NOOBJECT, BATCH assumes \$LINK /OBJECT.

/NOOBJECT does not include temporary files in the link.

/RUN executes the memory image files associated with this \$LINK command when the link is complete.

/NORUN only links the program and does not execute it.

filespec/OBJECT indicates the name of the object file BATCH must link; if you do not specify /OBJECT, BATCH assumes it as the default.

filespec/LIBRARY indicates that the file you specify is to be included in the link procedure as a library; the file you specify must be a library file (produced by the RT-11 librarian).

filespec/MAP indicates the load map file BATCH must create as a result of the \$LINK command.

filespec/EXECUTE indicates the memory image file BATCH must create as a result of the \$LINK command.

The following command links all temporary object files created since the last \$LINK command, or the last \$FORTRAN/OBJ or \$MACRO/OBJ command.
\$LINK /RUN

The next command links the temporary files and the object files PROG1.OBJ and PROG2.OBJ to form a memory image file named PROGA.SAV. It also creates and outputs a temporary map file.

\$LINK/MAP PROG1.OBJ+PROG2.OBJ/OBJ PROGA.SAV/EXE

## A.4.16 \$MACRO

The \$MACRO command calls the MACRO assembler to assemble a source program and, optionally, to provide printed listings or list files. You must specify any MACRO listing directives in the source program; you cannot enter them at BATCH command level.

The \$MACRO command has the following syntax:

\$MACRO[/option...] [source-filespec[/option]] [filespec/OBJECT]-[filespec/LIST] [filespec/MAP] [filespec/LIBRARY]-[filespec/EXECUTE] [!comments]

indicates an option you can append to the \$MACRO command. The options are as follows:

/RUN assembles, links, and runs the source program.

/NORUN only assembles the source program.

/OBJECT produces a temporary object file.

/NOOBJECT does not produce a temporary object file.

/LIST produces a listing file on the listing device (LST:).

/NOLIST does not produce a list file.

/cref produces a cross-reference listing during assembly.

/NOCREF does not produce a cross-reference listing during assembly.

/MAP produces a link map as part of the listing file on LST:.

/NOMAP does not create a MAP file.

/DOLLARS indicates that the data following this command can have a \$ in the first character position of a line.

/NODOLLARS indicates that a \$ cannot be in the first character position of a line.

/LIBRARY includes the default library in the link operation.

/NOLIBRARY does not include the default library in the link operation.

indicates the name of the source file. If you do not specify a file name, the \$MACRO source statements must immediately follow the \$MACRO command in the input stream.

You can terminate the source program you include after a \$MACRO statement with either a \$EOD command or any other BATCH command.

If, however, you include dollar signs in the first position in the source program, use the \$CREATE/DOLLARS command to enter the source program. In this case, you cannot use \$MACRO/DOLLARS.

can have one of the following values:

/MACRO indicates that the file name you specify is a MACRO source program. BATCH assumes that any file name with no option appended is the name of a source file.

/SOURCE performs the same function as /MACRO.

/INPUT performs the same function as /MACRO.

indicates the name you assign to the object file produced by compilation. The object file remains on the device you specify after the job finishes. If you include an object file specification, follow it with the /OBJECT option.

If you omit the object file specification but specify \$MACRO/OBJECT, BATCH creates a temporary object file. BATCH also includes the temporary object file in any \$LINK operations that follow the \$MACRO command in the job, and deletes it after the link operation (see Section A.2.5).

indicates the name you assign to the list file created by the assembler. BATCH does not print the list file if you assign LST: to a file-structured device, but you can list it using the \$PRINT command. The /LIST option must follow the list file specification.

indicates the file to which BATCH must output the storage map.

indicates that BATCH must include the file you specify in the link procedure as a library. The /LIBRARY option must follow the library file specification.

filespec/EXECUTE indicates the name you assign to a memory image file. The /EXECUTE option must follow the memory image file specification. If you do not include this field but do use \$MACRO/RUN, BATCH generates and runs a temporary memory image file (see Section A.2.5).

The following \$MACRO command assembles a program named PROG0.MAC, and creates a temporary object file and a temporary listing file.

\$MACRO/LIST/OBJECT PROGO, MAC

## A.4.17 \$MESSAGE

Use the \$MESSAGE command to issue a message to the operator at the console terminal. It provides a means for the job to communicate with the operator. The \$MESSAGE command has the syntax:

\$MESSAGE[/option] message [!comments]

where:

/option indicates an option you can append to the \$MESSAGE command. The options are:

/WAIT indicates that the job is to pause until the operator either types a carriage return to continue or enters commands to the BATCH handler followed by a carriage return (see Section A.7.3).

/NOWAIT does not pause for operator response.

message is a string of characters that must fit on one console line.
BATCH prints the message on the console.

For example, if you include the following message in the input stream:

\$MESSAGE/WAIT MOUNT SCRATCH TAPE ON MTO:

The message:

MOUNT SCRATCH TAPE ON MTO:
?

appears on the console terminal and a bell sounds. The operator mounts the tape and types carriage return to allow further processing of the job. (See Section A.7.3 for operator interaction with BATCH.)

## NOTE

BATCH compresses multiple spaces and tabs in BATCH command lines; therefore, attempts to format \$MESSAGE output with tabs or spaces may not provide you with the desired results.

## A.4.18 \$MOUNT

The \$MOUNT command assigns a logical device name and other characteristics to a physical device. When BATCH encounters \$MOUNT during the execution of a job, it prints the entire \$MOUNT command line on the console terminal to notify the operator which volume to use.

The \$MOUNT command has the syntax:

\$MOUNT[/option...] physical-device-name:[/PHYSICAL][/VID = x]
[logical-device-name:/LOGICAL] [!comments]

where:

indicates an option you can append to the \$MOUNT command. The options are:

/WAIT indicates that the job is to pause until the operator enters a response. If you do not specify either /WAIT or /NOWAIT, BATCH assumes /WAIT. BATCH rings a bell, prints the physical device name and a question mark (?), and waits for a response. (The response can consist of input for the BATCH handler; see Section A.7.3.)

/NOWAIT does not pause for operator response. BATCH prints the name of the physical device to be mounted.

/WRITE tells the operator to write-
enable the volume.

/NOWRITE tells the operator to write-protect the volume.

is required and specifies the physical device name and an optional unit number followed by a colon (for example, DT1:). If you specify a device name without a unit number, the operator can enter one in response to the question mark printed by the \$MOUNT command. If you want the operator to supply a unit number, do not use the /NOWAIT option, because it assumes unit 0.

identifies the device specification as a physical unit specification. If you do not specify either /PHYSICAL or /LOGICAL, BATCH assumes /PHYSICAL.

provides volume identification. The volume identification is the name physically attached to the volume. Include it to help the operator locate the volume. Use this option only on the physical device file specification. If x contains spaces, specify it as "x".

## NOTE

This volume identification is only a visual check for the operator. Make the identification match the visual label on the volume, not the identification that you wrote onto the volume at initialization time with the INIT/VOLUMEID command.

logical-device-name/LOGICAL is required to identify any logical device name you may assign to the device. The /LOGICAL option must follow the logical device name specification.

The following command instructs the operator to select a DECtape unit and mount DECtape volume BAT01 on that unit, write-enabled. It informs the operator by printing:

\$MOUNT/WAIT/WRITE DT:/VID=BATO1 2:/LOGICAL
DT?

The operator selects a unit, mounts DECtape volume BAT01, write-enabled, and responds to the question mark by typing the unit number (such as, 1) followed by a carriage return. BATCH assigns logical device name 2 to the physical device (in this case, DT1:) and proceeds.

If no unit number response is necessary, as this command shows,

\$MOUNT/WAIT/WRITE DT1: 2:/LOGICAL

the operator responds with a carriage return after mounting the DECtape and write-enabling the device.

## A.4.19 \$PRINT

Use the \$PRINT command to print the contents of the files you specify on the listing device (LST:). This command has the syntax:

\$PRINT[/option] filespec [...,filespec][/INPUT] [!comments]

where:

/option indicates an option you can append to the \$PRINT command. The options are:

/DELETE    deletes input files after printing.

```perl
$RUN DIR
$DATA
LP:=DK:/L
$EOD
```

/NODELETE does not delete input files after printing.

filespec represents a file to be printed.

/INPUT indicates that the file is an input file; BATCH assumes /INPUT if you omit it.

The following command prints a listing of files with file type .MAC that are stored on default device DK:.

\$PRINT \*.MAC

The following example creates listing files for the programs A and B, prints the listing files, and then deletes them.

\$MACRO A, MAC A/LIST
\$MACRO B, MAC B/LIST
\$PRINT/DELETE A, LST, B, LST

## A.4.20 \$RT11

The \$RT11 command allows the BATCH job to communicate directly with the RT-11 system. DIGITAL recommends that you use RT-11 mode if you use BATCH. This command puts BATCH in RT-11 mode until BATCH encounters a line beginning with \$. In RT-11 mode, BATCH interprets all data images as commands to the RT-11 monitor, to RT-11 system programs, or to the BATCH run-time system. The \$RT11 command has the syntax:

\$RT11 [!comments]

See Section A.5 for a complete description of the RT-11 mode.

## A.4.21 \$RUN

The \$RUN command executes a program for which a memory image file (.SAV) was previously created. It can also run RT-11 system programs.

The \$RUN command has the syntax:

\$RUN filespec [!comments]

where:

filespec represents the file to be executed. If you omit the file type, BATCH assumes .SAV.

For example, if DIR is on DK:, you can run DIR to print a directory listing:

## A.4.22 \$SEQUENCE

The \$SEQUENCE command is an optional command. If you use it, it must immediately precede a \$JOB command. The \$SEQUENCE command assigns a job an arbitrary identification number. BATCH assigns the last three characters of a sequence number as the first three characters of a temporary listing or object file (see Section A.2.5). If a sequence number is less than three characters long, BATCH fills it with zeroes on the left.

The syntax of this command is:.

\$SEQUENCE id [!comments]

where:

id represents an unsigned decimal number that indicates the identification number of a job

The following are examples of the \$SEQUENCE command:

```txt
$SEQUENCE 3 !SEQUENCE NUMBER IS 003
$JOB
```

\$SEQUENCE 100 !SEQUENCE NUMBER IS 100
\$JOB

## A.4.23 Sample BATCH Stream

The following sample BATCH stream creates a MACRO program, assembles and links that program, and runs the memory image file. It then deletes the object, memory image, and source files it created and prints a directory of DK: showing the files the BATCH stream created.

\$JOB
\$MESSAGE          THIS IS AN EXAMPLE BATCH STREAM
\$MESSAGE          NOW CREATE A MACRO PROGRAM
\$CREATE/LIST     EXAMPL.MAC
<TITLE  EXAMPL FOR BATCH
        .MCALL   .PRINT,,EXIT
START:    .PRINT   #MESSAG
        .EXIT
MESSAGE:   .ASCIZ  /EXAMPLE MACRO PROGRAM FOR BATCH/
        .END     START
\$EOD
\$MACRO  EXAMPL EXAMPL/OBJECT EXAMPL/LIST   !ASSEMBLE
\$LINK  EXAMPL EXAMPL/EXECUTE         !AND LINK
\$PRINT/DELETE EXAMPL.LST
\$MESSAGE          RUN THE MACRO PROGRAM
\$RUN     EXAMPL                   !AND EXECUTE
\$DELETE EXAMPL.OBJ+EXAMPL.SAV+EXAMPL.MAC
\$MESSAGE          PRINT A DIRECTORY
\$DIRECTORY      DK:EXAMPL.\*
\$MESSAGE          END OF THE EXAMPLE BATCH STREAM
\$EOJ

```powershell
$EOD
$MACRO  EXAMPL  EXAMPL/OBJECT  EXAMPL/LIST   !ASSEMBLE
```

To run this batch stream, type the following commands at the console. BATCH prints the messages.

```csv
LOAD BA,LP
ASSIGN LP:LOG
ASSIGN LP:LST
R BATCH
*EXAMPL
THIS IS AN EXAMPLE BATCH STREAM
NOW CREATE A MACRO PROGRAM
RUN THE MACRO PROGRAM
PRINT A DIRECTORY
END OF THE EXAMPLE BATCH STREAM
END BATCH
```

The above sample BATCH stream produces the following log file on the line printer:

## NOTE

The amount of free memory and the directory format are variable.

\$MESSAGE NOW CREATE A MACRO PROG.

\$CREATE/LIST     EXAMPLE.MAC

```asm
.TITLE EXAMPLE FOR BATCH
.MCALL PRINT, EXIT
START: PRINT #MESSAGE
.EXIT
MESSAGE: ASCIZ /EXAMPLE MACRO PROGRAM FOR BATCH/
.EVEN
.END START
```

ERRORS DETECTED: 0

```txt
EXAMPLE FOR BATCH MACRO V03.00 21-JUN-77 00:05:29 PAGE 1
```

```asm
.TITLE EXAMPLE FOR BATCH
.MCALL .PRINT,.EXIT
START: .PRINT #MESSAGE
.EXIT
MESSAG: .ASCIZ /EXAMPLE MACRO PROGRAM FOR BATCH
000010 105 130 101
000013 115 120 114
000016 105 040 115
000021 101 103 122
000024 117 040 120
000027 122 117 107
000032 122 101 115
000035 040 106 117
000040 122 040 102
000043 101 124 103
000046 110 000
.EVEN
.END START
```

EXAMPLE FOR BATCH MACRO V03.00 21-JUN-77 00:05:29 PAGE 1-1
SYMBOL TABLE
MESSAGE 00001OR START 000000R
ABS. 000000 000
000050 001
ERRORS DETECTED: 0
VIRTUAL MEMORY USED: 508 WORDS (2 PAGES)
DYNAMIC MEMORY AVAILABLE FOR 48 PAGES
EXAMPL,EXAMPL=EXAMPL
\$LINK EXAMPL EXAMPL/EXECUTE !AND LINK
\$PRINT/DELETE EXAMPL.LST
\$MESSAGE RUN THE MACRO PROGRAM
\$RUN EXAMPL !AND EXECUTE
EXAMPLE MACRO PROGRAM FOR BATCH
\$DELETE EXAMPL.OBJ+EXAMPL.SAV+EXAMPL.MAC
\$MESSAGE PRINT A DIRECTORY
\$DIRECTORY DK:EXAMPL.\*
21-JUN-77
EXAMPL.BAK 2 14-JUN-77 EXAMPL.BAT 2 21-JUN-77
EXAMPL.CTL 3 21-JUN-77
3 FILES, 7 BLOCKS
1903 FREE BLOCKS
\$MESSAGE END OF THE EXAMPLE BATCH STREAM
\$EOJ

## A.5 RT-11 MODE

RT-11 mode lets you enter commands to the RT-11 monitor or to system programs, and lets you create BATCH programs. You can enter RT-11 mode with either the \$JOB/RT11 command or the \$RT11 command. If you enter RT-11 mode with the \$JOB/RT11 command, RT11 mode remains in effect until BATCH encounters the next \$JOB command. If you enter RT-11 mode with the \$RT11 command, RT-11 mode is in effect until BATCH encounters a \$ in the first position of the command line.

When the characters ., \$, \*, and tab or space appear in the first position of a line (or card column. 1), they are control characters and indicate the following:

Command to the RT-11 monitor, for example,

\* Data line; any line not intended to go to the RT-11 monitor or to the BATCH run-time handler, such as a command to the RT-11 PIP program:

## NOTE

BATCH does not pass the \* as data to the program. Comment lines (!) cannot appear on data lines, as BATCH would consider them as data.

\$ BATCH command. It causes an exit from RT-11 mode if you entered RT-11 mode with the \$RT11 command. For example:

```txt
$RT11
.R PIP
*FILE1.DAT/D
$FORTRAN.
!ENTER RT-11 MODE
!LEAVE RT-11 MODE
```

space/tab Separator to indicate a line directed to BATCH run-time handler. This separator is indicated by a &lt;TAB&gt; in the following descriptions.

## A.5.1 Communicating with RT-11

The most common use of RT-11 mode is to send commands to the RT-11 monitor and to run system programs. For example, you can insert the following commands in the BATCH stream to run PIP and save backup copies of files on DECtape:

```txt
$RT11
.R PIP
*DT1:*, *= *.FOR
```

You must anticipate and include in the BATCH input stream responses that the called program requires, such as the Y response to DUP's Are you sure? query. Place a line in your BATCH file consisting of Y and RETURN or use the DUP /Y option to suppress the query. For example:

```powershell
$RT11
.INITIALIZE RK1:
*Y
```

You can communicate directly with the RT-11 monitor by using the keyboard monitor commands that are described in Section 4.5 of the RT-11 System User's Guide. For example:

```csv
$RT11
+DELETE/NOQUERY DX1:*,MAC
```

This command deletes all files with a file type of .MAC from device DX1:.

You cannot mix BATCH standard commands with RT-11 mode data lines (lines beginning with an asterisk). For example, the proper way to do a \$MOUNT within a sequence of RT-11 mode data commands is:

```powershell
$JOB/RT11
.R MACRO
*A1=A1
*A2=A2
$MOUNT DTO:/PHYSICAL
.R MACRO
*B1=DT:B1
*B2=DT:B2
```

## A.5.2 Creating RT-11 Mode BATCH Programs

Advanced system programmers can use RT-11 mode to create BATCH programs. These BATCH programs consist of standard RT-11 mode commands (monitor commands, data lines for input to system programs, etc.) plus special RT-11 mode commands. The BATCH run-time handler interprets these special commands to allow dynamic calculations and conditional execution of the RT-11 mode standard commands. The following can help you create BATCH programs and dynamically control their execution at run-time:

\- Labels

\- Variable modification:

1. Equating a variable to a constant or character (LET statement)

2. Passing the value of a variable to a program

3. Incrementing the value of a variable by 1

4. Conditional transfers on comparison of variable values with numeric or character values (IF and GOTO statements)

\- Commands to control terminal I/O

\- Other control characters

\- Comments

A.5.2.1 Labels – You define labels in RT-11 mode to provide a symbolic means of referring to a specific location within a BATCH program. If present, a label must begin in the first character position, must be unique within the first six characters, and must terminate with a colon (:) and a carriage return/line feed combination.

A.5.2.2 Variables - A variable in RT-11 mode is a symbol representing a value that can change during program execution. The 26 variables BATCH permits in a BATCH program have the names A-Z; each variable requires one byte of physical storage. There are four ways to modify variables.

You can assign values to variables in a LET statement.

You can then test these values by an IF statement to control the direction of program execution.

```javascript
or
    <TAB>IF(x-n) label1, label2, label3
```

Assign values to variables with a LET statement of the following form:

```twig
<TAB>LET x="c
```

where:

x represents a variable name in the range A–Z

"c indicates the ASCII value of a character

For example:

```txt
TAB LET A = "0
```

This example indicates that the value of variable A is the 7-bit ASCII value of the character 0 (60).

The LET statement can also specify an octal value in the form:

```txt
<TAB>LET A=n
```

where:

n represents an 8-bit signed octal value in the range 0–377. Positive numbers range from 0–177; negative numbers range from 200–377 (-200 to -1).

You can use variables to introduce control characters, such as ESCAPE, into a BATCH stream. For example, wherever 'A' appears in the following BATCH stream, BATCH substitutes the contents of variable A (the code for an ESCAPE):

```txt
$JOB/RT11
    LET A=33
    !A IS AN ESCAPE
.R EDIT
*EBFILE,MAC'A''A'
*R'A''A'
    !EDIT FILE TO CHANGE THE VERSION NUMBER TO 2
*GVERSION='A'DI2'A''A'
*EX'A''A'
```

Increment the value of a variable by 1 by placing a percentage sign (\%) before the variable. For example:

```txt
TAB % A
```

This command indicates that BATCH must increase the unsigned contents of variable A by 1.

Indicate with an IF statement conditional transfers of control according to the value of a variable. The IF statement has the syntax:

```txt
<TAB>IF(x-“c) label1, label2, label3
```

where:

x represents the variable to be tested

"c is the ASCII value to be compared with the contents of the variable

n is an octal integer in the range 0–377

label1
label2 represent the names of labels included in the BATCH stream
label3

When BATCH evaluates the expression (x-“c) or (x-n), the BATCH run-time handler transfers control to:

\- label1 if the value of the expression is less than zero

\- label2 if the value of the expression is equal to zero

\- label3 if the value of the expression is greater than zero

If you omit one of the labels, and the condition is met for the omitted label, control transfers to the line following the IF statement.

## NOTE

Since this comparison is a signed byte comparison, 377 is considered to be -1.

The characters + and - allow you to control where BATCH begins searching for label1, label2, and label3. If you precede the label by a minus sign (-), BATCH starts the label search just after the \$JOB command. If a plus sign (+) or no sign precedes the label, the label search starts after the IF statement. For example:

TAB IF (B-"9) -LOOP, LOOP1,

This statement transfers program control to the label LOOP following the \$JOB command if the contents of variable B are less than the ASCII value of 9. It transfers control to the label LOOP1 following the IF statement if B is equal to ASCII 9. If the contents of variable B are greater than the ASCII value of 9, program control goes to the next BATCH statement in sequence.

The GOTO statement unconditionally transfers program control to a label you specify as the argument of the statement. You can use one of the following three forms of this statement:

&lt;TAB&gt;GOTO label

Transfers control to the first occurrence of label that appears after this GOTO statement in the BATCH stream

&lt;TAB&gt;GOTO + label

Same as GOTO label

&lt;TAB&gt;GOTO -label Transfers control to the first occurrence of label that appears after the \$JOB command

The following GOTO statement transfers control unconditionally to the next label LOOP if such a label appears in the BATCH stream following the GOTO statement.

TAB GOTO LOOP

## NOTE

If BATCH cannot find a label (for example, you unintentionally omit a minus sign), the BATCH handler searches until it reaches the end of the .CTL file and ends the job.

A.5.2.3 Terminal I/O Control – You can issue commands directly to the BATCH run-time handler to control logging console terminal input and output. If you do not enter any of the following commands, BATCH assumes TTYOUT (this includes indirect command files).

&lt;TAB&gt;NOTTY Does not write terminal input and output to the log file. Comments to the log are still logged.

&lt;TAB&gt;TTYIN      Writes only terminal input to the log file.

&lt;TAB&gt;TTYIO Writes terminal input and output to the log file. (You should enter this command if using RT-11 mode so that RT-11 mode commands go to the log file.)

&lt;TAB&gt;TTYOUT Writes only terminal output to the log file (default).

A.5.2.4 Other Control Characters – The system permits other control characters in an RT-11 mode command that begins with a period (.) or an asterisk (\*). Following are these control characters and their meanings:

'text' command to BATCH run-time handler, where text can be one of the following:

CTY accepts input from the console terminal; notifies the operator that action is required by ringing a bell and printing a question mark (?).

FF outputs the current log buffer.

NL inserts a new line (line feed) in the BATCH stream.

x inserts the contents of a variable where x is an alphanumeric variable in the range A through Z. It indicates that BATCH should insert the contents of the variable as an ASCII character at this place in the command string.

"message" directs the message to the console terminal.

The following commands allow the operator to enter the name of a MACRO program to be assembled. The BATCH stream contains:

The operator receives the following message at the terminal and types a response, followed by a carriage return; BATCH processing continues.

```txt
ENTER MACRO COMMAND STRING
?
```

To run the same BATCH file on several systems with different configurations you need to assign a device dynamically. The following RT-11 mode command lets you request that the listing device name be entered by the operator.

The operator receives the message and responds with the device to be used as the listing device (DT2:).

```txt
PLEASE TYPE LST DEVICE NAME
?
```

A.5.2.5 Comments – You can include comments in RT-11 mode as separate comment statements. Include comments by typing a separator followed by a ! and the comment. For example:

## A.5.3 RT-11 Mode Examples

The following are examples of BATCH programs using the RT-11 mode.

This BATCH program assembles, lists, and maps 10 programs with only 12 BATCH commands.

The following program lets you set up a master control stream to run several BATCH jobs with one call to BATCH. First set up a BATCH job (INIT.BAT) that performs a \$CHAIN to the master control stream:

```txt
\$JOB/RT11
    LET I="O
    !INITIALIZE INDEX
\$CHAIN MASTER          !GO TO MASTER
\$EOJ
```

The following is the master control stream (MASTER.BAT) to which INIT chains.

```csv
$JOB/RT11 !MASTER CONTROL STREAM
%I
!BUMP INDEX BY 1
IF(I-"7),,END
.R BATCH
!THIS IS A $CHAIN
*JOB'I'
!RUNS JOB1-JOB7
END:
$MESSAGE END OF BATCH RUN
$EOJ
```

Each job MASTER.BAT will run must contain the following:

```txt
$JOB
!BATCH COMMANDS
$CHAIN MASTER
$EOJ
```

Activate the master control stream by calling BATCH as follows:

```txt
.R BATCH
*INIT
```

## A.6 Creating BATCH Programs on Punched Cards

To create a BATCH program on punched cards, punch into the cards the commands described in Section A.4. Each command line occupies a single punched card. Only one card, the EOF card, is different from the standard BATCH commands. The EOF (end-of-file) card terminates the list of jobs from the card reader.

To create the EOF card, hold the MULT PCH key on the keypunch keyboard while typing the following characters:

```txt
- & 0 1 6 7 8 9
```

This procedure produces an EOF card with holes punched in the first column (see Figure A-1).

Figure A-1: EOF Card

[figure omitted]

To run multiple jobs from the card reader, simply combine the jobs into a single card deck. Make sure that each job has its own \$JOB and \$EOJ card, and then follow the last \$EOJ card with two EOF cards.

Although in general, you terminate BATCH jobs on cards by placing two EOF cards after the last \$EOJ card, some card readers may require that you type —F followed by a carriage return. Put two EOF cards and a blank card in the reader and make sure that the card reader is ready. Note that a small card deck (less than 512 characters) may require more than two EOF cards to terminate the deck.

## A.7 Operating Procedures

This section describes the operations you must perform to prepare for using BATCH, and for running BATCH.

## A.7.1 Loading BATCH

After you bootstrap the RT-11 system and enter the date and time, you must make the BATCH run-time handler resident by typing the RT-11 LOAD command as follows:

·LOAD BA:

You detach and unload the BATCH run-time handler with the /U option in the BATCH compiler command line (see Section A.7.2).

## NOTE

If BATCH crashes, you must unload BATCH with the UNLOAD command and then reload BATCH with the LOAD command. This ensures that the BATCH handler is properly initialized when you rerun BATCH.

You must make the BATCH log device and list device resident unless the log or list device is SY:, or unless it is a device for which the handler is already resident. Load the log device, using the following syntax:

.LOAD log-device

where:

log-device represents the device to which BATCH must write the log file

For example:

• LOAD LP:

You can, of course, load device handlers with a single LOAD command. For example:

\- LOAD BA:,LP:

You must then assign the logical device name LOG to the log device. Use the RT-11 monitor ASSIGN command in the form:

.ASSIGN log-device LOG

For example, if LP: is the log device, type:

```txt
• ASSIGN LP LOG
```

Then assign the logical device name LST: using the RT-11 ASSIGN command in the form:

.ASSIGN list-device LST

where:

list-device represents the physical device BATCH must use for listings

If, for example, you want to produce listings on the line printer, type:

• ASSIGN LP LST

## NOTE

Do not use the DEASSIGN command with no arguments in a BATCH program since it deassigns the log and list devices, possibly causing the BATCH job to terminate.

You must also make resident the BATCH run-time handler input device (compiler output device). If this device is already resident or is SY:, you do not need to load it. For example, to load the DECtape handler as the input device, type:

• LOAD DT

If the input file to the BATCH compiler is on cards, load the card reader handler by typing:

. LOAD CR

## NOTE

If input is on cards, you must use the RT-11 monitor SET command (before loading the handler) to specify CRLF and NOIMAGE modes. That is, the following command appends a carriage return/line feed combination to each card image.

SET CR CRLF

The following command translates the card by packing card code into ASCII data, one column per byte.

. SET CR NOIMAGE

If card images do not properly translate to ASCII, you may have to change the card translation codes by using one of the following commands:

. SET CR CODE = 29

or

, SET CR CODE=26

See Section 4.4.

## A.7.2 Running BATCH

When you have loaded all necessary handlers, run the BATCH compiler as follows:

.R BATCH

BATCH responds by printing an asterisk (\*) to indicate its readiness to accept commands. In response to the \*, type the output file specifications for the control file followed by an equals sign. Then type the input file specifications for the BATCH file as follows:

[[output-filespec][,log-filespec][/option...] = ]input-filespec[...,
input-filespec][/option...]

where:

output-filespec is the BATCH compiler output device and file the BATCH run-time handler must use. The device you specify must be random-access. Your BATCH job should not delete or move this file. Your BATCH job should avoid compressing the system volume with the SQUEEZE command or the DUP /S option. If you omit output-filespec, BATCH generates a file on the default device DK: with the same name as the first input file but with a .CTL file type. If you do not specify a file type in output-filespec, BATCH assumes .CTL.

is the log file created by the BATCH run-time handler. If you do not specify a log device, BATCH assumes LOG:. The device name you specify for log-filespec must be the same as you assign to LOG:.

You can change the size of a log file on a file-structured device from the default size of 64(decimal) blocks. To make this change, enclose the required size in square brackets. For example:

\* ,FILE.LOG[10]=FILE

The default file type for the log-filespec is .LOG.

represents an input file. If you do not specify a file type, BATCH assumes .BAT. If you specify a .CTL file, BATCH assumes a precompiled file that must be the only file in the input list.

is an option from the following list:

/N compiles but does not execute. This option creates a BATCH control file (.CTL), generates an ABORT JOB message at the beginning of the log file, and returns to the RT-11 monitor.

/T:n if n=0, sets the /NOTIME option as the default on the \$JOB command. If n=1, the default option on the \$JOB command is /TIME.

/U indicates that the BATCH compiler must detach the BATCH run-time handler from the RT-11 monitor and unload the handler.

## NOTE

You need not specify the RT-11 monitor UNLOAD BA command to remove the handler. Specifying /U to BATCH causes the handler to detach and unload.

/X indicates that the input is a precompiled BATCH program. Use this option when you do not specify the .CTL file type.

&lt;RET&gt; prints the version number of the BATCH compiler.

The following example calls BATCH to compile and execute three input files (PROG1.BAT, PROG2.BAT, PROG3.BAT) to generate on DK: the compiler output files, and to generate on LOG: a log file.

• R BATCH
\* PROG1.BAT,PROG2.BAT,PROG3.BAT

The following commands print the version number of BATCH, then compile and run SYBILD.BAT.

```txt
• R BATCH
* RET
BATCH V04.00A
* SYBILD
```

The following commands compile PROTO.BAT to create PROTO.CTL but do not run the compiled BATCH stream.

• R BATCH
\* PROTO/N

Type the following commands to unlink BA.SYS from the monitor and to unload it.

• R BATCH
\* / U

The following commands compile FILE.BAT from magtape to create FILE.CTL on RK1:. They execute the compiled file and create a log file named FILE.LOG (of size 20) on LOG:.

.R BATCH
\*RK1:FILE,FILE[20]=MT:FILE

The following commands execute a precompiled job called FILE.TST.

```txt
.R BATCH
*FILE.TST/X
```

The following commands execute a precompiled job called FILE.CTL.

\*R BATCH
\*FILE/X

. )

The following commands accept input from the card reader to create a file called TEMP.CTL. BATCH stores this file on DK: and executes it.

. R BATCH

\* CR :

The following commands accept input from the card reader to create a file called JOB.CTL. BATCH stores the file on DK: and executes it.

. R BATCH

\* JOB = CR :

## A.7.3 Communicating with BATCH Jobs

During the execution of a BATCH stream, BATCH can request the operator to service a peripheral device, to provide information, or to insert a command line into the BATCH stream. The operator does this by typing directives to the BATCH handler on the console terminal.

## NOTE

These directives are equivalent to the compiler output that BATCH generates in the .CTL file. The .CTL file is an ASCII file that you can list by using the PRINT or TYPE commands or by running PIP.

These directives have the form:

\dir

where:

## dir represents one of the directives listed in Table A-6

To use these directives, the operator must get control of the BATCH runtime handler. This can be achieved through a /WAIT or a CTY in the BATCH stream, or by typing a carriage return on the console terminal. If a carriage return is typed, the operator does not know exactly where the BATCH stream has been interrupted. When BATCH executes a command, it acknowledges the carriage return and prints a carriage return/line feed combination at the terminal. The operator can then enter a directive from Table A-6. The most useful directives are marked with an asterisk (\*). Some directives are not particularly useful in this mode, but are listed to explain completely the BATCH compiler output.

In the following example, the operator must interrupt the BATCH handler to enter information from the console. As a result of a /WAIT or 'CTY' in the BATCH stream, the following message appears at the terminal:

\$MESSAGE/WAIT WRITE NECESSARY FILES TO DISK

Table A-6: Operator Directives to BATCH Run-Time Handler

| Directive | Function |
| --- | --- |
| \\@ | Sends the characters that follow to the console terminal. |
| *\\A | Changes the input source to be the console terminal. |
| *\\B | Changes the input source to be the BATCH stream. |
| *\\C | Sends the following characters to the log device. |
| *\\D | Considers the following characters as user data. |
| *\\E | Sends the following characters to the RT-11 monitor. |
| *\\F | Forces the output of the current log block. If this directive is followed by any characters other than another BATCH backslash (\\) directive, the BATCH job prints an error message and terminates. BATCH then returns control to the RT-11 monitor. |
| \\G | Gets characters from the console terminal until a carriage return is encountered. |
| \\Hn | Help function that changes the logging mode. n specifies the following:0 Log only .TTYOUT and .PRINT1 Log .TTYOUT, .PRINT, and .TTYIN2 Do not log .TTYOUT, .PRINT, and .TTYIN3 Log only .TTYIN |
| \\Ivxlabel1?label2?label3? | IF statement that causes conditional transfer, where v is a variable name in the range A-Z; x is a value for the signed 8-bit comparison (v-x); and label1, label2, label3 are 6-character labels to which control is transferred under certain conditions. (All labels must be six characters in length; if too short, pad with spaces.) If v-x is less than 0, control transfers to label1; if v-x is equal to 0, control goes to label2; if v-x is greater than 0, control goes to label3. The direction for the label search is indicated by ?; if ? is 0, the search begins at the beginning of this job; if ? is 1, the label search begins after the IF statement. |
| \\Jlabel? | Jump, unconditional transfer; where label is a 6-character label and ? is 0 or 1. (All labels must be six characters in length; if too short, pad with spaces.) If ?=0, label is a backward reference; if ? = 1, label is a forward reference. |
| \\Kv0 | Increment variable v, where v is a variable name in the range A-Z. |
| \\Kvln | Stores the 8-bit number n in variable v. |
| \\Kv2 | Takes the value in variable v and returns it to the program (via .TTYIN). |
| \\Llabel | Inserts label as a 6-character alphanumeric string in the BATCH stream. (All labels must be six characters in length; if too short, pad with spaces.) Labels must not include backslash characters. Characters beyond six are ignored. |

To divert BATCH stream input from the current file to the console terminal, the operator types \E, enters commands to the RT-11 monitor, then types \B. Control then returns to the BATCH stream. The following example illustrates this procedure.

```txt
.R BATCH
*NEXT
  WRITE NECESSARY FILES TO DISK
?\A\E

\ECOPY DT1:FILE.MAC RK:

  FILES COPIED:
DT1:FILE.MAC   TO RK:FILE.MAC
\E\F\B

2
END BATCH
```

The following BATCH program lets you make frequent edits to a file and list only the edits. First, create a BATCH program that assembles with a listing and link the file. This BATCH program, called COMPIL.BAT, contains:

```txt
$JOB/RT11
    TTYIO
    !WRITE TERMINAL I/O TO LOG FILE
,R MACRO
    !CALL THE MACRO ASSEMBLER
*FILE,FILE/C=FILE
$MESSAGE/WAIT OK TO TYPE EDIT COMMANDS
,R LINK
    !CALL THE RT-11 LINKER
*FILE,LOG:=FILE
$EOJ
```

At run time, you can insert commands into the BATCH stream from the console terminal. These commands search for the section of the listing file that has been edited, then list this section to the log. You must insert the command after the R MACRO command but before the R LINK command. The following example illustrates this procedure.

```asm
.R BATCH
*COMPIL
OK TO TYPE EDIT COMMANDS
?\A\E

\ER EDIT

*ERFILE.LST\$
*EWFILE.SEC\$
*PRETRY: \$=J\$
*\L\$
RETRY: 0                      ;HIGH ORDER BIT USED FOR "RESET IN PROGRESS FLAG
49 000020 016705 177764                 MOV     RKCQE,R5          ;GET Q P
50 000024 011502                   MOV     @R5,R2           ;R2 = BL
51 000026 016504 000002                 MOV     2(R5),R4         ;R4 = UN
52 000032 006204                   ASR    R4             ;ISOLATE
```

## A.7.4 Terminating BATCH

When BATCH terminates normally, it prints the following message and returns control to the RT-11 monitor:

END BATCH

To abort BATCH while it is executing a BATCH stream, interrupt the BATCH handler by typing a carriage return. When BATCH executes the next command after the carriage return, it prints a carriage return/line feed combination at the console terminal. You then gain control of the system. Type \F followed by a carriage return. The BATCH handler responds with the FE (forced exit) error message and writes the remainder of the log buffer. Control returns to the RT-11 monitor.

Typing two CTRL/Cs terminates BATCH immediately. Use two CTRL/Cs when BATCH is in a loop or when a long assembly is running. In these cases, BATCH responds slowly to your carriage return interrupt.

## A.8 Differences Between RT-11 BATCH and RSX-11D BATCH

Some programmers run their RT-11 BATCH programs under RSX-11D. Note the differences between the two BATCH implementations listed in Table A-7. BATCH programs that run under both systems must be compatible with both RT-11 and RSX-11D BATCH.

Table A-7: Differences Between RT-11 and RSX-11D BATCH

<table><tr><td>Characteristic</td><td>RT-11</td><td>RSX-11D</td></tr><tr><td>File descriptors</td><td>filespec/option</td><td>SY:filnam.typ/option</td></tr><tr><td>Default listing file type</td><td>.LST(or .LIS)</td><td>.LIS</td></tr><tr><td>Executable file type</td><td>.SAV</td><td>.EXE</td></tr><tr><td rowspan="6">Incompatible commands</td><td>$BASIC</td><td rowspan="6">$MCR</td></tr><tr><td>$CALL</td></tr><tr><td>$CHAIN</td></tr><tr><td>$LIBRARY</td></tr><tr><td>$RT11</td></tr><tr><td>$SEQUENCE</td></tr><tr><td rowspan="24">Incompatible options</td><td>$COPY/DELETE</td><td></td></tr><tr><td>$CREATE/DOLLARS</td><td></td></tr><tr><td>$CREATE/LIST</td><td></td></tr><tr><td>$DATA/DOLLARS</td><td></td></tr><tr><td>$DATA/LIST</td><td></td></tr><tr><td>$DIR file/LIST</td><td>$DIR file/DIRECTORY</td></tr><tr><td>$DISMOUNT/WAIT</td><td></td></tr><tr><td>$DISMOUNT lun:/LOGICAL</td><td></td></tr><tr><td>$FORTRAN/DOLLARS</td><td></td></tr><tr><td>$FORTRAN/MAP</td><td></td></tr><tr><td>$JOB/BANNER</td><td>$JOB/NAME</td></tr><tr><td>$JOB/LIST</td><td>$JOB/LIMIT</td></tr><tr><td>$JOB/RT11</td><td>$JOB/MCR</td></tr><tr><td>$JOB/TIME</td><td></td></tr><tr><td>$JOB/UNIQUE</td><td></td></tr><tr><td>$LINK/LIBRARY</td><td>$LINK/MCR</td></tr><tr><td>$LINK/OBJECT</td><td></td></tr><tr><td>$MACRO/CREF</td><td></td></tr><tr><td>$MACRO/DOLLARS</td><td></td></tr><tr><td>$MACRO/LIBRARY</td><td></td></tr><tr><td>$MACRO/MAP</td><td></td></tr><tr><td>$MESSAGE/WAIT</td><td></td></tr><tr><td>$MESSAGE/WRITE</td><td></td></tr><tr><td>$PRINT/DELETE</td><td></td></tr><tr><td>$DATA input</td><td>Appears as if from input</td><td>Appears as if from a file named FOR001.DAT</td></tr><tr><td>Logical device names</td><td>In $MOUNT and $DISMOUNT</td><td>Logical unit numbers only</td></tr><tr><td>$RUN</td><td>You must specify file name</td><td>RSX11DBAT.EXE is default</td></tr></table>
