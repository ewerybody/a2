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

#include lib\ahklib\CManifest.ahk

class ModuleModel
{
    /**
     * Allocate static properties for
     *     the name of the module
     *     the name of the module package
     *     the url to the documentation of this module
     */
    /**
     * A property witht he name of the Module Pack
     *     is populated in Construtor
     *
     * @type string
     */
    static moduleSource

    /**
     * A property witht the Name of the Module
     *     is populated in Construtor
     *
     * @type string
     */
    static moduleName

    /**
     * A property with the Link to the Module's HomePage
     *     is populated in Construtor
     *
     * @type string
     */
    static moduleURL

    /**
     * A property with the Module's base Directory
     *     is populated in Construtor
     *
     * @type string
     */
    static modulePath

    /**
     * A property with the Module's key for the DB
     *     is populated in Construtor
     *
     * @type string
     */
    static moduleKey

    /**
     * A property with the Module's icon
     *     is populated in Construtor
     *
     * @type hBitmap
     */
    static moduleIcon

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
        this.manifest     := new CManifest(LineFile)
        this.moduleSource := this.manifest.metaData.source
        this.moduleName   := this.manifest.metaData.name
        this.moduleURL    := this.manifest.metaData.url
        this.modulePath   := a2.path "\" a2.modules "\" this.moduleSource "\" this.moduleName
        this.moduleKey    := this.moduleSource "|" this.moduleName
        for i,v in [".svg", ".png", ".ico"] {
            iconFile := this.modulePath "\a2icon" v
            if (FileExist(iconFile)) {
                this.moduleIcon := iconFile  ; TODO extract icon
                break
            }
        }
        return this
    }
}
