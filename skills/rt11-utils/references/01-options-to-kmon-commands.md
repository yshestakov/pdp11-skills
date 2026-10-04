# Utility options and their keyboard-monitor (KMON) equivalents

From Table B-1 of the RT-11 System Utilities Manual (AA-M239B-TC). Left: utility run with `R <prog>` and a CSI command line (`*out=in/opt`). Right: the KMON command and option that do the same. OCR errors possible in individual cells; cross-check the utility chapter.

| Program | Option | KMON command | KMON option |
|---|---|---|---|
| BINCOM | /B | DIFFERENCES/BINARY | /BYTES |
| BINCOM | /D | DIFFERENCES/BINARY | /DEVICE |
| BINCOM | /E:n | DIFFERENCES/BINARY | /END[:n] |
| BINCOM | /H | * |  |
| BINCOM | /O | DIFFERENCES/BINARY | /ALWAYS |
| BINCOM | /Q | DIFFERENCES/BINARY | /QUIET |
| BINCOM | /S:n | DIFFERENCES/BINARY | /START[:n] |
| BUP |  | BACKUP | - |
| BUP | /I | BACKUP | /DEVICE |
| BUP | /L | DIRECTORY | /BACKUP |
| BUP | /X | BACKUP | /RESTORE |
| BUP | /Y | BACKUP | /NOQUERY |
| BUP | /Z | INITIALIZE | /BACKUP |
| DIR | /A | DIRECTORY | /ALPHABETIZE |
| DIR | /B | DIRECTORY | /BLOCKS (disks) /POSITION (magtapes) |
| DIR | /C:n | DIRECTORY | /COLUMNS:n |
| DIR | /D[:date] | DIRECTORY | /DATE[:date] |
| DIR | /E | DIRECTORY | /FULL |
| DIR | /F | DIRECTORY | /FAST |
| DIR | /G | DIRECTORY | /BEGIN |
| DIR | /J[:date] | DIRECTORY | /SINCE[:date] |
| DIR | /K[:date] | DIRECTORY | /BEFORE[:date] |
| DIR | /L | * |  |
| DIR | /M | DIRECTORY | /FREE |
| DIR | /N | DIRECTORY | /SUMMARY |
| DIR | /O | DIRECTORY | /OCTAL |
| DIR | /P | DIRECTORY | /EXCLUDE |
| DIR | /Q | DIRECTORY | /DELETED |
| DIR | /R | DIRECTORY | /REVERSE |
| DIR | /S[:xxx] | DIRECTORY | /SORT[:category] |
| DIR | /T | DIRECTORY | /PROTECTION |
| DIR | /U | DIRECTORY | /NOPROTECTION |
| DIR | /V[:ONL] | DIRECTORY | /VOLUMEID[:ONLY] |
| DUMP | /B | DUMP | /BYTES |
| DUMP | /E:n | DUMP | /END:n |
| DUMP | /G | DUMP | /IGNORE |
| DUMP | /N | DUMP | /NOASCII |
| DUMP | /O:n | DUMP | /ONLY:n |
| DUMP | /S:n | DUMP | /START:n |
| DUMP | /T | DUMP | /FOREIGN |
| DUMP | /W | DUMP | /WORDS |
| DUMP | /X | DUMP | /RAD50 |
| DUP | /B[:RET] | INITIALIZE | /BADBLOCKS[:RET] |
| DUP | /C | CREATE |  |
| DUP | /D | INITIALIZE | /RESTORE |
| DUP | /E:n | COPY | /END:n |
| DUP | /F | COPY, DIRECTORY | /FILES |
| DUP | /G:n | COPY, CREATE | /START:n * |
| DUP | /H |  |  |
| DUP | /I | COPY | /DEVICE |
| DUP | /L | ASSIGN, DEASSIGN |  |
| DUP | /K | DIRECTORY | /BADBLOCKS |
| DUP | /N:n | INITIALIZE | /SEGMENTS:n |
| DUP | /O | BOOT |  |
| DUP | /Q | BOOT | /FOREIGN |
| DUP | /R[:RET] | COPY | /RETAIN |
| DUP |  | INITIALIZE | /REPLACE[:RETAIN] |
| DUP | /S | SQUEEZE |  |
| DUP | /T:n | CREATE | /EXTENSION:n |
| DUP | /U[:xx] | COPY | /BOOT[:val] |
| DUP | /V[:ONL] | INITIALIZE | /VOLUMEID[:ONLY] |
| DUP | /W | DIRECTORY, COPY, INITIALIZE, SQUEEZE, BOOT | /WAIT |
| DUP | /X | * |  |
| DUP | /Y | COPY, INITIALIZE, SQUEEZE | /NOQUERY |
| DUP | /Z[:n] | INITIALIZE |  |
| ERROUT | /A | SHOW ERRORS | /ALL |
| ERROUT | /F:date | SHOW ERRORS | /FROM:date |
| ERROUT | /S | SHOW ERRORS | /SUMMARY |
| ERROUT | /T:date | SHOW ERRORS | /TO:date |
| FILEX | /A | COPY | /ASCII |
| FILEX | /D | DELETE |  |
| FILEX | /F | DIRECTORY | /FAST |
| FILEX | /I | COPY | /IMAGE |
| FILEX | /L | DIRECTORY |  |
| FILEX | /P | COPY | /PACKED |
| FILEX | /S | COPY | /DOS |
| FILEX | /T | COPY | /TOPS |
| FILEX | /U[:n.] | COPY | /INTERCHANGE[:size] |
| FILEX | /V[:ONL] | DIRECTORY, INITIALIZE | /VOLUMEID[:ONLY] |
| FILEX | /W | COPY, DELETE, DIRECTORY, INITIALIZE | /WAIT |
| FILEX | /Y | INITIALIZE | /NOQUERY |
| FILEX | /Z | INITIALIZE |  |
| FORMAT | /P:n | FORMAT | /PATTERN:value |
| FORMAT | /S | FORMAT | /SINGLEDENSITY |
| FORMAT | /V[:ONL] | FORMAT | /VERIFY[:ONLY] |
| FORMAT | /W | FORMAT | /WAIT |
| FORMAT | /Y | FORMAT | /NOQUERY |
| LD | /A:ddd | ASSIGN | - |
| LD | /C | SET LDn | CLEAN |
| LD | /L:n | MOUNT, DISMOUNT |  |
| LD | /R:n | MOUNT, DISMOUNT | NOWRITE |
| LD | /W:n | MOUNT, DISMOUNT | WRITE |
| LIBR | /A | * |  |
| LIBR | /C | LIBRARY | /PROMPT |
| LIBR | /D | LIBRARY | /DELETE |
| LIBR | /E | LIBRARY | /EXTRACT |
| LIBR | /G | LIBRARY | /REMOVE |
| LIBR | /M[:n] | LIBRARY | /MACRO[:n] |
| LIBR | /N | * |  |
| LIBR | /P | * |  |
| LIBR | /R | LIBRARY | /REPLACE |
| LIBR | /U | LIBRARY | /UPDATE |
| LIBR | /W | * |  |
| LIBR | /X | * |  |
| LIBR | // | * |  |
| LINK | /A | LINK | /ALPHABETIZE |
| LINK | /B:n | LINK | /BOTTOM:value |
| LINK | /C | LINK | /PROMPT |
| LINK | /D | LINK, EXECUTE | /DUPLICATE |
| LINK | /E:n | LINK | /EXTEND:n |
| LINK | /F | * |  |
| LINK | /G | * |  |
| LINK | /H:n | LINK | /TOP[:value] |
| LINK | /I | LINK | /INCLUDE |
| LINK | /K:n | LINK | /LIMIT:n |
| LINK | /L | LINK | /LDA |
| LINK | /M[:n] | LINK | /STACK[:value] |
| LINK | /N | LINK, EXECUTE | /GLOBAL |
| LINK | /O:n | * |  |
| LINK | /P:n | * |  |
| LINK | /Q | * |  |
| LINK | /R[:n] | LINK | /FOREGROUND[:STACKSIZE] |
| LINK | /S | LINK | /SLOWLY |
| LINK | /T[:n] | LINK | /TRANSFER[:value] |
| LINK | /U:n | LINK | /ROUND:n |
| LINK | /V:n[:m] | LINK | /XM |
| LINK | /W | LINK | /WIDE |
| LINK | /X | LINK | /NOBITMAP |
| LINK | /Y:n | LINK | /BOUNDARY:value |
| LINK | /Z:n | LINK | /FILL:n |
| LINK | // | * |  |
| MACRO | /C:arg | MACRO | /CROSSREFERENCE[:type[...:type]] |
| MACRO | /D:arg | MACRO | /DISABLE[:type[...:type]] |
| MACRO | /E:arg | MACRO | /ENABLE[:type[...:type]] |
| MACRO | /L:arg | MACRO | /SHOW:type |
| MACRO | /M | MACRO | /LIBRARY |
| MACRO | /N:arg | MACRO | /NOSHOW:type |
| PIP | /A | COPY | /ASCII |
| PIP | /B | COPY | /BINARY |
| PIP | /C[:date] | COPY, DELETE, PRINT PROTECT, RENAME TYPE, UNPROTECT | /DATE[:date], /NEWFILES |
| PIP | /D | DELETE | - |
| PIP |  | PRINT, TYPE | /DELETE |
| PIP | /E | COPY, DELETE, PRINT, PROTECT, RENAME TYPE, UNPROTECT | /WAIT |
| PIP | /F | COPY, RENAME PROTECT | /PROTECTION |
| PIP | /G | COPY | /IGNORE |
| PIP | /H | COPY | /VERIFY |
| PIP | /I[:date] | COPY, DELETE, PRINT, PROTECT, RENAME TYPE, UNPROTECT | /SINCE[:date] |
| PIP | /J[:date] | COPY, DELETE, PRINT, PROTECT, RENAME TYPE, UNPROTECT | /BEFORE[:date] |
| PIP | /K:n | PRINT, TYPE | /COPIES:n |
| PIP | /M:n | COPY, DELETE | /POSITION:n |
| PIP | /N | COPY, RENAME | /NOREPLACE |
| PIP | /O | COPY | /PREDELETE |
| PIP | /P | COPY, DELETE PROTECT, UNPROTECT | /EXCLUDE |
| PIP | /Q | COPY, DELETE, PRINT PROTECT, RENAME TYPE, UNPROTECT | /QUERY |
| PIP | /R | RENAME | - |
| PIP | /S | COPY | /SLOWLY |
| PIP | /T[:date] | COPY, PROTECT RENAME, UNPROTECT | /SETDATE[:date] |
| PIP | /U | COPY | /CONCATENATE |
| PIP | /V | COPY | /MULTIVOLUME |
| PIP | /W | COPY, DELETE, PRINT PROTECT, RENAME TYPE, UNPROTECT | /LOG |
| PIP | /X | COPY, DELETE, PRINT PROTECT, RENAME TYPE, UNPROTECT | /INFORMATION |
| PIP | /Y | COPY, DELETE, PRINT PROTECT, RENAME TYPE, UNPROTECT | /SYSTEM |
| PIP | /Z | COPY, RENAME UNPROTECT | /NOPROTECTION |
| QUEMAN | /A | * |  |
| QUEMAN | /C[:date] | PRINT | /DATE[:date], /NEWFILES |
| QUEMAN | /D | PRINT | /DELETE |
| QUEMAN | /H:n | PRINT | /FLAGPAGE:n |
| QUEMAN | /I[:date] | PRINT | /SINCE[:date] |
| QUEMAN | /J[:date] | PRINT | /BEFORE[:date] |
| QUEMAN | /K:n | PRINT | /COPIES:n |
| QUEMAN | /L | SHOW | QUEUE |
| QUEMAN | /M | DELETE | /ENTRY |
| QUEMAN | /N | PRINT | /NOFLAGPAGE |
| QUEMAN | /P | * |  |
| QUEMAN | /Q | PRINT | /QUERY |
| QUEMAN | /R | * |  |
| QUEMAN | /S | * |  |
| QUEMAN | /W | PRINT | /LOG |
| QUEMAN | /X | PRINT | /INFORMATION |
| QUEMAN | // | PRINT | /PROMPT |
| RESORC | /A | SHOW | ALL |
| RESORC | /C | * |  |
| RESORC | [dev:]/D | SHOW | DEVICES[dd:] |
| RESORC | /H | * |  |
| RESORC | /J | SHOW | JOBS |
| RESORC | /L | SHOW |  |
| RESORC | /M | * |  |
| RESORC | /O | * |  |
| RESORC | /Q | SHOW | QUEUE |
| RESORC | /S | SHOW | SUBSET |
| RESORC | /T | SHOW | TERMINALS |
| RESORC | /X | SHOW | MEMORY |
| RESORC | /Z | SHOW | CONFIGURATION |
| SRCCOM | /A | DIFFERENCES | /AUDITTRAIL |
| SRCCOM | /B | DIFFERENCES | /BLANKLINES |
| SRCCOM | /C | DIFFERENCES | /NOCOMMENTS |
| SRCCOM | /D | DIFFERENCES | /CHANGEBAR |
| SRCCOM | /F | DIFFERENCES | /FORMFEED |
| SRCCOM | /L:[n] | DIFFERENCES | /MATCH:[n] |
| SRCCOM | /S | DIFFERENCES | /NOSPACES |
| SRCCOM | /T | DIFFERENCES | /NOTRIM |
| SRCCOM | /V:i:d | * |  |
