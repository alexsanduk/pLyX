def helpnote(hv):
    if hv > 1:
        return header + version
    else:
        return header + tail

header = r'''\begin_layout LyX-Code
\family roman
\series bold
.Run script(s)           
\end_layout
'''
version = r'''\begin_layout LyX-Code
\family roman
Version 1.1 (24 November 2013) 
\family sans
.loop
\family roman
 inset introduced.
\end_layout
\begin_layout LyX-Code
\family roman
Version 1.0 (3 December 2012) 
\family default
.stop
\family roman
 inset introduced.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.2 (1 November 2012) Allow a sequence of scripts to be run.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.1 (6 October 2012)
\end_layout
'''
tail = r'''\begin_layout LyX-Code
\family roman
Run a script a script or scripts manipulating the current document.           
\end_layout
\begin_layout LyX-Code
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
Global options
\series default
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
-v --version  
\series default
show version information.
\end_layout

\begin_layout Itemize
\family roman
To run a script, insert a 
\begin_inset Quotes els
\end_inset
dotted
\begin_inset Quotes ers
\end_inset
custom inset (one with a leading dot) from those listed under 
\family sans
Insert \SpecialChar \menuseparator
 Custom Insets
\family roman
 into the 
\family sans
.Run script(s)
\family roman
 inset. Into the inserted inset insert any desired 
\emph on
global
\emph default
 options, e.g.,
 
\begin_inset Flex .Run script(s)
status open
\begin_layout Plain Layout
\family roman
\begin_inset Flex .calculate formula|calcul8
status open
\begin_layout Plain Layout
\family roman
-h
\end_layout
\end_inset
\end_inset
 to see the help note for the
 
\family sans
.calculate formula
\family roman
 inset, then either click the three pLyX activating buttons in sequence,
 or click the 
\family sans
View other formats
\family roman
 button and select 
\family sans
 View pLyX
\family roman
 from the list. The latter leaves the original document unaltered and is the
 safer method of proceeding.
\end_layout

\begin_layout Itemize
\family roman
To run a sequence of scripts, enter them in sequence in the 
\family sans
.Run script(s)
\family roman
 inset, e.g. 

\begin_inset Flex .Run script(s)
status open
\begin_layout Plain Layout
\family roman
\begin_inset Flex .calculate formula|calcul8
status open
\begin_layout Plain Layout
\end_layout
\end_inset

\begin_inset Flex .sort table|sortable
status open
\begin_layout Plain Layout
\end_layout
\end_inset

\end_inset
.
\end_layout

\begin_layout Itemize
\family roman
To run the same script repeatedly, insert its associated
 custom inset into the 
\family sans
.Run script(s)
\family roman
 inset, preceded by a 
\family sans
.Loop
\family roman
 custom inset. Only some scripts are capable of using this feature, e.g. the
 find-&-replace script. See the help for the individual script.
\end_layout

\begin_layout Itemize
\family roman
The undo list is emptied by running a script. To undo the effect of a script,
 click the 
\family sans
undo pLyX
\family roman
 then 
\family sans
reload
\family roman
 buttons. This reloads the back-up document (but does not restore the undo list).
\end_layout
'''

def unknown():
    return r'''\begin_layout LyX-Code
\family roman
Unknown script (or no script) specified! Ensure the 
\family typewriter
pLyX
\family roman
 module has been added
 to your document and insert the 
\family sans
.Run script(s)
\family roman
 custom inset in place of this note (perhaps with the  
\series bold
-h
\series default
 or
 \series bold
--help
\series default
 option entered in it).
\end_layout
'''

def whatopt():
    return r'''\begin_layout LyX-Code
\family roman
Unknown option specified!
\end_layout
\begin_layout LyX-Code
\family roman
 Enter 
\series bold
-h
\series default
 for help.
\end_layout
'''
