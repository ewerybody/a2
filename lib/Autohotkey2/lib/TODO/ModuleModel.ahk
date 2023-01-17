/**
 * Module Model
 *     This Class can be used as a Base for
 *     any module's class.
 *     It will add properties to every object
 *     of the Module's class with information
 *     about the Module itself. Such as:
 *         * Name of the Module (Name of the
 *             folder on the FileSystem)
 *         * Name of the Module Pack (Name of
 *             the folder on the FileSystem)
 *         * Manifest of the Module (a2module.json)
 */

#include <CManifest>
#include <RichObject>

class ModuleModel
{
    /**
     * Information about the module and its metadata
     *     is populated in Construtor
     *
     * @type RichObject
     * @property Source    Source of the Module
     * @property Name      Name of the Module
     * @property URL       URL of the Module
     * @property Path      Module's base Directory
     * @property DataPath  Module's path for "AppData"
     * @property DBKey     Module's key for the DB
     * @property Icon      Module's Icon
     */
    static module

    /*+
     * A property with the data from the Module's manifest
     * (content of a2module.json)
     *     is populated in Contructor
     *
     * @type CManifest
     */
    static manifest

    /**
     * Constructor
     *     Populate the module's information properties from the manifest
     *
     * When this class is extended by another class, the extendee must
     * call this (parent) constructor by `this.base.__New()`
     *
     * @sample
     *     class MyAwesomeModule extends ModuleModel
     *     {
     *         __New()
     *         {
     *             this.base.__New(A_LineFile)
     *         }
     *
     *         GetClassName()
     *         {
     *             return this.moduleName
     *         }
     *     }
     *     moduleName := new MyAwesomeModule()
     *     msgbox % moduleName.GetClassName()
     *
     * @sample
     *     MyAwesomeModule := new ModuleModel(A_LineFile)
     *     msgbox % MyAwesomeModule.moduleName
     *
     * @param   string  LineFile        Path to the file of the module (that extended this class)
     *
     */
    __New(LineFile)
    {
        global a2

        this.manifest           := new CManifest(LineFile)
        this.module             := new CRichObject()
        this.module["Source"]   := this.manifest.metaData.source
        this.module["Name"]     := this.manifest.metaData.name
        this.module["URL"]      := this.manifest.metaData.url
        this.module["Path"]     := a2.paths.modules "" this.module.Source "\" this.module.Name
        this.module["DataPath"] := a2.paths.module_data "" this.module.Source "\" this.module.Name
        this.module["DBKey"]    := this.module.Source "|" this.module.Name
        for i,v in [".svg", ".png", ".ico"] {
            iconFile := this.modulePath "\a2icon" v
            if (FileExist(iconFile)) {
                this.module["Icon"] := iconFile  ; TODO extract icon
                break
            }
        }
        return this
    }
}
