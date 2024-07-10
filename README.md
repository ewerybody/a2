# a2 [![Codacy Badge](https://api.codacy.com/project/badge/Grade/0bc56698a44144e68ff191105f97215d)](https://app.codacy.com/app/ewerybody/a2?utm_source=github.com&utm_medium=referral&utm_content=ewerybody/a2&utm_campaign=badger) [![Join the chat at https://gitter.im/ewerybody/a2](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/ewerybody/a2?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Join the chat on Telegram](ui/res/telegram_join.svg)](https://t.me/a2script_de)

[**Autohotkey**](https://github.com/AutoHotkey/AutoHotkey) is an awesome little scripting language to automate and simplify all things Windows.\
(See [Tom Scott ranting about it on YouTube](https://youtu.be/lIFE7h3m40U))\
**a2** helps getting, updating scripts and developing your own.

Basically a2 is an **Autohotkey runtime** running in the background that you conveniently configure with a [Qt for Python](https://wiki.qt.io/Qt_for_Python) **UI**.

Features for this background app come via **modules** bundled in **packages**.\
Each module can have various script or configuration files\
and is presented with its own frontend UI to setup Hotkey shortcuts, Variables ect...\
These frontend UIs are comprised of reusable elements that a developer can easily arrange.

See [the Wiki](https://github.com/ewerybody/a2/wiki) for more information especially:
* [How to use a2](../../wiki/How-to-use-a2).
* [How to develop a2](../../wiki/How-to-develop-a2).



## Who is it for?

### Everyday Computer people looking to automate/simplify working with Windows.
* Simple setup and management of scripts
  * no files to copy around or edit
  * updates via button press
  * no intrusive installation (all integrations steps visualized, uninstall/delete and its gone)
  * no Admin rights needed
* A range of things to try out
* Build own simple modules without a line of code
* ...

### Autohotkey Script Developers
* no boilderplate code needed
* broad library to keep your code DRY
* clickable UI components for most use-cases
* streamlined github driven deployment
* ...


## news:
* Apologies for the long silence here. But there are some nice big updates cooking :)
  * The AHK2 conversion is almost complete! Like [speculated in my blogpost]([url](https://goodsoul.de/blog/a2works4me/)) I jumped into [the Autohotkey 2 task]([url](https://github.com/ewerybody/a2/issues/266)) right away. There are now `ahk2` branches [in here]([url](https://github.com/ewerybody/a2/tree/ahk2)), [a2.modules]([url](https://github.com/ewerybody/a2.modules/tree/ahk2)) as well as [a2.modlab]([url](https://github.com/a2script/a2.modlab/tree/ahk2)) with over 140 commits!
  * What needs to be done now aren't just the other things I blogged, sadly. First the dev experience needs to be improved a bit! There will be some tooling, helping ahk1 workspaces to adapt to the changes. Some of that will also be valid for the releases. Like making custom changes fit for ahk2. I think I'll do another blog post about the general conversion soon there are some handfull of insights but not too many.
  * then the build scripts and install loop need some love
  * then we'll have a new release!
Really looking forward to this one :) I actually kind of forced myself to do this by no longer improving on anything ahk1. So if I wanna dogfeed the thing to me it HAS to be with the ahk2 stuff!

  
## a2 main loop layout:
![](https://i.imgur.com/zyv1mUb.gif)

## blog posts:
* [a2 – works for me](https://goodsoul.de/blog/a2works4me/)
* [a2 – the first humble steps]([http://goodsoul.de/?p=780](https://goodsoul.de/wp/?p=780))

## <a name="dev-team"></a>Authors/Contributors
* [Eric Werner (ewerybody)](https://github.com/ewerybody)
* [Oliver Lipkau](https://github.com/lipkau)

## versions in latest build package:
* AutoHotkey: 1.1.36.02
* Python: 3.11.3150.1013
* PySide: 6.4.2
