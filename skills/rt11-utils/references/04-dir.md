# RT-11 System Utilities Manual: Ch.4 DIR directory program: listing formats, sorting, options

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 4.1 Calling and Terminating DIR
- 4.2 Directory Command String Syntax
- 4.3 Reading Directory Listings
- 4.4 Options
- 4.4.1 Alphabetical Option (/A)
- 4.4.2 Block Number Option (/B)
- 4.4.3 Columns Option (/C[:n])
- 4.4.4 Date Option (/D[:date])
- 4.4.5 Entire Option (/E)
- 4.4.6 Fast Option (/F)
- 4.4.7 Begin Option (/G)
- 4.4.8 Since Option (/J[:date])
- 4.4.9 Before Option (/K[:date])
- 4.4.10 Listing Option (/L)
- 4.4.11 Unused Areas Option (/M)
- 4.4.12 Summary Option (/N)
- 4.4.13 Octal Option (/O)
- 4.4.14 Exclude Option (/P)
- 4.4.15 Deleted Option (/Q)
- 4.4.16 Reverse Option (/R)
- 4.4.17 . Sort Option (/S[:xxx])
- 4.4.18 Protection Option (/T)
- 4.4.19 No Protection Option (/U)
- 4.4.20 Volume ID Option (/V[:ONL])

---

## Chapter 4 Directory Program (DIR)

The directory program (DIR) performs a wide range of directory listing operations. It can list directory information about a specific device, either in summarized form — where only the number of files stored per segment is given — or in more detailed form — where file names, file types, creation dates, and other file information is given. DIR can organize its listings in several ways, such as alphabetically or chronologically.

## 4.1 Calling and Terminating DIR

To call DIR from the system device, respond to the dot (.) printed by the keyboard monitor by typing:

. R DIR (RET)

The Command String Interpreter (CSI) prints an asterisk at the left margin of the terminal and waits for you to enter a command string. If you enter only a carriage return in response to the asterisk, DIR prints its current version number. You can type CTRL/C to halt DIR and return control to the monitor when DIR is waiting for input from the console terminal. You must type two CTRL/Cs to abort DIR at any other time. To restart DIR, type R DIR or REENTER in response to the monitor's dot.

## 4.2 Directory Command String Syntax

Chapter 1, Command String Interpreter, describes the general syntax of the command line that DIR accepts. Unless otherwise indicated, numeric arguments are interpreted as octal. Remember to put a decimal point after a decimal number to distinguish it from an octal number.

Some of the DIR options accept a date as an argument in the command line. The syntax for specifying the date is:

dd.:mmm:yy.

where:

dd. represents the day (a decimal integer in the range 1–31)

mmm represents the month (the first three characters of the name of the month)

yy. represents the year (a decimal integer in the range 73–99)

You can specify only one input device and one output device, but you can specify up to six file names on the input device. The default device for output is the terminal. The default file type for an output file is .DIR. The default device for input is DK:. If you omit the input specification completely, DIR uses DK:\*.\*. If you do not supply an option, DIR performs the /L operation. Note that wildcards are valid with DIR for the input specification only.

If you have selected timer support through the system generation process, but have not selected automatic end-of-month date advancement, make sure that you set the date at the beginning of each month with the DATE command. If you fail to set the date at the beginning of each month, DIR prints -BAD- in the creation date column of each file created beyond the end-of-month. (Note that you can eliminate a -BAD- entry by using the RENAME/SETDATE command after you have set the date.)

## 4.3 Reading Directory Listings

Directory listings normally print on the terminal in two columns. Read the entries across the columns, moving from left to right, one row at a time. Directory listings that are sorted, however, are an exception to this. (Sorted directories are produced by /A, /R, and /S options.) Read these listings by reading the left column from top to bottom, then reading the right column from top to bottom.

## 4.4 Options

You can perform many different directory operations by specifying options in the DIR command line. Table 4-1 summarizes the operations these options permit you to perform with DIR. The sections following the table describe the various DIR options and give examples; the options are arranged alphabetically in these sections.

## 4.4.1 Alphabetical Option (/A)

The /A option lists the directory of the device you specify in alphabetical order by file name and type. Note that /A sorts numbers after letters. It has the same effect as the /S:NAM option. The following example lists the directory of device DY0: in alphabetical order.

```txt
* DYO:/A
 14-Mar-83
BUILD .SAV 100 06-Sep-82 SWAP .SYS 25 05-Dec-82
DY .SYS 3 06-Sep-82 SYSMAC.MAC 41 19-Nov-82
MYPROG.MAC 36P 12-Oct-82 TM .MAC 25 27-Nov-82
RFUNCT.SYS 4 19-Nov-82 TT .SYS 2 19-Nov-82
RT11SJ.SYS 67 19-Nov-82 VTMAC .MAC 7 19-Nov-82
 10 Files, 30G Blocks
 180 Free Blocks
```

Table 4-1: DIR Options

| Option | Section | Operation |
| --- | --- | --- |
| /A | 4.4.1 | Lists the directory of the volume you specify in alphabetical order by file name and type (this is the same as /S:NAM). |
| /B | 4.4.2 | Lists the directory of the volume you specify, including file names and types, creation dates, starting block numbers, and the number of blocks in each file. For magtape, the starting block number is the file sequence number. Note that DIR lists block numbers in decimal, unless you use the /O option. |
| /C[:n] | 4.4.3 | Lists the directory in n columns; n is an integer in the range 1-9. The default value is two columns for normal listings and five columns for abbreviated listings. |
| /D[:date] | 4.4.4 | Lists a directory containing only those files having the date you specify. If you do not supply a date, DIR uses the system's current date. |
| /E | 4.4.5 | Adds unused spaces and their sizes to the listing of the volume directory. |
| /F | 4.4.6 | Prints a five-column, short directory (file names and types only) of the volume you specify. |
| /G | 4.4.7 | Lists the file you specify and all files that follow it in the directory. This option does not list any files that precede the file you specify. |
| /J[:date] | 4.4.8 | Prints a directory of the files created on or after the date you specify. If you do not supply a date, DIR uses the system's current date. |
| /K[:date] | 4.4.9 | Prints a directory of files created before the date you specify. If you do not supply a date, DIR uses the system's current date. |
| /L | 4.4.10 | Lists the directory of the volume you specify, including the number of files, their dates, and the number of blocks each file occupies. (This is the default operation.) |
| /M | 4.4.11 | Lists a directory of unused areas of the volume you specify. |
| /N | 4.4.12 | Lists a summary of the device directory. |
| /O | 4.4.13 | Similar to /L but lists the sizes and block numbers of the files in octal. |
| /P | 4.4.14 | Prints a directory of the volume you specify, excluding the files you list. |
| /Q | 4.4.15 | Lists a directory of the volume you specify, listing the file names and types, sizes, creation dates, and starting block numbers of files that have been deleted and whose file name information has not been destroyed. |
| /R | 4.4.16 | Lists the files in the reverse order of the sort specified with /A or /S. |
| /S[:xxx] | 4.4.17 | Lists the directory of the volume you specify in the order you specify; xxx indicates the order in which DIR sorts the listing (xxx can be DAT, NAM, POS, SIZ, or TYP). |

(Continued on next page)

Table 4-1: DIR Options (Cont.)

| Option | Section | Operation |
| --- | --- | --- |
| /T | 4.4.18 | Lists a directory of all files on the volume you specify that are protected against deletion. |
| /U | 4.4.19 | Lists a directory of all files on the volume you specify that are not protected against deletion. |
| /V[:ONL] | 4.4.20 | Lists the volume ID and owner name as part of the directory listing header. If you specify /V:ONL, DIR lists only the volume ID and owner name. |

## 4.4.2 Block Number Option (/B)

The /B option includes the starting block number in decimal of all the files listed in a directory of the volume you specify. The following example lists the directory of device DY0:, including the starting block numbers of files.

```txt
* DYO:/B
 14-Jan-83
FSM .MAC 31P 19-Nov-82 2955 BATCH .MAC 102P 19-Nov-82 2986
ELCOPY.MAC 8P 19-Nov-82 3088 ELINIT.MAC 15P 19-Nov-82 3096
ELTASK.MAC 15P 19-Nov-82 3111 ERROUT.MAC 48P 19-Nov-82 3126
ERRTXT.MAC 9P 19-Nov-82 3174 SYCND .BL 3P 19-Nov-82 3183
SYSTBL.BL 4P 19-Nov-82 3186 SYCND .DIS 5P 19-Nov-82 3190
SYSTBL.DIS 4P 19-Nov-82 3195 SYCND .HD 5P 19-Nov-82 3199
ABSLOD.SAV 48 15-MAR-82 3204 CHESS .SAV 40 17-Aus-82 3252
PETAL .SAV 36 11-Sep-82 3292 LAMP .SAV 29 16-Mar-82 3328
WUMPUS.SAV 30 16-Mar-82 3357
 17 Files, 348 Blocks
 138 Free blocks
```

## 4.4.3 Columns Option (/C[:n])

The /C[:n] option lists the directory in the number of columns you specify. The argument, n, represents an integer in the range 1–9. If you do not use the /C:n option, DIR lists the directory in two columns for normal listings and five columns for abbreviated listings. The following command, for example, lists the directory of device DY1: in one column.

```txt
* DY1:/C:1
 4-Jan-83
SWAP .SYS 25P 19-Nov-82
RT11SJ.SYS 67P 19-Nov-82
RT11FB.SYS 80P 19-Nov-82
RT11BL.SYS 64P 19-Nov-82
TT .SYS 2P 19-Nov-82
DT .SYS 3P 19-Nov-82
DP .SYS 3P 19-Nov-82
 7 Files, 244 Blocks
 242 Free blocks
```

## 4.4.4 Date Option (/D[:date])

The /D[:date] option includes in the directory listing only those files having the date you specify. The default date is the system's current date. For example, the following command lists all the files created on January 14, 1983.

```txt
* DYO:/D:14::JAN:83.
 15-Jan-83
RT11SJ.SYS      67P 14-Jan-83
RT11BL.SYS      63P 14-Jan-83
SWAP   .SYS      25P 14-Jan-83
DP       .SYS      3P 14-Jan-83
LP       .SYS      2P 14-Jan-83
DUP     .SAV      41 14-Jan-83
DIR     .SAV      17 14-Jan-83
EDIT    .SAV      19 14-Jan-83
SRCCOM.SAV      13 14-Jan-83
SLP     .SAV      9 14-Jan-83
 20 Files, 412 Blocks
 73 Free blocks
```

```powershell
RT11FB.SYS 80P 14-Jan-83
DX .SYS 3P 14-Jan-83
TT .SYS 2P 14-Jan-83
DY .SYS 4P 14-Jan-83
PIP .SAV 16 14-Jan-83
RESORC.SAV 15 14-Jan-83
RK .SYS 3 14-Jan-83
DD .SYS 5 14-Jan-83
BINCOM.SAV 11 14-Jan-83
SIPP .SAV 14 14-Jan-83
```

## 4.4.5 Entire Option (/E)

The /E option lists the entire directory including the unused areas and their sizes in blocks (decimal). Use it to find free space before you extend a file (with the monitor CREATE command or DUP /C option). The following example lists the entire directory of device DY1:, including unused areas.

```txt
* DY1:/E
 20-Mar-83
SWAP .SYS 25P 23-Oct-82
RT11FB.SYS 80P 19-Nov-82
TT .SYS 2P 19-Nov-82
DP .SYS 3P 23-Oct-82
DY .SYS 4P 19-Nov-82
RK .SYS 3P 19-Nov-82
DM .SYS 5P 23-Oct-82
DD .SYS 5P 23-Oct-82
LS .SYS 2P 19-Nov-82
MS .SYS 9P 27-Nov-82
DISMT1.COM 9P 27-Nov-82
NUMBER.PAS 1 11-Dec-82
NUM3 .LST 1 13-Dec-82
 25 Files, 322 Blocks
 164 Free blocks
```

```txt
RT11SJ.SYS 67P 23-Oct-82
RT11BL.SYS 64P 19-Nov-82
DT .SYS 3P 19-Nov-82
DX .SYS 3P 19-Nov-82
RF .SYS 3P 19-Nov-82
DL .SYS 4P 23-Oct-82
DS .SYS 3P 19-Nov-82
LP .SYS 2P 23-Oct-82
CR .SYS 3P 19-Nov-82
MTHD .SYS 3P 23-Oct-82
MMHD .SYS 4P 19-Nov-82
TONY .AGP 14 17-Aug-82
< UNUSED > 565
```

## 4.4.6 Fast Option (/F)

The /F option lists only file names and file types, omitting file lengths and associated dates. For example, the following command lists only file names and types from device DY0:.

```asm
*DYO:/F
 16-Aug-82
DY      .SYS    PIP     .SAV    DIR     .SAV    DUP     .SAV    SWAP   .SYS
RT11SJ.SYS    RT11FB.SYS    RT11BL.SYS    TT     .SYS    DT     .SYS
 10 Files, 312 Blocks
 174 Free blocks
```

| DIR | .SAV | 17 | 03-Aus-82 |
| --- | --- | --- | --- |
| EDIT | .SAV | 19 | 03-Aus-82 |
| DD | .SYS | 5 | 19-Aus-82 |
| BINCOM | .SAV | 11 | 05-Oct-82 |
| SIPP | .SAV | 14 | 05-Oct-82 |

## 4.4.7 Begin Option (/G)

The /G option lists the directory of the volume you specify, beginning with the file you specify and including all the files that follow it in the directory.

Usually, the disk you are using as a system device contains a number of files the operating system needs. These files include .SYS monitor files, .SAV utility program files, and various .OBJ, .MAC, and .BAK files. They are generally grouped together and usually listed at the beginning of a normal volume directory. Files that you create and use, such as source files and text files, are also generally grouped together and follow the operating system files in the directory. If you specify the name of the last system file with the /G in the command line, DIR prints a directory of only those files that you created and stored on the volume.

The following command, for example, lists the last system file (CT.SYS) and all the user files that follow it.

```txt
* DYO:CT.SYS/G
 10-Jan-83
CT     .SYS     5   10-Aug-82
RK      .SYS     3   13-Aug-82
STARTS.COM       1   27-Aug-82
SRCCOM.SAV    13   13-Aug-82
SLP     .SAV     9   13-Aug-82
 10 Files, 107 Blocks
 73 Free blocks
```

## 4.4.8 Since Option (/J[:date])

The /J[:date] option lists a directory of all files stored on the device you specify created on or after the date you supply. The default date is the system's current date. The following command lists all files on device DY0: created on or after January 20, 1983.

```txt
* DYO:/J:20.:JAN:83,
  20-Mar-83
RT11SJ.SYS      67P 28-Jan-83
RT11BL.SYS      63P 19-Feb-83
SWAP   .SYS     25P 02-Feb-83
SIPP   .SAV      14   02-Feb-83
  7 Files, 154 Blocks
  332 Free blocks
```

## 4.4.9 Before Option (/K[:date])

The /K[:date] option prints a directory of files created before the date you specify. The default date is the system's current date. The following command lists all files stored on device DY1: created before March 15, 1983.

```txt
* DY1:/K:15,:MAR:83.
20-Mar-83
FORTRA.SAV 191 14-Mar-83 BASIC .SAV 51 25-Feb-83
2 Files, 242 Blocks
38 Free blocks
```

## 4.4.10 Listing Option (/L)

The /L option lists the directory of the volume you specify. The listing contains the current date, all files and their associated creation dates, the number of blocks used by each file, total free blocks on the device (if disk), the number of files listed, and the total number of blocks used by the files. File lengths, number of blocks, and number of files are indicated as decimal values. For example, the following command lists on the line printer the directory for device DY1:.

```txt
* LP:=DY1:/L
```

The line printer output looks like this:

```txt
20-Nov-82
RT11SJ.SYS          67P 03-Jul-82
RT11BL.SYS          63P 15-Mar-82
SWAP     .SYS         25P 13-Aug-82
DP           .SYS         3P 13-Aug-82
LP           .SYS         2P 20-Nov-82
DUP     .SAV         41   26-Mar-82
EDIT     .SAV         19   13-Aug-82
SIPP     .SAV         14   13-Aug-82
15 Files, 413 Blocks
73 Free blocks
```

```txt
RT11FB.SYS 80P 13-Aug-82
DX .SYS 3P 13-Aug-82
TT .SYS 2P 13-Aug-82
DY .SYS 4P 13-Aug-82
PIP .SAV 16 25-Jul-82
RESORC.SAV 15 13-Aug-82
STARTS.COM 1 27-Aug-82
```

Note that if you specify no options in the command string, this is the default directory operation.

## 4.4.11 Unused Areas Option (/M)

The /M option lists only a directory of unused areas and their size on the volume you specify. For example, the following command lists all the unused areas on device DL0:.

```txt
* DLO:/M
 14-Dec-82
< UNUSED >      11                  < UNUSED >       2
< UNUSED >      26                  <UNUSED >       32
< UNUSED >      1                  <UNUSED >       525
<UNUSED >      0                  <UNUSED >       565
 0 Files, O Blocks
 1162 Free blocks
```

## 4.4.12 Summary Option (/N)

The /N option lists a summary of the volume directory. The summary lists the number of files in each directory segment and the number of segments in use on the volume you specify. The segments are listed in the order in which they are linked on the volume.

```asm
* DY1:_*,SAV/P
 29-Feb-83
RT11SJ.MAC     67P 06-Jan-83          RT11FB.MAC    80P 06-Jan-83
RT11BL.MAC     63P 06-Jan-83          DY   .MAC    3P 06-Jan-83
SWAP   .MAC     25P 06-Jan-83          TT   .MAC    2P 06-Jan-83
DP      .MAC     3P 06-Jan-83          DY   .MAC    4P 06-Jan-83
LP      .MAC     2P 06-Jan-83          RK   .MAC    3 06-Jan-83
STARTS.COM     1   27-Jan-83          DD   .MAC    5 06-Jan-83
 12 Files, 258 Blocks
 73 Free blocks
```

The following command lists the summary of the directory for device DK:.

```txt
* /N
14-Jan-83

  44 Files in segment 1

  46 Files in segment 4

  37 Files in segment 2

  34 Files in segment 5

  38 Files in segment 3

  16 Available segments, 5 in use

199 Files, 3647 Blocks
1115 Free blocks
```

## 4.4.13 Octal Option (/O)

The /O option is similar to the /L option, but lists the sizes (and starting block numbers if you use /B) of the files in octal. If the device you specify is a magnetic tape, DIR prints the sequence number in octal. For example, the following command lists the directory of device DY0:, with sizes in octal.

```asm
* DYO:/O
 14-Jan-83 Octal
MYPROG.MAC     44P 12-Nov-82      TM    .MAC     31   27-Nov-82
VTMAC .MAC     7   18-Oct-82      SYSMAC.MAC    51   19-Nov-82
SWAP .SYS     31   05-Sep-82      ANTON .MAC     4   19-Nov-82
RT11SJ.SYS    103   19-Nov-82      TT    .SYS     2   19-Nov-82
DX    .SYS     3   29-Aug-82      BUILD .MAC    144   19-Nov-82
 10 Files, 462 Blocks
 264 Free blocks
```

## 4.4.14 Exclude Option (/P)

The /P option lists a directory of all files on a volume, excluding those that you specify. You may specify up to six files.

This command lists all files on device DY1: except .SAV files.

| TM | .MAC | 25 | 27-Nov-82 |
| --- | --- | --- | --- |
| VTMAC | .MAC | 7 | 19-Nov-82 |
| RFUNCT | .SYS | 4 | 19-Nov-82 |
| DX | .SYS | 3 | 06-Sep-82 |
| TT | .SYS | 2 | 19-Nov-82 |

## 4.4.15 Deleted Option (/Q)

The /Q option lists a directory of the volume you specify, listing the file names, types, sizes, creation dates, and starting block numbers in decimal of files that have been deleted but whose file name information has not been destroyed. The file names that print represent either tentative files or files that have been deleted. This can be useful in recovering files that have been accidentally deleted. Once you identify the file name and location, you can use DUP to rename the area. See Section 6.3.1 for this procedure.

```txt
* DISK . DIR = /Q
```

This command creates a file called DISK.DIR on device DK: that contains directory information about unused areas from device DK:. Use the monitor TYPE command to read the file:

```asm
, TYPE DISK.DIR/LOG
  Files copied:
DK:DISK.DIR      to TT:
  12-Oct-82
EXAMPL.FOR     23   03-Sep-82  1403    MTHD  ,SMP     5   09-Sep-82 2895
SCOPE .PIC     3   22-Sep-82 2926
  O Files, O Blocks
  O Free blocks
```

## 4.4.16 Reverse Option (/R)

The /R option lists a directory in the reverse order of the sort you specify with the /A or /S option.

```asm
* DYO:/S:SIZ/R
 14-Jan-83
BUILD .MAC      100   06-Sep-82
RT11SJ.SYS       67   19-Nov-82
SYSMAC.MAC     41   19-Nov-82
MYPROG.MAC      36P 12-Oct-82
SWAP .SYS      25   05-Dec-82
 10 Files, 306 Blocks
 180 Free blocks
```

This command lists the directory of device DY0: in reverse file size order (from largest to smallest).

## 4.4.17 . Sort Option (/S[:xxx])

The /S[:xxx] option sorts the directory of the specified volume according to a three-character code you specify as :xxx. Table 4-2 summarizes the codes and their functions.

Table 4-2: Sort Codes

| Code | Function |
| --- | --- |
| DAT | Chronological by creation date. Files that have the same date are sorted alphabetically by file name and file type. |
| NAM | Alphabetical by file name. Files that have the same file name are sorted alphabetically by file type (this has the same effect as the /A option). |
| POS | According to the position of the files on the device. This is the same as using /S with no code. |
| SIZ | Based on file size (in blocks). Files that are the same size are sorted alphabetically by file name and file type. Files are sorted from smallest to largest unless you also use /R. |
| TYP | Alphabetical by file type. Files that have the same file type are sorted alphabetically by file name. |

## The following examples illustrate the /S option.

<table><tr><td colspan="6">* DYO:/S:DAT</td></tr><tr><td colspan="6">4-Feb-83</td></tr><tr><td>BUILD .MAC</td><td>100</td><td>06-Sep-82</td><td>SYSMAC.MAC</td><td>41</td><td>19-Nov-82</td></tr><tr><td>DY .SYS</td><td>3</td><td>06-Sep-82</td><td>TT .SYS</td><td>2</td><td>19-Nov-82</td></tr><tr><td>MYPROG.MAC</td><td>3GP</td><td>12-Oct-82</td><td>VTMAC .MAC</td><td>7</td><td>19-Nov-82</td></tr><tr><td>RFUNCT.MAC</td><td>4</td><td>19-Nov-82</td><td>TM .MAC</td><td>25</td><td>27-Nov-82</td></tr><tr><td>RT11SJ.SYS</td><td>67</td><td>19-Nov-82</td><td>SWAP .SYS</td><td>25</td><td>05-Dec-82</td></tr><tr><td colspan="6">10 Files, 30G Blocks</td></tr><tr><td colspan="6">180 Free blocks</td></tr><tr><td colspan="6">* DYO:/S:NAM</td></tr><tr><td colspan="6">4-Feb-83</td></tr><tr><td>BUILD .MAC</td><td>100</td><td>06-Sep-82</td><td>SWAP .SYS</td><td>25</td><td>05-Dec-82</td></tr><tr><td>DY .SYS</td><td>3</td><td>06-Sep-82</td><td>SYSMAC.MAC</td><td>41</td><td>19-Nov-82</td></tr><tr><td>MYPROG.MAC</td><td>3GP</td><td>12-Oct-82</td><td>TM .MAC</td><td>25</td><td>27-Nov-82</td></tr><tr><td>RFUNCT.SYS</td><td>4</td><td>19-Nov-82</td><td>TT .SYS</td><td>2</td><td>19-Nov-82</td></tr><tr><td>RT11SJ.SYS</td><td>67</td><td>19-Nov-82</td><td>VTMAC .MAC</td><td>7</td><td>19-Nov-82</td></tr><tr><td colspan="6">10 Files, 30G Blocks</td></tr><tr><td colspan="6">180 Free Blocks</td></tr><tr><td colspan="6">* DYO:/S:POS</td></tr><tr><td colspan="6">4-Feb-83</td></tr><tr><td>RT11SJ.SYS</td><td>67</td><td>19-Nov-82</td><td>BUILD .MAC</td><td>100</td><td>06-Sep-82</td></tr><tr><td>DY .SYS</td><td>3</td><td>06-Sep-82</td><td>SYSMAC.MAC</td><td>41</td><td>19-Nov-82</td></tr><tr><td>MYPROG.MAC</td><td>3GP</td><td>12-Oct-82</td><td>TM .MAC</td><td>25</td><td>27-Nov-82</td></tr><tr><td>SWAP .SYS</td><td>25</td><td>05-Dec-82</td><td>VTMAC .MAC</td><td>7</td><td>19-Nov-82</td></tr><tr><td>RFUNCT.SYS</td><td>4</td><td>19-Nov-82</td><td>TT .SYS</td><td>2</td><td>19-Nov-82</td></tr><tr><td colspan="6">10 Files, 30G Blocks</td></tr><tr><td colspan="6">180 Free blocks</td></tr><tr><td colspan="6">* DYO:/S:SIZ</td></tr><tr><td colspan="6">4-Jan-83</td></tr><tr><td>TT .SYS</td><td>2</td><td>19-Nov-82</td><td>TM .MAC</td><td>25</td><td>27-Nov-82</td></tr><tr><td>DY .SYS</td><td>3</td><td>06-Sep-82</td><td>MYPROG.MAC</td><td>3GP</td><td>12-Oct-82</td></tr><tr><td>RFUNCT.SYS</td><td>4</td><td>19-Nov-82</td><td>SYSMAC.MAC</td><td>41</td><td>19-Nov-82</td></tr><tr><td>VTMAC .MAC</td><td>7</td><td>19-Nov-82</td><td>RT11SJ.SYS</td><td>67</td><td>19-Nov-82</td></tr><tr><td>SWAP .SYS</td><td>25</td><td>05-Dec-82</td><td>BUILD .MAC</td><td>100</td><td>06-Sep-82</td></tr><tr><td colspan="6">10 Files, 30G Blocks</td></tr><tr><td colspan="6">180 Free blocks</td></tr></table>

```txt
* DYO:/S:TYP
14-Dec-82
BUILD .MAC 100 06-Sep-82 DY .SYS 3 06-Sep-82
MYPROG.MAC 36P 12-Oct-82 RFUNCT.SYS 4 19-Nov-82
.SYSMAC.MAC 41 19-Nov-82 RT11SJ.SYS 67 19-Nov-82
TM .MAC 25 27-Nov-82 SWAP .SYS 25 05-Dec-82
VTMAC .MAC 7 19-Nov-82 TT .SYS 2 19-Nov-82
.10 Files, 306 Blocks
180 Free blocks
```

## 4.4.18 Protection Option (/T)

The /T option includes in the directory listing only those files on the volume you specify that are protected against deletion. A letter P next to the block size number in the file's directory entry indicates that the file is protected. The following command lists only those files on DK: that are protected.

```txt
* DK:/S:SIZ/R/T
5-Jan-83
BUILD .MAC 100P 06-Sep-82 TM .MAC 25P 27-Nov-82
RT11SJ 67P 19-Nov-82 VTMAC .MAC 7P 19-Nov-82
SYSMAC.MAC 41P 19-Nov-82 RFUNCT.SYS 4P 19-Nov-82
MYPROG.MAC 36P 12-Oct-82 DX .SYS 3P 06-Sep-82
SWAP .SYS 25P 05-Dec-82 TT .SYS 2P 19-Nov-82
10 Files, 306 Blocks
5584 Free blocks
```

## 4.4.19 No Protection Option (/U)

The /U option includes in the directory listing only those files on the volume you specify that are not protected against deletion. Files that are not protected do not have a P in the file's directory entry. The following command lists only those files on DK: that are not protected.

```txt
* /S:SIZ/R/U
 14-Dec-82
COUNT .MAC          100 06-Sep-82      SBT .TXT         25 27-Nov-82
ASCII .MAC          67 19-Nov-82      MAIL.MAI       7 19-Nov-82
SUBONE.MAC          41 19-Nov-82      SORT.FOR        4 19-Nov-82
MYPROG.MAC          36 12-Oct-82      DX   .SYS         3 06-Sep-82
 8 Files, 283 Blocks
 325 Free blocks
```

## 4.4.20 Volume ID Option (/V[:ONL])

The /V option prints the volume identification and owner name as part of the directory listing header. The optional argument, :ONL, prints only the volume ID and owner name. You can combine /V with any other option.

The following example uses the /V option.

```txt
* DY:/V
 14-Jan-83
  Volume ID: BACKUP2
  Owner : Marcy
SWAP .SYS 25P 19-Nov-82 RT11SJ.SYS 67P 19-Nov-82
RT11FB.SYS 80P 19-Nov-82 RT11BL.SYS 64P 19-Nov-82
TT .SYS 2P 19-Nov-82 DT .SYS 3P 19-Nov-82
DP .SYS 3P 19-Nov-82 DX .SYS 3P 19-Nov-82
DY .SYS 4P 19-Nov-82 RF .SYS 3P 19-Nov-82
RK .SYS 3P 19-Nov-82 DL .SYS 4P 19-Nov-82
 12 Files, 271 Blocks
 215 Free blocks
```

The next example uses the :ONL·argument.

```txt
* DYO:/V:ONL
Volume ID: RT11 V5
Owner : Donna
```
