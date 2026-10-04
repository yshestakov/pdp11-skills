# RT-11 System Utilities Manual: Ch.5 DUMP: octal/ASCII/RAD50 dumps of files and devices

Source: RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1), OCR-converted. OCR noise: '.' may read as ',', 'R0' as 'RO', option slashes may be lost; check the option tables.

Contents:
- 5.1 Calling And Terminating DUMP
- 5.2 DUMP Command String Syntax
- 5.3 Options
- 5.4 Example Commands and Listings

---

# Chapter 5 Dump Program (DUMP)

The DUMP program prints on the console or line printer, or writes to a file, all or any part of a file as words or bytes (in octal), ASCII characters, or Radix-50 characters. DUMP is particularly useful for examining directories and files that contain binary data.

## 5.1 Calling And Terminating DUMP

To call the DUMP program from the system device, respond to the dot (.) printed by the keyboard monitor by typing:

• R DUMP RET

The Command String Interpreter (CSI) prints an asterisk at the left margin of the console terminal when it is ready to accept a command line. If you respond to the asterisk by typing only a carriage return, DUMP prints its current version number.

You can type CTRL/C to halt DUMP and return control to the monitor when DUMP is waiting for input from the console terminal. You must type two CTRL/Cs to abort DUMP at any other time. To restart DUMP, type R DUMP or REENTER in response to the monitor's dot.

## 5.2 DUMP Command String Syntax

Chapter 1, Command String Interpreter, describes the general syntax of the command line that DUMP accepts. If you do not specify an output file, the listing prints on the line printer. If you do not specify a file type for an output file, the system uses .DMP.

## 5.3 Options

Table 5-1 summarizes the options that are valid for DUMP.

Table 5-1: DUMP Options

| Option | Function |
| --- | --- |
| /B | Outputs bytes, in octal. |
| /E:n | Ends output at block n, where n is an octal block number. |
| /G | Ignores input errors. |
| /N | Suppresses ASCII output. |
| /O:n | Outputs only block n, where n is an octal block number. With this option, you can dump only one block for each command line. |
| /S:n | Starts output with block n, where n is an octal block number. For random-access devices, n may not be greater than the number of blocks in the file. |
| /T | Defines a tape as non-file-structured. |
| /W | Outputs words, in octal (the default mode). |
| /X | Outputs Radix-50 characters. |

ASCII characters are always dumped unless you type /N.

If you specify an input file name, the block numbers (n) you supply are relative to the beginning of that file. If you do not specify a file name, that is, if you are dumping a device, the block numbers are the absolute (physical) block numbers on that device. Remember that the first block of any file or device is block 0.

## NOTE

## DUMP does not print data from track 0 of diskettes.

DUMP handles operations that involve magtape differently from operations involving random-access devices.

If you dump an RT-11 file-structured tape and specify only a device name in the input specification, DUMP reads only as far as the logical EOF1. Logical end-of-tape is indicated by an end-of-file label followed by two tape marks. For non-file-structured tape, logical end-of-tape is indicated by two consecutive tape marks. For magtape dumps, tape mark messages appear in the output listing as DUMP encounters them on the tape.

If you use /S:n with magtape, n can be any positive value. However, an error can occur if n is greater than the number of blocks written on the tape. For example, if a tape has 100 written blocks and n is 110, an error can occur if DUMP accesses past the 100th block. If you specify /E:n, DUMP reads the tape from its starting position (block 0, unless you specify otherwise) to block n or to logical end-of-tape, whichever comes first.

## 5.4 Example Commands and Listings

This section includes sample DUMP commands and the listings they produce.

The following command string directs DUMP to print, in words, information contained in block 1 of the file DMPX.SAV stored on device DK:.

\* DMPX.SAV/0:1

<table><tr><td colspan="10">DMPX.SAV/O:1</td></tr><tr><td colspan="10">BLOCK NUMBER 000001</td></tr><tr><td>000/</td><td>000000</td><td>042062</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,.2D...........*</td></tr><tr><td>020/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>040/</td><td>000000</td><td>000000</td><td>001002</td><td>000000</td><td>000000</td><td>003356</td><td>001010</td><td>001104</td><td>*,........n...D.*</td></tr><tr><td>060/</td><td>000014</td><td>000400</td><td>004001</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>100/</td><td>000000</td><td>000000</td><td>045504</td><td>043072</td><td>046111</td><td>030505</td><td>044456</td><td>046523</td><td>*,..DK:FILE1.ISM*</td></tr><tr><td>120/</td><td>000000</td><td>046061</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,.1L...........*</td></tr><tr><td>140/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>160/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>001356</td><td>002000</td><td>001234</td><td>*,........n...*</td></tr><tr><td>200/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>220/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>240/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>260/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>300/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>320/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>340/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>360/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>400/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>420/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>440/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>460/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>500/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>520/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000080</td><td>000000</td><td>000000</td><td>000000</td><td>*,...........*</td></tr><tr><td>540/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000080</td><td>000080</td><td>000080</td><td>000080</td><td>*,...........*</td></tr><tr><td>560/</td><td>000000</td><td>000000</td><td>000080</td><td>0008888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>600/</td><td>0000888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>620/</td><td>00088888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>640/</td><td>000888888888888888888888888888888888888888888888888888888888888888888888888888888888</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>660/</td><td>000888888888888888888888888888888888888888888888888888888888888888888888</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>700/</td><td>0008888888888888888888888888888888888888888888888888</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>720/</td><td>00088888888888888888888888888888888888888</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>740/</td><td>00088888888888888888888888888888888888</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>760/</td><td>000888888888888888888888888888</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

In the printout above, the heading shows which block of the file follows. The numbers in the leftmost column indicate the byte offset from the beginning of the block. Remember that these are all octal values and that there are two bytes per word. The words that were dumped appear in the next eight columns. The rightmost column contains the ASCII equivalent of each word. DUMP substitutes a dot (.) for nonprinting codes, such as those for control characters.

The next command dumps block 1 of file PIP.SAV. The /N option suppresses ASCII output.

\* PIP.SAV/N/O:1

<table><tr><td colspan="9">SY:PIP.SAV/N/D:1</td></tr><tr><td colspan="9">BLOCK NUMBER 000001</td></tr><tr><td>000/</td><td>060502</td><td>010046</td><td>010146</td><td>010246</td><td>000422</td><td>062701</td><td>001100</td><td>012102</td></tr><tr><td>020/</td><td>022512</td><td>001406</td><td>012100</td><td>005046</td><td>011146</td><td>010246</td><td>104217</td><td>103405</td></tr><tr><td>040/</td><td>012602</td><td>012601</td><td>012600</td><td>011505</td><td>000205</td><td>104376</td><td>175400</td><td>012767</td></tr><tr><td>060/</td><td>011501</td><td>177724</td><td>016701</td><td>000012</td><td>005021</td><td>020167</td><td>000006</td><td>103774</td></tr><tr><td>100/</td><td>000743</td><td>005562</td><td>015260</td><td>005562</td><td>000006</td><td>002112</td><td>005562</td><td>000013</td></tr><tr><td>120/</td><td>003147</td><td>014100</td><td>000022</td><td>000211</td><td>014100</td><td>000023</td><td>000423</td><td>014100</td></tr><tr><td>140/</td><td>000025</td><td>000470</td><td>004537</td><td>001002</td><td>000006</td><td>006456</td><td>004537</td><td>001002</td></tr><tr><td>160/</td><td>000014</td><td>005764</td><td>004537</td><td>001002</td><td>000022</td><td>014102</td><td>004537</td><td>001002</td></tr><tr><td>200/</td><td>000030</td><td>014102</td><td>004537</td><td>001002</td><td>000036</td><td>014120</td><td>000000</td><td>000000</td></tr><tr><td>220/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>240/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>260/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>300/</td><td>000000</td><td>000000</td><td>000000</td><td>001000</td><td>015260</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>320/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>340/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>360/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>400/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>420/</td><td>000000</td><td>000000</td><td>002056</td><td>002063</td><td>003452</td><td>000000</td><td>005020</td><td>000000</td></tr><tr><td>440/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>460/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>500/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>520/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>540/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>560/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>600/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>620/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>640/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>660/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>0000Q</td><td>000000</td><td>000000</td><td>000000</td></tr><tr><td>700/</td><td>000000</td><td>000000</td><td>000000</td><td>000000</td><td>0000Q</td><td>0000Q</td><td>0000Q</td><td>000Q</td></tr><tr><td>720/</td><td>000Q</td><td>00Q</td><td>Q</td><td>Q</td><td>Q</td><td>Q</td><td>Q</td><td>Q</td></tr><tr><td>740/</td><td>Q</td><td>Q</td><td>Q</td><td>Q</td><td>Q</td><td>Q</td><td>Q</td><td>Q</td></tr><tr><td>760/</td><td>Q</td><td>Q</td><td>Q</td><td>Q</td><td>Q</td><td>Q</td><td>Q</td><td>Q</td></tr></table>

The following command dumps block 1 of SYSMAC.MAC in bytes. ASCII equivalents appear underneath each byte.

\* SYSMAC + MAC / B / 0 : 1

<table><tr><td colspan="17">SY:SYSMAC,MAC/B/D:1</td></tr><tr><td colspan="17">BLOCK NUMBER 000001</td></tr><tr><td>000/</td><td>120</td><td>040</td><td>117</td><td>106</td><td>040</td><td>040</td><td>124</td><td>110</td><td>105</td><td>040</td><td>040</td><td>123</td><td>117</td><td>106</td><td>124</td><td>127</td></tr><tr><td></td><td>P</td><td></td><td>D</td><td>F</td><td></td><td></td><td>T</td><td>H</td><td>E</td><td></td><td></td><td>S</td><td>O</td><td>F</td><td>T</td><td>W</td></tr><tr><td>020/</td><td>101</td><td>122</td><td>105</td><td>040</td><td>040</td><td>111</td><td>123</td><td>040</td><td>040</td><td>110</td><td>105</td><td>122</td><td>105</td><td>102</td><td>131</td><td>015</td></tr><tr><td></td><td>A</td><td>R</td><td>E</td><td></td><td></td><td>I</td><td>S</td><td></td><td></td><td>H</td><td>E</td><td>R</td><td>E</td><td>B</td><td>Y</td><td>.</td></tr><tr><td>040/</td><td>012</td><td>073</td><td>040</td><td>124</td><td>122</td><td>101</td><td>116</td><td>123</td><td>106</td><td>105</td><td>122</td><td>122</td><td>105</td><td>104</td><td>056</td><td>015</td></tr><tr><td></td><td>.</td><td>;</td><td></td><td>T</td><td>R</td><td>A</td><td>N</td><td>S</td><td>F</td><td>E</td><td>R</td><td>R</td><td>E</td><td>D</td><td>.</td><td>.</td></tr><tr><td>060/</td><td>012</td><td>073</td><td>015</td><td>012</td><td>073</td><td>040</td><td>124</td><td>110</td><td>105</td><td>040</td><td>111</td><td>116</td><td>106</td><td>117</td><td>122</td><td>115</td></tr><tr><td></td><td>.</td><td>;</td><td>.</td><td>.</td><td>;</td><td></td><td>T</td><td>H</td><td>E</td><td></td><td>I</td><td>N</td><td>F</td><td>O</td><td>R</td><td>M</td></tr><tr><td>100/</td><td>101</td><td>124</td><td>111</td><td>117</td><td>116</td><td>040</td><td>111</td><td>116</td><td>040</td><td>124</td><td>110</td><td>111</td><td>123</td><td>040</td><td>123</td><td>117</td></tr><tr><td></td><td>A</td><td>T</td><td>I</td><td>O</td><td>N</td><td></td><td>I</td><td>N</td><td></td><td>T</td><td>H</td><td>I</td><td>S</td><td></td><td>S</td><td>O</td></tr><tr><td>120/</td><td>106</td><td>124</td><td>127</td><td>101</td><td>122</td><td>105</td><td>040</td><td>111</td><td>123</td><td>040</td><td>123</td><td>125</td><td>102</td><td>112</td><td>105</td><td>103</td></tr><tr><td></td><td>F</td><td>T</td><td>W</td><td>A</td><td>R</td><td>E</td><td></td><td>I</td><td>S</td><td></td><td>S</td><td>U</td><td>B</td><td>J</td><td>E</td><td>C</td></tr><tr><td>140/</td><td>124</td><td>040</td><td>124</td><td>117</td><td>040</td><td>103</td><td>110</td><td>101</td><td>116</td><td>107</td><td>105</td><td>040</td><td>040</td><td>127</td><td>111</td><td>124</td></tr><tr><td></td><td>T</td><td></td><td>T</td><td>O</td><td></td><td>C</td><td>H</td><td>A</td><td>N</td><td>G</td><td>E</td><td></td><td></td><td>W</td><td>I</td><td>T</td></tr><tr><td>160/</td><td>110</td><td>117</td><td>125</td><td>124</td><td>040</td><td>040</td><td>116</td><td>117</td><td>124</td><td>111</td><td>103</td><td>105</td><td>015</td><td>012</td><td>073</td><td>040</td></tr><tr><td></td><td>H</td><td>O</td><td>U</td><td>T</td><td></td><td></td><td>N</td><td>O</td><td>T</td><td>I</td><td>C</td><td>E</td><td>.</td><td>.</td><td>;</td><td></td></tr><tr><td>200/</td><td>101</td><td>116</td><td>104</td><td>040</td><td>040</td><td>123</td><td>110</td><td>117</td><td>125</td><td>114</td><td>104</td><td>040</td><td>040</td><td>116</td><td>117</td><td>124</td></tr><tr><td></td><td>A</td><td>N</td><td>D</td><td></td><td></td><td>S</td><td>H</td><td>O</td><td>U</td><td>L</td><td>D</td><td></td><td></td><td>N</td><td>O</td><td>T</td></tr><tr><td>220/</td><td>040</td><td>040</td><td>102</td><td>105</td><td>040</td><td>040</td><td>103</td><td>117</td><td>116</td><td>123</td><td>124</td><td>122</td><td>125</td><td>105</td><td>104</td><td>040</td></tr><tr><td></td><td></td><td></td><td>B</td><td>E</td><td></td><td></td><td>C</td><td>O</td><td>N</td><td>S</td><td>T</td><td>R</td><td>U</td><td>E</td><td>D</td><td></td></tr><tr><td>240/</td><td>040</td><td>101</td><td>123</td><td>040</td><td>040</td><td>101</td><td>040</td><td>103</td><td>117</td><td>115</td><td>115</td><td>111</td><td>124</td><td>115</td><td>105</td><td>116</td></tr><tr><td></td><td></td><td>A</td><td>S</td><td></td><td></td><td>A</td><td></td><td>C</td><td>O</td><td>M</td><td>M</td><td>I</td><td>T</td><td>M</td><td>E</td><td>N</td></tr><tr><td>260/</td><td>124</td><td>040</td><td>102</td><td>131</td><td>040</td><td>104</td><td>111</td><td>107</td><td>111</td><td>124</td><td>101</td><td>114</td><td>040</td><td>105</td><td>121</td><td>125</td></tr><tr><td></td><td>T</td><td></td><td>B</td><td>Y</td><td></td><td>D</td><td>I</td><td>G</td><td>I</td><td>T</td><td>A</td><td>L</td><td></td><td>E</td><td>Q</td><td>U</td></tr><tr><td>300/</td><td>111</td><td>120</td><td>115</td><td>105</td><td>116</td><td>124</td><td>015</td><td>012</td><td>073</td><td>040</td><td>103</td><td>117</td><td>122</td><td>120</td><td>117</td><td>122</td></tr><tr><td></td><td>I</td><td>P</td><td>M</td><td>E</td><td>N</td><td>T</td><td>.</td><td>.</td><td>;</td><td></td><td>C</td><td>O</td><td>R</td><td>P</td><td>O</td><td>R</td></tr><tr><td>320/</td><td>101</td><td>124</td><td>111</td><td>117</td><td>116</td><td>056</td><td>015</td><td>012</td><td>073</td><td>015</td><td>012</td><td>073</td><td>040</td><td>104</td><td>111</td><td>107</td></tr><tr><td></td><td>A</td><td>T</td><td>I</td><td>O</td><td>N</td><td>,</td><td>.</td><td>.</td><td>;</td><td>.</td><td>.</td><td>;</td><td></td><td>D</td><td>I</td><td>G</td></tr><tr><td>340/</td><td>111</td><td>124</td><td>101</td><td>114</td><td>040</td><td>101</td><td>123</td><td>123</td><td>125</td><td>115</td><td>105</td><td>123</td><td>040</td><td>116</td><td>117</td><td>040</td></tr><tr><td></td><td>I</td><td>T</td><td>A</td><td>L</td><td></td><td>A</td><td>S</td><td>S</td><td>U</td><td>M</td><td>E</td><td>S</td><td></td><td>N</td><td>O</td><td></td></tr><tr><td>360/</td><td>122</td><td>105</td><td>123</td><td>120</td><td>117</td><td>116</td><td>123</td><td>111</td><td>102</td><td>111</td><td>114</td><td>111</td><td>124</td><td>131</td><td>040</td><td>106</td></tr><tr><td></td><td>R</td><td>E</td><td>S</td><td>P</td><td>O</td><td>N</td><td>S</td><td>I</td><td>B</td><td>I</td><td>L</td><td>I</td><td>T</td><td>Y</td><td></td><td>F</td></tr><tr><td>400/</td><td>117</td><td>122</td><td>040</td><td>124</td><td>110</td><td>105</td><td>040</td><td>125</td><td>123</td><td>105</td><td>040</td><td>117</td><td>122</td><td>040</td><td>040</td><td>122</td></tr><tr><td></td><td>O</td><td>R</td><td></td><td>T</td><td>H</td><td>E</td><td></td><td>U</td><td>S</td><td>E</td><td></td><td>O</td><td>R</td><td></td><td></td><td>R</td></tr><tr><td>420/</td><td>105</td><td>114</td><td>111</td><td>101</td><td>102</td><td>111</td><td>114</td><td>111</td><td>124</td><td>131</td><td>040</td><td>040</td><td>117</td><td>106</td><td>040</td><td>040</td></tr><tr><td></td><td>E</td><td>L</td><td>I</td><td>A</td><td>B</td><td>I</td><td>L</td><td>I</td><td>T</td><td>Y</td><td></td><td></td><td>O</td><td>F</td><td></td><td></td></tr><tr><td>440/</td><td>111</td><td>124</td><td>123</td><td>015</td><td>012</td><td>073</td><td>040</td><td>123</td><td>117</td><td>106</td><td>124</td><td>127</td><td>101</td><td>122</td><td>105</td><td>040</td></tr><tr><td></td><td>I</td><td>T</td><td>S</td><td>.</td><td>.</td><td>;</td><td></td><td>S</td><td>O</td><td>F</td><td>T</td><td>W</td><td>A</td><td>R</td><td>E</td><td></td></tr><tr><td>460/</td><td>117</td><td>116</td><td>040</td><td>105</td><td>121</td><td>125</td><td>111</td><td>120</td><td>115</td><td>105</td><td>116</td><td>124</td><td>040</td><td>127</td><td>110</td><td>111</td></tr><tr><td></td><td>O</td><td>N</td><td></td><td>E</td><td>Q</td><td>U</td><td>I</td><td>P</td><td>M</td><td>E</td><td>N</td><td>T</td><td></td><td>W</td><td>H</td><td>I</td></tr><tr><td>500/</td><td>103</td><td>110</td><td>040</td><td>111</td><td>123</td><td>040</td><td>116</td><td>117</td><td>124</td><td>040</td><td>123</td><td>125</td><td>120</td><td>120</td><td>114</td><td>111</td></tr><tr><td></td><td>C</td><td>H</td><td></td><td>I</td><td>S</td><td></td><td>N</td><td>O</td><td>T</td><td></td><td>S</td><td>U</td><td>P</td><td>P</td><td>L</td><td>I</td></tr><tr><td>520/</td><td>105</td><td>104</td><td>040</td><td>102</td><td>131</td><td>040</td><td>104</td><td>111</td><td>107</td><td>111</td><td>124</td><td>101</td><td>114</td><td>056</td><td>015</td><td>012</td></tr><tr><td></td><td>E</td><td>D</td><td></td><td>B</td><td>Y</td><td></td><td>D</td><td>I</td><td>G</td><td>I</td><td>T</td><td>A</td><td>L</td><td>.</td><td>.</td><td>.</td></tr><tr><td>540/</td><td>104</td><td>056</td><td>115</td><td>101</td><td>103</td><td>122</td><td>117</td><td>040</td><td>056</td><td>056</td><td>126</td><td>061</td><td>056</td><td>056</td><td>015</td><td>012</td></tr><tr><td></td><td>.</td><td>.</td><td>M</td><td>A</td><td>C</td><td>R</td><td>O</td><td></td><td>.</td><td>.</td><td>V</td><td>1</td><td>.</td><td>.</td><td>.</td><td>.</td></tr><tr><td>560/</td><td>056</td><td>115</td><td>103</td><td>101</td><td>114</td><td>114</td><td>011</td><td>056</td><td>056</td><td>056</td><td>103</td><td>115</td><td>060</td><td>054</td><td>056</td><td>056</td></tr><tr><td></td><td>.</td><td>M</td><td>C</td><td>A</td><td>L</td><td>L</td><td>.</td><td>.</td><td>.</td><td>.</td><td>C</td><td>M</td><td>O</td><td>.</td><td>.</td><td>.</td></tr><tr><td>600/</td><td>056</td><td>103</td><td>115</td><td>061</td><td>054</td><td>056</td><td>056</td><td>056</td><td>103</td><td>115</td><td>062</td><td>054</td><td>056</td><td>056</td><td>056</td><td>103</td></tr><tr><td></td><td>.</td><td>C</td><td>M</td><td>1</td><td>;</td><td>.</td><td>.</td><td>.</td><td>C</td><td>M</td><td>2</td><td>,</td><td>.</td><td>.</td><td>.</td><td>C</td></tr><tr><td>620/</td><td>115</td><td>063</td><td>054</td><td>056</td><td>056</td><td>056</td><td>103</td><td>115</td><td>064</td><td>054</td><td>056</td><td>056</td><td>056</td><td>103</td><td>115</td><td>065</td></tr><tr><td></td><td>M</td><td>3</td><td>,</td><td>.</td><td>.</td><td>.</td><td>C</td><td>M</td><td>4</td><td>,</td><td>.</td><td>.</td><td>.</td><td>C</td><td>M</td><td>5</td></tr><tr><td>640/</td><td>054</td><td>056</td><td>056</td><td>056</td><td>103</td><td>115</td><td>066</td><td>015</td><td>012</td><td>056</td><td>056</td><td>056</td><td>126</td><td>061</td><td>075</td><td>061</td></tr><tr><td></td><td>.</td><td>.</td><td>.</td><td>.</td><td>C</td><td>M</td><td>6</td><td>.</td><td>.</td><td>.</td><td>.</td><td>.</td><td>V</td><td>1</td><td>=</td><td>1</td></tr><tr><td>660/</td><td>015</td><td>012</td><td>056</td><td>105</td><td>116</td><td>104</td><td>115</td><td>015</td><td>012</td><td>015</td><td>012</td><td>056</td><td>115</td><td>101</td><td>103</td><td>122</td></tr><tr><td></td><td>.</td><td>.</td><td>.</td><td>E</td><td>N</td><td>D</td><td>M</td><td>.</td><td>.</td><td>.</td><td>.</td><td>.</td><td>M</td><td>A</td><td>C</td><td>R</td></tr><tr><td>700/</td><td>117</td><td>040</td><td>056</td><td>056</td><td>126</td><td>062</td><td>056</td><td>056</td><td>015</td><td>012</td><td>056</td><td>115</td><td>103</td><td>101</td><td>114</td><td>114</td></tr><tr><td></td><td>O</td><td></td><td>.</td><td>.</td><td>V</td><td>2</td><td>.</td><td>.</td><td>.</td><td>.</td><td>.</td><td>M</td><td>C</td><td>A</td><td>L</td><td>L</td></tr><tr><td>720/</td><td>011</td><td>056</td><td>056</td><td>056</td><td>103</td><td>115</td><td>060</td><td>054</td><td>056</td><td>056</td><td>056</td><td>103</td><td>115</td><td>061</td><td>054</td><td>056</td></tr><tr><td></td><td>.</td><td>.</td><td>.</td><td>.</td><td>C</td><td>M</td><td>O</td><td>.</td><td>.</td><td>.</td><td>.</td><td>C</td><td>M</td><td>1</td><td>,</td><td>.</td></tr><tr><td>740/</td><td>056</td><td>056</td><td>103</td><td>115</td><td>062</td><td>054</td><td>056</td><td>056</td><td>056</td><td>103</td><td>115</td><td>063</td><td>054</td><td>056</td><td>056</td><td>056</td></tr><tr><td></td><td>.</td><td>.</td><td>C</td><td>M</td><td>2</td><td>,</td><td>.</td><td>.</td><td>.</td><td>C</td><td>M</td><td>3</td><td>,</td><td>.</td><td>.</td><td>.</td></tr><tr><td>760/</td><td>103</td><td>115</td><td>064</td><td>054</td><td>056</td><td>056</td><td>056</td><td>103</td><td>115</td><td>065</td><td>054</td><td>056</td><td>056</td><td>056</td><td>103</td><td>115</td></tr><tr><td></td><td>C</td><td>M</td><td>4</td><td>,</td><td>.</td><td>.</td><td>.</td><td>C</td><td>M</td><td>5</td><td>,</td><td>,</td><td>.</td><td>.</td><td>C</td><td>M</td></tr></table>

The next example shows block 6 (the directory) of device RK0:. The output is in octal words with Radix-50 equivalents below each word.

\* RKO: /N/X/0:6

RKO:/N/X/0:6
BLOCK NUMBER 000006
000/ 000020 000002 000004000000 000046 002000 075131 062000
    P    B    D    B    YX    SWA    P
020/ 075273 000031 000000027147 002000 071677 142302 075273
    SYS    Y    GP9    YX    RT1    1SJ    SYS
040/ 000103 000000 027147002000 071677 141262 075273 000120
    A\$    GP9    XY    RT1    1FB    SYS    B

| 060/ | 000000 | 027147 | 002000071677 | 141034 | 075273 | 000100 | 000000 |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | GP9 | YX RT1 | 1BL | SYS | AX |  |
| 100/ | 027147 | 002000 | 100040000000 | 075273 | 000002 | 000000 | 027147 |
|  | GP9 | YX | TT | SYS | B |  | GP9 |
| 120/ | 002000 | 016040 | 000000075273 | 000003 | 000000 | 027147 | 002000 |
|  | YX | DT | SYS | C |  | GP9 | YX |
| 140/ | 015600 | 000000 | 075273000003 | 000000 | 027147 | 002000 | 016300 |
|  | DP |  | SYS C |  | GP9 | YX | DX |
| 160/ | 000000 | 075273 | 000003000000 | 027147 | 002000 | 016350 | 000000 |
|  |  | SYS | C | GP9 | YX | DY |  |
| 200/ | 075273 | 000004 | 000000027147 | 002000 | 070560 | 000000 | 075273 |
|  | SYS | D | GP9 | YX | RF |  | SYS |
| 220/ | 000003 | 000000 | 027147002000 | 071070 | 000000 | 075273 | 000003 |
|  | C |  | GP9 YX | RK |  | SYS | C |
| 240/ | 000000 | 027147 | 002000015340 | 000000 | 075273 | 000004 | 000000 |
|  |  | GP9 | YX DL |  | SYS | D |  |
| 260/ | 027147 | 002000 | 015410000000 | 075273 | 000005 | 000000 | 027147 |
|  | GP9 | YX | DM | SYS | E |  | GP9 |
| 300/ | 002000 | 015770 | 000000075273 | 000003 | 000000 | 027147 | 002000 |
|  | YX | DS | SYS | C |  | GP9 | YX |
| 320/ | 014640 | 000000 | 075273000005 | 000000 | 027147 | 002000 | 046600 |
|  | DD |  | SYS E |  | GP9 | YX | LP |
| 340/ | 000000 | 075273 | 000002000000 | 027147 | 002000 | 046770 | 000000 |
|  |  | SYS | B | GP9 | YX | LS |  |
| 360/ | 075273 | 000002 | 000000027147 | 002000 | 012620 | 000000 | 075273 |
|  | SYS | B | GP9 | YX | CR |  | SYS |
| 400/ | 000003 | 000000 | 027147002000 | 052070 | 000000 | 075273 | 000011 |
|  | C |  | GP9 YX | MS |  | SYS | I |
| 420/ | 000000 | 027547 | 002000052150 | 014400 | 075273 | 000003 | 000000 |
|  |  | GWD | YX MTH | D | SYS | C |  |
| 440/ | 027147 | 002000 | 015173052177 | 012445 | 000011 | 000000 | 027547 |
|  | GP9 | YX | DIS MT1 | COM | I |  | GWD |
| 460/ | 002000 | 051520 | 014400075273 | 000004 | 000000 | 027147 | 002000 |
|  | YX | MMH | D SYS | D |  | GP9 | YX |
| 500/ | 015173 | 052200 | 012445000010 | 000000 | 027547 | 002000 | 052100 |
|  | DIS | MT2 | COM H |  | GWD | YX | MSH |
| 520/ | 014400 | 075273 | 000004000000 | 027147 | 002000 | 054540 | 000000 |
|  | D | SYS | D | GP9 | YX | NL |  |
| 540/ | 075273 | 000002 | 000000027147 | 002000 | 062170 | 000000 | 075273 |
|  | SYS | B | GP9 | YX | PC |  | SYS |
| 560/ | 000002 | 000000 | 027147002000 | 062240 | 000000 | 075273 | 000003 |
|  | B |  | GP9 YX | PD |  | SYS | C |
| 600/ | 000000 | 027147 | 002000012740 | 000000 | 075273 | 000005 | 000000 |
|  |  | GP9 | YX CT |  | SYS | E |  |
| 620/ | 027147 | 002000 | 006250000000 | 075273 | 000007 | 000000 | 027147 |
|  | GP9 | YX | BA | SYS | G |  | GP9 |
| 640/ | 002000 | 016130 | 000000073376 | 000051 | 000000 | 027147 | 002000 |
|  | YX | DUP | SAV | AA |  | GP9 | YX |
| 660/ | 023752 | 050574 | 073376000023 | 000000 | 027147 | 002000 | 070533 |
|  | FOR | MAT | SAV S |  | GP9 | YX | RES |
| 700/ | 060223 | 073376 | 000017000000 | 027147 | 002000 | 015172 | 000000 |
|  | ORC | SAV | O | GPO | YX | DIR |  |
| 720/ | 073376 | 000021 | 000000027147 | 002000 | 075273 | 050553 | 074324 |
|  | SAV | Q | GPO | YX | SYS | MAC | SML |
| 740/ | 000052 | 000000 | 027147002000 | 017751 | 076400 | 073376 | 000023 |
|  | AB |  | GP9 YX | EDI | T | SAV | S |
| 760/ | 000000 | 027147 | 002000042614 | 000000 | 073376 | 000073 | 000000 |
|  |  | GP9 | YX KED |  | SAV | AS |  |
