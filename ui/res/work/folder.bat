set inkscape="C:\Program Files\Inkscape\bin\inkscape.exe"
set /p magick= < magick_path.txt

set name=folder2
%inkscape% --export-type=png --export-dpi=200 --export-background-opacity=0 ..\%name%.svg
move ..\%name%.png %name%.png
"%magick%" %name%.png -resize 48x48 %name%48.png
"%magick%" %name%.png -resize 16x16 %name%16.png
"%magick%" %name%16.png %name%48.png ..\%name%.ico