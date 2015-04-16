def helpnote(hv):
    if hv > 1:
        return header + version
    else:
        return header + tail

header = r'''\begin_layout LyX-Code
\family roman
\series bold
.sort list
\end_layout
'''
version = r'''\begin_layout LyX-Code
\family roman
Version 1.1 (22 November 2013) Allow random sorts (shuffles);
 fix numerical sort bug.
\end_layout
\begin_layout LyX-Code
\family roman
Version 1.0 (16 December 2012) Allow secondary, tertiary, etc. sorts.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.2 (13 December 2012) Include -a and -n options.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.1 (8 November 2012)
\end_layout
'''
tail = r'''\begin_layout LyX-Code
\family roman
Sort one or more lists and sub-lists.
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
     show this help message.
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
-a  
\series default
                sort across changes of list-type.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-c 
\emph on
n
\emph default
\series default
              
\emph on
n
\emph default
 = number of characters in sort-key
 strings; default is 20 characters.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-n  --notes
\series default
    make LyX's (yellow) notes sortable; notes are sort-neutral by default.
\end_layout
\begin_layout LyX-Code
 
\end_layout
\begin_layout LyX-Code
\family roman
A change of list type at the top level (e.g.
 from 
\family sans
Itemize
\family roman
 to 
\family sans
Description
\family roman
) usually halts a sort; the 
\series bold
-a
\series default
 option ensures the sort continues across the list-type boundary.
 (The result is generally a mess, but a sorted one.) Sorting always
 continues across list-type boundaries in sub-lists (but, again,
 generates a sorted mess).
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
1a2a3+
\series default
 or 
\series bold
2r
\series default
 where the number indicates the list level (1 = first or top level, 2 =
 sub-list, etc.) and the qualifying letter or sign indicates the kind
 of sort. A specification may involve from one to (potentially) all six list
 levels; if desired, only sub-levels may be sorted (as in the second example)
 For secondary, tertiary ... sorts, separate the sort specs. by a solidus, e.g. 
\series bold
1a2a3+/1A2A
\series default
.
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
\series bold
a, A, z, Z
\series default
 indicate alphabetical sorts, uppercase indicating case sensitivity;
\end_layout
\begin_layout Itemize
\family roman
\series bold
+, -
\series default
 indicate numerical sorts.
\end_layout
\begin_layout Itemize
\family roman
\series bold
r, R
\series default
 indicate random sorts (shuffles),  
\series bold
R
\series default
 forcing a new seed for the random number generator with each sort.
\end_layout
\begin_layout LyX-Code
\family roman
The specification is placed either before or within a 
\emph on
top-level
\emph default
 item in a list. The 
\emph on
next
\emph default
 and subsequent items in a list following a sort specification are sorted. If
 the 
\emph on
 kind
\emph default
 of list changes (say from
\family sans
 Labeling
\family roman
 to
\family sans
 Description
\family roman
), the sort stops at the change, unless the 
\series bold
-a
\series default
 option has been invoked.
\end_layout
'''


