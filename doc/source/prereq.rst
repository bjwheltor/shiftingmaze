Prerequisites
=============

External libraries
------------------

The code makes use of three external libraries:

 * 
 * `NumPy <https://numpy.org/>`_ - handles state of the board
 * `Pygame <https://www.pygame.org/>`_ - handles visual aspects and keyboard input
 * `sys <https://docs.python.org/3/library/sys.html>`_ - handles game exit

Windows X server
----------------

This was developed Linux environment in Windows Subsystem for Linux (WSL), 
using Visual Studio Code (VSC or Code) as an IDE, 
running in a Windows enviroment.
However, there is a need to cast the display onto an X-window, 
which requires some additional code to run a Windows  xServer.
`VcXsrv Windows X Server <https://sourceforge.net/projects/vcxsrv/>`_
was use for this purpose.

This is separate from the game and needs to be launched
before running the game code.
During setup is important to disable the access control to avoid the 
permission denied error when trying to run a GUI application.
Ensure that “Disable access control” will be always checked.

Also ensure the ``$DISPLAY`` is always set correctly using:

``echo "export DISPLAY=localhost:0.0" >> ~/.bashrc``