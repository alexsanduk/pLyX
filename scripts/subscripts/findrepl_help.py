def helpnote(hv):
    if hv > 1:
        return header + version
    else:
        return header + tail

header = r'''\begin_LyX-Code
\family roman
\series bold
.find-&-replace
\end_layout
'''

version = r'''\begin_layout LyX-Code
\family roman
Version 1.3 (15 Jan 2014) Fix bug with -i (inset) searches; use of \n
\end_layout
\begin_layout LyX-Code
\family roman
Version 1.2 (3 Dec 2013) Repeated (loop) searches; refined text, math,
 inset searches; use of LyX insets/formatting in arguments
\end_layout
\begin_layout LyX-Code
\family roman
Version 1.1 (11 Nov 2013) Text or math only searches; removed count function.
\end_layout
\begin_layout LyX-Code
\family roman
Version 1.0 (19 Jan 2013) RE flags & search block size spec.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.2 (13 Jan 2013) Regular expression searches.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.1 (8 Jan 2013)
\end_layout
'''
tail = r'''\begin_layout LyX-Code
\family roman
Replace elements of LyX format code (including restricted text, math
 and inset searches).
\end_layout
\begin_layout LyX-Code

\end_layout
\begin_layout LyX-Code
\family roman
\series bold
Global options
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-h --help  
\series default
show this help note.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-s --suppress  
\series default
suppress number-of-replacements messages.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-v --version  
\series default
show version information.
\end_layout
\begin_layout LyX-Code

\end_layout
\begin_layout LyX-Code
\family roman
\series bold
Global/local options
\end_layout
\begin_layout LyX-Code
\family roman
\emph on
Modifiers:
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-r  
\series default
use regular expressions.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-x  
\series default
exclude (allow a narrower search).
\end_layout
\begin_layout LyX-Code
\family roman
\emph on
Search modes:
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
(no option)    
\series default
default mode: search everything.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-m  
\series default
restrict searches to math insets only.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-m -x  
\series default
math search: exclude control sequences and labels from the search.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-t  
\series default
restrict searches to text only.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-t -x  
\series default
text search: exclude inset text.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-t -i  
\series default
text search: restrict searches to insets only.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-i -x  
\series default
inset settings search (inset search: exclude inset text). (
\emph on
Note:
\emph default
 as currently implemented, the 
\series bold
-i
\series default
 option, without modifier, is equivalent to 
\series bold
-i -x
\series default
.)
\end_layout
\begin_layout Itemize
\family roman
To find & replace some (possibly multi-line) element of LyX format code,
 enter the code to be found in an 
\family sans
.[argument]
\family roman
 inset immediately following a 
\family sans
.find-&-replace (LyX format)
\family roman
 inset inserted in the document. The replacement code is entered in another 
\family sans
.[argument]
\family roman
 inset immediately following the first. (You can copy code from the  
\family sans
View Source
\family roman
 window and use 
\family sans
Paste Special
\family roman
, in the 
\family sans
Edit
\family roman
 menu, to paste it into either inset.)
 Another 
\family sans
.find-&-replace (LyX format)
\family roman
 inset inserted later in the document will stop the find & replace
 at that point, where the total number of replacements will be displayed
 in a (yellow) note.
 Depending on whether this second 
\family sans
.find-&-replace (LyX format)
\family roman
 inset is followed by two 
\family sans
.[argument]
\family roman
 insets, the first (at least) with content, a new find & replace may be
 initiated at this point.
\end_layout

\begin_layout Itemize
\family roman
To restrict replacement to text only, leaving LyX format code
 and math insets unaffected, use the 
\series bold
-t
\series default
 option in a 
\family sans
.find-&-replace (LyX format) 
\family roman
 inset. To further restrict the search to main document text, excluding text in
 captions, tables, notes and other insets, use the 
\series bold
-t -x
\series default
 option. Alternatively, to search only the text in insets, use the 
\series bold
-t -i
\series default
 option. (For text searches, the find-&-replace is restricted to within
 paragraphs, nor does it straddle changes in character styling, like emphasis,
 or other LyX commands.)
\end_layout

\begin_layout Itemize
\family roman
To restrict replacement to math insets only, leaving 
 text and (other) insets unaffected, use the 
\series bold
-m
\series default
 option in a 
\family sans
.find-&-replace (LyX format) 
\family roman
 inset. To further restrict the search so that control sequences and
 labels are excluded, use the 
\series bold
-m -x
\series default
 option.
\end_layout

\begin_layout Itemize
\family roman
To restrict replacement to (non-math) insets only, use either the 
\series bold
-i -t
\series default
 option in a 
\family sans
.find-&-replace (LyX format) 
\family roman
 inset to search inset 
\emph on
text
\emph default
, or the 
\series bold
-i -x
\series default
 option to search inset 
\emph on
settings
\emph default
. (As currently implemented, the latter
 is equivalent to 
\series bold
-i
\series default
 without modifier.)
\end_layout

\begin_layout Itemize
\family roman
The yellow note messages detailing how many replacements
 have been made can be suppressed with the global 
\series bold
-s
\series default
 option.
 The default is to show them. For text-only or math-only searches, 
 the number of replacements indicated is only a 
\emph on
lower
\emph default
 estimate.
\end_layout

\begin_layout Itemize
\family roman
Regular expression searches can be conducted in all modes
 (default, text, math, inset) by using the 
\series bold
-r
\series default
 (or 
\series bold
--regexp
\series default
) option, globally or locally, in a 
\family sans
.find-&-replace (LyX format)
\family roman
 inset. Regular expression flags (e.g. I = ignore case sensitivity, D = dot all,
 meaning . now includes the new line character),
 and a search block size specification can also be inserted in this inset. 
\end_layout

\begin_layout Itemize
\family roman
If a 
\emph on
third 
\emph default
\family sans
.[argument]
\family roman
 inset is added to the 
\begin_inset Quotes els
\end_inset
find
\begin_inset Quotes ers
\end inset
 and 
\begin_inset Quotes els
\end_inset
replace
\begin_inset Quotes ers
\end inset
 argument insets, and a 
\family sans
.loop
\family roman
 custom inset inserted in the 
\family sans
.Run script(s)
\family roman
 inset, a sequence of replacements can be made, one for each
  paragraph-separated item in the third argument inset. This allows,
  e.g., the semi-automatic indexing of a list of terms.
\end_layout

\begin_layout Itemize
\family roman
For more details on these subjects, with examples of use, see
 the accompanying documentation: 
\emph on
The pLyX system: replacing LyX format code
\emph default
 for details.
\end_layout

\end_layout

'''
