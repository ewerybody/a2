# Translation with Weblate

Our translations are in simple `key/value` `.json` files.\
The layout supports 2 patterns:
* `/i18n/{language_code}/{section_name}.json` - **sections in dedicated files** under `/i18n/{language_code}/`
  * e.g. [`/i18n/en/general.json`](https://github.com/ewerybody/a2/blob/ahk2/i18n/de/general.json), [`/i18n/de/general.json`](https://github.com/ewerybody/a2/blob/ahk2/i18n/en/general.json)
  * For the main a2 runtime and a2 ui or very big modules with different components
  * For example translate here: https://hosted.weblate.org/projects/a2/a2-general/
* `/i18n/{language_code}.json` - **flat `key/value` files per language** under `/i18n/`
  * e.g.: [`/i18n/en.json`](https://github.com/ewerybody/a2/blob/ahk2/lib/Autohotkey/lib/test/i18n/de.json), [`/i18n/de.json`](https://github.com/ewerybody/a2/blob/ahk2/lib/Autohotkey/lib/test/i18n/de.json), [`/i18n/fr.json`](https://github.com/ewerybody/a2/blob/ahk2/lib/Autohotkey/lib/test/i18n/fr.json) (test)
  * For smaller modules where we would just have 1 section anyway
  * For example translate here: https://hosted.weblate.org/projects/a2/a2-modules-gtranslate/

## What are components?

A component is either **one** section like `general` in the a2 main translation files.
Or **one small style** module translation withou sections.

Within the one Weblate project we'll try to host all the main files for the Autohotkey runtime and any UI weather it's Qt or Autohotkey
and all of the main modules like a2.modules (and a2.modlab?)

## How to create a new component:

* Got to our Weblate project: https://hosted.weblate.org/projects/a2
* log in with admin account
* hit the **➕** in the top right and "**Add new translation component**"\
  (or go to: https://hosted.weblate.org/create/component/?project=8564)
* **Component name**:\
  please keep the existing patterns!
  * `a2 {section_name}` for a section under `{a2_project_root}/i18n/{lang_name}/` and the filename being `{section_name}.json`
    * for example [a2 general](https://hosted.weblate.org/settings/a2/a2-general/) for the files `/i18n/en/general.json` and `/i18n/de/general.json` ...
  * `{package.name} - {module_name}` for a small module under `{a2-module-root}/{module_name}/i18n/` and the filenames being `en.json`, `de.json` ...
    * for example [a2.modules - getWinfo](https://hosted.weblate.org/settings/a2/a2-modules-getwinfo/) for the files `/getWinfo/i18n/en.json` and `/getWinfo/i18n/de.json` ...
* **URL slug** - leave it like it was generated
* **Use as glossary** off (for now)
* **Project** a2
* **Source language** English
* **Version control system** Git
* **Source code repository**: the .git address. That's:
  * for a2: https://github.com/ewerybody/a2.git
  * for a2.modules https://github.com/ewerybody/a2.modules.git
* **Repository branch** `ahk2` (for now)
* 







