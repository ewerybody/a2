#include lib\ahklib\Class_SQLiteDB.ahk

/**
 * a2 global object definition
 */
class Ca2
{
    /**
     * Title of the a2 instance
     *
     * @type string
     */
    static title := "a2"

    /**
     * Root path of the a2 instance
     *
     * @type string
     */
    static path := A_ScriptDir "\.."

    /**
     * Path to the module folder of the a2 instance
     *
     * @type string
     */
    static modules := a2_modules

    /**
     * Constructor
     *     Creates an object for the DB of the a2 instance
     */
    __New()
    {
        this.db := new this.Ca2DB()
    }

    /**
     * API for modules to inteact with the DB
     */
    class Ca2DB
    {
        /**
         * Path to the DB file of the a2 instance
         *
         * @type string
         */
        static path := A_ScriptDir "\..\settings\a2.db"

        /**
         * Constructor
         *     Opens connection to the DB
         */
        __New()
        {
            ; Ensure the DB file does exist
            if (!FileExist(this.path))
                throw Exception("Database could not be found", -1)

            this.dbObject := new SQLiteDB
            If (!this.dbObject.OpenDB(this.path))
                throw Exception(this.dbObject.ErrorMsg, this.dbObject.ErrorCode)
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
        increment(modulePack, moduleName, key, step = 1)
        {
            if (!IsNumeric(step))
                return -1

            moduleTable := this.__moduleTable(modulePack, moduleName)

            this.__validateTable(moduleTable) ; will throw an error if invalid

            if (!IsNumeric(currentValue))
                return -2

            currentValue := this.__get(moduleTable, key)

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
            sql := "INSERT INTO '" moduleTable "' ('key', 'value') VALUES ('" key "', '" value "')"
            if (!this.dbObject.Exec(sql))
                throw Exception(this.dbObject.ErrorMsg, this.dbObject.ErrorCode)
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
            sql := "UPDATE '" moduleTable "' set value = '" value "' WHERE key = '" key "'"
            if (!this.dbObject.Exec(sql))
                throw Exception(this.dbObject.ErrorMsg, this.dbObject.ErrorCode)
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
            sql := "DELETE FROM '" moduleTable "' WHERE key = '" key "'"
            if (!this.dbObject.Exec(sql))
                throw Exception(this.dbObject.ErrorMsg, this.dbObject.ErrorCode)
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

        /**
         * Private Method
         *     Ensures the Table exists in the DB
         *     Throws a terminating Exception if it doesn't
         *
         * @param   string  moduleTable     Name of the Table
         */
        __validateTable(moduleTable)
        {
            sql := "SELECT COUNT(*) FROM '" moduleTable "'"
            table := ""
            if (!this.dbObject.getTable(sql, table))
                throw Exception(this.dbObject.ErrorMsg, this.dbObject.ErrorCode)
        }
    }
}
