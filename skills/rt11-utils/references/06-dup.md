# RT-11 System Utilities Manual: Ch.6 DUP device utility: INIT, SQUEEZE, BOOT, COPY/DEVICE images, bad block scan, CREATE, volume ID

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 6.1 Calling and Terminating DUP
- 6.2 DUP Command String Syntax
- 6.3 Options
- 6.3.1 Create Option (/C[/G:n])
- 6.3.2 Image Copy Option (/I)
- 6.3.3 Bad Block Scan Option (/K)
- 6.3.4 File Option (/F)
- 6.3.5 Boot Option (/O)
- 6.3.6 Boot Foreign Volume Option (/Q)
- 6.3.7 Squeeze Option (/S)
- 6.3.8 Extend Option (/T:n)
- 6.3.9 Bootstrap Copy Option (/U[:xx])
- 6.3.10 Volume ID Option (/V[:ONL])
- 6.3.11 Wait for Volume Option (/W)
- 6.3.12 No Query Option (/Y)
- 6.3.13 Directory Initialization Option (/Z[:n])

---

## Chapter 6 Device Utility Program (DUP)

The device utility program (DUP) is a device maintenance program that creates files on file-structured RT-11 devices (disks, single- and double-density diskettes, DECtape II, and magtape). It can also extend files on certain file-structured devices (disks, single- and double-density diskettes, and DECtape II), and it can compress, image copy, initialize, or boot RT-11 file-structured devices. DUP does not operate on non-file-structured devices (line printer, terminal).

## 6.1 Calling and Terminating DUP

To call DUP from the system device, respond to the dot (.) printed by the keyboard monitor by typing:

• R DUP RET

The Command String Interpreter (CSI) prints an asterisk (\*) at the left margin of the terminal and waits for you to type a command string. If you enter only a carriage return at this point, DUP prints its current version number and prompts you again for a command string. You can type CTRL/C to halt DUP and return control to the monitor when DUP is waiting for input from the console terminal. You must type two CTRL/Cs to abort DUP at any other time. Note that the /S, /T, and /C operations lock out the CTRL/C command until the operation completes; these three operations cannot be interrupted with CTRL/C. To restart DUP, type R DUP or REENTER in response to the monitor's dot.

## 6.2 DUP Command String Syntax

Chapter 1, Command String Interpreter, describes the general syntax of the command line that DUP accepts. DUP accepts only one input file specification and one output file specification in the command line.

## 6.3 Options

Certain options are available for use with DUP. These options are divided into two categories: action, and mode. Action options cause specific operations to occur. You can use these options alone or with valid mode options.

Usually, you can specify only one action option at a time. Mode options modify action options. Table 6–1 illustrates which mode options you can use with a particular action option.

Table 6-1: DUP Option Combinations

| Action | Mode |
| --- | --- |
| C | W, Y, G |
| D | W, Y |
| I | Y, G, E, F, H, R |
| K | W, F, G, E, F, H, R |
| O | Q, W, Y |
| S | W, X, Y |
| T | W, Y |
| U | W, Y |
| V | W, Y |
| Z | W, B, N, R, V, Y, D |

Note that /V can be either an action or a mode option, depending on how you use it.

You can use DUP action options to perform operations such as creating files, copying devices, scanning for bad blocks, performing a bootstrap operation, and initializing volumes. You can use the DUP mode options to modify the action options, where necessary.

The following sections describe the various DUP options and give examples of typical uses. Table 6–2 summarizes the options you can use with DUP.

## 6.3.1 Create Option (/C[/G:n])

The /C option creates a file with a specific name, location, and size on the random-access device that you specify. This option is useful in recovering files that have been deleted, and for creating files to assign as logical disks (see Chapter 9). The /C option creates only a directory entry for the file. It does not store any data in the file. You must specify both the file name and file type of the file to be created.

The syntax of the command is:

filespec[n] = /C[/G:n]

where:

filespec[n]

represents the device, file name, and file type of the file to be created; [n] is a decimal number representing the size in blocks of the file to be created. Note that the brackets here are part of the command; that is, they do not indicate n is optional. If you do not specify this number, DUP creates a one-block file.

Table 6-2: DUP Options

| Option | Section | Function |
| --- | --- | --- |
| /B[:RET] | 6.3.13.4 | Use with /Z to write files with the file type .BAD over any bad blocks DUP finds on the disk to be initialized.Use :RET to retain through initialization all .BAD entries created by a previous /B. |
| /C | 6.3.1 | Creates a file on the volume you specify. DUP creates the file in the first available location, unless you specify a starting block number by using the /G option. |
| /D | 6.3.13.5 | Use with /Z to uninitialized (restore) a device. Use only if no files have been transferred to the device since it was initialized. |
| /E:n | 6.3.2 | Specifies the ending block number for a read operation (used with the /I and /K options). |
| /F | 6.3.4 | Use with the /K option to transfer the file name containing the bad block together with the relative block number of the bad block in the file. Or use with /I either to copy a file to an output device or copy a device to an output file. |
| /G:n | 6.3.1 | Specifies the starting block number for a read operation (on an input device) and the starting block number for a write operation (on an output device); n is an integer that represents a block number. Use this option with the /C, /I, and /K options. |
| /H | 6.3.2 | Use with the /I option to verify that the output is equal to the input. |
| /I | 6.3.2 | Copies the image of a disk to another disk or magtape or from magtape to disk. Use with /G and /E if you want to specify block numbers. |
| /K | 6.3.3 | Scans a device for bad blocks and outputs the octal address of the bad blocks to the output device. Use with /G and /E if you want to specify block numbers as boundaries for the scan. |
| /N:n | 6.3.13.1 | Use with /Z to set the number of directory segments you require if you do not want the default size; n is an integer in the range 1-37 (octal). |
| /O | 6.3.5 | Boots the device or file you specify. |
| /Q | 6.3.6 | Use with /O to boot a volume that is not RT-11, or is a pre-Version 4 volume of RT-11. |
| /R[:RET] | 6.3.13.3 | Use with /Z to scan a device that supports bad block replacement for bad blocks, or with /I to preserve the output volume's bad block replacement table. When used with /Z, /R creates a replacement table on the disk for any bad blocks DUP finds. If you use /R:RET with /Z, DUP retains the replacement table that is already on the disk and does not prescan the disk for bad blocks. |
| /S | 6.3.7 | Compresses a disk onto itself or onto another disk; the output device, if any, must be initialized. |
| /T:n | 6.3.8 | Extends an existing file by the number of blocks that n indicates. |
| /U[:xx] | 6.3.9 | Writes the bootstrap portion of the monitor file in blocks 0 and 2–5 of the target device. The optional argument, xx, represents the target system device name. |
| /V[:ONL] | 6.3.10 | Prints the user ID and owner name. Use it with /Z (as a mode option) to place a new user ID and owner name in block 1 of the initialized disk, or in the VOL1 header block on magtape. Using /V:ONL with /Z changes only the ID and owner name, and does not initialize the device (not applicable for magtape). |
| /W | 6.3.11 | Use with any action option except /I (but only one) to initiate an operation and then pause to allow you to change volumes. This is useful on small, single-disk systems because it lets you replace the system device with another disk before performing an operation. |
| /X | 6.3.7 | Use with /S to inhibit automatic booting of the system device when it is compressed. |
| /Y | 6.3.12 | Use with /C, /I, /O, /S, /T, U, V, or /Z to ensure immediate execution of the operation by inhibiting the confirmation messages. |
| /Z[:n] | 6.3.13 | Initializes the directory of the device you specify. The size of the directory defaults to the standard RT-11 size; use n to allocate extra directory words for each entry beyond the default. |

/G:n represents the octal numeric value of the starting block of the file to be created. If you do not use /G:n, DUP creates the file in the first unused area large enough to contain the file. Use a decimal point with n (n.) to specify a decimal starting block number.

You can use the /C option to cover bad blocks on a disk by creating a file with a file type .BAD to cover the bad area.

Use /C to recover accidentally deleted files. In this case, use DIR to obtain a listing of the device. Use the /E and /Q options in DIR to list files, tentative files, empty areas, and the sizes of all areas. You can then assign a file name to the area that contains the data you lost.

You can also use DUP to set aside a file on a disk without performing any input or output operations on the file.

When you use the /C option, make sure that the area in which the file is to be created is empty (using the DIR /E and /Q options). If there are more blocks in the empty area than the file you are creating needs, DUP attempts to put the extra blocks in empty areas that are contiguous to the file you are creating. If there is not enough room in contiguous empty areas, the error message ?DUP-F-No room for file DEV:FILNAM.TYP prints, and DUP does not create the file.

The /C option checks for duplicate file names. If the file name you specify already exists on the device, DUP issues an error message and does not create a second file with the same name.

If you attempt to create a file over a tentative file (one that was opened but never closed) and the foreground is loaded, the system prompts you to confirm the operation. If you type Y to continue, DUP writes over the tentative file. Be sure that you do not write over a tentative file being used by the foreground job; this will corrupt the file and cause unpredictable results.

The following example uses /C to create a file named FILE.MAC consisting of blocks 140, 141, and 142 on device DK1:.

\* DK1:FILE.MAC[3]=/C/G:140

## 6.3.2 Image Copy Option (/I)

The /I option copies block for block from one volume to another. This operation is applicable for magtape only when copying to or from a random-access volume, such as disk or diskette. The /I option is often used to copy one disk to another without changing the file structure or location of files on the device. For this purpose, it is an added convenience that you do not have to copy a boot block to the device. You can also copy disks that are not in RT-11 format, if they have no bad blocks. If DUP encounters a bad block on either the input or output volume, it retries the operation and performs the copy one block at a time. If no error message prints, you can assume that the transfer completed correctly.

Qualifiers to the /I option let you:

1. Specify the blocks to be read from the input device and a starting block number for the write operation on the output device.

2. Copy a file to a device, or a device to a file, by specifying a file name with either the input or output device. For example, you can copy a diskette to a file on an RL02, or a file on an RL02 to a diskette.

3. Preserve the output volume's bad block replacement table when you are copying between like volumes that support bad block replacement.

4. Verify that the output matches the input after a copy operation.

## NOTE

When you use /I in an operation involving magtape, you must specify a file name and follow it with the /F option.

The syntax of the command is:

output-device: filename [/F][/G:rn] = input-device[filename]/I[/G:rn/E:rn][/F][/H][/R]
\*

## where:

filename represents the file name to which you are copying the input device, or (when specified with the input device) represents the input file name you are copying to the output device. You must specify a file name when you use the /F option. If you specify an input file and you do not use /F, use the dummy file name \* with the output specification. Note that you can use a file name with either the input or output, but never with both.

\* represents a dummy file name (required when you do not use the /F option, and when the output device is not a mag-tape). Note that either filename or \*, but not both, can be specified with the output device.

/G:rn when specified with the output device, represents the starting block number for the write operation. When specified with the input device, it represents the starting block number of the read operation.

/E:rn represents the ending block number on the input device for the read operation.

/F indicates that you want to copy a file to an output volume, or that you are copying an entire input volume to an output file. You must also use the /F option when you specify mag-tape as the input or output device (because you must always specify a file on the magtape).

/H verifies that the input matches the output.

/R preserves the output volume's bad block replacement table. DUP copies all blocks from the input volume to the output volume except those blocks that contain the input volume's bad block replacement table.

The command string must include an input and an output specification; there is no default device.

If one device is smaller than the other, DUP copies only the number of blocks of the smaller device. DUP may therefore copy the entire directory of the input volume, but not all of its files. If you copy a larger device to a smaller one, DUP asks you to confirm the copy operation before DUP performs the operation. If you use the /G:n and /E:n options, DUP asks you to confirm the copy only if the number of blocks to be copied is larger than the area on the output volume defined by the /G:n option and the end of the output volume.

DUP prints the confirmation message after the normal copy confirmation.

Do not use the /I option with the /W option.

If the /F option is used the relative sizes of the input and output volumes are ignored and you are not asked to confirm the copy. The confirmation messages can also be suppressed by using the /Y option.

You can use the /H option with /I to verify that the input matches the output after an image mode copy operation.

## NOTE

The /I option does not copy track 0 of diskettes. However, this restriction has no impact on any copy operations involving RT-11 formatted diskettes.

The following examples use the /I option. The file name \* is not significant; it is a dummy file name required by the Command String Interpreter.

\* DL1: \*=DLO:/I
DL1:/Copy; Are you sure?

The command shown above copies all blocks from DL0: to DL1:.

\* DL1:\*/G:501=DLO:/I/G:O/E:500
DL1:/Copy; Are you sure? Y

The command shown above copies blocks 0–500 from DL0: to blocks 501–1000 on DL1:

\* DL1:FLOPPY,BAK/F=DYO:/I
DL1:/Copy;Are you sure? Y

The last command copies device DY0: to a file named FLOPPY.BAK on DL1:.

## 6.3.3 Bad Block Scan Option (/K)

Some mass storage volumes (disks, diskettes, and DECtape II) have bad blocks, or they develop bad blocks as a result of age and use. You can use the /K option to scan a device and locate bad blocks on it. DUP prints the absolute block number of those blocks that return hardware errors when DUP tries to read them. If you specify an output file, DUP prints the bad block report in that file. Remember that block numbers are octal and the first block on a device is block 0. If DUP finds no bad blocks, it prints an informational message. A complete scan of a volume takes from one to several minutes depending on the size of the volume. It does not destroy data that is stored on the device.

You can scan selected portions of a device by specifying beginning and ending block numbers. The syntax of this command is:

[filespec = ]input-device:/K[/G:m][/E:n]

where:

filespec represents the output file specification for the bad block report. If no bad blocks are found, no file is created.

/G:m represents the block number of the first block to be scanned.

/E:n represents the block number of the last block to be scanned.

If you specify only a starting block number, DUP scans from the block you specify to the end of the device.

If the device to be scanned has files on it, you can use /F with the /K option to print the name of the file containing the bad block and the relative block number within the file that is bad.

The following command scans the entire diskette in DY1:.

\* DY1:/K

The next command scans blocks 100 to 200(decimal) of the diskette in DY1: and sends the bad block report to DY0:BLOCKS.BAD.

\* DYO: BLOCKS, BAD=DY1:/K/G:100:/E:100.

Sometimes a block that is reported as bad can recover. To verify whether the reported bad blocks are the result of soft or hard errors (that is, whether a bad block can recover), perform a second bad block scan and compare the two reports. Blocks reported as bad on both reports are caused by hard errors and cannot recover. Blocks that are reported as bad on the first report but not on the second report indicate that a soft error has occurred, and the blocks have recovered.

## 6.3.4 File Option (/F)

The file option serves two different purposes as a mode option, depending on whether you use it with /K or with /I.

When you use /F with /K, DUP does a bad block scan and displays a file name for each bad block it finds. DUP then prints a list of these bad block files along with their locations within the file. This list includes the relative block number of each bad block within the file and a report on whether each bad block is hard or soft. An example of such a list, along with the command line that generated it, follows.

```txt
* DYO:/K/F
Block Type File Block
000717 463. Hard NUMBER.PAS 000546 358.
000725 469. Hard ANTONY.MAC 000554 364.
000732 474. Hard CAESAR.MAC 000561 369.
000743 483. Hard < UNUSED > 000572 378.
000751 489. Hard <UNUSED > 000600 384.
000754 492. Hard <UNUSED > 000603 387.
?DUP-W-Bad blocks detected G.
```

DUP outputs the following list if you use /F with /K on a disk that supports bad block replacement. In the column marked Type, DUP lists whether the bad block is replaced in the manufacturer's bad block replacement table or if it is hard or soft.

```c
* DM1:/K/F
Block Type File Block
003055 1581. Replaced MSX .SYS 000007 7.
003465 1845. Replaced DRV .OBJ 000077 63.
037061 15921. Replaced < UNUSED > 010550 4456.
056106 23622. Replaced <UNUSED > 027575 12157.
056210 23688. Replaced <UNUSED > 027677 12223.
077521 32593. Replaced <UNUSED > 051210 21128.
143116 50766. Replaced <UNUSED > 043374 18172.
145337 51935. Replaced <UNUSED > 045615 19341.
?DUP-W-Bad blocks detected 8,
```

When you use /F with /I, you use it either to copy a file from an input device to an output device, or to copy an input device to an output file. Note that /I does not copy track 0 of diskettes. If you use a magtape for either the input or output device, you must specify a file name for the magtape followed by the /F option. Do not include wildcards in either the input or output file specification when you use the /F option.

## 6.3.5 Boot Option (/O)

The /O option can perform two operations: a hardware bootstrap of a specific device containing an RT-11 system, and a bootstrap of a particular RT-11 monitor file that does not affect the bootstrap blocks on the device.

The command syntax for a device bootstrap is as follows:

dev:/O

This operation has the same results as a hardware bootstrap. Valid devices for the boot operation follow:

```yaml
DD0:-DD1:          DW:
DK:                    DX0:-DX1:
DL0:-DL3:         DY0:-DY1:
DM0:-DM7:        DZ0:-DZ1:
DS0:-DS7:         RK0:-RK7:
DU0:-DU7:        SY:
```

## NOTE

The following unsupported devices are also valid for the /O option:

Use the following syntax to boot a monitor without changing the bootstrap on the device:

```txt
dev:monitor-name/O
```

This makes it easy for you to switch from one monitor to another. Whether bootstrapping a specific monitor or a specific device, DUP checks to see if the bootstrap blocks are correctly formatted. If the boot operation you request is invalid, DUP prints an error message and waits for another command.

When you reboot with the /O option, you do not have to reenter the date and time of day with the monitor DATE and TIME commands. However, the clock does lose a few seconds during the reboot.

The following command reboots the RT-11 system under the SJ monitor:

\* DLO:RT11SJ.SYS/0
RT-11SJ      V05.00

To boot a different monitor, for example the FB monitor\` (for DY0:), type:

\* DYO:RT11FB.SYS/0

## 6.3.6 Boot Foreign Volume Option (/Q)

Use the /Q option with /O to boot a volume that has a monitor other than the RT-11 Version 4 or 5 monitor. Note that you must use /Q to boot any version of RT-11 previous to Version 4.

The following example boots an RT-11 Version 3B volume.

```txt
* DYO:/O/Q
.RT-11SJ V03B-00B
```

DUP does not retain the date and time when you use the /Q option.

## 6.3.7 Squeeze Option (/S)

Use the /S option to compress a volume (disk, diskette) onto itself or onto another disk. To do this, DUP moves all the files to the beginning of the volume, producing a single, unused area after the group of files. The squeeze operation does not change the bootstrap blocks of a volume. Since it is critical to perform an error-free squeeze operation, be sure to scan a volume (with /K) before you use /S.

The output volume you specify, if any, must be an initialized volume. If you specify an output volume, DUP does not request confirmation before it performs the operation. If you do not specify an output volume, DUP prints the Are you sure? message and waits for your response before proceeding. You must type Y followed by a carriage return for the command to be executed.

The /S option does not operate on files with .BAD file types, preventing you from reusing bad blocks that occur on a disk. You can rename files containing bad blocks, giving them a .BAD file type, and therefore cause DUP to leave them in place when you execute a /S. During a squeeze operation, files with a .BAD file type are renamed FILE.BAD. DUP inserts files before and after .BAD files until the space between the last file it moved and the .BAD file is smaller than the next file to be moved.

If an error occurs during a squeeze operation, DUP continues the operation, performing it one block at a time. If no error message prints, you can assume that the operation completed correctly.

The syntax of the command is:

$$
[ \text {output - device} = ] \text {input - device / S}
$$

Do not use /S on the system device (SY:) when a foreground or system job is loaded. A ?DUP-F-Can't squeeze SY: while foreground loaded error message results if you attempt this, and DUP ignores the /S operation. You must unload the foreground job before using the /S option. Also, you should not attempt to squeeze any volume that a running foreground job is using. Data may be written over a file that the foreground job has open, thereby corrupting the file and possibly causing a system crash.

## NOTE

If you perform a compress operation on the system volume, the system automatically reboots when the compress operation is completed. This occurs to prevent system crashes that can occur when a system file is moved.

You can use /X with /S to suppress the automatic reboot and leave DUP running. However, you should use /X only if you are certain that the monitor file will not move. Even then, you should reboot the system when the squeeze operation completes if the device handlers have moved.

The following examples use the /S option:

\* SY:/S
SY:/Squeeze; Are you sure? Y
RT-11SJ      V05.00

The command shown above compresses the files on the system volume and reboots the system when the compress operation completes.

## NOTE

If you compress your system volume, make sure the DUP program has the name DUP.SAV. If not, a system failure may occur.

```txt
* DYO: *=DY1:/S
```

This command transfers all the files from device DY1: to device DY0:, leaving DY1: unchanged. The file name \* is not significant; it is a dummy file name required by the Command String Interpreter.

## 6.3.8 Extend Option (/T:n)

Use the /T option to extend the size of a file. The syntax of the command is:

filespec = /T:n

where:

filespec represents the device, file name, and file type of the file to be extended

n represents the number of blocks to add to the file

You can extend a file in this manner only if it is followed by an unused area at least n blocks long. Any blocks not required by the extend operation remain in the unused area.

The following example uses the /T option:

\* DY1:ZYZ,TST=/T:100

This command assigns 100 more blocks to the file named ZYZ.TST on device DY1:.

## 6.3.9 Bootstrap Copy Option (/U[:xx])

In order to use a volume as a system volume, you must copy a bootstrap onto it. To do this, first make sure that the appropriate monitor file and handler are stored on the volume. For a double-density diskette system, for example, check to see that the file DY.SYS is in the diskette directory. If it is, then you can copy the desired monitor onto the diskette, using the /U option.

The option argument, xx, represents a target system device name. For example, you can use this argument when you are creating a bootable RX01 diskette if the current system is on an RX02 system.

## NOTE

When you use the /U option, make sure that the input volume is also the output volume.

To copy a bootstrap for the SJ monitor on DL1:, for example, use the following procedure:

1. Obtain a formatted disk. (Most disks, diskettes, and DECtape II volumes are formatted by the manufacturer. However, Chapter 8, FORMAT, does outline the procedure for reformatting RK05, RK06, RK07, RP02, and RP03 disks, and RX01 and RX02 diskettes.)

2. Initialize the disk with /Z (see Section 6.3.13).

3. Copy files onto the disk.

4. Copy the monitor and RL02 handler, DL.SYS, onto the disk.

5. Copy the monitor bootstrap onto the disk with /U.

The following example shows how to initialize a diskette, copy files to it, and write a bootstrap onto the diskette:

\* DY1:/Z/Y

The command shown above (step 2 of the procedure described above) initializes the diskette.

\* DY1: \*=DYO:/S

This command, which combines steps 3 and 4, squeezes all the files from DY0: onto DY1:.

\* DY1: \*=DYO:RT11FB, SYS/U

The last command (step 5) writes the bootstrap for the FB monitor onto the bootstrap blocks (blocks 0 and 2–5) of DY1:. The file name \* is not significant; it is a dummy file name required by the Command String Interpreter.

## 6.3.10 Volume ID Option (/V[:ONL])

You can use the /V option as an action option to print the volume ID of a device or to change the volume ID.

The syntax of the command is:

device:[/Z]/V[:ONL]

where:

device: is the device whose volume ID you want to display or change

If you specify only /V, DUP prints out on the console terminal the volume ID and owner name of the device you specify. If you specify /Z with /V, DUP initializes the device and prompts you for a new volume ID and owner name. If you specify /Z/V:ONL, DUP assumes you want only to change the volume ID and owner name and not initialize the device.

When you specify either /Z/V or /Z/V:ONL, DUP prompts you for a volume ID:

```txt
Volume ID?
```

Respond with a volume ID that is up to 12 characters long for an RT-11 directory-structured volume or up to six characters long for magtape. Terminate your response with a carriage return. DUP then prompts for an owner name:

```txt
Owner?
```

Respond with an owner name that is up to 12 characters long for an RT-11 directory-structured volume or up to 10 characters long for magtape. Terminate your response with a carriage return. DUP ignores characters you type beyond the valid length.

You cannot change the volume ID of a magtape without initializing the entire tape. The /V:ONL command changes only the volume ID and owner name; it does not initialize the device. Section 6.3.13.2 describes how to use /V with the /Z option to initialize a device and write new volume identification on it.

The following example uses the /V:ONL option:

```txt
*   DL1:/Z/V:ONL
DLO:/Volume ID change; Are you sure?      Y
Volume ID?       FORTRAN VOL
Owner?           Nancy
```

This command writes a new volume ID and owner name on device DL1:.

## 6.3.11 Wait for Volume Option (/W)

The /W option causes DUP to prompt you for the volumes to operate on, and waits for you to mount them. It is useful for single-disk systems or diskette systems. /W is a mode option that you can use with any of the action options, but you can specify only one action with it in a command line. Do not use the /W option with the /I option.

The /W option initiates execution of a command, but then pauses and prints the message Mount input volume in &lt;device&gt;; Continue?, where &lt;device&gt; represents the device into which you mount the input volume. At this time you can remove the system volume (if necessary) and mount the volume on which you actually want the operation to take place. When the new volume is loaded, type Y or any string beginning with Y followed by a carriage return to execute the operation. If you type N or any string beginning with N, or CTRL/C, the operation is not completed. Instead DUP prompts you to remount the system volume if you have removed it and returns control to the keyboard monitor. Any other response causes the message to repeat.

If you type Y, DUP prompts you for the input volume, if any. When the operation completes (except the /O operation, which boots the system), the Mount system volume in &lt;device&gt;; Continue? message prints. Replace the system device and type Y or any string beginning with Y followed by a carriage return. If you type any other response, DUP prompts you to mount the system volume until you type Y. When you type Y, the asterisk (\*) prompt prints, and DUP waits for you to enter another command.

The following example uses the /W option:

```txt
* DY1:/K/F/W
Mount input volume in DY1; Continue? Y
?DUP-I-No bad blocks detected DY1:
Mount system volume in DY1; Continue? Y
*
```

This command directs DUP to scan the diskette for bad blocks. During the first pause, the system diskette is removed and another diskette is mounted. A Y is typed and the scan operation executes. During the second pause, the system disk (on which DUP is stored) is replaced and another Y is typed. DUP prompts for another command. When you use /W, make sure that DUP is on the system volume.

## 6.3.12 No Query Option (/Y)

Use the /Y option to suppress the query messages that some commands print.

Certain options normally print the Foreground job loaded, Continue? message if a foreground job is loaded when you issue one of them (/C, /I, /O, /Q, /S, /T, and /Z). You must respond to the query message by typing Y or any string beginning with Y followed by a carriage return for the operation to proceed. Some other options (/C, /I, /O, /S, /V, and /Z) print the Are you sure? message and wait for your response. If a foreground job is loaded and you specify one of these options, DUP combines the two query messages into one message and waits for your response. You can suppress all these messages and the pause associated with them by specifying /Y in the command string.

Note, if you use /Y with /Z to initialize your system volume, the system ignores /Y.

## 6.3.13 Directory Initialization Option (/Z[:n])

You must initialize a device before you can store files on it. Use the /Z option to clear and initialize the directory of an RT-11 directory-structured device. The /Z option must always be the first operation you perform on a new device after you receive it, formatted, from a manufacturer. After you use /Z, there are no files in the directory.

The syntax of the command is as follows:

device:/Z[:n]

where:

device represents the device you want to initialize.

:n is an octal integer (greater than or equal to 1) that represents the size increase, in words, of each directory entry. DUP adds this number to the default number of words allocated for each entry (valid only for directory-structured devices).

The size of the directory determines the number of files that can be stored on a device. The system allows a maximum of 72 files per directory segment, and 31 directory segments per device. Each segment uses two blocks of disk space. If you do not specify n, each entry is seven words long (for file name, creation date, and file position information). When you allocate extra words, the number of entries per directory segment decreases. The formula for determining the number of entries per directory segment is:

(512-7)/((number of extra words) + 7)

For example, if you use /Z:1, you can make 63 entries per segment. RT-11 does not normally support nonstandard directory formats, and DIGITAL does not recommend altering the directory format.

6.3.13.1 Changing Directory Segments (/N:n) — If you do not want the default directory size of the device, use /N with /Z to set the desired number of directory segments for entries in the directory. The syntax is as follows:

/Z/N:n

In this option, n is an integer in the range 1–31 that represents the number of directory segments you want the directory to have.

Table 6–3 lists the default directory sizes, in segments, for RT-11-supported directory-structured devices.

If the default directory size for diskettes is too small for your needs, see the RT-11 Installation Guide for details on increasing the default number of directory segments.

Table 6-3: Default Directory Sizes

| Device | Number (decimal) of Segments in Directory |
| --- | --- |
| DD | 1 |
| DL (RL01) | 16 |
| DL (RL02) | 31 |
| DM | 31 |
| DU (disk) | 31 |
| DU (diskette) | 1 |
| DW (RD50) | 16 |
| DW (RD51) | 31 |
| DX | 1 |
| DY (single-density) | 1 |
| DY (double-density) | 4 |
| DZ (RX50) | 4 |
| RK | 16 |

The following example initializes the directory on device DL1: and allocates six directory segments.

```txt
* DL1:/Z/N:G
DL1:/Initialize; Are you sure? Y
```

6.3.13.2 Changing Volume ID (/V) — When you initialize a disk or magtape, DUP normally maintains the volume ID and owner name. If at initialization time you want to change the volume ID and owner name, use the /V option with /Z. For example, the following command initializes device DL1: and prompts you for a volume ID and owner name. Section 6.3.10 illustrates these prompts and shows how to use them.

```txt
* DL1:/Z/V
DL1:/Initialize; Are you sure? Y
Volume ID? VOUCHERS
Owner? PAYABLES
```

6.3.13.3 Replacing Bad Blocks (/R[:RET]) — If you have RK06, RK07, RL01, or RL02 disks, you can use the /R option with either /I or /Z.

Use this option with /I to preserve the output volume's bad block replacement table. DUP copies all blocks from the input volume to the output volume except those blocks that contain the input volume's bad block replacement table.

Use this option with /Z to scan a disk for bad blocks. If DUP finds any bad blocks, it creates a replacement table so that routine operations access good blocks instead of bad ones. Thus, the disk appears to have only good blocks. Note, though, that accessing this replacement table slows response time for routine input and output operations. If you use :RET with /R, DUP initializes the volume and retains the bad block replacement table (and

FILE.BAD files) created by the previous /R command. Note that the :RET argument is invalid when you use /R with /I.

Note that the monitor file cannot reside on a block that contains a bad sector error (BSE) if you are doing bad block replacement. If this condition occurs, a boot error results when you attempt to bootstrap the system. If this occurs, move the monitor.

With an RK06, RK07, RL01, or RL02 you have the option of deciding which bad blocks you want replaced if the number of bad blocks exceeds what can fit in the replacement table (replacement table overflow). The RK06s and RK07s support up to 32(decimal) bad blocks in the replacement table; the RL01s and RL02s support up to 10.

With an RK06 or RK07 disk, DUP can replace only those bad blocks that generate a BSE. Of the blocks DUP cannot replace, DUP can report a bad block as being hard or soft. If you perform two bad block scans and a block is reported as bad in both reports, this indicates a hard error. If in the second report the block is not reported as bad, the block has recovered from a soft error.

With an RL01 or RL02, DUP can replace any kind of bad block. The following paragraphs describe how to designate which blocks to replace on an RK06, RK07, RL01, or RL02 disk.

When you use /R, DUP prints out a list of replaceable bad blocks as in the following sample:

```txt
Block . Type
030722 12754, Replaceable
115046 39462, Replaceable
133617 46991, Replaceable
136175 48253, Replaceable
136277 48319, Replaceable
136401 48385, Replaceable
140405 49413, Replaceable
146252 52394, Replaceable
?DUP-W-Bad blocks detected B.
```

If there is a replacement table overflow, DUP prompts you to indicate which blocks you want replaced as follows:

```txt
?DUP-W-Replacement table overflow DEV:
Type <RET>, O, or nnnnnn (<RET>)
Replace block #
```

The value nnnnnn represents the octal block number of the block you want the system to replace.

After you enter a block number, DUP responds by repeating the Replace block # prompt. Type a 0 at any time if you do not want any more blocks replaced, and this will end prompting. DUP marks any blocks not placed in the replacement table as FILE.BAD.

If you enter a carriage return at any time, DUP places all bad blocks you have not entered into the replacement table, starting with the first on the disk, until the table is full. DUP assigns the name FILE.BAD to any remaining bad blocks and prompting ends.

If you use /Y with /R, the effect will be as if you entered a carriage return in response to the first Replace block # prompt.

6.3.13.4 Covering Bad Blocks (/B[:RET]) — To scan the volume for bad blocks and write files over them, use the /B option with /Z. For every bad block DUP encounters on the device, it creates a file called FILE.BAD to cover it. After the disk is initialized and the scan completed, the directory consists only of FILE.BAD entries that cover the bad blocks. If DUP finds a bad block in the boot block or the directory, it prints an error message and the disk is not usable.

If you specify :RET with /B, DUP will retain through initialization all FILE.BAD files created by a previous /B. If you use the /B option to initialize a volume that has been previously initialized using the /R option, DUP creates FILE.BAD files to cover the bad blocks on the volume, and the system then ignores the bad block replacement table.

If the volume being initialized contains bad blocks, the system prints the locations of the bad blocks in octal and in decimal, as in the following example:

```txt
* DYO:/Z/B
DYO:/Initialize: Are you sure? Y
    Block        Type
000120      80.  Hard
000471      313.  Hard
000521      337.  Hard
?DUP-W-Bad blocks detected 3.
```

The left column lists the locations in octal, and the middle column lists the locations in decimal. The right column indicates the type of bad block found: hard or soft.

6.3.13.5 Restoring a Disk (/D) — Use /D to uninitialized (restore) a volume if you have not transferred any files to it since initialization. DUP will restore all files and directory entries that were present before the volume was initialized. This option is useful if you initialize a volume by mistake. However, you cannot restore volumes that support bad block replacement if bad blocks were found during initialization.

The following command restores volume DY1:.

```txt
* DY1:/Z/D
```

Note that /D does not restore boot blocks. Thus, if you use /D to restore a previously bootable volume, use the bootstrap copy option, /U[:xx], to make the volume bootable again.
