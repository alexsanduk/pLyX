def helpnote(hv):
    if hv > 1:
        return header + version
    else:
        return header + tail

header = r'''\begin_layout LyX-Code
\family roman
\series bold
.update citations .[Argument]
\end_layout
'''
version = r'''\begin_layout LyX-Code
\family roman
Version 0.1 (8 April 2015) with -v , -h and -s options.
\end_layout
'''
tail = r''' \begin_layout LyX-Code
\family roman
Update the citations according to the excel file provided as an argument.
 The excel file is compulsory.
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
-v           
\series default
        verbose statistics for each citation key at the end of the file.
\end_layout

\begin_layout LyX-Code

\family roman
\series bold
-s --suppress  
\series default
suppress number-of-replacements for each key at the end of the file.
\end_layout

\begin_layout LyX-Code

\end_layout

\begin_layout Itemize

\family roman
Several
\family default
\series bold
 .update citations
\family roman
\series default
  can be provided in the document.
\end_layout

\begin_layout Itemize
The citations keys to be updated are the one following the command.
 The citations keys before are not going to be updated.
\end_layout

\begin_layout Itemize
Excel file should contain two columns.
 The first column should contain the keys to be updated.
 The second column should contain the corresponding new keys.
\end_layout
'''
