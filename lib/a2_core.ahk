#include Autohotkey\lib\Class_SQliteDB.ahk
/**
 * a2 global object definition
*/
class A2Core_Class
{
    /**
     * Title of the a2 instance
     *
     * @type string
    */
    static title := ""

    /**
     * Constructor
     *     Creates an object for the DB of the a2 instance
    */
    __New(data_path)
    {
        this.title := "a2"

        if (A_ScriptName = "a2.exe")
            root_dir := A_ScriptDir "\"
        else
            root_dir := path_dirname(A_ScriptDir) "\"

        this.paths := {a2: root_dir
            ,lib: root_dir "lib\"
            ,ahklib: root_dir "lib\Autohotkey\lib\"
            ,ui: root_dir "ui\"
            ,resources: root_dir "ui\res\"
            ,data: data_path
            ,modules: data_path "modules\"
            ,module_data: data_path "module_data\"
            ,temp: data_path "temp\"
        ,includes: data_path "includes\includes.ahk"}

        this.cfg := {}

        this._check_sqlite()
        this.db := _Ca2DB(data_path)
    }

    _check_sqlite() {
        ; make sure the SQLlite-dll can be found
        ini_path := path_join(this.paths.lib, "SQLiteDB.ini")
        if (FileExist(ini_path))
            Return

        sqldll := "SQLite3.dll"
        dll_path := path_join(this.paths.ui, sqldll)

        if (!FileExist(dll_path)) {
            msg := 'The "' sqldll '" must exist here:`n' dll_path '!`n`nWhere is it?'
            msgbox_error(msg, sqldll ' missing?!')
            Return
        }

        ini_code := "[Main]`nDllPath=" dll_path
        FileAppend(ini_code, ini_path)
    }
}


/**
 * API for modules to inteact with the DB
*/
class _Ca2DB
{
    /**
     * Path to the DB file of the a2 instance
     *
     * @type string
    */
    static path := ""

    /**
     * Constructor
     *     Opens connection to the DB
    */
    __New(data_path)
    {
        this.path := data_path "a2.db"
        ; Ensure the DB file does exist
        if (!FileExist(this.path))
        {
            db_file := FileOpen(this.path, "w")
            db_file.Write("")
            db_file.Close()
        }

        this.dbObject := SQLiteDB()
    }

    /**
     * Destructor
     *     Closes the connection to the DB
    */
    __Delete()
    {
        this.dbObject.CloseDB()
    }

    /**
     * Get the value of key from the DB
     * Entry in DB is a key/value pair
     *
     * @param  string   modulePack  Name of the Module Pack that called the method
     * @param  string   moduleName  Name of the Module that called the method
     * @param  string   key         Name of the key in the Table
     * @return string
    */
    get(modulePack, moduleName, key)
    {
        moduleTable := this.__moduleTable(modulePack, moduleName)
        this.__validateTable(moduleTable) ; will throw an error if invalid
        return this.__get(moduleTable, key)
    }

     /**
     * From a A_LineFile path build the module key and fetch the wanted value.
     * Entry in DB is a key/value pair.
     *
     * @param  string   line_file  Path to a file in a module directory.
     * @param  string   key        Name of the key in the Table.
     * @return string
    */
    find(line_file, key) {
        moduleTable := this.__moduleTableFromFile(line_file)
        this.__validateTable(moduleTable)
        return this.__get(moduleTable, key)
    }

    /**
     * Set a new value to a key from the DB
     * Entry in DB is a key/value pair
     *
     * @param  string   modulePack  Name of the Module Pack that called the method
     * @param  string   moduleName  Name of the Module that called the method
     * @param  string   key         Name of the key in the Table
     * @param  string   value       Value to be set in the Table
    */
    set(modulePack, moduleName, key, value)
    {
        moduleTable := this.__moduleTable(modulePack, moduleName)

        this.__validateTable(moduleTable) ; will throw an error if invalid

        if (this.get(modulePack, moduleName, key))
            this.__update(moduleTable, key, value)
        else
            this.__insert(moduleTable, key, value)
    }

    /**
     * From a A_LineFile path build the module key and set the according value.
     * Entry in DB is a key/value pair.
     *
     * @param  string   line_file  Path to a file in a module directory.
     * @param  string   key        Name of the key in table.
     * @param  string   value      Value to be set in table.
     * @return string
    */
    find_set(line_file, key, value) {
        moduleTable := this.__moduleTableFromFile(line_file)
        this.__validateTable(moduleTable)
        if (this.__get(moduleTable, key))
            this.__update(moduleTable, key, value)
        else
            this.__insert(moduleTable, key, value)
    }

    /**
     * Delete a row from the table in the DB
     * based on the key name
     *
     * @param   string  modulePack  Name of the Module Pack that called the method
     * @param   string  moduleName  Name of the Module that called the method
     * @param   string  key         Name of the key in the Table
    */
    delete(modulePack, moduleName, key)
    {
        moduleTable := this.__moduleTable(modulePack, moduleName)

        this.__validateTable(moduleTable) ; will throw an error if invalid

        this.__remove(moduleTable, key)
    }

    /**
     * Increment the value of a key by a specific amount
     * - Value MUST be numeric/integer
     * - Amount can be negative
     * - If the key was non-existing, it will be creted with value = amount
     *
     * @param   string  modulePack  Name of the Module Pack that called the method
     * @param   string  moduleName  Name of the Module that called the method
     * @param   string  key         Name of the key in the Table
     * @param   integer step        Amount to increase the value by
     * @return  integer             Value after adding the amount
    */
    increment(modulePack, moduleName, key, step := 1)
    {
        ; if step is not number
        ;     return -1

        moduleTable := this.__moduleTable(modulePack, moduleName)

        this.__validateTable(moduleTable) ; will throw an error if invalid

        currentValue := this.__get(moduleTable, key)

        ; if currentValue is not number
        ;     return -2

        value := ((currentValue) ? currentValue : 0) + step

        this.set(modulePack, moduleName, key, value)

        return value
    }

    /**
     * Private Method
     *     Get value from Table row
     *     Only supports 1 entry
     *
     * @param   string  moduleTable     Name of the Table
     * @param   string  key             Value in column "key"
     * @return  string
    */
    __get(moduleTable, key)
    {
        this.__openConnection()

        row := ""
        result := ""
        recordSet := ""

        sql := "SELECT value FROM '" moduleTable "' WHERE key = '" key "'"
        this.dbObject.Query(sql, recordSet) ; no error handle

        if (recordSet.HasRows)
        {
            Loop(recordSet.HasRows)
            {
                recordSet.next(row)
                result := row[1]
            }
        }
        recordSet.Free()

        ; Close connection to DB to unlock the file
        this.__closeConnection()

        return (result) ? result : false
    }

    /**
     * Private Method
     *     Set value to Table row
     *     Only supports 1 entry
     *
     * @param   string  moduleTable     Name of the Table
     * @param   string  key             Value for column "key"
     * @param   string  value           Value for column "value"
    */
    __insert(moduleTable, key, value)
    {
        this.__openConnection()

        sql := "INSERT INTO '" moduleTable "' ('key', 'value') VALUES ('" key "', '" value "')"
        if (!this.dbObject.Exec(sql))
            throw Error("[" this.dbObject.ErrorCode "] " this.dbObject.ErrorMsg, -1)

        ; Close connection to DB to unlock the file
        this.__closeConnection()
    }

    /**
     * Private Method
     *     Update value in Table row
     *     Only supports 1 entry
     *
     * @param   string  moduleTable     Name of the Table
     * @param   string  key             Value in column "key"
     * @param   string  value           Value for column "value"
    */
    __update(moduleTable, key, value)
    {
        this.__openConnection()

        sql := "UPDATE '" moduleTable "' set value = '" value "' WHERE key = '" key "'"
        if (!this.dbObject.Exec(sql))
            throw Error("[" this.dbObject.ErrorCode "] " this.dbObject.ErrorMsg, -1)

        ; Close connection to DB to unlock the file
        this.__closeConnection()
    }

    /**
     * Private Method
     *     Delete row from Table
     *     Renamed, as __delete() is the destructor
     *
     * @param   string  moduleTable     Name of the Table
     * @param   string  key             Value in column "key"
    */
    __remove(moduleTable, key)
    {
        this.__openConnection()

        sql := "DELETE FROM '" moduleTable "' WHERE key = '" key "'"
        if (!this.dbObject.Exec(sql))
            throw Error("[" this.dbObject.ErrorCode "] " this.dbObject.ErrorMsg, -1)

        ; Close connection to DB to unlock the file
        this.__closeConnection()
    }

    /**
     * Private Method
     *     Generate the Table name based on the module
     *     that called the method
     *
     * @param   string  modulePack  Name of the Module Pack that called the method
     * @param   string  moduleName  Name of the Module that called the method
     * @return  string
    */
    __moduleTable(modulePack, moduleName)
    {
        return modulePack "|" moduleName
    }

    __moduleTableFromFile(line_file) {
        parts := StrSplit(line_file, "\")
        num_parts := parts.Length
        if num_parts < 3
            throw Error('Unusable path input! Cannot find db entry from "' line_file '"!', -1)
        return this.__moduleTable(parts[num_parts - 2], parts[num_parts - 1])
    }

    /**
     * Private Method
     *     Ensures the Table exists in the DB
     *     Throws a terminating Exception if it doesn't
     *
     * @param   string  moduleTable     Name of the Table
    */
    __validateTable(moduleTable)
    {
        this.__openConnection()

        sql := "SELECT COUNT(*) FROM '" moduleTable "'"
        table := ""
        if (!this.dbObject.getTable(sql, table))
            throw Error("[" this.dbObject.ErrorCode "] " this.dbObject.ErrorMsg, -1)

        ; Close connection to DB to unlock the file
        this.__closeConnection()
    }

    /**
     * Private Method
     *     Handles the establishing of the connection to the DB
    */
    __openConnection()
    {
        if (this.dbObject._Handle) ; connection is already open
            Return

        Loop(5)
        {
            if (this.dbObject.OpenDB(this.path))
                break
            else
                sleep 50
        }

        if (!this.dbObject._Handle)
            throw Error("[" this.dbObject.ErrorCode "] " this.dbObject.ErrorMsg, -1)
    }

    /**
     * Private Method
     *     Handles the terminate of the connection to the DB
    */
    __closeConnection()
    {
        if (!this.dbObject.CloseDB())
            throw Error("[" this.dbObject.ErrorCode "] " this.dbObject.ErrorMsg, -1)
    }

}