#include lib\ahklib\Class_SQLiteDB.ahk

/**
 * a2 global object definition
 */
class Ca2
{
    static title := "a2"
    static path := A_ScriptDir "\.."
    static modules := a2_modules

    __New()
    {
        this.db := new this.Ca2DB()
    }

    /**
     * API for modules to inteact with the DB
     */
    class Ca2DB
    {
        static path := A_ScriptDir "\..\settings\a2.db"

        __New()
        {
            if (!FileExist(this.path))
                throw Exception("Database could not be found", -1)
            this.dbObject := new SQLiteDB
            If (!this.dbObject.OpenDB(this.path))
                throw Exception(this.dbObject.ErrorMsg, this.dbObject.ErrorCode)
        }

        __Delete()
        {
            this.dbObject.CloseDB()
        }

        get(modulePack, moduleName, key)
        {
            moduleTable := this.__moduleTable(modulePack, moduleName)

            this.__validateTable(moduleTable)

            return this.__get(moduleTable, key)
        }

        set(modulePack, moduleName, key, value)
        {
            moduleTable := this.__moduleTable(modulePack, moduleName)

            this.__validateTable(moduleTable)

            if (this.get(modulePack, moduleName, key))
                return this.__update(moduleTable, key, value)
            else
                return this.__insert(moduleTable, key, value)
        }

        delete(modulePack, moduleName, key)
        {
            moduleTable := this.__moduleTable(modulePack, moduleName)

            this.__validateTable(moduleTable)

            return this.__remove(moduleTable, key)
        }

        increment(modulePack, moduleName, key, step = 1)
        {
            if (!IsNumeric(step))
                return -1

            moduleTable := this.__moduleTable(modulePack, moduleName)

            this.__validateTable(moduleTable)

            currentValue := this.__get(moduleTable, key)

            value := ((currentValue) ? currentValue : 0) + step

            return this.set(modulePack, moduleName, key, value)
        }

        __get(moduleTable, key)
        {
            sql := "SELECT value FROM '" moduleTable "' WHERE key = '" key "'"
            recordset := ""
            if (!this.dbObject.Query(sql, recordset))
            row := ""
            result := ""
            if (recordset.HasRows)
                Loop % recordset.HasRows
                {
                    recordset.next(row)
                    result := row[1]
                }
            return (result) ? result : false
        }

        __insert(moduleTable, key, value)
        {
            sql := "INSERT INTO '" moduleTable "' ('key', 'value') VALUES ('" key "', '" value "')"
            if (!this.dbObject.Exec(sql))
                throw Exception(this.dbObject.ErrorMsg, this.dbObject.ErrorCode)
            return true
        }

        __update(moduleTable, key, value)
        {
            sql := "UPDATE '" moduleTable "' set value = '" value "' WHERE key = '" key "'"
            if (!this.dbObject.Exec(sql))
                throw Exception(this.dbObject.ErrorMsg, this.dbObject.ErrorCode)
            return true
        }

        __remove(moduleTable, key)
        {
            sql := "DELETE FROM '" moduleTable "' WHERE key = '" key "'"
            if (!this.dbObject.Exec(sql))
                throw Exception(this.dbObject.ErrorMsg, this.dbObject.ErrorCode)
            return true
        }

        __moduleTable(modulePack, moduleName)
        {
            return modulePack "|" moduleName
        }

        __validateTable(moduleTable)
        {
            sql := "SELECT COUNT(*) FROM '" moduleTable "'"
            recordset := ""
            if (!this.dbObject.getTable(sql, recordset))
                throw Exception(this.dbObject.ErrorMsg, this.dbObject.ErrorCode)
        }
    }
}
