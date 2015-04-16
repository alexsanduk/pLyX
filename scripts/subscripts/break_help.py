def helpnote(hv):
    if hv > 1:
        return header + version
    else:
        return header + tail

header = r'''\begin_layout LyX-Code
\family roman
\series bold
.stop
\end_layout
'''
version = r'''\begin_layout LyX-Code
\family roman
Version 1.0 (10 December 2012) -x option added.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.1 (3 December 2012)
\end_layout
'''
tail = r'''\\begin_layout LyX-Code
\family roman
Stop activation of any following scripts.
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
-h  
\series default
show this help message.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-v  
\series default
show version information.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-x  
\series default
stop activation of any following scripts but also delete the 
\family default
.stop
\family roman
 inset.
\end_layout
'''


