; hier einfach weitere Menüeinträge erweitern
Menu, MyMenu, Add, li, htmlSurrounder
Menu, MyMenu, Add, b, htmlSurrounder
Menu, MyMenu, Add, i, htmlSurrounder
Menu, MyMenu, Add, a, htmlSurrounderLink
Menu, MyMenu, Add, img, htmlSurrounderImage
Menu, MyMenu, Add, testHTML, testHTML

Menu, MyMenu, Show
return

getSelection:
	tmp := ClipboardAll
	textClip := Clipboard
	Clipboard =
	Send, ^c
	ClipWait, 0.4
	sel := Clipboard
return

;Nimmt den Namen des Menüs und umschließt die Auswahl damit in <> und </>
htmlSurrounder:
	; selektion holen
	Gosub, getSelection
	; ins Clipboard packen
	Clipboard := "<" A_ThisMenuItem ">" sel "</" A_ThisMenuItem ">"
	; pasten
	Send, ^v
	; recover clipboard
	Clipboard := tmp
return

; erzeugt html-links im style <a href="http://safdsadf">text</a>
; wenn ein URL im Clipboard ist wird dieser sofort in den href geschrieben
; nix markiert: kommt der cursor dann in die >< ansonsten kommt das markierte dazwischen
; ist ein link markiert wird der auch ins href geschrieben und der cursor zw. >< positioniert
htmlSurrounderLink:
	Gosub, getSelection
	; if selection contains http* put that into the href, point cursor between >< then
	If SubStr(sel,1,4) = "http" ;
	{
		Clipboard = <a href="%sel%"></a>
		Send, ^v{Left 4}
	}
	; if clipboard already contains http* put that in the href and the selection into the ><
	Else If SubStr(textClip,1,4) = "http"
	{
		Clipboard = <a href="%textClip%">%sel%</a>
		Send, ^v
	}
	; otherwise just put the selected into the ><
	Else
	{
		Clipboard = <a href="">%sel%</a>
		StringLen, hLen, sel
		hLen += 6
		SendInput, ^v{Left %hLen%}
	}
	; recover clipboard
	Clipboard := tmp
return

htmlSurrounderImage:
	Gosub, getSelection

	Clipboard = <img src="%sel%" />
	Send, ^v
	Clipboard := tmp
return

testHTML:
	Gosub, getSelection
	fileName = %A_Temp%\testHTML.html
	FileDelete %fileName%
	FileAppend, %sel%, %fileName%
	Run, %fileName%,,Hide
Return