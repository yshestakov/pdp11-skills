# RT-11 System Utilities Manual: Ch.17 QUEUE package (QUEUE, QUEMAN, PRINT/QUEUE)

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 17.1 Calling and Using the Queue Package
- 17.1.1 Running QUEUE
- 17.1.2 Running QUEMAN
- 17.2 QUEMAN Options
- 17.2.1 Terminating QUEUE (/A)
- 17.2.2 Date Option (/C[:date])
- 17.2.3 Deleting Input Files After Printing (/D)
- 17.2.4 Printing Banner Pages (/H:n)
- 17.2.5 Since Option (/I[:date])
- 17.2.6 Before Option (/J[:date])
- 17.2.7 Printing Multiple Copies (/K:n)
- 17.2.8 Listing the Contents of the Queue (/L)
- 17.2.9 Removing a Job from the Queue (/M)
- 17.2.10 No Banner Pages Option (/N)
- 17.2.11 Setting Queue Package Defaults (/P)
- 17.2.12 Query Option (/Q)
- 17.2.13 Suspending Output (/S)
- 17.2.14 Resuming/Restarting Output (/R)
- 17.2.15 Log Option (/W)
- 17.2.16 Information Option (/X)
- 17.2.17 Continuing a Command String (//)

---

## Chapter 17 Queue Package

The Queue Package is a utility you can use for sending files to any valid RT-11 device. Although the Queue Package is particularly useful for queuing files for printing, queuing is not restricted to a line printer or any other serial device.

The Queue Package consists of two programs and a work file that contains the lineup of files, or queue, waiting to be output:

QUEUE    Queues and sends the files you specify. QUEUE runs as a
    foreground or system job.

QUEMAN A background job that processes command lines and file specifications you enter, and sends that information to QUEUE. It serves as the interface between you and the Queue Package.

QUFILE.WRK Contains the queue for the files QUEUE sends to the device(s) you specify.

The Queue Package runs only with the FB or XM monitor.

## NOTE

To prevent QUEUE and another job from intermixing output on the same non-file-structured device, use the LOAD command to assign exclusive ownership of a device to QUEUE.

## 17.1 Calling and Using the Queue Package

To use the Queue Package; you must first run QUEUE from the system volume as either a foreground or system job. (Note that system job support is a special feature. You can perform the system generation process to build a monitor and handlers that support system jobs.) You can then run QUEMAN in the background when you are ready to output files.

## 17.1.1 Running QUEUE

To run QUEUE as a foreground job, call QUEUE from the system volume by typing in response to the keyboard monitor dot (.):

. FRUN QUEUE RET

To run QUEUE as a system job, type in response to the keyboard monitor dot:

\+ SRUN QUEUE RET

To halt QUEUE, see Section 17.2.1.

## 17.1.2 Running QUEMAN

To run QUEMAN from the system volume, type in response to the keyboard monitor dot (.):

, R QUEMÁN

The Command String Interpreter (CSI) prints an asterisk at the left margin of the terminal, indicating it is ready to accept input. Enter a command string according to this general syntax:

[dev:[jobname[/options]] = ][filespec][/options][,filespec[/options]...]

where:

dev: represents any valid RT-11 device. (The default output device is LP0:.)

jobname represents the output job name. This is the logical name for all the files specified in the command. If you send a job to a file-structured device, QUEUE uses this name as the file name of the job, and assigns a .JOB file type. If you do not specify a job name, QUEMAN uses the file name of the first input file. The job name can have up to six characters.

filespec represents the input file specification. If you do not specify a file type, QUEMAN assumes a .LST file type.

options represents one or more of the options from Table 17-1.

If you use commas in place of file specifications, QUEMAN ignores all remaining file specifications on the command line. (Note, however, that if your command string consists of several lines, entering commas in place of a file specification does not affect file specifications on subsequent lines in the command string. Using commas in place of a file specification affects only those remaining files in that particular command line.)

## 17.2 QUEMAN Options

Table 17-1 summarizes the options you can use in the QUEMAN command line. The sections that follow Table 17-1 provide detailed explanations and examples of each option. Note that some of the options are position-dependent - that is, their function depends on where you place them in the command line. Also, some of the options accept a date as an argument. The syntax for specifying the date is:

Table 17-1: QUEMAN Options

| Option | Section | Function |
| --- | --- | --- |
| /A | 17.2.1 | Terminates QUEUE. |
| /C[:date] | 17.2.2 | Prints only those files with the specified date. If you use /C and do not specify a date, QUEMAN prints only those files with the current date. |
| /D | 17.2.3 | Deletes the input file(s) after printing. This option is position-dependent. |
| /H:n | 17.2.4 | Prints n banner pages for each specified input file, where n is a decimal number. This option is position-dependent. |
| /I[:date] | 17.2.5 | Prints only those files created on or after the specified date. |
| /J[:date] | 17.2.6 | Prints only those files created before the specified date. |
| /K:n | 17.2.7 | Prints n copies of each specified file, where n is a decimal number. This option is position-dependent. |
| /L | 17.2.8 | Lists the contents of the queue. |
| /M | 17.2.9 | Removes a job from the queue. |
| /N | 17.2.10 | Specifies no banner pages for the input file(s). |
| /P | 17.2.11 | Sets two Queue Package default values: the number of banner pages, and whether you want QUFILE.WRK deleted when you terminate QUEUE. |
| /Q | 17.2.12 | Causes QUEMAN to request confirmation that a particular file should be included in the operation. QUEMAN prints the name of each file that can be included in the operation. You must respond Y to include a particular file. |
| /R | 17.2.14 | Resumes sending the current job after it has been suspended, or restarts the current file in the job being sent. |
| /S | 17.2.13 | Suspends output at the end of the current file. |
| /W | 17.2.15 | Prints on the console a log of the files involved in the operation. |
| /X | 17.2.16 | Allows QUEMAN to continue processing instead of halting when it cannot find a file you specified in the command line. |
| // | 17.2.17 | Continues command on the next line. |

[:dd.][:mmm][:yy.]

where:

dd. represents the day (a decimal integer in the range 1–31)

mmm represents the first three characters of the name of the month

yy. represents the year (a decimal integer in the range 73–99)

The default value for the date is the current system date. If you omit any of these values (dd, mmm, or yy), the system uses the values from the current system date. For example, if you specify only the year ::82. and the current system date is May 4, 1983, the system uses the date 4.:MAY:82.. If the current date is not set; it is considered 0 (the same as for an undated file in a directory listing). The date values are position-dependent. If you omit the day (dd) or month (mmm), you must use a colon (:) in place of the value.

If you have selected timer support through the system generation process, but have not selected automatic end-of-month date advancement, make sure that you set the date at the beginning of each month with the DATE command. If you fail to set the date at the beginning of each month, the system prints -BAD- in the creation date column of each file created beyond the end-of-month. (Note that you can eliminate -BAD- by using the RENAME/SETDATE command after you set the date.)

If QUEUE is sending a job that has multiple input files to an RT-11 file-structured volume, QUEUE copies each input file to a separate output file with the same file name and type as the input file. The jobname is used in the JOBNAME field of the banner page (if you request banner pages).

## 17.2.1 Terminating QUEUE (/A)

When you type /A in response to the CSI asterisk, QUEMAN terminates QUEUE. If you use /A while a job is printing, QUEUE halts output. If QUEUE is running as a foreground job, using /A has the same effect as typing CTRL/F and two CTRL/Cs. If QUEUE is running as a system job, using /A has the same effect as typing CTRL/X and then specifying QUEUE as the system job to which you want to direct input, followed by two CTRL/Cs.

The following example terminates QUEUE

• R QUEMAN

\* /A

If you use CTRL/Cs to termiante QUEUE, this may take a few seconds because QUEUE performs the following I/O rundown before terminating:

\- Waits for all current I/O transfers to complete

\- Removes protection from the input file if it was unprotected before QUEUE began copying it to the output device

\- Closes the work file if you have chosen to save the work file

## 17.2.2 Date Option (/C[:date])

The /C[:date] option prints only those files with the specified date. If no date is specified only those files with the current date are printed. Specify /C only once in the command line; it applies to all the file specifications in the entire command. The following command prints on LP0: all files named ITEM1 and ITEM2 that also have the date March 20, 1983.

\* ITEM1/C:20.:MAR:83.,ITEM2

## 17.2.3 Deleting Input Files After Printing (/D)

Use the /D option to delete input files after QUEUE has sent them. This option is position-dependent. If you use it with the job name, /D applies to all the input files. If you use it with an input file specification, /D applies only to that input file.

The following example deletes all input files after they have been sent:

```csv
* MYJOB/D=FILE1,FILE2,FILE3
```

The following example deletes FILE1 and FILE3 but retains FILE2 after QUEUE has sent them:

```csv
* MYJOB=FILE1/D,FILE2,FILE3/D
```

Input files are protected from deletion while QUEUE is copying them to the output device. This protects input files from accidental deletion.

## 17.2.4 Printing Banner Pages (/H:n)

Use the /H:n option to print banner pages for the input files you specify, where n is a decimal number selecting the number of banner pages. This option is position-dependent. If you use /H:n with the jobname, QUEUE prints n banner pages for each input file. If you use /H:n with an input file specification, QUEUE prints n banner pages for that file, and prints the default number of banner pages for the remaining input files. (Note that you set the default number of banner pages with the /P option, described in Section 17.2.11. If the default number of banner pages set with the /P option is 0, n defaults to 1.)

The sample command line that follows prints four banner pages for each input file:

\* LAUGHN/H:4=ROWAN.TXT,MARTIN.TXT.

The following sample command prints four banner pages for MARTIN.TXT and the default number of banner pages for ROWAN.TXT:

\* LAUGHN=ROWAN.TXT,MARTIN.TXT/H:4

Note that QUEUE never prints a banner for the job; it prints banners only for the input files.

## 17.2.5 Since Option (/I[:date])

The /I[:date] option prints only those files created on or after the specified date. If you specify no date QUEMAN uses the current system date. The following command prints only those .MAC files on device DK: created on or after April 21, 1983:

\* \*.MAC/I:21.:APR:83.

## 17.2.6 Before Option (/J[:date])

The /J[:date] option copies only those files created before the specified date. If you specify no date QUEMAN uses the current system date. The following command prints only those .MAC files on device DK: created before April 21, 1983:

```batch
* *.MAC/J:21.:APR:83.
```

## 17.2.7 Printing Multiple Copies (/K:n)

Use the /K:n option to specify the number of copies of the input files you specify, where n is a decimal number. The /K:n option is position-dependent. If you use /K:n with the job name, QUEUE prints n copies of each input file. If you use /K:n with an input file specification, QUEUE prints n copies of that particular file.

The next command line prints four copies of LAUREL.LST and four copies of HARDY.LST:

```csv
* JOB/K:4=LAUREL,HARDY
```

The following sample command line prints four copies of LAUREL.LST and the default number of copies of HARDY.LST:

\* JOB = HARDY, LAUREL / K : 4

## 17.2.8 Listing the Contents of the Queue (/L)

Use the /L option to get a listing of the contents of the queue. The listing gives the output device, job name, input files, job status, and number of copies for each job that is in the queue. The job STATUS column prints P if the job is currently being sent, S if the job being sent is suspended, or Q if the job is waiting to be sent. If you have a large queue and your console is a video terminal, you can use the keyboard CTRL/S and CTRL/Q commands to control the scrolling of the listing.

The sample command line that follows lists the queue:

<table><tr><td>* /LDEVICE</td><td>JOB</td><td>STATUS</td><td>COPIES</td><td>FILES</td></tr><tr><td rowspan="3">LPO:</td><td rowspan="3">LAB2</td><td rowspan="3">P</td><td>1</td><td>PASS3 ,LST</td></tr><tr><td>2</td><td>PASS4 ,LST</td></tr><tr><td>2</td><td>PASS5 ,LST</td></tr><tr><td>LPO:</td><td>HODG</td><td>Q</td><td>3</td><td>MESMAN ,DOC</td></tr><tr><td rowspan="2">MT1:</td><td rowspan="2">JUDITH</td><td rowspan="2">Q</td><td>2</td><td>PART1 ,DOC</td></tr><tr><td>2</td><td>PART2 ,DOC</td></tr><tr><td rowspan="2">LPO:</td><td rowspan="2">JOYCE</td><td rowspan="2">Q</td><td>1</td><td>SSM ,DOC</td></tr><tr><td></td><td>DOCPLN ,DOC</td></tr></table>

## 17.2.9 Removing a Job from the Queue (/M)

Use the /M option to remove a job from the queue. When you use this option, specify the job name followed by /M and the equal sign (=). The following example removes the job LAB4 from the queue:

\* LAB.4/M=

When you use /M, you do not have to specify the input files, only the job name. You remove all the files associated with the job name.

## 17.2.10 No Banner Pages Option (/N)

Use the /N option to specify that you do not want QUEUE to print any banner pages for the input file(s). Use /N if you have previously set the default number of banner pages with the /P option (see Section 17.2.11). The /N option is position-dependent; that is, if you use it after the job name, it applies to each input file. Use /N after an input file to apply to only the particular file.

The following example uses /N to specify no banner pages for each file in the job, MYJOB2.

\* 'MYJOB2/N=PASS1,PASS2,PASS3

The /N option has the same effect as /H:0 (see Section 17.2.4).

## 17.2.11 Setting Queue Package Defaults (/P)

Use the /P option to set defaults for two values:

1. Number of banner pages printed for each input file. You can override the default number of banner pages by using the /H option.

2. Whether you want the work file, QUFILE.WRK, deleted when you halt QUEUE. (Note that QUFILE.WRK contains the lineup of files, or queue, waiting to be sent to an output device.)

When you type /P in response to the CSI asterisk, QUEMAN prints the following prompt at the terminal:

```txt
1) Number of banner pages ?
```

QUEUE uses the number you type as the default number of banner pages it prints for each file it sends to a device. If you type only a carriage return, QUEMAN assumes 0. This value remains in effect until the work file, QUFILE.WRK, is deleted (see below).

After you have responded to the previous prompt, QUEMAN prints the following prompt at the terminal:

```txt
2) Delete workfile ?
```

If you type N followed by a carriage return, or only a carriage return, QUEUE maintains the current QUFILE.WRK after you halt QUEUE. That is, if you start QUEUE later, QUFILE.WRK retains the queue it had prior to the halt. By maintaining QUFILE.WRK between the times QUEUE is halted, you have an automatic queue restart capability. This value remains in effect until you reset it.

If you type Y followed by a carriage return, QUEUE deletes QUFILE.WRK when you halt QUEUE. The next time you start QUEUE, it creates a new QUFILE.WRK. This value remains in effect only until the next time you start QUEUE.

## 17.2.12 Query Option (/Q)

Use the /Q option to list all files and to confirm individually which of these files should be printed. Typing Y or any string beginning with Y followed by a carriage return causes the named file to be printed. Typing anything else excludes the file. The following example prints files that reside on DY1:.

```txt
* DY1:*,*/Q
DY1:FIX463.SAV to LP: ?
DY1:GRAPH.BAK to LP: ?
DY1:DMPX.MAC to LP: ?
DY1:MATCH.BAS to LP: ?
DY1:EXAMP.FOR to LP: ?
DY1:GRAPH.FOR to LP: ?
DY1:GLOBAL.MAC to LP: ?
DY1:PROSEC.MAC to LP: ?
DY1:KB.MAC to LP: ?
DY1:EXAMP.MAC to LP: ?
```

## 17.2.13 Suspending Output (/S)

Use the /S option to suspend output of a job being sent. When you type /S in response to the CSI asterisk, QUEUE suspends output only after it has completed output of the current file in the job. This option is useful if you want access to an output device while a large job is being sent to it.

To resume output, use the /R option (Section 17.2.14).

## 17.2.14 Resuming/Restarting Output (/R)

Use the /R option either to resume output of a suspended job, or to restart output of the current file in the job from the beginning of the file. Note that a job resumes if you previously suspended it with /S, and a job restarts if you have not previously suspended it.

Resuming a job with multiple input files when the job is being sent to an RT-11, file-structured volume can be useful if the volume involved is too small to contain the entire job. You can suspend the job being sent (using the /S option), change volumes, and resume output of the remainder of the job on the new volume. QUEUE uses the same file name for both parts of the job.

## 17.2.15 Log Option (/W)

When you use the /W option, QUEMAN prints a list of all files printed or copied to a file. The /W option is useful if you do not want to take the time to use the query mode (the /Q option, described in Section 17.2.12), but you do want a list of the files printed or copied by QUEMAN.

QUEMAN prints the log for an operation on the terminal under the command line. This example shows logging when files are queued to be printed on LP0:.

```txt
* DY1:*,*/W
Files queued:
DY1:TEST.MAC to LP:
DY1:FIX463.SAV to LP:
DY1:GRAPH.BAK to LP:
DY1:DMPX.MAC to LP:
DY1:MATCH.BAS to LP:
DY1:EXAMP.FOR to LP:
DY1:GRAPH.FOR to LP:
DY1:GLOBAL.MAC to LP:
DY1:PROSEC.MAC to LP:
DY1:EXAMP.MAC to LP:
```

## 17.2.16 Information Option (/X)

The /X option causes QUEMAN to print an information message when QUEMAN fails to find all of the files you specify in a command line. If you do not use /X, QUEMAN prints a fatal error message when it is unable to find an input file, and returns control to the keyboard monitor after the rest of the operation completes. Use /X in indirect command files to ensure that processing will continue even if QUEMAN fails to find a file you specify.

In the following example, QUEMAN is unable to find the file FILE2.MAC. QUEMAN prints a message informing you that the file was not found and continues processing.

```csv
* LP:*,*=DLO:FILE1,MAC,FILE2,MAC,FILE3,MAC
?QUEMAN-I-File not found DLO:FILE2,MAC
```

## 17.2.17 Continuing a Command String (//)

Use the // option to continue a command string on subsequent lines. This option is useful if you want to output more files than you can specify on one line. When you want to include several lines in a CSI command string, type // at the end of the first line, and again at the end of the command string.

The following command string uses the // option:

\* JOBNAM=LML1,MAC,LML2A,MAC//

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">\* LML51, MAC, LML95, MAC</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">\* LML4, MAC, LML56, MAC //</span></small>
