# RT-11 System Utilities Manual: Ch.3 BUP backup utility (back up big volumes to multiple smaller ones, restore)

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 3.1 Calling and Terminating BUP
- 3.2 BUP Command String Syntax
- 3.3 Options
- 3.3.1 File Backup Operation
- 3.3.2 Volume Backup Operation (/I)
- 3.3.3 Directory Option (/L)
- 3.3.4 Restore Option (/X)
- 3.3.5 Initialize Option (/Z)

---

# Chapter 3 Backup Utility Program (BUP)

The backup utility program (BUP) is a specialized file transfer program for storing large files or volumes. BUP allows you to copy a file or volume to several volumes that are smaller than the input file or volume. BUP also performs the reverse operation of restoring the fragmented file or volume to its original form on a single large volume.

Since you cannot use the file or volume while it is fragmented on several smaller volumes, BUP is most useful as a means of backing up information that you want to store.

## 3.1 Calling and Terminating BUP

To call BUP from the system device, respond to the keyboard monitor prompt (.) by typing:

, R BUP RET

The Command String Interpreter (CSI) prints an asterisk at the left margin of the terminal and waits for you to type a command string. If you enter only a carriage return at this point, BUP prints its current version number and prompts you again for a command string. You can type CTRL/C to terminate BUP and return to the monitor when BUP is waiting for input from the console terminal. You must type two CTRL/Cs to terminate BUP at any other time.

## 3.2 BUP Command String Syntax

Chapter 1, Command String Interpreter, describes the general syntax of the command line BUP accepts, but you can type only one input specification and only one output specification. You must specify the input file name and type. DK: is the default device for both input and output. Wildcards are ignored when initializing or obtaining the directory of a backup volume. Wildcards are not allowed in either the input or output file specification for backup and restore operations.

You can use random-access volumes as either input or output volumes for both backup and restore operations. Magtapes, however, can be used only as output volumes for a backup operation, and only as input volumes for a restore operation. If you use TSV05 magtapes as backup volumes, you must set the extended features switch (switch S0 on switch pack E58) if you want the tape to stream at 100 in/s. See Appendix A of either the TSV05 Installation Guide or the TSV05 User's Guide for more information on setting the Extended Features Switch.

Output volumes for backup operations, except magtape, must be initialized by BUP. See Section 3.3.5 for information on initializing backup volumes.

## 3.3 Options

BUP options, summarized in Table 3–1, permit you to perform various operations with BUP. If you specify none of these options, BUP assumes that you want to back up a file to smaller volumes.

Table 3-1: BUP Options

| Option | Section | Function |
| --- | --- | --- |
| /I | 3.3.2 | Backs up an entire volume to smaller volumes in image mode. Also used with /X during restore operations. |
| /L | 3.3.3 | Prints a directory listing of a backup volume. Cannot be used with any other option. |
| /X | 3.3.4 | Restores a file that has been backed up using BUP. Use with /I to restore a volume. |
| /Y | 3.3.5 | Used with /Z to suppress the BUP confirmation message printed during initialization. |
| /Z | 3.3.5 | Initializes a volume specifically for use as an output volume in a backup operation. Cannot be used with any other option except /Y. |

## 3.3.1 File Backup Operation

When you specify no options in the BUP command line, BUP assumes that you want to back up a file. BUP performs all copy operations in image mode.

You must first initialize the output volumes, unless the output volumes are magtape, by using the BUP /Z option, so BUP can recognize the volumes as backup volumes and to ensure that the volumes contain no bad blocks. (The /Z option is invalid with magtape; BUP initializes magtapes during the backup operation.) See Section 3.3.5 for details on initializing volumes for BUP operations.

Use the following syntax to perform a file backup operation.

output-spec = input-spec

## where:

output-spec represents the device in which you will mount the output volumes for the backup operation, and the file to which you are copying the input file. If you specify no output file name, BUP uses the input file name. The default output file type is .BUP. Wildcards are invalid in the output specification.

input-spec represents the device and file specification of the file you want to back up. Wildcards are invalid in the input specification.

BUP copies the input file to the first output volume until the output volume is full. If the entire input file fits on the first output volume, BUP prints an error message unless the output volume is magtape.

?BUP-F-Enough space on one volume -- use PIP

When the first of the output volumes is full, BUP prompts you to mount the next output volume. BUP also tells you which volume BUP is creating so you can properly label each volume.

Mount output volume in &lt;dev&gt;; Continue? Y
?BUP-I-Creatins volume n

BUP repeats this process until the entire input file has been copied.

The output file's creation date recorded in the directory is the system date during the backup operation. If no system date was set, no creation date is entered in the directory.

If BUP detects an output volume that has not been initialized as a backup volume (see Section 3.3.5), BUP prints a message and allows you to either initialize the volume as a backup volume or replace that volume with an already initialized backup volume.

?BUP-W-Not a backup volume DEV:
&lt;dev:&gt;/BUP Initialize; Are you sure? Y

If you are using magtape for the backup volumes, BUP always attempts to initialize the output volume, and asks you to confirm the initialization.

If BUP detects a volume that is not a valid RT-11 volume, or a volume that already contains files, BUP prints the appropriate message and allows you to either initialize the volume or replace that volume with another initialized backup volume.

Volume not RT-11 format. Are you sure?

```txt
Volume contains files. Are you sure?
```

Type Y or any string beginning with Y, followed by a carriage return, to initialize the volume already mounted. BUP automatically performs the copy operation once the initialization completes. If you choose not to initialize the volume, type anything other than Y. BUP prompts you to mount another volume.

```txt
Mount output volume in <dev>; Continue?
```

The following example shows a large file being backed up to RX02 diskettes. BUP finds that the second diskette has not been initialized as a backup volume, and queries for initialization.

```txt
* DYO:=DL1:LGFIL.DAT
Mount output volume in DYO; Continue? Y
?BUP-I-Creating volume 1
Mount output volume in DYO; Continue? Y
?BUP-W-Not a backup volume DYO:
DYO:/BUP Initialize; Are you sure? Y
Volume contains files. Are you sure? Y
?BUP-I-Bad block scan started...
?BUP-I-No bad blocks detected
?BUP-I-Creating volume 2
```

## 3.3.2 Volume Backup Operation (/I)

To back up an entire volume in image mode, use the /I option.

You must first initialize the output volumes, unless the output volumes are magtapes, by using the the BUP /Z option, so BUP can recognize the volumes as backup volumes and to ensure that the volumes contain no bad blocks. (The /Z option is invalid with magtapes; BUP initializes magtapes during the backup operation.) See Section 3.3.5 for details on initializing volumes for BUP operations.

Use the following syntax to perform an image mode backup operation.

output-spec = input-device/I

where:

output-spec represents the device in which you will mount the output volumes for the backup operation, and the file specification for the backup file. You must copy to a file even when you are backing up a volume. If you specify no output file name, BUP uses the 2-letter mnemonic of the input device (for example, DL for an RL02). The default output file type is .BUP. Wildcards are invalid in the output specification.

```txt
Volume not RT-11 format. Are you sure?
or
Volume contains files. Are you sure?
```

input-device represents the device and unit number in which you will mount the volume to be backed up.

BUP copies the input volume to the first of the output volumes until the output volume is full. If the entire input volume fits on the first of the output volumes, BUP prints an error message unless the output volume is magtape:

```txt
?BUP-F-Enough space on one volume -- use PIP
```

When the first of the output volumes is full, BUP prompts you to mount the next output volume. BUP also tells you which volume BUP is creating so you can properly label each volume.

```txt
Mount output volume in <dev>; Continue?Y
?BUP-I-Creating volume n
```

BUP repeats this process until the entire input volume has been copied.

The output file's creation date recorded in the directory is the system date during the backup operation. If no system date was set, no creation date is entered in the directory.

If BUP detects an output volume that has not been initialized as a backup volume (see Section 3.3.5), BUP prints a message and allows you to either initialize the volume as a backup volume or replace that volume with an already initialized backup volume.

```txt
?BUP-W-Not a backup volume DEV:
<dev:>/BUP Initialize; Are you sure? Y
```

If you are using magtape for the backup volumes, BUP always attempts to initialize the output volume, and asks you to confirm the initialization.

If BUP detects a backup volume that is not a valid RT-11 volume, or a volume that already contains files, BUP prints the appropriate message and allows you to either initialize the volume or replace that volume with another initialized backup volume.

Type Y or any string beginning with Y to initialize the volume already mounted. BUP automatically performs the copy operation once the initialization completes. If you choose not to initialize the volume, type anything other than Y. BUP prompts you to mount another volume by printing the following message.

```txt
Mount output volume in <dev>; Continue?
```

The following command backs up an RL02 volume to several RX02 diskettes. The backup volumes will contain the file DL.BUP when the backup operation is complete.

```txt
* DY := DL1 : / I
```

## 3.3.3 Directory Option (/L)

Use the /L option to display on the terminal the directory of the backup volume you specify. The syntax of the command is:

device/L

where:

device represents the volume whose directory you want to display

The listing for random-access volumes begins with the system date and the volume number of the specified backup volume. The volume number indicates that volume's position within the set of volumes that compose a single file or volume. The volume number is followed by a four-column listing of information about each volume in the set. The first column lists the volume numbers. The second column lists the name of the file, part of which resides on that volume. The third column lists the number of blocks from the file each volume contains. The last column lists the date on which the file or volume was backed up. Underneath the four columns, BUP prints the number of free blocks on the specified volume. Since this directory information is determined when you first begin a backup operation, all the predetermined backup directory information prints when you use this option even if you do not complete the backup operation.

The following command lists the backup information for backup volume 3 of the four-volume set that composes the file CAFIL.TXT.

<table><tr><td colspan="4">* DYO:/L</td></tr><tr><td colspan="4">23-Jan-83</td></tr><tr><td colspan="4">VOLUME 3 OF 4</td></tr><tr><td>VOLUME</td><td>FILENAME</td><td>BLOCKS</td><td>DATE</td></tr><tr><td>V1</td><td>CAFIL .BUP</td><td>980</td><td>23-Jan-83</td></tr><tr><td>V2</td><td>CAFIL .BUP</td><td>980</td><td>23-Jan-83</td></tr><tr><td>V3</td><td>CAFIL .BUP</td><td>980</td><td>23-Jan-83</td></tr><tr><td>V4</td><td>CAFIL .BUP</td><td>400</td><td>23-Jan-83</td></tr><tr><td colspan="4">1 file, 980 blocks</td></tr><tr><td colspan="4">0 free blocks</td></tr></table>

For magtapes, the listing appears in the same four-column format. However, only the current system date, and information for the magtape specified, is displayed. The third column lists the total number of blocks used in the set of magtapes that compose the file or volume.

The next example shows the backup information for a magtape.

\* MT1:/L
23-Jan-83

VOLUME FILENAME BLOCKS DATE
V1 DL1, .BUP 27450 23-Jan-83

## 3.3.4 Restore Option (/X)

The /X option restores a file or volume from several backup volumes to a single file or volume on a regular RT-11 structured volume. Type a command with the following syntax to restore a file.

output-spec = input-spec/X

where:

output-spec represents the device, and file name and type to which you want to restore the backup volumes. If you specify no output file, BUP uses the input file name and type. Wildcards are invalid in the output specification.

input-spec represents the device and file to restore. Wildcards are invalid in the input specification.

Use the following command syntax to restore a volume.

output-dev = input-spec/I/X

output-dev represents the volume to which you want to copy the backup volumes. Wildcards are invalid in the output specification.

input-spec represents the input volume (and optionally the file name under which it is stored) to restore. Wildcards are invalid in the input specification.

BUP prompts you to mount volume 1 of the set of volumes that contain the file or volume and tells you when the restore operation begins:

Mount input volume n in &lt;dev&gt;; Continue? Y
?BUP-I-Restore operation started from volume n

When BUP has copied all of the first input volume to the output volume, BUP prompts you to mount the next volume. BUP continues this process until the entire set of backup volumes composing the original file or volume have been copied to a single volume. If you mount a volume with the wrong volume number, BUP prints an error message and prompts you to mount the correct volume.

```txt
?BUP-E-Wrons volume number
Mount input volume n in <dev>; Continue?
```

If you mount a volume with the correct volume number but it contains the wrong file, BUP notifies you and prompts you to mount the correct volume.

```txt
?BUP-W-File nqt found DEV:FILNAM,TYP
Mount input volume number n in <dev>; Continue?
```

In either case, type any string beginning with Y after you have replaced the incorrect volume with the correct volume. Type any string beginning with N to abort the entire operation. Any other response causes BUP to continue to prompt you to mount the proper volume.

The following example shows a backup file being restored from two RX02 diskettes to a single file on an RL02 disk.

```txt
* DL1:=DY1:LGFIL.DAT/X
Mount input volume 1 in DY1; Continue?
?BUP-I-Restore operation started from volume 1
Mount input volume 2 in DY1; Continue?
?BUP-I-Restore operation started from volume 2
?BUP-I-Copy operation is complete
```

The next command restores a volume from RX02 diskettes to an RL02 disk.

```txt
* DL1: = DYO:/X/I
```

## 3.3.5 Initialize Option (/Z)

You must use the /Z option to initialize any volume, except magtape, before you can use that volume for output during a backup operation. (The /Z option is invalid with magtape. BUP initializes magtapes during the backup operation.) The /Z option clears the directory of the volume and writes information into the home block (block 0) so BUP can recognize the volume as a backup volume. In addition, /Z scans the volume for bad blocks, since backup volumes must not contain bad blocks.

The syntax of the initialization command is as follows:

device:/Z

where:

device represents the device that contains the volume you want to initialize

BUP prompts you to confirm the initialization. Type Y or any string beginning with Y to continue with the initialization of the backup volume. If your response begins with anything other than Y or you type CTRL/C, the operation is aborted and the CSI asterisk appears.

You can use the /Y option with /Z to suppress the confirmation message that prints during initialization.

The following command initializes a double-density diskette as a backup volume:

```txt
* DYO:/Z
DYO:/BUP Initialize; Are you sure? Y
?BUP-I-Bad block scan started...
?BUP-I-No bad blocks detected
```

If BUP detects bad blocks, BUP prints the following message to notify you that the volume could not be successfully initialized:

```txt
?BUP-I-Bad blocks detected; use another volume
```

You must mount and initialize another volume.

After BUP initializes a volume, no files exist in the directory. Therefore, if you attempt to have BUP initialize a volume that already contains files, BUP warns you that files exist and asks you to confirm the initialization.

```txt
Volume contains files. Are you sure?
```

Type anything that begins with Y to continue the initialization operation. Type anything else to abort the operation.

To return a BUP-initialized volume to an RT-11 structure volume for use other than with BUP, initialize the volume using DUP. Refer to Chapter 6 of this manual for more information on initializing volumes with DUP.

(1)
