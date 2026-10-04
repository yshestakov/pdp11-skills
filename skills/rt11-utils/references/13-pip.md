# RT-11 System Utilities Manual: Ch.13 PIP peripheral interchange: copy, rename, delete, protect, dates, ASCII/image/binary modes, wildcards

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 13.1 Calling and Terminating PIP
- 13.2 PIP Command String Syntax
- 13.3 Using Wildcards with PIP
- 13.4 Options
- 13.4.1 Operations Involving Magtape (/M:n)
- 13.4.2 Copy Operations
- 13.4.3 Date Option (/C[:date])
- 13.4.4 Delete Option (/D)
- 13.4.5 Wait Option (/E)
- 13.4.6 Protection Option (/F)
- 13.4.7 Ignore Errors Option (/G)
- 13.4.8 Verify Option (/H)
- 13.4.9 Since Option (/I[:date])
- 13.4.10 Before Option (/J[:date])
- 13.4.11 Copies Option (/K:n)
- 13.4.12 No Replace Option (/N)
- 13.4.13 Predelete Option (/O)
- 13.4.14 Exclude Option (/P)
- 13.4.15 Query Option (/Q)
- 13.4.16 Rename Operation (/R)
- 13.4.17 Single-Block Transfer Option (/S)
- 13.4.18 Set Date Option (/T[:date])
- 13.4.19 Concatenate Option (/U)
- 13.4.20 Multivolume Option (V)
- 13.4.21 Logging Option (/W)
- 13.4.22 Information Option (/X)
- 13.4.23 System Files Option (/Y)
- 13.4.24 No Protection Option (/Z)

---

# Chapter 13 Peripheral Interchange Program (PIP)

The peripheral interchange program (PIP) is a file transfer and file maintenance utility program. You can use PIP to transfer files between any of the RT-11 devices (listed in Table 3-1 of the RT-11 System User's Guide) and to merge, rename, delete, and change the protection status of files.

## 13.1 Calling and Terminating PIP

To call PIP from the system device, respond to the keyboard monitor prompt (.) by typing:

, R PIP RET

The Command String Interpreter (CSI) prints an asterisk at the left margin of the terminal and waits for you to type a command string. If you enter only a carriage return at this point, PIP prints its current version number and prompts you again for a command string. You can type CTRL/C to halt PIP and return control to the monitor when PIP is waiting for input from the console terminal. You must type two CTRL/Cs to abort PIP at any other time. To restart PIP, type R\_PIP or REENTER followed by a carriage return in response to the monitor's dot.

## 13.2 PIP Command String Syntax

Chapter 1, Command String Interpreter, describes the general syntax of the command line PIP accepts. You can type as many as six input file names, but only one output file name is allowed. Some of the PIP options accept a date as an argument. The syntax for specifying the date is:

[:dd.][:mmm][:yy.]

where:

dd, represents the day (a decimal integer in the range 1–31)

mmm represents the first three characters of the name of the month

yy. represents the year (a decimal integer in the range 73–99)

The default value for the date is the current system date. If you omit any of the date values (dd, mmm, or yy), the system uses the values from the current system date. For example, if you specify only the year ::82. and the current system date is May 4, 1983, the system uses the date 4.:MAY:82.. If the current date is not set, it is considered 0 (the same as for an undated file in a directory listing).

On random-access devices such as disks, and in transfers from magtape, PIP operations retain a file's creation date. If the file's creation date is 0, PIP gives it the current system date. However, in transfers to magtape, PIP always gives files the current system date.

If you have selected timer support through the system generation process, but have not selected automatic end-of-month date advancement, make sure that you set the date at the beginning of each month with the DATE command. If you fail to set the date at the beginning of each month, the system prints -BAD- in the creation date column of each file created beyond the end-of-month. (Note that you can eliminate -BAD- by using the RENAME/SETDATE command after you set the date.)

If you specify a command involving random-access devices for which the output specification is the same as the input specification, PIP does not move any files. However, it can change the creation dates on the files if you use /T, it can rename the files if you use /R, it can protect files if you use /F, or it can remove protection from files if you use /Z.

Because PIP performs file transfers for all RT-11 data formats (ASCII, object, and image), it does not assume file types for either input or output files. You must explicitly specify all file types where file types are applicable.

## 13.3 Using Wildcards with PIP

You can use all variations of the wildcard construction for the input file specifications in the PIP command line (Section 4.2 of the RT-11 System User's Guide describes wildcard usage). Output file specifications cannot contain embedded wildcards. If you use any wild character in an input file specification, the corresponding output file name or file type must be an asterisk. (The concatenate copy operation is an exception to this rule because it does not allow wildcards in the output specification.) The following example shows wildcard usage:

\* \* . B = A % B . MAC

In this example, the embedded percent character (%) represents any single, valid file name character. In the output file specification, the asterisk represents any valid file name.

The following command deletes all files with the file type .BAK (regardless of their file names) from device DK:.

\* \*.BAK/D

The next command renames all files with a .BAK file type (regardless of file names) so that these files now have a .TST file type (maintaining the same file names).

\* \* , TST = \* , BAK / R

In most cases, PIP performs operations on files in the order in which they appear in the device directory. In transfers from magtape (and for all other transfers requested on the same command line), PIP performs operations on files in the order in which they appear on the volume. When you use wild-cards in the input file types, PIP ignores system files with the file type .SYS unless you also use the /Y option. PIP prints the error message ?PIP-W-No .SYS action if you omit the /Y option on a command that would operate on .SYS files.

## NOTE

You cannot perform any operations that result in deleting a protected file. For example, you cannot transfer a file to a volume if a protected file with the same name already exists on the output volume.

PIP ignores all files with the file type .BAD unless you explicitly specify both the file name and file type in the command string. PIP does not print a warning message when it does not include .BAD files in an operation.

This example transfers all files, including system files (regardless of file name or file type) from device DK: to device DL1:. It does not transfer .BAD files.

\* DL1: \*, \*/Y=\*, \*

## 13.4 Options

PIP options, summarized in Table 13–1, permit you to perform various operations with PIP. If you do not specify an option, PIP assumes that the operation is a file transfer in image mode. You can put command options at the end of the command string or type them after any file name in the string. Operations involving magtape are an exception, because the /M option is device-dependent and has a different meaning when you specify it on the input or output side of a command line. Type any number of options in a command line, as long as only one operation (copy, delete, or rename) is represented. You can, however, combine copy and delete operations on one line. Also, the protect and noprotect options can be combined with copy and rename operations.

Table 13-1: PIP Options

| Option | Section | Function |
| --- | --- | --- |
| /A | 13.4.2.2 | Copies files in ASCII mode, ignoring and discarding nulls and rubouts. It converts input file to 7-bit ASCII and treats CTRL/Z (32 octal) as the logical end-of-file on input (the default copy mode is image). |
| /B | 13.4.2.3 | Copies files in formatted binary mode (the default copy mode is image). |
| /C[:date] | 13.4.3 | Used with other options to include only files with the specified date in the operation. If you use /C and do not specify a date, PIP includes only files with the current date in the specified operation.. |
| /D | 13.4.4 | Deletes input files from a specific device. Note that PIP does not automatically query before it performs the operation. If you combine /D with a copy operation, PIP performs the delete operation after the copy completes. This option is invalid in an input specification with magtape. |
| /E | 13.4.5 | Transfers files in a single- or small-disk system. PIP initiates the transfer, but pauses and waits for you to mount the volumes involved in the transfer. |
| /F | 13.4.6 | Protects files from deletion. Gives protected status to output files during a copy operation so you cannot delete them. If you use neither /F nor /Z, the output files retain the protection status of the input files. Can also be used with /R. Invalid for magtapes. |
| /G | 13.4.7 | Ignores any input errors that occur during a file transfer and continues copying. |
| /H | 13.4.8 | Verifies that the output file matches the input file after a copy operation. Cannot be used with /A or /B. |
| /I[:date] | 13.4.9 | Used with other options to include only files created on or after the specified date. |
| /J[:date] | 13.4.10 | Used with other options to include only files created before the specified date. |
| /K:n | 13.4.11 | Makes n copies of the output files to any sequential device, such as LP:, TT:, or PC:. |
| /M:n | 13.4.1 | Used when I/O transfers involve magtape. |
| /N | 13.4.12 | Does not copy or rename a file if a file with the same name exists on the output device. This option protects you from accidentally deleting a file. It is invalid for magtape in the output specification. |
| /O | 13.4.13 | Deletes a file on the output device if you copy a file with the same name to that device. The delete operation occurs before the copy operation. This option is invalid for magtape in the output specification. |
| /P | 13.4.14 | Copies or deletes all files except those you specify. |
| /Q | 13.4.15 | Use only with another operation. The /Q option causes PIP to print the name of each file to be included in the operation you specify. You must respond with a Y to include a particular file. |
| /R | 13.4.16 | Renames the file you specify. This operation is invalid for magtape. |
| /S | 13.4.17 | Copies files one block at a time. |
| /T[:date] | 13.4.18 | Puts the specified date on all files involved in the operation. This option is invalid when copying to magtape; operations involving magtape devices always use the current date. |
| /U | 13.4.19 | Copies and concatenates all files you specify. |
| /V | 13.4.20 | Copies files from one input volume to two or more smaller output volumes. |
| /W | 13.4.21 | Prints on the terminal a log of all files involved in the operation. |
| /X | 13.4.22 | Causes PIP to print an information message instead of a fatal message when it cannot find a file you specified in the command line. |
| /Y | 13.4.23 | Includes .SYS files in the operation you specify. You cannot modify or delete these files unless you use the /Y option when you use wildcards in the input file types. |
| /Z | 13.4.24 | Removes protected status from output files so you can delete them. If you use neither /F nor /Z, the output files retain the protection status of the input files. When used with /R, enables files for deletion if they have been previously protected with /F. Invalid for magtapes. |

## 13.4.1 Operations Involving Magtape (/M:n)

PIP handles magtape, which is a sequential-access device, differently from random-access devices, such as disks, diskettes, and DECtape II. On magtape, files are stored serially, one after another, and there is no directory at the beginning of each device that lists the files and gives their location. Thus, you can access only one file at a time on each sequential-access device unit. Avoid commands that specify the same device unit number for both the input and output files — they are invalid.

The /M:n option makes operations that involve magtape more efficient. This option lets you specify different tape handling procedures for PIP to follow. The following sections outline the operations that involve magtape and describe the different procedures for using these devices that you can specify with the /M:n option. Remember that when you use the /M:n option, n is interpreted as an octal number. You must use n. (n followed by a decimal point) to represent a decimal number.

Magnetic tape is a convenient auxiliary storage medium for large amounts of data, and is often used as backup for disks. Reflective strips indicate the beginning and end of the tape. A special label (an EOF1 or EOV1 tape label) followed by two tape marks indicates the end of current data and also where new data can begin.

The following PIP options are valid for use with magtape: /A, /B, /C[:date], /F, /G, /H, /I, /J, /M, /P, /Q, /S, /U, /V (only when magtape is the output volume), /W, /X, /Y, and /Z. These options are invalid with magtape: /E, /K, /R, /T, and /V (when magtape is the input volume). The /M:n option lets you direct the tape operation; you can move the tape and perform an operation at the point you specify. Note that /D is invalid for input from magtape; /N and /O are invalid for output to magtape.

The /M:n option can be different for the output and input side of the command line. Since the option applies to the device and not to the files, you can specify one /M:n option for the output file and one for each input file.

Sometimes PIP begins an operation at the current position. To determine the current position, the magtape handler backspaces from its present position on the tape until it finds either an EOF indicator or the beginning of tape (BOT), whichever comes first. PIP then begins the operation with the file that immediately follows the EOF or BOT. The magtape handler also has a special procedure for locating a file with sequence number n:

1. If the file sequence number is greater than the current position, PIP searches the tape in the forward direction.

2. If the file sequence number is more than one file before the current position, or if the file sequence number is less than five files from BOT, the tape rewinds before PIP begins its search.

3. If the file sequence number is at the current position, or if it is one file past the current position, PIP searches the tape in the reverse direction.

Whenever you fetch or load a new copy of the magtape handler, the tape position information is lost. The new handler searches backward until it locates either BOT or a label from which it can learn the position of the tape. It then operates normally, according to steps 1, 2, and 3 described above.

If you omit the /M:n option, the tape rewinds between each operation. Using /M:0 has the same effect as omitting /M:n. When n is positive, it represents the file sequence number. When n is negative, it represents an instruction to the magtape handler.

In copying from magtapes, /M:n functions as follows:

## 1. If n is 0:

The tape rewinds and PIP searches for the file you specify. If you specify more than one file, the tape rewinds before each search. If the file specification contains a wildcard, the tape rewinds only once and then PIP copies all the appropriate files.

## 2. If $n$ is a positive integer:

PIP goes to file sequence number n. If the file it finds there is the one you specified, PIP copies it. Otherwise, PIP prints the ?PIP-F-File not found DEV:FILNAM.TYP message. If you use a wildcard in the file specification, PIP goes to file sequence number n and then begins to search for matching files.

## 3. If n is -1:

PIP starts the search at the current position. If the current position is not the beginning of the tape, PIP may not find the file you specify, even though it does exist on the tape.

In writing to magtapes, /M:n functions as follows:

## 1. If n is 0:

The tape rewinds before PIP copies each file. PIP prints a warning message if it finds a file with the same name and file type as the input file and does not perform the copy operation.

## 2. If $n$ is a positive integer:

PIP goes to the file sequence number n and enters the file you specify. If PIP reaches logical end-of-tape (LEOT) before it finds file sequence number n, it prints the ?PIP-F-File sequence number not found message. If you specify more than one file or if you use a wildcard in the file specification, the tape does not rewind before PIP writes each file, and PIP does not check for duplicate file names.

## 3. If n is -1:

PIP goes to the LEOT and enters the file you specify. It does not rewind, and it does not check for duplicate file names.

## 4. If n is -2:

The tape rewinds between each copy operation. PIP enters the file at LEOT or at the first occurrence of a duplicate file name.

If PIP reaches the physical end-of-tape before it completes a copy operation, it cannot continue the file on another tape volume. Instead, it deletes the partial file by backspacing and writing a logical end-of-tape over the file's header label. You must restart the operation and use another magtape.

If you type consecutive CTRL/Cs during any output operation to magtape, PIP does not write a logical end-of-tape at the end of the data. Consequently, you cannot transfer any more data to the tape unless you follow one of the following recovery procedures.

1. Transfer all good files from the interrupted tape to another tape and initialize the interrupted tape in the following manner:

```txt
*     dev1:*,*=devO:*,*
-     CTRL/C
,     R DUP
*     devO:/Z/Y
```

2. Determine the sequential number of the file that was interrupted and use the /M:n construction to enter a replacement file (either a new file or a dummy) over the interrupted file. PIP writes the replacement file and a good LEOT after it. The following example assumes the bad file is the fourth file on the tape:

\*devo:file,new/M:4=file.dum

## 13.4.2 Copy Operations

PIP copies files in image, ASCII, and binary format. Other options let you change the date on the files, access .SYS files, combine files, change a file's protection status, and perform other similar operations. PIP automatically allocates the correct amount of space for new files in copy operations. For block-replaceable devices, PIP stores the new file in the first empty space large enough to accommodate it. If an error occurs during a copy operation, PIP prints a warning message, stops the copy operation, and prompts you for another command. You cannot copy .BAD files unless you specifically type each file name and file type.

13.4.2.1 Image Mode – If you enter a command line without an option, PIP copies files onto the destination device in image mode. Note that you cannot reliably transfer memory image files to the line printer or console terminal. PIP can image-copy ASCII and binary data but it does not do any of the data checking described in Section 13.4.2.3.

The following command makes a copy of the file named XYZ.SAV on device DK: and assigns it the name ABC.SAV. (Both files exist on device DK: after the operation.)

\* ABC, SAV = XYZ, SAV

The next example copies from DK: all .MAC files whose names are three characters long and begin with A. PIP stores the resulting files on DY1:.

\* DY1: \*, \*=A%%.MAC

13.4.2.2 ASCII Mode (/A) — Use the /A option to copy files in 7-bit ASCII mode. PIP ignores and eliminates nulls and rubouts during file transfer. PIP treats CTRL/Z (32 octal) as logical end-of-file if it encounters that character in the input file. You cannot use the /A option with the /V option.

The following command copies F2.FOR from device DK: onto device DY1: in ASCII mode and assigns it the name F1.FOR.

\* DY1:F1.FOR=F2.FOR/A

13.4.2.3 Binary Mode (/B) — Use the /B option to transfer formatted binary files (such as .OBJ files produced by the assembler or the FORTRAN compiler and .LDA files produced by the linker). You cannot use the /B option with the /V option.

The following command transfers a formatted binary file from device DL0: to device DK: and assigns it the name FILE.OBJ.

\*DK: FILE.OBJ=DL:/B

When performing formatted binary transfers, PIP prints a warning if a checksum error occurs. If there is a checksum error and you did not use /G to ignore the error, PIP does not perform the copy operation. You cannot copy library files with the /B option. Copy library files in image mode.

## 13.4.3 Date Option (/C[:date])

The /C[:date] option includes only those files with the specified date. If no date is specified only those files with the current date are included. Specify /C only once in the command line; it applies to all the file specifications in the entire command.

The following command copies (in ASCII mode) all files with the file type .MAC on DL0: that also have the date January 12, 1983. It also copies the file RDWR.MAC, if it has the date January 12, 1983, from DY0: to DY1:. It combines all these files under the name NN3.MAC on DY1:.

\*DY1:NN3.MAC=DLO:\*.MAC/C:12.:JAN:83.,DYO:RDWR.MAC/A/U

The next command copies all files with the current date (except .SYS and .BAD files) from DK: to DY1:. This is an efficient way to back up all new files after a session at the computer.

\* DY1:\*,\*=\*,\*/C

## 13.4.4 Delete Option (/D)

Use the /D option to delete one or more files from the device you specify. Note that PIP does not query you before it performs this operation unless you use /Q. Remember to use the /Y option to delete .SYS files if you use wildcards in the input file types. You cannot delete .BAD files, unless you name each one specifically, including file name and file type. You can specify only six files in a delete operation unless you use wildcards. You must always indicate a file specification in the command line. A delete command consisting only of a device name (dev:/D) is invalid. The delete option is also invalid for magtape.

The following examples illustrate the delete operation.

\* FILE1,SAV/D

The command shown above deletes FILE1.SAV from device DK:.

```csv
* DY1:*,*/D
?PIP-W-No .SYS action
*
```

The command shown above deletes all files from device DY1: except those with a .SYS or .BAD file type. Since there is a file with a .SYS file type, PIP prints a warning message to remind you that this file has not been deleted.

\* \*.MAC/D

This command deletes all files with a .MAC file type from device DK:.

## 13.4.5 Wait Option (/E)

If you have a single-disk system or a diskette system, you will find the /E option useful for copy operations. Use this option when you need to change storage volumes during a copy procedure. The general format of the command line follows.

filespec/E = filespec

You can use any option with /E that is valid with your RT-11 configuration. You cannot use wildcards as input. When you use /E, make sure that PIP is on your system volume.

When you use the /E option, PIP guides you through a series of steps in the process of completing the file transfer. PIP initiates execution of the command, but then pauses and prints the message Mount input volume in &lt;device&gt;; Continue?, where &lt;device&gt; represents the device into which you mount the input volume. At this time you can remove the system volume (if necessary) and mount the volume on which you actually want the operation to take place.

When the new volume is loaded, type Y or any string beginning with Y followed by a carriage return to execute the operation. If you type N or any string beginning with N, or CTRL/C, the operation is not completed. Instead PIP prompts you to remount the system volume if you have removed it and the monitor prompt (.) appears. Any other response causes the message to repeat.

If you type Y, PIP prompts you for the input volume, if any. When the operation completes the Mount system volume in &lt;device&gt;; Continue? message prints. Replace the system device and type Y or any string beginning with Y followed by a carriage return. If you type any other response, PIP prompts you to mount the system volume until you type Y. When you type Y, the asterisk (\*) prompt prints, and PIP waits for you to enter another command.

The sections that follow describe the procedures for single-drive and double-drive transfer.

13.4.5.1 Single-Drive Operation — If you want to transfer a file between two storage volumes, and you have only one drive for that type of storage volume, follow the procedure below.

1. Enter a command string according to this general syntax:

$^{*}$ output-filespec/E = input-filespec

where output-filespec represents the destination device and file specification, and input-filespec represents the source device and file specification.

2. PIP responds by printing the following message at the terminal.

```txt
Mount input volume in <device>; Continue?
```

where &lt;device&gt; represents the device into which you are to mount your input volume. Type Y or any string beginning with Y followed by a carriage return after you have mounted your input volume. If you type any string beginning with N or if you type CTRL/C, the operation is not performed and the monitor prompt (.) appears. If you have removed the system volume, PIP prompts you to remount it.

3. PIP continues the copy procedure and prints the following message on the terminal:

```txt
Mount output volume in <device>; Continue?
```

After you have removed your input volume from the device, mount your output volume and type Y or any string beginning with Y followed by a carriage return. If you type any string beginning with N or if you type CTRL/C, the operation is not performed and the monitor prompt (.) appears. If you have removed the system volume, PIP prompts you to remount it.

4. Depending on the size of the file, PIP may repeat the transfer cycle (steps 2 and 3) several times before the transfer is complete. When the transfer is complete, PIP prints the following message if you had to remove the system volume from &lt;device&gt;:

```txt
Mount system volume in <device>; Continue?
```

When you remount the system volume and type Y or any string beginning with Y followed by a carriage return in response to the last instruction, you complete the copy operation. If you type anything other than Y, PIP continues to prompt you to remount the system volume until you type Y.

13.4.5.2 Double-Drive Operation – You can use the /E option for transferring files between two nonsystem volumes. The procedure for transferring files this way follows.

1. With your system volume mounted, enter a command string according to the following general syntax:

```txt
output-filespec/E = input-filespec
```

where output-filespec represents the destination device and file specification, and input-filespec represents the source device and file specification.

2. After you have entered the command string, PIP responds with the message:

```txt
Mount input volume in <device>; Continue?
```

Type Y or any string beginning with Y followed by a carriage return when you have mounted the input volume. If you type any string beginning with N or if you type CTRL/C, the operation is not performed and the monitor prompt (.) appears. If you have removed the system volume, PIP prompts you to remount it.

## 3. PIP then prints:

```txt
Mount output volume in <device>; Continue?
```

Type Y or any string beginning with Y followed by a carriage return after you have mounted the output volume. If you type any string beginning with N or if you type CTRL/C, the operation is not performed and the monitor prompt (.) appears. If you have removed the system volume, PIP prompts you to remount it.

4. Unlike the single-volume transfer, the double-volume transfer involves only one cycle of mounting the input and output volumes. When the file transfer is complete, PIP prints the following message if you had to remove the system volume from &lt;device&gt;:

```txt
Mount system volume in <device>; Continue?
```

When you type Y or any string beginning with Y followed by a carriage return in response to the last instruction, you complete the copy operation. If you type anything other than Y, PIP continues to prompt you to mount the system volume until you type Y.

## 13.4.6 Protection Option (/F)

Use the /F option to protect files. The letter P next to the block size number in the file's directory entry indicates the file is protected.

If a file is protected you cannot perform any operations on it that result in deleting the file. You can copy a protected file to another volume or change its name. However, you cannot change its protected status unless you use the /Z (no protection) option. Note that the contents of a protected file are not protected; that is, although you cannot delete a protected file, you can change or delete its contents.

You can also use the /F option during copy operations to protect the output file, and with /R to change a file's protection status. If during a copy operation you use neither /F nor /Z, the output files retain the protection status of the input files.

The following command protects all files with the file type .MAC on DK:.

```csv
* *,MAC/F
```

The following command copies all files with file type .ORI from DL0: to DL1:. The resulting output files on DL1: are protected from deletion.

```txt
* DL1:*, *=DLO:*,ORI/F
```

If you use the /F option with a file that is already protected, no operation is performed on that file regardless of any other options in the command string. For example, the following command requests PIP to protect the file DY1:CALCAB.MAC and change its creation date to April 21, 1983. However, because the file is already protected, PIP performs neither operation.

```lisp
* DL1:CALCAB.MAC/F/T:21.:APR:83.
```

## 13.4.7 Ignore Errors Option (/G)

The /G option copies files, but ignores all input errors. This option forces a single-block transfer, which you can invoke at any other time with the /S option. Use the /G option if an input error occurred when you tried to perform a normal copy operation. The procedure can sometimes recover a file that is otherwise unreadable. If an error still occurs, PIP prints the ?PIP-W-Input error DEV:FILNAM.TYP message and continues the copy operation.

The following command, copies the file TOP.SAV in image mode from device DY1: to device DK: and assigns it the name ABC.SAV.

```txt
* ABC, SAV=DY1:TOP, SAV/G
```

The next command copies files F1.MAC and F2.MAC in ASCII mode from device DY0: to device DY1:. This command creates one file with the name COMB.MAC, and ignores any errors that occur during the operation.

\* DY1:COMB.MAC=DY0:F1.MAC,F2.MAC/A/G/U

## 13.4.8 Verify Option (/H)

Use the /H option to verify that the output file matches the input file when a copy operation is performed. If the two files are different a message is printed on the terminal. This option cannot be used with /A or /B.

The following command verifies that the output file A.BAK on DY1: is the same as the input file A.MAC on DY0:.

```txt
* DY1:A.BAK=DYO:A.MAC/H
```

## 13.4.9 Since Option (/I[:date])

The /I[:date] option includes only those files created on or after the specified date. If no date is specified, PIP uses the current date.

The following command copies from DK: only those .MAC files created on or after January 4, 1983:

```javascript
* DLO:*,MAC=*,MAC/I:4.:JAN:83,
```

## 13.4.10 Before Option (/J[:date])

The /J[:date] option includes only those files created before the specified date. If you do not specify a date, PIP uses the current date.

The following command copies only those .MAC files created before January 14, 1983:

```txt
* DLO:*.MAC=*.MAC/J:14.:JAN:83.
```

## 13.4.11 Copies Option (/K:n)

The /K:n option directs PIP to generate n copies of the file you specify. The only valid output devices are the console terminal and the line printer. Normally, each copy of the file begins at the top of a page; copies are separated by form feeds.

```txt
* LP := STOTLE, LST/K : 3
```

This command, for example, prints three copies of the listing file, STOTLE.LST, on the line printer.

## 13.4.12 No Replace Option (/N)

The /N option prevents execution of a copy or rename operation if a file with the same name as the output file already exists on the output device. This option is not valid when output is to magtape.

The following example uses the /N option.

```txt
* DYO:CT.SYS=DK:CT.SYS/Y/N
?PIP-W-Output file found, no operation Performed DK:CT.SYS
*
```

The file named CT.SYS already exists on DY0:, and the copy operation does not proceed.

## 13.4.13 Predelete Option (/O)

The /O option deletes a file on the output device if you copy a file with the same name to that device. PIP deletes the file on the output device before the copy operation occurs. Normally, PIP deletes a file of the same name after the copy completes. This option is not valid when output is to magtape.

The following example uses the /O option.

```txt
* DL1:TEST1.MAC=DY1:TEST.MAC/O
```

If a file named TEST1.MAC already exists on DL1:, PIP deletes it before copying TEST.MAC from DY1: to TEST1.MAC on DL1:.

## 13.4.14 Exclude Option (/P)

The /P option directs PIP to include all files in the operation except the ones you specify. Note that if you want to include system (.SYS) files and you use the /P option, you must always use the /Y option with it.

```txt
* DYO:*, *=DY1:*.MAC/P
```

This command directs PIP to transfer all files from DY1: to DY0: except the .MAC files. The .SYS files will also be excluded from the operation because the /Y option was not specified.

## 13.4.15 Query Option (/Q)

Use the /Q option with another PIP operation to list all files and to request confirmation for each file before it is included. Typing Y or any string beginning with Y followed by a carriage return causes the named file to be processed; typing anything else excludes the file.

The following example deletes four files from DY1:.

```txt
* DY1:*,*/D/Q
  Files deleted:
DY1:FIX463.SAV?
DY1:GRAPH.BAK ? Y
DY1:DMPX.MAC ?
DY1:MATCH.BAS ?
DY1:EXAMP.FOR ?
DY1:GRAPH.FOR ? Y
DY1:GLOBAL.MAC? Y
DY1:PROSEC.MAC? Y
DY1:KB.MAC ?
-DY1:EXAMP.MAC ?
*
```

## 13.4.16 Rename Operation (/R)

Use the /R option to rename a file you specify as input, giving it the name you specify in the output specification. The input and output volumes for a rename operation must be the same. PIP prints an error message if the command specifications are not valid. Use the /Y option if you rename .SYS files and you use wildcards in the input file types. You cannot use /R with magtape.

The following examples illustrate the rename operation.

```txt
* DY1:F1.MAC=DY1:FO.MAC/R
```

The command shown above renames F0.MAC to F1.MAC on device DY1:.

\* DL1:OUT, SYS=DL1:CT, SYS/R

This command renames file CT.SYS to OUT.SYS.

The rename command is particularly useful when a file contains bad blocks. By giving the file a .BAD file type, you can ensure that the file permanently resides in that area of the device. Thus, the system makes no other attempts to use the bad area. Once you give a file a .BAD file type, you cannot move it during a compress operation. You cannot rename .BAD files unless you specifically indicate both the file name and file type.

## 13.4.17 Single-Block Transfer Option (/S)

The /S option directs PIP to copy files one block at a time. On some devices, this operation increases the chances of an error-free transfer. You can combine the /S option with other PIP copy options. For example:

\* DL1:TEST.MAC=DLO:TEST.MAC/S

PIP performs this transfer one block at a time.

## 13.4.18 Set Date Option (/T[:date])

This option causes PIP to put the specified date on all files involved in the operation. If you specify no date, PIP uses the current system date. Normally, PIP preserves the existing file creation date on copy and rename operations. This option is invalid when copying to magtape, because PIP always uses the current date for these operations.

The following command copies all the files with file type .COM copied from DY0: to DY1:, and assigns the output files the date January 24, 1983.

\* DY1: \*, \*=DYO: \*, COM/Y/T:24, :JAN:83.

## 13.4.19 Concatenate Option (/U)

To combine more than one file into a single file, use the /U option. This option is particularly useful when you want to combine several object modules into a single file for use by the linker or librarian. PIP does not accept wildcards on the output specification. Use the /B option with /U if you are concatenating object (.OBJ) files.

The following examples show the /U option.

\* DK: AA, OBJ = DY1: BB, OBJ, CC, OBJ, DD, OBJ/U/B

The command shown above transfers files BB.OBJ, CC.OBJ, and DD.OBJ to device DK: as one file and assigns it the name AA.OBJ.

```txt
* DL1:MERGE.MAC=DLO:FILE2.MAC,FILE3.MAC/A/U
```

This command merges ASCII files FILE2.MAC and FILE3.MAC on DL0: into one ASCII file named MERGE.MAC on device DL1:.

## 13.4.20 Multivolume Option (V)

The /V option copies files from an input volume to two or more smaller output volumes. This option is useful when you are copying several files from a large input volume and you are not sure whether all the files will fit on one output volume.

When you use this option PIP copies files to the output volume until the system finds a file that will not fit. PIP continues to search that file's directory segment, copying all files from the segment that will fit onto the output volume. When no more files from that segment will fit on the output volume, PIP prompts you to mount the next output volume and prints the Continue? message. Mount another output volume of the same type and type Y or any string beginning with Y followed by a carriage return to continue the copy operation. If you type any string beginning with N or if you type CTRL/C, the operation is aborted and the monitor prompt (.) appears.

When you type Y to continue, PIP copies the first file that would not fit to the previous output volume to the new output volume. PIP continues to copy files from that directory segment until no more files from that segment will fit on the output volume or until all files from that directory segment have been copied. If all files from that segment have been copied, PIP begins copying files from the next directory segment. File copying continues in this fashion until all the specified input files have been copied.

The following example copies all files on DL0: to several double-density diskettes:

```txt
*    DYO:*,*=DLO:*,*/V
Mount next output volume in DYO:; Continue?      Y
Mount next output volume in DYO:; Continue?      Y
Mount next output volume in DYO:; Continue?      Y
*
```

## 13.4.21 Logging Option (/W)

When you use the /W option, PIP prints a list of all files included in the operation. The /W option is useful if you do not want to take the time to use the query mode (the /Q option, described in Section 13.4.15), but you do want a list of the files operated on by PIP.

PIP prints the log for an operation on the terminal under the command line. This example shows logging with the delete operation.

```txt
* DY1:*,*/D/W
?PIP-W-No ,SYS action
  Files deleted:
DY1:TEST.MAC
DY1:FIX463.SAV
DY1:GRAPH.BAK
DY1:DMPX.MAC
DY1:MATCH.BAS
DY1:EXAMP.FOR
DY1:GRAPH.FOR
DY1:GLOBAL.MAC
DY1:PROSEC.MAC
DY1:EXAMP.MAC
*
```

## 13.4.22 Information Option (/X)

The /X option causes PIP to print an information message when PIP fails to find all of the files you specify in a command line. If you do not use the /X option, PIP prints a fatal error message when it is unable to find an input file, and control returns to the keyboard monitor after the operation completes. Use /X in indirect command files to ensure that processing will continue even if PIP fails to find a file you specify.

In the following example, the input files FILE1.TXT and FILE3.TXT are copied to DL1:. However, since the system is unable to find DL0:FILE2.TXT, PIP prints a message to inform you.

\* DL1:\*,\*=DLO:FILE1.TXT,FILE2.TXT,FILE3.TXT
?PIP-I-File not found DLO:FILE2.TXT

## 13.4.23 System Files Option (/Y)

Use the /Y option if you need to perform an operation on system (.SYS) files and you use wildcards in the input file type. For example:

```txt
* * , * = D Y 1 : * , * / Y
```

This command copies to device DK:, in image mode, all files (including .SYS files) from device DY1:. Note that you must always use /Y with the /P option to include .SYS files, even when you use no wildcards.

## 13.4.24 No Protection Option (/Z)

Use the /Z option to remove protected status from files, so that you can delete or change those files. You can also use the /Z option with /R to change the protection status of a file, and during copy operations to remove protection from the output file.

Note that since you cannot delete files assigned as logical disks, you cannot use the /Z option to remove protection from these files.

The following command removes protection from all .MAC files on DK:.

\*\*,MAC/Z

The following command copies the file PROGRAM.MAC from DY0: to DY1:. The resulting output file on DY1: is enabled for deletion.

\*DY1:PROGRAM.MAC=DYO:PROGRAM.MAC/Z

If you use the /R option with a file that is already unprotected, no operation is performed on that file regardless of any other options in the command string. For example, the following command requests PIP to unprotect the file DY1:CALCAB.MAC and change its creation date to April 21, 1983. However, because the file is already unprotected, PIP performs neither operation.

\*DL1:CALCAB.MAC/R/T:21.:APR:83.

(1)
