# RT-11 System Utilities Manual: Ch.11 LINK linker: options, .SAV/.REL/.LDA/.SYS outputs, maps, overlays, extended memory, library search

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 11.1 Overview of the Linking Process
- 11.1.1 What the Linker Does
- 11.1.2 How the Linker Structures the Load Module
- 11.1.3 Global Symbols: Communication Links Between Modules
- 11.2 Calling and Terminating the Linker
- 11.3 Link Command String Syntax
- 11.4 Input and Output
- 11.4.1 Input Object Modules
- 11.4.2 Input Library Modules
- 11.4.3 Output Load Module
- 11.4.4 Output Load Map
- 11.5 Creating an Overlay Structure
- 11.5.1 Low Memory Overlays
- 11.5.2 Extended Memory Overlays
- 11.5.3 Combining Low Memory Overlays with Extended Memory Overlays
- 11.5.4 Load Map
- 11.6 Options
- 11.6.1 Alphabetical Option (/A)
- 11.6.2 Bottom Address Option (/B:n)
- 11.6.3 Continuation Option (/C or //)
- 11.6.4 Duplicate Global Symbol Option (/D)
- 11.6.5 Extend Program Section Option (/E:n)
- 11.6.6 Default FORTRAN Library Option (/F)
- 11.6.7 Directory Buffer Size Option (/G)
- 11.6.8 Highest Address Option (/H:n)
- 11.6.9 Include Option (/I)
- 11.6.10 Memory Size Option (/K:n)
- 11.6.11 LDA Format Option (/L)
- 11.6.12 Modify Stack Address Option (/M[:n])
- 11.6.13 Cross-Reference Option (/N)
- 11.6.14 Low Memory Overlay Option (/O:n)
- 11.6.15 Library List Size Option (/P:n)
- 11.6.16 Absolute Base Address Option (/Q)
- 11.6.17 REL Format Option (/R[:n])
- 11.6.18 Symbol Table Option (/S)
- 11.6.19 Transfer Address Option (/T[:n])
- 11.6.20 Round Up Option (/U:n)
- 11.6.21 Extended Memory Overlay Option (/V:n[:m])
- 11.6.22 Map Width Option (/W)
- 11.6.23 Bitmap Inhibit Option (/X)
- 11.6.24 Boundary Option (/Y:n)
- 11.6.25 Zero Option (/Z:n)
- 11.7 Linker Prompts

---

## Chapter 11 Linker (LINK)

The linker (LINK) converts object modules to a format suitable for loading and execution. If you have no previous experience with the linker, see the Introduction to RT-11 for an introductory-level description of the linking process.

To make this chapter easy to use, the description that follows outlines the organization of this chapter.

Section 11.1, Overview of the Linking Process, explains:

\- Some of the terms used exclusively in this chapter

• The functions of the linker

\- How the linker structures your program to prepare it for execution

\- The communication links between modules within your program

Section 11.2, Calling and Terminating the Linker, describes how to invoke the linker from the system device and how to terminate the linker.

Section 11.3, LINK Command String Syntax, describes how to enter a LINK command string. This section also provides a summary of the options you can use in the command string.

Section 11.4, Input and Output, lists and describes the files valid for input to and output from the linker. This section also explains how to use library files, and how the linker processes library files, which you create with the librarian utility (see Chapter 10).

Section 11.5, Creating an Overlay Structure, describes how to design and implement overlay structures for your programs. This section provides detailed descriptions and illustrations of how overlaid programs work and how they reside in memory. This section also explains how to create an overlay structure in extended memory.

Section 11.6, Options, lists and describes the options you can use with the linker.

Section 11.7, Linker Prompts, lists and explains the prompts the linker prints at the terminal after you enter a command line.

## 11.1 Overview of the Linking Process

A few of the terms used frequently within this chapter, along with their definitions, are listed below. Although the descriptions are brief, you can find more information on these terms in the Introduction to RT-11 or the RT-11 Software Support Manual.

Program section A named, contiguous unit of code (instructions or data) that is considered an entity and that can be relocated separately without destroying the logic of the program. Also known as a p-sect.

Object module The primary output of an assembler or compiler, which can be linked with other modules and loaded into memory as a runnable program. The object module is composed of the relocatable machine language code, relocation information, and the corresponding global symbol table defining the use of the symbols within the program. Also known as a module.

Load module A program in a format ready for loading and executing.

Library file A file containing one or more relocatable object modules, which are routines that can be incorporated into other programs.

Library module A module from a library file.

Root segment The segment of an overlay-structure that, when loaded, remains resident in memory during the execution of a program. Also known as the root.

Overlay segment A section of code treated as a unit that can overlay code already in memory and be overlaid by other overlay segments when called from the root segment or another overlay segment. Also known as an overlay.

Global symbol A global value or global label.

Low memory Physical memory from 0 to 28K words.

Extended memory Physical memory above the 28K word boundary.

## 11.1.1 What the Linker Does

When the linker processes the object modules, it performs the functions listed below.

\- Relocates your program module and assigns absolute addresses

\- Links the modules by correlating global symbols that are defined in one module and referenced in another

\- Creates the initial control block for the linked program that the GET, R, RUN, SRUN, and FRUN commands use

\- Creates an overlay structure, if specified, and includes the necessary runtime overlay handlers and tables

\- Searches the library files you specify to locate unresolved global symbols

\- Produces a load map, if specified, that shows the layout of the load module

\- Produces a symbol table definition file, if specified

The linker requires two passes over the input modules. During the first pass it constructs the symbol table, which includes all program section names and global symbols in the input modules. Next, the linker scans the library files to resolve undefined global symbols. It links only those modules that are required to resolve undefined global symbols. During the second pass, the linker reads in object modules, performs most of the functions listed above, and produces the load module.

The linker runs in a minimal RT-11 system of 16K words of memory; any additional memory is used to facilitate linking and to extend the size of the symbol table. The linker accepts input from any random-access volume on the system; there must be at least one random-access volume (disk, diskette, or DECtape II) for memory image or relocatable format output.

## 11.1.2 How the Linker Structures the Load Module

When the linker processes the assembled or compiled object modules, it creates a load module in which it has assigned all absolute addresses, has created an absolute section, and has allocated memory for the program sections.

11.1.2.1 Absolute Section — The absolute section is often called the APECT because the assembler directive .ASECT allows information to be stored there. The absolute section appears in the load map with the name . ABS., and is always the first section in the listing. The absolute section typically ends at address 1000 (octal) and contains the following:

\- A system communication area

\- Hardware vectors

\- A user stack

The system communication area resides in locations 0–377, and contains data the linker uses to pass program control parameters and a memory usage bitmap. Section 11.4.3 provides a detailed description of each location in the system communication area.

The stack is an area that a program can use for temporary storage and subroutine linkage. General register 6, the stack pointer (SP), references the stack.

11.1.2.2 Program Sections — The program sections (p-sects) follow the absolute section. The set of attributes associated with each p-sect controls the allocation and placement of the section within the load module. The p-sect, as the basic unit of memory for a program, has:

\- A name by which it can be referenced

\- A set of attributes that define its contents, mode of access, allocation, and placement in memory

A length that determines how much storage is reserved for the p-sect

You create p-sects by using a COMMON statement in FORTRAN, or the .PSECT (or .CSECT) directive in MACRO. You can use the .PSECT (or .CSECT) directive to attach attributes to the section. Note that the attributes that follow the p-sect name in the load map are not part of the name; only the name itself distinguishes one p-sect from another. You should make sure, then, that p-sects of the same name that you want to link together also have the same attribute list. If the linker encounters p-sects with the same name that have different attributes, it prints a warning message and uses the attributes from the first time it encountered the p-sect.

## Program Section Attributes

The linker collects from the input modules scattered references to a p-sect and combines them in a single area of the load module. The attributes, which are listed in Table 11–1, control the way the linker collects and places this unit of storage.

The scope-code is meaningful only when you define an overlay structure for the program. In an overlaid program, a global section is known throughout the entire program. Object modules contribute to only one global section of the same name. If two or more segments contribute to a global section, then the linker allocates that global section to the root segment of the program. In contrast to global sections, local sections are only known within a particular program segment. Because of this, several local sections of the same name can appear in different segments. Thus, several object modules contributing to a local section do so only within each segment. An example of a global section is named COMMON in FORTRAN. An example of a local section is the default blank section for each macro routine.

The alloc-code determines the starting address and length of memory allocated by modules that reference a common p-sect. If the alloc-code indicates that such a p-sect is to be overlaid, the linker stores the allocations from each module starting at the same location in memory. It determines the total size from the length of the longest reference to the p-sect. Each module's allocation of memory to a location overwrites that of a previous module. If the alloc-code indicates that a p-sect is to be concatenated, the linker places the allocations from the modules one after the other in the load module; it determines the total allocation from the sum of the lengths of the contributions.

Table 11-1: P-Sect Attributes

<table><tr><td>Attribute</td><td>Value</td><td>Explanation</td></tr><tr><td rowspan="2">Access-code*</td><td>RW</td><td>Read/Write – data can be read from, and written into, the p-sect.</td></tr><tr><td>RO</td><td>Read Only – data can be read from, but cannot be written into, the p-sect.</td></tr><tr><td rowspan="2">Type-code</td><td>D</td><td>Data – the p-sect contains data, concatenated by byte.</td></tr><tr><td>I</td><td>Instruction – the p-sect contains either instructions, or data and instructions, concatenated by word.</td></tr><tr><td rowspan="3">Scope-code</td><td>GBL</td><td>Global – the p-sect name is recognized across segment boundaries. The linker allocates storage in the root for the p-sect from references outside the defining overlay segment. If the p-sect is referenced only in one segment, that p-sect has space allocated in that segment only.</td></tr><tr><td>LCL</td><td>Local – the p-sect name is recognized only within each individual segment. The linker allocates storage for the p-sect from references within the segment only.</td></tr><tr><td>SAV</td><td>Save – the p-sect name is recognized across segment boundaries. The linker always allocates storage in the root for the p-sect.</td></tr><tr><td rowspan="2">Reloc-code</td><td>REL</td><td>Relocatable – the base address of the p-sect is relocated relative to the virtual base address of the program.</td></tr><tr><td>ABS</td><td>Absolute – the base address of the p-sect is not relocated. It is always 0.</td></tr><tr><td rowspan="2">Alloc-code</td><td>CON</td><td>Concatenate – all allocations to a given p-sect name are concatenated. The total allocation is the sum of the individual allocations.</td></tr><tr><td>OVR</td><td>Overlay – all allocations to a given p-sect name overlay each other. The total allocation is the length of the longest individual allocation.</td></tr></table>

\* Not supported

Any data (D) p-sect that contains references to word labels must start on a word boundary. You can do this by using the .EVEN assembler directive at the end of each module's concatenated p-sect. (If you do not do this, the program may fail to link, printing the message ?LINK-F-Word relocation error in FILNAM.)

The allocation of memory for a p-sect always begins on a word boundary. If the p-sect has the D (data) and CON (concatenate) attributes, all storage that subsequent modules contribute is appended to the last byte of the previous allocation. This occurs whether or not that byte is on a word boundary. For a p-sect with the I (instruction) and CON attributes, however, all storage that subsequent modules contribute begins at the nearest following word boundary.

The .CSECT directive of MACRO is converted internally by both MACRO and the linker to an equivalent .PSECT with fixed attributes. An unnamed CSECT (blank section) is the same as a blank PSECT with the attributes RW, I, LCL, REL, and CON.

A named CSECT is equivalent to a named PSECT with the attributes RW, I, GBL, REL, and OVR. Table 11–2 shows these sections and their attributes.

Table 11-2: Section Attributes

| Section | Access-Code | Type-Code | Scope-Code | Reloc-Code | Alloc-Code |
| --- | --- | --- | --- | --- | --- |
| CSECT | RW | I | LCL | REL | CON |
| CSECT name | RW | I | GBL | REL | OVR |
| ASECT (. ABS.) | RW | I | GBL | ABS | OVR |
| COMMON/name/ | RW | D | GBL | REL | OVR |
| VSECT (. VIR.) | RW | D | GBL | REL | CON |

The names assigned to p-sects are not considered to be global symbols; you cannot reference them as such. For example:

MOV #PNAME,RO

This statement, where PNAME is the name of a section, is invalid and generates the undefined global error message if no global symbol of PNAME exists. A name can be the same for both a p-sect name and a global symbol. The linker treats them separately.

## Program Section Order

The linker determines the memory allocation of p-sects by the order of occurrence of the p-sects in the input modules. Table 11–3 shows the order in which p-sects appear for both overlaid and nonoverlaid files.

Table 11-3: P-Sect Order

| Nonoverlaid File | Overlaid File |
| --- | --- |
| Absolute (.ABS) | Absolute (.ABS) |
| Blank | Overlay handler ($OHAND) |
| Named (NAME) | Overlay table ($OTABL) |
|  | Blank |
|  | Named (NAME) |

If there is more than one named section, the named sections appear in the order in which they occur in the input files. For example, the FORTRAN compiler arranges the p-sects in the main program module so that the USR can swap over pure code in low memory rather than over data required by the function making the USR call.

If the size of the blank p-sect is 0, it does not appear in the load map.

## 11.1.3 Global Symbols: Communication Links Between Modules

Global symbols provide the link, or communication, between object modules. You create global symbols with the .GLOBL or .ENABL GBL assembler directive (or with double colon, :, double equal sign, == , or == :).

If the global symbol is defined in an object module (as a label using :: or by direct assignment using ==), other object modules can reference it. If the global symbol is not defined in the object module, it is an external symbol and is assumed to be defined in some other object module. If a global symbol is used as a label in a routine, it is often called an entry point — that is, it is an entry point to that subroutine.

As the linker reads the object modules it keeps track of all global symbol definitions and references. It then modifies the instructions and data that reference the global symbols. The linker always prints undefined globals on the console terminal after pass 1. A list of undefined globals is also included in any load maps you generate.

Table 11-4 shows how the linker resolves global references when it creates the load module.

Table 11-4: Global Reference Resolution

<table><tr><td>Module Name</td><td>Global Definition</td><td>Global Reference</td></tr><tr><td rowspan="4">IN1</td><td>B1</td><td>A</td></tr><tr><td>B2</td><td>L1</td></tr><tr><td></td><td>C1</td></tr><tr><td></td><td>XXX</td></tr><tr><td rowspan="2">IN2</td><td>A</td><td>B2</td></tr><tr><td>B1</td><td></td></tr><tr><td>IN3</td><td></td><td>B1</td></tr></table>

In processing the first module, IN1, the linker finds definitions for B1 and B2, and references to A, L1, C1, and XXX. Because no definition currently exists for these references, the linker defers the resolution of these global symbols. In processing the next module, IN2, the linker finds a definition for A that resolves the previous reference, and a reference to B2 that can be immediately resolved.

When all the object modules have been processed, the linker has three unresolved global references remaining: L1, C1, and XXX. A search of the default system library resolves XXX. The global symbols L1 and C1 remain unresolved and are, therefore, listed as undefined global symbols.

The relocatable global symbol, B1, is defined twice and is listed on the terminal as a global symbol with multiple definitions. The linker uses the first definition of such a symbol. An absolute global symbol can be defined more than once without being listed as having multiple definitions, as long as each occurrence of the symbol has the same value.

## 11.2 Calling and Terminating the Linker

To call the linker from the system device, respond to the dot printed by the keyboard monitor by typing:

```txt
. R LINK RET
```

The Command String Interpreter (CSI) prints an asterisk at the left margin of the console terminal when it is ready to accept a command line. If you enter only a carriage return at this point, the linker prints its current version number.

Type two CTRL/Cs to halt the linker at any time (or a single CTRL/C to halt the linker when it is waiting for console terminal input) and return control to the monitor. To restart the linker, type R LINK or REENTER in response to the monitor's dot.

## 11.3 Link Command String Syntax

The first command string you enter in response to the linker's prompt has this syntax:

[bin-filespec],[map-filespec],[stb-filespec] = obj-filespec[/option...][,...obj-filespec[/option...]]

where:

bin-filespec represents the device, file name, and file type to be assigned to the linker's output load module file

map-filespec represents the device, file name, and file type of the load map output file

stb-filespec represents the device, file name, and file type of the symbol definition file

obj-filespec represents an object module, a library file, or a symbol table file, created in a previous link

/option is one of the options listed in Table 11-6

In each file specification above, the device should be a random-access device, with these exceptions: the output device for the load map file can be any RT-11 device, as can the output device for an .LDA file if you use the /L option. If you do not specify a device, the linker uses default device DK:. Note that the linker load map contains lowercase characters. Use the SET LP LC command to enable lowercase printing if your printer has lowercase characters.

If you do not specify an output file, the linker assumes that you do not want the associated output. For example, if you do not specify the load module and load map (by using a comma in place of each file specification) the linker prints only error messages, if any occur.

Table 11-5 shows the default values for each specification.

Table 11-5: Linker Defaults

<table><tr><td></td><td>Device</td><td>File Name</td><td>File Type</td></tr><tr><td>Load Module</td><td>DK:</td><td>None</td><td>SAV, REL(/R), LDA(/L)</td></tr><tr><td>Load Map</td><td>DK: or same as load module</td><td>None</td><td>MAP</td></tr><tr><td>Symbol</td><td rowspan="3">DK: or same as previous output device</td><td rowspan="3">None</td><td rowspan="3">STB</td></tr><tr><td>Definition</td></tr><tr><td>Output</td></tr><tr><td>Object Module</td><td>DK: or same as previous object module</td><td>None</td><td>OBJ</td></tr></table>

If you make a syntax error in a command string, the system prints an error message. You can then retype the new command string following the asterisk. Similarly, if you specify a nonexistent file, a warning message occurs; control returns to the CSI, an asterisk prints, and you can reenter the command string.

Table 11–6 lists the options associated with the linker. You must precede the letter representing each option with the slash character. Options must appear on the line indicated if you continue the input on more than one line, but you can position them anywhere on the line. The column titled Command Line lists on which line in the command string the option can appear. (Section 11.6 provides a more detailed explanation of each option.)

Table 11-6: Linker Options

| Option Name | Command Line | Section | Explanation |
| --- | --- | --- | --- |
| /A | First | 11.6.1 | Lists global symbols in program sections in alphabetical order. |
| /B:n | First | 11.6.2 | Changes the bottom address of a program to n (invalid with /H and /R). |
| /C | Any but last | 11.6.3 | Continues input specification on another command line. (You can also use /C with /V and with /O; do not use /C with the // option.) |
| /D | First | 11.6.4 | Allows the global symbol you specify to be defined once in each segment that references that symbol. These symbols must be defined in library modules. |
| /E:n | First | 11.6.5 | Extends a particular program section in the root to a specific value. |
| /F | First | 11.6.6 | Instructs the linker to use the default FORTRAN library, FORLIB.OBJ; this option is provided only for compatibility with previous versions of RT-11. |
| /G | First | 11.6.7 | Adjusts the size of the linker's library directory buffer to accommodate the largest multiple definition library directory. |
| /H:n | First | 11.6.8 | Specifies the top (highest) address to be used by the relocatable code in the load module. Invalid with /B, /R, /Y and /Q. |
| /I | First | 11.6.9 | Extracts the global symbols you specify (and their associated object modules) from the library and links them into the load module. |
| /K:n | First | 11.6.10 | Inserts the value you specify (the valid range for n is from 2 to 28.) into word 56 of block 0 of the image file. This option allows you to limit the amount of memory allocated by a .SETTOP request to n K words (decimal). Invalid with /R. |
| /L | First | 11.6.11 | Produces a formatted binary output file (invalid for overlaid programs and for foreground links). |
| /M[:n] | First | 11.6.12 | Causes the linker to prompt you for a global symbol that represents the stack address or that sets the stack address to the value n. Do not use with /R. |
| /N | First | 11.6.13 | Produces a cross-reference in the load map of all global symbols defined during the linking process. |
| /O:n | Any but first | 11.6.14 | Indicates that the program is an overlay structure; n specifies the overlay region to which the module is assigned. Invalid with /L. |
| /P:n | First | 11.6.15 | Changes the default amount of space the linker uses for a library routines list. |
| /Q | First | 11.6.16 | Lets you specify the base addresses of up to eight root program sections. Invalid with /H or /R. |
| /R[:n] | First | 11.6.17 | Produces output in relocatable format and optionally indicates stack size for a foreground job. Invalid with /B, /H, /K, and /L. |
| /S | First | 11.6.18 | Makes the maximum amount of space in memory available for the linker's symbol table. (Use this option only when a particular link stream causes a symbol table overflow.) |
| /T[:n] | First | 11.6.19 | Cause the linker to prompt you for a global symbol that represents the transfer address or that sets the transfer address to the value n. |
| /U:n | First | 11.6.20 | Rounds up the root program section you specify so that the size of the root segment is a whole number multiple of the value you supply (n must be a power of 2). |
| /V | First | 11.6.21 | Enables special .SETTOP and .LIMIT features provided by the XM monitor. Invalid with /L. |
| /V:n[:m] | Any but first | 11.6.21 | Indicates that an extended memory overlay segment is to be mapped in virtual region n, and optionally in partition m. |
| /W | First | 11.6.22 | Directs the linker to produce a wide load map listing. |
| /X | First | 11.6.23 | Does not output the bitmap if the code is placed over the bitmap (location 360-377). This option is provided only for compatibility with the RSTS operating system. |
| /Y:n | First | 11.6.24 | Starts a specific program section in the root on a particular address boundary. Invalid with /H. |
| /Z:n | First | 11.6.25 | Sets unused locations in the load module to the value n. |
| // | First and last | 11.6.3 | Allows you to specify command string input on additional lines. Do not use this option with /C. |

## 11.4 Input and Output

Linker input and output is in the form of modules; the linker uses one or more input modules to produce a single output (load) module. The linker also accepts library modules and symbol table definition files as input, and can produce a load map and/or symbol table definition file. The sections that follow describe all valid forms of input to and output from the linker.

## 11.4.1 Input Object Modules

Object files, consisting of one or more object modules, are the input to the linker. (Entering files that are not object modules may result in a fatal error.) Object modules are created by language translators such as the FORTRAN compiler and the MACRO-11 assembler. The module name item declares the name of the object module (see Section 11.4.4).

The first six Radix—50 characters of the .TITLE assembler directive are used as the name of the object module. These six characters must be Radix—50 characters (the linker ignores any characters beyond the sixth character). The linker prints the first module name it encounters in the input file stream (normally the main routine of the program) on the second line of the map following TITLE:. The linker also uses the first identity label (issued by the .IDENT directive) for the load map. It ignores additional module names.

The linker reads each object module twice. During the first pass it reads each object module to construct a global symbol table and to assign absolute values to the program section names and global symbols. The linker uses the library files to resolve undefined globals. It places their associated object modules in the root if the global symbols in the module are referenced from more than one overlay segment or from the root. If you use the /D option and the global symbols are not referenced from the root, the linker places a copy of the global symbols you specify in each segment that references them. (See Section 11.6.4 for more information on the /D option.) On the second of its two passes, the linker reads the object modules, links and relocates the modules, and outputs the load module.

Symbol table definition files are special object files that can serve as input to LINK anywhere other object files are allowed.

## 11.4.2 Input Library Modules

The RT-11 linker can automatically search libraries. Libraries consist of library files, which are specially formatted files produced by the librarian program (described in Chapter 10) that contain one or more object modules. The object modules provide routines and functions to aid you in meeting specific programming needs. (For example, FORTRAN has a set of modules containing all necessary computational functions — SQRT, SIN, COS, and so on.) You can use the librarian to create and update libraries. Then you can easily access routines that you use repeatedly or routines that different programs use. Selected modules from the appropriate library file are linked as needed with your program to produce one load module. Libraries are further described in Chapter 10.

## NOTE

Library files that you combine with the monitor COPY command or with the PIP /U or /B option (described in Chapter 13) are invalid as input to both the linker and the librarian.

You specify libraries in a command string in the same way you specify normal modules; you can include them anywhere in the command string. If you are creating an overlay structure, specify libraries before you specify the overlay structure. Do not specify libraries on the same line as overlay segments. If a global symbol is undefined at the time the linker encounters the library in the input stream, and if a module is included in the library that contains that global definition, then the linker pulls that module from the library and links it into the load image. Only the modules needed to resolve references are pulled from the library; unreferenced modules are not linked.

Modules in one library can call modules from another library; however, the libraries must appear in the command string in the order in which they are called. For example, assume module X in library ALIB calls Y from the BLIB library. To correctly resolve all globals, the order of ALIB and BLIB should appear in the command line as:

\* Z = B, ALIB, BLIB

Module B is the root. It calls X from ALIB and brings X into the root. X in turn calls Y, which is brought from BLIB into the root.

## Library Module Processing

The linker selectively relocates and links object modules from specific user libraries that were built by the librarian. Figure 11–1 diagrams this general process. During pass 1 the linker processes the input files in the order in which they appear in the input command line. If the linker encounters a library file during pass 1, it takes note of the library in an internal save status block, and then proceeds to the next file. The linker processes only nonlibrary files during the initial phase of pass 1. In the final phase of pass 1 the linker processes only library files. This is when it resolves the undefined globals that were referenced by the nonlibrary files.

The linker processes library files in the order in which they appear in the input command line. The default system library (SY:SYSLIB.OBJ) is always processed last.

Figure 11-1: Library Searches

[figure omitted]

The search method the linker uses allows modules to appear in any order in the library. You can specify any number of libraries in a link and they can be positioned anywhere, with the exception of forward references between libraries, and they must come before the overlay structure. The default system library, SY:SYSLIB.OBJ, is the last library file the linker searches to resolve any remaining undefined globals.

Some languages, such as FORTRAN, have an Object Time System (OTS) that the linker takes from a library and includes in the final module. The most efficient way to accomplish this is to include these OTS routines (such as NHD, OTSCOM, and V2NS for FORTRAN) in SY:SYSLIB.OBJ. See the RT-11 Installation Guide for details on how to do this.

Libraries are input to the linker the same way as other input files. Here is a sample LINK command string:

\* TASKO1,LP:=MAIN,MEASUR

This causes program MAIN.OBJ to be read from DK: as the first input file. Any undefined symbols generated by program MAIN.OBJ should be satisfied by the library file MEASUR.OBJ specified in the second input file. The linker tries to satisfy any remaining undefined globals from the default library, SY:SYSLIB.OBJ. The load module, TASK01.SAV, is stored on DK: and a load map prints on the line printer.

## Multiple Definition Libraries

In addition to the libraries explained so far, LINK processes multiple definition libraries. DIGITAL does not recommend that you use this type of library in normal situations; its primary purpose is to provide special functions for RSTS. These libraries differ from other libraries in that they can contain more than one definition for a given global. You specify multiple definition libraries in the command line the same way you specify normal libraries. Modules that LINK obtains from multiple definition libraries always appear in the root.

It is useful to be aware of the differences between processing normal and multiple definition libraries. When you include modules from a multiple definition library, LINK has to store that library's directory in an internal buffer. A library's directory is often called an entry point table (EPT). If a library EPT is too large to fit into the internal buffer, LINK prints a message instructing you to use the /G option. The /G option changes the buffer's size to accommodate the largest EPT of all the multiple definition libraries you are using. Use the /G option only when LINK indicates it is required.

When a global symbol from a multiple definition library matches an undefined global, LINK removes from the undefined global list all other globals defined in the same library. LINK does this before it processes the library module. Thus, two modules with identical globals will not appear in the linked module.

## NOTE

The order of modules in multiple definition libraries is very important and will affect which modules LINK uses. The increased EPT size (due to duplicate entries, in addition to module name entries) will also slow LINK down.

## 11.4.3 Output Load Module

The primary output of the linker is a load module that you can run under RT-11. The linker creates as a load module a memory image file (file type of .SAV) for use under a single-job system or as the background job under the FB monitor; save images can also be run as virtual foreground jobs under the XM monitor. If you need to execute a program in the foreground, use the /R option to produce a relocatable format (file type of .REL) foreground load module. The linker can produce an absolute load module (file type of .LDA) if you need to load the module with the Absolute Loader. See the RT-11 Software Support Manual for more details on these formats.

The load module for a memory image file is arranged as follows:

| Root Segment | Overlay Segments (optional) |
| --- | --- |

For a relocatable image file the load modules are arranged as follows:

| Root Segment | Overlay Segments (optional) | Relocation information for root and overlay segments |
| --- | --- | --- |

The first 256-word block of the root segment (main program) contains the memory usage bitmap and the locations the linker uses to pass program control parameters. The memory usage bitmap outlines the blocks of memory that the load module uses; it is located in locations 360 through 377.

Table 11-7 lists the parameters that appear in the absolute block, the addresses the parameters occupy, and the conditions under which they are set.

The linker stores default values in locations 40, 42, and 50, unless you use options to specify otherwise. The /T option affects location 40, for example, and /M affects location 42. You can also use the .ASECT directive to change the defaults. The overlay bit is located in the job status word. LINK automatically sets this bit if the program is overlaid. Otherwise, the linker initially sets location 44 to 0. Location 46 also contains zero unless you specify another value by using the .ASECT directive.

You can assign initial values to memory locations 0–476 (which include the interrupt vectors and system communication area) by using an .ASECT assembler directive. The values appear in block 0 of the load module, but there are restrictions on the use of .ASECT directives in this region. You should not modify location 54 or locations 360–377 because the memory usage map is passed in those locations. In addition, for foreground links, modifications of words 52–62 are not permitted because additional parameters are passed to the FRUN command in those locations.

Table 11-7: Absolute Block Parameters

| Address | Parameter | When Set |
| --- | --- | --- |
| 0 | Identification of a program that was created with /V option | Only with /V |
| 2 | Highest virtual memory address used by the program | Only with /V |
| 14,16 | (XM only) BPT trap | Only with /R |
| 20,22 | (XM only) IOT trap | Only with /R |
| 34,36 | TRAP vector | Only with /R |
| 40 | Start address of program | Always |
| 42 | Initial setting of SP (stack pointer) | Always |
| 44 | Job Status Word (overlay bit set by LINK) | Always |
| 46 | USR swap (set by user) address; (0 implies normal location) | Always |
| 50 | Highest memory address used by the program (high limit) | Always |
| 52 | Size of root segment in bytes | Only with /R |
| 54 | Stack size in bytes (value with /R or default 128) | Only with /R |
| 56 | Size of overlay region in bytes | Only with /R |
| 60 | Identification of a file in relocatable (.REL) format | Only with /R |
| 62 | Relative block number for start of relocation information | Only with /R |
| 64 | Start address of overlay table | With /O or /V |
| 66 | Start of virtual overlay segment information in overlay handler tables | Only with /V |
| 360-377 | Memory usage bitmap | Always, except with /X or /L |

You can use an .ASECT directive to set any location that is not restricted, but be careful if you change the system communication area. The program itself must initialize restricted areas, such as locations 360–377. There are no restrictions on .ASECT directives if the output format is LDA.

Locations in addresses 0–476 might not be loaded at execution time, even though your program uses an .ASECT to initialize them. For background programs, this is because the R, RUN, and GET commands do not load addresses that are protected by the monitor's memory protection map. For foreground programs, the FRUN command loads only locations 14–22 and 34–50 and ignores all other low memory locations. To initialize a location at run time, use the .PROTECT programmed request. If it is successful, follow it with a MOV instruction to modify the location.

## 11.4.4 Output Load Map

The linker can produce a load map following the completion of the initial pass. This map, shown in Figure 11–2, diagrams the layout of memory for the load module.

The load map lists each program section that is included in the linking process. The line for a section includes the name and low address of the section and its size in bytes. The rest of the line lists the program section attributes, as shown in Table 11–2. The remaining columns contain the global symbols found in the section and their values.

Figure 11-2: Sample Load Map

```asm
RT-11 LINK V06.01 Load Map Friday 14-Jan-83 11:25 Page 1
TEST .SAV Title: TEST Ident:
Section Addr Size Global Value Global Value Global Value
, ABS, 000000 001000 = 256, words (RW,I,GBL,ABS,OVR)
001000 000200 = 64, words (RW,I,LCL,REL,CON)
TEST 001200 000174 = 62, words (RW,I,LCL,REL,CON)
START 001200 EXIT 001240
Transfer address = 001200, High limit = 001372 = 381, words
```

Table 11-8 describes each line in the sample load map above.

The map begins with the linker version number, followed by the date and time the program was linked. The second line lists the file name of the program, its title (which is determined by the first module name record in the input file), and the first identification record found. The absolute section is always shown first, followed by any nonrelocatable symbols. The modules located in the root segment of the load module are listed next, followed by those modules that were assigned to overlays in order by their region number (see Section 11.5). Any undefined global symbols are then listed. The map ends with the transfer address (start address) and high limit of relocatable code in both octal bytes and decimal words. If you use the /N option, a cross-reference of all global symbols defined during the linking process follows the transfer address line. See Figure 11–14 for a sample and description of a global cross-references table.

Table 11-8: Line-by-Line Sample Load Map Description

| Line | Contents |
| --- | --- |
| 1 | Load map header. |
| 2 | Program name, program title (.MAIN. default) and identity (default is blank). |
| 4 | P-sect description header. Section indicates the p-sect name; Addr indicates the p-sect start address; Size indicates p-sect length in octal bytes; Global and Value list the p-sect globals and their associated octal values. |
| 6 | Absolute p-sect, . ABS. This line includes the absolute p-sect's start address, length and attributes (for a complete description of these abbreviations, see Table 11-1). The linker always includes a . ABS. p-sect in the link. |
| 7 | Unnamed p-sect. This p-sect appears in the load map after the absolute p-sect. For overlaid programs, the unnamed p-sect appears in the load map after the overlay table p-sect (see Figure 11-11). |
| 8-9 | TEST p-sect. Line 9 lists TEST's two globals, START and EXIT, with their associated values. |
| 11 | Transfer address indicates the address in memory where the program starts. High limit indicates the last address used by the program. The number of words in the program appears last. |

## NOTE

The load map does not reflect the absolute addresses for a REL file that you create to run as a foreground job; you must add the base relocation address determined at FRUN time to obtain the absolute addresses. The linker assumes a base address of 1000.

For example, assume the FRUN command is used to run the program TEST:

• FRUN TEST/P

Loaded at 127276

The /P option causes FRUN to print the load address, which is 127276 in this example. To calculate the actual location in memory of any global in the program, first subtract 1000 from that global's value. (The value 1000 represents the base address assigned by the linker. This offset is not used at load time.) Then add the result to the load address determined with /P. The final result represents the absolute location of the global.

## 11.5 Creating an Overlay Structure

The ability of RT-11 to handle overlays gives you virtually unlimited memory space for an assembly language or FORTRAN program. A program using overlays can be much larger than would normally fit in the available memory space, since portions of the program reside on a storage device such as disk. To utilize this capability, you must define an overlay structure for your program.

Prior to Version 4, RT-11 permitted overlays to be placed only in low memory. Now you can place them in extended memory, too, if you run your program on a system that has an extended memory configuration and XM monitor. Overlays that reside in low memory are called low memory overlays, and those in extended memory are called extended memory overlays.

Section 11.5.1, Low Memory Overlays, describes low memory overlays in general and shows how to define a low memory overlay structure for your program. Section 11.5.2, Extended Memory Overlays, deals specifically with extended memory overlays, and shows how to define an overlay structure that has either extended memory overlays only or both extended memory and low memory overlays.

Read 11.5.1 before reading 11.5.2, because much of the information contained in the first section applies to the second section.

## 11.5.1 Low Memory Overlays

An overlay structure divides a program into segments. For each overlaid program there is one root segment and a number of overlay segments. Each overlay segment is assigned to a particular area of available memory called an overlay region. More than one overlay segment can be assigned to a given overlay region. However, each region of memory is occupied by one (and only one) of its assigned segments at a time. The other segments assigned to that region are stored on disk, diskette, or DECtape II. They are brought into memory when called, replacing (overlaying) the segment previously stored in that region. The root segment, on the other hand, contains those parts of the program that must always be memory resident. Therefore the root is never overlaid by another segment.

Figure 11–3 diagrams an overlay structure for a FORTRAN program. The main program is placed in the root segment and is never overlaid. The various MACRO subroutines and FORTRAN subprograms are placed in overlay segments. Each overlay segment is assigned to an overlay region and stored on DECtape until called into memory. For example, region 2 is shared by the MACRO subroutine A currently in memory and the MACRO subroutine B in segment 4. When a call is made to subroutine B, segment 4 is brought into region 2 of memory, overlaying or replacing segment 3.

The overlay file, shown on the DECtape in Figure 11–3, is created by the linker when you specify an overlay structure. The overlay file contains at all times a copy of the root segment and each overlay segment, including those overlay segments currently in memory.

Figure 11-3: Sample Overlay Structure for a FORTRAN Program

[figure omitted]

You specify an overlay structure to the linker by using the /O option (see Figure 11–4). To specify an overlay structure that uses extended memory, use the /V option (see Section 11.5.2 for a discussion of extended memory overlays). This option is described fully in Section 11.5.2.4.

## Figure 11-4: Overlay Scheme

Command line:

$$
\begin{array}{l} \text {A = A / /} \\ \text {B / O:1} \\ \text {C / O:1} \\ \text {D / O:2} \\ \text {E / O:2} \\ / / \end{array} \quad \left. \begin{array}{l} = \text {Root} \\ = \text {Segment 1} \\ = \text {Segment 2} \\ = \text {Segment 3} \\ = \text {Segment 4} \end{array} \right\} \quad \begin{array}{l} = \text {Region 1} \\ = \text {Region 2} \end{array} \quad \begin{array}{c c c c} \text {high} & & & \\ & D & E & \\ & B & C & \\ & & & \\ & & & A \\ & & & \text {low} \end{array} \quad \begin{array}{c c c c} & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \\ & & & \end{array}
$$

The linker calculates the size of any region to be the size of the largest segment assigned to that region. Thus, to reduce the size of a program (that is, the amount of memory it needs), you should first concentrate on reducing the size of the largest segment in each region. The linker delineates the overlay regions you specify, and prefaces your program with the run-time overlay handler code shown in Figure 11–5. The linker also sets up links between the overlay handler and program references to routines that reside in overlays. When, at run time, a reference is made to a section of your program that is not currently in memory, these links cause an overlay to be read into memory. The overlay segment containing the referenced code becomes resident.

There is no special formula for creating an overlay structure. You do not need a special code or function call. However, some general guidelines must be followed. For example, a FORTRAN main program must always be placed in the root segment. This is true also for a global program section (such as a named COMMON block) that is referenced by more than one overlay segment.

The assignment of region numbers to overlay segments is crucial. Segments that overlay each other (have the same region number) must be logically independent; that is, the components of one segment cannot reference the components of another segment assigned to the same region. Segments that need to be memory resident simultaneously must be assigned to different regions.

When you make calls to routines or subprograms that are in overlay segments, the entire return path must be in memory. This means that from an overlay segment you cannot call a routine that is in a different segment of the same region. If this is done, the called routine overlays the segment making the call, and destroys the return path.

## Figure 11-5: Run-Time Overlay Handler - Low Memory

```asm
;TITLE OHANDL LOW MEMORY OVERLAY HANDLER
;SBTTL THE RUN-TIME OVERLAY HANDLER
;ENABL GBL

;+
; THE FOLLOWING CODE IS INCLUDED IN THE USER'S PROGRAM BY THE
; LINKER WHENEVER LOW MEMORY OVERLAYS ARE REQUESTED BY THE USER,
; THE RUN-TIME LOW MEMORY OVERLAY HANDLER IS CALLED BY A DUMMY
; SUBROUTINE OF THE FOLLOWING FORM:
;
; JSR R5,$0VRH ;CALL TO COMMON CODE FOR LOW MEMORY OVERLAYS
; ,WORD <OVERLAY #*G> ;# OF DESIRED SEGMENT
; ,WORD <ENTRY ADDR> ;ACTUAL CORE ADDRESS (VIRTUAL ADDRESS)
;
; ONE DUMMY ROUTINE OF THE ABOVE FORM IS STORED IN THE RESIDENT PORTION
; OF THE USER'S PROGRAM FOR EACH ENTRY POINT TO A LOW MEMORY OVERLAY SEGMENT,
; ALL REFERENCES TO THE ENTRY POINT ARE MODIFIED BY THE LINKER TO BE
; REFERENCES TO THE APPROPRIATE DUMMY ROUTINE, EACH OVERLAY SEGMENT
; IS CALLED INTO CORE AS A UNIT AND MUST BE CONTIGUOUS IN CORE, AN
; OVERLAY SEGMENT MAY HAVE ANY NUMBER OF ENTRY POINTS, TO THE LIMITS
; OF CORE MEMORY, ONLY ONE SEGMENT AT A TIME MAY OCCUPY AN OVERLAY REGION.
;
; THERE IS ONE WORD PREFIXED TO EVERY OVERLAY REGION THAT IDENTIFIES THE
; SEGMENT CURRENTLY RESIDENT IN THAT OVERLAY REGION, THIS WORD IS AN INDEX
; INTO THE OVERLAY TABLE, AND POINTS AT THE OVERLAY SEGMENT INFORMATION.
;
; UNDEFINED GLOBALS IN THE OVERLAY HANDLER MUST BE NAMED "$0VDF1" TO
; "$0VDFn" SUCH THAT A RANGE CHECK MAY BE DONE BY LINK TO DETERMINE IF
; THE UNDEFINED GLOBAL NAME IS FROM THE OVERLAY HANDLER, A CHECK IS
; DONE ON THE .RAD50 CHARACTERS "$0V", AND THEN A RANGE CHECK IS DONE ON
; THE .RAD50 CHARACTERS "DF1" TO "DFn", THESE GLOBAL SYMBOLS DO NOT APPEAR
; ON LINK MAPS, SINCE THEIR VALUE IS NOT KNOWN UNTIL AFTER THE MAP HAS BEEN
; PRINTED, CURRENTLY $0VDF1 TO $0VDFS ARE IN USE.
;
; GLOBAL SYMBOLS O$READ AND O$DONE ARE USEFUL WHEN DEBUGGING OVERLAID
; PROGRAMS.
;
; O$READ:: WILL APPEAR IN THE LINK MAP AND LOCATES THE ,READW
; STATEMENT IN THE OVERLAY HANDLER.
;
; O$DONE:: WILL APPEAR IN THE LINK MAP AND LOCATES THE FIRST
; INSTRUCTION AFTER THE ,READW IN THE OVERLAY HANDLER.
;-
;MCALL .READW,,V1,..
; V1.. ;V1 FORMAT
;SBTTL OVERLAY HANDLER CODE
;PSECT $0HAND,GBL
;ENABL LSB
; $0VRH IS THE ENTRY POINT TO THE OVERLAY HANDLER
; RAD50 /0VR/ ;THIS KEEPS HANDLER THE SAME SIZE AS V03
$0VRH:: MOV R0,-(SP) ;/O OVERLAY ENTRY POINT
MOV R1,-(SP) ;SAVE REGISTERS
MOV R2,-(SP)
1$:
; BR 5$ ;FIRST CALL ONLY * * *
; MOV @R5,R1 ;PICK UP OVERLAY NUMBER
ADD #$0VTAB-6,R1 ;CALC TABLE ADDR
MOV (R1)+,R2 ;GET FIRST ARG, OF OVERLAY SEG, ENTRY
2$: CMP (R5)+,@R2 ;IS OVERLAY ALREADY RESIDENT?
BEQ 3$ ;YES, BRANCH TO IT
(Continued on next page)
```

```asm
;+
; THE .READW ARGUMENTS ARE AS FOLLOWS:
; CHANNEL NUMBER, CORE ADDRESS, LENGTH TO READ, RELATIVE BLOCK ON DISK.
; THESE ARE USED IN REVERSE ORDER FROM THAT SPECIFIED IN THE CALL.
;-

0$READ:: ,READW 17,R2,@R1,(R1)+ ;READ FROM OVERLAY FILE
0$DONE:: BCS 4$
3$: MOV (SP)+,R2 ;RESTORE USERS REGISTERS
MOV (SP)+,R1
MOV (SP)+,R0
MOV @R5,R5 ;GET ENTRY ADDRESS
RTS R5 ;ENTER OVERLAY ROUTINE AND RESTORE USER'S R5

4$: EMT 376 ;SYSTEM ERROR 10 (OVERLAY I/O)
.BYTE 0,373

5$: MOV #11501,1$ ;RESTORE SWITCH INSTR (MOV _@R5,R1)
MOV $ODF1,R1 ;START ADDR FOR CLEAR OPERATION
6$: CLR (R1)+ ;CLEAR ALL OVERLAY REGIONS
CMP R1,$ODF2 ;DONE?
BLO 6$ ;LO -> NO, REPEAT
BR 1$ ;AND RETURN TO CALL IN PROGRESS

$ODF1:: ,WORD $OVDF1 ;HIGH ADDR OF ROOT SEGMENT + 2 (NXT AVAIL)
$ODF2:: ,WORD $OVDF2 ;HIGH ADDRESS OF /O OVERLAYS + 2 (NXT AVAIL)

.DSABL LSB

.SBTTL $OVTAB OVERLAY TABLE

;+
; OVERLAY TABLE STRUCTURE:
;
; LOC G4 -> $OVTAB:
; ,WORD <CORE ADDR>,<RELATIVE BLK>,<WORD COUNT> /O OVERLAYS
; DUMMY SUBROUTINES FOR ALL OVERLAY SEGMENTS
;-

.PSECT $OTABL,D,GBL,OVR

$OVTAB:

.END
```

Figure 11–6 illustrates a sample set of subroutine calls and return paths. In the example, solid lines represent valid subroutine calls and dotted lines represent invalid calls.

Suppose the following subroutine calls were made:

1. The root calls segment 8

2. Segment 8 calls segment 4

3. Segment 4 calls segment 3

Segment 3 can now call any of the following, in any order:

```txt
Itself
Segment 4
Segment 8
The root
```

Figure 11-6: Sample Subroutine Calls and Return Paths

[figure omitted]

These segments and the root, of course, are all currently resident in memory.

Segment 3 cannot call any of the following segments because this would destroy its return path:

Segments 2 and 1
Segment 5
Segments 6 and 7

Look at what might happen if one of these invalid calls is made. Assume that segments 3, 4, and 5 all contain MACRO subroutines. Suppose segment 4 calls segment 3 and segment 3 in turn calls segment 5. Segment 5 is not resident in region 2, so an overlay read-in occurs: segment 5 is read into memory, thus destroying the memory-resident copy of segment 4. The subroutine in segment 5 executes and returns control to segment 3. Segment 3 finishes its task and tries to return control to segment 4. Segment 4, however, has been replaced in memory by segment 5. Segment 4 cannot regain control and the program loops indefinitely, traps, or random results occur.

The guidelines already mentioned and some additional rules for creating overlay structures are summarized below.

1. SYSLIB must be present to create an overlay structure because it contains the overlay handler.

2. Overlay segments assigned to the same region must be logically independent; that is, the components of one segment cannot reference the components of another segment assigned to the same region.

3. The root segment contains the transfer address, stack space, impure variables, data, and variables needed by many different segments. The FORTRAN main program unit must be placed in the root segment.

4. A global program section (such as a named COMMON block or a .PSECT with the GBL attribute) that is referenced in more than one segment is placed in the root segment by the linker. This permits common access across the different segments.

5. Object modules that are automatically acquired from a library file will automatically be placed in an overlay segment, so long as that library module is referenced only by that segment. If a library module is referenced by more than one segment, LINK places that library module in the root unless you use the /D option. See Section 11.6.4 for more details on /D.

Do not specify a library file on the same command line as an overlay segment. You must specify all library modules before specifying any overlay modules. Link places in the root any modules from a multiple definition library and any modules included with the /I option.

6. All COMMON blocks that are initialized with DATA statements must be similarly initialized in the segment in which they are placed.

7. When you make calls to overlay segments, the entire return path to the calling routine must be in memory. (With extended memory overlays, the entire return path must be mapped. See Section 11.5.2.) This means you should take the following points into account:

a. You can make calls with expected return (as from a FORTRAN main program to a FORTRAN or MACRO subroutine) from an overlay segment to entries in the same segment, the root segment, or to any other segment, so long as the called segment does not overlay in memory part of your return path to the main program.

b. You can make jumps with no expected return (as in a MACRO program) from an overlay segment to any entry in the program with one exception: you can not make such a jump to a segment if the called segment will overlay an active routine (that is, a routine whose execution has begun, but not finished, and that will be returned to) in that region.

c. Calls you make to entries in the same region as the calling routine must be entirely within the same segment, not within another segment in the same region.

8. You must make calls or jumps to overlay segments directly to global symbols defined in an instruction p-sect (entry points). For example, if ENTER is a global tag in an overlay segment, the first of the following two commands is valid, but the second is not:
JMP ENTER ;VALID
JMP ENTER+6 ;INVALID

9. You can use globals defined in an instruction p-sect (entry points) of an overlay segment only for transfer of control and not for referencing data within an overlay segment. The assembler and linker cannot detect a violation of this rule so they issue no error. However, such a violation can cause the program to use incorrect data. If you reference these global symbols outside of their defining segment, the linker resolves them by using dummy subroutines of four words each in the overlay handler. Such a reference is indicated on the load map by a @ following the symbol.

10. The linker directly resolves symbols that you define in a data p-sect. It is your responsibility to load the data into memory before referencing a global symbol defined in a data section.

11. You cannot use a section name to pass control to an overlay because it does not load the appropriate segment into memory. For example, JSR PC, OVSEC is invalid if you use OVSEC as a .CSECT name in an overlay. You must use a global symbol to pass control from one segment to the next.

12. In the linker command string, specify overlay regions in ascending order.

13. Overlay regions are read-only. Unlike USR swapping, an overlay handler does not save the segment it is overlaying. Any tables, variables, or instructions that are modified within a given overlay segment are reinitialized to their original values in the SAV or REL file if that segment has been overlaid by another segment. You should place any variables or tables whose values must be maintained across overlays in the root segment.

14. Your program cannot use channel 17 (octal) because overlays are read on that channel.

15. MACRO and FORTRAN directly resolve all global symbols that are defined in a module. If LINK moves the p-sect where they are defined from an overlay segment to the root, LINK will not generate an overlay table entry for those symbols.

Refer to the RT-11/RSTS/E FORTRAN IV User's Guide for additional information.

The absolute section (. ABS.) never takes part in overlaying in any way. It is part of the root and is always resident.

This set of rules applies only to communications among the various modules that make up a program. Internally, each module must only observe standard programming rules for the PDP-11 (as described in the PDP-11 Processor Handbook and in the FORTRAN and MACRO-11 Language Reference Manuals).

Note that the condition codes set by your program are not preserved across overlay segment boundaries.

The linker provides overlay services by including a small resident overlay handler in the same file with your program to be used at program run time. The linker inserts this overlay handler plus some tables into your program beginning at the bottom address. The linker then moves your program up in memory to make room for the overlay handler and tables, if necessary. The handler is stored in SYSLIB. This scheme is diagrammed in Figure 11–7.

## 11.5.2 Extended Memory Overlays

You can use LINK to create an overlay structure for your program that uses extended memory. Although you need a hardware configuration that includes a memory management unit to run a program that has overlays in extended memory, you can link it on any RT-11 system. Read Section 11.5.1, Low Memory Overlays, before reading this section — much of the information contained in that section applies to extended memory overlays as well.

Usually, you can convert an overlaid program to use extended memory without modifying the code. The extended memory overlay handler and the keyboard monitor include all the programmed requests necessary to access extended memory (see the RT-11 Software Support Manual for details on extended memory restrictions). The overlay tables also include additional data used by these requests, so you can access extended memory automatically without using extended memory programmed requests in your program. Refer to the RT-11 Software Support Manual for more information on extended memory.

The extended memory overlay structure is different from the low memory overlay structure in that extended memory overlays can reside concurrently in extended memory. This allows for speedier execution because, once read in, your program requires fewer I/O transfers with the auxiliary mass storage volume. If all program data is resident, and the program is loaded, the program may be able to run without an auxiliary mass storage volume. However, you must observe the same restrictions with extended memory overlays that apply to low memory overlays, especially regarding return paths. This section describes how to create a program with overlays in extended memory and ends with an example of such a program.

NOTE

Figure 11-7: Memory Diagram Showing BASIC Link with Overlay Regions

[figure omitted]

Overlays that reside in extended memory can contain impure data, but impure data is not automatically initialized each time a new overlay segment maps over a segment that contains impure data.

11.5.2.1 Virtual Address Space — When you set up an extended memory overlay structure, you set it up as though you had locations 0 to 177777 (that is, 32K words of memory) available for your use. Physically, not all these locations are available to you in low memory; your program's absolute section resides, typically, in locations 0 to 500, and the monitor takes up a good deal of memory starting at location 160000, going downward. Also, the computer sets aside addresses 160000 to 177777 for the I/O page. But, because of memory management, you can structure your program as though you had all 32K words of memory for your use. This space is called the program virtual address space (PVAS). The memory management hardware and the monitor will allow part of your 32K address space to reside in extended memory.

The PVAS is divided into eight sections called pages, numbered 0–7. Each page contains 4K words. RT-11 references each page by the Active Page Register (APR). The APR contains the relocation constant, which controls the mapping for each page. Figure 11–8 illustrates the PVAS, divided into pages. Keep in mind the structure of your program in terms of how it uses the virtual address space so that you can design its overlay structure correctly and efficiently.

Figure 11-8: Program Virtual Address Space

<table><tr><td colspan="3">PVAS</td></tr><tr><td></td><td></td><td>177777</td></tr><tr><td>APR 7</td><td>PAGE 7</td><td>160000</td></tr><tr><td>APR 6</td><td>PAGE 6</td><td>140000</td></tr><tr><td>APR 5</td><td>PAGE 5</td><td>120000</td></tr><tr><td>APR 4</td><td>PAGE 4</td><td>100000</td></tr><tr><td>APR 3</td><td>PAGE 3</td><td>60000</td></tr><tr><td>APR 2</td><td>PAGE 2</td><td>40000</td></tr><tr><td>APR 1</td><td>PAGE 1</td><td>20000</td></tr><tr><td>APR 0</td><td>PAGE 0</td><td>0</td></tr></table>

[figure omitted]

Figure 11-9: Physical Address Space for Program with Low Memory Overlays

Each overlay that is to reside in extended memory must start on one of the 4K-word pge boundaries. The linker automatically rounds up the size of each segment to achieve this. The linker thereby restricts you to a region reserved for the root, and a maximum of seven virtual overlay regions, each starting on a page boundary. If any of these segments extends beyond a 4K word boundary, then one fewer virtual overlay regions is available. For example, if the root is 5K words long, then the static region uses the addresses referenced by APRs 0 and 1. Only six virtual overlay regions will remain, those referenced by APRs 2 through 7.

11.5.2.2 Physical Address Space – When LINK creates the load module for a program that has overlays in extended memory, it defines how each overlay will be mapped to extended memory during run time. LINK handles extended memory overlays differently from low memory overlays. Figures 11–9 and 11–10 compare the differences.

Figure 11–9 shows the physical address space of a program that has low memory overlays. Overlay segments share each region, and each is read in from an auxiliary mass storage volume when called.

[figure omitted]

In Figure 11–10, the diagram on the left shows the program virtual address space (0 to 177777). The diagram on the right shows the physical address space. In the program virtual address space, there is only one overlay region, and it starts on a 4K word boundary (APR 1 references this region). The regions of address space that will map to extended memory are called virtual overlay regions. Notice the arrows that point from the virtual overlay region to a number of overlay segments that appear on the right.

The overlay segments in the virtual overlay region shown use the space specified by APR 1 (20000 to 37777), but they occupy contiguous areas of extended memory, called partitions. At run time, overlay segments 1 through 4, once called, are concurrently resident in extended memory, and no further disk I/O is done to access these segments.

11.5.2.3 Virtual and Privileged Jobs — The amount of virtual address space available to your program depends on the type of program you are running. Background, foreground, and system jobs can fall into two categories: virtual and privileged.

Virtual jobs can use all 32K words of the virtual address space, but they cannot directly access the I/O page, the monitor, the vectors, or other jobs. Unless you need to access these protected areas of memory, make your jobs virtual by setting bit 10 of the JSW.

Privileged jobs also have 32K words of virtual addressing space, but by default, the protected areas (monitor, I/O page, vectors, and so on) are part of this addressing space. Just as you may lose access to protected areas if you implement your own extended memory mapping, you may lose access to the monitor and I/O page if you use extended memory overlays with a privileged job.

Virtual and privileged jobs can map to extended memory. You can use extended memory overlays with any type of virtual or privileged job (foreground, system, background).

See the RT-11 Software Support Manual for more details on virtual and privileged jobs, and see the RT-11 Programmer's Reference Manual for instructions on how to make a job virtual.

11.5.2.4 Extended Memory Overlay Option (/V:n[:m]) — Use the /V option to describe your program's structure in terms of virtual overlay regions (areas of virtual address space) and partitions (areas of physical address space). The argument, n, represents a virtual overlay region, and m represents a partition. As you specify successive extended memory overlay segments in the command string, make sure that the n and m in the /V:n[:m] notation are in ascending order. The following examples show how to use the /V:n[:m] option.

In the first example, program PROG has four segments to be mapped to extended memory. The four segments are named SEG1, SEG2, SEG3, and SEG4.

, R LINK

\* PROG = PROG //

\* SEG1/V:1

\* SEG2/V:1

\* SEG3/V:1

\* SEG4/V:1//

These segments map to extended memory exactly as Figure 11–10 shows. Notice how each segment fits into its own partition in extended memory. Because each segment fits into its own partition, no storage volume access is necessary to change (or swap) segments once they have been read in.

## NOTE

The /V:n[:m] option works differently from the /O:n option. If /O:n were used in the previous example, the four segments would share the same physical locations, obviously requiring storage volume I/O as each segment is called. With /V:n[:m], each segment from the previous example occupies a unique area in extended memory, and no mass storage I/O is necessary after each segment is called.

The next example places the same four segments into virtual overlay regions 1 and 2. Although the program in this example uses two virtual overlay regions at run time, the segments will reside in memory the same as the segments shown in Figure 11–10. The virtual address space will be different for this example, however (see Figure 11–11). SEG1 and SEG2 use APR 1 (20000 to 37777), while SEG3 and SEG4 use APR 2 (40000 to 57777).

, R LINK
\* PROG=PROG//
\* SEG1/V:1
\* SEG2/V:1
\* SEG3/V:2
\* SEG4/V:2//

Figure 11-11: Virtual and Physical Address Space

[figure omitted]

The argument, m in /V:n[:m], represents the partition in extended memory for the overlay segment. If you use m, segments can share the same partition in extended memory. That is, a segment, when called by your program, can be read in from auxiliary storage, thus overlaying the segment that currently occupies the same partition. When segments share partitions, the program requires auxiliary storage for I/O during run time, as does a program with low memory overlays.

LINK makes each partition the size of the largest segment it must accommodate. The following example generates the overlay structure shown in Figure 11–12.

\* R LINK
\* PROG=PROG//
\* SEG1/V:1:1
\* SEG2/V:1:1
\* SEG3/V:2
\* SEG4/V:2
\* SEG5/V:2:1
\* SEG6/V:2:1//

Figure 11-12: Extended Memory Partitions that Contain Sharing Segments

[figure omitted]

Notice that there are four segments specified for virtual overlay region 2, and that two segments share partition 1. The m value in /V:n:m groups segments in a region. The only reason to use the argument m is to create a partition that contains two or more segments. As shown in the previous example, the m argument is specified in ascending order within each virtual overlay region. This means you can renumber m from 1 for each virtual overlay region.

If you specify four segments for the same virtual overlay region, as in Example 1 below, the result is the same as if you specified Example 2. Because two segments are not specified to share the same partition, the partition order is as Example 2 shows.

## Example 1

```txt
*       SEG1/V:1
*       SEG2/V:1
*       SEG3/V:1
*       SEG4/V:1
```

## Example 2

```txt
*     SEG1/V: 1:1
*     SEG2/V: 1:2
*     SEG3/V: 1:3
*     SEG4/V: 1:4
```

## 11.5.3 Combining Low Memory Overlays with Extended Memory Overlays

You can combine low memory overlays and extended memory overlays in the same program structure. If you do so, however, each low memory overlay region you use makes your remaining virtual address space smaller.

It is important to note that as you combine low memory overlays with extended memory overlays, you must list your regions in ascending order, whether or not one is a low memory overlay region and the next is a virtual region. That is, if the first overlay region is a low memory overlay region, specify it as region 1. If the next region is a virtual region, specify it as region 2. Note that you must specify low memory overlays before extended memory overlays.

The following example creates a low memory overlay region and a virtual overlay region above it.

```txt
R LINK
*   PROG=PROG//
*   SEG1/0:1
*   SEG2/0:1
*   SEG3/V:2
*   SEG4/V:2
*   SEG5/V:2:1
*   SEG6/V:2:1
*   SEG7/V:2:1
*   SEG8/V:2:2
*   SEG9/V:2:2
*   SEG10/V:3//
```

Figure 11–13 shows how low memory and extended memory might appear if the program from this example were loaded.

Figure 11-13: Memory Diagram Showing Low Memory and Extended Memory Overlays

[figure omitted]

## 11.5.4 Load Map

Figure 11–14 shows a sample load map for PROG.SAV, whose overlay structure is defined below.

```txt
* PROG,PROG=MODO//
* MOD1/0:1
* MOD2/0:1
* MOD3/V:2
* MOD4/V:3//
```

Table 11-9 describes the portions of this load map devoted to low memory and extended memory overlays.

Figure 11-14: Load Map for Program with Unmapped and Virtual Overlays

```txt
RT-11 LINK V08.00
V .SAV Title: .MAIN. Ident:
Section Addr Size Global Value Global Value Global Value
.ABS. 000000 001000 = 256. words (RW,I,GBL,ABS,OVR)
$OHAND 001000 000252 = 85. words (RW,I,GBL,REL,CON)
$OVRHV 001000 $OVRH 001004 V$READ 001034
$DONE 001046 $VDF5 001234 $VDF4 001236
$VDF1 001246 $VDF2 001250
$OTABL 001252 000114 = 38. words (RW,D,GBL,REL,OVR)
001366 000410 = 132. words (RW,I,LCL,REL,CON)
MAIN 001776 000070 = 28. words (RW,I,LCL,REL,CON)
START 001776 RET1 002010 RET2 002014
LIMIT 002024
LML4 002066 000026 = .11. words (RW,I,GBL,REL,CON)
MSGL 002066
LML5 002114 000026 = 11. words (RW,I,GBL,REL,CON)
MSGL2 002114
Segment size = 002142 = 561. words
Overlay region 000001 Segment 000001
LML2 002144 000032 = 13. words (RW,I,LCL,REL,CON)
START1@ 002144
Segment size = 000032 = 13. words
Overlay region 000001 Segment 000002
LML3 002144 000036 = 15. words (RW,I,LCL,REL,CON)
START2@ 002144
Segment size = 000036 = 15. words
```

```txt
Virtual overlay region 000002
-----------------
Partition        000001    Segment 000003
LML7      020002 000034 = 14.     words (RW,I,LCL,REL,CON)
                    START3   020002
LML6      020036 000042 = 17.     words (RW,I,GBL,REL,CON)
                    MSGL3   020036 RET4      020050
Segmentsize = 000076 = 31.     words

Virtual overlay region 000003
-----------------
```

(Continued on next page)

```txt
Partition          000002  Segment 000004
  LML9    040002 000076 = 31,      words (RW,I,GBL,REL,CON)
                  MSGL9@  040002
  Segment size = 000076 = 31,      words

Transfer address = 001776, High limit = 002200 = 576, words

Virtual high limit = 040076 = 8223, words, next free address = 060000

Extended memory required = 000200 = 64,           words
RT-11 LINK   VOB.00   Global Symbol Cross Reference Table   Pase 1

$OVDF1 VHANDL+
$OVDF2 VHANDL+
$OVDF3 VHANDL+
$OVDF4 VHANDL+
$OVDF5 VHANDL+
$OVRH   VHANDL++ 
$OVRHV VHANDL++ 
$VDF1   VHANDL++ 
$VDF2   VHANDL++ 
$VDF4   VHANDL++ 
$VDF5   VHANDL++ 
LIMIT   .MAIN.# 
MSGL     .MAIN.# 
MSGL2   .MAIN.# 
MSGL3   .MAIN.# 
MSGL9   .MAIN.,   .MAIN.# 
RET1     .MAIN.# 
RET2     .MAIN.# 
RET4     .MAIN.# 
START     .MAIN.# 
START1     .MAIN.,   .MAIN.# 
START2     .MAIN.,   .MAIN.# 
START3     .MAIN.# 
V$DONE VHANDL++ 
V$READ VHANDL++
```

Table 11–9 gives a line-by-line description of the load map above. This table makes references only to those portions of the load map that are unique to overlaid programs, and also describes the global cross-reference table (which is not unique to overlaid programs). For details on other parts of the load map, see Section 11.4.4.

Table 11-9: Line-by-Line Sample Load Map Description

| Line | Description |
| --- | --- |
| 7-10 | $OHAND p-sect. This is the overlay handler for overlays in both low and extended memory. |
| 11 | $OTABL p-sect. This program section contains tables of data used by the overlay handler. |
| 12 | Blank p-sect. The load map for overlaid programs lists the blank p-sect, when present, after the $OHAND and $OTABL p-sects. |
| 20 | Contains data about the size of the program’s root. The sections of the load map that follow provide information on the part of the program that is overlaid. |

(Continued on next page)

Table 11-9: Line-by-Line Sample Load Map Description (Cont.)

| Line | Description |
| --- | --- |
| 22 | Header for overlay region 1, segment 1 (low memory overlay region). |
| 23-24 | LML2 p-sect. This is the only p-sect in segment 1. Notice in line 24 the @ character next to the global START1. This character indicates that its associated global is accessed through data contained in the overlay table p-sect, $OTABL, which is in the root. |
| 25 | Contains data on the size of segment 1. |
| 32 | Delineates the portion of the load map devoted to low memory from the portion devoted to extended memory. |
| 34 | Header for virtual overlay region 2. Note that overlay regions are numbered in ascending order, whether in low or extended memory. |
| 37 | Header for partition 1, segment 3. |
| 41 | Notice the absence of the @ character for the globals in p-sect LML6. This indicates that LML6 is not called outside segment 3. |
| 42 | Contains data on the size of overlay segment 3. |
| 44 | Header for virtual overlay region 3. |
| 47 | Header for partition 2, segment 4. |
| 50 | Contains data on the size of segment 4. Notice that segments 3 and 4 have the same length. LINK automatically rounds up the size of virtual overlay segments to multiples of 32 (decimal) words (or 100 octal bytes). LINK adds an overlay segment number word to the segment size number (the number 000076 that follows 040002 in line 48) to give the actual segment size. |
| 53 | Transfer address and high limit. The transfer address is the start address of the program. The high limit is the last low memory address used by the root and unmapped overlays. |
| 56 | Virtual high limit. Indicates the last virtual address used by the part of the program in extended memory. The next free address is the address of the next page not in use by the program. |
| 59 | Indicates the amount of extended memory required by the program. Make sure you check this figure to ensure you have adequate space for your program at run time. |
| 60-87 | Cross-reference section of defined global symbols. Displays a cross-reference of all global symbols defined during the linking process. Note that global symbols are listed alphabetically and are followed by the names of the modules in which the global symbols are either defined or referenced. A pound sign (#) following a module name indicates that the global symbol is defined in that module. A plus sign (+) following a module name indicates that the module is from a library. |

## Figure 11-15 shows the extended memory overlay handler.

## Figure 11-15: Extended Memory Overlay Handler

```asm
.SBTTL THE RUN-TIME OVERLAY HANDLER
·ENABL GBL

;+
; THE FOLLOWING CODE IS INCLUDED IN THE USER'S PROGRAM BY THE
; LINKER WHENEVER LOW MEMORY OVERLAYS ARE REQUESTED BY THE USER.
; THE RUN-TIME LOW MEMORY OVERLAY HANDLER IS CALLED BY A DUMMY
; SUBROUTINE OF THE FOLLOWING FORM:
;
; JSR R5,$OVRH ;CALL TO COMMON CODE FOR LOW MEMORY OVERLAYS
; .WORD <OVERLAY **G> ;# OF DESIRED SEGMENT
; .WORD <ENTRY ADDR> ;ACTUAL CORE ADDRESS (VIRTUAL ADDRESS)

; ONE DUMMY ROUTINE OF THE ABOVE FORM IS STORED IN THE RESIDENT PORTION
; OF THE USER'S PROGRAM FOR EACH ENTRY POINT TO A LOW MEMORY OVERLAY SEGMENT,
; ALL REFERENCES TO THE ENTRY POINT ARE MODIFIED BY THE LINKER TO BE
; REFERENCES TO THE APPROPRIATE DUMMY ROUTINE, EACH OVERLAY SEGMENT
; IS CALLED INTO CORE AS A UNIT AND MUST BE CONTIGUOUS IN CORE, AN
; OVERLAY SEGMENT MAY HAVE ANY NUMBER OF ENTRY POINTS, TO THE LIMITS
; OF CORE MEMORY, ONLY ONE SEGMENT AT A TIME MAY OCCUPY AN OVERLAY REGION.

; IF OVERLAYS IN EXTENDED MEMORY ARE SPECIFIED, THE FOLLOWING DUMMY SUBROUTINE
; IS USED AS THE ENTRY POINT TO THE EXTENDED MEMORY OVERLAY HANDLER.

; JSR R5,$OVRHV ;ENTRY FOR /V (EXTENDED MEMORY) OVERLAYS
; .WORD <OVERLAY **G> ;# OF DESIRED SEGMENT
; .WORD <VIRTUAL ENTRY ADDRESS> ;VIRTUAL ADDRESS OF SEGMENT

; ADDITIONAL DATA STRUCTURES IN THE EXTENDED MEMORY OVERLAY HANDLER AND THE
; OVERLAY TABLE PERMIT USE OF EXTENDED MEMORY, ONE REGION DEFINITION
; BLOCK IS DEFINED IN THE HANDLER, AND XM EMT'S ARE ALSO INCLUDED, WINDOW
; DEFINITION BLOCKS FOR THE EXTENDED MEMORY PARTITIONS FOLLOW THE DUMMY
; SUBROUTINES IN THE OVERLAY TABLE.

; THERE IS ONE WORD PREFIXED TO EVERY OVERLAY REGION THAT IDENTIFIES THE
; SEGMENT CURRENTLY RESIDENT IN THAT OVERLAY REGION, THIS WORD IS AN INDEX
; INTO THE OVERLAY TABLE AND POINTS AT THE OVERLAY SEGMENT INFORMATION.

; UNDEFINED GLOBALS IN THE OVERLAY HANDLER MUST BE NAMED "$OVDF1" TO
; "$OVDFn" SUCH THAT A RANGE CHECK MAY BE DONE BY LINK TO DETERMINE IF
; THE UNDEFINED GLOBAL NAME IS FROM THE OVERLAY HANDLER, A CHECK IS
; DONE ON THE .RAD50 CHARACTERS "$OV", AND THEN A RANGE CHECK IS DONE ON
; THE .RAD50 CHARACTERS "DF1" TO "DFn", THESE GLOBAL SYMBOLS DO NOT APPEAR
; ON LINK MAPS, SINCE THEIR VALUE IS NOT KNOWN UNTIL AFTER THE MAP HAS BEEN
; PRINTED, CURRENTLY $OVDF1 TO $OVDFS ARE IN USE.

; GLOBAL SYMBOLS V$READ AND V$DONE ARE USEFUL WHEN DEBUGGING OVERLAID
; PROGRAMS.

; V$READ:: WILL APPEAR IN THE LINK MAP AND LOCATES THE ,READW
; STATEMENT IN THE OVERLAY HANDLER.

; V$DONE:: WILL APPEAR IN THE LINK MAP AND LOCATES THE FIRST
; INSTRUCTION AFTER THE ,READW IN THE OVERLAY HANDLER.

;-

.MCALL .WDBDF,.ROBDF,.PRINT,.EXIT,.READW,.V1..
;..V1.. ;V1 FORMAT
; .WDBDF ;DEFINE WDB OFFSETS
; .RDBDF ;DEFINE RDB OFFSETS

.SBTTL OVERLAY HANDLER CODE

.PSECT $OHAND,GBL

.ENABL LSB

(Continued on next page)
```

;+
; THERE ARE TWO ENTRY POINTS TO THE OVERLAY HANDLER: \$OVRHV FOR /V
; (EXTENDED MEMORY) OVERLAYS, AND \$OVRH FOR /O (LOW MEMORY) OVERLAYS,
;-

\$OVRHV:: INC      (PC)+          ;SET /V OVERLAY ENTRY SWITCH
10\$:     ,WORD    0                  ;=0 IF /0 ; =1 IF /V OVERLAY ENTRY
\$OVRH:: MOV       R0,-(SP)        ;/0 OVERLAY ENTRY POINT
        MOV       R1,-(SP)         ;SAVE REGISTERS
        MOV       R2,-(SP)

20\$:
    BR      90\$          ;FIRST CALL ONLY \* \* \*
;     MOV     @R5 ,R1       ;PICK UP OVERLAY NUMBER
    ADD     \$\*OVTAB-G ,R1   ;CALCULATE TABLE ADDRESS
    MOV     (R1)+ ,R2       ;GET FIRST ARG, OF OVERLAY SEG, ENTRY
    TST      10\$           ;IS THIS /V ENTRY?
    BNE      60\$           ;IF NON-ZERO THEN YES
30\$:    CMP     (R5)+ ,@R2   ;IS OVERLAY ALREADY RESIDENT?
    BEQ      40\$           ;YES, BRANCH TO IT

;+
; THE .READW ARGUMENTS ARE AS FOLLOWS:
; CHANNEL NUMBER, CORE ADDRESS, LENGTH TO READ, RELATIVE BLOCK ON DISK,
; THESE ARE USED IN REVERSE ORDER FROM THAT SPECIFIED IN THE CALL.
;-

V\$READ::,READW 17,R2,@R1,(R1)+ ;READ FROM OVERLAY FILE
V\$DONE::BCS 50\$
40\$: MOV (SP)+,R2 ;RESTORE USERS REGISTERS
MOV (SP)+,R1
MOV (SP)+,R0
MOV @R5,R5 ;GET ENTRY ADDRESS
CLR 10\$ ;CLEAR /V FLAG
RTS R5 ;ENTER OVERLAY ROUTINE AND RESTORE USER'S R5
50\$: EMT 376 ;SYSTEM ERROR 10 (OVERLAY I/O)
.BYTE 0,373

;+
; VIRTUAL OVERLAY SEGMENTS IN THE SAME REGION BUT IN DIFFERENT PARTITIONS
; USE DIFFERENT WDB'S.  ONLY ONE OF THESE WINDOWS EXISTS AT ANY TIME,
; THIS IS BECAUSE WHEN A NEW WINDOW IN A VIRTUAL OVERLAY REGION IS CREATED,
; THE MONITOR IMPLICITLY ELIMINATES ANY WINDOW THAT EXISTS IN THAT
; VIRTUAL OVERLAY REGION.  THUS, IF THE CALLED OVERLAY SEGMENT IS NOT
; CURRENTLY MAPPED, ITS WINDOW MUST BE RE-CREATED (,CRAW'ED) BESIDES
; BEING MAPPED,  THE MAPPING IS DONE IMPLICITLY IN THE FOLLOWING CODE
; SINCE THE WS.MAP BIT IS SET IN ALL OF THE VIRTUAL OVERLAY SEGMENTS'
; WDB'S.

GO\$: TSTB @R2 ;DO WE NEED TO CREATE A WINDOW (,CRAW)?
BEQ 70\$ ;YES
MOV @W,NBAS(R2),RO ;GET INDEX OF SEGMENT NOW MAPPED
BEQ 70\$ ;THERE ISN'T ONE; WE MUST ,CRAW
CMP \$OVTAB-G(RO),R2 ;IS OVERLAY REGION SAME AS THIS ONE?
BEQ 80\$ ;IF EQUAL, JUST WORRY ABOUT DISK I/O

70\$: MOV #AREA+2,RO ;POINT TO EMT ARGUMENT BLOCK + 2
MOV R2,@RO ;STUFF ADDRESS OF WDB IN EMT AREA
MOV 30,\*^0400+2,,-(RO) ;STUFF ,CRAW CODE; RO ->EMT AREA
EMT 375 ;DO THE EMT
BCS 110\$ ;CARRY SET MEANS ERROR!

90\$:     MOV     #11501,20\$          ;RESTORE SWITCH INSTR (MOV @R5,R1)
        MOV     \$VDF1,R1           ;START ADDRESS FOR CLEAR OPERATION
100\$:    CMP     R1,\$VDF2           ;ARE WE DONE?
        BHIS     20\$                  ;HIS -> DONE, OR NO /O OVERLAYS
        CLR     (R1)+           ;CLEAR ALL LOW MEMORY OVERLAY REGIONS
        BR      100\$

```asm
; ERROR MESSAGE
110\$:    MOV     *MSG2,RO          ;OTHERWISE ERROR
        .PRINT                  ;AND PRINT MESSAGE
        .EXIT                  ;AND EXIT

.DSABL  LSB

.SBTTL IMPURE AREA

.ENABL  LC
.NLIST BEX
MSG2:   .ASCIZ  /VHANDL-F-Window error/
LIST BEX

.EVEN
AREA:   .WORD   0,0             ;EMT AREA BLOCK FOR .CRAW

\$VDF5:: .WORD   \$OVDF5           ;POINTER TO WORD AFTER WDB'S IN OVERLAY TABLE
\$VDF4:: .WORD   \$OVDF4           ;POINTER TO START OF WDB'S IN OVERLAY TABLE

RGADR:   .WORD   0             ;THREE WORD REGION DEFINITION BLOCK
RGSIZ:   .WORD   \$OVDF3,0       ;\$OVDF3 -> SET BY LINK = SIZE OF REGION

\$VDF1:: .WORD   \$OVDF1           ;HIGH ADDR ROOT SEGMENT + 2 (NXT AVAIL)
\$VDF2:: .WORD   \$OVDF2           ;HIGH ADDR /O OVERLAYS + 2 (NXT AVAIL)

.SBTTL \$OVTAB OVERLAY TABLE

;+
; OVERLAY TABLE STRUCTURE:
;
; LOC 64 ->      \$OVTAB:
;
;     .WORD   <CORE ADDR>,<RELATIVE BLK>,<WORD COUNT> /O OVERLAYS
; LOC 66 =>      .WORD   <WDB ADDR>,<RELATIVE BLK>,<WORD COUNT> /V OVERLAYS
;         DUMMY SUBROUTINES FOR ALL OVERLAY SEGMENTS
; \$VDF4 ->      WINDOW DEFINITION BLOCKS FOR EXTENDED MEMORY OVERLAYS (/V)
; \$VDF5 ->      WORD AFTER THE END OF THE WINDOW DEFINITION BLOCKS (/V)
;-

.PSECT \$OTABL,D,GBL,OVR

\$OVTAB:

.END
```

## 11.6 Options

Full descriptions of the options summarized in Table 11–6 follow in alphabetical order.

## 11.6.1 Alphabetical Option (/A)

The /A option lists global symbols in program sections in alphabetical order.

## 11.6.2 Bottom Address Option (/B:n)

The /B:n option supplies the lowest address to be used by the relocatable code in the load module. The argument, n, is a six-digit unsigned, even octal number that defines the bottom address of the program being linked. If you do not supply a value for n, the linker prints:

```txt
?LINK-F-/B no value
```

Retype the command line, supplying an even octal value.

When you do not specify /B, the linker positions the load module so that the lowest address is location 1000 (octal). If the ASECT size is greater than 1000, the size of ASECT is used.

If you supply more than one /B option during the creation of a load module, the linker uses the first /B option specification. /B is invalid when you are linking to a high address (/H). The /B option is also invalid with foreground links. Foreground modules are always linked to a bottom address of 1000 (octal).

The bottom value must be an unsigned, even, octal number. If the value is odd, the ?LINK-F-/B odd value error message prints. Reenter the command string specifying an unsigned, even octal number as the argument to the /B option.

## 11.6.3 Continuation Option (/C or //)

The continuation option (/C or //) lets you type additional lines of command string input.

Use the /C option at the end of the current line and repeat it on subsequent command lines as often as necessary to specify all the input modules in your program. Do not enter a /C option on the last line of input.

The following command indicates that input is to be continued on the next line; the linker prints an asterisk.

```csv
* OUTPUT,LP:=INPUT/C
*
```

An alternate way to enter additional lines of input is to use the // option on the first line. The linker continues to accept lines of input until it encounters another // option, which can be either on a line with input file specifications or on a line by itself. The advantage of using the // option instead of the /C option is that you do not have to type the // option on each continuation line. This example shows the command file that links the linker:

```csv
R LINK
LINK,LINK=LINK0,LNKLB1/D//
LINK1/0:1
LINK2/0:1
LINK3/0:1
LINK4/0:1
LINK5/0:1
LINK6/0:1
LINK7/0:1
LINK8/0:1
LNKEM/0:1//
BITST
GETBUF
WRITO
WRTLRU
ZSWFIL
RET
```

You cannot use the /C option and the // option together in a link command sequence. That is, if you use // on the first line, you must use // to terminate input on the last line. If you use /C on the first line, use /C on all lines but the last.

## 11.6.4 Duplicate Global Symbol Option (/D)

The /D option allows you to specify library modules that you want to reside in more than one overlay segment. Type /D on the first command line. After you have typed all input command lines, the linker prompts:

Duplicate symbol?

Type the names of the global symbols in the library module that you want to be defined once in each segment that references those symbols. Follow each global symbol with a carriage return. A carriage return on a line by itself terminates the list of symbols. Only global symbols defined in library modules can be duplicated. If you use the /D option and specify a global symbol that is defined outside of a library module, the symbol definition is not duplicated and LINK prints the message ?LINK-W-Duplicate symbol SYMBOL defined in DEV:FILNAM.TYP.

When you do not use the /D option and a global symbol defined in a library module is externally referenced (that is, the global symbol is referenced from a segment other than the one in which it is defined), the linker places the library module in the program's root segment. Therefore, if a library module is referenced by more than one global symbol, each of the global symbols in the library module that is referenced should be named in response to the /D option. Otherwise, the library module will be placed in the root segment. Also, if any of a library module's global symbols are referenced from the root, the library module will be placed in the root even if you have named the global symbols in response to the /D option. In each of these cases when a library module that link places in the root contains global symbols declared with /D, LINK prints the following message and the global symbol is not duplicated.

?LINK-W-Duplicate symbol SYMBOL is forced to the root

## Special Programming Considerations for the /D Option

Even when a library module you duplicate is not referenced from the root, any global section within that module that is referenced from more than one segment is always placed in the root. If local sections within the same library module have no need to communicate with each other, define the global section with the CON attribute. This causes the linker to place a separate copy of the global section in the root for each copy of the library module's local sections placed in overlays. Although the global section resides in the root while the local sections reside in overlays, each copy of the library module retains its identity as a separate copy of the module. Since each copy of the global section is bound to its own local section in an overlay, this ensures that references between the local and global sections will be bound to the correct definitions.

However, when a library module that you want to duplicate will be placed in overlay segments that exchange information, another consideration exists. If the library module contains a section of global data to be referenced by local sections within the module, but the global section does not reference any local section within the module, you should move a copy of the global section to the root. To move this section to the root, define the section with a unique name and give the section the GBL and OVR attributes. When this section is placed in the root, the local sections from the duplicated library module that reside in the overlay segments can reference the global section in the root. Since the global section has been given the OVR attribute rather than CON, the local sections can pass information to specific locations in the global section, and the local sections can access the same locations to send and receive data.

Figure 11–16 illustrates a duplicated library module whose global data section has been forced to the root with the CON attribute. The arrows show each local section accessing information from its copy of the global section within the root. Notice, however, that the local sections (which are identical) cannot exchange data because their references are bound to different locations. Figure 11–17 illustrates the same duplicated library module, this time with the global data section forced to the root with the OVR attribute. Notice that the two local sections can now reference the same location in the global section to exchange information.

## Figure 11-16: Global Data Section with CON Attribute

[figure omitted]

Program MYPROG

Figure 11-17: Global Data Section with OVR Attribute

[figure omitted]

Duplicated library module MOD.
Local section B references section A,
which contains global data, but section
A does not reference section B.

[figure omitted]

## 11.6.5 Extend Program Section Option (/E:n)

The /E:n option allows you to extend a program section in the root to a specific value. Type the /E:n option at the end of the first command line. After you have typed all input command lines, the linker prompts with:

```txt
Extend section?
```

Respond with the name of the program section to be extended, followed by a carriage return. The resultant program section size is equal to or greater than the value you specify, depending on the space the object code requires. The value you specify must be an even byte value. Note that you can extend only one section.

The following example extends section CODE to 100 (octal) bytes.

\* X,TT:=LK001/E:100
Extend section? CODE

## 11.6.6 Default FORTRAN Library Option (/F)

By indicating the /F option in the command line, you can link the FORTRAN library (FORLIB.OBJ on the system device SY:) with the other object modules you specify. You do not need to specify FORLIB explicitly. For example:

\* FILE,LP:=AB/F

The object module AB.OBJ from DK: and the required routines from the FORTRAN library SY:FORLIB.OBJ are linked together to form a load module called FILE.SAV.

The linker automatically searches a default system library, SY:SYSLIB.OBJ. The library normally includes the modules that compose FORLIB. The /F option is provided only for compatibility with other versions of RT-11. You should not have to use /F.

See the RT-11 Installation Guide for details on combining SYSLIB and FORLIB library files.

## 11.6.7 Directory Buffer Size Option (/G)

When you are using modules for your program that are from a multiple definition library, LINK has to store that library's directory in an internal buffer. Occasionally, this buffer area is too small to contain an entire directory, in which case LINK is unable to process those modules. The /G option instructs LINK to adjust the size of its directory buffer to accommodate the largest directory size of the multiple definition libraries you are using.

You should use /G only when required because it slows down linking time. Use it only after an attempt to link your program failed because the buffer was too small. When a link failure of this sort occurs, LINK prints the message ?LINK-F-Library EPT too big, increase buffer with /G.

## 11.6.8 Highest Address Option (/H:n)

The /H:n option allows you to specify the top (highest) address to be used by the relocatable code in the load module. The argument n represents an unsigned, even octal number. If you do not specify n, the linker prints:

```txt
?LINK-F-/H no value
```

Retype the command, supplying an even octal number to be used as the value.

If you specify an odd value, the linker responds with:

?LINK-F-/H odd value

Retype the command, supplying an even octal number.

If the value is not large enough to accommodate the relocatable code, the linker prints:

```txt
?LINK-F-/H value too low
```

Relink the program with a larger value.

The /H option cannot be used with the /R, /Y, or /B options.

## NOTE

Be careful when you use the /H option. Most RT-11 programs use the free memory above the relocatable code as a dynamic working area for I/O buffers, device handlers, symbol tables, etc. The size of this area differs according to the memory configuration. Programs linked to a specific high address might not run in a system with less physical memory because there is less free memory.

## 11.6.9 Include Option (/I)

The /I option lets you take global symbols from any library and include them in the linking process even when they are not needed to resolve globals. This provides a method for forcing modules that are not called by other modules to be loaded from the library. All modules that you specify with /I go into the root. When you specify the /I option, the linker prints:

```txt
Library search?
```

Reply with the list of global symbols to be included in the load module; type a carriage return to enter each symbol in the list. A carriage return alone terminates the list of symbols.

The following example includes the global \$SHORT in the load module:

```txt
* SCCA=RK1:SCCA/I RET
Library search? $SHORT RET
Library search? RET
```

## 11.6.10 Memory Size Option (/K:n)

The /K:n option lets you insert a value into word 56 of block 0 of the image file. The argument n represents the number of 1K words of memory required by the program; n is an integer in the range 2–28 (decimal). This option allows you to limit the amount of memory allocated by a .SETTOP request to nK words. You cannot use the /K option with the /R option.

## 11.6.11 LDA Format Option (/L)

The /L option produces an output file in LDA format instead of memory image format. The LDA format file can be output to any device including those that are not block-replaceable. It is useful for files that are to be loaded with the absolute loader. The default file type .LDA is assigned when you use the /L option. You cannot use the /L option with the low memory overlay option (/O), the foreground link option (/R), or the extended memory overlay option (/V).

The following example links files IN and IN2 on device DK: and outputs an LDA format file, OUT.LDA, to the diskette and a load map to the line printer.

```txt
* DY:OUT,LP:=IN,IN2/L
```

## 11.6.12 Modify Stack Address Option (/M[:n])

The stack address, location 42, is the address that contains the initial value for the stack pointer. The /M option lets you specify the stack address. If you use the /R:n option (foreground link) with /M, LINK ignores the value on /R:n. The argument n is an even, unsigned, six-digit octal number that defines the stack address.

After all input lines have been typed, the linker prints the following message if you have not specified a value for n:

Stack symbol?

In this case, specify the global symbol whose value is the stack address and follow with a carriage return. You must not specify a number. If you specify a nonexistent symbol, an error message prints and the stack address is set to the system default (1000 for .SAV files) or to the bottom address if you used /B. If the program's absolute section extends beyond location 1000, the default stack space starts after the largest .ASECT allocation of memory.

Direct assignment (with .ASECT) of the stack address within the program takes precedence over assignment with the /M option. The statements to do this in a MACRO program are as follows:

```txt
.ASECT
.=42
.WORD INITSP          ;INITIAL STACK SYMBOL VALUE
.PSECT                  ;RETURN TO PREVIOUS SECTION
```

The following example modifies the stack address.

```txt
* OUTPUT=INPUT/M RET
Stack symbol? BEG RET
```

## 11.6.13 Cross-Reference Option (/N)

The /N option includes in the load map a cross-reference of all global symbols defined during the linking process. The global symbols are listed alphabetically. Each global symbol is followed by the names of the modules (also listed alphabetically) in which the symbol is defined or referenced. A pound sign (#) next to the module name indicates that the symbol is defined in that module. A plus sign (+) indicates that the module is from a library. The cross-reference section, if requested, begins on a new page at the end of the load map. See Figure 11–14 (and Table 11–9) for an illustration of a global cross-reference listing.

When you request a global symbol cross-reference listing with the /N option, LINK generates the temporary file DK:CREF.TMP.

If DK: is write-locked or if it contains insufficient free space for the temporary file, you can designate another device for the file. To designate another device for the temporary file, assign the logical name CF to the device by using the following command:

```txt
• ASSIGN dev: CF
```

If you have assigned CF to a physical device for MACRO cross-reference listing temporary file CREF.TMP, that device will also serve as the default device for the LINK global symbol cross-reference temporary file.

## 11.6.14 Low Memory Overlay Option (/O:n)

The /O option segments the load module so that the entire program is not memory resident at one time. This lets you execute programs that are larger than the available memory.

The argument n is an unsigned octal number (up to five digits in length) specifying the overlay region to which the module is assigned. The /O option must follow (on the same line) the specification of the object modules to which it applies, and only one overlay region can be specified on a command line. Overlay regions cannot be specified on the first command line; that is reserved for the root segment. You must use /C or // for continuation.

You specify coresident overlay routines (a group of subroutines that occupy the overlay region and segment at the same time) as follows:

```txt
* OBJA,OBJB,OBJC/0:1/C
* OBJD,OBJE/0:2/C
    :
    :
    :
```

All modules that the linker encounters until the next /O option will be coresident overlay routines. If you specify, at a later time, the /O option with the same value you used previously (same overlay region), then the linker opens up the corresponding overlay area for a new group of sub-routines. This group occupies the same locations in memory as the first group, but it is never needed at the same time as the previous group.

The following commands to the linker make R and S occupy the same memory as T (but at different times):

```csv
* MAIN,LP:=ROOT/C
* R,S/0:1/C
* T/0:1
```

The following example establishes two overlay regions.

```txt
* OUTPUT,LP:=INPUT//
* OBJA/0:1
* OBJB/0:1
* OBJC/0:2
* OBJD/0:2
* //
```

You must specify overlays in ascending order by region number. For example:

```txt
* A = A / C
* B / O : 1 / C
* C / O : 1 / C
* D / O : 1 / C
* G / O : 2
```

The following overlay specification is invalid since the overlay regions are not given in ascending numerical order. An error message prints in each case, and the overlay option immediately preceding the message is ignored.

```txt
* X=LIBRO//
* LIBR1/0:1
* LIBR2/0:0
?LINK-W-/0 or /V option error, re-enter line
*
```

In the above example, the overlay line immediately preceding the error message is ignored, and should be re-entered with an overlay region number greater than or equal to one.

## 11.6.15 Library List Size Option (/P:n)

The /P:n option lets you change the amount of space allocated for the library routine list. Normally, the default value allows enough space for your needs. It reserves space for approximately 170 unique library routines, which is the equivalent of specifying /P:170. (decimal) or /P:252 (octal). See the RT-11 Installation Guide for details on customizing this default number for the library routine list.

The error message ?LINK-F-Library list overflow, increase size with /P indicates that you need to allocate more space for the library routine list. You must relink the program that makes use of the library routines. Use the /P:n option and supply a value for n that is greater than 170 (decimal).

You can use the /P:n option to correct for symbol table overflow. Specify a value for n that is less than 170. This reduces the space used by the library routine list and increases the space allocated for the symbol table. If the value you choose is too small, the ?LINK-F-Library list overflow, increase size with /P message prints.

In the following command, the amount of space for the library routine list is increased to 300 (decimal).

\* SCCA=RK1:SCCA/P:300.

## 11.6.16 Absolute Base Address Option (/Q)

The /Q option lets you specify the absolute base addresses of up to eight psects in your program. This option is particularly handy if you are preparing your program sections in absolute loading format for placement in ROM storage.

When you use this option in the first command line, the linker prompts you for the p-sect names and load addresses. The p-sect name must be six characters or less, and the load address must be an even octal number. Terminate each line with a carriage return. If you enter only a carriage return in response to any of the prompts, LINK ceases prompting.

If you use /E, /Y, or /U with /Q, LINK processes those options before it processes /Q.

When you use the /Q option, observe the following restrictions:

\- Enter only even addresses. If you enter an odd address, no address, or invalid characters, LINK prints an error message and then prompts you again for the p-sect and load address.

\- /Q is invalid with /H or /R. These options are mutually exclusive.

\- LINK moves your p-sects up to the specified address; moving down might destroy code. If your address requires code to be moved down, LINK prints an error message, ignores the p-sect for which you have specified a load address, and continues.

The following example specifies the load addresses for three p-sects.

```txt
* FILE,TT:=FILE,FILE1/Q/L ⑧RET
Load Section:Address?    PSECT1:1000 ⑧RET
Load Section:Address?    PSECT3:4000 ⑧RET
Load Section:Address?    PSECT2:2500 ⑧RET
Load Section:Address?    ⑧RET
```

## 11.6.17 REL Format Option (/R[:n])

The /R[:n] option produces an output file in REL format for use as a foreground job with the FB or XM monitor. You cannot use .REL files under the SJ monitor. The /R option assigns the default file type .REL to the output file. The optional argument n represents the amount of stack space to allocate for the foreground job; it must be an even, octal number. The default value is 128 (decimal) bytes of stack space. If you also use the /M option, the value or global symbol associated with it overrides the /R value.

The following command links files FILEI.OBJ and NEXT.OBJ and stores the output on DY1: as FILEO.REL. It also prints a load map on the line printer.

\* DY1:FILEO,LP:=FILEI,NEXT/R:200

You cannot use the /B, /H, or /L option with /R since a foreground REL job has a temporary bottom address of 1000 and is always relocated by FRUN. An error message prints if you attempt this. The /K option is also invalid with /R.

## 11.6.18 Symbol Table Option (/S)

The /S option instructs the linker to allow the largest possible memory area for its symbol table at the expense of input and output buffer space. Because this makes the linking process slower, you should use the /S option only if an attempt to link a program failed because of symbol table overflow. When you use /S, do not specify a symbol table file or a map in the command string.

## 11.6.19 Transfer Address Option (/T[:n])

The transfer address is the address at which a program starts when you initiate execution with an R, RUN, SRUN (GET, START), or FRUN command. It prints on the last line of the load map. The /T option lets you specify the start address of the load module. The argument n is a six-digit unsigned, even octal number that defines the transfer address.

If you do not specify n the following message prints:

```txt
Transfer symbol?
```

In this case, specify the global symbol whose value is the transfer address of the load module. Terminate your response with a carriage return. You cannot specify a number in answer to this message. If you specify a nonexistent symbol, an error message prints and the transfer address is set to 1 so that the program traps immediately if you attempt to execute it. If the transfer address you specify is odd, the program does not start after loading and control returns to the monitor.

Direct assignment (.ASECT) of the transfer address within the program takes precedence over assignment with the /T option. The transfer address assigned with a /T option has precedence over that assigned with an .END assembly directive. To assign the transfer address within a MACRO program, use statements similar to these:

```asm
.ASECT
        .=40
        .WORD START1 ;SYMBOL VALUE FOR TRANSFER ADDRESS
        .PSECT ;RETURN TO PREVIOUS SECTION

START1: .
        .
        .
or
START2: .
        ;
        .
        .
        .END START2
```

The following example links the files LIBR0.OBJ and ODT.OBJ together and starts execution at ODT's transfer address.

```csv
* LBRODT,LBRODT=LIBRO,ODT/T/W//
* LIBR1/0:1
* LIBR2/0:1
* LIBR3/0:1
* LIBR4/0:1
* LIBR5/0:1
* LIBR6/0:1
* LBREM/0:1//
Transfer symbol? 0.0DT
*
```

## 11.6.20 Round Up Option (/U:n)

The /U:n option rounds up the section you name in the root so that the size of the root segment is a whole number multiple of the value you specify. The argument n must be a power of 2. When you specify the /U:n option, the linker prompts:

```txt
Round section?
```

Reply with the name of the program section to be rounded, followed by a carriage return. The program section must be in the root segment. Note that you can round only one program section.

The following example rounds up section CHAR.

```txt
* LK007,TT:=LK007/U:200
Round section? CHAR
```

If the program section you specify cannot be found, the linker prints ?LINK-W-Round section not found AAAAAA and the linking process continues with no rounding.

## 11.6.21 Extended Memory Overlay Option (/V:n[:m])

Use the /V option to create an extended memory overlay structure for your program. The variable n represents the overlay region number, and m represents a partition number. See Section 11.5.2 for a complete description of this option.

If you use /V on the first command line with no arguments, you enable special .SETTOP features provided by the XM monitor and special .LIMIT features. When used on the first line of the command string, this option allows virtual or privileged foreground or background jobs to map a work area in extended memory with the .SETTOP programmed request. Thus, your program does not need an extended memory overlay structure to make use of the XM .SETTOP features. See the RT-11 Programmer's Reference Manual and the RT-11 Software Support Manual for more details on these features and extended memory.

## 11.6.22 Map Width Option (/W)

The /W option directs the linker to produce a wide load map listing. If you do not specify the /W option, the listing is wide enough for three global value columns (normal for paper with 80-character columns). If you use the /W command, the listing is six columns wide, which is suitable for a 132-column page.

## 11.6.23 Bitmap Inhibit Option (/X)

The /X option instructs the linker not to output the bitmap if code lies in locations 360 to 377 inclusive. This option is provided for compatibility with the RSTS operating system. The bitmap is stored in locations 360–377 in block 0 of the load module, and the linker normally stores the program memory usage bits in these eight words. Each bit represents one 256-word block of memory. This information is required by the R, RUN, and GET commands when loading the program; therefore, use care when you use this option.

## 11.6.24 Boundary Option (/Y:n)

The /Y:n option starts a specific program section in the root on a particular address boundary. Do not use this option with /H. The linker generates a whole number multiple of n, the value you specify, for the starting address of the program section. The argument n must be a power of 2. The linker extends the size of the previous program section to accommodate the new starting address.

When you have entered all the input lines, the linker prompts:

```txt
Boundary section?
```

Respond with the name of the program section whose starting address you are modifying. Terminate your response with a carriage return. Note that you can specify only one program section for this option. If the program section you specify cannot be found, the linker prints ?LINK-W-Boundary section not found, and the linking process continues.

The RT-11 monitors have internal two-block overlays. The first overlay segment, OVLY0, must start on a disk block boundary:

\* RT11SJ.SYS=BTSJ,RMSJ,KMSJ,TBSJ/Y:1000
Boundary Section? OVLYO

## 11.6.25 Zero Option (/Z:n)

The /Z:n option fills unused locations in the load module and places a specific value in these locations. The argument n represents that value. This option can be useful in eliminating random results that occur when the program references uninitialized memory by mistake. The system automatically zeroes unused locations. Use the /Z:n option only when you want to store a value other than zero in unused locations. You cannot use the R, RUN, FRUN, or GET commands to load into memory a load image block of fill characters.

## 11.7 Linker Prompts

Some of the linker operations prompt for more information, such as the names of specific global symbols or sections. The linker issues the prompt after you have entered all the input specifications, but before the actual linking begins. Table 11–10 shows the sequence in which the prompts occur.

Table 11-10: Linker Prompting Sequence

| Prompt | Option |
| --- | --- |
| Transfer symbol? | /T |
| Stack symbol? | /M |
| Extend section? | /E:n |
| Boundary section? | /Y:n |
| Round section? | /U:n |
| Load section:address? | /Q |
| Library search? | /I |
| Duplicate symbol? | /D |

The library search, load section, and duplicate symbol prompts can accept more than one symbol and are terminated by a carriage return in response to the prompt.

Note that if the command lines are in an indirect file and the linker encounters an end-of-file before the prompting information has been supplied, the linker prints the prompt messages on the terminal.

The following example shows how the linker prompts for information when you combine options.

```shell
* LK001=LK001/T/M/E:100/Y:400/U:20/I/Q/D RET
Transfer symbol? 0.0DT RET
Stack symbol? ST3 RET
Extend section? CHAR RET
Boundary section? CODE RET
Round section? STKSP RET
Load section:address? MAIN:100000 RET
Load section:address? RET
Library search? $SHORT RET
Library search? RET
Duplicate symbol? RTN RET
Duplicate symbol? RET
*
```

， }
