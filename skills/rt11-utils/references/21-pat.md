# RT-11 System Utilities Manual: Ch.21 PAT object module patch program

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 21.1 Calling and Using PAT
- 21.2 PAT Command String Syntax
- 21.3 How PAT Effects Updates
- 21.3.1 Input File
- 21.3.2 Correction File
- 21.4 Updating Object Modules
- 21.4.1 Overlaying Lines in a Module
- 21.4.2 Adding a Subroutine to a Module
- 21.5 Determining and Validating the Contents of a File

---

# Chapter 21 Object Module Patch Program (PAT)

The RT-11 object module patch program (PAT) allows you to update code in a relocatable binary object module (.OBJ file). PAT does not permit you to examine the octal contents of an object module. PAT makes the patch to the object module by means of the procedure outlined in Figure 21-2. One advantage to using PAT is that you can add relatively large patches to an object module without performing any octal calculations. PAT accepts a file containing corrections or additional instructions and applies these corrections and additions to the original object module. You prepare correction input in source form and assemble it with the MACRO-11 assembler.

Two files form the input to PAT: the original input file, and a correction file containing the corrections and additions to that input file. The original input file consists of one or more concatenated object modules, only one of which can be corrected with a single execution of the PAT utility. The correction file consists of object code that, when linked by the linker, either replaces or appends to the original object module. Output from PAT is the updated input file.

It is always good practice to create a backup version of the file you want to patch before you use PAT to make the changes.

## 21.1 Calling and Using PAT

To call PAT from the system device, respond to the dot (.) printed by the keyboard monitor by typing:

## • R PAT RET

The Command String Interpreter (CSI) prints an asterisk at the left margin of the console terminal when it is ready to accept a command line. Chapter 1 describes the general syntax of the command line PAT accepts.

Type two CTRL/Cs to halt PAT at any time (or a single CTRL/C to halt PAT when it is waiting for console terminal input) and return control to the monitor. To restart PAT, type R PAT in response to the monitor's dot. When PAT completes an update operation it returns control to CSI level (\*).

Figure 21-1 shows how you use PAT to update a file (FILE1) consisting of three object modules (MOD1, MOD2, and MOD3) by appending a correction file to MOD2. After running PAT, you use the linker to relink the updated module with the rest of the file and to produce a corrected executable program.

Figure 21-1: Updating a Module Using PAT

[figure omitted]

There are several steps you must follow when using PAT to update a file. First, use a text editor to create the correction file. Then, assemble the correction file to produce an object module. Next, submit the input file and the correction file in object module form to PAT for processing. Finally, link the updated object module, along with the object modules that make up the rest of the file, to resolve global symbols and create an executable program. Figure 21–2 shows the processing steps involved in generating an updated executable file using PAT.

## 21.2 PAT Command String Syntax

Specify the PAT command string in the following form:

$$
[ \text {output - filespec} ] = \text {input - filespec} [ / \mathrm{C} [: \mathrm{n} ] ], \text {correct - filespec} [ / \mathrm{C} [: \mathrm{n} ] ]
$$

where:

output-filespec is the file specification for the output file. If you do not specify an output file, PAT does not generate one.

input-filespec is the file specification for the input file. This file can contain one or more concatenated object modules.

correct-filespec is the file specification for the correction file. This file contains the updates being made to a single module in the input file.

/C specifies the checksum option for the associated file. This directs PAT to generate an octal value for the sum of all the binary data composing the module in that file. (See Section 21.5 for more information on checksums.)

3. Execute PAT using as input the correction file and the module to be updated.

specifies an octal value. PAT compares the checksum value it computes for a module with the octal value you specify.

Figure 21-2: Processing Steps Required to Update a Module Using PAT

[figure omitted]

## 21.3 How PAT Effects Updates

PAT updates a base input module by using additions and corrections you supply in a correction file. This section describes the PAT input and correction files, and gives information on how to create the correction file.

## 21.3.1 Input File

The input file is the file to be updated; it is the base for the output file and must be in object module format. When PAT executes, the module in the correction file applies to this file.

## 21.3.2 Correction File

The correction file must be in object module format and it is usually created from a MACRO-11 source file in the following format:

<table><tr><td colspan="2">.TITLE inputname</td></tr><tr><td colspan="2">[.IDENT updatenum]</td></tr><tr><td colspan="2">[section name]</td></tr><tr><td colspan="2">inputline</td></tr><tr><td colspan="2">inputline</td></tr><tr><td colspan="2">*</td></tr><tr><td colspan="2">*</td></tr><tr><td colspan="2">*</td></tr><tr><td colspan="2">where:</td></tr><tr><td>inputname</td><td>is the name of the module to be corrected by the PAT update. That is, inputname must be the same name as the name on the input file .TITLE directive for a single module in the input file.</td></tr><tr><td>updatenum</td><td>is any value acceptable to the MACRO-11 assembler. Generally, this value reflects the update version of the file being processed by PAT, as shown in the examples below.</td></tr><tr><td>section name</td><td>is the ASECT, CSECT, or PSECT included in the correction file.</td></tr><tr><td>inputline</td><td>are lines of input for PAT&#x27;s use in correcting and updating the input file.</td></tr></table>

A duplicate PSECT or CSECT supersedes the previous PSECT or CSECT, provided:

\- Both have the same relocatability attribute (ABS or REL).

\- Both are defined with the same directive (.PSECT or .CSECT).

If PAT encounters duplicate PSECT names, it sets the length attribute for the PSECT to the length of the longer PSECT and appends a new PSECT to the module.

If you specify a transfer address, it supersedes that of the module you are patching.

## 21.4 Updating Object Modules

The following examples show the source code for an input file and a correction file to be processed by PAT and the linker. The examples show as output a single source file that, if assembled and linked, would produce a binary module equivalent to the file generated by PAT and LINK. Two techniques are described: one is for overlaying lines in a module, and the other is for appending a subroutine to a module.

## 21.4.1 Overlaying Lines in a Module

In the following example, PAT first appends the correction file to the input file. The linker is then executed to replace code within the input file.

The input file for this example is:

```csv
,TITLE ABC
,IDENT /01/
,ENABL GBL
ABC::
MOV A,C
JSR PC,XYZ
RTS PC
,END
```

To add the instruction ADD A,B after the JSR instruction, the following patch source file is included:

```csv
,TITLE ABC
,IDENT /01,01/
,ENABL GBL
, = , + 12
ADD A,B
RTS PC
,END
```

The patch source is assembled using MACRO-11 and the resulting object file is input to PAT along with the original object file. The following source code represents the result of PAT processing:

```csv
,TITLE ABC
,IDENT /01,01/
,ENABL GBL
ABC:::
MOV A,C
JSR PC,XYZ
RTS PC
:=ABC
:=,+12
ADD A,B
RTS PC
.END
```

After the linker processes these files, the load image appears, as this source code representation shows:

```csv
,TITLE ABC
,IDENT /01,01/
,ENABL GBL
ABC::
MOV A,C
JSR PC,XYZ
ADD A,B
RTS PC
.END
```

The linker uses the . = . + 12 in the program counter field to determine where to begin overlaying instructions in the program and, finally, overlays the RTS instruction with the patch code:

```txt
ADD A,B RTS PC
```

## 21.4.2 Adding a Subroutine to a Module

In many cases, a patch requires that more than a few lines be added to patch the file. A convenient technique for adding new code is to append it to the end of the module in the form of a subroutine. This way, you can insert a JSR instruction to the subroutine at an appropriate location. The JSR directs the program to branch to the new code, execute that code, and then return to in-line processing.

The source code for the input file for the example is:

```csv
,TITLE ABC
,IDENT /01/
,ENABL GBL
ABC:::
MOV A,B
JSR PC,XYZ
MOV C,RO
RTS PC
.END
```

```txt
MOV     D,RO
ASL     RO

between

MOV     A,B

and

JSR     PC,XYZ
```

Suppose you wish to add the instructions:

The correction file to accomplish this is as follows:

```asm
.TITLE ABC
    .IDENT /01,01/
    .ENABL GBL
JSR PC,PATCH
NOP
.PSECT PATCH
PATCH:
MOV A,B
MOV D,RO
ASL RO
RTS PC
.END
```

PAT appends the correction file to the input file, and the linker then processes the file, generating the following output file:

```csv
,TITLE ABC
,IDENT /01,01/
,ENABL GBL
ABC::JSR PC,PATCH
NOP
JSR PC,XYZ
MOV C,RO
RTS PC
.PSECT PATCH
PATCH:
MOV A,B
MOV D,RO
ASL RO
RTS PC
.END
```

In this example, the JSR PC,PATCH and NOP instructions overlay the three-word MOV A,B instruction. (The NOP is included because this is a case where a two-word instruction replaces a three-word instruction. NOP is required to maintain alignment.) The linker allocates additional storage for .PSECT PATCH, writes the specified code into this program section, and binds the JSR instruction to the first address in this section. Note that the MOV A,B instruction, replaced by the JSR PC,PATCH, is the first instruction the PATCH subroutine executes.

## 21.5 Determining and Validating the Contents of a File

Use the checksum option (/C) to determine or validate the contents of a module. The checksum option directs PAT to compute the sum of all binary data composing a file. If you specify the command in the form /C:n, /C directs PAT to compute the checksum and compare that checksum to the value you specify as n.

To determine the checksum of a file, enter the PAT command line with the /C option applied to the appropriate file (the file whose checksum you want to determine). For example, PAT responds to the command

= INFILE/C, INFILE.PAT

with the message

```txt
?PAT-W-Input module checksum is nnnnnn
```

PAT generates a similar message when you request the checksum for the correction file.

To validate the changes made to a file, enter the checksum option in the form /C:n. PAT compares the value it computes for the checksum with the value you specify as n. If the two values do not match, PAT enters the changes but displays a message reporting the checksum error as either:

?PAT-W-Input file checksum error

or

?PAT-W-Correction file checksum error

Checksum processing always results in a nonzero value.

Do not confuse this checksum with the record checksum byte.
