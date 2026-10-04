# RT-11 System Utilities Manual: Overview (chapter summary), Ch.1 Command String Interpreter: CSI syntax output=input/options, defaults, wildcards, options with values, invoking utilities with R/RUN

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 1.1 CSI Syntax
- 1.2 Prompting Characters

---

- A-5 BATCH Commands .A-12
- A-6 Operator Directives to BATCH Run-Time Handler .A-49
- A-7 Differences Between RT-11 and RSX-11D BATCH .A-51
- B-1 System Program/Monitor Command Equivalents .B-1

(1)

## Preface

This manual describes how to use the RT-11 system utilities. You can use the RT-11 system utilities instead of the keyboard monitor commands described in the RT-11 System User's Guide to perform program development, program execution, and file maintenance.

The manual is written for you if you are already familiar with computer software fundamentals and have some experience using RT-11 and RT-11 keyboard monitor commands. If you have no RT-11 experience, you should first read the Introduction to RT-11 and the RT-11 System User's Guide before consulting this manual. If you have experience with an earlier release of RT-11 (this is Version 5), you should read the RT-11 System Release Notes to learn how RT-11 Version 5 differs from earlier versions. If you are interested in more sophisticated programming techniques or in system programming, you should read this manual first and then proceed to the RT-11 Programmer's Reference Manual and the RT-11 Software Support Manual.

The next section, Chapter Summary, briefly describes the chapters in this manual and suggests a reading path to help you use the manual efficiently.

## Chapter Summary

Part I, Utility Programs, Chapters 1–15, describes the Command String Interpreter (CSI) and many utility programs provided with the RT-11 system. These programs include:

BINCOM Binary file comparison program

BUP Backup utility program

DIR Directory program

DUMP Dump program

DUP Device utility program

FILEX File exchange program

FORMAT Volume formatting program

LD Logical disk subsetting program

LIBR Librarian program

LINK Linker program

Part II, System Jobs, Chapters 16–19, describes four utilities that run under the foreground/background (FB) or extended memory (XM) monitor as foreground or system jobs: the Error Logger, the Queue Package, the transparent spooler (SPOOL) package, and the communication package (VTCOM). To run them as system jobs, you must enable system job support through the system generation process. The Error Logger also runs under the single-job (SJ) monitor.

Part III, Debugging and Altering Programs, Chapters 20–23, describes the four utility programs that permit you to examine and change assembled programs and source files. These utilities are:

ODT On-line debugging technique

PAT Object module patch program

SIPP Save image patch program

SLP Source language patch program

Appendix A describes BATCH processing. Appendix B contains a summary of the system utility programs and their keyboard monitor command equivalents.

## Documentation Conventions

A description of the symbolic conventions used throughout this manual follows. Familiarize yourself with these conventions before you continue reading.

1. Wherever possible, examples appear as if they are computer output. What you should type appears in red

2. This manual uses the symbol RET to represent a carriage return, LF to represent a line feed, SP for a space, and TAB to represent a tab. Unless the manual indicates otherwise, terminate all commands or command strings with a carriage return.

3. Terminal and console terminal are general terms used throughout all RT-11 documentation to represent any terminal device, including DECwriters and video terminals.

4. To produce certain characters in system commands, you must type a letter key while pressing the control CTRL/ key. For example, while holding down the CTRL key, type C to produce the CTRL/C character. Key combinations of this type are documented as CTRL/C, CTRL/O, and so on.

5. In discussions of command syntax, uppercase letters represent the command name, which you must type. Lowercase letters represent a variable, for which you must supply a value.

Square brackets ([ ]) enclose options; you may include the item in brackets, or you may omit it, as you choose.

The ellipsis symbol (...) represents repetition. You can repeat the item that precedes the ellipsis.

This is a typical illustration of command syntax:

This example shows that you must run the utility program PIP as shown, and enter file specifications and options of your choice (none are required) on the line that follows. The first file specification represents the output file, and the second represents the input file. Here is a typical command string:

• R PIP
\* DL1:MYFIL.BAK=DLO:MYFIL.MAC/A/J

}

## Part I Utility Programs

Part I of this manual presents, in alphabetical order, most of the utility programs available with RT-11. You can take advantage of nearly all of the capabilities of RT-11 by using the keyboard commands (described in Chapter 4 of the RT-11 System User's Guide), but it is the utility programs that actually perform many of the system's functions. For example, when you issue the CREATE command, the utility program DUP performs the create operation.

This part of the manual explains how to carry out utility operations, those not performed directly by the monitor, by running a specific utility program instead of using the keyboard monitor commands. It is not necessary to have an understanding of the material contained in Part I of this manual in order to use the RT-11 system. However, the information in this part may be of interest to you if you have experience with a previous version of RT-11, or if you are a systems programmer and need to perform certain functions with the utility programs that are not available with the keyboard monitor commands.

Note that the syntax required by the Command String Interpreter for input and output specifications is different from the syntax you use to issue a keyboard monitor command. Chapter 1, Command String Interpreter, describes the general syntax of the command string that the system utility programs accept, and explains certain conventions and restrictions. Read this chapter carefully before you use any of the system utility programs directly, and bear in mind that there are many differences between issuing a keyboard command and running a utility program. Chapters 2 through 15 describe the system utility programs themselves.

# Chapter 1 Command String Interpreter (CSI)

The Command String Interpreter (CSI) is the part of RT-11 that accepts a line of ASCII input, usually from the console terminal, and interprets it as a string of input specifications, output specifications, and options for use by a utility program.

To call a utility program, respond to the dot (.) printed by the keyboard monitor by typing R followed by a program name and a carriage return. This example shows how to call the directory program (DIR):

\* R DIR RET

The CSI prints an asterisk (\*) at the left margin of the terminal, indicating that it is ready to accept a list of specifications and options. The following section describes the syntax of the specifications and options you can enter.

You can use the single-line editor, described in Section 4.3 of the RT-11 System User's Guide, to edit CSI command strings and terminal input as well as keyboard monitor commands.

## 1.1 CSI Syntax

Once you have started a system program, you must enter the appropriate information before any operation can be performed. You type a specification string with the following general syntax in response to the prompting asterisk:

output-filespecs/options = input-filespecs/options

A few system programs — BINCOM, for example — require you to enter this information differently. Complete instructions are provided in the appropriate chapters.

In all cases, the syntax for output-filespecs is:

dev:filnam.typ[n],...dev:filnam.typ[n]

The syntax for input-filespecs is:

dev:filnam.typ,...dev:filnam.typ

The syntax for /option is:

/o[:oval]

/o[:dval].

where:

dev: represents either a logical device name or one of the physical device names from Table 3-1 in the RT-11 System User's Guide.

If you do not supply a device name, the system uses device DK:. DK:, or whatever device you specify for the first file in a list of input or output files, applies to all the files in that input or output list until you supply a different device name. For example:

\* DY1:FIRST,OBJ,LP:=TASK.1,DL1:TASK.2,TASK.3

This command is interpreted as follows:

\*DY1:FIRST.OBJ,LP:=DK:TASK.1,DL1:TASK.2,DL1:TASK.3

File FIRST.OBJ is stored on device DY1:. File TASK.1 is stored on default device DK:. Files TASK.2 and TASK.3 are stored on device DL1:. Notice that file TASK.1 is on device DK:. It is the first file in the input file list and the system uses the default device DK:. Device DY1: applies only to the file on the output side of the command.

## filnam.typ

is the name of a file (consisting of one to six alphanumeric characters followed optionally by a period and a zero- to three-character file type). No spaces or tabs are allowed in the file name or file type. As many as three output and six input files are allowed. If you omit the dot and the file type, the system may apply a default file type that the program specifies.

is an optional declaration of the number of blocks you need for an output file; n is a decimal number (up to 65,535) enclosed in square brackets immediately following the output filnam.typ to which it applies.

oval] is one or more options whose functions vary according to the program you are using (refer to the option table in the appropriate chapter). The variable oval is either an octal number or one to three alphanumeric characters (the first of which must be alphabetic) that the program converts to Radix-50 characters. The variable dval. is a decimal number followed by a decimal point. You can use a minus sign (-) to denote negative octal or decimal numbers.

This manual uses the /o:oval construction throughout, except for the keyboard monitor commands, where all values are interpreted as decimal (unless indicated otherwise) and the decimal point after a value is not necessary. However, the /o:dval. format is always valid. Generally, these options and their associated values, if any, should follow the device and file name to which they apply.

If the same option is to be repeated several times with different values (for example, /L:MEB/L:TTM/L:CND) you can abbreviate the line as /L:MEB:TTM:CND. You can mix octal, Radix-50, and decimal values.

is a delimiter that separates the output and input fields. You can use the < sign in place of the = sign. You can omit this separator entirely if there are no output files.

## NOTE

Except where noted, all numeric values you supply to the CSI must be in octal.

Concise Command Language (CCL) also uses CSI syntax. See Section 4.7 of the RT-11 System User's Guide for information on using CCL.

## 1.2 Prompting Characters

Table 1–1 summarizes the characters RT–11 prints either to indicate that the system is waiting for your response or to specify which job (foreground, system, or background) is producing output.

Table 1-1: Prompting Characters

| Character | Explanation |
| --- | --- |
| . (dot) | The keyboard monitor is waiting for a command. |
| ^ | When the console terminal is being used as an input file, the circumflex prompts you to enter information from the keyboard. Typing a CTRL/Z marks the end-of-file. See Section 3.6 of the RT-11 System User's Guide for details on special function keys. |
| > | If a foreground or system job is active, the > character identifies which job, foreground, system, or background, is producing the output that currently appears on the console terminal. Each time output from the background job is to appear, B> prints first, followed by the output. If the foreground job is to print output, F> prints first. If a system job is to print output, jobname> appears first, where jobname represents the name of the system job. |
| * | The current system utility program is waiting for a line of specifications and options. |

(1)
