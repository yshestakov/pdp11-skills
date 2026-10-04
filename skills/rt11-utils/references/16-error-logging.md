# RT-11 System Utilities Manual: Part II, Ch.16 error logging subsystem (ELINIT, ELTASK, ERROUT)

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 16.1 Uses
- 16.2 Error Logging Subsystem
- 16.3 Calling and Using the Error Logger with the SJ Monitor
- 16.4 Calling and Using the Error Logger with the FB or XM Monitor
- 16.4.1 Using ELINIT
- 16.5 Using ERROUT
- 16.6 Report Analysis
- 16.6.1 Storage Device Error Report
- 16.6.2 Memory Error Report
- 16.6.3 Summary Error Report

---

## Part II System Jobs

Part II describes four utilities that you can run as system jobs: the Error Logger and the Queue, SPOOL, and VTCOM Packages. System job support is a special feature, available only through the system generation process. The Queue, SPOOL, and VTCOM Packages must run under an FB or XM monitor. The Error Logger runs under the SJ monitor as well as under the FB and XM monitors. For an in-depth description of the system job feature, see the RT-11 Software Support Manual.

Chapter 16 describes the error logging subsystem that keeps statistical records of all I/O transfers, I/O errors, memory parity errors, and cache memory errors. Chapter 17 describes the Queue Package that sends files for output to any valid RT-11 device. Chapter 18 describes the transparent spooler (SPOOL) that automatically intercepts, stores, and sends data to the line printer. Chapter 19 describes the communication package (VTCOM) that lets you communicate with a host while running RT-11.

Note that you can run these utilities as foreground jobs, but running them as system jobs enables you to run a foreground and a background job in addition.

(1)

## Chapter 16 Error Logging Subsystem

The Error Logger monitors the hardware reliability of the system. The Error Logger keeps a statistical record of all I/O operations that occur on any of the following devices:

| DD | DX |
| --- | --- |
| DL | DY |
| DM | DZ |
| DU | RK |
| DW |  |

In addition to keeping these statistics, the Error Logger detects and records memory parity or cache errors and any errors that occur during I/O operations. At intervals, you determine, the Error Logger produces individual and/or summary reports on some or all of these errors. The Error Logger is available only as a special feature: that is, you must perform the system generation process to create the error logging files and enable error logging. It is available under the SJ monitor, the FB monitor, or the XM monitor. When you run the Error Logger with the FB or XM monitor, the Error Logger runs as either a foreground or system job.

## 16.1 Uses

Error logging reports are useful for maintaining the hardware on which RT-11 runs. Problems such as line noise, static discharges, or inherently error-prone media can cause recoverable errors on systems that are otherwise functioning normally. By studying error logging reports, you can learn to distinguish these errors from those that might be symptoms of an impending device failure. Also, some recoverable errors that are insignificant in themselves might be related to other more serious errors; their effects might not be immediately apparent to you. Information contained in the reports about each error and about the status of the system when the error occurred may alert you to a previously unforeseen hardware problem.

Sometimes a device fails so quickly that you are unable to prevent it. In this case, you can determine the cause more quickly if a report is available that describes the errors that occurred immediately prior to the failure.

In general, the error logging subsystem:

\- Gathers device error and I/O transfer information from the handlers

\- Gathers memory error information from the monitor

\- Stores the information in a file or in an internal buffer

\- Formats the information to produce a report

## NOTE

Because the Error Logger can record data on each I/O transfer, thereby using additional computer time and memory, you may wish to use the Error Logger only when you experience difficulty with a device. Keeping a backup system volume on which the Error Logger is enabled makes this easy. You can also issue the command SET dd: NOSUCCES (dd represents the device mnemonic) before running the error logger. This command causes the device to call the Error Logger only when an I/O transfer fails. Successful I/O transfer statistics are not recorded. (Remember to reload the dd handler after issuing the SET dd: NOSUCCES command.)

## 16.2 Error Logging Subsystem

When used with the FB and XM monitors, the Error Logger consists of three programs and a statistics file. When you run the Error Logger, you coordinate these programs to gather I/O and error-related information into its statistics file and create the error report you want. The Error Logger names the statistics file it creates ERRLOG.DAT. At any time you specify, you call another Error Logger program, ERROUT, to create error reports from the information it has gathered in ERRLOG.DAT.

When used with the SJ monitor, the Error Logger uses only two programs, and ERRLOG.DAT is not created. Instead, the Error Logger gathers I/O and error-related information in an internal buffer area. You can then generate a report from the information in the internal buffer by calling a second Error Logger program, ERROUT.

The names and functions of the Error Logger programs follow

A pseudohandler used with the SJ monitor to gather information about errors that occur during I/O transfers. The device handlers detect success and error information as each I/O tranfer occurs. The handlers communicate this information to EL.SYS, which gathers all the necessary statistics for an error report. EL.SYS stores these statistics in an internal buffer whose default size is 1 block. You can change the size of the internal buffer by setting the conditional ERL\$S (in SYCND.MAC) to n, where n is the number of blocks you want to reserve for the internal buffer. The variable n is interpreted as an octal number, unless you include a decimal point.

A foreground or system job that gathers information about I/O transfers and system errors. The device handlers detect success and error information as each I/O transfer occurs. The handlers communicate this information to ERRLOG.REL, which stores all the necessary statistics for an error report in an internal buffer. The buffer's contents are transferred to ERRLOG.DAT periodically, and whenever you request an error report. When you initiate error logging with the FB or XM monitor, ERRLOG.REL instructs you to start up the second error logging program, ELINIT.

ELINIT A background job under the FB or XM monitor that creates and maintains the statistics file, ERRLOG.DAT. You can direct ELINIT to initialize ERRLOG.DAT every time you have a session at the terminal, or you can direct ELINIT to continue compiling statistics in ERRLOG.DAT on a daily basis.

When you run ELINIT, it prompts you for the information it needs to maintain ERRLOG.DAT's size. By default, ELINIT allocates 100 decimal blocks for ERRLOG.DAT. Each time you run ELINIT, it prints a message that tells how many of those 100 blocks are filled. If ERRLOG.DAT fills to its limit, EL.REL is unable to store more information in it. So that you can increase ERRLOG.DAT's size, ELINIT prompts you for a file size change each time you run the program.

If you bootstrap a monitor whose features differ from those of the monitor under which ERRLOG.DAT was created, ELINIT may print a message indicating that it must initialize ERRLOG.DAT to make the statistics it has been maintaining compatible with the new configuration. When this happens, ELINIT renames the ERRLOG.DAT it formerly maintained to ERRLOG.TMP and creates a new ERRLOG.DAT. The Error Logger can still create a report from ERRLOG.TMP.

Note that you do not use ELINIT when you run the Error Logger with the SJ monitor. Instead, the Error Logger compiles statistics in an internal buffer area. When the internal buffer area fills to its limit EL is unable to store more information in it. You can generate a report from the information in the internal buffer or purge the internal buffer at any time.

A background job under the FB or XM monitor, or a program under the SJ monitor. ERROUT creates a report from the statistics in the EL internal buffer area, or from

ERRLOG.DAT or any file of that format. When you run ERROUT, you can direct the program to list the error report at the terminal or to create a file for the error report. You can also indicate whether you want a detailed report on each error that occurred or simply a summary report.

Figure 16–1 provides a diagram of the error logging subsystem under the FB and XM monitors. Figure 16–2 provides a diagram of the error logging subsystem under the SJ monitor.

Figure 16-1: Error Logging Subsystem - FB and XM

[figure omitted]

Figure 16-2: Error Logging Subsystem - SJ

[figure omitted]

## 16.3 Calling and Using the Error Logger with the SJ Monitor

To run the Error Logger with the SJ monitor, you must first load the Error Logger pseudohandler. Type in response to the keyboard monitor dot (.:):

• LOAD EL RET

Then type the following command in response to the keyboard monitor dot (.) to enable error logging:

\- SET EL LOG

When you type this command, the Error Logger begins to gather I/O transfer and error information in an internal buffer. The Error Logger also gathers statistics on the number of successful I/O transfers but does not create detailed records about successful transfers in the internal buffer. EL creates detailed records only for errors; these records contain such information as the device involved, when the error occurred, register contents, and number of retries. If the buffer becomes full, EL continues to compile I/O transfer statistics but writes no further detailed records to the internal buffer. When this occurs, the Error Logger displays the following message:

?EL-W-Buffer is full, logging suspended

You can clear the contents of the internal buffer when it becomes full, or at any other time, by typing in response to the keyboard monitor dot().:

\- SET EL PURGE

This command clears only the detailed records on errors stored in the internal buffer; the I/O statistics are retained. Before you clear the contents of the buffer you can generate an error report. Section 16.5 describes how to generate and interpret a report.

To suspend error logging, type in response to the keyboard monitor dot (.):

\- SET EL NOLOG

You can resume error logging by typing the SET EL LOG command.

You can disable error logging and unload the EL pseudohandler when you are through using the Error Logger by typing:

\- UNLOAD EL

This command clears the EL internal buffer area and all I/O statistics as well. If you want to save the contents of the internal buffer, copy it to a file before you unload EL. To save the internal buffer contents, type a command with the following syntax in response to the keyboard monitor prompt:

• COPY EL: dev:filnam,typ

## 16.4 Calling and Using the Error Logger with the FB or XM Monitor

With the FB or XM monitors, the Error Logger runs only as a foreground or system job. To run the Error Logger as a foreground job, call the Error Logger from the system device by typing in response to the keyboard monitor dot (.):

```txt
FRUN ERRLOG
```

To run the Error Logger as a system job, type in response to the keyboard monitor dot:

```txt
. SRUN ERRLOG
```

The Error Logger returns with a prompt, telling you how to initiate the error logging process.

```txt
?ERRLOG-I-To initiate Error Lossins, RUN ELINIT
```

To terminate the Error Logger if it is running as a foreground job, type a CTRL/F followed by two CTRL/Cs. If it is running as a system job, type a CTRL/X and then specify ERRLOG as the system job you want to terminate (followed by two CTRL/Cs).

## 16.4.1 Using ELINIT

After you type RUN ELINIT (or R ELINIT) followed by a carriage return, ELINIT returns with a prompt. This prompt asks you to specify which device you want the statistics file ERRLOG.DAT written to. The format of this prompt follows.

What is the name of the device for the ERRLOG.DAT file &lt;SY&gt;?

Type a carriage return in response to the last prompt if you want ELINIT to write ERRLOG.DAT to the system device.

ELINIT then prints a message indicating how many blocks allocated to ERRLOG.DAT are in use. This message is followed by a prompt asking you if you want ELINIT to initialize ERRLOG.DAT. The format of the block usage message and the initialization prompt follows (where xx represents the number of blocks in use).

```txt
xx blocks currently in use of xx Possible total in ERRLOG.DAT file
```

```txt
Do you want to zero the ERRLOG.DAT file and re-initialize (YES/NO) <NO>?
```

Type YES followed by a carriage return if you want ELINIT to initialize ERRLOG.DAT. When ELINIT initializes ERRLOG.DAT, it does not create a backup file for the statistics that were present prior to initialization. Enter a carriage return or type NO followed by a carriage return if you want ELINIT to retain the statistics already compiled in ERRLOG.DAT.

ELINIT proceeds by issuing the following prompt, asking you to indicate the number of blocks you want ELINIT to allocate to ERRLOG.DAT:

How many blocks for the ERRLOG.DAT file &lt;nnn&gt;?

The variable nnn represents the default size of 100, or the size of the current ERRLOG.DAT file. Type a carriage return if you want ERRLOG.DAT's file size to remain at the size indicated. If you want the file to be a different size, you can specify the number of blocks you want the file to have, followed by a carriage return. The only size limitation for ERRLOG.DAT is the amount of available space on the device in which it resides, and ERRLOG.DAT must be larger than one block.

## NOTE

Because of a rearrangement of your RT-11 configuration or bad header information in ERRLOG.DAT, it may be necessary for ELINIT to initialize ERRLOG.DAT even if you do not want it to. In this case, ELINIT automatically renames the current ERRLOG.DAT to ERRLOG.TMP, prints a message indicating it has done so, and returns the prompt How many blocks for the ERRLOG.DAT file <100>?

After you have responded to the file size prompt, ELINIT prints the following message:

RT-11 V5.0 ERROR LOGGING INITIATED

After the Error Logger has printed the last message, you can proceed.

## 16.5 Using ERROUT

The Error Logger program, ERROUT, creates a report from the information compiled in the file ERRLOG.DAT or in EL's internal buffer. You can instruct ERROUT to generate a report either indirectly, by typing the SHOW ERRORS command, or directly by running ERROUT. See Chapter 4 of the RT-11 System User's Guide for more information on the SHOW ERRORS command. To call ERROUT directly from the system device, type in response to the keyboard monitor dot (.):

\- RUN ERROUT

The Command String Interpreter (CSI) prints an asterisk at the left margin of the terminal and waits for you to enter a command string according to the following general syntax:

$$
[ \text {output - filespec} = ] [ \text {input - filespec} ] / \text {option}
$$

## where:

represents the device to which you want ERROUT to type the report. If you do not specify an output device, ERROUT prints the report at the terminal. If you specify a file name, ERROUT writes the error report to that file.

## input-filespec

represents ERRLOG.DAT or any file of the Error Logger statistics file format. (Thus, you can rename ERRLOG.DAT at any time and save it for later report formatting.) If you do not specify an input file, ERROUT assumes ERRLOG.DAT when running under the FB or XM monitor, and EL.SYS's internal buffer area when running under the SJ monitor.

option is one of the options listed below.

/A creates a report on each error in addition to a summary report of the errors and I/O transfers that occurred with each device.

/F:date use to create an error report for errors logged from the date you specify. Specify the date in the form dd:mmm:yy, where dd represents the two-digit day, mmm represents the first three letters of the month, and yy represents the last two digits of the year. ERROUT interprets the date you enter as octal; use a decimal point with the day and year to indicate the date is in decimal. If you do not use /F:date, ERROUT creates a report starting with the first error logged in the work file.

creates only a summary report of the errors and I/O transfers that occurred with each device.

use to create an error report for errors logged up to the date you specify. Specify the date as with the /F:date option above. If you do not use /T:date, ERROUT creates a report that includes the last error logged in the work file.

If you enter only a carriage return in response to the CSI asterisk, ERROUT types a full report from ERRLOG.DAT at the terminal.

## 16.6 Report Analysis

This section provides a line-by-line analysis of each different report the Error Logger creates. Basically, there are three report categories:

\- Storage device error report

• Memory error report

\- Summary report

## 16.6.1 Storage Device Error Report

When a device handler encounters an error during an I/O transfer, it automatically retries that transfer as many as eight times (the actual number of times a handler retries an unsuccessful transfer depends on the particular device handler and on the value you specify for n with the SET dd: RETRY = N command). Regardless of the number of retries, each unsuccessful transfer will be recorded as only one entry in the error report, unless the registers change during the retries. In that case, the Error Logger creates a report for each retry.

Figure 16–3 provides an example of a storage device error report. This example is a report of the second attempt for a read operation on an RX02 double-density diskette. Table 16–1 tells what some of the lines in the report mean. For ease of reference, each line in this example report is numbered (although lines in the actual report are not numbered).

## Figure 16-3: Sample Storage Device Error Report

```txt
**************************
DISK DEVICE ERROR
LOGGED 8-OCT-82 16:12:45
**************************
UNIT IDENTIFICATION
        PHYSICAL UNIT NUMBER                                      000001
        TYPE                                       RX211/RX02

SOFTWARE STATUS INFORMATION:
        MAXIMUM RETRIES       8,
        REMAINING RETRIES      G,
        OCCURRENCES OF THIS ERROR WITH IDENTICAL REGISTERS 2,

DEVICE INFORMATION
        REGISTERS:
        RX2CS               114560
        RX2DB               010400
        RX2ES               000120

        ACTIVE FUNCTION                  READ
        BLOCK                                     000001
        PHYSICAL BUFFER ADDRESS START   003734
        TRANSFER SIZE IN BYTES          512.
```

Table 16–1 explains each line in the sample report shown in Figure 16–3.

Table 16-1: Line-by-Line Analysis of the Sample Storage Device Error Report

| Line | Explanation |
| --- | --- |
| 1-4 | Report header. Includes the date and time error was logged. |
| 6-8 | Unit identification. Identifies the drive number, the device controller, and the storage device type. |
| 10-13 | Retry count. Line 11 shows the maximum number of retries the device handler can perform. Line 12 tells the number of retries left before the transfer fails. If the number of remaining retries is 0, the transfer has failed. If the number of remaining retries is not 0, this usually indicates that a soft error has occurred, or that the transfer failed and the registers differed. In this example, with 6 retries remaining, the report was generated on the second retry. Line 13 tells how many times the error occurred with the same register contents. |
| 15 | Labels the section on device information. The lines that follow provide statistics on the device registers and address information. |
| 16-19 | Register contents. Each device has a number of hardware registers, the contents of which are listed in these lines. |
| 21 | I/O transfer type. Tells whether the I/O transfer was a read or write operation. |
| 22 | Device block number. Tells which device block the error occurred in. |
| 23 | Physical buffer start address. Tells the physical address in memory of the user data buffer for this I/O transfer. |
| 24 | Transfer size in bytes. Tells the size in bytes of the unit of data the device handler has attempted to transfer. |

## 16.6.2 Memory Error Report

There are two kinds of memory errors for which the Error Logger creates reports: memory parity errors and cache memory errors. Figure 16–4 provides an example of a memory parity error report. As with the storage device report, this listing is numbered in the manual to aid in describing its contents. The listings that you obtain do not have line numbers.

## Figure 16-4: Sample Memory Parity Error Report

```asm
**************************
MEMORY PARITY ERROR
LOGGED 8-OCT-82 16:13:22
**************************
SOFTWARE STATUS INFORMATION:
        SYSTEM REGISTERS:
        PC    001026
        PSW   000000
        OCCURRENCES OF THIS ERROR WITH IDENTICAL PC  3,
```

```asm
DEVICE INFORMATION
    MEMORY REGISTERS:
    ADDRESS      CONTENTS
    172100       100001

    MEMORY SYSTEM ERROR REGISTER:   100000
    CACHE CONTROL REGISTER:     000000
    HIT/MISS REGISTER:         027000

    ERROR TYPE IS MEMORY
```

Table 16–2 tells what each line in the last report shown in Figure 16–4 means.

Table 16–2: Line-by-Line Analysis of the Sample Memory Error Report

| Line | Explanation |
| --- | --- |
| 1-4 | Report header. Tells the date and time the error was logged. |
| 7-10 | System register contents. Gives the contents of the program counter and the processor status word at the time of the error, as well as the number of times the program counter was the same for this error. |
| 13-15 | Memory parity register contents. Identifies your system's memory parity control and status register(s) and gives their contents. |
| 17-19 | Cache memory register contents. This information is displayed for both a memory parity error and a cache memory error if your system includes cache memory. See the PDP-11 Processor Handbook for more information on the cache memory registers. |
| 21 | Error type. Tells whether the error was a memory error or a cache memory error (see the following cache memory report for cache memory statistics). |

The report in Figure 16–5 is an example of the report the Error Logger creates when it logs a cache memory error.

## Figure 16-5: Sample Cache Memory Error Report

```asm
**************************
CACHE MEMORY ERROR
LOGGED 8-OCT-82 16:21:20
**************************
SOFTWARE STATUS INFORMATION:
        SYSTEM REGISTERS:
        PC   001026
        PSW   000000
        OCCURRENCES OF THIS ERROR WITH IDENTICAL PC 3,
DEVICE INFORMATION
        MEMORY REGISTERS:
        ADDRESS      CONTENTS
```

```asm
172100          100001

MEMORY SYSTEM ERROR REGISTER:      000200
CACHE CONTROL REGISTER:         000000
HIT/MISS REGISTER:               000032

ERROR TYPE IS CACHE
```

The description provided in Table 16–2 also applies to Figure 16–5. Line 21 indicates that the memory error was in cache memory.

## 16.6.3 Summary Error Report

The summary error report provides statistics for all the devices the Error Logger supports. These statistics include counts for successful and unsuccessful I/O transfers for storage devices, and error counts for memory errors. The report consists of three sections:

\- Device statistics

• Memory statistics

\- Report file environment and error count

Figure 16-6 provides an example of a summary error report.

Figure 16-6: Sample Summary Error Report for Device Statistics

```asm
**************************
DEVICE STATISTICS
LOGGED SINCE 8-OCT-82 16:01:12
**************************
UNIT IDENTIFICATION
    PHYSICAL UNIT NUMBER                                      000000
    TYPE                                      RL11/RL02/RL02

DEVICE STATISTICS FOR THIS UNIT:
    NUMBER OF ERRORS LOGGED          0,
    NUMBER OF ERROR RECEIVED         0,
    NUMBER OF READ SUCCESSES     65,
    NUMBER OF WRITE SUCCESSES      4,

UNIT IDENTIFICATION
    PHYSICAL UNIT NUMBER                                      000000
    TYPE                                      RX211/RX02

DEVICE STATISTICS FOR THIS UNIT:
    NUMBER OF ERRORS LOGGED          1,
    NUMBER OF ERRORS RECEIVED         1,
    NUMBER OF READ SUCCESSES     0,
    NUMBER OF WRITE SUCCESSES      0,

UNIT IDENTIFICATION
    PHYSICAL UNIT NUMBER                                      000001
    TYPE                                      RX211/RX02

DEVICE STATISTICS FOR THIS UNIT:
    NUMBER OF ERRORS LOGGED          0,
    NUMBER OF ERRORS RECEIVED         0,
    NUMBER OF READ SUCCESSES     2,
    NUMBER OF WRITE SUCCESSES      0,
```

The Error Logger provides summary statistics for each device. Notice that for each device, the count of the number of errors logged and the count of the number of errors received can be different. Sometimes, the Error Logger may receive an error but be unable to log it. This is usually due to full buffers or some other momentary software limitation. However, even if the Error Logger is unable to log an error, it is at least able to inform you of this fact.

Figure 16–7 provides an example of the second section of the summary error report, memory statistics. This report immediately follows the report on device statistics.

## Figure 16–7: Sample Summary Error Report for Memory Statistics

```txt
**************************
MEMORY STATISTICS
LOGGED SINCE 8-OCT-82 16:01:12
**************************
STATISTICS:
    NUMBER OF MEMORY PARITY ERRORS          3,
    NUMBER OF CACHE ERRORS                  0,
```

Figure 16–8 provides an example of the third section of the error report summary, the report file environment and error count.

## Figure 16-8: Sample Report File Environment and Error Count Report

```txt
REPORT FILE ENVIRONMENT:
        INPUT FILE            DLO:ERRLOG,DAT
        OUTPUT FILE          LP :      ,LST
        OPTIONS                  /A
        DATE INITIALIZED         8-OCT-82
        DATE OF LAST ENTRY       8-OCT-82

TOTAL ERRORS LOGGED                          15,
MISSED REPORTS (TASK NOT READY)               11,
MISSED REPORTS (BUFFER FULL)                   0,
MISSED REPORTS (FILE FULL)                   0,
UNKNOWN DEVICE STATISTICS ENTRIES                 0,
UNKNOWN ERROR RECORD ENTRIES                   0,
```

The segment of the report file environment shown in Figure 16–8 provides information concerning the input report file name (usually ERRLOG.DAT or ERRLOG.TMP) and the output report file name (any name that you specify in the initial ERROUT command line). In line 5, the report tells when the input report file was initialized, and in line 6, the date of the last error entry to the input report file.

Lines 8 through 13 count additional error count statistics. Lines 9 through 11 count the number of missed reports. A missed report is an I/O transfer or error for which the Error Logger was unable to gather information because ERRLOG was running but ELINIT had not been run, the internal buffer was full, or the ERRLOG.DAT statistics file was full.

Line 12 provides a count of unknown device statistics entries. An unknown device statistics entry occurs when ERROUT does not recognize the device identifier byte the EL program recorded in the statistics portion of the ERRLOG.DAT file. (All DIGITAL-distributed device handlers that support Error Logging can be identified by ERROUT, so this problem occurs most often with user-written handlers. See the RT-11 Software Support Manual for details on adding a device to ERROUT.)

Line 13 keeps a count of the unknown error record entries. This condition occurs when the ERROUT task cannot identify a device error recorded in the ERRLOG.DAT file. (Again, this condition occurs most often with user-written handlers.)
