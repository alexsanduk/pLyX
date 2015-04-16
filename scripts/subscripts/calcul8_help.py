def helpnote(hv):
    if hv > 1:
        return header + version
    else:
        return header + tail

header = r'''\begin_layout LyX-Code
\family roman
\series bold
.calculate formula
\end_layout
'''
version = r'''\begin_layout LyX-Code
\family roman
Version 1.0 (19 November 2012)
\end_layout
'''
tail = r'''\begin_layout LyX-Code
\family roman
Calculate a (real or complex) mathematical expression.
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
 show this help note.
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
-j
\series default
    evaluate (higher) functions of a complex variable.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-r
\series default
    retain the expression to be calculated in the document; default is to
 retain only the result.
\end_layout
\begin_layout Itemize

\family roman
The calculator will evaluate 
\emph on
rational
\emph default
 expressions involving complex numbers without the 
\series bold
-j
\series default
 option.
 (
\family default
Enter complex numbers in the form 
\series bold
2+1j
\series default
, 
\series bold
7.3-2.8j
\series default
, etc.; note that, e.g., 
\series bold
2+j
\series default
 will result in error
\family roman
.) The option makes available trigonometric, hyperbolic, exponential, logarithmic
, and some other functions.
 For a complete list see the documentation for python's 
\family typewriter
cmath
\family roman
 module.
\end_layout
\begin_layout Itemize
\family roman
If the expression is retained in the document (the
 
\series bold
-r
\series default
 option), it is followed by 
\begin_inset Quotes els
\end_inset
 = 
\begin_inset Quotes ers
\end_inset
 and the result (e.g.

\series bold
 1+1 = 2
\series default
) but is 
\emph on
not
\emph default
 placed in a mathematical inset.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
Local options
\end_layout
\begin_layout LyX-Code
\family roman
Enter an arithmetic or mathematical expression (e.g.
 
\series bold
1+1
\series default
, or 
\series bold
sqrt(3**2+4**2)
\series default
, or 
\series bold
pi**e-e**pi
\series default
) into the inset.
\end_layout
\begin_layout Itemize
Use the four familiar arithmetic operators +,  -, *, /; use ** for exponentiatio
n and parentheses to clarify ambiguous expressions or assert order of calculatio
n.
\end_layout
\begin_layout Itemize
\family roman
Two constants are available:
\series bold
 pi
\series default
 and
\series bold
 e
\series default
.
\end_layout
\begin_layout Itemize
\family roman
Also available are the familiar trigonometric, hyperbolic, exponential and
 logarithmic functions.
 For inverse trigonometric or hyperbolic functions, use
\series bold
 asin(x)
\series default
,
\series bold
 asinh(x)
\series default
, etc.
\end_layout
\begin_layout Itemize
\family roman
For a complete list of the available functions (which is much greater than
 those instanced) see the help file for python's
 
\family typewriter
math
\family roman
 module.
\end_layout
'''


