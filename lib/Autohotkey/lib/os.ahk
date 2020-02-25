/**
 * Helper Function
 *     Formats a file size in bytes to a human-readable size string
 *
 * @sample
 *     x := FormatFileSize(31236)
 *
 * @param   int     Bytes      Number of bytes to be formated
 * @param   int     Decimals   Number of decimals to be shown
 * @param   int     Prefixes   List of which the best matching prefix will be used
 * @return  string
 */
FormatFileSize(Bytes, Decimals = 1, Prefixes = "B,KB,MB,GB,TB,PB,EB,ZB,YB")
{
    StringSplit, Prefix, Prefixes, `,
    Loop, Parse, Prefixes, `,
        if (Bytes < e := 1024 ** A_Index)
            return % Round(Bytes / (e / 1024), decimals) Prefix%A_Index%
}
