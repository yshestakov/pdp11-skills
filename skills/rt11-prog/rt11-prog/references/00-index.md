# Index: every programmed request, SYSMAC macro and SYSLIB subroutine

§ numbers are RT-11 PRM (AA-H378C-TC) sections. Grep the file for `## <§>`; a few headings were lost in OCR - then grep the name (e.g. `\.GTLIN`).
Concepts: 01-programmed-request-concepts.md (Ch.1.1), 02-syslib-concepts.md (Ch.1.2). Real macro source: sysmac_v53.mac.


## Chapter 2 - programmed requests and SYSMAC macros

| § | Name | File |
| --- | --- | --- |
| 2.1 | .ABTIO | 03-requests-ABTIO-CTIMIO.md |
| 2.2 | .ADDR | 03-requests-ABTIO-CTIMIO.md |
| 2.3 | .ASSUME | 03-requests-ABTIO-CTIMIO.md |
| 2.4 | .BR | 03-requests-ABTIO-CTIMIO.md |
| 2.5 | .CDFN | 03-requests-ABTIO-CTIMIO.md |
| 2.6 | .CHAIN | 03-requests-ABTIO-CTIMIO.md |
| 2.7 | .CHCOPY (FB and XM Only) | 03-requests-ABTIO-CTIMIO.md |
| 2.8 | .CLOSE | 03-requests-ABTIO-CTIMIO.md |
| 2.9 | .CMKT (FB and XM; SJ Monitor Special Feature) | 03-requests-ABTIO-CTIMIO.md |
| 2.10 | .CNTXSW (FB and XM Only) | 03-requests-ABTIO-CTIMIO.md |
| 2.11 | .CRAW (XM Only) | 03-requests-ABTIO-CTIMIO.md |
| 2.12 | .CRRG (XM Only) | 03-requests-ABTIO-CTIMIO.md |
| 2.13 | .CSIGEN | 03-requests-ABTIO-CTIMIO.md |
| 2.14 | .CSISPC | 03-requests-ABTIO-CTIMIO.md |
| 2.15 | .CSTAT | 03-requests-ABTIO-CTIMIO.md |
| 2.16 | .CTIMIO (Device Handler Only) | 03-requests-ABTIO-CTIMIO.md |
| 2.17 | .DATE | 04-requests-DATE-LOOKUP.md |
| 2.18 | .DELETE | 04-requests-DATE-LOOKUP.md |
| 2.19 | .DEVICE (FB and XM Only) | 04-requests-DATE-LOOKUP.md |
| 2.20 | .DRAST (Device Handler Only) | 04-requests-DATE-LOOKUP.md |
| 2.21 | .DRBEG (Device Handler Only) | 04-requests-DATE-LOOKUP.md |
| 2.22 | .DRBOT (Device Handler Only) | 04-requests-DATE-LOOKUP.md |
| 2.23 | .DRDEF (Device Handler Only) | 04-requests-DATE-LOOKUP.md |
| 2.24 | .DREND (Device Handler Only) | 04-requests-DATE-LOOKUP.md |
| 2.25 | .DRFIN (Device Handler Only) | 04-requests-DATE-LOOKUP.md |
| 2.26 | .DRINS | 04-requests-DATE-LOOKUP.md |
| 2.27 | .DRSET (Device Handler Only) | 04-requests-DATE-LOOKUP.md |
| 2.28 | .DRVTB (Device Handler Only) | 04-requests-DATE-LOOKUP.md |
| 2.29 | .DSTATUS | 04-requests-DATE-LOOKUP.md |
| 2.30 | .ELAW (XM Only) | 04-requests-DATE-LOOKUP.md |
| 2.31 | .ELRG (XM Only) | 04-requests-DATE-LOOKUP.md |
| 2.32 | .ENTER | 04-requests-DATE-LOOKUP.md |
| 2.33 | .EXIT | 04-requests-DATE-LOOKUP.md |
| 2.34 | .FETCH/.RELEAS | 04-requests-DATE-LOOKUP.md |
| 2.35 | .FORK (Device Handler and Interrupt Service Routine Only) | 04-requests-DATE-LOOKUP.md |
| 2.36 | .FPROT | 04-requests-DATE-LOOKUP.md |
| 2.37 | .GMCX (XM Only) | 04-requests-DATE-LOOKUP.md |
| 2.38 | .GTIM | 04-requests-DATE-LOOKUP.md |
| 2.39 | .GTJB | 04-requests-DATE-LOOKUP.md |
| 2.40 | .GTLIN | 04-requests-DATE-LOOKUP.md |
| 2.41 | .GVAL/.PVAL | 04-requests-DATE-LOOKUP.md |
| 2.42 | .HERR/.SERR | 04-requests-DATE-LOOKUP.md |
| 2.43 | .HRESET | 04-requests-DATE-LOOKUP.md |
| 2.44 | .INTEN | 04-requests-DATE-LOOKUP.md |
| 2.45 | .LOCK/.UNLOCK | 04-requests-DATE-LOOKUP.md |
| 2.46 | .LOOKUP | 04-requests-DATE-LOOKUP.md |
| 2.47 | .MAP (XM Only) | 05-requests-MAP-SAVESTATUS.md |
| 2.48 | .MFPS/.MTPS | 05-requests-MAP-SAVESTATUS.md |
| 2.49 | .MRKT (FB and XM; SJ Monitor Special Feature) | 05-requests-MAP-SAVESTATUS.md |
| 2.50 | .MTATCH (Special Feature) | 05-requests-MAP-SAVESTATUS.md |
| 2.51 | .MTDTCH (Special Feature) | 05-requests-MAP-SAVESTATUS.md |
| 2.52 | .MTGET (Special Feature) | 05-requests-MAP-SAVESTATUS.md |
| 2.53 | .MTIN (Special Feature) | 05-requests-MAP-SAVESTATUS.md |
| 2.54 | .MTOUT (Special Feature) | 05-requests-MAP-SAVESTATUS.md |
| 2.55 | .MTPRNT (Special Feature) | 05-requests-MAP-SAVESTATUS.md |
| 2.56 | .MTPS | 05-requests-MAP-SAVESTATUS.md |
| 2.57 | .MTRCTO (Special Feature) | 05-requests-MAP-SAVESTATUS.md |
| 2.58 | .MTSET (Special Feature) | 05-requests-MAP-SAVESTATUS.md |
| 2.59 | .MTSTAT (Special Feature) | 05-requests-MAP-SAVESTATUS.md |
| 2.60 | .MWAIT (FB and XM Only) | 05-requests-MAP-SAVESTATUS.md |
| 2.61 | .PEEK/.POKE | 05-requests-MAP-SAVESTATUS.md |
| 2.62 | .POKE | 05-requests-MAP-SAVESTATUS.md |
| 2.63 | .PRINT | 05-requests-MAP-SAVESTATUS.md |
| 2.64 | .PROTECT/.UNPROTECT (FB and XM Only) | 05-requests-MAP-SAVESTATUS.md |
| 2.65 | .PURGE | 05-requests-MAP-SAVESTATUS.md |
| 2.66 | .PVAL | 05-requests-MAP-SAVESTATUS.md |
| 2.67 | .QELDF (Device Handler Only) | 05-requests-MAP-SAVESTATUS.md |
| 2.68 | .QSET | 05-requests-MAP-SAVESTATUS.md |
| 2.69 | .RCTRLO | 05-requests-MAP-SAVESTATUS.md |
| 2.70 | .RCVD/.RCVDC/.RCVDW (FB and XM Only) | 05-requests-MAP-SAVESTATUS.md |
| 2.71 | .RDBBK (XM Only) | 05-requests-MAP-SAVESTATUS.md |
| 2.72 | .RDBDF (XM Only) | 05-requests-MAP-SAVESTATUS.md |
| 2.73 | .READ/.READC/.READW | 05-requests-MAP-SAVESTATUS.md |
| 2.74 | .RELEAS | 05-requests-MAP-SAVESTATUS.md |
| 2.75 | .RENAME | 05-requests-MAP-SAVESTATUS.md |
| 2.76 | .REOPEN | 05-requests-MAP-SAVESTATUS.md |
| 2.77 | .RSUM (FB and XM Only) | 05-requests-MAP-SAVESTATUS.md |
| 2.78 | .SAVESTATUS | 05-requests-MAP-SAVESTATUS.md |
| 2.79 | .SCCA | 06-requests-SCCA-WRITE.md |
| 2.80 | .SDAT/.SDATC/.SDATW (FB and XM Only) | 06-requests-SCCA-WRITE.md |
| 2.81 | .SDTTM | 06-requests-SCCA-WRITE.md |
| 2.82 | .SERR | 06-requests-SCCA-WRITE.md |
| 2.83 | .SETTOP | 06-requests-SCCA-WRITE.md |
| 2.84 | .SFDAT | 06-requests-SCCA-WRITE.md |
| 2.85 | .SFPA (Special Feature) | 06-requests-SCCA-WRITE.md |
| 2.86 | .SOB | 06-requests-SCCA-WRITE.md |
| 2.87 | .SPCPS (FB and XM SYSGEN Option) | 06-requests-SCCA-WRITE.md |
| 2.88 | .SPFUN | 06-requests-SCCA-WRITE.md |
| 2.89 | .SPND/.RSUM (FB and XM Only) | 06-requests-SCCA-WRITE.md |
| 2.90 | .SRESET | 06-requests-SCCA-WRITE.md |
| 2.91 | .SYNCH (Device Handler and Interrupt Service Routine Only) | 06-requests-SCCA-WRITE.md |
| 2.92 | .TIMIO (Device Handler Only) | 06-requests-SCCA-WRITE.md |
| 2.93 | .TLOCK | 06-requests-SCCA-WRITE.md |
| 2.94 | .TRPSET | 06-requests-SCCA-WRITE.md |
| 2.95 | .TTYIN/.TTINR | 06-requests-SCCA-WRITE.md |
| 2.96 | .TTYOUT/.TTOUTR | 06-requests-SCCA-WRITE.md |
| 2.97 | .TWAIT (SYSGEN Option for SJ) | 06-requests-SCCA-WRITE.md |
| 2.98 | .UNLOCK | 06-requests-SCCA-WRITE.md |
| 2.99 | .UNMAP (XM Only) | 06-requests-SCCA-WRITE.md |
| 2.100 | .UNPROTECT | 06-requests-SCCA-WRITE.md |
| 2.101 | .WAIT | 06-requests-SCCA-WRITE.md |
| 2.102 | .WDBBK (XM Only) | 06-requests-SCCA-WRITE.md |
| 2.103 | .WDBDF (XM Only) | 06-requests-SCCA-WRITE.md |
| 2.104 | .WRITE/.WRITC/.WRITW | 06-requests-SCCA-WRITE.md |

## Chapter 3 - SYSLIB subroutines (FORTRAN-callable)

| § | Name | File |
| --- | --- | --- |
| 3.1 | AJFLT | 07-syslib-AJFLT-IQSET.md |
| 3.2 | CHAIN | 07-syslib-AJFLT-IQSET.md |
| 3.3 | CLOSEC/ICLOSE | 07-syslib-AJFLT-IQSET.md |
| 3.4 | CONCAT | 07-syslib-AJFLT-IQSET.md |
| 3.5 | CVTTIM | 07-syslib-AJFLT-IQSET.md |
| 3.6 | DEVICE (FB and XM Only) | 07-syslib-AJFLT-IQSET.md |
| 3.7 | DJFLT | 07-syslib-AJFLT-IQSET.md |
| 3.8 | GETSTR | 07-syslib-AJFLT-IQSET.md |
| 3.9 | GTIM | 07-syslib-AJFLT-IQSET.md |
| 3.10 | GTJB/IGTJB | 07-syslib-AJFLT-IQSET.md |
| 3.11 | GTLIN | 07-syslib-AJFLT-IQSET.md |
| 3.12 | IABTIO | 07-syslib-AJFLT-IQSET.md |
| 3.13 | IADDR | 07-syslib-AJFLT-IQSET.md |
| 3.14 | IAJFLT | 07-syslib-AJFLT-IQSET.md |
| 3.15 | IASIGN | 07-syslib-AJFLT-IQSET.md |
| 3.16 | ICDFN | 07-syslib-AJFLT-IQSET.md |
| 3.17 | ICHCPY (FB and XM Only) | 07-syslib-AJFLT-IQSET.md |
| 3.18 | ICLOSE | 07-syslib-AJFLT-IQSET.md |
| 3.19 | ICMKT | 07-syslib-AJFLT-IQSET.md |
| 3.20 | ICSI | 07-syslib-AJFLT-IQSET.md |
| 3.21 | ICSTAT | 07-syslib-AJFLT-IQSET.md |
| 3.22 | IDELET | 07-syslib-AJFLT-IQSET.md |
| 3.23 | IDJFLT | 07-syslib-AJFLT-IQSET.md |
| 3.24 | IDSTAT | 07-syslib-AJFLT-IQSET.md |
| 3.25 | IENTER | 07-syslib-AJFLT-IQSET.md |
| 3.26 | IFETCH | 07-syslib-AJFLT-IQSET.md |
| 3.27 | IFPROT | 07-syslib-AJFLT-IQSET.md |
| 3.28 | IFREEC | 07-syslib-AJFLT-IQSET.md |
| 3.29 | IGETC | 07-syslib-AJFLT-IQSET.md |
| 3.30 | IGETSP | 07-syslib-AJFLT-IQSET.md |
| 3.31 | IGTJB | 07-syslib-AJFLT-IQSET.md |
| 3.32 | IJCVT | 07-syslib-AJFLT-IQSET.md |
| 3.33 | ILUN | 07-syslib-AJFLT-IQSET.md |
| 3.34 | INDEX | 07-syslib-AJFLT-IQSET.md |
| 3.35 | INSERT | 07-syslib-AJFLT-IQSET.md |
| 3.36 | INTSET | 07-syslib-AJFLT-IQSET.md |
| 3.37 | IPEEK | 07-syslib-AJFLT-IQSET.md |
| 3.38 | IPEEKB | 07-syslib-AJFLT-IQSET.md |
| 3.39 | IPOKE | 07-syslib-AJFLT-IQSET.md |
| 3.40 | IPOKEB | 07-syslib-AJFLT-IQSET.md |
| 3.41 | IPUT | 07-syslib-AJFLT-IQSET.md |
| 3.42 | IQSET | 07-syslib-AJFLT-IQSET.md |
| 3.43 | IRAD50 | 07-syslib-AJFLT-IQSET.md |
| 3.44 | IRCVD/IRCVDC/IRCVDF/IRCVDW (FB and XM Only) | 08-syslib-IRAD50-LOCK.md |
| 3.45 | IREAD/IREADC/IREADF/IREADW | 08-syslib-IRAD50-LOCK.md |
| 3.46 | IRENAM | 08-syslib-IRAD50-LOCK.md |
| 3.47 | IREOPN | 08-syslib-IRAD50-LOCK.md |
| 3.48 | ISAVES | 08-syslib-IRAD50-LOCK.md |
| 3.49 | ISCHED | 08-syslib-IRAD50-LOCK.md |
| 3.50 | ISCOMP | 08-syslib-IRAD50-LOCK.md |
| 3.51 | ISDAT/ISDATC/ISDATF/ISDATW (FB and XM Only) | 08-syslib-IRAD50-LOCK.md |
| 3.52 | ISDTTM | 08-syslib-IRAD50-LOCK.md |
| 3.53 | ISFDAT | 08-syslib-IRAD50-LOCK.md |
| 3.54 | ISLEEP | 08-syslib-IRAD50-LOCK.md |
| 3.55 | ISPFN/ISPFNC/ISPFNF/ISPFNW | 08-syslib-IRAD50-LOCK.md |
| 3.56 | ISPY | 08-syslib-IRAD50-LOCK.md |
| 3.57 | ITIMER | 08-syslib-IRAD50-LOCK.md |
| 3.58 | ITLOCK (FB and XM Only) | 08-syslib-IRAD50-LOCK.md |
| 3.59 | ITTINR | 08-syslib-IRAD50-LOCK.md |
| 3.60 | ITTOUR | 08-syslib-IRAD50-LOCK.md |
| 3.61 | ITWAIT (SYSGEN Option in SJ) | 08-syslib-IRAD50-LOCK.md |
| 3.62 | IUNTIL (SYSGEN Option in SJ) | 08-syslib-IRAD50-LOCK.md |
| 3.63 | IVERIF | 08-syslib-IRAD50-LOCK.md |
| 3.64 | IWAIT | 08-syslib-IRAD50-LOCK.md |
| 3.65 | IWRITE/IWRITC/IWRITF/IWRITW | 08-syslib-IRAD50-LOCK.md |
| 3.66 | JADD | 08-syslib-IRAD50-LOCK.md |
| 3.67 | JAFIX | 08-syslib-IRAD50-LOCK.md |
| 3.68 | JCMP | 08-syslib-IRAD50-LOCK.md |
| 3.69 | JDFIX | 08-syslib-IRAD50-LOCK.md |
| 3.70 | JDIV | 08-syslib-IRAD50-LOCK.md |
| 3.71 | JICVT | 08-syslib-IRAD50-LOCK.md |
| 3.72 | JJCVT | 08-syslib-IRAD50-LOCK.md |
| 3.73 | JMOV | 08-syslib-IRAD50-LOCK.md |
| 3.74 | JMUL | 08-syslib-IRAD50-LOCK.md |
| 3.75 | JSUB | 08-syslib-IRAD50-LOCK.md |
| 3.76 | JTIME | 08-syslib-IRAD50-LOCK.md |
| 3.77 | LEN | 08-syslib-IRAD50-LOCK.md |
| 3.78 | LOCK | 08-syslib-IRAD50-LOCK.md |
| 3.79 | LOOKUP | 08-syslib-IRAD50-LOCK.md |
| 3.80 | MRKT (SYSGEN Option in SJ) | 09-syslib-MRKT-VERIFY.md |
| 3.81 | MTATCH (Special Feature) | 09-syslib-MRKT-VERIFY.md |
| 3.82 | MTDTCH (Special Feature) | 09-syslib-MRKT-VERIFY.md |
| 3.83 | MTGET (Special Feature) | 09-syslib-MRKT-VERIFY.md |
| 3.84 | MTIN (Special Feature) | 09-syslib-MRKT-VERIFY.md |
| 3.85 | MTOUT (Special Feature) | 09-syslib-MRKT-VERIFY.md |
| 3.86 | MTPRNT (Special Feature) | 09-syslib-MRKT-VERIFY.md |
| 3.87 | MTRCTO (Special Feature) | 09-syslib-MRKT-VERIFY.md |
| 3.88 | MTSET (Special Feature) | 09-syslib-MRKT-VERIFY.md |
| 3.89 | MTSTAT (Special Feature) | 09-syslib-MRKT-VERIFY.md |
| 3.90 | MWAIT (FB and XM Only) | 09-syslib-MRKT-VERIFY.md |
| 3.91 | PRINT | 09-syslib-MRKT-VERIFY.md |
| 3.92 | PURGE | 09-syslib-MRKT-VERIFY.md |
| 3.93 | PUTSTR | 09-syslib-MRKT-VERIFY.md |
| 3.94 | R50ASC | 09-syslib-MRKT-VERIFY.md |
| 3.95 | RAD50 | 09-syslib-MRKT-VERIFY.md |
| 3.96 | RCHAIN | 09-syslib-MRKT-VERIFY.md |
| 3.97 | RCTRLLO | 09-syslib-MRKT-VERIFY.md |
| 3.98 | REPEAT | 09-syslib-MRKT-VERIFY.md |
| 3.99 | RESUME (FB and XM Only) | 09-syslib-MRKT-VERIFY.md |
| 3.100 | SCCA | 09-syslib-MRKT-VERIFY.md |
| 3.101 | SCOMP/ISCOMP | 09-syslib-MRKT-VERIFY.md |
| 3.102 | SCOPY | 09-syslib-MRKT-VERIFY.md |
| 3.103 | SECNDS | 09-syslib-MRKT-VERIFY.md |
| 3.104 | SETCMD | 09-syslib-MRKT-VERIFY.md |
| 3.105 | STRPAD | 09-syslib-MRKT-VERIFY.md |
| 3.106 | SUBSTR | 09-syslib-MRKT-VERIFY.md |
| 3.107 | SUSPND (FB and XM Only) | 09-syslib-MRKT-VERIFY.md |
| 3.108 | TIMASC | 09-syslib-MRKT-VERIFY.md |
| 3.109 | TIME | 09-syslib-MRKT-VERIFY.md |
| 3.110 | TRANSL | 09-syslib-MRKT-VERIFY.md |
| 3.111 | TRIM | 09-syslib-MRKT-VERIFY.md |
| 3.112 | UNLOCK | 09-syslib-MRKT-VERIFY.md |
| 3.113 | VERIFY | 09-syslib-MRKT-VERIFY.md |

## Appendix A - display file handler

| § | Name | File |
| --- | --- | --- |
| A.1 | Description | 10-display-file-handler.md |
| A.2 | Description of Graphics Macros | 10-display-file-handler.md |
| A.3 | Extended Display Instructions | 10-display-file-handler.md |
| A.4 | Using the Display File Handler | 10-display-file-handler.md |
| A.5 | Display File Structure | 10-display-file-handler.md |
| A.6 | Summary of Graphics MACRO Calls | 10-display-file-handler.md |
| A.7 | Display Processor Mnemonics | 10-display-file-handler.md |
| A.8 | Assembly Instructions | 10-display-file-handler.md |
| A.9 | VTMAC | 10-display-file-handler.md |
| A.10 | Examples Using GTON | 10-display-file-handler.md |
