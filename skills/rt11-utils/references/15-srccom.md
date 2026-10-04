# RT-11 System Utilities Manual: Ch.15 SRCCOM source comparison, SLP-format differences output

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 15.1 Calling and Terminating SRCCOM
- 15.2 SRCCOM Command String Syntax
- 15.3 Using Wildcards with SRCCOM
- 15.4 Options
- 15.5 Differences Listing Format
- 15.5.1 Sample Text
- 15.5.2 Sample Differences Listing
- 15.5.3 Changebar Option (/D[/V:i:d])
- 15.6 Creating a SLP Command File

---

# Chapter 15 Source Comparison (SRCCOM)

The RT-11 source comparison program (SRCCOM) compares two ASCII files and lists the differences between them. SRCCOM can either print the results or store them in a file. SRCCOM is particularly useful when you want to compare two similar versions of a source program. A file comparison listing highlights the changes made to a program during an editing session.

SRCCOM is also useful for creating a command file that you can run with the source language patch program (SLP), described in Chapter 23. When you use SRCCOM for creating a command file, you can patch one version of a source file so that it matches another version. Section 15.6 describes how to create a command file for SLP.

## 15.1 Calling and Terminating SRCCOM

To call SRCCOM from the system device, respond to the dot (.) printed by the keyboard monitor by typing:

.R SRCCOM RET

The Command String Interpreter (CSI) prints an asterisk at the left margin of the terminal and waits for you to enter a command string. If you respond to the asterisk by entering only a carriage return, SRCCOM prints its current version number.

You can type CTRL/C to halt SRCCOM and return control to the monitor when SRCCOM is waiting for input from the console terminal. You must type two CTRL/Cs to abort SRCCOM at any other time. To restart SRCCOM, type R SRCCOM or REENTER and a carriage return in response to the monitor's dot.

## 15.2 SRCCOM Command String Syntax

The syntax of the SRCCOM command string is:

$$
[ \text {output - filespec} ], [ \text {SLP - filespec} = ] \text {old - filespec}, \text {new - filespec} [ / \text {option}... ]
$$

where:

output-filespec represents the destination device or file for the listing of differences.

SLP-filespec represents the destination device or file for the command file to be run with SLP. See Section 15.6 for more information on creating a command file for SLP.

old-filespec represents the first file to be compared.

new-filespec represents the second file to be compared.

option is one of the options listed in Table 15-1.

Note that you can specify the input files in any order if you want only a comparison. If you are creating a patch for use with the SLP utility, then specify the input files in the old-file, new-file order shown above. The console terminal is the default output device. The default file type for input files is .MAC. SRCCOM assigns .DIF as the default file type for differences files. The default file type for a SLP command file is .SLP.

Either or both output file specifications can be omitted. However the output file specifications are position-dependent. If you specify a SLP-filespec but no output-filespec, you must place a comma before the SLP file specification to denote the absence of an output-filespec.

SRCCOM examines the two source files line by line, looking for groups of lines that match. When SRCCOM finds a mismatch, it lists the lines from each file that are different. SRCCOM continues to list the differences until a specific number of lines from the first file matches the second file. The specific number of lines that constitutes a match is a variable that you can set with the /L:n option.

## 15.3 Using Wildcards with SRCCOM

You can use wildcards to perform multiple source file comparisons by typing only one command line. However, you can use wildcards only to compare files; you cannot use wildcards when creating a command file to run with SLP.

You can use wildcards in either input file specification (old-filespec or new-filespec). A different type of comparison is performed depending on whether you use wildcards in only one or in both of the input file specifications.

If you use wildcards in only one of the input file specifications, SRCCOM compares the file you specify without any wildcards to all variations of the file specification with wildcards. The wildcard represents the part of the file specification to be varied. You can use this method to compare one file to several other files. For example, when the following command line is executed, SRCCOM compares the file TEST1.MAC on device DY0: to all files on device DY1: with the file name TEST2:

\* TEST=DYO:TEST1.MAC,DY1:TEST2.\*

You can send the results of all the comparisons to a file on a volume rather than to the console by specifying an output file. In this example, all differences from the comparisons are sent to the file TEST.DIF on device DK:.

If you use wildcards in both input file specifications, the wildcards represent a part of a file specification that you want to be the same in both files being compared. You can use this method to compare several pairs of files; each input file is compared to only one other input file. For example, when the following command line is executed, SRCCOM compares pairs of files; the first input file in each pair has the file name PROG1, and the second has the file name PROG2. The file type of both files in each pair must match.

```csv
* DYO:PROG1,*,DY1:PROG2,*
```

SRCCOM searches for the first file on DY0: with the file name PROG1, and takes note of its file type. Then, SRCCOM searches DY1: for a file with the file name PROG2 and the same file type as PROG1. If a match is found, SRCCOM compares the two files and lists the differences on the console (or sends the differences to an output file if one is specified). SRCCOM then searches DY0: for more files with the file name PROG1 and DY1: for PROG2 files with matching file types.

## 15.4 Options

Table 15-1 summarizes the operations you can perform with SRCCOM options. You can place these options anywhere in the command string, but it is conventional to place them at the end of the command line.

## 15.5 Differences Listing Format

This section describes the SRCCOM differences listing format and explains how to interpret it.

## 15.5.1 Sample Text

It will be helpful first to look at a sample text file, DEMO.BAK:

```txt
FILE1
HERE'S A BOTTLE AND AN HONEST FRIEND!
WHAT WAD YE WISH FOR MAIR, MAN?
WHA KENS, BEFORE HIS LIFE MAY END,
WHAT HIS SHAME MAY BE O' CARE, MAN?
THEN CATCH THE MOMENTS AS THEY FLY,
AND USE THEM AS YE OUGHT, MAN:--
BELIEVE ME, HAPPINESS IS SLY,
AND COMES NOT AYE WHEN SOUGHT, MAN.
```

--SCOTTISH SONG

Table 15-1: SRCCOM Options

| Option | Function |
| --- | --- |
| /A | Lets you specify an audit trail (a string of characters that marks each updated line of a patched source file). Use /A with the SLP output file specification to create a file that can be used as command file input for the source language patch program SLP (see Chapter 23). |
| /B | Compares blank lines; normally, SRCCOM ignores blank lines. |
| /C | Ignores comments (all text on a line preceded by a semicolon) and spacing (spaces and tabs). A line consisting entirely of a comment is still included in the line count. |
| /D | Creates a listing of the new file specified in the command line with the differences from the old file marked with vertical bars (1) to indicate insertions and bullets (0) to indicate deletions. |
| /F | Includes form feeds in the output listing; SRCCOM normally compares form feeds, but does not include them in the differences listing. |
| /L[:n] | Specifies the number of lines that determines a match; n is an octal integer in the range 1 through 310. The default value for n is 3. |
| /S | Ignores spaces and tabs. |
| /T | Compares blanks and tabs that appear at the end of a line. Normally SRCCOM ignores these trailing blanks and tabs. |
| /V:i:d | Used with /D to specify the characters you want SRCCOM to use in place of vertical bars and bullets. This option is useful if your terminal does not print the vertical bar character. Both i and d represent the numeric codes for ASCII characters in the range 40 through 176 (octal), where i represents the code for the insertion character and d the deletion character code. |

This file contains two typing errors. In the fourth line of the song, shame should be share. In the seventh line, sly should be shy. Here is a file called DEMO.TXT that has the correct text:

```csv
FILE2
HERE'S A BOTTLE AND AN HONEST FRIEND!
WHAT WAD YE WISH FOR MAIR, MAN?
WHA KENS, BEFORE HIS LIFE MAY END,
WHAT HIS SHARE MAY BE O' CARE, MAN?
THEN CATCH THE MOMENTS AS THEY FLY,
AND USE THEM AS YE OUGHT, MAN:--
BELIEVE ME, HAPPINESS IS SHY,
AND COMES NOT AYE WHEN SOUGHT, MAN.
--SCOTTISH SONG
```

## 15.5.2 Sample Differences Listing

SRCCOM can list the differences between the two files. The example below compares the original file, DEMO.BAK, to its edited version, DEMO.TXT:

```txt
_DEMO.BAK,DEMO.TXT/L:1
1) DK:DEMO.BAK
2) DK:DEMO.TXT

*****
1)1 FILE1
1) HERE'S A BOTTLE AND AN HONEST FRIEND!
****
2)1 FILE2
2) HERE'S A BOTTLE AND AN HONEST FRIEND!
*****
1)1 WHAT HIS SHAME MAY BE O' CARE, MAN?
1) THEN CATCH THE MOMENTS AS THEY FLY,
****
2)1 WHAT HIS SHARE MAY BE O' CARE, MAN?
2) THEN CATCH THE MOMENTS AS THEY FLY,
*****
1)1 BELIEVE ME, HAPPINESS IS SLY,
1) AND COMES NOT AYE WHEN SOUGHT, MAN,
****
2)1 BELIEVE ME, HAPPINESS IS SHY,
2) AND COMES NOT AYE WHEN SOUGHT, MAN.
*****
?SRCCOM-W-Files are different
```

If the files are different, SRCCOM always prints the file name of each file as identification:

```txt
1) DK:DEMO.BAK
2) DK:DEMO.TXT
```

The numbers at the left margin have the form n)m, where n represents the source file (either 1 or 2) and m represents the page (delineated by form feeds) of that file on which the specific line is located.

SRCCOM next prints ten asterisks and then lists the differences between the two files. The /L:n option was used in this example to set to 1 the number of lines that must agree to constitute a match.

The first line of both files differs. SRCCOM prints the first line from the first file, followed by the second line as a reference. SRCCOM then prints four asterisks, followed by the corresponding two lines of the second file.

```txt
1) 1
1)     HERE'S A BOTTLE AND AN HONEST FRIEND!
****
2) 1
2)     HERE'S A BOTTLE AND AN HONEST FRIEND!
**********
```

The fourth line contains the second discrepancy. SRCCOM prints the fourth line from the first file, followed by the next matching line as a reference.

```txt
1) 1 WHAT HIS SHAME MAY BE O' CARE, MAN?
1) THEN CATCH THE MOMENTS AS THEY FLY,
****
```

The four asterisks terminate the differences from the first file. SRCCOM then prints the fourth line from the second file, again followed by the next matching line as a reference:

```txt
2)1 WHAT HIS SHARE MAY BE O' CARE, MAN?
2) THEN CATCH THE MOMENTS AS THEY FLY,
**********
```

The ten asterisks terminate the listing for a particular differences section.

SRCCOM scans the remaining lines in the files in the same manner. When it reaches the end of each file, it prints the ?SRCCOM-W-Files are different message on the terminal.

The following example is slightly different. The default value for the /L:n option sets to 3 the number of lines that must agree to constitute a match. The output listing is directed to the file DIFF.TXT on device DK:.

```gitattributes
* DIFF.TXT=DEMO.BAK,DEMO.TXT
?SRCCOM-W-Files are different
```

The monitor TYPE command lists the information contained in the output file:

```c
, TYPE DIFF.TXT
1) DK:DEMO.BAK
2) DK:DEMO.TXT
*************************
1)1 FILE1
1) HERE'S A BOTTLE AND AN HONEST FRIEND!
****
2)1 FILE2
2) HERE'S A BOTTLE AND AN HONEST FRIEND!
*************************
1)1 WHAT HIS SHAME MAY BE O' CARE, MAN?
1) THEN CATCH THE MOMENTS AS THEY FLY,
1) AND USE THEM AS YE OUGHT, MAN:--
1) BELIEVE ME, HAPPINESS IS SLY,
1) AND COMES NOT AYE WHEN SOUGHT, MAN.
****
2)1 WHAT HIS SHARE MAY BE O' CARE, MAN?
2) THEN CATCH THE MOMENTS AS THEY FLY,
2) AND USE THEM AS YE OUGHT, MAN:--
2) BELIEVE ME, HAPPINESS IS SHY,
2) AND COMES NOT AYE WHEN SOUGHT, MAN.
*************************
```

As in the first example, SRCCOM prints the file name of each file:

```txt
.1) DK:DEMO.BAK
2) DK:DEMO.TXT
```

The first line of both files differs, so SRCCOM prints the first two lines of both files, as in the listing at the terminal from the previous example:

```txt
1)1 FILE1
1) HERE'S A BOTTLE AND AN HONEST FRIEND!
****
```

2)1 FILE2
2) HERE'S A BOTTLE AND AN HONEST FRIEND!
\*\*\*\*\*\*\*\*\*\*

Again, the fourth line differs. SRCCOM prints the fourth line of the first file, followed by the next matching line:

1)1 WHAT HIS SHAME MAY BE O' CARE, MAN?
1) THEN CATCH THE MOMENTS AS THEY FLY,

However, SRCCOM did not find a match (three identical lines) before it encountered the next difference. So, the second matching line prints, followed by the next differing line from the first file:

1) AND USE THEM AS YE OUGHT, MAN:--

1) BELIEVE ME, HAPPINESS IS SLY,

Again, the next matching line prints:

1) AND COMES NOT AYE WHEN SOUGHT, MAN.

The /B option to include blank lines in the comparison was not used in this example. Thus, SRCCOM recognizes only one more line before the end of file. Since the two identical lines do not constitute a match (three are needed), SRCCOM prints the last line as part of the differences for the first file:

1) --SCOTTISH SONG

In a similar manner, SRCCOM prints the differences for the second file, ending the listing with the ?SRCCOM-W-Files are different message.

## NOTE

Regardless of the output specification, the differences message always prints on the terminal. If you compare two files that are identical and specify a file for the differences listing, the message ?SRCCOM-I-No differences found prints on the terminal and SRCCOM does not create an output file.

## 15.5.3 Changebar Option (/D[/V:i:d])

When you use the /D option in the SRCCOM command line, SRCCOM creates a listing in which it inserts vertical bars (1) and bullets (0) to denote the differences between the two files in the command line. The vertical bar indicates insertion; the bullet indicates deletion. If you do not specify an output file, SRCCOM prints the listing at the terminal.

If you include the /V:i:d option with /D (you cannot use /V:i:d without /D), you can specify what characters you would like in place of the vertical bar and/or bullet. The argument i represents the ASCII code (between 40 and 176 octal) for the character you want in place of the vertical bar. The argument d represents the ASCII code (between 40 and 176 octal) for the character you want to use in place of the bullet.

In the following command line, SRCCOM compares DEMO.BAK to DEMO.TXT:

\* DEMO.BAK,DEMO.TXT/D/L:1

When SRCCOM processes the last command, it prints at the terminal the following listing:

```txt
FILE2
HERE'S A BOTTLE AND AN HONEST FRIEND!
WHAT WAD YE WISH FOR MAIR, MAN?
WHA KENS, BEFORE HIS LIFE MAY END,
WHAT HIS SHARE MAY BE O' CARE, MAN?
THEN CATCH THE MOMENTS AS THEY FLY,
AND USE THEM AS YE OUGHT, MAN:--
BELIEVE ME, HAPPINESS IS SHY,
AND COMES NOT AYE WHEN SOUGHT, MAN.
--SCOTTISH SONG
?SRCCOM-W-Files are different
```

## 15.6 Creating a SLP Command File

You can use SRCCOM to create an input command file to the source language patch program, SLP, described in Chapter 23. Specify a SLP file specification in the SRCCOM command line. The SRCCOM option /A can be used for specifying an audit trail while creating this command file.

When you specify a SLP-filespec file in the SRCCOM command line, SRCCOM creates a file you can use as the SLP input command file. If you specify both an output-filespec and a SLP-filespec, SRCCOM creates both a differences listing and a SLP input command file. If you specify only an output-filespec, SRCCOM generates only a differences listing. If you specify only a SLP-filespec, SRCCOM creates only a SLP input command file.

In the following sample command line, SRCCOM creates an output file, MOD.SLP, which contains the necessary commands that, when used with SLP, can modify DEMO.BAK so that it matches DEMO.TXT.

```csv
* ,MOD=DEMO,BAK,DEMO,TXT
```

You can use the /A option to specify an audit trail. When SLP updates a file, it creates two output files. One output file is the patched source file; the second is a listing file. The listing file contains a numbered listing of the patched file, and it also has an audit trail SLP has appended to each changed line. The audit trail is a string of characters that keeps track of the update status of each line in the patched source file. SLP appends the audit trail to the right margin of each updated line in the patched source file. Note that when SLP must change a line, it appends an additional audit trail below the audit trail of the changed line. The additional audit trail keeps track of the number of consecutive lines that change.

When you use the /A option you can specify what characters you want in the audit trail. SRCCOM prompts you for the audit trail:

Audit trail?

Respond with a string of up to 12 characters. Do not use a slash (/) in the audit trail. The example below provides a sample of a SLP listing file that contains a meaningful audit trail: the author's initials and the date of the patch.

SLP 05.00

## ADDRSS,ADDRSS=ADDRSS,ADDRSS

1. FOURSCORE AND SEVEN YEARS AGO,
2. OUR FATHERS BROUGHT FORTH ON THIS CONTINENT
3. A NEW NATION, CONCEIVED IN LIBERTY ;AL-4\*29\*1863
4. AND DEDICATED TO THE PROPOSITION ;AL-4\*29\*1863
5. THAT ALL MEN ARE CREATED EQUAL, ;\*\*-2
6. NOW WE ARE ENGAGED IN A GREAT CIVIL WAR,
7. TESTING WHETHER THAT NATION, OR ANY NATION ;AL-4\*29\*1863
8. SO CONCEIVED AND SO DEDICATED, ;\*\*-1
9. CAN LONG ENDURE,

(1)
