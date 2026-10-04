# RT-11 System Utilities Manual: Ch.9 LD logical disk subsetting (MOUNT/DISMOUNT, logical disk files)

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 9.1 Calling and Terminating LD
- 9.2 LD Command String Syntax
- 9.3 Options
- 9.3.1 Assign Logical Device Name Option (/A:ddd)
- 9.3.2 Validate Logical Disk Assignments Option (/C)
- 9.3.3 Define Logical Disk Option (/L:n)
- 9.3.4 Write-Lock Logical Disk Option (/R:n)
- 9.3.5 Write-Enable Logical Disk Option (/W:n)

---

# Chapter 9

# Logical Disk Subsetting Program (LD)

The logical disk subsetting utility (LD) allows you to define and access logical disks, which is a way of subsetting physical disks. You define a logical disk by associating a logical disk unit number with a file. Once defined, you can use keyboard commands and utility programs to initialize, copy, and utilize these logical disks as if they were physical disks. For example, the COPY/DEVICE command can be used to copy logical disks as well as physical disks.

Disk subsetting is particularly useful when you work with large disks such as RC25, RL01/02, and RK06/07. Large disks such as these often run out of directory entry space before the volume is full. Since each logical disk has its own directory, dividing a physical disk into several logical disks creates more directory entry space. Logical disk subsetting provides a convenient way to group files into logical collections. Logical disk subsetting also allows you to perform some device and file operations more quickly.

## 9.1 Calling and Terminating LD

To call LD from the system device, first be sure that LD is installed (see the INSTALL command in Chapter 4 of the RT-11 System User's Guide). Then respond to the keyboard monitor prompt (.) by typing:

• R LD, SYS RET

When running under the XM monitor, type:

• R LDX.SYS RET

The Command String Interpreter (CSI) prints an asterisk at the left margin of the terminal and waits for you to type a command string. If you enter only a carriage return, LD prints its current version number and prompts you again for a command string. You can type CTRL/C to terminate LD and return control to the monitor when LD is waiting for input from the console terminal. You must type two CTRL/Cs to terminate LD at any other time.

## 9.2 LD Command String Syntax

Specify the LD command string in the following general format:

input-specs/options

where:

input-specs represents the files to be assigned as logical disk units. You can specify up to six input file specifications in a command line. The default file type is .DSK.

options represents an option from Table 9-1. You must specify at least one option in a command line, and you can specify more than one as long as the operations you specify do not conflict.

## 9.3 Options

The logical disk subsetting options allow you to mount and dismount logical disk unit numbers and associate them with files; write-lock or write-enable logical disks; and verify and correct logical disk assignments. Table 9-1 summarizes these options. The sections following Table 9-1 describe the LD options and give examples.

Table 9-1: LD Options

| Option | Section | Function |
| --- | --- | --- |
| /A:ddd | 9.3.1 | Assigns a logical device name to a logical disk. Must be used with /L. |
| /C | 9.3.2 | Verifies all logical disk assignments against the files on the volumes currently mounted. |
| /L:n | 9.3.3 | Mounts a logical disk and associates it with a file on a disk, or dismounts a logical disk and disassociates it from a file on a disk. |
| /R:n | 9.3.4 | Write-locks a logical disk. When you use /R:n the logical disk you specify has read-only access. |
| /W:n | 9.3.5 | Write-enables a logical disk. When you use /W:n, read/write access is allowed for the logical disk you specify. |

## 9.3.1 Assign Logical Device Name Option (/A:ddd)

Use the /A:ddd option with /L to assign a logical device name to a logical disk. The variable ddd represents the logical device name, from one to three characters long, that you want to assign. The first character must be a letter. You can optionally include a colon after the logical device name. After you have assigned a logical device name to a logical disk, you can refer to the logical disk by using the form LDn: or by using the logical device name.

The following command assigns the logical device name VOL to logical disk unit 2 (LD2:) when it is assigned to the file DK:LOGFIL.DSK.

\* LOGFIL.DSK/L:2/A:VOL

## 9.3.2 Validate Logical Disk Assignments Option (/C)

The /C option validates all logical disk assignments. When you use /C, LD checks the current logical disk assignments against the files on volumes that are mounted.

The /C option is most useful after you have moved or removed files on a volume, or after you have removed a volume from a device. If a logical disk file has moved, LD takes note of the new location so that you can continue to use that logical disk. If you have deleted a logical disk file or the volume containing a logical disk file is no longer mounted, LD disconnects the logical disk assignment. In the case of a volume that you have removed, the disconnection is temporary. You can reestablish the assignment when you remount the volume by using the /C option.

Note that after a squeeze (DUP /S option) or bootstrap operation, the system automatically performs a /C operation to update logical disk assignments.

The /C option must be used alone on a command line. The following command verifies current logical disk assignments.

\* / C

## 9.3.3 Define Logical Disk Option (/L:n)

The /L:n option mounts a logical disk by associating it with a file on a device, or frees a logical disk number so it can be associated with another file.

Use the following command syntax to mount a logical disk unit number.

filespec/L:n

where:

filespec represents the file to be associated with a logical disk unit number. The file can reside on either a physical disk or another logical disk.

n represents the logical disk unit-number to associate with the file. After it is mounted, the logical disk is referenced by using the device name LDn:. The variable n must be an integer in the range 0–7.

## NOTE

You must be careful to avoid accidentally destroying files while performing logical disk subsetting. LD allows you to assign logical disk unit numbers to both protected and .SYS files, and to write to those files.

To free a logical disk unit number from a file association, type a command with the following syntax.

/L:n

You can mount and dismount several logical disks on the same command line. For example, the following command associates logical disk unit 0 with file MYFILE.DSK on DL0:, logical disk unit 4 with DATFIL.DSK on DY0:, and dismounts logical disk unit 2.

```c
* DLO:MYFILE/L:0,DYO:DATFIL,DSK/L:4,/L:2
```

You can also reassign a logical disk unit number by simply specifying the /L option with the same logical disk unit number and a different file name.

## 9.3.4 Write-Lock Logical Disk Option (/R:n)

Use the /R:n option to write-lock a logical disk. You then have read-only access to that logical disk. The variable n represents the logical disk unit number; n must be an integer in the range 0–7. The default mode is /W (write-enabled).

The following command mounts logical disk unit 3 to JMS.TXT on DY1: and write-locks it.

```txt
* JMS.TXT/L:3/R:3
```

The next command write-locks logical disk unit 4.

```txt
* /R:4
```

## 9.3.5 Write-Enable Logical Disk Option (/W:n)

Use the /W:n option to write-enable a logical disk. You then have read/write access to that logical disk. The variable n represents the logical disk unit number; n must be an integer in the range 0–7. This is the default mode.

The following command mounts logical disk unit 5 to file JMS.DSK on DL0: and write-enables the new logical disk.

```txt
* DLO:JMS/L:5/W:5
```
