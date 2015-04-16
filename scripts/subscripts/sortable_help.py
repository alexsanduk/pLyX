def helpnote(hv):
    if hv > 1:
        return header + version
    else:
        return header + tail

header = r'''\begin_layout LyX-Code
\family roman
\series bold
.sort table
\end_layout
'''
version = r'''\begin_layout LyX-Code
\family roman
Version 1.0 (15 December 2012) Columns can be sorted more than once for
 inter-filed mixed-case alphabetical sorting.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.4 (1 November 2012) First version for pLyX system.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.3 (17 September 2012) Use of custom insets; yellow notes option,
 hrules and vrules preserved.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.2 (13 September 2012) Script now ignores ERT insets.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.1 (12 September 2012 Table sorting script posted to user's list.
\end_layout
'''
tail = r'''\begin_layout LyX-Code
\family roman
Sort the
\emph on
 rows
\emph default
 by the values in specified columns.
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
-
\series bold
h  --help
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
\series bold
-n  --notes
\series default
    make LyX's (yellow) notes sortable; notes are
 sort-neutral by default.
\end_layout
\begin_layout LyX-Code
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
Local options
\end_layout
\begin_layout LyX-Code
\family roman
A sort specification is a sequence like 
\series bold
2a3A1+
\series default
 (or 
\series bold
2a 3A 1+
\series default
 or 
\series bold
2a
\series default
,
\series bold
 3A
\series default
,
\series bold
 1+
\series default
, etc.) where the number indicates the column and the qualifying letter or
 sign indicates the kind of sort. A specification may involve from one to
 all columns in the table and a column may appear in the spec. more than once.
 The primary sort is by the first column specified, the secondary sort by
 the second column, etc. 
\end_layout
\begin_layout Itemize
\family roman
\series bold
a, A, +
\series default
 indicate ascending sorts; 
\end_layout
\begin_layout Itemize
\family roman
\series bold
z, Z, -
\series default
 indicate descending sorts; 
\end_layout
\begin_layout Itemize
\family roman
letters indicate alphabetical sorts, uppercase indicating case sensitivity;
\end_layout
\begin_layout Itemize
\family roman
\series bold
+, -
\series default
 indicate numerical sorts.
\end_layout
\begin_layout LyX-Code
\family roman
The 
\emph on
next
\emph default
 and subsequent rows of a table following a sort specification are sorted.
 For neat alphabetical sorts involving inter-filed mixed case, specify columns
 twice, e.g. 
\series bold
1a1A
\series default
 for an AaBbCc ... sort, or
\series bold
1a1Z
\series default
 for an aAbBcC ... sort.
\end_layout
'''


