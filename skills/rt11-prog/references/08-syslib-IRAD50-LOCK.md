# RT-11 PRM reference: Ch.3 SYSLIB subroutines 3.44 through 3.79

Source: RT-11 Programmer's Reference Manual AA-H378C-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' sometimes reads as ',' (`,MCALL` = `.MCALL`), 'R0' as 'RO', '#' as '\*' or '*'. Verify exact macro expansions against `sysmac_v53.mac`.

Contents:
- 3.44 IRCVD/IRCVDC/IRCVDF/IRCVDW (FB and XM Only)
- 3.45 IREAD/IREADC/IREADF/IREADW
- 3.46 IRENAM
- 3.47 IREOPN
- 3.48 ISAVES
- 3.49 ISCHED
- 3.50 ISCOMP
- 3.51 ISDAT/ISDATC/ISDATF/ISDATW (FB and XM Only)
- 3.52 ISDTTM
- 3.53 ISFDAT
- 3.54 ISLEEP
- 3.55 ISPFN/ISPFNC/ISPFNF/ISPFNW
- 3.56 ISPY
- 3.57 ITIMER
- 3.58 ITLOCK (FB and XM Only)
- 3.59 ITTINR
- 3.60 ITTOUR
- 3.61 ITWAIT (SYSGEN Option in SJ)
- 3.62 IUNTIL (SYSGEN Option in SJ)
- 3.63 IVERIF
- 3.64 IWAIT
- 3.65 IWRITE/IWRITC/IWRITF/IWRITW
- 3.66 JADD
- 3.67 JAFIX
- 3.68 JCMP
- 3.69 JDFIX
- 3.70 JDIV
- 3.71 JICVT
- 3.72 JJCVT
- 3.73 JMOV
- 3.74 JMUL
- 3.75 JSUB
- 3.76 JTIME
- 3.77 LEN
- 3.78 LOCK
- 3.79 LOOKUP

---

## 3.44 IRCVD/IRCVDC/IRCVDF/IRCVDW (FB and XM Only)

There are four forms of the receive data function; these are used in conjunction with the ISDAT (send data) functions to allow a general data/message transfer system. The receive data functions issue RT-11 receive data programmed requests (see Section 2.70). These functions require a queue element; this should be considered when the IQSET function (Section 3.42) is executed.

## IRCVD

The IRCVD function receives data and continues execution. The operation is queued and the issuing job continues execution. When the job has to receive the transmitted message, an MWAIT should be executed. This causes the job to be suspended until all pending messages have been received.

```txt
Form: i = IRCVD (buff, wcnt)
```

## where:

buff is the array to be used to buffer the data received. The array must be one word larger than the message to be received because the first word contains the integer number of words actually transmitted when IRCVD is complete

wcnt is the maximum integer number of words that can be received

## Errors:

```txt
i = 0 Normal return.
```

= 1 No such job exists in the system. (A job exists as long as it is loaded, whether or not it is active.)

## Example:

```txt
INTEGER*2 MSG(41)
.
.
.
CALL IRCVD(MSG,40)
.
.
.
CALL MWAIT
```

## IRCVDC

The IRCVDC function receives data and enters an assembly language completion routine when the message is received. The IRCVDC is queued, and program execution stays with the issuing job. When the other job sends a message, the completion routine specified is queued and run according to standard scheduling of completion routines.

Form: i = IRCVDC (buff,wcnt,crtn)

## where:

buff is the array to be used to buffer the data received. The array must be one word larger than the message to be received because the first word contains the integer number of words actually transmitted when IRCVDC is complete

wcnt is the maximum integer number of words to be received

crtn is the assembly language completion routine to be entered. This name must be specified in a FORTRAN EXTERNAL statement in the routine that issues the IRCVDC call

## Errors:

i = 0 Normal return.

= 1 No such job exists in the system. (A job exists as long as it is loaded, whether or not it is active.)

## IRCVDF

The IRCVDF function receives data and enters a FORTRAN completion subroutine when the message is received. The IRCVDF is queued, and program execution continues with the issuing job. When the other job sends a message, the FORTRAN completion routine specified is entered.

Form: i = IRCVDF (buff,wcnt,area,crtn)

## where:

buff is the array to be used to buffer the data received. The array must be one word larger than the message to be received because the first word contains the integer number of words actually transmitted when IRCVDF is complete

wcnt is the maximum integer number of words to be received

area is a four-word area to be set aside for linkage information. This area must not be modified by the FORTRAN program and the USR must not swap over it. This area can be reclaimed by other FORTRAN completion routines when crtn has been entered

crtn is the FORTRAN completion routine to be entered. This name must be specified in an EXTERNAL statement in the FORTRAN routine that issues the IRCVDF call

## Errors:

i = 0 Normal return.

= 1 No such job exists in the system. (A job exists as long as it is loaded, whether or not it is active.)

## Example:

```txt
INTEGER*2 MSG(41),AREA(4)
EXTERNAL RMSGRT
.
.
.
CALL IRCVDF(MSG,40,AREA,RMSGRT)
```

## IRCVDW

The IRCVDW function receives data and waits. This function queues a message request and suspends the job issuing the request until the other job sends a message. When execution of the issuing job resumes, the message has been received, and the first word of the buffer indicates the number of words transmitted.

Form: i = IRCVDW (buff,wcnt)

where:

buff is the array to be used to buffer the data received. The array must be one word larger than the message to be received because the first word contains the integer number of words actually transmitted when IRCVDW is complete

wcnt is the maximum integer number of words to be received

Errors:

i = 0 Normal return.

= 1 No such job exists in the system. (A job exists as long as it is loaded, whether or not it is active.)

Example:

```txt
INTEGER*2 MSG(41)
IF(IRCVDW(MSG,40),NE,0) STOP 'UNEXPECTED ERROR'
```

## 3.45 IREAD/IREADC/IREADF/IREADW

The functions IREAD, IREADC, IREADF, and IREADW transfer a specified number of words from a file into memory. These functions require a queue element, which should be considered when the IQSET function (Section 3.42) is executed.

IREAD

The IREAD function transfers into memory a specified number of words from the file associated with the indicated channel. Control returns to the user program immediately after the IREAD function is initiated. No special action is taken when the transfer is completed.

Form: i = IREAD (wcnt,buff,blk,chan)

where:

wcnt is the relative integer number of words to be transferred

buff      is the array to be used as the buffer; this array must contain
at least wcnt words

blk is the integer block number of the file to be read. The first block of a file is block number 0. The blk argument must be updated when necessary. For example, if the program is reading two blocks at a time, blk should be updated by 2

chan is the integer specification for the RT-11 channel to be used

When the user program needs to access the data read on the specified channel, an IWAIT function should be issued. This makes sure that the

IREAD operation has been completed. If an error occurred during the transfer, the IWAIT function indicates the error.

## Errors:

i = n    Normal return; n equals the number of words requested (0 for non-file-structured read, multiple of 256[decimal] for file-structured read). If the read is from a magtape, the number of words requested is returned. For example:

If $wcnt$ is a multiple of 256 and less than that number of words remain in the file, $n$ is shortened to the number of words that remain in the file; thus, if $wcnt$ is 512 and only 256 words remain, $i = 256$.

If $wcnt$ is not a multiple of 256 and more than $wcnt$ words remain in the file, $n$ is rounded up to the next block; thus, if $wcnt$ is 312 and more than 312 words remain, $i = 512$, but only 312 are read.

If $wcnt$ is not a multiple of 256 and less than $wcnt$ words remain in the file, $n$ equals a multiple of 256 that is the actual number of words being read.

= -1 Attempt to read past end-of-file; no words remain in the file.

= -2 Hardware error occurred on channel.

= -3 Specified channel is not open.

## NOTE

If an asynchronous operation on a channel (for example, IREAD) results in end-of-file, the following IWAIT will not detect it. IWAIT detects only hard error conditions. A subsequent operation on that channel will detect end-of-file and returns to the user with the end-of-file error code. Under these conditions, the subsequent operation is not initiated.

## Example:

INTEGER\*2 BUFFER(25G),RCODE,BLK
:
:
RCODE = IREAD(25G,BUFFER,BLK,ICHAN)
IF(RCODE+1) 1010,1000,10
C     IF NO ERROR, START HERE
10    (
      (
      IF(IWAIT(ICHAN).NE.0) GOTO 1010
      (
      (
      (
1000 CONTINUE
C     END OF FILE PROCESSING
      (
      (
      CALL EXIT          !NORMAL END OF PROGRAM
1010 STOP 'FATAL READ'
      END

## IREADC

The IREADC function transfers a specified number of words from the indicated channel into memory. Control returns to the user program immediately after the IREADC function is initiated. When the operation is complete, the specified assembly language routine (crtn) is entered as an asynchronous completion routine.

Form: i = IREADC (wcnt,buff,blk,chan,crtn)

## where:

wcnt is the integer number of words to be transferred

buff      is the array to be used as the buffer; this array must contain
at least wcnt words

blk is the integer block number of the file to be read. The user program normally updates blk before it is used again. The first block of a file is block number 0

chan is the integer specification for the RT-11 channel to be used

crtn is the assembly language routine to be activated when the transfer is complete. This name must be specified in an EX-TERNAL statement in the FORTRAN routine that issues the IREADC call

## Errors:

See the errors under IREAD.

## Example:

```matlab
INTEGER*2 IBUF(256),RCODE,IBLK
EXTERNAL RDCMP
.
.
RCODE=IREADC(256,IBUF,IBLK,ICHAN,RDCMP)
```

## IREADF

The IREADF function transfers a specified number of words from the indicated channel into memory. Control returns to the user program immediately after the IREADF function is initiated. When the operation is complete, the specified FORTRAN subprogram (crtn) is entered as an asynchronous completion routine (see Section 1.2.1.2).

Form: i = IREADF (wcnt,buff,blk,chan,area,crtn)

## where:

wcnt is the integer number of words to be transferred

buff is the array to be used as the buffer; this array must contain at least wcnt words

blk is the integer block number of the file to be used. The user program normally updates blk before it is used again. The first block of a file is block number 0

chan is the integer specification for the RT-11 channel to be used

area is a four-word area to be set aside for link information; this area must not be modified by the FORTRAN program or swapped over by the USR. This area can be reclaimed by other FORTRAN completion functions when crtn has been activated

crtn is the FORTRAN routine to be activated on completion of the transfer. This name must be specified in an EXTERNAL statement in the routine that issues the IREADF call. Section 1.2.1.2 describes completion routines

## Errors:

See the errors under IREAD.

## Example:

INTEGER\*2 DBLK(4),BUFFER(25G),BLKNO
DATA DBLK/3RDX0,3RINP,3RUT ,3RDAT/,BLKNO/O/
EXTERNAL RCMPLT
:
.
.
ICHAN=IGETC()
IF(ICHAN.LT.O) STOP 'NO CHANNEL AVAILABLE'
IF(IFETCH(DBLK),NE.O) STOP 'BAD FETCH'
IF(LOOKUP(ICHAN,DBLK),LT.O) STOP 'BAD LOOKUP'
:
.
.
20 IF(IREADF(25G,BUFFER,BLKNO,ICHAN,DBLK,RCMPLT),LT.O) GOTO
100
C PERFORM OVERLAP PROCESSING
:
.
.
C SYNCHRONIZER
CALL IWAIT(ICHAN) !WAIT FOR COMPLETION ROUTINE TO RUN
BLKNO=BLKNO+1 !UPDATE BLOCK NUMBER
GOTO 20
:
.
.
C END OF FILE PROCESSING
100 CALL ICLOSE(ICHAN,I)
I=ICLOSE()
CALL IFREEC(ICHAN)
:
.
.
CALL EXIT
END
SUBROUTINE RCMPLT(I,J)
C THIS IS THE COMPLETION ROUTINE
:
.
RETURN
END

## IREADW

The IREADW function transfers a specified number of words from the indicated channel into memory. Control returns to the user program when the transfer is complete or when an error is detected.

Form: i = IREADW (wcnt,buff,blk,chan)

## where:

wcnt is the integer number of words to be transferred

buff is the array to be used as the buffer; this array must contain at least wcnt words

blk is the integer block number of the file to be read. The user program normally updates blk before it is used again

chan is the integer specification for the RT-11 channel to be used

## Errors:

See the errors under IREAD.

```python
Example:
    INTEGER*2 IBUF(1024)
    :
    :
    ICODE=IREADW(1024,IBUF,IBLK,ICHAN)
    IF(ICODE.EQ,-1) GOTO 100      !END OF FILE PROCESSING AT 100
    IF(ICODE.LT,-1) GOTO 200      !ERROR PROCESSING AT 200
C
C     MODIFY BLOCKS
C
    :
    :
    :
C
C     WRITE THEM OUT
C
    ICODE=IWRITW(1024,IBUF,IBLK,ICHAN)
```

## 3.46 IRENAM

The IRENAM function causes an immediate change of the name of a specified file.

```txt
Form: i = IRENAM (chan,dblk)
```

where:

chan is the integer specification for the RT-11 channel to be used for the operation. You must obtain this channel through an IGETC call, or you can use channel 16(decimal) or higher if you have done an ICDFN call. The channel is again available for use once the rename operation is completed

dblk is the eight-word area specifying the name of the existing file and the new name to be assigned. If considered as an eight-element INTEGER\*2 array, dblk has the form:

Words 1–4 specify the Radix-50 file descriptor for the old file name

Words 5–8 specify the Radix–50 file descriptor for the new file name

## NOTE

The arguments of IRENAM must be positioned so that the USR does not swap over them.

If a file already exists with the same name as the new file on the indicated device, it is deleted. IRENAM requires that the handler to be used be resident at the time the IRENAM is issued. If it is not, a monitor error occurs. The device names specified in the file descriptors must be the same.

For more information on renaming files, see the .RENAME programmed request (Section 2.75).

Errors:

```python
i = 0    Normal return.
    = 1    Specified channel is already open.
    = 2    Specified file was not found.
    = 3    A file by that name already exists and is protected.
```

Example:

```txt
REAL*8 NAME(2)
DATA NAME/12RDKOFTN2  DAT,12RDKOFTN2  OLD/
.
.
.
ICHAN=IGETC()
IF(ICHAN.LT.O) STOP 'NO CHANNEL'
CALL IRENAM(ICHAN,NAME)      !PRESERVE OLD DATA FILE
CALL IFREEC(ICHAN)
```

## 3.47 IREOPN

The IREOPN function reassociates a specified channel with a file on which an ISAVES was performed. The ISAVES/IREOPN combination is useful when a large number of files must be operated on at one time. Necessary files can be opened with LOOKUP and their status preserved with ISAVES. When data is required from a file, an IREOPN enables the program to read from the file. The IREOPN need not be done on the same channel as the original LOOKUP and ISAVES.

```txt
Form: i = IREOPN (chan,cblk)
```

where:

chan is the integer specification for the RT-11 channel to be associated with the reopened file; this channel must be initially inactive

```txt
i = 0    Normal return.
    = 1    Specified channel is already in use.
Example:
INTEGER*2 SAVES(5,10)
DATA ISVPTR/1/
.
.
.
CALL ISAVES(ICHAN,SAVES(1,ISVPTR))
.
.
.
CALL IREOPN(ICHAN,SAVES(1,ISVPTR))
```

cblk is the five-word block where the channel status information was stored by a previous ISAVES. This block, considered as a five-element INTEGER\*2 array, has the following format:

Word 1 Channel status word.

2 Starting block number of the file; zero for non-file-structured devices.

3 Length of file (in 256-word blocks).

4 Reserved for future use.

5 Two information bytes. Even byte: I/O count of the number of requests outstanding on this channel. Odd byte: unit number of the device associated with the channel.

## Errors:

## 3.48 ISAVES

The ISAVES function stores five words of channel status information into a user-specified array. These words contain all the information that RT-11 requires to completely define a file. When an ISAVES is finished, the data words are placed in memory and the specified channel is closed, so that it is again available for use. When the saved channel data is required, the IRE-OPN function (Section 3.47) is used.

ISAVES can be used only if a file was opened with a LOOKUP call (see Section 3.79). If IENTER was used, ISAVES returns an error. Note that ISAVES is not legal on magtape or cassette files.

```txt
Form: i = ISAVES (chan,cblk)
```

where:

chan is the integer specification for the RT-11 channel whose status is to be saved. You must obtain this channel through an IGETC call, or you can use channel 16 or higher if you have done an ICDFN call

cblk is a five-word block in which the channel status information describing the open file is stored (see Section 3.47 for the format of this block).

The ISAVES/IREOPN combination is very useful, but care must be exercised when using it. In particular, the following cases should be avoided.

1. If an ISAVES is performed on a file and the same file is then deleted before it is reopened, the space occupied by the file becomes available as an empty space which could then be used by the IENTER function. If this sequence occurs, there is a change in the contents of the file whose status was supposedly saved.

2. Although the handler for the required peripheral need not be in memory for execution of an IREOPN, a fatal error is generated if the handler is not in memory when an IREAD or IWRITE is executed.

Errors:

i = 0 Normal return.

= 1 The specified channel is not currently associated with any file.

= 2 The file was opened with an IENTER call.

Example:

```m4
INTEGER*2 BLK(5)
.
.
IF(ISAVES(ICHAN,BLK),NE,0) STOP 'ISAVES ERROR'
```

## 3.49 ISCHED

The ISCHED function schedules a specified FORTRAN subroutine to be run as an asynchronous completion routine at a specified time of day. Support for ISCHED in SJ requires timer support.

```javascript
Form: i = ISCHED (hrs,min,sec,tick,area,id,crtn)
```

where:

hrs is the integer number of hours

min is the integer number of minutes

sec is the integer number of seconds

tick is the integer number of ticks (1/60 of a second on 60-cycle clocks; 1/50 of a second on 50-cycle clocks)

area is a four-word area that must be provided for link information; this area must never be modified by the FORTRAN program, and the USR must not swap over it. This area can be reclaimed by other FORTRAN completion functions when crtn has been activated

id is the identification integer to be passed to the routine being scheduled

```txt
i = 0    Normal return.
    = 1    No queue elements available; unable to schedule request.
```

```txt
SUBROUTINE crtn(id)
INTEGER id
```

crtn is the name of the FORTRAN subroutine to be entered at the time of day specified. This name must be specified in an EX-TERNAL statement in the FORTRAN routine that issues the ISCHED call. The subroutine has one argument. For example:

When the routine is entered, the value of the integer argument is the value specified for id in the appropriate ISCHED call

## Notes:

1. The scheduling request made by ISCHED can be canceled at a later time by an ICMKT function call.

2. If the system is busy, the actual time of day that the completion routine is run may be later than the requested time of day.

3. A FORTRAN subroutine can periodically reschedule itself by issuing its own ISCHED or ITIMER calls from within the routine.

4. ISCHED requires a queue element; this should be considered when the IQSET function (Section 3.42) is executed.

```txt
INTEGER*2 LINK(4)                      !LINKAGE AREA
EXTERNAL NOON                          !NAME OF ROUTINE TO RUN
:
:
I=ISCHEO(12,0,0,0,LINK,0,NOON)      !RUN SUBR NOON AT 12 PM
:
:     (rest of main program)
END
SUBROUTINE NOON(ID)
C
C THIS ROUTINE WILL TERMINATE EXECUTION AT LUNCHTIME,
C IF THE JOB HAS NOT COMPLETED BY THAT TIME.
C
STOP       'ABORT JOB -- LUNCHTIME'
END
```

## 3.50 ISCOMP

(See SYSLIB subroutine SCOMP.)

## 3.51 ISDAT/ISDATC/ISDATF/ISDATW (FB and XM Only)

The functions ISDAT, ISDATC, ISDATF, and ISDATW are used with the IRCVD, IRCVDC, IRCVDF, and IRCVDW calls to allow message transfers under the FB or XM monitor. Note that the buffer containing the message

i = 0 Normal return.

should not be modified or reused until the message has been received by the other job. These functions require a queue element, which should be considered when the IQSET function (see Section 3.42) is executed.

## ISDAT

The ISDAT function transfers a specified number of words from one job to the other. Control returns to the user program immediately after the transfer is queued. This call is used with the MWAIT routine (see Section 3.90).

Form: i = ISDAT (buff,wcnt)

## where:

buff is the array containing the data to be transferred

wcnt is the integer number of data words to be transferred

## Errors:

```python
i = 0    Normal return.
    = 1    No such job currently exists in the system. (A job exists as long as it is loadable, whether or not it is active.)
```

```txt
Example:
INTEGER*2 MSG(40)
.
.
.
CALL ISDAT(MSG,40)
.
.
.
CALL MWAIT
C PUT NEW MESSAGE IN BUFFER
```

## ISDATC

The ISDATC function transfers a specified number of words from one job to another. Control returns to the user program immediately after the transfer is queued. When the other job accepts the message through a receive data request, the specified assembly language routine (crtn) is activated as an asynchronous completion routine.

```javascript
Form: i = ISDATC (buff,wcnt,crtn)
```

where:

buff is the array containing the data to be transferred

wcnt is the integer number of data words to be transferred

crtn is the name of an assembly language routine to be activated on completion of the transfer. This name must be specified in an EXTERNAL statement in the FORTRAN routine that issues the ISDATC call

## Errors:

= 1 No such job currently exists in the system. (A job exists as long as it is loaded, whether or not it is active.)

```txt
i = 0 Normal return.
```

```txt
Example:
    INTEGER*2 MSG(40)
    EXTERNAL RTN
    .
    .
    .
    CALL ISDATC(MSG,40,RTN)
```

## ISDATF

The ISDATF function transfers a specified number of words from one job to the other. Control returns to the user program immediately after the transfer is queued and execution continues. When the other job accepts the message through a receive data request, the specified FORTRAN subprogram (crtn) is activated as an asynchronous completion routine (see Section 1.2.1.2).

```txt
Form: i = ISDATF (buff,wcnt,area,crtn)
```

## where:

buff      is the array containing the data to be transferred

wcnt is the integer number of data words to be transferred

area is a four-word area to be set aside for link information; this area must not be modified by the FORTRAN program and the USR must not swap over it. This area can be reclaimed by other FORTRAN completion functions when crtn has been activated

crtn is the name of a FORTRAN routine to be activated on completion of the transfer. This name must be specified in an EXTERNAL statement in the FORTRAN routine that issues the ISDATF call

## Errors:

= 1 No such job currently exists in the system. (A job exists as long as it is loaded, whether or not it is active.)

## Example:

```txt
INTEGER*2 MSG(40),SPOT(4)
EXTERNAL RTN
.
.
.
CALL ISDATAF(MSG,40,SPOT,RTN)
```

## ISDATW

The ISDATW function transfers a specified number of words from one job to the other. Control returns to the user program when the other job has accepted the data through a receive data request.

Form: i = ISDATW (buff,wcnt)

```txt
where:
    buff     is the array containing the data to be transferred
    wcnt     is the integer number of data words to be transferred
Errors:
    i = 0   Normal return.
        = 1   No such job exists in the system. (A job exists as long as it is loaded, whether or not it is active.)
Example:
    INTEGER*2 MSG(40)
    :
    :
    IF (ISDATW(MSG,40),NE,0) STOP 'FOREGROUND JOB NOT RUNNING'
```

## 3.52 ISDTTM

The ISDTTM function sets the system date and time. An argument of -1 leaves the corresponding value unchanged.

```txt
C DEFINE NEW SYSTEM DATE BUT LEAVE TIME UNCHANGED
IDATE = IMONTH*1024+IDAY*32+(IYEAR-1972)
CALL ISDTTM (IDATE, -1, -1)
:
```

## 3.53 ISFDAT

The ISFDAT function allows user programs to modify the creation date of an RT-11 file. The device must have an RT-11 file structure.

```txt
Form: i = ISFDAT (chan,dblk,idate)
```

where:

chan is the integer value of the RT-11 channel to be used for the operation. You must obtain this channel through an IGETC call, or you can use channel 16(decimal) or higher if you have done an ICDFN call

```txt
dblk is the four word RT-11 file specification, in Radix-50, of the file whose date is being changed
```

idate is the integer date in RT-11 date format

## Errors:

```txt
i = 0    Normal return.
    = 1    Channel in use.
    = 2    File not found.
    = 3    Invalid operation.
```

## Example:

This example changes the date of the file DY1:OLD23.DAT to July 4, 1976.

```txt
REAL*4 FILNAM(2)
DATA FILNAM /GRDY1OLD,6R23 DAT/
IDATE=7*1024 + 4*32 + (1976-1972)      !JULY 4, 1976
ICHAN = IGETC()                       !ALLOCATE CHANNEL
I = ISFDAT(ICHAN,FILNAM,IDATE)       !SET THE DATE
IF (I.NE.O) STOP 'ERROR DURING ISFDAT CALL'
.
.
.
END
```

## 3.54 ISLEEP

The ISLEEP function suspends the main program execution of a job for a specified amount of time. The specified time is the sum of hours, minutes, seconds, and ticks specified in the ISLEEP call. All completion routines continue to execute.

```txt
Form: i = ISLEEP (hrs,min,sec,tick)
```

## where:

```txt
hrs is the integer number of hours
```

```txt
min is the integer number of minutes
```

sec is the integer number of seconds

tick is the integer number of ticks (1/60 of a second on 60-cycle clocks; 1/50 of a second on 50-cycle clocks)

## Notes:

1. SLEEP requires a queue element, which should be considered when the IQSET function (Section 3.42) is executed.

2. If the system is busy, the time for which execution is suspended may be longer than that specified.

## Errors:

```python
i = 0    Normal return.
    = 1    No queue element available.
```

```txt
Example:
.
.
.
CALL IQSET(2)
.
.
.
CALL ISLEEP(0,0,0,4)      !GIVE BACKGROUND JOB SOME TIME
```

## 3.55 ISPFN/ISPFNC/ISPFNF/ISPFNW

The functions ISPFN, ISPFNC, ISPFNF, and ISPFNW are used in conjunction with special functions to various handlers. They provide a means of doing device-dependent functions, such as rewind and backspace, to those devices. If ISPFN function calls are made to any other devices, the function call is ignored. For more information on programming for specific devices, see the RT-11 Software Support Manual.

To use these functions, the handler must be in memory, and a channel must be associated with a file via a non-file-structured LOOKUP call. These functions require a queue element; this should be considered when the IQSET function (Section 3.42) is executed.

## ISPFN

The ISPFN function queues the specified operation and immediately returns control to the user program. The IWAIT function can be used to ensure completion of the operation.

Form: i = ISPFN (code,chan[,wcnt,buff,blk])

## where:

code is the integer numeric code of the function to be performed (see Table 3-1)

chan is the integer specification for the RT-11 channel to be used for the operation. You must obtain this channel through an IGETC call, or you can use channel 16(decimal) or higher if you have done an ICDFN call

wcnt is the integer number of data words in the operation. This parameter is optional with some ISPFN calls, depending on the particular function. Default value is 0. In magtape operations, it specifies the number of records to space forward or backward. For a backspace operation (wcnt=0), the tape drive backspaces to a tape mark or to the beginning-of-tape. For a forward space operation (wcnt=0), the tape drive forward spaces to a tape mark or the end-of-tape

buff is the array to be used as the data buffer. This parameter is optional with some ISPFN calls, depending on the particular function. Default value is 0

is the integer block number of the file to be operated upon. This parameter is optional with some ISPFN calls, depending on the particular function. Default value is 0

When this argument is supplied by magtape, it is the address of a four-word error and status block used for returning the exception conditions. The four words must be initialized to zero.

The error and status block must always be mapped when running in the XM monitor, and the USR must not swap over it. To obtain the address of the error block, execute the following instructions:

```prolog
INTEGER*2        ERRADR, ERRBLK(4)
DATA ERRBLK     /0,0,0,0,/

.
.
.
.
ERRADR = IADDR (ERRBLK)  !GET THE ADDRESS OF THE 4-WORD ERROR BLOCK
ICODE = ISPFN (CODE,ICHAN,WDCT,BUF,ERRADR)
```

The three optional arguments (wcnt, buff, blk) are not individually optional. You must have all or none present.

Table 3-1: Functions and Function Codes (Octal)

| Function | MS,MT,MM | CT | DX | DM | DY | DL | LD | DU | DW | DZ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Read absolute |  |  | 377 | 377 | 377 | 377 |  |  | 377* | 377* |
| Write absolute |  |  | 376 | 376 | 376 | 376 |  |  | 376* | 376* |
| Write absolute with deleted data |  |  | 375 |  | 375 |  |  |  |  |  |
| Forward to last file |  | 377 |  |  |  |  |  |  |  |  |
| Forward to last block |  | 376 |  |  |  |  |  |  |  |  |
| Forward to next file |  | 375 |  |  |  |  |  |  |  |  |
| Forward to next block |  | 374 |  |  |  |  |  |  |  |  |
| Rewind to load point | 373 | 373 |  |  |  |  |  |  |  |  |
| Write file gap |  | 372 |  |  |  |  |  |  |  |  |
| Write end-of-file | 377 |  |  |  |  |  |  |  |  |  |
| Forward 1 block | 376 |  |  |  |  |  |  |  |  |  |
| Backspace 1 block | 375 |  |  |  |  |  |  |  |  |  |
| Initialize the bad block replacement table |  |  |  | 374 |  | 374 |  |  |  |  |
| Write with extended record gap | 374 |  |  |  |  |  |  |  |  |  |
| Offline | 372 |  |  |  |  |  |  |  |  |  |
| Return volume size |  |  |  | 373 | 373 | 373 | 373 | 373 | $373^†$ |  |
| Read/write translation table |  |  |  |  |  |  | 372 | 372 |  |  |
| Write variable size blocks | 371 |  |  |  |  |  |  |  |  |  |
| Direct MSCP access |  |  |  |  |  |  |  | 371 |  |  |
| Read variable size blocks | 370 |  |  |  |  |  |  |  |  |  |
| Stream at 100 ips (MS only) | 367 |  |  |  |  |  |  |  |  |  |

\* When using special functions 376 and 377 with DW or DZ:

wcnt is the track to be read or written.

blk is the sector.

buf is the address of a 256-word buffer.

Special functions 376 and 377 with DZ handler do not interleave sectors. RX50 diskettes, handled by DZ, have 80 tracks. Special functions 376 and 377 wrap to track 0 after track 79.

$^{+}$  When using special function 373 with DW:

chan is the channel on which DW was opened with .LOOKUP.

buf is the address of a one-word buffer in which the size of the volume will be returned: 9727(decimal) blocks for an RD50, 19519(decimal) blocks for an RD51.

blk is not used and should be set to 0.

```txt
Example:
CALL ISPFN("373,ICHAN) !REWIND
```

## Errors:

i = 0 Normal return.

= 1 Attempt to read or write past end-of-file.

= 2 Hardware error occurred on channel.

= 3 Channel specified is not open.

## ISPFNC

The ISPFNC function queues the specified operation and immediately returns control to the user program. When the operation is complete, the specified assembly language routine (crtn) is entered as an asynchronous completion routine.

Form: i = ISPFNC (code,chan,wcnt,buff,blk,crtn)

## where:

code is the integer numeric code of the function to be performed (see Table 3-1)

chan is the integer specification for the RT-11 channel to be used for the operation. You must obtain this channel through an IGETC call, or you can use channel 16(decimal) or higher if you have done an ICDFN call

wcnt is the integer number of data words in the operation; the default value for this argument is 0

buff      is the array to be used as the data buffer; the default value for
        this argument is 0

blk      is the integer block number of the file to be operated upon;
        this argument must be 0 if not required

When this argument is supplied by magtape, it is the address of a four-word error and status block used for returning the exception conditions. The four words must be initialized to 0.

The error and status block must always be mapped when running in the XM monitor, and the USR must not swap over it. To obtain the address of the error block execute the following instructions:

```fortran
INTEGER*2        ERRADR, ERRBLK(4)
DATA ERRBLK     /0,0,0,0,/

    .

    .

!GET ADDRESS OF 4-WORD ERROR BLOCK
ERRADR = IADDR (ERRBLK)
ICODE = ISPFNC (CODE,ICHAN,WDCT,BUF,ERRADR)
```

crtn is the name of an assembly language routine to be activated on completion of the operation. This name must be specified in an EXTERNAL statement in the FORTRAN routine that issues the ISPFNC call

## Errors:

i = 0 Normal return.

= 1 Attempt to read or write past end-of-file.

= 2 Hardware error occurred on channel.

= 3 Channel specified is not open.

## Example:

```txt
EXTERNAL SFCOMP          !NAME OF ASSEMBLY LANGUAGE COMPLETION RTN
:
:
ICODE = ISPFNC(CODE,ICHAN,WDCT,BUF,BLK,SFCOMP)
```

## ISPFNF

The ISPFNF function queues the specified operation and immediately returns control to the user program. When the operation is complete, the specified FORTRAN subprogram (crtn) is entered as an asynchronous completion routine.

Form: i = ISPFNF (code,chan,wcnt,buff,blk,area,crtn)

## where:

code is the integer numeric code of the function to be performed (see Table 3-1)

chan is the integer specification for the RT-11 channel to be used for the operation. You must obtain this channel through an IGETC call, or you can use channel 16(decimal) or higher if you have done an ICDFN call

wcnt is the integer number of data words in the operation; this argument must be 0 if not required

buff      is the array to be used as the data buffer; this argument must
                             be 0 if not required

blk      is the integer block number of the file to be operated upon;
        this argument must be 0 if not required

When this argument is supplied by magtape, it is the address of a four-word error and status block used for returning the exception conditions. The four words must be initialized to 0.

The error and status block must always be mapped when running in the XM monitor, and the USR must not swap over it. To obtain the address of the error block, execute the following instructions:

```fortran
INTEGER*2        ERRADR, ERRBLK(4)
DATA ERRBLK     /0,0,0,0,/

.
.
!
!GET THE ADDRESS OF THE 4-WORD ERROR BLOCK
ERRADR = IADDR (ERRBLK)
ICODE = ISPFNF (CODE,ICHAN,WDCT,BUF,ERRADR)
```

area is a four-word area to be set aside for linkage information; this area must not be modified by the FORTRAN program, and the USR must not swap over it. This area can be reclaimed by other FORTRAN completion functions when crtn has been activated

crtn is the name of a FORTRAN routine to be activated on completion of the operation. This name must be specified in an EXTERNAL statement in the FORTRAN routine that issues the ISPFNF call (Section 1.2.1.2 describes completion routines)

## Errors:

```python
i = 0    Normal return.
    = 1    Attempt to read or write past end-of-file.
    = 2    Hardware error occurred on channel.
    = 3    Channel specified is not open.
```

## Example:

```prolog
REAL*4 MTNAME(2),AREA(2)
DATA MTNAME/3RMTO,0./
EXTERNAL DONSUB
.
.
.
I=IGETC()                      !ALLOCATE CHANNEL
CALL IFETCH(MTNAME)          !FETCH MT HANDLER
CALL LOOKUP(I,MTNAME)      !NON-FILE-STRUCTURED LOOKUP ON MTO
IERR=ISPFNF("373,I,0,0,0,AREA,DONSUB)   !REWIND MAGTAPE
.
.
.
END
SUBROUTINE DONSUB
C
C RUNS WHEN MTO HAS BEEN REWOUND
C
.
.
.
END
```

## ISPFNW

The ISPFNW function queues the specified operation and returns control to the user program when the operation is complete.

Form: i = ISPFNW (code,chan[,wcnt,buff,blk])

```txt
code is the integer numeric code of the function to be performed
(see Table 3-1)
chan is the integer specification for the RT-11 channel to be used
for the operation. You must obtain this channel through an
IGETC call, or you can use channel 16(decimal) or higher if
you have done an ICDFN call
wcnt is the integer number of data words in the operation. This
parameter is optional with some ISPFNW calls, depending on
the function
buff is the array to be used as the data buffer. This parameter is
optional with some ISPFNW calls, depending on the function
blk is the integer block number of the file to be operated upon.
This parameter is optional with some ISPFNW calls, depend-
ing on the function
When this argument is supplied by magtape, it is the address
of a four-word error and status block used for returning the
exception conditions. The four words must be initialized to 0.
The error and status block must always be mapped when
running in the XM monitor, and the USR must not swap over
it. To obtain the address of the error block execute the follow-
ing instructions:
INTEGER*2 ERRADR, ERRBLK(4)
DATA ERRBLK /0,0,0,0,/:
!
!GET THE ADDRESS OF THE 4-WORD ERROR BLOCK
ERRADR = IADDR (ERRBLK)
ICODE = ISPFN (CODE,ICHAN,WDCT,BUF,ERRADR)
Errors:
i = 0 Normal return.
= 1 Attempt to read or write past end-of-file.
= 2 Hardware error occurred on channel.
= 3 Channel specified is not open.
Example:
INTEGER*2 BUF(65),TRACK,SECTOR,DBLK(4)
DATA DBLK/3RDX0,0,0,0/
:
:
ICHAN=IGETC()
IF(ICHAN,LT,0) STOP 'NO CHANNEL AVAILABLE'
IF(LOOKUP(ICHAN,DBLK),LT,0) STOP 'BAD LOOKUP'
:
:
C READ AN ABSOLUTE TRACK AND SECTOR FROM THE FLOPPY
C
```

## where:

```python
ICODE=ISPFNW("377,ICHAN,TRACK,BUF,SECTOR)
C
C     BUF(1) IS THE DELETED DATA FLAG
C     BUF(2-65) IS THE DATA
```

## 3.56 ISPY

The ISPY function returns the integer value of the word at a specified offset from the RT-11 resident monitor. This subroutine uses the .GVAL programmed request to return fixed monitor offsets. (See the RT-11 Software Support Manual for information on fixed offset references.)

```txt
Form: i = ISPY (ioff)
```

where:

ioff is the offset (from the base of RMON) to be examined

Function Result:

The function result (i) is set to the value of the word examined.

Example:

```txt
C
C     BRANCH TO 200 IF RUNNING UNDER FB MONITOR
C
      IF(ISPY("300).AND.1) GOTO 200
C
C     WORD AT OCTAL 300 FROM RMON IS
C     THE CONFIGURATION WORD.
```

## 3.57 ITIMER

The ITIMER function schedules a specified FORTRAN subroutine to be run as an asynchronous completion routine after a specified time interval has elapsed. This request is supported by SJ when the timer support special feature is included during system generation.

```javascript
Form: i = ITIMER (hrs,min,sec,tick,area,id,crtn)
```

where:

hrs is the integer number of hours

min is the integer number of minutes

sec is the integer number of seconds

tick is the integer number of ticks (1/60 of a second on 60-cycle clocks; 1/50 of a second on 50-cycle clocks)

area is a four-word area that must be provided for link information; this area must never be modified by the FORTRAN program, and the USR must never swap over it. This area can be reclaimed by other FORTRAN completion functions when crtn has been activated

id is the identification integer to be passed to the routine being scheduled

crtn is the name of the FORTRAN subroutine to be entered when the specified time interval elapses. This name must be specified in an EXTERNAL statement in the FORTRAN routine that references ITIMER. The subroutine has one argument. For example:

```txt
SUBROUTINE crtn(id)
INTEGER id
```

When the routine is entered, the value of the integer argument is the value specified for id in the appropriate ITIMER call

## Notes:

1. This function can be canceled at a later time by an ICMKT function call.

2. If the system is busy, the actual time interval after which the completion routine is run can be longer than the time interval requested.

3. FORTRAN subroutines can periodically reschedule themselves by issuing ISCHED or ITIMER calls.

4. ITIMER requires a queue element, which should be considered when the IQSET function (Section 3.42) is executed.

For more information on scheduling completion routines, see Section 1.2.1.2 and the .MRKT programmed request, Section 2.49.

```txt
Errors:
    i = 0    Normal return.
    = 1    No queue elements available; unable to schedule request.
```

```asm
Example:
    INTEGER*2 AREA(4)
    EXTERNAL WATCHD
    :
    :
    :
C     IF THE CODE FOLLOWING ITIMER DOES NOT REACH THE ICMKT CALL
C     IN 12 MINUTES, WATCH DOG COMPLETION ROUTINE WILL BE
C     ENTERED WITH ID OF 3
C
    CALL ITIMER(0,12,0,0,AREA,3,WATCHD)
    :
    :
    :
    CALL ICMKT(3,AREA)
    :
    :
    :
    END
    SUBROUTINE WATCHD(ID)
C
C     THIS IS CALLED AFTER 12 MINUTES
    :
    :
    :
    RETURN
    END
```

```txt
IF(ITLOCK(),NE,0) GOTO 100 !GOTO 100 IF USR BUSY
```

## 3.58 ITLOCK (FB and XM Only)

The ITLOCK function is used in an FB or XM system to attempt to gain ownership of the USR. It is similar to LOCK (Section 3.78) in that, if successful, the user job returns with the USR in memory. However, if a job attempts to LOCK the USR while the other job is using it, the requesting job is suspended until the USR is free. With ITLOCK, if the USR is not available, control returns immediately and the lock failure is indicated. ITLOCK cannot be called from a completion or interrupt routine.

```txt
Form: i = ITLOCK()
```

For further information on gaining ownership of the USR, see the .TLOCK programmed request (Section 2.93).

Errors:

```python
i = 0    Normal return.
    = 1    USR is already in use.
```

Example:

## 3.59 ITTINR

The ITTINR function transfers a character from the console terminal to the user program. If no characters are available, system action is determined by the setting of bit 6 of the Job Status Word.

```txt
Form: i = ITTINR()
```

If the function result  $(i)$  is less than 0 when execution of the ITTINR function is complete, it indicates that no character was available. Under the FB or XM monitor, ITTINR does not return a result of less than zero unless bit 6 of the Job Status Word was on when the request was issued.

There are two modes of doing console terminal input, and they are governed by bit 12 of the Job Status Word (JSW). The JSW is at octal location 44. If bit 12 is 0, normal I/O is performed under the following conditions:

1. The monitor echoes all characters typed.

2. CTRL/U and RUBOUT perform line deletion and character deletion, respectively.

3. A carriage return, line feed, CTRL/Z, or CTRL/C must be struck before characters on the current line are available to the program. When one of these is typed, characters on the line typed are passed one by one to the user program.

If the console is in special mode (bit 12 set to 1), the following conditions apply:

1. The monitor does not echo characters typed except for CTRL/C and CTRL/O.

2. CTRL/U and RUBOUT do not perform special functions.

3. Characters are immediately available to the program.

4. No ALTMODE conversion is done.

In special mode, the user program must echo the characters desired. However, CTRL/C and CTRL/O are acted on by the monitor in the usual way.

Bit 12 in the JSW must be set by the user program if special console mode is desired. Bit 14 in the JSW must be set if lowercase characters are desired. These bits are cleared when control returns to RT-11.

Regardless of the setting of bit 12, when a carriage return is entered, both carriage return and line feed characters are passed to the program; if bit 12 is 0, these characters will be echoed.

Lowercase conversion is determined by the setting of bit 14. If bit 14 is 0, lowercase characters are converted to uppercase before being echoed (if bit 12 is 0) and passed to a program; if bit 14 is 1, lowercase characters are echoed (if bit 12 is 0) and passed as received. Bit 14 is cleared when the program terminates.

## NOTE

To set and/or clear bits in the JSW, do an IPEEK and then an IPOKE (see example under IPOKE). In special terminal mode (JSW bit 12 set), normal FORTRAN formatted I/O from the console is undefined.

If the single-line editor has been enabled with the SET SL ON and SET SL TTYIN commands, input from an ITTINR request can be edited by the single-line editor if JSW bits 4 and 12 are 0. However, if either bit 4 or bit 12 is set, SL will not edit ITTINR input. If SL is editing input, the state of bit 6 (inhibit TT wait) is ignored and an ITTINR request will not return until an edited line is available.

In the FB or XM monitor, CTRL/F and CTRL/B (and CTRL/X in monitors with the system job feature) are not affected by the setting of bit 12. The monitor always acts on these characters if the SET TT FB command is in effect.

Also under the FB or XM monitor, if a terminal input request is made and no character is available, job execution is normally suspended until a character is ready. If a program requires execution to continue and ITTINR to return a result of less than zero, it must turn on bit 6 of the JSW before the ITTINR. Bit 6 is cleared when a program terminates. The results of ITTINR must be stored in an INTEGER type variable for the purposes of error checking. Once it is known that the call did not have an error return, the result can be moved into a LOGICAL\*1 variable or array element. Direct placement into a LOGICAL\*1 variable will lead to incorrect results, because the negative flag (bit 15 set) is lost in conversion to a LOGICAL\*1 variable.

Function Results:

i >0 Character read.

<0 No character available.

## 3.60 ITTOUR

The ITTOUR function transfers a character from the user program to the console terminal if there is room for the character in the monitor buffer. If it is not currently possible to output a character, an error flag is returned.

Form: i = ITTOUR (char)

where:

char is the character to be output, right-justified in the integer (can be LOGICAL\*1 entity if desired)

If the function result (i) is 1 when execution of the ITTOUR function is complete, it indicates that there is no room in the buffer and that no character was output. Under the FB or XM monitor, ITTOUR normally does not return a result of 1. Instead, the job is blocked until room is available in the output buffer. If a job requires execution to continue and a result of 1 to be returned, it must turn on bit 6 of the JSW (location 44) before issuing the request.

## NOTE

If a foreground job has characters in the TT output buffer, they are not output under the following conditions:

1. If a background job is doing output to the console TT, the foreground job cannot output characters from its buffer until the background job outputs a line feed character. This can be troublesome if the console device is a graphics terminal and the background job is doing graphic output without sending any line feeds.

2. If no background job is running (that is, KMON is in control of background), the foreground job cannot output its characters until the user types a carriage return or a line feed. In the former case, KMON gets control again and locks out foreground output as soon as the foreground output buffer is empty.

Note that the use of PRINT eliminates these problems.

Function Results:

i = 0 Character was output.

= 1 Ring buffer is full.

Example:

```matlab
DO 20 I=1,5
10     IF(ITTOUR("007),NE,0) GOTO 10
20     CONTINUE
```

!RING BELL 5 TIMES

## 3.61 ITWAIT (SYSGEN Option in SJ)

The ITWAIT function suspends the main program execution of the current job for a specified time interval. All completion routines continue to execute.

```txt
Form: i = ITWAIT (itime)
```

where:

itime is the two-word internal format time interval

```txt
itime (1) is the high-order time
itime (2) is the low-order time
```

Notes:

1. WAIT requires a queue element, which should be considered when the IQSET function (Section 3.42) is executed.

2. If the system is busy, the actual time interval during which execution is suspended may be longer than the time interval specified.

```python
Errors:
    i = 0   Normal return.
      = 1   No queue element available.
Example:
    INTEGER*2 TIME(2)
    :
    :
    CALL ITWAIT(TIME)      !WAIT FOR TIME
```

## 3.62 IUNTIL (SYSGEN Option in SJ)

The IUNTIL function suspends main program execution of the job until the time of day specified. All completion routines continue to run.

```javascript
Form: i = IUNTIL (hrs,min,sec,tick)
```

where:

min is the integer number of minutes

sec is the integer number of seconds

tick is the integer number of ticks (1/60 of a second on 60-cycle clocks; 1/50 of a second on 50-cycle clocks)

Notes:

1. IUNTIL requires a queue element, which should be considered when the IQSET function (Section 3.39) is executed.

2. If the system is busy, the actual time of day that the program resumes execution may be later than that requested.

```python
Errors:
    i = 0   Normal return.
    = 1   No queue element available.
Example:
C     TAKE A LUNCH BREAK
      CALL IUNTIL(13,0,0,0)      !START UP AGAIN AT 1 P.M.
```

## 3.63 IVERIF

See SYSLIB subroutine VERIFY, Section 3.113.

## 3.64 IWAIT

The IWAIT function suspends execution of the main program until all input/output operations on the specified channel are complete. This function is used with IREAD, IWRITE, and ISPFN calls. Completion routines continue to execute.

```txt
Form: i = IWAIT (chan)
```

where:

chan is the integer specification for the RT-11 channel to be used. You must obtain this channel through an IGETC call, or you can use channel 16(decimal) or higher if you have done an ICDFN call

For further information on suspending execution of the main program, see the .WAIT programmed request (Section 2.101).

Errors:

i = 0 Normal return.

= 1 Channel specified is not open.

= 2 Hardware error occurred during the previous I/O operation on this channel.

Example:

```cmake
IF(IWAIT(ICHAN),NE,0) CALL IDERR(4)
```

## 3.65 IWRITE/IWRITC/IWRITF/IWRITW

The functions IWRITE, IWRITC, IWRITF, and IWRITW transfer a specified number of words from memory to the specified channel. The IWRITE functions require queue elements; this should be considered when the IQSET function (Section 3.42) is executed.

## IWRITE

The IWRITE function transfers a specified number of words from memory to the specified channel. Control returns to the user program immediately after the request is queued. No special action is taken upon completion of the operation.

Form: i = IWRITE (wcnt,buff,blk,chan)

## where:

wcnt is the integer number of words to be transferred

buff      is the array to be used as the output buffer

blk         is the integer block number of the file to be written. The user
                   program normally updates blk before it is used again

chan is the integer specification for the RT-11 channel to be used. You must obtain this channel through an IGETC call, or you can use channel 16(decimal) or higher if you have done an ICDFN call

## Errors:

i = n    Normal return; n equals the number of words written, rounded to a multiple of 256 (0 for non-file-structured writes).

## NOTE

If the word count returned is less than that requested, an implied end-of-file has occurred although the normal return is indicated.

= -1 Attempt to write past end-of-file; no more space is available in the file.

= -2 Hardware error occurred.

= -3 Channel specified is not open.

## Example:

Refer to the example for IREAD.

## IWRITC

The IWRITC function transfers a specified number of words from memory to the specified channel. The request is queued and control returns to the user program. When the transfer is complete, the specified assembly language routine (crtn) is entered as an asynchronous completion routine.

Form: i = IWRITC (wcnt,buff,blk,chan,crtn)

## where:

wcnt is the relative integer number of words to be transferred

buff      is the array to be used as the output buffer

blk is the relative integer block number of the file to be written. The user program normally updates blk before it is used again (for example, if the program is writing two blocks at a time, blk should be updated by 2)

chan is the relative integer specification for the RT-11 channel to be used. You must obtain this channel through an IGETC call, or you can use channel 16(decimal) or higher if you have done an ICDFN call

crtn is the name of the assembly language routine to be activated upon completion of the transfer. This name must be specified in an EXTERNAL statement in the FORTRAN routine that issues the IWRITC call

## Errors:

See the errors under IWRITE.

Example:

```txt
INTEGER*2 IBUF(256)
EXTERNAL CRTN
.
.
ICODE=IWRITC(256,IBUF,IBLK,ICHAN,CRTN)
```

## IWRITF

The IWRITF function transfers a number of words from memory to the specified channel. The transfer request is queued and control returns to the user program. When the operation is complete, the specified FORTRAN subprogram (crtn) is entered as an asynchronous completion routine (see Section 1.2.1.2).

Form: i = IWRITF (wcnt,buff,blk,chan,area,crtn)

## where:

wcnt is the integer number of words to be transferred

buff      is the array to be used as the output buffer

blk         is the integer block number of the file to be written. The user
                   program normally updates blk before it is used again

chan is the integer specification for the RT-11 channel to be used. You must obtain this channel through an IGETC call, or you can use channel 16(decimal) or higher if you have done an ICDFN call

area is a four-word area to be set aside for link information; this area must not be modified by the FORTRAN program, and the USR must not swap over it. This area can be reclaimed by other FORTRAN completion functions when crtn has been activated

crtn is the name of the FORTRAN routine to be activated upon completion of the transfer. This name must be specified in an EXTERNAL statement in the FORTRAN routine that issues the IWRITF call (Section 1.2.1.2 describes completion routines)

## Errors:

See the errors under IWRITE.

Example:

Refer to the example under IREADF, Section 3.45.

## IWRITW

The IWRITW function transfers a specified number of words from memory to the specified channel. Control returns to the user program when the transfer is complete.

```javascript
Form: i = IWRITW (wcnt,buff,blk,chan)
```

where:

wcnt is the integer number of words to be transferred

buff      is the array to be used as the output buffer

blk         is the integer block number of the file to be written. The user
                   program normally updates blk before it is used again

chan is the integer specification for the RT-11 channel to be used. You must obtain this channel through an IGETC call, or you can use channel 16(decimal) or higher if you have done an ICDFN call

Errors:

See the errors under IWRITE.

Example:

Refer to the example under IREADW, Section 3.45.

## 3.66 JADD

The JADD function computes the sum of two INTEGER\*4 values.

Form: i = JADD (jopr1,jopr2,jres)

where:

jopr1 is an INTEGER\*4 variable

jopr2 is an INTEGER\*4 variable

jres is an INTEGER\*4 variable that receives the sum of jopr1 and jopr2

Function Results:

i = -1    Normal return; the result is negative.

$= 0$ Normal return; the result is zero.

= 1 Normal return; the result is positive.

```txt
Form: i = JAFIX (asrc,jres)
```

```python
Errors:
    i = -2   An overflow occurred while computing the result.
Example:
    INTEGER*4 JOP1,JOP2,JRES
    :
    .
    IF(JADD(JOP1,JOP2,JRES),EQ,-2) GOTO 100
```

## 3.67 JAFIX

The JAFIX function converts a REAL\*4 value to INTEGER\*4.

asrc is a REAL\*4 variable, constant, or expression to be converted to INTEGER\*4

jres is an INTEGER\*4 variable that is to contain the result of the conversion

Function Results:

Errors:

i = -2 An overflow occurred while computing the result.

Example:

```txt
INTEGER*4 JOP1
C READ A LARGE INTEGER FROM THE TERMINAL
ACCEPT 99,A
99 FORMAT (F15,0)
IF(JAFIX(A,JOP1),EQ,-2) GOTO 100
:
:
:
```

## 3.68 JCMP

The JCMP function compares two INTEGER\*4 values and returns an INTEGER\*2 value that reflects the signed comparison result.

```txt
Form: i = JCMP (jopr1,jopr2)
```

where:

jopr1 is the INTEGER\*4 variable or array element that is the first operand in the comparison

```txt
jopr2 is the INTEGER*4 variable or array element that is the second operand in the comparison
Function Results:
    i = -1 If jopr1 is less than jopr2.
        = 0 If jopr1 is equal to jopr2.
        = 1 If jopr1 is greater than jopr2.
Errors:
    None.
Example:
    INTEGER*4 JOPX, JOPY
    .
    .
    .
    IF (JCMP(JOPX,JOPY)) 10,20,30
IX
The JDFIX function converts a REAL*8 (DOUBLE PRECISION) value to INTEGER*4.
Form: i = JDFIX (dsrc,jres)
where:
    dsrc is a REAL*8 variable, constant, or expression to be converted to INTEGER*4
    jres is an INTEGER*4 variable to contain the conversion result
Function Results:
    i = -1 Normal return; the result is negative.
        = 0 Normal return; the result is zero.
        = 1 Normal return; the result is positive.
Errors:
    i = -2 An overflow occurred while computing the result.
Example:
        INTEGER*4 JNUM
        REAL*8 DPNUM
        .
        .
        .
    20 TYPE 98
    98 FORMAT('ENTER POSITIVE INTEGER')
        ACCEPT 99,DPNUM
    99 FORMAT(F20.0)
        IF(JDFIX(DPNUM,JNUM),LT.0) GOTO 20
        .
        .
        .
```

## 3.69 JDFIX

## 3.70 JDIV

```txt
The JDIV function computes the quotient of two INTEGER*4 values.
Form: i = JDIV (jopr1,jopr2,jres[,jrem])
where:
    jopr1 is an INTEGER*4 variable that is the dividend of the operation
    jopr2 is an INTEGER*4 variable that is the divisor of jopr1
    jres is an INTEGER*4 variable that receives the quotient of the operation (that is, jres=jopr1/jopr2)
    jrem is an INTEGER*4 variable that receives the remainder of the operation. The sign is the same as that for jopr1
Function Results:
    i = -1 Normal return; the quotient is negative.
    = 0 Normal return; the quotient is 0.
    = 1 Normal return; the quotient is positive.
Errors:
    i = -3 An attempt was made to divide by 0.
Example:
    INTEGER*4 JN1,JN2,JQUO
    .
    .
    CALL JDIV(JN1,JN2,JQUO)
    .
    .
    .
VT
The JICVT function converts a specified INTEGER*2 value to INTEGER*4.
Form: i = JICVT (isrc,jres)
where:
    isrc is the INTEGER*2 quantity to be converted
    jres is the INTEGER*4 variable or array element to receive the result
Function Results:
    i = -1 Normal return; the result is negative.
    = 0 Normal return; the result is 0.
    = 1 Normal return; the result is positive.
```

## 3.71 JICVT

```txt
Errors:
    None.
Example:
    INTEGER*4 JVAL
    CALL JICYT(478,JVAL)      !FORM A 32-BIT CONSTANT
```

## 3.72 JJCVT

The JJCVT function interchanges words of an INTEGER\*4 value to form an internal format time or vice versa. This procedure is necessary when the INTEGER\*4 variable is to be used as an argument in a timer-support function such as ITWAIT. When a two-word internal format time is specified to a function such as ITWAIT, it must have the high-order time as the first word and the low-order time as the second word.

Form: CALL JJCVT (jsrc)

where:

jsrc is the INTEGER\*4 variable whose contents are to be inter-
changed

Errors:

Example:

```txt
INTEGER*4 TIME
.
.
.
CALL GTIM(TIME)      !GET TIME OF DAY
CALL JJCVT(TIME)      !TURN IT INTO INTEGER*4 FORMAT
```

## 3.73 JMOV

The JMOV function assigns the value of an INTEGER\*4 variable to another INTEGER\*4 variable and returns the sign of the value moved.

```txt
Form: i = JMOV (jsrc,jdest)
```

where:

jsrc      is the INTEGER\*4 variable whose contents are to be moved

jdest is the INTEGER\*4 variable that is the target of the assignment

Function Results:

The value of the function is an INTEGER\*2 value that represents the sign of the result as follows:

i = -1 Normal return; the result is negative.

$= 0$ Normal return; the result is 0.

= 1 Normal return; the result is positive.

```javascript
Form: i = JSUB (jopr1,jopr2,jres)
```

```txt
Errors:
    None.
Example:
    The JMOV function allows an INTEGER*4 quantity to be compared with 0 by using it in a logical IF statement. For example:
    INTEGER*4 INT1
    :
    :
    IF(JMOV(INT1,INT1),NE,0) GOTO 300 !GO TO STMT 300 IF INT1 NOT 0
```

## 3.74 JMUL

The JMUL function computes the product of two INTEGER\*4 values.

```txt
Form: i = JMUL (jopr1,jopr2,jres)
where:
    jopr1 is an INTEGER*4 variable that is the multiplicand
    jopr2 is an INTEGER*4 variable that is the multiplier
    jres is an INTEGER*4 variable that receives the product of the operation
```

```csv
INTEGER*4 J1,J2,JRES
:
:
IF(JMUL(J1,J2,JRES)+1) 100,10,20
C GOTO 100 IF OVERFLOW
C GOTO 10 IF RESULT IS NEGATIVE
C GOTO 20 IF RESULT IS POSITIVE OR ZERO
```

## 3.75 JSUB

The JSUB function computes the difference between two INTEGER\*4 values.

jopr1 is an INTEGER\*4 variable that is the minuend of the operation

jopr2 is an INTEGER\*4 variable that is the subtrahend of the operation

jres is an INTEGER\*4 variable that is to receive the difference between $jopr1$ and $jopr2$ (that is, $jres = jopr1 - jopr2$)

## Function Results:

i = -1    Normal return; the result is negative.

= 1 Normal return; the result is positive.

Errors:

i = -2 An overflow occurred while computing the result.

## Example:

```csv
INTEGER*4 JOP1,JOP2,J3
:
.
CALL JSUB(JOP1,JOP2,J3)
```

## 3.76 JTIME

The JTIME subroutine converts the time specified to the internal two-word format time.

```txt
Form: CALL JTIME (hrs,min,sec,tick,time)
```

where:

hrs is the integer number of hours

min is the integer number of minutes

sec is the integer number of seconds

tick is the integer number of ticks (1/60 of a second for 60-cycle clocks; 1/50 of a second for 50-cycle clocks)

time is the two-word area to receive the internal format time: time(1) is the high-order time; time(2) is the low-order time

```txt
Errors:
    None.
Example:
        INTEGER*4 J1
        .
        .
        .
C CONVERT 3 HRS, 7 MIN, 23 SECONDS TO INTEGER *4 VALUE
CALL JTIME(3,7,23,0,J1)
CALL JJCVT(J1)
```

## 3.77 LEN

The LEN function returns the number of characters currently in the string contained in a specified array. This number is computed as the number of characters preceding the first null byte encountered. If the specified array contains a null string, a value of 0 is returned.

Form: $\mathbf{i} = \mathbf{LEN(a)}$

where:

a specifies the array containing the string, which must be terminated by a null byte

Errors:

None.

Example:

```txt
LOGICAL*1 STRNG(73)
:
:
.
TYPE 99,(STRNG(I),I=1,LEN(STRNG))
99 FORMAT('0',132A1)
```

## 3.78 LOCK

The LOCK subroutine keeps the USR in memory for a series of operations involving various RT-11 file management functions.

If all the conditions that cause swapping are satisfied, a portion of the user program is written out to the disk file SWAP,SYS and the USR is loaded. Otherwise, the USR in memory is used, and no swapping occurs. The USR is not released until an UNLOCK (see Section 3.112) is given. (Note that in an FB system, calling the CSI can also perform an implicit UNLOCK.) To save time in swapping, a program that has many USR requests to make can LOCK the USR in memory, make all the requests, and then UNLOCK the USR.

In an FB or XM environment, a LOCK inhibits another job from using the USR. Thus, the USR should be locked only for as long as necessary.

## NOTE

If any job does a LOCK, it can cause the USR to be unavailable for other jobs for a considerable period of time. The USR is not reentrant and only one job has use of the USR at a time, which should be considered for systems requiring concurrent foreground and background jobs. This is particularly true when magtape and/or cassette are active.

File operations by the USR require a sequential search of the tape for magtape and cassette. This could lock out the foreground job for a long time while the background job does a tape operation. The programmer should keep this in mind when designing such systems. The FB and XM monitors supply the ITLOCK routine, which permits the foreground job to check for the availability of the USR.

## Form: CALL LOCK

After a LOCK has been executed, the UNLOCK routine must be executed to release the USR from memory. The LOCK/UNLOCK routines are complementary and must be matched. That is, if three LOCKs are issued, at least three UNLOCKs must be done, otherwise the USR is not released. More UNLOCKs than LOCKs can occur without error; the extra UNLOCKs are ignored.

## Notes:

1. It is vital that the LOCK call not come from within the area into which the USR will be swapped. If this should occur, the return from the USR request would not be to the user program, but to the USR itself, since the LOCK function causes part of the user program to be saved on disk and replaced in memory by the USR. Furthermore, subroutines, variables, and arrays in the area where the USR is swapping should not be referenced while the USR is locked in memory.

2. Once a LOCK has been performed, it is not advisable for the program to destroy the area the USR is in, even though no further use of the USR is required. This causes unpredictable results when an UNLOCK is done.

3. LOCK cannot be called from a completion or interrupt routine.

4. If a SET USR NOSWAP command has been issued, LOCK and UNLOCK do not cause the USR to swap. However, in FB, LOCK still inhibits the other job from using the USR, and UNLOCK allows the other job access to the USR.

5. The USR cannot accept argument lists, such as device file name specifications, located in the area into which it has been locked.

Errors:

Example:

```txt
None.
nple:
INTEGER*2 DBLK(4)
DATA DBLK /3RDK ,3RDT,3RFIL,3RF4 /
.
.
.
CALL LOCK                      !LOCK THE USR IN MEMORY
ICHN=IGETC()                  !GET A CHANNEL TO USE
IF(LOOKUP(ICHN,DBLK),LT,0) STOP '?LOOKUP FAILED'
CALL UNLOCK                          !RELEASE THE USR
.
.
.
```

## 3.79 LOOKUP

The LOOKUP function associates a specified channel with a device and/or file for the purpose of performing I/O operations. The channel used is then busy until one of the following functions is executed.

CLOSEC or ICLOSE

ISAVES

PURGE

Form: i = LOOKUP (chan,dblk[,count,seqnum,])

i = LOOKUP (chan,jobdes)

## where:

chan is the integer specification for the RT-11 channel to be associated with the file. You must obtain this channel through an IGETC call, or you can use channel 16(decimal) or higher if you have done an ICDFN call

dblk is the four-word area specifying the Radix-50 file descriptor. Note that unpredictable results occur if the USR swaps over this four-word area

count         is an optional argument used for the cassette handler; this
            argument defaults to 0

seqnum is a file number. For cassette operations, if this argument is blank, a value of 0 is assumed

For magtape, it describes a file sequence number. The action taken depends on whether the file name is given or null. The sequence number can have the following values:

-1 Suppress rewind and search for the specified file name from the current tape position. If a file name is given, a file-structured lookup is performed (do not rewind). If the file name is null, a non-file-structured lookup is done (tape is not moved). You must specify a -1 and no other negative number.

0 Rewind to the beginning of the tape and do a non-file-structured lookup.

n Where n is any positive number. Position the tape at file sequence number n and check that the file names match. If the file names do not match, an error is generated. If the file name is null, a file-structured lookup is done on the file designated by seq-num.

## jobdes

is an argument that allows communication between jobs in a system job environment. It is a pointer to a four-word job descriptor of the job to which messages will be sent or received. The syntax is

jobdes → .RAD50 /MQ/

.ASCII /logical-job-name/

where the logical-job-name is six characters long. If the logical-job-name is zero, the channel will be opened only for .READ/C/W requests, and such requests will accept messages from any jobs.

If the jobdes argument is omitted, .LOOKUP operates as it did for Version 3B.

## NOTE

The arguments of LOOKUP must be positioned so that the USR does not swap over them.

The handler for the selected device must be in memory for a LOOKUP. If the first word of the file name in dblk is 0 and the device is a file-structured device, absolute block 0 of the device is designated as the beginning of the file. This technique, called a non-file-structured lookup, allows I/O to any physical block on the device. If a file name is specified for a device that is not file structured (such as LP:FILE.TYP), the name is ignored.

## NOTE

Since a non-file-structured lookup allows I/O to any physical block on the device, the user must be aware that, in this mode, it is possible to overwrite the RT-11 device directory, thus destroying all file information on the device.

## Function Results:

i = n    Indicates a successful file-structured lookup on a random-access storage volume.

i = 0 Indicates a successful non-file-structured lookup on both random-access and non-file-structured volumes, or a successful file-structured lookup on magtape.

## Errors:

$\times \quad \mathrm{i} = -1$ Channel specified is already open.

= -2 File specified was not found on the device.

$= -3$ Device in use.

= -4 Tape drive is not available.

= -5 Illegal argument error with a file-structured volume.

= -6 Illegal argument error with a non-file-structured volume.

## Example:

```txt
INTEGER*2 DBLK(4)
DATA DBLK/3RDK0,3RFTN,3R44 ,3RDAT/
.
.
.
ICHAN=IGETC()
IF(ICHAN,LT,O) STOP 'NO CHANNEL'
IF(IFETCH(DBLK),NE,O) STOP 'BAD FETCH'
IF(LOOKUP(ICHAN,DBLK),LT,O) STOP 'BAD LOOKUP'
.
.
.
```

```txt
CALL ICLOSE(ICHAN,I)
I = ICLOSE()
CALL IFREEC(ICHAN)
.
.
.
```

or using LOOKUP with a system job

```txt
LOGICAL*1 JNAM(6)
DIMENSION JBLK(4)
EQUIVALENCE (JNAM(1),JBLK(2))
DATA JNAM /'Q','U','E','U','E',0/
DATA JBLK(1) /3RMQ /
:
.
.
C OPEN A MESSAGE CHANNEL TO 'QUEUE'
ICHN=GETC()
IF(LOOKUP(ICHN,JBLK),LT,0) STOP 'QUEUE IS NOT RUNNING'
:
:
.
```
