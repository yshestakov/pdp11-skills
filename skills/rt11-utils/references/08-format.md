# RT-11 System Utilities Manual: Ch.8 FORMAT volume formatting

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 8.1 Calling And Terminating Format
- 8.2 FORMAT Command String Syntax
- 8.3 FORMAT Confirmation Prompts
- 8.4 Options
- 8.4.1 Default Format
- 8.4.2 Pattern Verification Option (/P:n)
- 8.4.3 Single-Density Option (/S)
- 8.4.4 Verification Option (/V[:ONL])
- 8.4.5 Wait Option (/W)
- 8.4.6 No Query Option (/Y)

---

## Chapter 8

# Volume Formatting Program (FORMAT)

The FORMAT utility program formats disks and diskettes. You can also use FORMAT to convert single-density diskettes to double-density and vice versa. FORMAT can format RX01/RX02 diskettes, RD50/RD51 disks, RK05 disks; RK06/RK07 disks, and RP02/RP03 disks.

Formatting a volume makes that volume usable by RT-11. When you format a volume, FORMAT writes headers on each block in that volume. The header of a block contains data the device controller uses to transfer information to and from that block.

RD50/RD51 disks can be formatted for the DW: handler only.

When you use FORMAT to convert a single-density diskette to double density, or vice versa, FORMAT writes media density marks on each block of the diskette. You can format a diskette only in a double-density diskette drive, DY:. If you attempt to format a diskette in a single-density diskette drive, DX:, FORMAT prints an error message.

Reformatting with the FORMAT program can also eliminate bad blocks that disks and diskettes sometimes develop as a result of age and use. Although formatting does not guarantee that each bad block will be eliminated, formatting can reduce the number of bad blocks.

## NOTE

FORMAT destroys any data that currently exists on the disk.

## 8.1 Calling And Terminating Format

To call FORMAT from the system device, respond to the dot (.) printed by the keyboard monitor by typing:

. R FORMAT RET

The Command String Interpreter (CSI) prints an asterisk (\*) at the left margin of the terminal and waits for a command string. If you enter only a carriage return in response to the asterisk, FORMAT prints its current version number. You can type CTRL/C to halt FORMAT and return control to the monitor when FORMAT is waiting for input from the console terminal. You cannot halt FORMAT during an operation by typing two CTRL/Cs.

If you interrupt the program during a formatting operation by some other means, the disk or diskette involved is not completely formatted. You must restart the operation on the same disk or diskette and allow it to run to completion.

## 8.2 FORMAT Command String Syntax

Chapter 1, Command String Interpreter, describes the general syntax of the command line that system utility programs accept. FORMAT accepts one device specification (either a physical or logical device name) followed, if necessary, by one or more options. An RK05 disk you wish to format can be located in any unit (0–7) of device RK:. A diskette you need to format must be mounted on an RX02 device (device DY:), but it can be located in any unit (0–3) of that device. You cannot format diskettes on an RX01 device.

## 8.3 FORMAT Confirmation Prompts

FORMAT automatically prints the device-name:/Are you sure? message before it begins any operation. The device name that prints out in the message is the physical name of the device you specify in the command line. Therefore, if you use a logical device name in the command line, the device name that FORMAT displays in the confirmation message is different from the name you type. If you want the operation to continue, type Y or any string beginning with Y followed by a carriage return in response to the confirmation message. Type N or CTRL/C to prevent the formatting operation from occurring. Any other response causes FORMAT to repeat the prompt.

You can use FORMAT from an indirect command file. To satisfy the device-name:/Are you sure? message, enter a Y as the next line of the indirect file immediately following the FORMAT command line. You can suppress the confirmation message completely by using the /Y option in the FORMAT command line. If you use /Y, you do not need to enter the Y on the following line.

If you try to format a volume while a foreground job is loaded, the system prints the following message.

Foresround Loaded.

&lt;dev:&gt;/FORMAT-Are you sure?

Type Y or any string beginning with Y followed by a carriage return to continue with the formatting operation. Type N or any string beginning with N, or CTRL/C, to abort the operation. Any other response causes the message to repeat.

## NOTE

Although you can format or verify a volume while a foreground job is loaded, it is not recommended. If you try to format or verify a volume that the foreground job is using, data on the volume will be written over and corrupted, which may cause the foreground job or the system to crash.

If you try to format a volume that contains protected files, the system prints the following message.

Volume contains protected files; Are you sure?

Type Y or any string beginning with Y to continue the formatting operation. Type N or any string beginning with N, or CTRL/C, to abort the operation. Any other response causes the message to repeat.

After you format a disk, you should use the INITIALIZE command to prepare the volume for use with RT-11. See Chapter 4 of the RT-11 System User's Guide for more information on the INITIALIZE command.

## 8.4 Options

Options that you specify in a command line to the FORMAT program perform several functions. Table 8–1 summarizes these options and the operations they perform. You can combine these options, if necessary, in any order. More detailed explanations of the options are arranged alphabetically by option name in the sections that follow the table.

Table 8-1: FORMAT Options

| Option | Section | Function |
| --- | --- | --- |
| none | 8.4.1 | If you do not supply an option, FORMAT formats the volume you specify. If you specify an RX01 or RX02 diskette, the default operation that occurs is double-density diskette formatting. You can use /Y and /W with the default operation. |
| /P:n | 8.4.2 | Pattern verification option, where n represents an octal integer in the range 0 to 177777. The option specifies the specific 16-bit word pattern that FORMAT uses to write to the volume, and read from the volume, during the process of verification. If you do not use this option, FORMAT defaults to /P:200. |
| /S | 8.4.3 | Single-density option. This option formats a diskette in a single-density format. |
| /V[:ONL] | 8.4.4 | Verification option. When you specify /V in the command line, FORMAT first formats the specified volume, then verifies it. If you specify /V:ONL, FORMAT only verifies the specified device. Note that you can use /V:ONL with RX01 diskettes, RL01/RL02 disks, TU56 (DECtape I), and TU58 (DECtape II). |
| /W | 8.4.5 | Wait option. This option permits you to substitute another volume for the volume you specify in the command line, format the second volume, then replace the original volume. Note that this option is invalid for RC25 disks, RD51 disks, and RX50 diskettes. |
| /Y | 8.4.6 | No query option. This option suppresses the Are you sure? message FORMAT automatically prints before each operation. |

## 8.4.1 Default Format

To format diskettes in double-density mode, specify the device name in the command line. You can also use /Y to suppress the query message, and /W to pause for a volume substitution. The following example formats the diskette in DY: evice unit 1 as a double-density diskette.

```txt
* DY1:
DY1:/FORMAT-Are you sure? Y
?FORMAT-I-Formattins complete
*
```

To format an RK05 or RK06/07 disk, specify the device name in the command line. You can also use /Y to suppress the query message and /W to pause for a volume substitution. The following example formats an RK05 disk in RK: device unit 1:

```txt
* RK1:
RK1:/FORMAT-Are you sure? Y
?FORMAT-I-Formattins complete
*
```

When you format an RK06 or RK07 disk, FORMAT lists the block numbers of all the bad blocks in the manufacturer's bad block table and in the software bad block table.

## 8.4.2 Pattern Verification Option (/P:n)

When you use the /P:n option with /V[:ONL] in the command line; you can specify the 16-bit word pattern you want FORMAT to use when it performs volume verification. The argument n represents an octal integer in the range 0 to 177777 that specifies the pattern or successive patterns you want FORMAT to use. Table 8–2 lists the verification patterns FORMAT uses and the corresponding values of n.

In /P:n, the number you specify for n indicates the value for the bit patterns to be run during verification. Bits set in /P:n select the patterns to be run. Table 8–2 shows which bit, when set, corresponds to each 16-bit verification pattern. To calculate the equivalent value of n, convert the bit set to an octal number. For example, FORMAT runs pattern 3 when bit 2 is set. When bit 2 alone is set, the equivalent octal number is 4.

Table 8–2 gives the equivalent n value for each verification bit pattern. If you want to run more than one bit pattern, add the values of n for the patterns you select. For example, suppose you want to run bit patterns 1, 3, and 5. The corresponding values of n are 1, 4, and 20, for a sum of 25. This is the value of n you would specify with /P to run all three bit patterns.

FORMAT converts the number you specify into a binary number; the number of each set bit specifies which patterns to run. The number 25 translates to the binary number 010 101. In the number 010 101, bits 0, 2, and 4 are set. As Table 8–2 shows, bit 0 specifies pattern 1, bit 2 specifies pattern 3, and bit 4 specifies pattern 5. If you specify /P:25, FORMAT runs patterns 1, 3, and 5. If you specify /P:255, FORMAT runs patterns 1, 3, 4, 6, and 8. If you specify /P:777, FORMAT runs patterns 1 though 9 during verification. If you do not use the /P:n option, FORMAT runs only pattern 8.

Table 8-2: Verification Bit Patterns

| Pattern | Bit Set | n | 16-Bit Pattern |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 000000 |
| 2 | 1 | 2 | 177777 |
| 3 | 2 | 4 | 163126 |
| 4 | 3 | 10 | 125252 |
| 5 | 4 | 20 | 052525 |
| 6 | 5 | 40 | 007417 |
| 7 | 6 | 100 | 021042 |
| 8 | 7 | 200 | 104210 |
| 9 | 8 | 400 | 155555 |
| 10 | 9 | 1000 | 145454 |
| 11 | 10 | 2000 | 146314 |
| 12 | 11 | 4000 | * |
| 13 | 12 | 10000 | * |
| 14 | 13 | 20000 | * |
| 15 | 14 | 40000 | * |
| 16 | 15 | 100000 | * |

\* These patterns are reserved for future use. Currently these bit patterns run the default bit pattern (pattern 8).

When you use the /P:n option, and you specify more than one pattern, FORMAT runs each pattern successively. After it completes verification, FORMAT prints at the terminal each bad block it found during each verification pass. The format of the verification report is:

```txt
PATTERN #x
----------.
nnnnnnn
```

In the example above, x represents the pattern number, and nnnnnn represents the bad block number. FORMAT makes a separate verification pass for each pattern it runs, and reports on each pass.

The sample command line that follows formats volume RK1: and verifies it with patterns 4, 5, and 6.

```txt
* RK1:/V/P:70
RK1:/FORMAT-Are you sure? Y
?FORMAT-I-Formatting complete
PATTERN #6
PATTERN #5
PATTERN #4
?FORMAT-I-Verification complete
*
```

The next sample command line verifies volume DL0: with pattern 2.

```txt
* DLO:/V:ONL/P:2
DLO:/VERIFY-Are you sure? Y
PATTERN #2
?FORMAT-I-Verification complete
```

## 8.4.3 Single-Density Option (/S)

Use /S to format a diskette in single-density mode. You can also use /Y to suppress the query message and /W to pause for a volume substitution.

The following example formats the diskette in DY: device unit 1 as a single-density diskette.

```txt
* DY1:/S
DY1:/FORMAT-Are you sure? Y
?FORMAT-I-Formattins complete
*
```

## 8.4.4 Verification Option (/V[:ONL])

Use the /V[:ONL] option to provide a verification of all blocks on a volume immediately following formatting. If you use the optional argument :ONL, FORMAT executes only the verification procedure. Although FORMAT can format only a limited assortment of storage volumes, it can verify any disk, diskette, or DECtape II.

In the process of verifying a storage volume, FORMAT first writes a 16-bit word pattern on each block of the specified volume, and then reads each pattern. For each read or write error it encounters, FORMAT prints at the terminal the block number for each block that generated the error.

## NOTE

FORMAT destroys data on any storage volume it verifies.

The following command line uses /V to verify an RK05 disk after formatting.

```txt
* RKO:/V
RXO:/FORMAT-Are you sure? Y
?FORMAT-I-Formatting complete
PATTERN #B
?FORMAT-I-Verification complete
```

The next example uses /V:ONL to verify, but not format, an RX01.

```txt
* DX1:/V:ONL
DX1:/VERIFY-Are you sure? Y
PATTERN #8
?FORMAT-I-Verification complete
```

## 8.4.5 Wait Option (/W)

Use /W to pause before formatting begins in order to substitute a second volume for the disk you specify in the command line. This is useful for single-disk systems.

After the FORMAT program accepts your command line, it pauses while you exchange volumes. Type Y or any string beginning with Y followed by a carriage return in response to the Continue? prompt when you are ready for formatting to begin. If you type N or any string beginning with N, or CTRL/C, the operation is not performed and the monitor prompt (.) appears. Any other response causes the message to repeat.

When formatting completes, the program pauses again while you replace the original volume. Respond to the Continue? prompt by typing Y or any string beginning with Y followed by a carriage return.

You can combine /W with any other option. The following example formats the diskette in DY: device unit 1 as a single-density diskette.

```txt
* DY1:/W/S
DY1:/FORMAT-Are you sure? Y
Mount input volume in _<dev:>; Continue? Y
?FORMAT-I-Formattins complete
Mount system volume in _<dev:>; Continue? Y
*
```

When you use the /W option, make sure that FORMAT is on the system volume.

## 8.4.6 No Query Option (/Y)

Use /Y to suppress the Are you sure? confirmation message FORMAT prints before each operation begins. When you use /Y, formatting begins as soon as FORMAT accepts and interprets your command line.

The following example formats the diskette in DY: device unit 1 as a double-density diskette.

```txt
* DY1:/Y
?FORMAT-I-Formattins complete
*
```

(1)
