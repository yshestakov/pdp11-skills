# RT-11 System Utilities Manual: Ch.10 LIBR librarian: object and macro libraries, create/insert/replace/delete/list

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 10.1 Calling and Terminating LIBR
- 10.2 LIBR Command String Syntax
- 10.2.1 Creating a Library File
- 10.2.2 Inserting Modules into a Library
- 10.2.3 Merging Library Files
- 10.3 Option Commands and Functions for Object Libraries
- 10.3.1 Include All Global and Absolute Global Symbols Option (/A)
- 10.3.2 Command Continuation Options (/C Or //)
- 10.3.3 Delete Option (/D)
- 10.3.4 Extract Option (/E)
- 10.3.5 Delete Global Option (/G)
- 10.3.6 Include Module Names Option (/N)
- 10.3.7 Include P-Section Names Option (/P)
- 10.3.8 Replace Option (/R)
- 10.3.9 Update Option (/U)
- 10.3.10 Wide Option (/W)
- 10.3.11 Creating Multiple Definition Libraries Option (/X)
- 10.3.12 Listing the Directory of a Library File
- 10.3.13 Combining Library Option Functions
- 10.4 Option Commands and Functions for Macro Libraries
- 10.4.1 Command Continuation Options (/C or //)
- 10.4.2 Macro Option (/M[:n])

---

## Chapter 10 Librarian (LIBR)

The librarian utility program (LIBR) lets you create, update, modify, list, and maintain object library files. It also lets you create macro library files to use with the V03 and later versions of the MACRO-11 assembler.

A library file is a direct access file (a file that has a directory) that contains one or more modules of the same module type. The librarian organizes the library files so that the linker and MACRO-11 assembler can access them rapidly. Each library contains a library header, library directory (or global symbol table, or macro name table), and one or more object modules, or macro definitions. The object modules in a library file can be routines that are repeatedly used in a program, routines that are used by more than one program, or routines that are related and simply gathered together for convenience. The contents of the library file are determined by your needs. An example of a typical object library file is the default system library that the linker uses, SYSLIB.OBJ. An example of a macro library file is SYSMAC.SML, which MACRO uses to process programmed requests.

You access object modules in a library file from another program by making calls or references to their global symbols; you then link the object modules with the program that uses them, producing a single load module (see Chapter 11).

Consult the RT-11 Software Support Manual for more information on the internal data structure of a library file.

## 10.1 Calling and Terminating LIBR

To call the RT-11 librarian from the system device, respond to the dot (.) printed by the keyboard monitor by typing:

• R LIBR RET

The Command String Interpreter (CSI) prints an asterisk at the left margin of the console terminal when it is ready to accept a command line.

Type two CTRL/Cs to halt the librarian at any time (or a single CTRL/C to halt the librarian when it is waiting for console terminal input) and return control to the monitor. To restart the librarian, type R LIBR or REENTER in response to the monitor's dot.

## 10.2 LIBR Command String Syntax

Chapter 1, Command String Interpreter, describes the general syntax of the command line LIBR accepts.

Specify the LIBR command string in the following general format:

library-filespec[n],list-filespec[n] = input-filespecs/option

where:

library-filespec[n] represents the library file to be created or updated. The optional argument n represents the number of blocks to allocate for the output file.

list-filespec[n] represents a listing file for the library's contents. The optional argument n represents the number of blocks to allocate for the listing file.

input-filespecs represents the input object modules (you can specify up to six input files); it can also represent a library file to be updated.

option represents an option from Table 10-1.

You specify devices and file names in the standard RT-11 command string syntax, with default file types for object libraries assigned as follows:

| Object File | Default File Type |
| --- | --- |
| List file | .LST |
| Library output file | .OBJ |
| Input file (library or module) | .OBJ |

If you do not specify a device, the default device (DK:) is assumed.

Each input file consists of one or more object modules and is stored on a given device under a specific file name and file type. Once you insert an object module into a library file, you no longer reference the module by the name of the file of which it was a part; instead you reference it by its individual module name. You assign this module name with the assembler with either a .TITLE statement in the assembly source program, or with the default name .MAIN. in the absence of a .TITLE statement or the subprogram name for FORTRAN routines. Thus, for example, the input file FORT.OBJ can exist on DY1: and can contain an object module called ABC. Once you insert the module into a library file, reference only ABC (not FORT.OBJ).

The input files normally do not contain main programs but rather subprograms, functions, and subroutines. The library file must never contain a FORTRAN BLOCK DATA subprogram because there is no undefined global symbol to cause the linker to load it automatically.

This section and Section 10.3 explain how to use the librarian to create and maintain object libraries; Section 10.4 describes how to create macro libraries.

## 10.2.1 Creating a Library File

To create a library file, specify a file name on the output side of a command line.

The following example creates a new library called NEWLIB.OBJ on the default device (DK:). The modules that make up this library file are in the files FIRST.OBJ and SECOND.OBJ, both on the default device.

\* NEWLIB=FIRST,SECOND

## 10.2.2 Inserting Modules into a Library

Whenever you specify an input file without specifying an associated option, the librarian inserts the input file's modules into the library file you name on the output side of the command string. You can specify any number of input files.

If you include section names (by using /P) in the global symbol table and if you attempt to insert a file that contains a global symbol or PSECT (or CSECT) having the same name as a global symbol or PSECT already existing in the library file, the librarian prints a warning message (see Section 10.3.11 for multiple definition library creation). The librarian does, however, update the library file, ignore the global symbol or section name in error, and return control to the CSI. You can then enter another command string.

Although you can insert object modules that exist under the same name (as assigned by the .TITLE statement), this practice is not recommended because of possible confusion when you need to update these modules (Sections 10.3.8 and 10.3.9 describe replacing and updating).

## NOTE

The librarian performs module insertion, replacement, deletion, merge, and update when creating the library file. Therefore, you must indicate the library file to which the operation is directed on both the input and output sides of the command line, since effectively the librarian creates a new output library file each time it performs one of these operations. You must specify the library file first in the input field.

The following command line inserts the modules included in the files FA.OBJ, FB.OBJ, and FC.OBJ on DY1: into a library file named DXY-NEW.OBJ on the default device. The resulting library also includes the contents of library DXY.OBJ.

\* DXYNEW=DXY, DY1:FA, FB, FC

The next command line inserts the modules contained in files THIRD.OBJ and FOURTH.OBJ into the library NEWLIB.OBJ.

```csv
* NEWLIB,LIST=NEWLIB,THIRD,FOURTH
```

Note that the resulting library contains the original library plus some new modules, and replaces the original library because the same name was used in this example for the input and output library.

## 10.2.3 Merging Library Files

You can merge two or more library files under one file name by specifying in a single command line all the library files to be merged. The librarian does not delete the individual library files following the merge unless the output file name is identical to one of the input file names.

The command syntax is as follows:

library-filespec = input-filespecs

where:

library-filespec

represents the library file that will contain all the merged files. (If a library file already exists under this name, you must also indicate it in the input side of the command line so that it is included in the merge.)

input-filespec represents library files to be merged.

Thus, the following command combines library files MAIN.OBJ, TRIG.OBJ, STP.OBJ, and BAC.OBJ under the existing library file name MAIN.OBJ; all files are on the default device DK:. Note that this replaces the old contents of MAIN.OBJ.

\* MAIN=MAIN,TRIG,STP,BAC

The next command creates a library file named FORT.OBJ and merges existing library files A.OBJ, B.OBJ, and C.OBJ under the file name FORT.OBJ.

\* FORT=A,B,C

## NOTE

Library files that you combine using PIP are invalid as input to both the librarian and the linker.

## 10.3 Option Commands and Functions for Object Libraries

You maintain object library files by using option commands. Functions that you can perform include object module deletion, insertion, replacement, and listing of an object library file's contents.

Table 10-1 summarizes the options available for you to use with RT-11 LIBR for object libraries and tells on which command line you must use each option. The following sections, which are arranged alphabetically by option, describe the options in greater detail.

Table 10-1: LIBR Object Options

| Option | Command Line | Section | Function |
| --- | --- | --- | --- |
| /A | First | 10.3.1 | Puts all globals in the directory, including all absolute global symbols. |
| /C | Any but last | 10.3.2 | Command continuation; allows you to type the input specification on more than one line. |
| /D | First | 10.3.3 | Delete; deletes modules that you specify from a library file. |
| /E | First | 10.3.4 | Extract; extracts a module from a library and stores it in an OBJ file. |
| /G | First | 10.3.5 | Global deletion; deletes global symbols that you specify from the library directory. |
| /M[:n] | First | 10.4.2 | Creates a macro library. |
| /N | First | 10.3.6 | Names; includes the module names in the directory. |
| /P | First | 10.3.7 | P-sect names; includes the program section names in the directory. |
| /R | First | 10.3.8 | Replace; replaces modules in a library file. This option must follow the file specification to which it applies. |
| /U | First | 10.3.9 | Update; inserts and replaces modules in a library file. This option must follow the file specification to which it applies. |
| /W | First | 10.3.10 | Indicates a wide format for the listing file. |
| /X | First | 10.3.11 | Allows multiple definitions of global entry points to appear in the library entry point table. |
| // | First and last | 10.3.2 | Command continuation; allows you to type the input specification on more than one line. |

There is no option to indicate module insertion. If you do not specify an option, the librarian automatically inserts modules into the library file.

## 10.3.1 Include All Global and Absolute Global Symbols Option (/A)

Use the /A option when you want all the global symbols to appear in the library file's directory. When you use /A, the librarian includes in the directory all absolute global symbols, including those that have a value of 0.

Normally, the librarian includes in the directory only global entry points (labels), and not absolute global symbols.

The following example places all the global symbols from modules MOD1 and MOD2 in the library directory for ALIB.OBJ.

```javascript
* ALIB=MOD1,MOD2/A
```

## 10.3.2 Command Continuation Options (/C Or //)

You must use a continuation option whenever there is not enough room to enter a command string on one line. The maximum number of input files that you can enter on one line is six; you can use the /C option or the // option to enter more.

Type the /C option at the end of the current line and repeat it at the end of subsequent command lines as often as necessary, so long as memory is available; if you exceed memory, an error message prints. Each continuation line after the first command line can contain only input file specifications (and no other options). Do not specify a /C option on the last line of input. If you use the // option, type it at the end of the first input line and again at the end of the last input line.

The following example creates a library file on the default device (DK:) under the file name ALIB.OBJ; it also creates a listing of the library file's contents as LIBLST.LST (also on the default device). The file names of the input modules are MAIN.OBJ, TEST.OBJ, FXN.OBJ, and TRACK.OBJ, all from DY1:.

```csv
* ALIB,LIBLST=DY1:MAIN,TEST,FXN/C
* DY1:TRACK
```

The next example creates a library file on the default device (DK:) under the name BLIB.OBJ. It does not produce a listing. Input files are MAIN.OBJ from the default device, TEST.OBJ from DL1:, FXN.OBJ from DL0:, and TRACK.OBJ from DY1:.

```c
* BLIB=MAIN//  
* DL1:TEST  
* DLO:FXN  
* DY1:TRACK//
```

Another way of writing this command line is:

```txt
* BLIB=MAIN,DL1:TEST,DLO:FXN//
* DY1:TRACK
* //
```

## 10.3.3 Delete Option (/D)

The /D option deletes modules and all their associated global symbols from a library file's directory. Since modules are deleted only from the directory (and not from the object module itself), all modules that were previously deleted are restored whenever you update that library, unless you use /D again to delete them.

When you use the /D option, the librarian prompts:

```txt
Module name?
```

Respond with the name of the module to be deleted, followed by a carriage return. Continue until you have entered all modules to be deleted. Type a carriage return immediately after the Module name? message to terminate input and initiate execution of the command line.

The following example deletes the modules SGN and TAN from the library file TRAP.OBJ on DY1:.

```ruby
* DY1:TRAP=DY1:TRAP/D
Module name? SGN
Module name? TAN
Module name?
```

The next example deletes the module FIRST from the library LIBFIL.OBJ; all modules in the file ABC.OBJ replace old modules of the same name in the library. It also inserts the modules in the file DEF.OBJ into the library.

```txt
* LIBFIL=LIBFIL/D,ABC/R,DEF
Module name? FIRST
Module name?
```

In the following example, the librarian deletes two modules of the same name from the library file LIBFIL.OBJ.

```txt
* LIBFIL=LIBFIL/D
Module name? X
Module name? X
Module name?
```

## 10.3.4 Extract Option (/E)

The /E option allows you to extract an object module from a library file and place it in an .OBJ file.

When you specify the /E option, the librarian prints:

```txt
Global?
```

Respond with the name of the object module you want to extract. If you specify a global name, the librarian extracts the entire module of which that global is a part. Type a carriage return to terminate the prompting for a global.

You cannot use the /E option on the same command line as another option.

The following example extracts the ATAN routine from the FORTRAN library, SYSLIB.OBJ, and stores it in a file called ATAN.OBJ on DX1:.

```txt
* DX1:ATAN=SYSLIB/E
Global? ATAN
Global?
```

The next example extracts the \$PRINT routine from SYSLIB.OBJ and stores it on DM1: as PRINT.OBJ.

```txt
* DM1:PRINT=SYSLIB/E
Global? $PRINT
Global?
```

## 10.3.5 Delete Global Option (/G)

The /G option lets you delete specific global symbols from a library file's directory.

When you use the /G option, the librarian prints:

```txt
Global?
```

Respond with the name of the global symbol you want to delete followed by a carriage return; continue until you have entered all globals to be deleted. Type a carriage return immediately after the Global? message to terminate input and initiate execution of the command line.

The following command instructs LIBR to delete the global symbols NAMEA and NAMEB from the directory found in the library file ROLL.OBJ on DK:.

```txt
* ROLL=ROLL/G
Global? NAMEA
Global? NAMEB
Global?
```

The librarian deletes globals only from the directory (and not from the library itself). Whenever you update a library file, all globals that you previously deleted are restored unless you use the /G option again to delete them. This feature lets you recover if you delete the wrong global.

## 10.3.6 Include Module Names Option (/N)

When you use the /N option on the first line of the command, the librarian includes module names in the directory. The linker loads modules from libraries based on undefined globals, not on module names. The linker also provides equivalent functions by using global symbols and not module names. Normally, then, it is a waste of space and a performance compromise to include module names in the directory.

If you do not include module names in the directory, the MODULE column of the directory listing is blank, unless the module requires a continuation line to print all its globals. A plus (+) sign in the MODULE column indicates continued lines. The /N option is useful mainly when you create a temporary library in order to obtain a directory listing.

If the library does not have module names in its directory, you must create a new library to include the module names. The following example illustrates how to do this. It creates a temporary new library from the current library (by specifying the null device for output) and lists its directory on the terminal. The current library OLDLIB remains unchanged.

<table><tr><td colspan="4">* NL:TEMP,TT:=OLDLIB/N</td></tr><tr><td>RT-11 LIBRARIAN V05.00</td><td colspan="3">WED 02-MAR-83 20:36:41</td></tr><tr><td>NL:TEMP.OBJ</td><td colspan="3">TUE 02-MAR-83 20:36:40</td></tr><tr><td>MODULE</td><td>GLOBALS</td><td>GLOBALS</td><td>GLOBALS</td></tr><tr><td>IRAD50</td><td>IRAD50</td><td>RAD50</td><td></td></tr><tr><td>JMUL</td><td>JMUL</td><td></td><td></td></tr><tr><td>LEN</td><td>LEN</td><td></td><td></td></tr><tr><td>SUBSTR</td><td>SUBSTR</td><td></td><td></td></tr><tr><td>JADD</td><td>JADD</td><td></td><td></td></tr><tr><td>JCMP</td><td>JCMP</td><td></td><td></td></tr></table>

## 10.3.7 Include P-Section Names Option (/P)

The librarian does not include program section names in the directory unless you use the /P option on the first line of the command. The linker does not use section names to load routines from libraries — in fact, including the names can decrease linker performance. Including program section names also causes a conflict in the library directory and subsequent searches, since the librarian treats section names and global symbols identically.

This option is provided for compatibility with RT-11 V2C. DIGITAL recommends that you avoid using it with later versions of RT-11.

## 10.3.8 Replace Option (/R)

Use the /R option to replace modules in a library file. The /R option replaces existing modules in the library file you specify as output with the modules of the same names contained in the file(s) you specify as input. In the command string, enter the input library file before the files used in the replacement operation.

If an old module does not exist under the same name as an input module, or if you specify the /R option on a library file, the librarian prints an error message followed by the module name and ignores the replace command.

The /R option must follow each input file name containing modules for replacement.

The following command line indicates that the modules in the file INB.OBJ are to replace existing modules of the same names in the library file TFIL.OBJ. The object modules in the files INA.OBJ and INC.OBJ are to be added to TFIL. All files are stored on the default device DK:.

```csv
* TFIL=TFIL,INA,INB/R,INC
```

The same operation occurs in the next command as in the preceding example, except that this updated library file is assigned the new name XFIL.

```csv
* XFIL=TFIL,INA,INB/R,INC
```

## 10.3.9 Update Option (/U)

The /U option lets you update a library file by combining the insert and replace functions. If the object modules that compose an input file in the command line already exist in the library file, the librarian replaces the old modules in the library file with the new modules in the input file. If the object modules do not already exist in the library file, the librarian inserts those modules into the library. (Note that some of the error messages that might occur with separate insert and replace functions do not print when you use the update function.)

/U must follow each input file that contains modules to be updated. Specify the input library file before the input files in the command line.

The following command line instructs the librarian to update the library file BALIB.OBJ on the default device. First the modules in FOLT.OBJ and BART.OBJ replace old modules of the same names in the library file, or if none already exist under the same names, the modules are inserted. The modules from the file TAL.OBJ are then inserted; an error message prints if the name of a module in TAL.OBJ already exists.

\* BALIB=BALIB,FOLT/U,TAL,BART/U

In the next example, there are two object modules of the same name, X, in both Z and XLIB; these are first deleted from XLIB so that both the modules called X in file Z are correctly placed in the library. Globals SEC1 and SEC2 are also deleted from the directory but automatically return the next time the library XLIB.OBJ is updated.

```txt
* XLIB=XLIB/D,Z/U/G
Module name? X
Module name? X
Module name?
Global? SEC1
Global? SEC2
Global?
```

## 10.3.10 Wide Option (/W)

The /W option gives you a wider listing if you request a listing file. The wider listing has six global columns instead of three, as in the normal listing. This is useful if you list the directory on a line printer or a terminal that has 132 columns.

## 10.3.11 Creating Multiple Definition Libraries Option (/X)

The /X option lets you create libraries that can have more than one definition for a global entry point. These libraries are called multiple definition libraries. They are processed differently from libraries that contain only one definition for each global entry point name that appears in the library's directory (for more information on processing multiple definition libraries, see Chapter 11).

In multiple definition libraries, two library modules may use the same global entry point name, and both definitions may appear in the entry point table (EPT). At least one entry point name should be unique in each module so that you can easily identify it.

When you use the /X option, the librarian does not issue the ?LIBR-W-Invalid insert of AAAAAA message when it encounters a duplicate global symbol name, and the global name will appear in the directory for each module that defines it. In addition, the /X option causes the librarian to turn on the /N option (see Section 10.3.6).

The following example creates the multiple definition library MLTLIB from modules MOD1, MOD2, and MOD3, and lists the library on the terminal. Since MOD3 contains only absolute global symbols, this example must also use the /A option.

\*MLTLIB,TT:=MOD1,MOD2,MOD3/X/A

RT-11 LIBRARIAN V05.00 THU 11-NOV-82 09:45:31
DK:MLTLIB.OBJ THU 11-NOV-82 09:45:31

| MODULE | GLOBALS | GLOBALS | GLOBALS |
| --- | --- | --- | --- |
| MOD1 | OMA$R | SWP$ | ATP$ |
| MOD2 | ATP$ | OMA$R | MER$CR |
|  | LBM |  |  |
| MOD3 | ATP$ | OMA$R | MER$CR |
|  | ENTZ |  |  |

## 10.3.12 Listing the Directory of a Library File

You can request a listing of the contents of a library file (the global symbol table) by indicating both the library file and a list file in the command line. Since a library file is not being created or updated, you do not need to indicate the file name on the output side of the command line; however, you must use a comma to designate a null output library file.

The command syntax is as follows:

```makefile
,LP:=library-filespec
```

or

```txt
,list-filespec = library-filespec
```

where:

| library-filespec | represents the existing library file |
| --- | --- |
| LP: | indicates that the listing is to be sent directly to the line printer (or terminal, if you use TT:) |
| list-filespec | represents a list file of the library file's contents |

The following command outputs to DY1: as LIST.LST a listing of all modules in the library file LIBFIL.OBJ, which is stored on the default device.

```c
* ,DY1:LIST=LIBFIL
```

The next command sends to the line printer a listing of all modules in the library file FLIB.OBJ, which is stored on the default device.

```txt
* ,LP:=FLIB
```

Here is a sample section of a large directory listing:

```txt
* ,TT:=SYSLIB
RT-11 LIBRARIAN V05.00 TUE 02-NOV-82 21:01:01
DK:SYSLIB.OBJ TUE 02-NOV-82 20:59:47
```

| MODULE | GLOBALS | GLOBALS | GLOBALS |
| --- | --- | --- | --- |
|  | DCO$ | ECO$ | FCO$ |
| + | GCO$ | RCI$ |  |
|  | DIC$IS | DIC$MS | DIC$PS |
| + | DIC$SS | $DIVC | $DVC |
|  | ADD$IS | ADD$MS | ADD$PS |
| + | ADD$SS | SUD$IS | SUD$MS |
| + | SUD$PS | SUD$SS | $ADD |

The first line of the listing file shows the version of the librarian that was used and the current date and time. The second line prints the library file name and the date and time the library was created. Each line in the rest of the listing shows only the globals that appear in a particular module. If a module contains more global symbol names than can print on one line, a new line will be started with a plus (+) sign in column 1 to indicate continuation.

If you request a listing of a library file that was created with the /X or /N option, the listing includes module names under the MODULE heading.

## 10.3.13 Combining Library Option Functions

You can specify two or more library functions in the same command line, with the exception of the /E and /M options, which cannot be specified on the same command line with any other option. The librarian performs functions (and issues appropriate prompts) in the following order:

```txt
1. /C or //
2. /D
3. /G
4. /U
5. /R
6. Insertions
7. Listing
```

Here is an example that combines options:

```txt
* FILE,LP:=FILE/D,MODX,MODY/R
Module name? XYZ
Module name? A
Module name?
```

The librarian performs the functions in this example in the following order:

1. Deletes modules XYZ and A from the library file FILE.OBJ.

2. Replaces any duplicate of the modules in the file MODY.OBJ.

3. Inserts the modules in the file MODX.OBJ.

4. Lists the directory of FILE.OBJ on the line printer.

## 10.4 Option Commands and Functions for Macro Libraries

The librarian lets you create macro libraries. A macro library works with the V03 or later MACRO-11 assembler to reduce macro search time.

The .MACRO directive produces the entries in the library directory (macro names). LIBR does not maintain a directory listing file for macro libraries; you can print the ASCII input file to list the macros in the library.

The default input file type for macro files is .MAC. The default output file type for macro library files is .MLB.

If you give the library file the same name as one of the input files, the librarian prints the error message: ?LIBR-F-Output and input filnames the same.

The librarian removes all comments from your source input file except for those within a macro (that is, between a .MACRO and .ENDM pair of directives). Because comments take up space during the assembly and in the library, remove them from the macros wherever possible before creating a macro library, if saving space and shortening assembly time are important to you.

Table 10-2 summarizes the options you can use with macro libraries.

The options are explained in detail in the following two sections.

Table 10-2: LIBR Macro Options

| Option | Command Line | Section | Meaning |
| --- | --- | --- | --- |
| /C | Any but last | 10.4.1 | Command continuation; allows you to type the input specification on more than one line. |
| /M[:n] | First | 10.4.2 | Macro; creates a macro library from the ASCII input file containing .MACRO directives. |
| // | First and last | 10.4.1 | Command continuation; allows you to type the input specification on more than one line. |

## 10.4.1 Command Continuation Options (/C or //)

These options are the same for macro libraries as for object libraries. See Section 10.3.2.

## 10.4.2 Macro Option (/M[:n])

The /M[:n] option creates a macro library file from an ASCII input file that contains .MACRO directives. The optional argument n determines the amount of space to allocate for the macro name directory by representing the number of macros you want the directory to hold. Remember that n is interpreted as an octal number; you must follow n with a decimal point (n.) to indicate a decimal number. One block of library directory space holds 64 macros. The default value for n is 128, enough space for 128 macros, which will use 2 blocks for the macro name table.

The command syntax is as follows:

$$
\text {library - filespec} = \text {input - filespec / M[:n]}
$$

where:

library-filespec represents the macro library to be created

input-filespec represents the ASCII input file that contains .MACRO definitions

The continuation options (/C or //) are the only options you can use with the macro option.

The following example creates the macro library SYSMAC.SML from the ASCII input file SYSMAC.MAC. Both files are on device DK:.

\* SYSMAC.SML=SYSMAC/M
