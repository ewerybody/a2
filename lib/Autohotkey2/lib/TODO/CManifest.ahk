#include <jxon>

/**
 * Global class to read the manifest (a2module.json)
 *
 * @param   string  Path of the ahk file which is calling the manifest
 *
 * @usage
 *     ; call the manifest
 *     myvar := new CManifest(A_LineFile)
 *     ; Name of the module which called the manifest
 *     myvar.metaData.name
 *     ; find a UI element by the field "name"
 *     myvar.manifest.findUIElementByKey("name", "MyModule_CheckBox1")
 */
class CManifest
{
    /**
     * Constructor
     *     Creates an object with the manifest's data
     *
     * @param   string  Path of the ahk file which is calling the manifest
     */
    __New(relativePath)
    {
        ; Read the file and convert to an object
        manifestText := FileRead(relativePath "\..\a2module.json")
        this.data := Jxon_Load(manifestText)

        ; find the module infodata
        this.metaData := this.findUIElementByKey("typ", "nfo")

        ; set the module name and source name
        RegExMatch(relativePath, ".*\\(.+?)\\(.+?)\\.+?$", filename)
        this.metaData.source := filename1
        this.metaData.name := filename2
    }

    /**
     * Find a module element by a key
     *
     * @sample
     *     ; find all the include elements
     *     manifest.findUIElementByKey("typ", "include")
     *
     * @sample
     *     ; find all elements with name "MyModule_CheckBox1"
     *     manifest.findUIElementByKey("name", "MyModule_CheckBox1")
     *
     * @param  string   key         Name of the key in the manifest
     * @param  string   value       Value of the key in the manifest
     * @return array
     * @return object
     */
    findUIElementByKey(key, value)
    {
        this._recursiveSearch(this.data, elements := [], key, value)
        return (elements.MaxIndex() == 1) ? elements[1] : elements
    }

    /**
     * Private Method
     *     Search recursively in an object structure
     *
     * @param   object  object      Object in which to search
     * @param   byref   @trace      variable in which the results will be stored. Should by an Array()
     * @param  string   key         Name of the key in the object
     * @param  string   value       Value of the key in the object
     */
    _recursiveSearch(object, ByRef @trace, key, value)
    {
        for i,v in object
            if (IsObject(v))
                this._recursiveSearch(v, @trace, key, value)
            else
                if ((i == key) AND (v == value))
                    @trace.Insert(object)
        return
    }
}
