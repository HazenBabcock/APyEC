### APyEC ###
A Git / Python / PyQt electronic notebook.

### Overview ###
This uses git for version control and PyQt for the user interface. It makes heavy use of context menus, so when in doubt try right clicking.

Content can be in markdown or ReST format. This is specified with the Content Type spin box in the note editor.

Attachments can be added to a note by dragging and dropping to the attachments area of the note editor.

You can add an attachment into a note by right clicking on the attachment to get a link that you can paste into the note.

You can link to another note by selecting the note that you want to link to, right clicking on the note content display to get a link, and then pasting this link into the content of the note that you are editting.

Each notebook is an independent git repository.

To sync your notes with a remote git server you will need to have SSH keys configured.

### Dependencies ###
* [docutils](https://pypi.python.org/pypi/docutils)
* [git](https://git-scm.com/)
* [markdown](https://pypi.python.org/pypi/Markdown)
* [Python 2.7](https://www.python.org/)
* [PyQt4](http://www.riverbankcomputing.com/software/pyqt/intro)
