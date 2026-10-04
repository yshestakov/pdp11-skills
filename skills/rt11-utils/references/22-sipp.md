# RT-11 System Utilities Manual: Ch.22 SIPP save image patch program

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 22.1 Calling and Using SIPP
- 22.2 SIPP Options
- 22.3 SIPP Dialog
- 22.4 SIPP Commands
- 22.4.1 Opening and Modifying Locations Within a File
- 22.4.2 Backing Up Through Files
- 22.4.3 Advancing in Bytes
- 22.4.4 Entering Octal Values (;O)
- 22.4.5 Displaying and Entering ASCII Values
- 22.4.6 Displaying and Entering Radix-50 Values
- 22.4.7 Searching Through Files (;S)
- 22.4.8 Verifying (;V)
- 22.4.9 Backing Up to a Previous Prompt
- 22.4.10 Completing Code Modifications
- 22.4.11 Extending Files and Overlay Segments
- 22.5 SIPP Checksum
- 22.6 Running SIPP from an Indirect File
- 20.7 Running SIPP from a Batch Stream

---

# Chapter 22

# Save Image Patch Program (SIPP)

The save image patch program (SIPP) lets you make code modifications to any RT-11 file that exists on a random-access storage volume. You use SIPP primarily for maintaining save image files. Although SIPP is designed for maintaining programs that have been created with the RT-11 Version 4 or later linker, you can use SIPP for pre-Version 4 programs that are not overlaid.

SIPP is also useful for examining locations within a file. If you do not modify any locations within a file, SIPP makes no changes. Also, you can run SIPP from an indirect command file, a BATCH stream, or from the console.

When you run SIPP, you have the option of installing your code modifications when you close the file, or you can create a command file that contains both the code modifications and the instructions necessary for SIPP to install them. You can run this command file as an indirect file whenever you wish. When SIPP patches a file, the creation date of the patched file is changed to the current system date.

Because SIPP does not install code modifications until you have finished making them, SIPP's checksum is not affected by a CTRL/U or DELETE. This feature also makes the code modification, or patching, procedure easier for you.

## NOTE

DIGITAL does not recommend that you modify the following data within a save image file: locations 50, 64, and 66; the Job Status Word; the overlay handler; the overlay tables; and the window definition blocks. SIPP uses these locations for internal calculations and will automatically update them as necessary. Note, however, that if you use the /A option, SIPP does not modify any of these locations.

## 22.1 Calling and Using SIPP

To call SIPP, respond to the dot (.) printed by the keyboard monitor by typing:

• R SIPP RET

The Command String Interpreter (CSI) prints an asterisk (\*) at the left margin of the terminal and waits for a command string. If you enter only a carriage return in response to the asterisk, SIPP prints its current version number. If you type a CTRL/C in response to the asterisk, control returns to the monitor. If you type a CTRL/C in response to any of SIPP's prompts, SIPP prints the following confirmation message:

?SIPP - Are you sure?

If you type Y or any string beginning with Y followed by a carriage return, SIPP aborts the patching procedure, and returns control to the monitor, without making any changes to your file. Any other response returns control to the procedure that was interrupted. You must type two consecutive CTRL/Cs at any other time, including while running from an indirect command file, to get the ?SIPP - Are you sure? message.

Enter a command string according to this general syntax:

[com-filespec = ]input-filespec[/option...]

where:

com-filespec represents the file specifications of the command file that you want SIPP to create. You can run this file as an indirect file. The default file type is .COM. If you do not specify a command file, SIPP does not create one.

input-filespec represents the file specifications of the file you want to modify. If you do not specify a file type, SIPP assumes.SAV.

/option is one of the options listed in Table 22-1.

If you enter only a device specification in response to the CSI asterisk, SIPP opens the first block of that volume and assumes the /A option.

## 22.2 SIPP Options

Table 22-1 summarizes the options that you can use in the CSI command string to SIPP.

## 22.3 SIPP Dialog

After you have entered the initial command string to SIPP, SIPP prints a series of prompts at the terminal. The responses you give to these prompts guide SIPP to the location in the input file or volume where you want to begin code modifications. If the input file is overlaid, the first prompt SIPP prints at the terminal is:

Segment?

Table 22-1: SIPP Options

| Option | Function |
| --- | --- |
| /A | Prevents SIPP from automatically modifying either location 50, the window definition blocks, the overlay table, or the overlay handler. Use /A when you are patching anything other than save image files. When you use the option, SIPP modifies only those locations that you specify. |
| /C | Requires you to enter a checksum after you finish code modifications. If you make no modifications, SIPP ignores /C. The command file will automatically contain /C. You cannot use /C and /D together. See Section 22.5 for more details on the checksum. |
| /D | Use if you do not know the checksum for a particular patch and you want SIPP to create one. SIPP prints the checksum for the patch after you have finished entering all the code modifications. If you make no modifications, SIPP ignores the /D option. You cannot use /C and /D together. |
| /L | When you use /L, SIPP does not modify the input file after the patching session. This option is useful if you wish only to create a command file and preserve the input file. |

Respond to this prompt by typing the number of the overlay segment that contains the locations you want to modify. (SIPP does not print this prompt: if the file you are modifying is not overlaid, if you are using the /A option, or if you are modifying a volume.) You can find the segment number in the program's load map. Type a carriage return, or 0 followed by a carriage return, if you want to modify the program's root segment.

SIPP prompts you for the base address within the program or overlay segment where you want to begin code modifications or examination. SIPP prints the following prompt for both overlaid and non-overlaid files. (Note that the following prompt is the second prompt for overlaid files, and the first prompt for anything else.)

## Base?

If the file you are modifying is overlaid, respond to the last prompt by entering the base address specified on the load map for the segment you want to modify. If the file is not overlaid, enter the load address of the program section you wish to modify or examine.

After you have entered the base address, SIPP prompts you for the offset as follows:

## Offset?

Respond to the offset prompt by typing the offset from the current base where you want to begin modifying or examining your program.

If the offset you specify is an even number, SIPP opens the corresponding location as a word. If the offset is odd, SIPP opens the location as a byte.

Section 22.4 describes how you can alternate between words and bytes as you proceed to modify or examine the file.

After you have responded to Offset?, SIPP prints the following header:

If the file is not overlaid, SIPP does not print the segment column. Below the header, SIPP prints the segment, base, and offset you have specified by responding to the dialog prompts.

A sample dialog format follows. In this example, SIPP is to begin code modifications in overlay segment 2 of program PROG.SAV.

```txt
• R SIPPRET
* PROG=PROGRET
Segment? 2RET
Base? 20000RET
Offset? 100RET
Segment Base Offset Old New?
000002 20000 20100 103425
```

Under the column marked Old, SIPP prints the contents of the currently open location. Under the column designated New?, you can enter either a new value for the current location and/or a command. Section 22.4 gives more details on opening and modifying locations. Table 22–2 summarizes the commands you can enter.

## NOTE

SIPP does not make changes to a file as you type them. Instead, SIPP stores the changes in a buffer, allowing you to abort a partially completed patch operation without leaving behind a partially patched file. When you finish a patching operation by typing CTRL/Y or multiple CTRL/Zs (see Table 22-2), SIPP makes all the changes in one pass.

## 22.4 SIPP Commands

Table 22-2 summarizes the commands you can enter during the code modification procedure and lists the sections in which you can find more details on each command. You can follow command with either a line feed or a carriage return.

Table 22-2: SIPP Commands

| Command | Section | Function |
| --- | --- | --- |
|  | 22.4.1 | Closes the current location without modifying it, and opens and displays the next location. |
| n | 22.4.1 | Enters the value represented by n in the current location, closes it, and opens the next location. |
| ^ | 22.4.2 | Closes the current location without modifying it, and opens the previous location. |
| n^ | 22.4.2 | Enters the value represented by n in the current location, closes it, and opens the previous location. |
| \\ | 22.4.3 | Reopens the current location as a byte (starting with the low, or even, byte for that word). From this point, SIPP will continue opening byte locations and accepting byte values. Do not use this command when in Radix-50 or ASCII mode. |
| / | 22.4.3 | Reopens the current location as a word. SIPP displays the contents of the currently open word location. All further displays and input will be word values. Do not use this command when in Radix-50 or ASCII mode. |
| ;O | 22.4.4 | Reopens the current location as an octal word value. This is the default mode. Use ;O to return to octal after having been in Radix-50 or ASCII mode. All further displays and input are octal values. |
| ;A | 22.4.5 | Displays the byte of the current location as an ASCII value. All further displays are in ASCII, and SIPP advances in byte mode. |
| ;Ax | 22.4.5 | Inserts an ASCII character represented by x in the byte of the current location, closes that byte, and opens and displays the next location. Use this command for inserting only one ASCII character at a time. You can also use this command to search for an ASCII value (see Section 22.4.7). |
| ;R | 22.4.6 | Displays the current location as a word of up to three Radix-50 characters. All further displays are in Radix-50. |
| ;Ryyy | 22.4.6 | Inserts up to three Radix-50 characters represented by yyy into the current location. SIPP then closes the current location, and opens and displays the next location. Use this command for inserting up to three Radix-50 characters. You can also use this command to search for a Radix-50 value (see Section 22.4.7). |
| ;S | 22.4.7 | Searches for a value within the file. When you type this command, SIPP prompts you for a value for which it is to search. SIPP also prompts you for the boundaries within which you want it to conduct the search. |
| ;V | 22.4.8 | Prints all the modifications you have made in the current patching session. You can use this command at any time, except in response to Checksum?. |
| CTRL/Z | 22.4.9 | Backs up to the previous prompt: Offset?, Base?, or Segment?. This command allows you insert code modifications in more than one area of the file during the same patching session. |
| CTRL/Y | 22.4.10 | Completes the current patching session, installs the patch, creates the command file (if requested), and prompts you with an asterisk for another file specification. |

## 22.4.1 Opening and Modifying Locations Within a File

As stated earlier, after you guide SIPP to the location in the file where you want to begin making code modifications, SIPP prints out a header under which it lists the address and contents of the location specified, called the current location. Under the last column in the header, New?, you can enter a value that replaces the contents of the current location. After you enter the new value, type a carriage return to advance to the next location.

In the following example, the value 240 is inserted in the current location. Next, a carriage return advances SIPP to the next 16-bit location.

$$
\begin{array}{c c c c} \text {Base} & \text {Offset} & \text {Old} & \text {New?} \\ 0 0 1 0 0 0 & 0 0 1 2 0 0 & 0 0 4 7 6 7 & 2 4 0 _ {\text {RET}} \\ 0 0 1 0 0 0 & 0 0 1 2 0 2 & 0 0 3 1 0 6 \end{array}
$$

If you do not want to modify the current location, simply type a carriage return to advance to the next location.

## 22.4.2 Backing Up Through Files

When you type the up-arrow character ( $^{\wedge}$ ) followed by a carriage return in place of entering data into the current location, SIPP closes the current location and opens the previous location. If you specify a value followed by an up-arrow, SIPP enters that value into the current location, closes that location, and opens that location.

If you type an up-arrow when the offset from a specified base is 0, SIPP opens the previous location and displays the offset as a double-precision negative number.

In the following example, the value 112000 is entered into the current location, and the previous location is opened.

$$
\begin{array}{c c c c} \text {Base} & \text {Offset} & \text {Old} & \text {New?} \\ 0 0 2 0 0 0 & 0 0 2 1 3 4 & 0 2 0 0 2 7 & 1 1 2 0 0 0 ^ {\text {RET}} \\ 0 0 2 0 0 0 & 0 0 2 1 3 2 & 0 0 1 7 3 2 \end{array}
$$

In the last example, notice how SIPP decrements the offset by 2 to designate the previous 16-bit location.

You can use the up-arrow after you use the backslash (\) to back up to the previous byte (if currently in word mode). You can also use the up-arrow after you use the slash (/) to back up to the previous word (if currently in word mode).

## 22.4.3 Advancing in Bytes

By default, SIPP operates in word mode. That is, locations are displayed as 16-bit words, and values are displayed and entered as word values. If you type the backslash character (\), SIPP closes the current location, and reopens the low, or even byte, of that location. Values that are displayed and entered from this point are in bytes.

To revert to word mode, type the slash character (/). When you type the slash, SIPP reopens the current location as a 16-bit word.

The following example uses the backslash to advance in byte mode, and then the slash to revert to word mode. Notice that SIPP prints out a new header each time it changes from word to byte mode, and vice versa.

| Base | Offset | Old | New? |
| --- | --- | --- | --- |
| 0020000 | 002112 | 003002 |  |
|  |  |  | \\RET |
| Base | Offset | Old | New? |
| 002000 | 002112 | 002 |  |
| 002000 | 002113 | 006 | RET |
| 002000 | 002114 | 132 | RET/RET |
| Base | Offset | Old | New? |
| 002000 | 002114 | 003132 |  |

If you are in byte mode when you get the Offset? prompt, SIPP automatically resets itself to word mode.

## 22.4.4 Entering Octal Values (;O)

Use the ;O command, followed by a carriage return, to reopen the current location, and display its contents as an octal value. Since octal mode is the default setting, you need to use it only if you are currently operating in ASCII or Radix-50 mode and wish to revert to octal mode. You can also use the ;O command to switch from byte mode to word mode.

The following example uses the ;O command to switch from ASCII mode to octal mode.

```asm
Base          Offset      Old      New?
002000       002100   051101
002000       002100     <A>        ;ARET
                    ;ORET

Base          Offset      Old      New?
002000       002100   051101
```

Note that unlike the ;A and ;R commands, ;O accepts no optional argument. If you return to the Offset? prompt, SIPP automatically resets itself to octal mode.

## 22.4.5 Displaying and Entering ASCII Values

Use the ;A command, followed by a carriage return, to open the current location as a byte and display its contents as an ASCII value. When you use the ;A command, SIPP continues to display contents in ASCII until you use the ;O or ;R command. Note that when you operate in ASCII mode, you advance through the file in byte mode.

The following example uses the ;A command to open the low byte of the current location and display its contents as an ASCII value.

| Base | Offset | Old | New? |
| --- | --- | --- | --- |
| 003000 | 003100 | 050524 | ;ARET |
| 003000 | 003100 | &lt;T> | RET |
| 003000 | 003101 | &lt;Q> |  |

Use the ;Ax command to insert an ASCII character, represented by x, into the low byte of the current location. When you use the ;Ax command, SIPP enters the ASCII character directly into the current byte, closes that byte, opens and displays the next location as an octal, ASCII, or Radix-50 value (depending on what mode you were in prior to using the ;Ax command). Note that you can insert only one ASCII character at a time, and that you should not insert control characters. You can use the ;Ax command when displaying in ASCII mode.

The next example uses the ;Ax command to enter the ASCII character, W, into the current byte and proceed to the next byte.

| Base | Offset | Old | New? |
| --- | --- | --- | --- |
| 003000 | 003100 | 050524 | ;AWRET |
| 003000 | 003101 | 121 |  |

You can also use the ;Ax command to search for an ASCII value (see Section 22.4.7).

## 22.4.6 Displaying and Entering Radix-50 Values

Use the ;R command, followed by a carriage return, to reopen the current location and display its contents in Radix-50. When you use the ;R command, SIPP continues in Radix-50 mode until you use either the ;A or ;O command. Note that Radix-50 mode advances in word mode.

The following example uses the ;R command to reopen the current location and display its contents as a Radix-50 value.

| Base | Offset | Old | New? |
| --- | --- | --- | --- |
| 001000 | 005220 | 071070 | ;RRET |
| 001000 | 005220 |  | RET |
| 001000 | 005222 |  |  |

If the contents of a location is an invalid Radix-50 value, SIPP displays the contents as &lt;???&gt;.

You can use the ;Ryyy command to insert up to three Radix-50 characters, represented by yyy, into the current location. When you use the ;Ryyy command, SIPP inserts the Radix-50 value into the current location, closes the current location, and opens and displays the contents of the next location as an octal, ASCII, or Radix-50 value (depending on what mode you were in prior to using the ;Ryyy command).

If you use the ;Ryyy command, and you enter only two Radix-50 characters, SIPP inserts a blank as the third character. Likewise, if you enter only one Radix-50 character, SIPP inserts blanks for the second and third characters. If you use an imbedded blank (for example, X Z), SIPP inserts all characters as typed. Note that you can insert up to only three Radix-50 characters at a time. Use the ;Ryyy command only when the low byte of the current location is open; SIPP prints an error message if you attempt to insert a Radix-50 value when the high byte of the current location is open.

The following Radix-50 values are valid for use with the ;Ryyy command:
A through Z
0 through 9
\$
\*
.
%

Note that a space is also a valid Radix-50 character, and that SIPP translates the percentage character to a dot (.).

The following example uses the ;Ryyy command to insert three Radix-50 characters in the current location, and proceed to the next location.

Base          Offset      Old      New?
001000       005332    000240     ;RABCRET
001000       005334    002110

You can also use the ;Ryyy command to search for a Radix-50 value (see Section 22.4.7).

## 22.4.7 Searching Through Files (;S)

You can use the ;S command to search between two specified boundaries of a file for a given value. With this feature, you can find the location where you want to make a change by searching for a specific value.

To request a search, type the following in response to any of SIPP's dialog questions or in place of entering new data into the current location.

Do not type the ;S command in response to the Checksum? prompt. After you type the ;S command, SIPP responds with the following prompt:

Enter the value for which you want SIPP to search. You can use the ;Ax or ;Ryyy command in response to the last prompt to search for ASCII or Radix-50 values. If you type a backslash after the value you enter, SIPP searches for a byte value. Otherwise, it searches for a word value. Note that if you use the ;Ax notation to search for an ASCII value, SIPP conducts the search in byte mode.

SIPP then asks for the lower address limit at which to begin the search:

Start?

Enter an address, followed by a carriage return, or just a carriage return. If you enter a carriage return, SIPP begins its search at the beginning of the file. If you enter an address, SIPP begins the search at that address. If you are searching through an overlay segment, use the following notation for the start address:

m : m .

In the n:m notation, n represents the number of the segment you want to search, and m represents the offset from the start of the segment where you want SIPP to begin the search.

SIPP then asks for the upper address limit for the search:

End?

You can enter an address (including the n:m notation) or a carriage return. If you enter a carriage return, SIPP searches to the end of the file or volume. (If you use the /A option, SIPP searches to the end of the last block in the file or volume; otherwise it searches up to and including the last address in the program.) If you enter an address, SIPP conducts the search up to, but not including, that address.

After you have specified the search limits, the search begins. Each time SIPP finds a value that matches the one you specified, SIPP prints out the address of that value. If you use the /A option or if SIPP is searching the root segment of a program, SIPP prints the search results as follows:

Found at nnnnnn

If a search crosses segments in an overlaid file, SIPP prints the following each time it finds the specified value:

Found at seg:mm,nnn

In the seg:mmm,nnn notation, seg represents the segment number, mmm represents the load map address of the segment, and nnn represents the offset from the start of the specified segment. Note that if you are searching an overlaid file, and you have specified the /A option in the command line, SIPP does not use the seg:mmm,nnn notation.

## 22.4.8 Verifying (;V)

Use the ;V command to list at the terminal all the changes you have made during the current patching session. After SIPP prints out the addresses and new contents of all the locations that have changed, SIPP returns you to the operation that was interrupted.

You can use the ;V command at any time, except in response to the Check-sum? prompt and the search Start?, and End? prompts. You can use the ;V command in response to the Search for? prompt.

The following example uses the ;V command to list at the terminal all the changes that have been made during the current patching session.

| Base | Offset | Old | New |
| --- | --- | --- | --- |
| 003000 | 003200 | 003112 | 240RET |
| 003000 | 003202 | 002300 | RET |
| 003000 | 003204 | 002300 | RET |
| 003000 | 003206 | 000230 | 240RET |
| 003000 | 003210 | 000101 | ;VRET |
| Base | Offset | Old | New? |
| 003000 | 003200 | 003112 | 000240 |
| 003000 | 003206 | 000230 | 000240 |
| Base | Offset | Old | New? |
| 003000 | 003210 | 000101 |  |

Note that when you use the ;V command to verify your modifications, all displays are in octal words. Note also that if you change a location and later restore that location to its original contents, SIPP includes that location in the verification.

## 22.4.9 Backing Up to a Previous Prompt

You can use the CTRL/Z sequence (or up-arrow Z), followed by a carriage return, to back up to a previous prompt. For example, after you have modified a series of locations, you can type CTRL/Z, followed by a carriage return, to back up to the Offset? prompt. Backing up to a previous prompt enables you to examine and/or modify other series of locations in your program.

If you use CTRL/Z in place of entering a value into a location, SIPP prompts Offset?. If you type CTRL/Z, followed by carriage return, in response to Offset?, SIPP prompts Base?. If you type yet another CTRL/Z, followed by a carriage return, SIPP either:

1. Prompts Segment?, if the file is overlaid, or

2. Prompts you for a checksum (if you used /C), then installs the patch (if the checksum is valid). (Note that if you have used the /L option, SIPP does not install the patch, but does create the command file, if requested.)

If the file is overlaid, and you type another CTRL/Z followed by a carriage return sequence in response to Segment?, SIPP prompts you for a checksum (if specified) then installs the modifications.

Using CTRL/Y provides a more efficient way of installing a patch (see the following subsection). The CTRL/Z sequence is designed primarily to request a particular prompt.

## 22.4.10 Completing Code Modifications

You can type the CTRL/Y sequence (or up-arrow Y), followed by a carriage return, to install the code modifications you have entered. If you have used the /C option, which requires you to enter a checksum, SIPP will prompt you for a checksum before it installs the modifications. If the checksum you type is valid, SIPP then installs the patch. If you have used the /L option and you enter the correct checksum, SIPP does not install the patch, but does create the command file, if requested.

After SIPP installs the modifications, an asterisk appears in the left margin, indicating that SIPP is ready to accept a new command string.

## 22.4.11 Extending Files and Overlay Segments

The limits to which you can extend programs and overlay segments while patching vary, depending on if the program is

\- Nonoverlaid

Overlaid, but has only low memory overlays

\- Overlaid, but has only extended memory overlays

\- Overlaid, and has both low memory and extended memory overlays

The subsections that follow describe in detail the restrictions on extending programs, root sections, and overlay segments. Each subsection also details what data within your program SIPP does or does not automatically modify as you extend root sections and/or overlay segments.

Listed below are the data that SIPP may automatically modify as you make extensions. (Note that each is identified by an abbreviation; the subsections that follow reference these data by their abbreviations.)

Location 50 Contains the last address used by the program, if the program is nonoverlaid. If the program has low memory overlays, location 50 contains the last address used by the low memory overlay region(s). If the program has only extended memory overlays, location 50 contains the last address used by the root.

Reg. Size Indicates the size of the extended memory region. This data appears in the extended memory overlay handler.

High Root + 2 Indicates the address of the next available location beyond the root segment. This data appears in either the low memory overlay handler or the extended memory handler.

High /O + 2 Indicates the address of the next available location beyond the last low memory overlay region. This data appears in either the low memory overlay handler or the extended memory overlay handler.

Wdcnt. in Seg. Indicates the number of words in the current overlay segment. This data appears in the overlay handler segment table.

WDB Size and Length Indicates the window size and length to map in the window definition block (WDB) for the extended memory overlay you are extending. This data appears in each extended memory overlay segment's WDB.

WDB Offset Indicates the offset into the extended memory region of the windows following the segment you are extending. This data appears in each extended memory overlay segment's WDB.

22.4.11.1 Nonoverlaid Program — If necessary, SIPP automatically extends a nonoverlaid program up to the end of the last block of the save image on which the program exists (SIPP automatically modifies location 50). Refer to DUP (Chapter 6) for details on extending a nonoverlaid program beyond that point.

22.4.11.2 Overlaid Program, Low Memory Overlays Only — If your program is overlaid, but has only low memory overlays, SIPP does not permit you to extend the root. If an overlay segment is not in the last overlay region, you can extend it to the size of the largest segment in its region. If the overlay segment is in the last overlay region, you can extend it to the end of the last block of that overlay segment.

Table 22–3 shows the locations that SIPP modifies if necessary when you extend the root or overlay segment of a program that has low memory overlays only. Note in this table that there is a column heading for an overlay segment that is not the largest in its overlay region (Not Largest in Region), and for an overlay segment that you extend beyond the largest overlay segment in its region (Past Largest in Last Region). YES indicates that SIPP does modify the data in question if necessary, NO indicates SIPP does not modify the data in question, and N/A indicates that the data in question is not applicable.

22.4.11.3 Overlaid Program, Extended Memory Overlays Only — If your program is overlaid, but has extended memory overlays only, you can extend the root segment up to the end of the last block on which the root resides. You can also extend any overlay segment up to the end of the last block of that particular segment, so long as you do not exceed the physical address space.

Table 22-3: Overlaid Program Segment Limits

|  | Not Largest in Region | Past Largest in Last Region |
| --- | --- | --- |
| Location 50 | NO | YES |
| Reg. Size | N/A | N/A |
| High Root + 2 | NO | NO |
| High /O + 2 | NO | YES |
| Wdcnt. in Seg. | YES | YES |
| WDB Size and Length | N/A | N/A |
| WDB Offset | N/A | N/A |

Table 22–4 shows the locations that SIPP modifies if necessary when you extend the root or overlay segment of a program that has extended memory overlays only. Note in this table that there is a column heading for the root (Root), an overlay segment that is not the largest in its overlay region (Not Largest), and an overlay segment that you extend beyond the largest overlay segment in its region (Past Largest). YES indicates that SIPP does modify the data in question if necessary, and NO indicates SIPP does not modify the data in question.

Table 22-4: Overlaid Program Segment Limits

|  | Root | Not Largest | Past Largest |
| --- | --- | --- | --- |
| Location 50 | YES | NO | NO |
| Reg. Size | NO | YES | YES |
| High Root + 2 | YES | NO | NO |
| High /O + 2 | YES | NO | NO |
| Wdcnt. in Seg. | NO | YES | YES |
| WDB Size and Length | NO | YES | YES |
| WDB Offset | NO | YES | YES |

22.4.11.4 Overlaid Program, Both Low Memory and Extended Memory Overlays — If your program has both low memory and extended memory overlays, SIPP does not permit you to extend the root segment. You can extend any low memory overlay segment up to the size of the largest segment in the same region. If the low memory overlay segment is in the last low memory overlay region, you can extend it to the end of the last block of that overlay segment.

You can extend any extended memory overlay segment up to the end of the block limit of that particular segment, so long as you do not exceed your physical address space.

Table 22–5 shows the locations that SIPP modifies if necessary when you extend the root or overlay segment of a program that has both low memory and extended memory overlays. Note in this table that there is a column heading for a low memory overlay segment that is not the largest in its overlay region (/O Not Largest), a low memory overlay segment that extends beyond the largest segment in its region (/O Past Largest), an extended memory overlay segment that is not the largest in its region (/V Not Largest), and an extended memory overlay segment that extends beyond the largest segment in its region (/V Past Largest). YES indicates that SIPP does modify the data in question if necessary, and NO indicates SIPP does not modify the data in question.

Table 22-5: Overlaid Program Segment Limits

|  | /ONot Largest | /OPast Largest | /VNot Largest | /VPast Largest |
| --- | --- | --- | --- | --- |
| Location 50 | NO | YES | NO | NO |
| Reg. Size | NO | NO | YES | YES |
| High Root + 2 | NO | NO | NO | NO |
| High /O + 2 | NO | YES | NO | NO |
| Wdcnt. in Seg. | YES | YES | YES | YES |
| WDB Size and Length | NO | NO | YES | YES |
| WDB Offset | NO | NO | YES | YES |

## NOTE

It is possible when extending extended memory overlay segments to exceed the 96K word physical address space (SIPP prints a warning message if you do this). If you do exceed the 96K word limit, use the CTRL/C sequence to abort the patching session; many system communication area locations will have already changed to contain invalid data.

## 22.5 SIPP Checksum

SIPP's checksum algorithm creates the checksum only after you have finished creating a patch. The checksum helps you verify your work. It lets you compare the patch you make to another that is known to be correct. The checksum does not tell you where your error is, but it does tell you that an inconsistency exists. SIPP's checksum algorithm uses the calculated address of a changed location and its new contents. SIPP includes in its checksum only those values of locations that have changed during a patching session.

If you change a word several times during a patching session, SIPP enters into its checksum only the last value you specify. This feature allows you to correct a mistake, yet maintain a valid checksum.

If you are creating a checksum (/D option), SIPP prints the following when you finish the patch:

Checksum=nnnnnnn

If you are verifying a checksum (/C option), SIPP asks the following when you complete the patch:

Checksum?

Respond by entering the checksum for the patch.

If the checksum is incorrect, SIPP prints:

?SIPP-E-Checksum error

SIPP then returns to the beginning of its dialog (the Segment? or Base? prompt), allowing you to find and correct your error without exiting from the patching session. In this way, you do not lose the changes you have made; you can go back and verify them (see Section 22.4.8 for details on the verify command).

SIPP does not install the patch until you enter the correct checksum. You can type CTRL/C to abort the patching procedure.

## 22.6 Running SIPP from an Indirect File

The SIPP indirect command file contains the commands necessary to install a patch in a particular file or volume. The order in which the modifications appear in the command file may not correspond to the actual sequence in which you typed them; however, the changes are the same as you typed. The contents of the command file always appear as octal word values. When you specify a command file in the initial command string, SIPP creates that file for use as an indirect command file. If you use the /L option when you create the command file, SIPP installs the patch contained within only when you run this file as an indirect command file. By default, SIPP assigns this file a .COM default file type.

A command file always contains a checksum generated during the console input session. If you use the /C option, SIPP prompts you for a checksum after you finish making the code modifications. If the checksum is valid, SIPP completes this command file, and you can execute this command file at any time you wish. If you use the /A option, SIPP inserts /A in the command file.

The command file TEST.COM is created in the following example. (Note that SIPP does not modify TEST.SAV in the example, because /L was specified in the command string.)

```asm
.R SIPPRET
* TEST=TEST/LRET
Base?      5000RET
Offset? 20RET

Base          Offset      Old      New
005000         000020    032764     240RET
005000         000022    177400     240RET
005000         000024    000002     1016RET
005000         000026    001016     CTRL/YRET
* CTRL/C
```

A copy of TEST.COM as it appears in indirect command file format follows.

```txt
. TYPE TEST.COM
RUN SIPP
DK:TEST.SAV/C
5000
20
240
240
1016
^Y
165617
^C
```

The number 165617 (the last line in the file) is the checksum for that patch.

To run the command file TEST.COM as an indirect file, type the following in response to the monitor dot.

```txt
@TESTRET
```

If you run a SIPP indirect command file when the SET TT: QUIET setting is in effect, SIPP overstrikes its output at the terminal but does install the patch correctly.

## 20.7 Running SIPP from a Batch Stream

An easy way to install a patch from a BATCH stream is to follow the instructions for creating a command file. When you get your command file, simply open it with an editor, enter the BATCH commands, and insert a dot before the line RUN SIPP, and insert asterisks before each subsequent line. Remember to remove the CTRL/C (^C) from the command file. An example of preparing TEST.COM (from the previous section) for a BATCH stream follows.

```txt
$JOB/RT11
TTYIO
.RUN SIPP
*DK:TEST.SAV/C
*5000
*20
*240
*240
*1016
*^Y
*165617
$EOJ
```
