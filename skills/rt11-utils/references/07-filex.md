# RT-11 System Utilities Manual: Ch.7 FILEX file exchange: DOS-11, interchange (RX01), DECtape formats

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 7.1 File Formats
- 7.2 Calling and Terminating FILEX
- 7.3 Options
- 7.3.1 Transferring Files Between RT-11 and DOS/BATCH or RSTS (/S)
- 7.3.2 Transferring Files Between RT-11 and Interchange Diskette (/U)
- 7.3.3 Transferring Files to RT-11 from DECsystem-10 (/T)
- 7.3.4 Listing Directories (/L)
- 7.3.5 Deleting Files from DOS/BATCH (RSTS) DECTapes and Interchange Diskettes (/D)
- 7.3.6 Initializing the Directories of DECtapes and Interchange Diskettes (/Z)
- 7.3.7 Interchange Diskette Volume ID Option (/V[:ONL])
- 7.3.8 Wait Option (W)

---

# Chapter 7 File Exchange Program (FILEX)

The file exchange program (FILEX) is a general file transfer program that converts files from one format to another so that you can use them with various operating systems. You can copy files between any block-replaceable RT-11 directory-structured device and any device listed in Table 7-1.

Table 7-1: Supported FILEX Devices

| Device | Valid as Input | Valid as Output |
| --- | --- | --- |
| PDP-11 | X | X |
| DOS/BATCH DECtape |  |  |
| DOS/BATCH disk | X |  |
| RSTS | X | X |
| DECtape |  |  |
| DECsystem-10 | X |  |
| DECtape |  |  |
| Interchange diskette (RX01, RX02 single-density, PDT-11/150) | X | X |

FILEX does not support magtapes, cassettes, or double-density diskettes in any operation. Note that you can transfer only one file at a time to interchange diskette format.

Section 4.2 of the RT-11 System User's Guide describes how to use wildcards, which you can use in the FILEX command string. The default device for all FILEX operations is DK:. You can use wildcards when transferring from interchange to RT-11 format. However, you cannot use embedded wildcards in any file name or file type. For example, the following line represents a valid file specification.

\* \*.MAC

The next line is an invalid file specification for FILEX.

\* T%ST, MAC

## 7.1 File Formats

FILEX can transfer files created by four different operating systems: RT-11, DECsystem-10, universal interchange format (IBM) system (see the RT-11 Software Support Manual), and DOS/BATCH (PDP-11 Disk Operating System). You can use the following three data formats in a transfer: ASCII, image, and packed image. ASCII files conform to the American Standard Code for Information Interchange in which each character is represented by a 7-bit code. In ASCII mode, FILEX deletes null and rubout characters, as well as parity bits:

## NOTE

If you attempt to use RT-11 volumes for both input and output, FILEX generates an error message.

Because the file structure and data formats for each system vary, options are needed in the command line to indicate the file-structures and the data formats involved in the transfer. These options are discussed in Section 7.3. FILEX assumes that all devices are RT-11-structured. You can use options to indicate otherwise.

## 7.2 Calling and Terminating FILEX

To call FILEX from the system device, respond to the keyboard monitor prompt by typing:

. R FILEX RET

The Command String Interpreter (CSI) prints an asterisk at the left margin of the terminal and waits for you to enter a command.

Type CTRL/C to halt FILEX when it is waiting for console terminal input and return control to the monitor. To restart FILEX, type R FILEX or REENTER in response to the monitor's dot.

## 7.3 Options

Table 7–2 lists the options that initiate various FILEX operations. The table contains four categories: transfer, operation, modifier, and device.

## 7-2 File Exchange Program (FILEX)

Transfer options direct FILEX to copy data in a certain mode. The three transfer modes are: ASCII, image, and packed image.

Operation options perform other functions in addition to the data transfer. These additional functions include deleting files, producing listings, and zeroing device directories. FILEX accepts one transfer option and one operation option in a single command.

Modifier options cause transfers and operations to be performed in a certain manner. For example, when you use the /Y option to modify the /Z option, FILEX suppresses the /Init are you sure? message. There are three modifier options: /V[:ONL], /W and /Y.

Device options indicate the formats of devices that are involved in a transfer. These formats are DOS/BATCH or RSTS, DECsystem-10, and interchange. You can specify one device option for each file involved in the transfer. The device options (/S, /T, and /U) must appear following the device and file name to which they apply; other options may appear anywhere in the command line. These options are explained in more detail in the sections following Table 7–2.

Table 7-2: FILEX Options

<table><tr><td>Options</td><td>Function</td></tr><tr><td colspan="2">Transfer</td></tr><tr><td>/A</td><td>Indicates a character-by-character ASCII transfer in which FILEX deletes rubouts and nulls. If you use /U with /A, FILEX also ignores all sector boundaries on the diskette and assumes that records are to be terminated by a line feed, vertical tab, or form feed. If you use /A with /T, FILEX assumes that each PDP-10 36-bit word contains five 7-bit ASCII bytes. The transfer terminates when a CTRL/Z is encountered. (This feature is included for compatibility with RSTS.) FILEX does not transfer the CTRL/Z.</td></tr><tr><td>/I</td><td>Performs an image mode transfer. If the input is DOS/BATCH, RSTS, or RT-11, the transfer is word-for-word. If the input is from DECsystem-10, /I indicates that the file resembles a file created on DECsystem-10 by MACY11, MACX11, or LNKX11 with the /I option. In this case, each PDP-10 36-bit word will contain one PDP-11 8-bit byte in its low-order bits. If input or output is an interchange diskette, FILEX reads and writes four diskette sectors for each RT-11 block.</td></tr><tr><td>/P</td><td>Performs a packed image mode transfer. If the input is DOS/BATCH, RSTS, or RT-11, the transfer will be word-for-word. If the input is from DECsystem-10, /P indicates that the file resembles a file created on DECsystem-10 by MACY11, MACX11, or LNKX11 with the /P option. In this case, each PDP-10 36-bit word will contain four PDP-11 8-bit bytes aligned on bits 0, 8, 18, and 26. This is the default mode. If the output is interchange diskette, FILEX writes the data as EBCDIC.</td></tr><tr><td colspan="2">Operation</td></tr><tr><td>/D</td><td>Deletes the file you specify from the device directory. This option is valid only for DOS/BATCH, RSTS DECtape, and interchange diskette.</td></tr><tr><td>/F</td><td>Produces a brief listing of the device directory on the terminal. It lists only file names and file types. FILEX can only list directories of block-replaceable devices, and those directories only on the console terminal.</td></tr><tr><td>/L</td><td>Produces a complete listing of the device directory on the console terminal, including file names, block lengths, and creation dates.</td></tr><tr><td>/Z</td><td>Initializes the directory of the device you specify. This option is valid only for DOS/BATCH, RSTS DECtape, and interchange diskette.</td></tr><tr><td colspan="2">Modifier</td></tr><tr><td>/V[:ONL]</td><td>/V is used with /Z and /U[:n] together to write a volume identification on an interchange diskette during initialization. A volume identification can be up to six characters long. Using /V:ONL with /Z and /U[:n] changes only the ID and does not initialize the interchange diskette. You can also use /V[:ONL] with /F or /L to list the volume identification of an interchange diskette as well as its directory.</td></tr><tr><td>/W</td><td>Transfers files in a single- or small-disk system. FILEX initiates the transfer, but pauses and waits for you to mount the volumes involved in the transfer.</td></tr><tr><td>/Y</td><td>Used with /Z to suppress the dev:/Init are you sure? message.</td></tr><tr><td colspan="2">Device</td></tr><tr><td>/S</td><td>Indicates that the device is a valid DOS/BATCH or RSTS block-replaceable device.</td></tr><tr><td>1/T</td><td>Indicates that the device is a valid DECsystem-10 DECtape.</td></tr><tr><td>/U[:n.]</td><td>Indicates that the device is an interchange diskette. The symbol n. represents the length of each output record, in characters. The argument n. is a decimal integer in the range 1-128. The default value is 80; n. is not valid with an input file specification, or with /A or /I.</td></tr></table>

## 7.3.1 Transferring Files Between RT-11 and DOS/BATCH or RSTS (/S)

You can transfer files between block-replaceable devices used by RT-11 and the PDP-11 DOS/BATCH system. Input from DOS/BATCH may be either disk or DECtape. You can use both linked and contiguous files.

If the input device is a DOS/BATCH disk, you should specify a DOS/BATCH user identification code (UIC) in the form [nnn,nnn]. The initial default value is [1,1]. The UIC you supply will be the default for all future transfers.

If you do not specify a UIC, FILEX will use the current default UIC. Note that the square brackets ([ ]) are part of the UIC; you must type them when you specify a UIC.

Output to DOS/BATCH is limited to DECtape only. You do not need a UIC in a command line where you are accessing only DECtape. Individual users do not own files on DECtape under DOS. However, no error occurs if you do use a UIC. DECtape used under the RSTS system is valid as both input and output, since its format is identical to DOS/BATCH DECtape. You may use any valid RT-11 file storage device for either input or output in the transfer. The RT-11 device DK: is assumed if you do not indicate a device.

An RT-11 DECtape can hold more information than a DOS/BATCH or RSTS DECtape. When you copy files from a full RT-11 tape to a DOS DECtape, some information may not transfer. In this case, an error message prints and the transfer does not complete.

When a transfer from an RT-11 device to a DOS DECtape occurs, the block size of the file can increase. However, if the file is later transferred back to an RT-11 device, the block size does not decrease.

To transfer a file from a DOS/BATCH block-replaceable device or RSTS DECtape to an RT-11 device, type a command with the following syntax:

output-filespec = input-filespec/S[/option]

where:

output-filespec represents any valid RT-11 device, file name, and file type (if the device is not file structured, you may omit the file name and file type).

input-filespec represents the DOS/BATCH or RSTS device, UIC, file name, and file type to be transferred. (See Table 7-1 for a list of valid devices.)

/S is the option that designates a DOS/BATCH or RSTS block-replaceable device. (This option must be included in the command line.)

/option is one of the three transfer options from Table 7-2, and the /W modifier option if necessary.

To transfer files from an RT-11 storage device to a DOS/BATCH or RSTS DECtape, type a command with the following syntax:

DTn:output-filename/S[/option] = input-filespec

where:

DTn:output-filename represents the file name and file type of the file to be created, as well as the DOS/BATCH or RSTS DECtape on which to store the file.

input-filespec represents the device, file name, and file type of the RT-11 file to be transferred.

is the option that designates a DOS/BATCH or RSTS DECtape. (This option must be included in the command line.)

/option

is one of the three transfer options from Table 7-2, and the /W modifier option if necessary.

The following examples illustrate the use of the /S option.

The following command instructs FILEX to transfer a file called SORT.ABC from the RT-11 default device DK: to a DECTape in DOS/BATCH or RSTS format on unit DT2. The transfer is in image mode.

\* DT2:SORT,ABC/S=SORT,ABC/I

The next command allows a file to be transferred from DOS/BATCH (or RSTS) DECtape to the line printer under RT-11. The transfer is done in ASCII mode.

\* LP := DT2: FIL, TYP/S/A

The next command causes the file MACR1.MAC to be transferred from the DOS/BATCH disk on unit 1, stored under the UIC [1,2], to the RT-11 device DK:. [1,2] becomes the default UIC for any further DOS/BATCH operations.

\* DK: \*, \*=RK1:[1,2]MACR1.MAC/S

## 7.3.2 Transferring Files Between RT-11 and Interchange Diskette (/U)

You can transfer files between block-replaceable devices used by RT-11 and interchange format diskettes. Files are transferred in one of three formats: ASCII, image, and packed image EBCDIC mode.

A universal diskette consists of 77 tracks (some of which are reserved), each containing 26 sectors numbered from 1 to 26. A sector contains one record of 128 or fewer characters. When an interchange diskette is in packed image mode, records always begin on a sector boundary. There is only one record per sector. If a record does not fill a sector, the remainder is filled with blanks. Since packed image EBCDIC mode is inefficient and wastes space, packed image mode is recommended only to read or write diskettes that must be compatible with IBM 3741 format. Packed image (EBCDIC) mode is generally compatible with IBM 3741 format. (Although IBM 3741 format supports error mapping of bad sectors and multivolume files, FILEX does not.) Packed image (EBCDIC) is the default mode, so you must use one of the options from Table 7–2 to specify ASCII or image mode. All records of a file must be the same size. You indicate this with the /U:n. option.

## NOTE

File types are not usually recognized in interchange format; instead, a single, 8-character file name is used. However, in order to provide uniformity throughout RT-11, FILEX has been designed to accept a 6-character file name with a 2-character file type. If you transfer a file from RT-11 to interchange diskette, any 3-character file type is truncated to two characters.

To transfer files from RT-11 format to interchange format, type a command with the following syntax:

output-filespec/U[:n.][/option] = input-filespec

where:

output-filespec represents the device, file name, and file type of the interchange file to be created. Note that you cannot use wildcards in the output file specification.

/U[:n.] is the option that designates an interchange diskette. This option must be included in the command line. The argument n. represents the length of each output record, in characters; n is a decimal integer in the range 1 to 128 (default is 80). The argument n is invalid with either /A or /I.

/option is one of the three transfer options from Table 7-2, and the /W modifier option if necessary.

input-filespec represents the device, file name, and file type of the RT-11 file to be transferred. The file name is six characters long, with a 2-character file type. Any 3-character file type is truncated to two characters.

To transfer files from interchange diskette to RT-11 format, type a command with the following syntax:

output-filespec = input-filespec/U[/option]

where:

output-filespec represents the device, file name, and file type of the RT-11 file to be created. Note that you can use wild-cards as input.

input-filespec represents the device, file name, and file type of the interchange file to be transferred.

/U is the option that designates an interchange diskette. (This option must be included in the command line.)

/option is one of the three transfer options from Table 7-2, and the /W modifier option if necessary.

The following command transfers the file IVAN.CAT from RT-11 RK05 unit 2 to the diskette on unit 1. The transfer is done in exact image mode (indicated by /I), ignoring all sector boundaries.

\* DX1: IVAN, CA/U/I = RK2: IVAN, CAT

The next command instructs FILEX to transfer the file BENMAR.FRM from the RT-11 disk unit 2 to the diskette on unit 0, and rename it KENJOS.JO. The /U option indicates that the format is to be changed from ASCII to the interchange format. There will be one record per sector of 128 or fewer characters. If there are fewer than 128 characters, the remainder of the sector will be filled with spaces.

\* DXO:KENJOS.JO/U=RK2:BENMAR.FRM

The next command transfers the file TYPE.SET from RT-11 diskette unit 0 to the interchange diskette on unit 2. The exchange converts ASCII to interchange format, putting a maximum of seven (indicated by :7.) characters into each sector until the entire record has been transferred. Records in excess of seven characters will be broken up and placed in succeeding sectors on the diskette. New records always begin on a sector boundary; carriage returns and line feeds are discarded. However, if you use /A or /I, FILEX ignores boundary limits and preserves carriage returns and line feeds.

\* DX2:TYPE,SE/U:7.=DX0:TYPE,SET

File TYPE.SET before transfer:

## ABCDEFGHIJKLMNOPQRSTUVWXYZ

File TYPE.SET after transfer:

ABCDEFG----(spaces up to 128 characters) Sector 1
HIJKLMN----(spaces up to 128 characters) Sector 2

The next command copies file IVAN.CA from the interchange diskette on unit 1 to the RT-11 line printer, treating the input as ASCII characters. Note that once a record has been divided into sectors, it cannot be transferred back to its original size.

\* LP:=DX1:IVAN.CA/U/A

## 7.3.3 Transferring Files to RT-11 from DECsystem-10 (/T)

Output may be to any valid RT-11 device. DECsystem-10 DECtape is the only valid input device.

To transfer files from DECsystem-10 format to RT-11 format, use this command syntax:

output-filespec = input-filespec/T[/option]

where:

output-filespec represents any valid RT-11 device, file name, and file type. (If the device is not file-structured, you can omit the file name and file type.)

input-filespec represents the DECtape unit, file name, and file type of the DECsystem-10 file to be transferred.

/T is the option that signifies a DECsystem-10 DECtape (When you use /T, and especially when you also use /A, the system clock loses time. Examine the time, and reset it if necessary with the TIME command.)

/option is one of the three transfer options from Table 7-2, and the /W modifier option if necessary.

You cannot convert RT-11 files to DECsystem-10 format directly. However, there is a two-step procedure for doing this. First, run RT-11 FILEX and convert the files to DOS formatted DECtape. Then run DECsystem-10 FILEX to read the DOS DECtape.

The following command converts the ASCII file STAND.LIS from DECsystem-10 ASCII format to RT-11 ASCII format and stores the file under RT-11 on DECtape unit 2 as STAND.LIS.

\* DT2:STAND.LIS=DT1:STAND.LIS/T/A

Transfers from DECsystem-10 DECtape to RT-11 may cause an &lt;UNUSED&gt; block to appear after the file on the RT-11 device. This is a result of the way RT-11 handles the increased amount of information on a DECsystem-10 DECtape.

The next command indicates that all files on the DECsystem-10 formatted DECtape on unit 0 with the file type .LIS are to be transferred to the RT-11 system device using the same file name and a file type of .NEW. The /P option is the assumed transfer mode.

\* SY:\*,NEW=DTO:\*,LIS/T

Files may not be transferred to RT-11 devices from a DECsystem-10 DECtape if a foreground job is running. This restriction is due to the fact that when FILEX reads DECsystem-10 files, it accesses the DECtape control registers directly instead of using the RT-11 DECtape handler.

## 7.3.4 Listing Directories (/L)

You can list at the terminal a directory of any of the block-replaceable devices used in a FILEX transfer. The command syntax is:

device:/L/option

where:

device represents the block-replaceable device. These are the valid device types:

DOS/BATCH, RSTS DTn:, RKn:

DECsystem-10 DTn:

Interchange diskette DXn: DYn:

/L is the listing option. (You can substitute /F if you want a brief listing of file names only.)

/option is /S, /T, or /U, and the /W modifier option if necessary. These are the valid format and option combinations:

DOS/BATCH, RSTS /S

DECsystem-10/T

Interchange diskette /U

The following example shows the complete disk directory for UIC[1,7] of the device RK1:. The letter C following the file size on a DOS/BATCH or RSTS directory listing indicates that the file is contiguous.

```asm
* RK1:/L/S
 18-FEB-83
BADB     .SYS      1       18-FEB-83
MONLIB   .CIL    175C     18-FEB-83
DU11     .PAL     45       18-FEB-83
VERIFY    .LDA      67C     18-FEB-83
CILUS     .LDA      39       18-FEB-83
```

The next example is a command that lists all files with the file type .PAL that are stored on DECtape unit 1.

```csv
* DT1:*,PAL/L/S
```

The next command produces a brief directory listing of the interchange diskette on unit 0, giving file names only.

```txt
* DXO:/U/F
```

The following command lists all files on the DECsystem-10 formatted DECtape on unit 1, regardless of file name or file type; with the /F, a brief directory is requested in which only file names print.

```txt
* DT1:*,*/F/T
```

## 7.3.5 Deleting Files from DOS/BATCH (RSTS) DECTapes and Interchange Diskettes (/D)

Use FILEX to delete files from DOS/BATCH and RSTS formatted DECtapes, and from interchange diskettes.

To delete files, type a command with the following syntax:

filespec/D/option

where:

filespec represents the device, file name, and file type of the file to be deleted.

/D is the delete option.

/option can be either /S, for DOS/BATCH and RSTS block-replaceable devices, or /U, for interchange diskettes. You can also include the /W modifier option, if necessary.

The following command deletes all files with the file type .PAL on DECtape unit 0.

\* DTO:\*.PAL/D/S

The next command deletes the file TABLE.OBJ from the DECtape on unit 2.

\* DT2: TABLE.OBJ/D/S

The next command deletes all files with an .RNO file type from the interchange diskette on unit 0.

\* DXO:\*,RN/D/U

## 7.3.6 Initializing the Directories of DECtapes and Interchange Diskettes (/Z)

You can also use FILEX to initialize the directories of DOS/BATCH DECTapes, RSTS DECTapes, and interchange diskettes.

Use this command syntax:

device:/Z/option[/Y]

where:

device represents the DOS/BATCH or RSTS DECtape, or the interchange diskette to, be zeroed.

/Z is the initialize option.

/option can be either /S, for DOS/BATCH and RSTS DECTapes, or /U, for interchange diskettes. You can also include the /W modifier option, if necessary.

/Y inhibits the FILEX confirmation message.

The following command directs FILEX to initialize the directory of the interchange diskette on unit 0.

\* DXO: /Z/U

FILEX prints a confirmation message:

DXO:/Initialize; are you sure?

Respond with a Y or any string beginning with Y followed by a carriage return for initialization to begin. Any other response aborts the command.

The next command initializes the DECtape on unit 1 in DOS/BATCH (RSTS) format. Note that by using the /Y option you suppress the confirmation message.

```txt
* DT1:/Z/S/Y
```

## NOTE

The directory of an initialized interchange diskette has a single file entry, DATA, that reserves the entire diskette. You must delete this file before you can write any new files on the diskette. This is necessary for IBM compatibility. Do this by using the following command:

\* DXO:DATA/D/U

## 7.3.7 Interchange Diskette Volume ID Option (/V[:ONL])

The /V option enables you to write a volume identification on an interchange diskette when it is initialized. This option is used with the /U[:n] and /Z options together. You can also use /V[:ONL] with /L or /F to list a volume ID.

When you use this option, FILEX prompts you for a volume ID. Respond by typing a volume identification of up to six characters. Any string over six characters is truncated. If you type only a carriage return in response to the volume ID prompt, the default volume ID RT11A is written on the interchange diskette.

Use /V:ONL to change only the volume ID without initializing the interchange diskette.

The following command initializes an interchange diskette and writes a volume identification:

\* DXO:/Z/U/V
Volume ID? Nancy

The next command changes only the volume ID of an interchange diskette.

```txt
* DXO:/Z/U/V:ONL
Volume ID change; are you sure? Y
Volume ID? Nancy
```

## 7.3.8 Wait Option (W)

The /W option permits you to replace the system volume with another volume during an operation. You can use the /W option for a delete, directory listing, and initialization operation on a single-disk system, or to copy files between volumes when the system volume is neither the input nor the output volume if you have two drives available. When you use the /W option, you cannot use wildcards in the input specification.

When you use the /W option, FILEX guides you through a series of steps in the process of completing the operation. After you enter the initial command string, FILEX prints a message telling you which volume to mount. After you complete each step, type Y or any string beginning with Y followed by a carriage return to proceed to the next step. If you type N or any string beginning with N, or CTRL/C, FILEX prompts you to mount the system volume if you have removed it and the operation is not performed. Any other response causes the message to repeat.

When the operation is complete, FILEX prints a message instructing you to mount your system volume. Mount the system volume and type Y or any string beginning with Y followed by a carriage return. If you type any other response, FILEX prompts you to mount the system volume until you type Y.

When you use /W, make sure that FILEX is on your system volume.

The procedure for copying files with /W follows:

With your system volume mounted, enter a command string according to the FILEX syntax. After you have entered the command string, FILEX responds with the message:

Mount input volume in &lt;device&gt;; Continue?

Type Y or any string beginning with Y followed by a carriage return to continue the operation when you have mounted the input volume. FILEX then prints:

Mount output volume in &lt;device&gt;; Continue?

Type Y or any string beginning with Y followed by a carriage return to continue the operation after you have mounted the output volume.

When the file transfer is complete, FILEX prints the following message if you had to remove the system volume from &lt;device&gt;:

Mount system volume in &lt;device&gt;; Continue?

Type Y or any string beginning with Y followed by a carriage return to terminate the copy operation. If you type any other response, FILEX prompts you to mount the system volume until you type Y.

(1)
