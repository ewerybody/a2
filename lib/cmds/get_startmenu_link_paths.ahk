; Return common target paths of links a2 Start Menu Dir
#include <path>
#include <string>

link_names := ["Start a2 Runtime", "Open a2 UI", "Uninstall a2", "Explore a2 Directory"],
start_menu_dir := A_Programs "\a2\"
target_paths := []

for _, link_name in link_names {
    link_path := start_menu_dir . link_name . ".lnk"
    FileGetShortcut link_path, &target_path
    If path_is_file(target_path)
        target_path := path_dirname(target_path)

    If !string_is_in_array(target_path, target_paths)
        target_paths.Push(target_path)
}

if (target_paths.Length == 1)
    result := target_paths[1]
Else {
    result := ""
    Loop(target_paths.Length)
        result .= target_paths[A_Index] "`n"
}

FileAppend(result, "*")
