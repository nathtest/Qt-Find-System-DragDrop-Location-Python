# Qt-Find-System-DragDrop-Location-Python
A solution to find DragDrop file location for Qt

This example can be used to find the path of a drop location in Windows (not tested on Linux). Since Windows does not provide a way to know a drop location nor to track a file movement across its system.
It can be useful if you need to create a temporary file in case it's creation take too long or if you need to download the file (from an FTP server).
Watching the whole drive does not seem to be too heavy resource wise as it's used only a couple of seconds to find the drop location.

A QTable example is also provided.

TODO:Watch every drive connected to the system.
