# a2 [![Join the chat at https://gitter.im/ewerybody/a2](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/ewerybody/a2?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Script managing and developing framework for [Autohotkey](http://ahkscript.org/) with [PySide](https://wiki.qt.io/PySide) (Python/Qt) frontend.<br>
See [wiki](https://github.com/ewerybody/a2/wiki) for more information especially the page about [setting you up](https://github.com/ewerybody/a2/wiki/setting-you-up).

## news:
* **package building** :package: works now! Using [PyInstaller](https://github.com/pyinstaller/pyinstaller) and some batch and py scripting we can now build self-containing a2 packages with no further dependencies. To do that of course there is now one more dependency: `pip install PyInstaller`. [The milestone](https://github.com/ewerybody/a2/milestones/alpha%20preview) is coming closer!!
* since there is no option for a default issue view [**backlog**](https://github.com/ewerybody/a2/issues?q=label%3Abacklog) and [**wontfix**](https://github.com/ewerybody/a2/issues?q=label%3Awontfix) issues have been "closed" for better overview (and looking like there is less todo). They are still there! That's why I put the links. When such an issue is tackled it will be opened again. When closed the wontfix or backlog label will be removed.
* **a2/a2.modules separation complete!** There are still a lot of features to add but the main functionality is implemented: One can have multiple module sources and enable/disable them individually. You see there is a lot less [Autohotkey code here](https://github.com/ewerybody/a2/search?l=autohotkey) now. See [the **a2.modules** project](https://github.com/ewerybody/a2.modules) for the standard ones. 

## a2 main loop layout:
![](doc/a2_layout.gif?raw=true)

## blog posts:
* [a2 – the first humble steps](http://goodsoul.de/?p=780)

## <a name="dev-team"></a>Authors/Contributors  
* [ewerybody](https://github.com/ewerybody)
* [Oliver Lipkau](https://github.com/lipkau)
