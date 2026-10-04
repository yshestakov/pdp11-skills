# RT-11 System Utilities Manual: Ch.18 SPOOL transparent spooling package

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 18.1 SPOOL Components
- 18.2 Running SPOOL
- 18.2.1 Loading the Line Printer Handler
- 18.2.2 Running the SPOOL Program
- 18.2.3 Assigning a Logical Name to SP
- 18.3 SPOOL Work File
- 18.4 SPOOL Output Device
- 18.5 Starting SPOOL from an Indirect Command File
- 18.6 SPOOL Set Commands
- 18.7 SPOOL Status
- 18.8 SPOOL Flag Pages

---

# Transparent Spooling Package (SPOOL)

The transparent spooling package (SPOOL) is a utility you can use for sending files to any RT-11 device. Although SPOOL is especially useful for spooling files for printing, the output device is not restricted to the line printer, but must be a serial non-file-structured device. SPOOL is distributed with two default output devices, LP and LS, but you can change the default output device by applying the customization in Section 18.4.

SPOOL is functionally similar to the Queue Package. However, use of the transparent spooling package is, as its name implies, transparent. Once running, SPOOL automatically intercepts all data directed to the line printer or other designated output device, stores it, then forwards it to the line printer or output device. You can send output to the line printer explicitly, by typing a command such as COPY MYFIL.MAC LP:, or implicitly by typing a command whose default is to send output to the line printer, such as MACRO/LIST MYFIL. In either case, you need not type a specific command to spool output, as is necessary when you use the Queue Package.

Another major advantage to using SPOOL is that SPOOL begins sending output as it is received. The Queue Package must wait until a complete file is available before it can begin sending output. Therefore, using SPOOL can be considerably faster than using QUEUE.

## 18.1 SPOOL Components

The transparent spooling package consists of a program, a pseudo-device handler, and a work file:

SPOOL.REL Gathers output directed to the line printer or other output device, stores (spools) it in a work file, and sends the output to the line printer or other designated output device. SPOOL runs as a foreground or system job.

SP A pseudo-device handler for SPOOL. The handler file is SP.SYS for the FB monitor and SPX.SYS for the XM monitor.

SPOOL.SYS The work file where SPOOL stores output before sending it to the line printer or other output device.

When output it directed to the line printer, the SP pseudohandler causes SPOOL to receive the data and spool it in the work file SPOOL.SYS. As soon as one block of information is available in SPOOL.SYS, SPOOL begins sending the output to the line printer. Since SPOOL runs as a foreground or system job, you can continue working in the background while files are spooled and printed.

## 18.2 Running SPOOL

To use SPOOL, you must make sure the output device's handler is loaded, run the SPOOL program as a foreground or system job, and assign the SP pseudohandler the name of the output device as a logical name. System job support is a special feature available through the system generation process.

The following sections describe the commands you must issue to run SPOOL. You can include the commands in your start-up indirect command files so SPOOL is automatically available whenever you run under the FB or XM monitor.

## 18.2.1 Loading the Line Printer Handler

Use the SHOW command to see if the LP handler is loaded. If it is not, load the LP handler by typing this command:

• LOAD LPRET

If you are running on a Professional 300 series computer, or you have a serial-line printer, load the LS handler instead:

• LOAD LSRET

If you customize your system to use an output device other than the line printer, substitute your output device's mnemonic for LP or LS.

You need not load the SP handler itself.

## 18.2.2 Running the SPOOL Program

You can run SPOOL as a foreground or system job. If you are running under the FB monitor, you must set the USR to NOSWAP (SET USR NOSWAP) before running SPOOL. After you issue the command to run SPOOL, you can allow the USR to swap (SET USR SWAP). Under the XM monitor, you need not set the USR to NOSWAP to run SPOOL.

To run SPOOL as a foreground job, type this command:

• FRUN SPOOL/BUF:256, RET

To run SPOOL as a system job, type this command:

\- SRUN SPOOL/BUF:256.RET

The FRUN command assumes SPOOL.REL is on the default volume (DK:). The SRUN command assumes SPOOL.REL is on the system volume (SY:). If SPOOL.REL is on another volume, include the device mnemonic in the command (ddn:SPOOL).

## . NOTE

The option /BUF:256. should not be included in the command to run SPOOL when running under the XM monitor. SPOOL will allocate working space in extended memory.

## 18.2.3 Assigning a Logical Name to SP

In order for SPOOL to work transparently, you must assign the device mnemonic of the line printer as a logical name for SP, the SPOOL pseudohandler. This causes SP to intercept output directed to the line printer.

To assign LP as the logical device name, type this command:

\- ASSIGN SPO: LP:

To ensure that logical LP: and LP0: are the same, also type this command:

• ASSIGN SPO: LPO:

If you want SPOOL to intercept output directed to another physical device, assign that device's mnemonic as SP's logical device name. For example, if you want SPOOL to intercept all output directed to LS, make the following logical assignment:

\- ASSIGN SPO: LS:

## 18.3 SPOOL Work File

SPOOL attempts to create its work file, SPOOL.SYS, on the device whose logical name is SFD (spool file device). If you have not assigned the logical name SFD to any device, SPOOL creates SPOOL.SYS on the system volume.

SPOOL allocates by default 1000(decimal) blocks on SFD: or SY: for its work file SPOOL.SYS. You can change the default size of SPOOL.SYS by applying the software customization located in Section 2.7.52 of the RT-11 Installation Guide.

If there is not enough room on the volume for a work file of the default size, SPOOL.SYS occupies the largest empty area on the volume.

Do not squeeze the volume on which SPOOL.SYS resides while spooling is in progress. SPOOL.SYS may be moved, causing unpredictable results.

## 18.4 SPOOL Output Device

SPOOL attempts to send output to the device whose logical name is SO0. If you have not assigned the logical name SO0 to any device, SPOOL sends output to the line printer LP. If LP is not installed on your system, SPOOL sends output to the line printer LS.

You can change SPOOL's default output device to any other RT-11 non-file-structured device by installing the software customization located in Section 2.7.53 of the RT-11 Installation Guide.

You cannot cause SPOOL to send output to another device by assigning the logical name LP to the device. SPOOL bypasses the logical translation and finds physical LP instead.

## 18.5 Starting SPOOL from an Indirect Command File

If you want SPOOL to run automatically whenever you run RT-11, include a sequence of commands like the following in your start-up indirect command file. These commands run SPOOL as a foreground job under the FB monitor.

```dockerfile
FRUN SY:SPOOL/BUF:256./PAUSE
*ASSIGN LS: LP:
LOAD LP:=F
SET USR NOSWAP
RESUME
ASSIGN SPO LP
ASSIGN SPO LPO
SET USR SWAP
```

\* Enter this command line only when using a Professional 300 series processor.

## 18.6 SPOOL Set Commands

Although SPOOL operates transparently, you can use SET commands to control spooling operations. The following table lists and explains the SET command options for SPOOL. Most of these options require you to specify the unit number 0 (SET SP0), because SPOOL as distributed supports only one output device at a time.

Type the SET command in response to the keyboard monitor prompt (.). You can set several conditions on a single command line by separating the conditions with commas. For example:

\- SET SPO WIDE,FLAG=3

This command sets SPOOL to generate 132-column banner pages, and sets the default number of banner pages to 3.

You must unload SP and load a fresh copy for a SET command to take effect.

Option
Function

SP0 FLAG = n Sets the number of banner pages to generate whenever SPOOL begins printing a file. The value n can be any integer in the range 0 to 4. The default value for n is 0.

SP0 FORM0 Issues a form feed each time SPOOL encounters block 0 of a file to be printed; useful if the output device is part of a multiterminal system, or if the output device handler does not support its own FORM0 option. The default mode is NOFORM0.

## NOTE

Setting SP0 and either LS or LP to FORM0 simultaneously generates multiple form feeds.

SP0 NOFORM0 Turns off FORM0 mode. This is the default mode.

SP0 KILL Removes all spooled output from SPOOL's work file.

SP0 NEXT Stops printing the current file, discards the remaining spooled output for that file, and begins printing the next listing in SPOOL's work file.

SP0 WAIT Suspends sending output from SPOOL's work file to the output device, but does not delete anything from the work file. SPOOL continues to accept input when SET SP0 WAIT is in effect.

SP0 NOWAIT Resumes sending spooled output suspended by the command SET SP0 WAIT.

SP0 WIDE Causes SPOOL to generate 132-column flag pages. This is the default setting.

SP0 NOWIDE Causes SPOOL to generate 80-column flag pages.

## 18.7 SPOOL Status

You can check the spooler's status by using the SHOW QUEUE command. The SHOW QUEUE command tells whether or not the spooler is active, and gives the number of blocks spooled for output and the number of blocks in the SPOOL work file free for spooling.

The following is an example of the SHOW QUEUE display.

```txt
• SHOW QUEUE
Unit O status
Device is active
00045 blocks are spooled for output
00954 blocks are free to be spooled
```

If QUEUE is running, the SHOW QUEUE command prints a QUEUE status report as well.

## 18.8 SPOOL Flag Pages

SPOOL flag page support is included in the distributed monitors. However, SPOOL generates flag pages only after you issue the command SET SP0 FLAG=n. This command causes SPOOL to print that number (n) of flag pages for all files subsequently spooled for printing, unless the files are spooled without an associated file name. For example, the command .PIP LP:=MYFIL.MAC sends output to the line printer without an associated file name, so no flag pages would be generated.

You can exclude SPOOL flag page support through system generation. Excluding SPOOL flag page support saves 927(decimal) words in the monitor.
