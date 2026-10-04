# MACRO-11 Reference: Ch.6.1-6.5 Listing control, .ENABL/.DSABL, data storage (.BYTE/.WORD/.ASCII/.ASCIZ/.RAD50), radix/numeric control, location counter (.EVEN/.BLKW)

Source: DEC PDP-11 MACRO-11 Language Reference Manual, AA-5075A-TC (Aug 1977). OCR-converted; code examples may have lost alignment, and a few table rows/headings were dropped by OCR.

Contents:
- CHAPTER 6 GENERAL ASSEMBLER DIRECTIVES
- 6.1 LISTING CONTROL DIRECTIVES
- 6.1.1 .LIST and .NLIST Directives
- 6.1.2 Page Headings
- 6.1.3 .TITLE Directive
- 6.1.4 .SBTTL Directive
- 6.1.5 .IDENT Directive
- 6.1.6 .PAGE Directive/Page Ejection
- 6.2 FUNCTION DIRECTIVES: .ENABL AND .DSABL
- 6.3 DATA STORAGE DIRECTIVES
- 6.3.1 .BYTE Directive
- 6.3.2 .WORD Directive
- 6.3.3 ASCII Conversion Characters
- 6.3.4 .ASCII Directive
- 6.3.6 .RAD50 Directive
- 6.3.7 Temporary Radix-50 Control Operator: ^R
- 6.4 RADIX AND NUMERIC CONTROL FACILITIES
- 6.4.1 Radix Control and Unary Control Operators
- 6.4.2 Numeric Directives and Unary Control Operators
- 6.5 LOCATION COUNTER CONTROL DIRECTIVES
- 6.5.1 .EVEN Directive
- 6.5.2 .ODD Directive
- 6.5.3 .BLKB and .BLKW Directives

---

## PART III

**MACRO-11 DIRECTIVES**

Chapters 6 and 7 describe all the directives used with MACRO-11. Directives are statements that cause MACRO-11 to perform certain operations during assembly. Chapter 6 describes several types of directives, including those which control symbol interpretation, listing header material, program sections, data storage formats, and assembly listings. Chapter 7 describes those directives concerning macros, macro arguments, and repetitive coding sequences.

MACRO-11 directives can be preceded by a label (subject to any restrictions associated with specific directives) and followed by a comment. A MACRO-11 directive occupies the operator field of a source statement. Only one directive can be included in any given source line. The operand field may be occupied by one or more operands or left blank; legal operands differ with each directive specified.

## CHAPTER 6 GENERAL ASSEMBLER DIRECTIVES

This category of directives includes:

1. Listing control

2. Function control

3. Data storage

4. Radix and numeric control

5. Location counter control

6. Terminators

7. Program boundaries

8. Program sectioning

9. Symbol control

10. Conditional assembly

11. PAL-11R conditional assembly.

Each is described in its own section of this chapter.

### 6.1 LISTING CONTROL DIRECTIVES

Listing control directives control the content, format, and pagination of all line printer and teleprinter listing output generated during assembly. Facilities also exist for creating object module names and other identification information in the listing output.

#### 6.1.1 .LIST and .NLIST Directives

Listing control options can be specified in the text of a MACRO-11 program through the .LIST and .NLIST directives. These directives are of the form:

.LIST

.LIST arg

.NLIST

.NLIST arg

where: arg

represents one or more of the optional symbolic arguments defined in Table 6-1.

As indicated above, the listing control directives may be used without arguments, in which case the listing directives alter the listing level count. The listing level count is initialized to zero. At each occurrence of a .LIST directive, the listing level count is incremented; at each occurrence of an .NLIST directive, the listing level count is decremented. When the listing level count is negative, the listing is suppressed (unless the line contains an error). Conversely, when the listing level count is greater than zero, the listing is always generated. Finally, when the count is zero, the line is either listed or suppressed, contingent upon the other listing controls currently in effect for the program. For example, the following macro definition employs the .LIST and .NLIST directives to selectively list portions of the macro body when the macro is expanded:

.MACRO LTEST
; A-THIS LINE SHOULD LIST
.NLIST

; B-THIS LINE SHOULD NOT LIST
.NLIST

; C-THIS LINE SHOULD NOT LIST
.LIST

; D-THIS LINE SHOULD NOT LIST
.LIST

; E-THIS LINE SHOULD LIST
.ENDM

;LIST TEST
;LISTING LEVEL COUNT IS 0.
;LISTING LEVEL COUNT IS -1.

;LISTING LEVEL COUNT IS -2.

;LISTING LEVEL COUNT IS -1.

;LISTING LEVEL COUNT IS 0.
;LISTING LEVEL COUNT IS BACK TO 0.

.LIST ME
LTEST
; A-THIS LINE SHOULD LIST
; E-THIS LINE SHOULD LIST;LIST MACRO EXPANSION.
;CALL THE MACRO
;LISTING LEVEL COUNT IS 0.
;LISTING LEVEL COUNT IS BACK TO 0.

An important purpose of the level count is to allow macro expansions to be listed selectively and yet exit with the listing level count restored to the value existing prior to the macro call.

When used with arguments, the listing directives do not alter the listing level count; however, the .LIST and .NLIST directives can be used to override current listing control, as shown in the example below:

.MACRO XX
.
.
.
.LIST
X=.
.NLIST
.
.
.
.ENDM
.NLIST: ME
XX

X = .

;LIST NEXT LINE.

;DO NOT LIST REMAINDER OF MACRO
;EXPANSION.

;DO NOT LIST MACRO EXPANSIONS.

The symbolic arguments allowed for use with the listing directives are described in Table 6-1. These arguments can be used singly or in combination with each other. If multiple arguments are specified in a listing directive, each argument must be separated by a comma, tab, or

**GENERAL ASSEMBLER DIRECTIVES**

space. For any argument not specifically included in a listing control statement, the associated default assumption (List or No list) is applicable throughout the source program. The default assumptions for the listing control directives also appear in Table 6-1.

Table 6-1

Symbolic Arguments of Listing Control Directives

| Argument | Default | Function |
| --- | --- | --- |
| SEQ* | List | Controls the listing of source line sequence numbers. MACRO-11 assigns sequence number 1 to the first source line in a file, and increments the sequence number for each additional line in the file. If this field is suppressed through an .NLIST SEQ directive, MACRO-11 generates a tab, effectively allocating space for the field, but fills the field with blanks. Thus, the inter-positional relationships of subsequent fields in the listing remain undisturbed. During the assembly process, MACRO-11 examines each source line for possible error conditions. For any line in error, an appropriate error flag is printed preceding the line sequence number field (see Appendix D). MACRO-11 does not assign sequence numbers for files that have had sequence numbers assigned by other programs, such as an editor. |
| LOC* | List | Controls the listing of the current location counter field. Normally, this field is not suppressed. However, if it is suppressed through the .NLIST LOC directive, MACRO-11 does not generate a tab, nor does it allocate space for the field, as is the case with the source line sequence number field (SEQ) described above. Thus, the suppression of the current location counter (LOC) field effectively left-justifies all subsequent fields (while preserving inter-positional relationships) to that position otherwise normally occupied by this field. |
| BIN* | List | Controls the listing of generated binary code. If this field is suppressed through an .NLIST BIN directive, left-justification of the source code field occurs in the same manner described above for the current location counter (LOC) field. |
| BEX | List | Controls the listing of binary extensions, i.e., the locations and binary contents beyond those that will fit on the source statement line. This is a subset of the BIN argument. |
| SRC* | List | Controls the listing of source lines. |

(Continued on next page)

Table 6-1 (Cont.)
Symbolic Arguments of Listing Control Directives

| Argument | Default | Function |
| --- | --- | --- |
| COM | List | Controls the listing of comments. This is a subset of the SRC argument. The .NLIST COM directive reduces listing time and space when comments are not desired. |
| MD | List | Controls the listing of macro definitions and repeat range expansions. |
| MC | List | Controls the listing of macro calls and repeat range expansions. |
| ME | No list | Controls the listing of macro expansions. |
| MEB | No list | Controls the listing of macro expansion binary code. A .LIST MEB directive causes only those macro expansion statements that generate binary code to be listed. This is a subset of the ME argument. |
| CND | List | Controls the listing of unsatisfied conditional coding and associated .IF and .ENDC directives in the source program. This argument permits conditional assemblies to be listed without including unsatisfied conditional coding. |
| LD | No list | Controls the listing of all listing directives having no arguments, i.e., those listing directives that alter the listing level count. |
| TOC | List | Controls the listing of the table of contents during assembly pass 1 (see Section 6.1.4 describing the .SBTTL directive). This argument does not affect the printing of the full assembly listing during assembly pass 2. |
| SYM | List | Controls the listing of the symbol table resulting from the assembly of the source program. |
| TTM | List | Controls the listing output format. The default can be set by the system manager. If the system manager does not set a default, it is set to line printer format. Figure 6-1 illustrates the line printer output format. Figure 6-2 illustrates the teleprinter output format. |

\* If the .NLIST arguments SEQ, LOC, BIN, and SRC are in effect at the same time, i.e., if all four significant fields in the listing are to be suppressed, the printing of the resulting blank line is inhibited.

An example of an assembly listing, as sent to a 132-column line printer, is shown in Figure 6-1. Note that binary extensions for statements generating more than one word are formatted horizontally on the source line.

An example of an assembly listing, as sent to a teleprinter (in the same format as for an 80-column line printer), is shown in Figure 6-2. Notice that binary extensions for statements generating more than one word are printed on subsequent lines. There is no explicit truncation of output to 80 characters by the assembler.

Any argument specified in a .LIST/.NLIST directive other than those listed in Table 6-1 causes the directive to be flagged with an error code (A) in the assembly listing.

The listing control options can also be specified at assembly time through switches included in the command string to MACRO-11 (see the appropriate system manual). The use of these switches overrides all corresponding listing control (.LIST or .NLIST) directives specified in the source program.

<table><tr><td>209</td><td></td><td></td><td></td><td></td><td colspan="2">.SBTTL READ AND PARSE COMMAND LINES</td></tr><tr><td>210</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>211 001230</td><td></td><td></td><td></td><td>GETLN!</td><td colspan="2">GCMLS #GCLBLK IGET LINE VIA GCML</td></tr><tr><td>212 001244</td><td>103003</td><td></td><td></td><td></td><td colspan="2">BCC 1$ ISKIP IF NO ERROR</td></tr><tr><td>213 001246</td><td></td><td></td><td></td><td></td><td colspan="2">EXITSS JELSE, EXIT</td></tr><tr><td>214 001254</td><td></td><td></td><td></td><td>1$!</td><td colspan="2">TYPE G.CMLD+2(R0),G.CMLD(R0),#!0 ISEND OUT THE INPUT LINE</td></tr><tr><td>215 001300</td><td></td><td></td><td></td><td></td><td colspan="2">CSIS1 #CSIBLK,GCLBLK+G.CMLD+2,GCLBLK+G.CMLD</td></tr><tr><td>216 001324</td><td>103064</td><td></td><td></td><td></td><td colspan="2">BCC 2$ JBRANCH IF NO ERROR DETECTED</td></tr><tr><td>217 001326</td><td>016046</td><td>000020</td><td></td><td></td><td colspan="2">MOV C.FILD+2(R0),-(SP) IPUT STRING ERROR ADDR IN STK</td></tr><tr><td>218 001332</td><td>166016</td><td>000004</td><td></td><td></td><td colspan="2">SUB C.CMLD+2(R0),(SP) ICALCULATE LENGTH OF FIRST PART</td></tr><tr><td>219 001336</td><td></td><td></td><td></td><td></td><td colspan="2">TYPE C.CMLD+2(R0),(SP),#!$ ISEND OUT FIRST PART OF STRING</td></tr><tr><td>220 001360</td><td></td><td></td><td></td><td></td><td colspan="2">TYPE C.FILD+2(R0),C.FILD(R0),#!$ ISEND OUT SECOND PART</td></tr><tr><td>221 001404</td><td>066060</td><td>000016</td><td>000020</td><td></td><td colspan="2">ADD C.FILD(R0),C.FILD+2(R0) ICALC ADDR OF LAST PART OF STRING</td></tr><tr><td>222 001412</td><td>162660</td><td>000002</td><td></td><td></td><td colspan="2">SUB (SP)+,C.CMLD(R0) IDEDUCT LENGTH OF FIRST PART</td></tr><tr><td>223 001416</td><td>166060</td><td>000016</td><td>000002</td><td></td><td colspan="2">SUB C.FILD(R0),C.CMLD(R0) ICALC LENGTH OF LAST PART</td></tr><tr><td>224 001424</td><td></td><td></td><td></td><td></td><td colspan="2">TYPE C.FILD+2(R0),C.CMLD(R0),#40 ISEND OUT LAST PART</td></tr><tr><td>225 001450</td><td></td><td></td><td></td><td></td><td colspan="2">TYPEM STX,40 ISEND SYNTAX ERROR MESSAGE</td></tr><tr><td>226 001474</td><td>000655</td><td></td><td></td><td></td><td colspan="2">BR GETLN ITRY FOR MORE</td></tr><tr><td>227</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>228 001476</td><td>005760</td><td>000002</td><td></td><td>2$!</td><td colspan="2">TST C.CMLD(R0) ICHECK LENGTH OF LINE</td></tr><tr><td>229 001502</td><td>001652</td><td></td><td></td><td></td><td colspan="2">BEQ GETLN IIF NULL, SKIP BACK FOR NEXT LINE</td></tr><tr><td>230 001504</td><td>112767</td><td>000060</td><td>176432</td><td></td><td colspan="2">MOVB #!0,EQUBIT IASSUME EQUAL SIGN NOT FOUND</td></tr><tr><td>231 001512</td><td>132760</td><td>000040</td><td>000001</td><td></td><td colspan="2">BITB #CS,EQU,C.STAT(R0) ICHECK STATUS</td></tr><tr><td>232 001520</td><td>001402</td><td></td><td></td><td></td><td colspan="2">BEQ 10$ ISKIP IF EQUAL SIGN NOT SEEN</td></tr><tr><td>233 001522</td><td>105267</td><td>176416</td><td></td><td></td><td colspan="2">INCB EQUBIT IELSE, INDICATE EQUAL SIGN FOUND</td></tr><tr><td>234 001526</td><td></td><td></td><td></td><td>10$!</td><td colspan="2">TYPEM EQU,40 ISEND EQUAL SIGN STATUS MESSAGE</td></tr><tr><td>235 001552</td><td></td><td></td><td></td><td></td><td colspan="2">TYPEM OPT,40 ISEND OUTPUT SCAN MESSAGE</td></tr><tr><td>236 001576</td><td></td><td></td><td></td><td colspan="3">OPARSE: CALL INIT2 INIT LOCNS FOR CSI2 CALL/TEST</td></tr><tr><td>237 001602</td><td></td><td></td><td></td><td></td><td colspan="2">CSIS2 ,OUTPUT,*SWTBL IPARSE OUTPUT SPEC</td></tr><tr><td>238 001620</td><td>103441</td><td></td><td></td><td></td><td colspan="2">BCS CS2ERR ISKIP ON ERROR</td></tr><tr><td>239 001622</td><td></td><td></td><td></td><td></td><td colspan="2">CALL EVALU8 IEVALUATE RESULTS OF SEMANTIC PARSE</td></tr><tr><td>240 001626</td><td>132760</td><td>000020</td><td>000001</td><td></td><td colspan="2">BITB #CS.MOR,C.STAT(R0) IADDITIONAL OUTPUT SPECS?</td></tr><tr><td>241 001634</td><td>001360</td><td></td><td></td><td></td><td colspan="2">BNE OPARSE IYES, CONTINUE WITH OUTPUT SCAN</td></tr><tr><td>242 001636</td><td></td><td></td><td></td><td></td><td colspan="2">TYPEM IPT,40 ISEND INPUT SCAN MESSAGE</td></tr><tr><td>243 001662</td><td></td><td></td><td></td><td colspan="3">IPARSE: CALL INIT2 INIT LOCNS FOR CSI2 CALL/TEST</td></tr><tr><td>244 001666</td><td></td><td></td><td></td><td></td><td colspan="2">CSIS2 ,INPUT,*SWTBL IPARSE INPUT SPEC</td></tr><tr><td>245 001704</td><td>103407</td><td></td><td></td><td></td><td colspan="2">BCS CS2ERR ISKIP ON ERROR</td></tr><tr><td>246 001706</td><td></td><td></td><td></td><td></td><td colspan="2">CALL EVALU8 IEVALUATE RESULTS OF SEMANTIC PARSE</td></tr><tr><td>247 001712</td><td>132760</td><td>000020</td><td>000001</td><td></td><td colspan="2">BITB #CS.MOR,C.STAT(R0) IADDITIONAL INPUT SPECS?</td></tr><tr><td>248 001720</td><td>001360</td><td></td><td></td><td></td><td colspan="2">BNE IPARSE IYES, CONTINUE WITH INPUT SCAN</td></tr><tr><td>249 001722</td><td>000412</td><td></td><td></td><td></td><td colspan="2">BR JMPGET IGET ANOTHER COMMAND LINE</td></tr></table>

<table><tr><td>209</td><td></td><td></td><td>.SBTTL</td><td colspan="2">READ AND PARSE COMMAND LINES</td></tr><tr><td>210</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>211</td><td>001230</td><td>GETLN1</td><td>GCMLS</td><td>#GCLBLK</td><td>JGET LINE VIA GCML</td></tr><tr><td>212</td><td>001244</td><td>103003</td><td>BCC</td><td>1$</td><td>JSKIP IF NO ERROR</td></tr><tr><td>213</td><td>001246</td><td></td><td>EXITSS</td><td></td><td>JELSE, EXIT</td></tr><tr><td>214</td><td>001254</td><td>1$1</td><td>TYPE</td><td>G.CMLD+2(R0),G.CMLD(R0),*10</td><td>JSEND OUT THE INPUT LINE</td></tr><tr><td>215</td><td>001300</td><td></td><td>CSI$1</td><td colspan="2">*CSIBLK,GCLBLK+G.CMLD+2,GCLBLK+G.CMLD</td></tr><tr><td>216</td><td>001324</td><td>103064</td><td>BCC</td><td>2$</td><td>JBRANCH IF NO ERROR DETECTED</td></tr><tr><td>217</td><td>001326</td><td>016046</td><td>MOV</td><td>C.FILD+2(R0),-(SP)</td><td>JPUT STRING ERROR ADDR IN STK</td></tr><tr><td></td><td></td><td>000020</td><td></td><td></td><td></td></tr><tr><td>218</td><td>001332</td><td>166016</td><td>SUB</td><td>C.CMLD+2(R0),(SP)</td><td>JCALCULATE LENGTH OF FIRST PART</td></tr><tr><td></td><td></td><td>000004</td><td></td><td></td><td></td></tr><tr><td>219</td><td>001336</td><td></td><td>TYPE</td><td>C.CMLD+2(R0),(SP),*1$</td><td>JSEND OUT FIRST PART OF STRING</td></tr><tr><td>220</td><td>001360</td><td></td><td>TYPE</td><td>C.FILD+2(R0),C.FILD(R0),*1$</td><td>JSEND OUT SECOND PART</td></tr><tr><td>221</td><td>001404</td><td>066060</td><td>ADD</td><td>C.FILD(R0),C.FILD+2(R0)</td><td>JCALC ADDR OF LAST PART OF STRING</td></tr><tr><td></td><td></td><td>000016</td><td></td><td></td><td></td></tr><tr><td></td><td></td><td>000020</td><td></td><td></td><td></td></tr><tr><td>222</td><td>001412</td><td>162660</td><td>SUB</td><td>(SP)+,C.CMLD(R0)</td><td>JDEDUCT LENGTH OF FIRST PART</td></tr><tr><td></td><td></td><td>000002</td><td></td><td></td><td></td></tr><tr><td>223</td><td>001416</td><td>166060</td><td>SUB</td><td>C.FILD(R0),C.CMLD(R0)</td><td>JCALC LENGTH OF LAST PART</td></tr><tr><td></td><td></td><td>000016</td><td></td><td></td><td></td></tr><tr><td></td><td></td><td>000002</td><td></td><td></td><td></td></tr><tr><td>224</td><td>001424</td><td></td><td>TYPE</td><td>C.FILD+2(R0),C.CMLD(R0),*40</td><td>JSEND OUT LAST PART</td></tr><tr><td>225</td><td>001450</td><td></td><td>TYPEM</td><td>STX,40</td><td>JSEND SYNTAX ERROR MESSAGE</td></tr><tr><td>226</td><td>001474</td><td>000555</td><td>BR</td><td>GETLN</td><td>JTRY FOR MORE</td></tr><tr><td>227</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>228</td><td>001476</td><td>005760</td><td>2$1</td><td>TST</td><td>C.CMLD(R0) JCHECK LENGTH OF LINE</td></tr><tr><td></td><td></td><td>000002</td><td></td><td></td><td></td></tr><tr><td>229</td><td>001502</td><td>001652</td><td>BEQ</td><td>GETLN</td><td>JIF NULL, SKIP BACK FOR NEXT LINE</td></tr><tr><td>230</td><td>001504</td><td>112767</td><td>MOVB</td><td>*10,EQUBIT</td><td>JASSUME EQUAL SIGN NOT FOUND</td></tr><tr><td></td><td></td><td>000060</td><td></td><td></td><td></td></tr><tr><td></td><td></td><td>176432</td><td></td><td></td><td></td></tr><tr><td>231</td><td>001512</td><td>132760</td><td>BITB</td><td colspan="2">*CS,EQU,C.STAT(R0) JCHECK STATUS</td></tr><tr><td></td><td></td><td>000040</td><td></td><td></td><td></td></tr><tr><td></td><td></td><td>000001</td><td></td><td></td><td></td></tr><tr><td>232</td><td>001520</td><td>001402</td><td>BEQ</td><td>10$</td><td>JSKIP IF EQUAL SIGN NOT SEEN</td></tr><tr><td>233</td><td>001522</td><td>105267</td><td>INCB</td><td>EQUBIT</td><td>JELSE, INDICATE EQUAL SIGN FOUND</td></tr><tr><td></td><td></td><td>176416</td><td></td><td></td><td></td></tr><tr><td>234</td><td>001526</td><td></td><td>10$1</td><td>TYPEM</td><td>EQU,40 JSEND EQUAL SIGN STATUS MESSAGE</td></tr><tr><td>235</td><td>001552</td><td></td><td>TYPEM</td><td>OPT,40</td><td>JSEND OUTPUT SCAN MESSAGE</td></tr><tr><td>236</td><td>001576</td><td></td><td>OPARSE:</td><td>CALL INIT2</td><td>JINIT LOCNS FOR CSI2 CALL/TEST</td></tr><tr><td>237</td><td>001602</td><td></td><td>CSI$2</td><td>,OUTPUT,#SWTBL</td><td>JPARSE OUTPUT SPEC</td></tr><tr><td>238</td><td>001620</td><td>103441</td><td>BCS</td><td>CS2ERR</td><td>JSKIP ON ERROR</td></tr><tr><td>239</td><td>001622</td><td></td><td>CALL</td><td>EVALU8</td><td>JEVALUATE RESULTS OF SEMANTIC PARSE</td></tr><tr><td>240</td><td>001626</td><td>132760</td><td>BITB</td><td colspan="2">*CS.MOR,C.STAT(R0) JADDITIONAL OUTPUT SPECS?</td></tr><tr><td></td><td></td><td>000020</td><td></td><td></td><td></td></tr><tr><td></td><td></td><td>000001</td><td></td><td></td><td></td></tr><tr><td>241</td><td>001634</td><td>001360</td><td>BNE</td><td>OPARSE</td><td>JYES, CONTINUE WITH OUTPUT SCAN</td></tr><tr><td>242</td><td>001636</td><td></td><td>TYPEM</td><td>IPT,40</td><td>JSEND INPUT SCAN MESSAGE</td></tr><tr><td>243</td><td>001662</td><td></td><td>IPARSE:</td><td>CALL INIT2</td><td>JINIT LOCNS FOR CSI2 CALL/TEST</td></tr><tr><td>244</td><td>001666</td><td></td><td>CSI$2</td><td>,INPUT,#SWTBL</td><td>JPARSE INPUT SPEC</td></tr><tr><td>245</td><td>001704</td><td>103407</td><td>BCS</td><td>CS2ERR</td><td>JSKIP ON ERROR</td></tr><tr><td>246</td><td>001706</td><td></td><td>CALL</td><td>EVALU8</td><td>JEVALUATE RESULTS OF SEMANTIC PARSE</td></tr><tr><td>247</td><td>001712</td><td>132760</td><td>BITB</td><td colspan="2">*CS.MOR,C.STAT(R0) JADDITIONAL INPUT SPECS?</td></tr><tr><td></td><td></td><td>000020</td><td></td><td></td><td></td></tr><tr><td></td><td></td><td>000001</td><td></td><td></td><td></td></tr><tr><td>248</td><td>001720</td><td>001360</td><td>BNE</td><td>IPARSE</td><td>JYES, CONTINUE WITH INPUT SCAN</td></tr></table>

Figure 6-2 Example of Terminal Assembly Listing

Figure 6-3 shows a listing, produced in line printer format, reflecting the use of the .LIST and .NLIST directives in the source program and the effects such directives have on the assembly listing output.

#### 6.1.2 Page Headings

MACRO-11 prints each assembly page in the format shown in either Figure 6-1 or Figure 6-2, depending on the listing mode (see TTM, Table 6-1). On the first line of each page, MACRO-11 prints the following (from left to right):

1. Title of the object module, as established through the .TITLE directive (see next section).

2. Assembler version identification.

3. Date.

4. Time-of-day.

5. Page number.

The second line of each assembly listing page contains the subtitle text specified in the last-encountered .SBTTL directive (see Section 6.1.4).

| 27 |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| 28 |  |  |  |  |  |  |
| 29 | 000062 |  |  |  | LSTMAC COM | ;COMMENT LINES TEST |
|  |  |  |  |  | .NLIST COM |  |
|  | 000062 | 000001 | 000002 | 000003 | .WORD 1,2,3,4,5 |  |
|  | 000070 | 000004 | 000005 |  | .LIST COM |  |
| 30 |  |  |  |  |  |  |
| 31 |  |  |  |  |  |  |
| 32 | 000074 |  |  |  | LSTMAC <COM,BEX> | ;COMMENT LINES AND EXTENDED BINARY TEST |
|  |  |  |  |  | .NLIST COM,BEX |  |
|  | 000074 | 000001 | 000002 | 000003 | .WORD 1,2,3,4,5 |  |
|  |  |  |  |  | .LIST COM,BEX |  |

| 1 |  |  |  | .NLIST TTM | JWIDE LISTING MODE IS IN EFFECT |
| --- | --- | --- | --- | --- | --- |
| 2 |  |  |  | .LIST ME | JLIST MACRO EXPANSIONS |
| 3 |  |  |  |  |  |
| 4 |  |  | ; |  |  |
| 5 |  |  | ; LISTING CONTROL TEST MACRO |  |  |
| 6 |  |  | ; |  |  |
| 7 |  |  |  | .MACRO LSTMAC ARG |  |
| 8 |  |  |  | .NLIST ARG |  |
| 9 |  |  |  | .WORD 1,2,3,4,5 | ;THIS IS A COMMENT |
| 10 |  |  |  | .LIST ARG |  |
| 11 |  |  |  | .ENDM |  |
| 12 |  |  |  |  |  |
| 13 |  |  |  |  |  |
| 14 |  |  |  |  |  |
| 15 |  |  |  |  |  |
| 16 |  |  |  |  |  |
| 17 | 000012 |  |  | LSTMAC LOC | ;LOCATION COUNTER TEST |
|  | 000001 | 000002 | 000003 | .NLIST LOC |  |
|  | 000004 | 000005 |  | .WORD 1,2,3,4,5 | ;THIS IS A COMMENT |
|  |  |  |  | .LIST LOC |  |
| 18 |  |  |  |  |  |
| 19 |  |  |  |  |  |
| 20 | 000024 |  |  | LSTMAC BIN | ;GENERATED BINARY TEST |
|  |  |  | .NLIST BIN |  |  |
|  | 000024 |  | .WORD 1,2,3,4,5 | ;THIS IS A COMMENT |  |
|  |  |  |  | .LIST BIN |  |
| 21 |  |  |  |  |  |
| 22 |  |  |  |  |  |
| 23 | 000036 |  |  | LSTMAC BEX | ;EXTENDED BINARY TEST |
|  |  |  |  | .NLIST BEX |  |
|  | 000036 | 000001 | 000002 | .WORD 1,2,3,4,5 | ;THIS IS A COMMENT |
|  |  |  |  | .LIST BEX |  |
| 24 |  |  |  |  |  |
| 25 |  |  |  |  |  |
| 26 | 000050 |  |  | LSTMAC SRC | ;SOURCE LINES TEST |
|  | 000050 | 000001 | 000002 | 000003 |  |
|  | 000056 | 000004 | 000005 |  |  |
|  |  |  |  | .LIST SRC |  |

.MAIN. MACRO M0707 09-JUL-74 16129 PAGE 1

#### 6.1.3 .TITLE Directive

The .TITLE directive is used to assign a name to the object module as the first entry in the header of each page in the assembly listing. The name so assigned is the first six non-blank characters following the .TITLE directive. This name should be six Radix-50 characters or less in length; any characters beyond the first six are checked for ASCII legality, but they are not used as part of the object module name. For example, the directive:

    .TITLE PROGRAM TO PERFORM DAILY ACCOUNTING

causes the assembled object module to be named PROGRA. Note that this 6-character name bears no relationship to the filename of the object module, as specified in the command string to MACRO-11. The name of an object module (specified in the .TITLE directive) appears in the load map produced at link time. This is also the module name which the Librarian will recognize.

If the .TITLE directive is not specified, MACRO-11 assigns the default name .MAIN. to the object module. If more than one .TITLE directive is specified in the source program, the last .TITLE directive encountered establishes the name for the entire object module.

All spaces and/or tabs up to the first non-space/non-tab character following the .TITLE directive are ignored by MACRO-11 when evaluating the text string.

If the .TITLE directive is specified without an object module name, or if the first non-space/non-tab character in the object module name is not a Radix-50 character, the directive is flagged with an error code (A) in the assembly listing.

Section A.2 of Appendix A contains a table of Radix-50 characters.

#### 6.1.4 .SBTTL Directive

The .SBTTL directive is used to produce a table of contents immediately preceding the assembly listing and to further identify each page in the listing. In the latter case, the text following the .SBTTL directive is printed as the second line of the header of each page in the listing, continuing until altered by a subsequent .SBTTL directive in the program. For example, the directive:

    .SBTTL CONDITIONAL ASSEMBLIES

    causes the text

**CONDITIONAL ASSEMBLIES**

to be printed as the second line in the header of the assembly listing.

During assembly pass 1, a table of contents is printed for the assembly listing, containing the line sequence number, the page number, and the text accompanying each .SBTTL directive. The listing of the table of contents is suppressed whenever an .NLIST TOC directive is encountered in the source program (see Table 6-1). An example of a table of contents listing is shown in Figure 6-4.

CSITST -- TEST OF CSI1 AND CSI2 MACRO M0707 09-JUL-74 15:47 TABLE OF CONTENTS

2- 55 MACRO DEFINITIONS
3- 74 MESSAGE STRINGS
4-153 MISCELLANEOUS DATA
5-209 READ AND PARSE COMMAND LINES
6-255 EVALUATE THE SEMANTIC ANALYSIS
7-345 SUBROUTINES

Figure 6-4 Assembly Listing Table of Contents

#### 6.1.5 .IDENT Directive

The .IDENT directive provides an additional means of labeling the object module produced by MACRO-11. In addition to the name assigned to the object module with the .TITLE directive (see Section 6.1.3), a character string up to six Radix-50 characters can be specified between paired printing delimiters to label the object module with the program version number. This directive takes the following form:

    .IDENT /string/

where: string represents six or fewer legal Radix-50 characters which establish the program identification or version number. This number is included in the global symbol directory of the object module; the first four characters are printed in the load map and librarian listing.

/ / represent delimiting characters. These delimiters may be any paired printing characters, other than the equal sign (=), the left angle bracket (<), or the semicolon (;), as long as the delimiting character is not contained within the text string itself. If the delimiting characters do not match, or if an illegal delimiting character is used, the .IDENT directive is flagged with an error code (A) in the assembly listing.

An example of the .IDENT directive is shown below:

.IDENT /V05A/

The character string V05A is converted to Radix-50 representation and included in the global symbol directory of the object module. This character string also appears in the load map produced at link time and the Librarian directory listings.

When more than one .IDENT directive is encountered in a given program, the last such directive encountered establishes the character string which forms part of the object module identification.

#### 6.1.6 .PAGE Directive/Page Ejection

Page ejection is accomplished in one of four ways:

1. After reaching a count of 58 lines in the listing, MACRO-11 automatically performs a page eject to skip over page perforations on line printer paper and to formulate teleprinter output into pages. The page number is not changed.

2. In addition, the .PAGE directive is used within the source program to perform a page eject at desired points in the listing. The format of this directive is:

.PAGE

This directive takes no arguments and causes a skip to the top of the next page when encountered. It also causes the page number to be incremented and the line sequence counter to be cleared. The .PAGE directive does not appear in the listing.

When used within a macro definition, the .PAGE directive is ignored during the assembly of the macro definition. Rather, the page eject operation is performed as the macro itself is expanded. In this case, the page number is also incremented.

3. A page eject is performed when a form-feed character is encountered. If the form-feed character appears within a macro definition, a page eject occurs during the assembly of the macro definition, but not during the expansion of the macro itself. A page eject resulting from the use of the form-feed character likewise causes the page number to be incremented and the line sequence counter to be cleared.

4. Encountering a new source file causes the page number to be incremented and the line sequence count to be reset.

### 6.2 FUNCTION DIRECTIVES: .ENABL AND .DSABL

Several function control options are provided by MACRO-11 through the .ENABL and .DSABL directives. These directives are included in a source program to invoke or inhibit certain MACRO-11 functions and operations incidental to the assembly process itself. These directives take the following form:

.ENABLE arg
.DSABL arg

where: arg represents one or more of the optional symbolic arguments defined in Table 6-2.

Specifying any argument in an .ENABL/.DSABL directive other than those listed in Table 6-2 causes that directive to be flagged with an error code (A) in the assembly listing.

Table 6-2

Symbolic Arguments of Function Control Directives

| Argument | Default | Function |
| --- | --- | --- |
| ABS | Disable | Enabling this function produces absolute binary output in FILES-11 format. To convert this output to Formatted Binary format (as required by the Absolute Loader), use the FLX utility. |
| AMA | Disable | Enabling this function causes all relative addresses (address mode 67) to be assembled as absolute addresses (address mode 37). This function is useful during the debugging phase of program development. |
| CDR | Disable | Enabling this function causes source columns 73 and greater, i.e., to the end of the line, to be treated as a comment. The most common use of this feature is to permit sequence numbers in card columns 73-80. |
| CRF | Enable | Disabling this function inhibits the generation of cross-reference output. This function only has meaning if cross-reference output generation is specified in the command string. |
| FPT | Disable | Enabling this function causes floating-point truncation; disabling this function causes floating-point rounding. |
| LC | Disable | Enabling this function causes MACRO-11 to accept lower-case ASCII input instead of converting it to upper-case. If this function is not enabled, all text is converted to upper-case. |
| LSB | Disable | This argument permits the enabling or disabling of a local symbol block. Although a local symbol block is normally established by encountering a new symbolic label or a .PSECT directive in the source program, an .ENABL LSB directive establishes a new local symbol block which is not terminated until (1) another .ENABL LSB is encountered, or (2) another symbolic label or .PSECT directive is encountered following a paired .DSABL LSB directive. |
|  |  | Although the .ENABL LSB directive permits a local symbol block to cross .PSECT boundaries, local symbols cannot be defined in a program section other than the one that was in effect when the block was entered. The basic function of this directive with regard to .PSECT's is limited to those instances |

(Continued on next page)

Table 6-2 (Cont.)
Symbolic Arguments of Function Control Directives

| Argument | Default | Function |
| --- | --- | --- |
| LSB(Cont.) | Disable | where it is desirable to leave a program section temporarily to store data, followed by a return to the original program section. Attempts to define local symbols in an alternate program section are flagged with an error code (P) in the assembly listing.An example of the .ENABL LSB and .DSABL LSB directives, as typically used in a source program, is shown in Figure 6-5. |
| PNC | Enable | Disabling this function inhibits binary output until an .ENABL PNC statement is encountered within the same module. |
| REG | Enable | When specified, the .DSABL REG directive inhibits the normal MACRO-11 default register definitions; if not disabled, the default definitions listed below remain in effect.R0=%0R1=%1R2=%2R3=%3R4=%4R5=%5SP=%6PC=%7 |
| GBL | Enable* | The .ENABL REG statement may be used as the logical complement of the .DSABL REG directive. The use of these directives, however, is not recommended. For logical consistency, use the normal default register definitions listed above.When the .ENABL GBL directive is specified, MACRO-11 treats all symbol references that are undefined at the end of assembly pass 1 as default global references; when the .DSABL GBL directive is specified, MACRO-11 treats all such references as undefined symbols. In assembly pass 2, if the .DSABL GBL function is still in effect, these undefined symbols are flagged with an error code (U) in the assembly listing; otherwise, they continue to be regarded by MACRO-11 as global references. |

\* The default is Disable for RT-11 MACRO programs.

| 272 |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| 273 |  |  |  |  |  |  |
| 274 |  |  |  |  |  |  |
| 275 |  |  |  |  |  |  |
| 276 |  |  |  | ,ENABL | LSB |  |
| 277 |  |  |  |  |  |  |
| 278 | 003142 | 010103 | FNDSMI: | MOV | R1,R3 | IPUT ADDR OF LINE IN R3 |
| 279 | 003144 | 060203 |  | ADD | R2,R3 | IPOINT R3 PAST LAST CHAR IN LINE |
| 280 | 003146 | 020301 | 1S: | CMP | R3,R1 | IDOES R3 POINT TO START OF LINE? |
| 281 | 003150 | 001422 |  | BEQ | 30$ | JIF SO, LEAVE INDICATING FAILURE |
| 282 | 003152 | 124327 | 000073 | CMPB | -(R3),#SEMIC | JIS THE LAST CHARACTER SEMICOLON? |
| 283 | 003156 | 001373 |  | BNE | 1$ | INO, CONTINUE LOOKING |
| 284 | 003160 | 010302 |  | MOV | R3,R2 | JYES, POINT R2 PAST NEW END-OF-LINE |
| 285 | 003162 | 000412 |  | BR | 20$ | ILEAVE VIA COMMON SUCCESS CODE |
| 286 |  |  |  |  |  |  |
| 287 | 003164 | 060102 | SKPBLK: | ADD | R1,R2 | IPOINT R2 PAST END-OF-LINE |
| 288 | 003166 | 020201 | 10$: | CMP | R2,R1 | IDOES R2 POINT TO START OF LINE? |
| 289 | 003170 | 001412 |  | BEQ | 30$ | JIF SO, LEAVE WITH FAILURE |
| 290 | 003172 | 124227 | 000011 | CMPB | -(R2),#TAB | JIS THE LAST CHARACTER A TAB? |
| 291 | 003176 | 001773 |  | BEQ | 10$ | JIF SO, IGNORE IT |
| 292 | 003200 | 121227 | 000040 | CMPB | (R2),#BLANK | JIS IT A BLANK? |
| 293 | 003204 | 001770 |  | BEQ | 10$ | JIF SO, IGNORE IT |
| 294 | 003206 | 005202 |  | INC | R2 | JNON-BLANK CHARACTER--POINT PAST IT |
| 295 | 003210 | 160102 | 20$: | SUB | R1,R2 | JRE-COMPUTE LINE LENGTH |
| 296 | 003212 | 000241 |  | CLC |  | JINDICATE SUCCESS |
| 297 | 003214 | 000401 |  | BR | 40$ | JBRANCH TO LEAVE |
| 298 | 003216 | 000261 | 30$: | SEC |  | JINDICATE FAILURE |
| 299 | 003220 |  | 40$: | RETURN |  |  |
| 300 |  |  |  | ,DSABL | LSB |  |
| 301 |  |  |  |  |  |  |
| 302 |  |  |  |  |  |  |

SQUEEZE MACRO M0707 09-JUL-74 15:13 PAGE 4

### 6.3 DATA STORAGE DIRECTIVES

A wide range of data and data types can be generated with the following directives, ASCII conversion characters, and radix-control operators:

[figure from original manual omitted]

These MACRO-11 facilities are described in the following sections.

#### 6.3.1 .BYTE Directive

The .BYTE directive is used to generate successive bytes of binary data in the object module. The directive is of the form:

```txt
.BYTE    exp            ;STORES THE BINARY VALUE OF THE
                ;EXPRESSION "EXP" IN THE NEXT BYTE.
```

.BYTE     expl,exp2,expn    ;STORES THE BINARY VALUES OF THE LIST
                   ;OF EXPRESSIONS IN SUCCESSIVE BYTES.

A legal expression must reduce to eight bits of data or less. The operands of a .BYTE directive are evaluated as word expressions before being truncated to the low-order eight bits. The 16-bit value of the specified expression must have a high-order byte (which is truncated) that is either all zeros (0) or all ones (1). Each expression value is stored in the next byte of the object module. Multiple expressions, which must be separated by commas, are stored in successive bytes, as described below:

SAM=5
.=410
.BYTE ^D48,SAM ;THE VALUE 060 (OCTAL EQUIVALENT OF 48
;DECIMAL) IS STORED IN LOCATION 410.
;THE VALUE 005 IS STORED IN LOCATION
;411.

If the high-order byte of the expression reduces to a value other than 0 or -1, the value is truncated to the low-order eight bits and flagged with an error code (T) in the assembly listing.

The construction ^D in the first operand of the .BYTE directive above illustrates the use of a temporary radix-control operator. The function of such special unary operators is described in Section 6.4.1.2.

At link time, it is likely that a relocatable expression will result in a value having more than eight bits, in which case the linker

issues a truncation diagnostic for the object module in question. For example, the following statements create such a possibility:

        .BYTE 23          ;STORES OCTAL 23 IN NEXT BYTE.
A:
        .BYTE A          ;RELOCATABLE VALUE A WILL PROBABLY
            ;CAUSE TRUNCATION
            ;DIAGNOSTIC.

If an expression following the .BYTE directive is null, it is interpreted as a zero, as described below:

.=420
.BYTE , , , ;ZEROS ARE STORED IN BYTES 420, 421,
;422, AND 423.

Note that in the above example, four bytes of storage result from the .BYTE directive. The three commas in the operand field represent an implicit declaration of four null values, each separated from the other by a comma. Hence, four bytes, each containing a value of zero (0), are reserved in the object module.

#### 6.3.2 .WORD Directive

The .WORD directive is used to generate successive words of data in the object module. The directive is of the form:

.WORD exp ;STORES THE BINARY EQUIVALENT OF THE
;EXPRESSION EXP IN THE NEXT WORD.

.WORD     expl,exp2,expn    ;STORES THE BINARY EQUIVALENTS OF THE
                   ;LIST OF EXPRESSIONS IN SUCCESSIVE
                   ;WORDS.

A legal expression must result in 16 bits of data or less. Each expression is stored in the next word of the object program. Multiple expressions must be separated by commas and stored in successive words, as shown in the following example:

SAL=0
.=500
.WORD 177535,.+4,SAL ;STORES THE VALUES 177535, 506, AND
;0 IN WORDS 500, 502, AND 504,
;RESPECTIVELY.

If an expression following the .WORD directive contains a null value, it is interpreted as a zero, as shown in the following example:

.WORD      ,5,                  ;STORES THE VALUES 0, 5, AND 0 IN
                        ;LOCATION 500, 502, AND 504,
                        ;RESPECTIVELY.

A statement containing a blank operator field, i.e., a symbol that is not recognized by MACRO-ll as a macro call, an instruction mnemonic, a MACRO-ll directive, or a semicolon is interpreted during assembly as an implicit .WORD directive, as shown in the example below:

.=440
LABEL: 100, LABEL ;STORES THE VALUE 100 IN LOCATION 440
;AND THE VALUE 440 IN LOCATION 442.

**CAUTION:**

You should not use this technique to generate .WORD directives because it may not be included in future PDP-11 assemblers.

#### 6.3.3 ASCII Conversion Characters

The single quote (') and the double quote (") characters are unary operators that can appear in any MACRO-11 expression. When so used, these characters cause a 16-bit expression value to be generated.

When the single quote is used, MACRO-11 takes the next character in the expression and converts it from its 7-bit ASCII value to a 16-bit expression value. The 16-bit value is then used as an absolute term within the expression. For example, the statement:

MOV          # 'A, R0

results in the following 16-bit expression value being moved into
register 0:

[figure from original manual omitted]

Thus, in the example above, the expression 'A results in a value of 101(8). Note that the high-order byte is always zero (0) in the resulting expression value when the single quote unary operator is used.

The ' character must not be followed by a carriage-return, null, RUBOUT, line-feed, or form-feed character; if it is, an error code (A) is generated in the assembly listing.

When the double quote is used, MACRO-11 takes the next two characters in the expression and converts them to a 16-bit binary expression value from their 7-bit ASCII values. This 16-bit value is then used as an absolute term within the expression. For example, the statement:

MOV          #"AB,R0

results in the following 16-bit expression value being moved into
register 0:

[figure from original manual omitted]

Thus, in the example above, the expression "AB results in a value of 041101(8).

The " character also must not be followed by a carriage-return, null, RUBOUT, line-feed, or form-feed character; if it is, an error code (A) is likewise generated in the assembly listing.

The ASCII character set is listed in Section A.1, Appendix A.

#### 6.3.4 .ASCII Directive

The .ASCII directive translates character strings into their 7-bit ASCII equivalents and stores them in the object module. The format of the .ASCII directive is as follows:

    .ASCII /string l/.../string n/

where: string is a string of printable ASCII characters. All printable ASCII characters are legal. The vertical-tab, null, line-feed, RUBOUT, and all other non-printable ASCII characters, except carriage-return and form-feed, are illegal characters. Such an illegal non-printing character is flagged with an error code (I) in the assembly listing. The carriage-return and form-feed characters terminate the scan of the source line. This premature termination of the .ASCII statement results in the generation of an error code (A) in the assembly listing, because MACRO-11 is unable to complete the scan of the matching delimiter at the end of the character string.

/ / represent delimiting characters. These delimiters may be any paired printing characters, other than the equal sign (=), the left angle bracket (<), or the semicolon (;), as long as the delimiting character is not contained within the text string itself. If the delimiting characters do not match, or if an illegal delimiting character is used, the .ASCII directive is flagged with an error code (A) in the assembly listing.

A non-printing character can be expressed in an .ASCII statement only by enclosing its equivalent octal value within angle brackets. Each set of angle brackets so used represents a single character. For example, in the following statement:

    .ASCII <15>/ABC/<A+2>/DEF/<5><4>

the expressions <15>, <A+2>, <5>, and <4> represent the values of non-printing characters. Furthermore, the expressions must reduce to eight bits of absolute data or less, subject to the same rules for generating data as with the .BYTE directive (see Section 6.3.1).

Angle brackets can be embedded between delimiting characters in the character string, but angle brackets so used do not take on their usual significance as delimiters for non-printing characters. For example, the statement:

    .ASCII /ABC<expression>DEF/

contains a single ASCII character string, and performs no evaluation of the embedded, bracketed expression. This use of the angle brackets is shown in the third example of the .ASCII directive below:

```txt
.ASCI I /HELLO/ ;STORES THE BINARY REPRESENTATION
;OF THE LETTERS HELLO IN FIVE
;CONSECUTIVE BYTES.
.ASCI I /ABC/<15><12>/DEF/ ;STORES THE BINARY REPRESENTATION
;OF THE CHARACTERS A,B,C,CARRIAGE
;RETURN,LINE FEED,D,E,F IN EIGHT
;CONSECUTIVE BYTES.
.ASCI I /A<15>B/ ;STORES THE BINARY REPRESENTATION
;OF THE CHARACTERS A,<,1,5,>,
;AND B IN SIX CONSECUTIVE BYTES.
The semicolon (;) and equal sign (=) can be used as delimiting
characters in an ASCII string, but care must be exercised in so doing
because of their significance as a comment indicator and assignment
operator, respectively, as illustrated in the examples below:
.ASCI I ;ABC;/DEF/ ;STORES THE BINARY REPRESENTATION OF
;THE CHARACTERS A, B, C, D, E, AND F
;IN SIX CONSECUTIVE BYTES; NOT
;RECOMMENDED PRACTICE.
.ASCI I /ABC/;DEF; ;STORES THE BINARY REPRESENTATIONS OF
;THE CHARACTERS A, B, AND C IN THREE
;CONSECUTIVE BYTES; THE CHARACTERS D,
;E, F, AND ; ARE TREATED AS A COMMENT.
.ASCI I /ABC/=DEF= ;STORES THE BINARY REPRESENTATION
;OF THE CHARACTERS A, B, C, D, E, AND
;F IN SIX CONSECUTIVE BYTES; NOT
;RECOMMENDED PRACTICE.
An equal sign is treated as an assignment operator when it appears as
the first character in the ASCII string, as illustrated by the
following example:
.ASCI I =DEF= ;THE DIRECT ASSIGNMENT OPERATION
;.ASCII=DEF IS PERFORMED, AND A Q
;(SYNTAX) ERROR IS GENERATED UPON
;ENCOUNTERING THE SECOND = SIGN.
6.3.5 .ASCIZ Directive
The .ASCIZ directive is equivalent to the .ASCII directive described
above, except that a zero byte is automatically inserted as the final
character of the string. Thus, when a list or text string has been
created with an .ASCIZ directive, a search for the null character in
the last byte can effectively determine the end of the string, as
reflected by the coding below:
CR=15
LF=12
HELLO: .ASCII <CR><LF>/MACRO-11 V01A/<CR><LF> ;INTRODUCTORY MESSAGE
.EVEN
.
.
.
MOV #HELLO,R1 ;GET ADDRESS OF MESSAGE.
MOV #LINBUF,R2 ;GET ADDRESS OF OUTPUT BUFFER.
10$: MOVB (R1)+,(R2)+ ;MOVE A BYTE TO OUTPUT BUFFER.
BNE 10$ ;IF NOT NULL, MOVE ANOTHER BYTE.
.
.
.
6-21
```

The .ASCIZ directive is subject to the same checks for character legality and proper character string construction as described above for the .ASCII directive.

#### 6.3.6 .RAD50 Directive

The .RAD50 directive allows the user to generate data in Radix-50 packed format. Radix-50 form allows three characters to be packed into sixteen bits (one word); therefore, any 6-character symbol can be stored in two consecutive words. The form of the directive is:

.RAD50 /string l/.../string n/

If fewer than three characters are to be packed, the string is packed left-justified within the word, and trailing spaces are assumed.

As with the .ASCII directive described in Section 6.3.4, the vertical-tab, null, line-feed, RUBOUT, and all other non-printing characters, except carriage-return and form-feed, are illegal characters, resulting in an error code (I) in the assembly listing. Similarly, the carriage-return and form-feed characters result in an error code (A) because these characters end the scan of the line, preventing MACRO-11 from detecting the terminating matching delimiter.

/ / represent delimiting characters. These delimiters may be any paired printing characters, other than the equal sign (=), the left angle bracket (<), or the semicolon (;), provided that the delimiting character is not contained within the text string itself. If the delimiting characters do not match, or if an illegal delimiting character is used, the .RAD50 directive is flagged with an error code (A) in the assembly listing.

Examples of .RAD50 directives are shown below:

.RAD50 /ABC/ ;PACKS ABC INTO ONE WORD.

.RAD50 /ABCD/ ;PACKS ABC INTO FIRST WORD AND

| (space) | 0 |
| --- | --- |
| A-Z | 1-32 |
| $ | 33 |
| . | 34 |
| (undefined) | 35 |
| 0-9 | 36-47 |

Each character is translated into its Radix-50 equivalent, as indicated in the following table:

Character Radix-50 Octal Equivalent

The Radix-50 equivalents for characters 1 through 3 (C1,C2,C3) are combined as follows:

$$
\text {Radix - 50 Value} = ((\mathrm{C1} ^ {*} 5 0) + \mathrm{C2}) ^ {*} 5 0 + \mathrm{C3}
$$

For example:

$$
\text {Radix - 50 Value of ABC} = ((1 * 5 0) + 2) * 5 0 + 3 = 3 2 2 3
$$

Refer to Section A.2 in Appendix A for a table of Radix-50 equivalents.

Angle brackets (<>) must be used in the .RAD50 directive whenever special codes are to be inserted in the text string, as shown in the example below:

```asm
.RAD50 /AB/<35> ;STORES 3255 IN ONE WORD.
CHR1=1
CHR2=2
CHR3=3
.
.
.
.RAD50 <CHR1><CHR2><CHR3> ;EQUIVALENT TO .RAD50 /ABC/.
```

#### 6.3.7 Temporary Radix-50 Control Operator: ^R

The ^R operator specifies that an argument is to be converted to Radix-50 format. This allows up to three characters to be stored in one word. The ^R operator is coded as follows:

where ccc represents a maximum of three characters to be converted to a 16-bit Radix-50 value. If more than three characters are specified, any following the third character are ignored. If fewer than 3 are specified, it is assumed that the trailing characters are blanks. The following example shows how the ^R operator might be used to pack a 3-character file type specifier (MAC) into a single 16-bit word.

    MOV #^RMAC,FILEXT ;STORE RAD50 MAC AS FILE EXTENSION

The number sign (#) is used to indicate immediate data, i.e., data to be assembled directly into object code. ^R specifies that the characters MAC are to be converted to Radix-50. This value is then stored in location FILEXT.

### 6.4 RADIX AND NUMERIC CONTROL FACILITIES

#### 6.4.1 Radix Control and Unary Control Operators

The normal default assumption for numeric values or expression values appearing in a MACRO-ll source program is octal. However, numerous instances may occur where an alternate radix is useful for portions of a program or for variables within a given statement. It may be useful, for example, to declare a given radix for applicability throughout a program or to specify a numeric value or expression value in a manner that causes it to be interpreted as a binary, octal, or decimal value during assembly. In other such instances, it may be useful to complement numeric values or expression values. These MACRO-ll facilities are described in the following sections.

**NOTE:**

When two or more unary operators appear together, modifying the same term, the operators are applied, from right to left, to the term.

6.4.1.1 .RADIX Directive - Numbers used in a MACRO-ll source program are initially considered to be octal values; however, you can declare any one of the following radices for applicability throughout the source program or within specific portions of the program:

    2, 8, 10

This is accomplished via a .RADIX directive of the form:

    .RADIX n

where: n represents one of the three acceptable radices listed above. If the argument n is not specified, the octal default radix is assumed.

The argument in the .RADIX directive is always interpreted as a decimal value. Any alternate radix declared in the source program through the .RADIX directive remains in effect until altered by the occurrence of another such directive, i.e., a given radix declaration is valid throughout a program until changed. For example, the statement:

;BEGINS A SECTION OF CODE HAVING A
;DECIMAL RADIX.

    ;REVERTS TO OCTAL RADIX.

Any value other than null, 2, 8, or 10 specified as an argument in the .RADIX directive causes an error code (A) to be generated in the assembly listing.

In general, macro definitions should not contain or rely on radix settings established with the .RADIX directive. Rather, temporary radix control operators should be used within a macro definition. Where a possible radix conflict exists within a macro definition or in possible future uses of that code, it is recommended that the user

```txt
.RADIX 10
.WORD ^O<A+10>*10
```

specify numeric or expression values using the temporary radix control operators described below.

6.4.1.2 Temporary Radix Control Operators: ^D, ^O, and ^B - Once the user has specified a given radix for a section of code or has decided to use the default octal radix, he may discover a number of cases where an alternate radix is more convenient or desirable (particularly within macro definitions). The creation of a mask word, for example, might best be accomplished through the use of a binary radix.

MACRO-11 has three unary operators that allow the user to establish an alternate radix, as shown below:

```txt
^D"number" ("number" is evaluated as a decimal number)
^O"number" ("number" is evaluated as an octal number)
^B"number" ("number" is evaluated as a binary number)
```

Thus, an alternate radix can be declared temporarily to meet a localized requirement in the source program. Such a declaration can be made at any time, regardless of the existence of the default octal radix or another specific radix declaration elsewhere in the program. In other words, the effect of a temporary radix control operator is limited to the term or expression immediately following the operator. Any value specified in connection with a temporary radix control operator is evaluated during assembly as a 16-bit entity. Temporary radix control declarations can be included in the source program anywhere a numeric value is legal.

The expressions below are representative of the methods of specifying temporary radix control operators:

```csv
^D123 Decimal radix
^O 47 Octal Radix
^B 00001101 Binary Radix
^O<A+13> Octal Radix
```

Note that the up-arrow and the radix control operator may not be separated, but the radix control operator and the following term or expression can be physically separated by spaces or tabs for legibility or formatting purposes. A multi-element term or expression that is to be interpreted in an alternate radix should be enclosed within angle brackets, as shown in the last of the four temporary radix control expressions above.

The following example also illustrates the use of angle brackets to delimit an expression that is to be interpreted in an alternate radix:

A=10

When the temporary radix expression in the .WORD directive above is evaluated, it effectively yields the following equivalent statement:

```txt
.WORD 180.
```

MACRO-11 also allows a temporary radix change to decimal by specifying a number, immediately followed by a decimal point (.), as shown below:

100. Equivalent to 144(8)
1376. Equivalent to 2540(8)
128. Equivalent to 200(8)

The above expression forms are equivalent in function to those listed below:

^D100
^D1376
^D128

#### 6.4.2 Numeric Directives and Unary Control Operators

Two storage directives and two numeric control operators are available to simplify the use of the floating-point hardware on the PDP-11. These facilities allow floating-point data to be created in the program, and numeric values to be complemented or treated as floating-point numbers.

A floating-point number is represented by a string of decimal digits. The string (which can be a single digit in length) may optionally contain a decimal point, and may be followed by an optional exponent indicator in the form of the letter E and a signed decimal integer exponent. The number may not contain embedded blanks, tabs or angle brackets and may not be an expression. Such a string will result in one or more errors (A or Q) in the assembly listing.

The list of numeric representations below contains seven distinct, valid representations of the same floating-point number:

3
3.
3.0
3.0E0
3E0
.3E1
300E-2

As can be inferred, the list could be extended indefinitely (e.g., 3000E-3, .03E2, etc.). A leading plus sign is optional (e.g., 3.0 is considered to be +3.0). A leading minus sign complements the sign bit. No other operators are allowed (e.g., 3.0+N is illegal).

All floating-point numbers are evaluated as 64 bits in the following format:

64 63 56 55 0

S EEEEEEEE MMM.....MMM

Mantissa      (55 bits)
Exponent     (8 bits)
Sign          (1 bit)

MACRO-11 returns a value of the appropriate size and precision via one of the floating-point directives. The values returned may be truncated or rounded (see Section 6.2).

Floating-point numbers are normally rounded. That is, when a floating-point number exceeds the limits of the field in which it is to be stored, the high-order bit of the unretained word is added to the low-order bit of the retained word, as shown below. For example, if the number is to be stored in a 2-word field, but more than 32 bits are needed to express its exact value, the highest bit (32) of the

unretained field is added to the least significant bit (0) of the retained field (see illustration below). The .ENABL FPT directive is used to enable floating-point truncation; .DSABL FPT is used to return to floating-point rounding (see Table 6-2).

Bit                  Bit  Bit           Bit
32                 0 32 31          0

Retained              Unretained
field                field

Note that all numeric operands associated with Floating Point Processor instructions are automatically evaluated as single-word, decimal, floating-point values unless a temporary radix control operator is specified. For example, to add (floating) the octal constant 41040 to the contents of floating accumulator zero, the following instruction must be used:

ADDF #^041040,F0

where: F0 is assumed to represent floating accumulator zero.

Floating-point numbers are described in greater detail in the applicable PDP-11 Processor Handbook.

[figure from original manual omitted]

6.4.2.2 Temporary Numeric Control Operators: ^C and ^F - The ^C unary operator allows you to specify an argument that is to be complemented as it is evaluated during assembly. The ^F unary operator allows you to specify an argument consisting of a l-word floating-point number.

As with the radix control operators described above, the numeric control operator ( $^{C}$ ) can be used anywhere in the source program that an expression value is legal. Such a construction is evaluated by MACRO-11 as a 16-bit binary value before being complemented. For example, the following statement:

TAG4: .WORD \`C151

causes the l's complement of the value 15l (octal) to be stored as a 16-bit value in the program. The resulting value expressed in octal form is 177626(8).

Because the $^{C}$ construction is a unary operator, the operator and its argument are regarded as a term. Thus, more than one unary operator may be applied to a single term. For example, the following construction:

^C^D25

causes the decimal value 25 to be complemented during assembly. The resulting binary value, when expressed in octal form, reduces to 177746(octal).

The term created through the use of the temporary numeric control operator thus becomes an entity that can be used alone or in combination with other expression elements. For example, the following construction:

^C2+6

is equivalent in function to:

<^C2>+6

This expression is evaluated during assembly as the l's complement of 2, plus the absolute value of 6. When these terms are combined, the resulting expression value generates a carry beyond the most significant bit, leaving 000003(8) as the reduced value.

As shown above, when the temporary numeric control operator and its argument are coded as a term within an expression, angle brackets should be used as delimiters to ensure precise evaluation and readability.

MACRO-ll also supports a unary operator for numeric control which allows you to specify an argument consisting of a l-word floating-point number. For example, the following statement:

A:        MOV     #^F3.7,R0

creates a l-word floating-point number at location A+2 containing the value 3.7 formatted as shown below.

BIT 15                      14      7                   6       0
    S                       EEEEEEEE                  MMMMMMM
    Sign (bit 15)   Exponent (bits 14-7)  Mantissa (bits 6-0)

[figure from original manual omitted]

### 6.5 LOCATION COUNTER CONTROL DIRECTIVES

The directives used in controlling the value of the current location counter and in reserving storage space in the object program are described in the following sections.

In this connection, it should be noted that several MACRO-11 statements may cause an odd number of bytes to be allocated, as listed below:

1. .BYTE directive

2. .BLKB directive

3. .ASCII or .ASCIZ directive

4. .ODD directive

5. A direct assignment statement of the form .=.+expression, which results in the assignment of an odd address value.

In cases that yield an odd address value, the next word-boundaried instruction automatically forces the location counter to an even value, but that instruction is flagged with an error code (B) in the assembly listing.

#### 6.5.1 .EVEN Directive

The .EVEN directive ensures that the current location counter contains an even value by adding 1 if the current value is odd. If the current location counter is already even, no action is taken. Any operands following an .EVEN directive are flagged with an error code (Q) in the assembly listing.

The .EVEN directive is used as follows:

.ASCIZ /THIS IS A TEST/
.EVEN ;ENSURES THAT THE NEXT STATEMENT WILL
;BEGIN ON A WORD BOUNDARY.
.WORD XYZ

#### 6.5.2 .ODD Directive

The .ODD directive ensures that the current location counter contains an odd value by adding 1 if the current value is even. If the current location counter is already odd, no action is taken. Any operands following an .ODD directive are also flagged with an error code (Q) in the assembly listing.

#### 6.5.3 .BLKB and .BLKW Directives

Blocks of storage can be reserved in the object program by means of the .BLKB and .BLKW directives. The .BLKB directive is used to reserve byte blocks; similarly, the .BLKW directive reserves word blocks. The two directives are of the form:

.BLKB exp
.BLKW exp

where: exp represents the specified number of bytes or words to be reserved in the object program. If no argument is present, a default value of 1 is assumed. These directives should not be used without arguments. Any expression that is completely defined at assembly-time and that reduces to an absolute value is legal. If the expression specified in either of these directives is not an absolute value, the statement is flagged with an error code (A) in the assembly listing.

Figure 6-6 illustrates the use of the .BLKB and .BLKW directives.

[figure from original manual omitted]

Figure 6-6 Example of .BLKB and .BLKW Directives

The .BLKB directive in a source program has the same effect as the following statement:

    .=.+expression

which causes the value of the expression to be added to the current value of the location counter. The .BLKB directive, however, is easier to interpret in the context of the source code in which it appears and is therefore recommended.
