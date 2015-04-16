def helpnote(hv):
    if hv > 1:
        return header + version
    else:
        return header + tail

header = r'''\begin_layout LyX-Code
\family roman
\series bold
.count word frequency
\end_layout
'''
version = r'''\begin_layout LyX-Code
\family roman
Version 1.0 (20 February 2013) --incl option for numbers & hyphens
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.3 (16 February 2013) replaced --note with --style option
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.2 (8 February 2013) replaced --all with --env option
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.1 (7 February 2013) with -n, -m, --all, --alpha options
\end_layout
'''
tail = r'''\begin_layout LyX-Code

\family roman
Count the frequency of occurrence of words in a document.
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
-h  --help
\series default
      show this help note.
\end_layout

\begin_layout LyX-Code

\family roman
\series bold
-v --version
\series default
  show version information.
\end_layout

\begin_layout LyX-Code

\family roman
\emph on
Scanning text:
\end_layout

\begin_layout LyX-Code

\family roman
\series bold
--env
\emph on
 Env1 Env2 ...

\series default
\emph default
  scan text in specified environments (default is Standard only); use 
\series bold
--env All
\series default
 to scan all environments.
\end_layout

\begin_layout LyX-Code

\family roman
\series bold
--incl
\emph on
 [[hyphens] [numerals]]
\series default
\emph default
  include hyphens and/or numerals as letters; e.g.
 
\series bold
--incl hyphens
\series default
 (or just 
\series bold
--incl h
\series default
) will treat hyphens (but not numbers) as letters.
\end_layout

\begin_layout LyX-Code

\family roman
\series bold
--min 
\emph on
N
\series default
\emph default
  minimum word length: count only words of 
\emph on
N
\emph default
 or more characters (default is 1).
\end_layout

\begin_layout LyX-Code

\family roman
\emph on
Displaying results:
\end_layout

\begin_layout LyX-Code

\family roman
\series bold
--alpha
\series default
  sort words in occurrence lists alphabetically (default is by word length).
\end_layout

\begin_layout LyX-Code

\family roman
\series bold
--style 
\emph on
[[text][note][ert]]
\series default
\emph default
  display results at end of document either as text, or in a LyX note  (both
 are verbose modes), or only occurrence, instance number pairs in an ERT
 inset.
\end_layout

\begin_layout Itemize

\family roman
The text scanned is, by default, only that within Standard paragraphs.
 To include different environments (e.g., Standard, Quotation, Verse, section
 headings, etc.), use the
\series bold
 --env
\series default
 option followed by a space-separated list of the desired environments (as
 they appear in the drop-down box on the toolbar).
 To scan 
\emph on
all
\emph default
 environments, write
\series bold
 --env All
\series default
.
\end_layout

\begin_layout Itemize
Note that
\emph on
 insets are not scanned
\emph default
.
 Hence, footnotes are not scanned (and paragraphs not to be scanned can
 be hidden in a branch).
\end_layout

\begin_layout Itemize
To count only words of at least a certain length, use the 
\series bold
--min
\emph on
 N
\series default
\emph default
 option.
\end_layout

\begin_layout Itemize
Hyphens are treated as letters with the 
\series bold
--incl h
\series default
 option; numbers are treated as letters with the 
\series bold
--incl n
\series default
 option (so that 
\series bold
--incl h n
\series default
 does both).
\end_layout

\begin_layout Itemize
The script scans text from the start of the document, counting the number
 of occurrences of different words and presenting the results at the end
 of the document, either as normal text (the default) or in a (yellow) LyX
 note, or  .
 A typical line in the display is:
\begin_inset Newline newline
\end_inset


\begin_inset Newline newline
\end_inset

5 occ.
 (9 inst.): as, up, into, were, only, climb, river, there, remember
\begin_inset Newline newline
\end_inset


\begin_inset Newline newline
\end_inset

indicating that within the text scanned there were 9 instances of  words
 occurring 5 times; the words are, by default, listed in order of word length,
 which makes it easy to pick out 
\begin_inset Quotes els
\end_inset

debris
\begin_inset Quotes ers
\end_inset

.
\end_layout

\begin_layout Itemize
 If the minimum word length is set at, say, 4 or more, an alphabetical ordering
 may be preferred; in that case, use the 
\series bold
--alpha
\series default
 option.
\end_layout
'''


