# RT-11 System Utilities Manual: Ch.2 BINCOM binary file comparison

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 2.1 Calling and Terminating BINCOM
- 2.2 BINCOM Command String Syntax
- 2.3 Using Wildcards with BINCOM
- 2.4 Options
- 2.5 Output Format
- 2.6 Examples
- 2.7 Creating a SIPP Command File

---

# Chapter 2

# Binary File Comparison Program (BINCOM)

The RT-11 binary comparison program (BINCOM) compares two volumes or binary files and lists the differences between them. BINCOM can either print the results at the terminal or line printer, or store them in a file. BINCOM is particularly useful when you need to compare two executable programs, because it provides a quick way of telling whether two data files are identical. Another use of BINCOM is to verify whether two versions of a program produce identical output files when given identical input files.

BINCOM examines the two input files word by word (or byte by byte), looking for differences. When BINCOM finds a mismatch, it prints the block number and offset within the block at which the difference occurs, the octal values from each input file, and the logical exclusive OR of the two values. This last number helps you find the bits that are different in the two values.

You can also use BINCOM to create an indirect command file that invokes the save image patch program (SIPP, described in Chapter 22) to patch one version of a file so that it matches another version. Section 2.6 describes the procedure you can use to create an indirect command file for SIPP.

## 2.1 Calling and Terminating BINCOM

To call BINCOM from the system device, respond to the dot (.) printed by the keyboard monitor by typing:

: R BINCOM RET

The Command String Interpreter (CSI) prints an asterisk at the left margin of the terminal and waits for you to enter a command string. If you respond to the asterisk by entering only a carriage return, BINCOM prints its current version number. You can type a CTRL/C to halt BINCOM and return control to the monitor when BINCOM is waiting for input from the console terminal. You must type two CTRL/Cs to abort BINCOM at any other time. To restart BINCOM, type R BINCOM or REENTER and a carriage return in response to the monitor's dot.

## 2.2 BINCOM Command String Syntax

BINCOM accepts command strings with the following syntax:

[output-spec[/option]][,patch-spec[/option]] = old-filespec,
new-filespec[/option...]

where:

output-spec represents the file or volume to which you want the differences between the two files or volumes you are comparing sent. If omitted, the default is TT:.

patch-spec represents the file that you can run as an indirect command file; it will contain the commands necessary to patch old-filespec so it matches new-filespec.

old-filespec represents the first file to be compared.

new-filespec represents the second file to be compared.

option is one or more of the options listed in Table 2-1.

The console terminal is the default output device. There is no default file type for input files; you must always specify the file type. BINCOM assigns .DIF as the default file type for the difference output file, and .COM as the default file type for the SIPP indirect command file.

## 2.3 Using Wildcards with BINCOM

You can use wildcards to perform multiple binary file comparisons by typing only one command line. However, you can use wildcards only to compare files; you cannot use wildcards when creating a SIPP indirect command file.

You can use wildcards in either input file specification (old-filespec or new-filespec). A different type of comparison is performed depending on whether you use wildcards in only one or in both of the input file specifications.

If you use wildcards in only one of the input file specifications, BINCOM compares the file you specify without any wildcards to all variations of the file specification that contains wildcards. The wildcards represent the part of the file specification to be varied. You can use this method to compare one particular file to several other files. For example, when the following command line is executed, BINCOM compares the file TEST1.SAV on device DY0: to all files on device DY1: with the filename TEST2:

\* TEST=DYO:TEST1.SAV,DY1:TEST2,\*

You can send the results of all the comparisons to a file on a volume rather than to the console by specifying an output file. In the last example, all differences from the comparisons are sent to the file TEST.DIF on device DK:.

If you use wildcards in both input file specifications, the wildcards represent a part of the file specifications that you want to be the same in both files being compared. You can use this method to compare several pairs of files; each input file specification is compared to only one other input file specification. For example, when the following command line is executed, BINCOM compares pairs of files; the first input file in each pair has the file name PROG1, and the second has the file name PROG2. The file type of both files in each pair must match.

```txt
* DYO:PROG1.*,DY1:PROG2.*
```

BINCOM searches for the first file on DY0: with the file name PROG1, and takes note of its file type. Then, BINCOM searches DY1: for a file with the file name PROG2 and the same file type as PROG1. If a match is found, BINCOM compares the two files and lists the differences on the console (or sends the differences to an output file if one is specified). BINCOM then searches DY0: for more files with the file name PROG1 and DY1: for PROG2 files with matching file types.

## 2.4 Options

Table 2-1 summarizes the options that you can use with BINCOM. Except for the /O option, you can place these options anywhere in the command string, but it is conventional to place them at the end of the command string.

Table 2-1: BINCOM Options

| Option | Function |
| --- | --- |
| /B | Compares the input files byte by byte. If you do not specify this option, BINCOM compares the files word by word. |
| /D | Compares two entire volumes starting with block 0. If one volume is longer, BINCOM prints a message and compares the volumes up to the point where the shorter volume ends and the longer one continues. Invalid when creating a SIPP command file. |
| /E:n | Ends comparison at block n, where n is an octal value. If you do not include this option, BINCOM ends the comparison when it reaches end-of-file on one of the input files, or end-of-device on one of the input devices. |
| /H | Types on the console terminal the list of available options. |
| /O | Creates an output file or patch file, even if there are no differences between the two input files. If you enter this option after the differences output file, BINCOM creates the differences output file whether or not there are differences between the two input files:If you enter this option after the SIPP indirect command file, BINCOM creates a SIPP indirect command file whether or not differences exist. You can enter this option at the end of the command line if you want both output files.This option is useful in BATCH streams to prevent later job steps from failing because BINCOM did not create the expected control file. |

(Continued on next page)

Table 2-1: BINCOM Options (Cont.)

| Option | Function |
| --- | --- |
| /Q | Suppresses the printing of the differences and prints only the message ?BINCOM-W-Files are different or ?BINCOM-W-Devices are different if applicable (or ?BINCOM-I-No differences found). This option is useful in BATCH control files when you want to test for differences and perhaps abort execution, but do not want the log file filled with output. |
| /S:n | Starts the comparison at block n, where n is an octal value. |

## 2.5 Output Format

This section describes the BINCOM output file format and explains how to interpret it.

If you include an output file specification in the command line, BINCOM creates a file that contains the differences between the two input files or devices. If you do not specify an output file, BINCOM prints the differences only on the terminal. If you include the /Q option, BINCOM does not print the differences and does not create an output file.

The first line of the difference listing is a header line that identifies the files or devices you are comparing. Next, BINCOM prints a blank line and then lists the differences between the two files or devices. Each difference line has the following format:

bbbbbb ooo/ fffff f ssssss xxxxxx

where:

bbbbbb is the octal number of the block that contains the difference

ooo is the octal offset within the block

ffffff is the value in the first file or device

ssssss is the value in the second file or device

xxxxxx is the logical exclusive OR of the two values

If there are several differences in a block, BINCOM prints the block number only once for that block. Thus, each time you see a block number appear, it indicates that the differences being printed are in a new block.

If you specify the /B option to compare byte by byte, BINCOM prints ffffff, ssssss, and xxxxxx as three-digit, octal byte values.

When BINCOM reaches the end of one of the input files or devices, it checks its position in the other. If the files or devices have different lengths, BINCOM prints the message:

?BINCOM-W-File is longer DEV:FILNAM.TYP

```txt
or
?BINCOM-W-Device is longer DEV:
```

BINCOM prints the following message on the terminal if it encountered any differences:

```txt
?BINCOM-W-Files are different
```

```txt
?BINCOM-W-Devices are different
```

If the two files or devices are identical up to that point, BINCOM prints this message:

```txt
?BINCOM-I-No differences found
```

If you include a SIPP indirect command file specification in the command line, BINCOM creates a file that is a valid command file for the save image patch program (see Chapter 22). This command file contains commands that instruct SIPP to patch the first input file so that it matches the second input file. If you want BINCOM to create only the patch file, enter a comma before the patch file specification in the command line, in place of the output file specification.

## 2.6 Examples

The first example compares files TEST1.TST and TEST3.TST, both on device DK:. Notice that there are no output files and no options in the command line.

```txt
* R BINCOM
* TEST1.TST.TEST3.TST
BINCOM comparing/DK:TEST1.TST - DK:TEST3.TST
000000 002/ 051511 051502 000013
?BINCOM-W-Files are different
```

Notice the fourth line in the above example. The third number, 051511, represents the contents of location 2, block 0, in file TEST1.TST. The fourth number, 051502, represents the contents of the same location in file TEST3.TST. The last number is the logical exclusive OR of the two values.

The next example specifies the output file FOO1 as the file in which to store the differences between TEST1.TST and TEST3.TST.

```txt
• R BINCOM
* F001=TEST1.TST,TEST3.TST
?BINCOM-W-Files are different
```

The contents of file FOO1 from the last example follow. Note that FOO1 has the default file type .DIF.

```txt
• TYPE F001.DIF
BINCOM comparing/DK:TEST1.TST - DK:TEST3.TST
000000 002/ 051511 051502 000013
```

## 2.7 Creating a SIPP Command File

You can use BINCOM to create an indirect command file that invokes the save image patch program (SIPP, described in Chapter 20) to patch one version of a file you are comparing to match the other version. As noted earlier in this chapter, you specify this indirect file as the second output file in the CSI command string. If you wish to create only the indirect file as output, place a comma before the output file specification in the command line, in place of the first output file specification.

The example that follows specifies FOO2 as the patch output file, which will contain the commands necessary to patch file TEST1.TST so it matches TEST3.TST. Notice the comma that appears before the patch file specification. This indicates that a difference output file is not requested, resulting in the printing of all the differences at the terminal when the command is executed.

```csv
• R BINCOM
* ,F002=TEST1.TST,TEST3.TST
BINCOM comparing/DK:TEST1.TST - DK:TEST3.TST
000000 002/ 051511 051502 000013
?BINCOM-W-Files are different
```

The contents of file FOO2 follow. Note that BINCOM assigns to this file the .COM file type.

```csv
* TYPE F002.COM
R SIPP
DK:TEST1.TST/A
000000
000000002
051502
^Y
^C
```

The file FOO2 from the previous example can be run as an indirect command file to make TEST1.TST match TEST3.TST. This can be done with the following command, when typed in response to the keyboard monitor dot:

@F002.COM
