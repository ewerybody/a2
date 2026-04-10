#include <Class_SQliteDB>
#include <a2dlg>
#include <path>

/**
 * a2 global object definition
 */
Class A2Core_Class {
    /**
     * Title of the a2 instance
     *
     * @type {(String)}
     */
    static title := ""

    /**
     * Constructor
     *     Creates an object for the DB of the a2 instance
     */
    __New(data_path) {
        this.title := "a2"

        if (A_ScriptName = "a2.exe")
            root_dir := A_ScriptDir "\"
        else
            root_dir := path_dirname(A_ScriptDir) "\"

        data_path := string_suffix(data_path, "\")

        this.paths := {a2: root_dir
            ,lib: root_dir "lib\"
            ,ahklib: root_dir "lib\Autohotkey\lib\"
            ,ui: root_dir "ui\"
            ,resources: root_dir "theme\"
            ,data: data_path
            ,modules: data_path "modules\"
            ,module_data: data_path "module_data\"
            ,temp: data_path "temp\"
            ,includes: data_path "includes\includes.ahk"
        }

        this.cfg := {}

        this._check_sqlite()
        this.db := _Ca2DB(data_path)
    }

    _check_sqlite() {
        sql_dll := "SQLite3.dll"
        if (FileExist(path_join(this.paths.lib, sql_dll)))
            Return

        ; make sure the SQLlite-dll can be found
        ini_path := path_join(this.paths.lib, "SQLiteDB.ini")
        if (FileExist(ini_path))
            Return

        dll_path := path_join(this.paths.ui, sql_dll)

        if (!FileExist(dll_path)) {
            msg := 'The "' sql_dll '" must exist here:`n' dll_path '!`n`nWhere is it?'
            a2dlg_error(msg, sql_dll ' missing?!')
            Return
        }

        ini_code := "[Main]`nDllPath=" dll_path
        FileAppend(ini_code, ini_path)
    }
}


/**
 * API for modules to interact with the DB
 */
Class _Ca2DB {
    /**
     * Path to the DB file of the a2 instance
     *
     * @type {(String)}
     */
    static path := ""

    /**
     * Constructor
     *     Open connection to the DB.
     * @param {(String)} data_path
     * Sting path to the database file.
     */
    __New(data_path) {
        this.path := data_path "a2.db"
        ; Ensure DB file exists.
        if (!FileExist(this.path)) {
            db_file := FileOpen(this.path, "w")
            db_file.Write("")
            db_file.Close()
        }

        this.db_object := SQLiteDB()
    }

    /**
     * Destructor
     *     Close connection to DB.
     */
    __Delete() {
        this.db_object.CloseDB()
    }

    /**
     * From a A_LineFile path build the module key and fetch the wanted value.
     * Entry in DB is a key/value pair.
     *
     * @param {(String)} line_file
     * Path to a file in a module directory.
     * @param {(String)} key
     * Name of the key in the table.
     * @returns {(String)}
     */
    find(line_file, key) {
        table_name := this.__module_tableFromFile(line_file)
        this.__validate_table(table_name)
        return this.__get(table_name, key)
    }

    /**
     * From a A_LineFile path build the module key and set the according value.
     * Entry in DB is a key/value pair.
     *
     * @param {(String)} line_file
     * Path to a file in a module directory.
     * @param {(String)} key
     * Name of the key in table.
     * @param {(String)} value
     * Value to be set in table.
     * @return {(String)}
     */
    find_set(line_file, key, value) {
        table_name := this.__module_tableFromFile(line_file)
        this.__validate_table(table_name)
        if (this.__get(table_name, key))
            this.__update(table_name, key, value)
        else
            this.__insert(table_name, key, value)
    }

    /**
     * Get single value of key from the DB.
     * Entry in DB is a key/value pair.
     *
     * @param {(String)} key
     * Name of the key in the table.
     * @param {(String)} module_pack
     * Name of the Module Pack that called the method.
     * @param {(String)} module_name
     * Name of the Module that called the method.
     * @return {(String)}
     */
    get(key, module_pack, module_name := "") {
        table_name := this.__module_table(module_pack, module_name)
        this.__validate_table(table_name)
        return this.__get(table_name, key)
    }

    /**
     * Set a single value to a key from the DB.
     * Entry in DB is a key/value pair.
     *
     * @param {(String)} key
     * Name of the key in the table.
     * @param {(String)} value
     * Value to be set in the table.
     * @param {(String)} module_pack
     * Name of the Module Pack that called the method.
     * @param {(String)} [module_name]
     * Name of the Module that called the method.
     */
    set(key, value, module_pack, module_name := "") {
        table_name := this.__module_table(module_pack, module_name)
        this.__validate_table(table_name) ; will throw an error if invalid
        if (this.get(table_name, key))
            this.__update(table_name, key, value)
        else
            this.__insert(table_name, key, value)
    }

    /**
     * Delete a row from the table in the DB
     * based on the key name
     *
     * @param {(String)} key
     * Name of the key in the table.
     * @param {(String)} module_pack
     * Name of the Module Pack that called the method.
     * @param {(String)} [module_name]
     * Name of the Module that called the method.
     */
    delete(key, module_pack, module_name := "") {
        table_name := this.__module_table(module_pack, module_name)
        this.__validate_table(table_name) ; will throw an error if invalid
        this.__remove(table_name, key)
    }

    /**
     * Increment the value of a key by a specific amount
     * - Value MUST be numeric/integer
     * - Amount can be negative
     * - If the key was non-existing, it will be created with value = amount
     *
     * @param {(String)} module_pack
     * Name of the Module Pack that called the method.
     * @param {(String)} [module_name]
     * Name of the Module that called the method.
     * @param {(String)} key
     * Name of the key in the table.
     * @param {(Integer)} step
     * Amount to increase the value by.
     * @return {(Integer)}              Value after adding the amount
     */
    increment(key, module_pack, module_name := "", step := 1) {
        ; if step is not number
        ;     return -1

        table_name := this.__module_table(module_pack, module_name)
        this.__validate_table(table_name) ; will throw an error if invalid
        currentValue := this.__get(table_name, key)

        ; if currentValue is not number
        ;     return -2

        value := ((currentValue) ? currentValue : 0) + step
        this.set(module_pack, module_name, key, value)
        return value
    }

    /**
     * Get the list of tables available in the database.
     * @return {(Array)}
     * List of string table names.
     */
    tables() {
        this.__open_connection()
        sql := "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"

        If !this.db_object.GetTable(sql, &TB)  {
            msgbox_error("Could not perform a2.db.tables:`n" this.db_object.ErrorMsg, "SQLite Error")
            Return []
        }

        tables := []
        Loop TB.RowCount {
            If TB.GetRow(A_Index, &Row)
                tables.Push(Row[1])
        }
        this.__close_connection()
        return tables
    }

    /**
     * Get single value from table row.
     *
     * @param {(String)} table_name
     * Name of the table.
     * @param {(String)} key
     * Value in column "key".
     * @return {(String)}
     */
    __get(table_name, key) {
        this.__open_connection()

        result := ""
        Table := ""
        sql := "SELECT value FROM '" table_name "' WHERE key = '" key "'"
        If !this.db_object.GetTable(SQL, &Table)
            msgbox_error("Msg:`t" . this.db_object.ErrorMsg . "`nCode:`t" . this.db_object.ErrorCode, "SQLite Error")
        If (Table.HasRows)
            result := Table.Rows[1][1]

        this.__close_connection()
        Return (result) ? result : false
    }

    /**
     * Set single value to table row.
     *
     * @param {(String)} table_name
     * Name of the table.
     * @param {(String)} key
     * Value for column "key".
     * @param {(String)} value
     * Value for column "value".
     */
    __insert(table_name, key, value) {
        this.__open_connection()

        sql := "INSERT INTO '" table_name "' ('key', 'value') VALUES ('" key "', '" value "')"
        if (!this.db_object.Exec(sql))
            throw Error("[" this.db_object.ErrorCode "] " this.db_object.ErrorMsg, -1)

        this.__close_connection()
    }

    /**
     * Update single value in table row.
     *
     * @param {(String)} table_name
     * Name of the table.
     * @param {(String)} key
     * Value in column "key".
     * @param {(String)} value
     * Value for column "value".
     */
    __update(table_name, key, value) {
        this.__open_connection()

        sql := "UPDATE '" table_name "' set value = '" value "' WHERE key = '" key "'"
        if (!this.db_object.Exec(sql))
            throw Error("[" this.db_object.ErrorCode "] " this.db_object.ErrorMsg, -1)

        this.__close_connection()
    }

    /**
     * Delete single row from table.
     * Renamed, as __delete() is the destructor.
     *
     * @param {(String)} table_name
     * Name of the table.
     * @param {(String)} key
     * Value in column "key".
     */
    __remove(table_name, key) {
        this.__open_connection()

        sql := "DELETE FROM '" table_name "' WHERE key = '" key "'"
        if (!this.db_object.Exec(sql))
            throw Error("[" this.db_object.ErrorCode "] " this.db_object.ErrorMsg, -1)

        this.__close_connection()
    }

    /**
     * Generate the table name based on the module package and module name.
     *
     * @param {(String)} module_pack
     * Name of the Module Package.
     * @param {(String)} module_name
     * Name of the Module.
     * @return {(String)}
     */
    __module_table(module_pack, module_name := "") {
        if module_name == ""
            return module_pack
        return module_pack "|" module_name
    }

    /**
     * Build table-name from incoming line_file path.
     * @param {(String)} line_file
     * String path of calling script file.
     * @returns {(String)}
     */
    __module_tableFromFile(line_file) {
        parts := StrSplit(line_file, "\")
        num_parts := parts.Length
        if num_parts < 3
            throw Error('Unusable path input! Cannot find db entry from "' line_file '"!', -1)
        return this.__module_table(parts[num_parts - 2], parts[num_parts - 1])
    }

    /**
     * Ensure the table exists in the DB.
     * Throw a terminating Exception if it doesn't.
     *
     * @param {(String)} table_name
     * Name of the table.
     */
    __validate_table(table_name) {
        this.__open_connection()

        sql := "SELECT COUNT(*) FROM '" table_name "'"
        table := ""
        If (!this.db_object.getTable(sql, &table))
            Throw Error("[" this.db_object.ErrorCode "] " this.db_object.ErrorMsg, -1)

        this.__close_connection()
    }

    /**
     * Handle establishing connection to DB.
     */
    __open_connection() {
        if (this.db_object._Handle)
            ; connection is already open
            Return

        Loop(5) {
            if (this.db_object.OpenDB(this.path))
                break
            else
                sleep 50
        }

        if (!this.db_object._Handle)
            throw Error("[" this.db_object.ErrorCode "] " this.db_object.ErrorMsg, -1)
    }

    /**
     * Handle connection termination to DB.
     */
    __close_connection() {
        if (!this.db_object.CloseDB())
            throw Error("[" this.db_object.ErrorCode "] " this.db_object.ErrorMsg, -1)
    }
}
