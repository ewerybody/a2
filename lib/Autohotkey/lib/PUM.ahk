/*
PUM class represents popup menu manager
; By Deo from the archived forums:
; https://www.autohotkey.com/board/topic/73599-ahk-l-pum-owner-drawn-object-based-popup-menu/
*/
class PUM extends PUM_base
{
  __New( params = "" )
  {
      this.instance := 1
      this.Init()
      this.SetParams( params )
      this.gdipToken := pumAPI.Gdip_Startup()
  }

  __Get( aName )
  {
    if ( aName = "__Class" )
      return PUM.__Class
    return PUM._defaults[ aName ]
  }

  __Delete()
  {
    pumAPI.Gdip_Shutdown( this.gdipToken )
    this.Free()
    return
  }

  Free()
  {
    for i,menu in this._menus.Clone()
      menu.Destroy()
    for i,item in this._items.Clone()
      item.Destroy()
    for i,hBrush in this._brush
      pumAPI.DeleteObject( hBrush )
    for i,hFont in this._font
      pumAPI.DeleteObject( hFont )
  }

  Init()
  {
      this._menus := Object()
      this._menus.SetCapacity( 20 )
      this._items := Object()
      this._items.SetCapacity( 50 )
      this._itemIDbyUID := Object()
      this._itemIDbyUID.SetCapacity( 50 )
      this._itemsCount := 0
      this._brush := object()
      this._font := object()
      this.CreateFonts()
  }

  Destroy()
  {
    this.IsInstance()
    this.Free()
    this.Init()
  }

  IsInstance()
  {
    if this.instance
      return 1
    else
      this.Err( "Object is not an instance.`nUse 'new' to make one" )
  }

  CreateFonts()
  {
    if !this.pumfont
      pumAPI.GetSysFont( LOGFONT )
    else
      pumAPI.obj2LOGFONT( this.pumfont, LOGFONT )
    this._font[ "normal" ] := pumAPI.CreateFontIndirect( &LOGFONT )
    pumAPI.obj2LOGFONT( { weight : 700 }, LOGFONT )
    this._font[ "bold" ] := pumAPI.CreateFontIndirect( &LOGFONT )
  }

  GetFontNormal()
  {
    return this._font[ "normal" ]
  }

  GetFontBold()
  {
    return this._font[ "bold" ]
  }

  GetBrush( clr )
  {
    this.IsInstance()
    return ( this._brush.HasKey( clr ) ? this._brush[ clr ] : ( this._brush[ clr ] := pumAPI.CreateSolidBrush( clr ) ) )
  }

  SetParams( params )
  {
    this.IsInstance()
    if !IsObject( params )
      return 0
    for name, val in params
      this[ name ] := val
    if ( !pumAPI.isEmpty( params["seltcolor"] ) && this.seltcolor != -1 )
      this.seltcolor := pumAPI.RGBtoBGR( this.seltcolor )
    if ( !pumAPI.isEmpty( params["selbgcolor"] ) && this.selbgcolor != -1 )
      this.selbgcolor := pumAPI.RGBtoBGR( this.selbgcolor )
  }

  GetMenu( menuHandle )
  {
    this.IsInstance()
    if ObjHasKey( this._menus, menuHandle )
      return this._menus[ menuHandle ]
    else
      return 0
  }

  GetItemByID( id )
  {
    this.IsInstance()
    if ( id && ObjHasKey( this._items, id ) )
      return this._items[ id ]
    else
      return 0
  }

  GetItemByUID( uid )
  {
    this.IsInstance()
    return this.GetItemByID( this._itemIDbyUID[ uid ] )
  }

  CreateMenu( params = "" )
  {
    this.IsInstance()
    handle := pumAPI._CreatePopupMenu()
    newmenu := new PUM_Menu( handle, this )
    this._menus[ handle ] := newmenu
    newmenu.setParams( params )
    return newmenu
  }

  static _defaults := { "selMethod"   : "fill"  ;may be "frame","fill"
                          ,"selBGColor"  : pumAPI.GetSysColor( 29 )       ;background color of selected item, -1 means invert, default - COLOR_MENUHILIGHT
                          ,"selTColor"   : pumAPI.GetSysColor( 14 )       ;text color of selected item, -1 means invert, default - COLOR_HIGHLIGHTTEXT
                          ,"frameWidth"  : 1        ;width of select frame when selMethod = "frame"
                          ,"mnemonicCmd" : "run" ;may be "select","run"
                          ,"oninit"      : ""
                          ,"onuninit"    : ""
                          ,"onselect"    : ""
                          ,"onrbutton"   : ""
                          ,"onmbutton"   : ""
                          ,"onrun"       : ""
                          ,"onshow" : ""
                          ,"onclose" : ""
                          ,"pumfont" : "" }
}

/*
PUM_Item class represent single menu item
*/

class PUM_Item extends PUM_base
{
  __New( id, objMenu )
  {
    this.id := id
    this.menu := objMenu
    this.alive := 1
  }

  ; return default value for parameter if it wasn't set
  __Get( aName )
  {
    if ( aName = "__Class" )
      return PUM_Item.__Class
    return PUM_Item._defaults[ aName ]
  }

  __Delete()
  {
    return
  }

  GetPos()
  {
    return pumAPI._GetItemPosByID( this.menu.handle, this.id )
  }

  GetRECT()
  {
    if (( nPos := this.GetPos() ) != -1 )
      return pumAPI._GetItemRect( this.menu.handle, nPos )
    return 0
  }

  GetParent()
  {
    return this.menu
  }

  Detach()
  {
    this.detachSubMenu := 1
    this.Destroy()
  }

  ;deletes item from it's own menu and, if associated, submenu this item opens
  Destroy()
  {
    if !this.alive
      return 0
    this.Free()
    if pumAPI.IsInteger( this.uid )
      this.menu.objPUM._itemIDbyUID.Remove( this.uid, "" )
    else
      this.menu.objPUM._itemIDbyUID.Remove( this.uid )
    this.menu.objPUM._items.Remove( this.id, "" )
    if this.detachSubMenu
    {
      this.RemoveSubMenu()
      pumAPI._RemoveItem( this.menu.handle, this.id )
    }
    else
    {
      ;PUM menu cleanup should go first, because we will not be able retrieve items from atached menu if we destroy item through API first ( it destroys menu as well )
      this.DestroySubMenu()
      pumAPI._DeleteItem( this.menu.handle, this.id )
    }
    this.menu := ""
    this.submenu := ""
    this.alive := 0
  }

  Free()
  {
    ;~ DeleteObject( this.hfont )
    if this.icondestroy
      pumAPI.DestroyIcon( this.hIcon )
    this.hotCharCode := ""
  }

  DestroySubMenu()
  {
    if IsObject( this.assocMenu )
      this.assocMenu.Destroy()
  }

  RemoveSubMenu()
  {
    if !this.alive
      return 0
    if ( this.assocMenu.handle )
    {
      fMask := pumAPI.MIIM_SUBMENU
      cbsize := pumAPI.MENUITEMINFOsize
      VarSetCapacity( struct, cbsize, 0 )
      NumPut( cbsize, struct, 0, "UInt" )
      NumPut( fMask, struct, 4, "UInt" )
      NumPut( 0, struct, 16+A_PtrSize, "Ptr" )
      pumAPI._setMenuItemInfo( this.menu.handle, this.id, False, &struct )
      this.assocMenu.owner := ""
      this.assocMenu := ""
      this.submenu := ""
      pumAPI.free( struct )
    }
  }

  SetParams( params, newItemPos = "", fByPos = True )
  {
    if !this.alive
      return 0
    if isObject( params )
    {
      for name,val in params
        this[ name ] := val
      if ( this.uid != "" )
        this.menu.objPUM._itemIDbyUID[ this.uid ] := this.id
    }
    else if !pumAPI.IsEmpty( params )
      this.name := params
    else
      this.issep := 1
    if !pumAPI.isEmpty( params["tcolor"] )
      this.tcolor := pumAPI.RGBtoBGR( this.tcolor )
    if !pumAPI.isEmpty( params["bgcolor"] )
      this.bgcolor := pumAPI.RGBtoBGR( this.bgcolor )
    this._update( newItemPos, fByPos )
    return 1
  }

  Update()
  {
    this._update()
  }

  GetTColor()
  {
    return pumAPI.RGBtoBGR( this.tcolor )
  }

  GetBGColor()
  {
    return pumAPI.RGBtoBGR( this.bgcolor )
  }

  GetIconHandle()
  {
    return this.hicon
  }

  _update( newItemPos = "", fByPos = True )
  {
    this.Free()
    this.hfont := this.bold ? this.menu.objPUM.GetFontBold() : this.menu.objPUM.GetFontNormal()

    if ( mnemPos := InStr( this.name, "&" ) )
    {
      hotChar := SubStr( this.name, mnemPos+1, 1 )
      StringLower, hotChar, hotChar
      this.hotCharCode := asc( hotChar )
    }

    fMask := 0

    fMask |= pumAPI.MIIM_FTYPE
    fMask |= pumAPI.MIIM_ID
    fMask |= pumAPI.MIIM_STATE
    fMask |= pumAPI.MIIM_SUBMENU
    fMask |= pumAPI.MIIM_BITMAP

    fType := 0
    fType |= pumAPI.MFT_OWNERDRAW
    if this.issep
      fType |= pumAPI.MFT_SEPARATOR
    else
    {
      if this.break
        fType |= this.break = 2 ? pumAPI.MFT_MENUBARBREAK : pumAPI.MFT_MENUBREAK
    }

    fState := 0
    if this.disabled
      fState |= pumAPI.MFS_DISABLED
    wID := this.id

    ownedMenu := IsObject( this.submenu ) ? this.submenu    ;if menu object passed
               : pumAPI.IsInteger( this.submenu ) ? this.menu.objPUM._menus[ this.submenu ] ;if menu handle passed
               : 0
    ; check if submenu is valid menu
    if ( IsObject( ownedMenu ) && !ownedMenu.owner && pumAPI._isMenu( ownedMenu.handle ) )
    {
      ;checking if associated with item submenu changed
      if !( this.assocMenu.handle == ownedMenu.handle )
      {
        this.DestroySubMenu()
        ownedMenu.owner := this
        this.assocMenu := ownedMenu
        ownedMenu := ""
      }
    }

    itemNoIcons := this.noicons = -1 ? this.menu.noicons : this.noicons
    if !itemNoIcons
    {
      this.hicon := pumAPI.IsInteger( this.icon ) && this.iconUseHandle ? this.icon : pumAPI._loadIcon( this.icon, this.menu.iconssize )
      this.icondestroy := pumAPI.IsInteger( this.icon ) && this.iconUseHandle ? 0 : 1
    }

    fMask |= pumAPI.MIIM_DATA
    dwItemData := &this             ;storing address to 'this' item object

        ;typedef struct tagMENUITEMINFO {
    ;  UINT    cbSize;            0
    ;  UINT    fMask;             4
    ;  UINT    fType;             8
    ;  UINT    fState;            12
    ;  UINT    wID;               16
    ;  HMENU   hSubMenu;          16+ptr
    ;  HBITMAP hbmpChecked;       16+2ptr
    ;  HBITMAP hbmpUnchecked;     16+3ptr
    ;  ULONG_PTR dwItemData;      16+4ptr
    ;  LPTSTR  dwTypeData;        16+5ptr
    ;  UINT    cch;               16+6ptr
    ;  HBITMAP hbmpItem;          16+7ptr
    ;                             16+8ptr

    cbsize := pumAPI.MENUITEMINFOsize
    VarSetCapacity( struct, cbsize, 0 )
    NumPut( cbsize, struct, 0, "UInt" )
    NumPut( fMask, struct, 4, "UInt" )
    NumPut( fType, struct, 8, "UInt" )
    NumPut( fState, struct, 12, "UInt" )
    NumPut( wID, struct, 16, "UInt" )
    NumPut( this.assocMenu.handle, struct, 16+A_PtrSize, "Ptr" )
    NumPut( dwItemData, struct, 16+4*A_PtrSize, "Ptr" )
    ;~ NumPut( PUM.HBMMENU_CALLBACK, struct, 16+7*A_PtrSize, "Ptr" )

    if ( newItemPos != "" )
      pumAPI._insertMenuItem( this.menu.handle, newItemPos, fByPos, &struct )
    else
      pumAPI._setMenuItemInfo( this.menu.handle, this.id, False, &struct )
  }

  static _defaults := { "issep"  : 0
                          ,"name"   : ""
                          ,"bold"   : 0
                          ,"icon"   : 0
                          ,"iconUseHandle" : 0
                          ,"break"  : 0 ;0,1,2
                          ,"submenu": 0
                          ,"tcolor" : ""
                          ,"bgcolor": ""
                          ,"noPrefix" : 0
                          ,"disabled" : 0
                          ,"noicons" : -1   ;-1 means use parent menu's setting
                          ,"notext" : -1 }
}

/*
PUM_Menu class represent single menu
*/

class PUM_Menu extends PUM_base
{
  static _defaults := { "tcolor"     : pumAPI.GetSysColor( 7 ) ;default - COLOR_MENUTEXT
                        ,"bgcolor"    : pumAPI.GetSysColor( 4 ) ;default - COLOR_MENU
                        ,"nocolors"   : 0
                        ,"noicons"    : 0
                        ,"notext"     : 0
                        ,"iconssize"  : 32
                        ,"textoffset" : 15
                        ,"maxheight"  : 0
                        ,"xmargin"   : 8
                        ,"ymargin"   : 8
                        ,"textMargin" : 15 } ;this is a pixels zmount which will be added after the text to make menu look pretty

  static _trackConsts := {  "context"   : 0x00001  ;TPM_RECURSE
                          ,"hcenter"  : 0x4     ;TPM_CENTERALIGN
                          ,"hleft"    : 0x0     ;TPM_LEFTALIGN
                          ,"hright"   : 0x8     ;TPM_RIGHTALIGN
                          ,"vbottom"  : 0x20    ;TPM_BOTTOMALIGN
                          ,"vtop"     : 0x0     ;TPM_TOPALIGN
                          ,"vcenter"  : 0x10    ;TPM_VCENTERALIGN
                          ,"animlr" : 0x400   ;TPM_HORPOSANIMATION
                          ,"animrl" : 0x800   ;TPM_HORNEGANIMATION
                          ,"animtb" : 0x1000  ;TPM_VERPOSANIMATION
                          ,"animbt" : 0x2000  ;TPM_VERNEGANIMATION
                          ,"noanim" : 0x4000 }  ;TPM_NOANIMATION

  __New( handle, objPUM )
  {
    this.handle := handle
    this.objPUM := objPUM
    this.alive := 1
  }

  ; return default value for parameter if it wasn't set
  __Get( aName )
  {
    if ( aName = "__Class" )
      return PUM_Menu.__Class
    return PUM_Menu._defaults[ aName ]
  }

  __Delete()
  {
    ;~ msgbox % "menu destr: " this.handle
    return
  }

  EndMenu()
  {
    pumAPI._EndMenu()
  }

  Detach()
  {
    if isObject( this.owner )
    {
      this.owner.RemoveSubMenu()
      this.owner := ""
    }
  }

  Destroy()
  {
    if !this.alive
      return 0
    this.Free()
    if pumAPI.IsInteger( this.handle )
      this.objPUM._menus.Remove( this.handle, "" )
    else
      this.objPUM._menus.Remove( this.handle )
    if this.owner
    {
      this.owner.assocMenu := ""
      this.owner.submenu := ""
      this.owner := ""
    }
    this.DestroyItems()
    pumAPI._DestroyMenu( this.handle )
    this.objPUM := ""
    this.alive := 0
  }

  DestroyItems()
  {
    for i,item in this.GetItems()
      item.Destroy()
  }

  IsMenu()
  {
    return pumAPI._isMenu( this.handle )
  }

  GetTColor()
  {
    return pumAPI.RGBtoBGR( this.tcolor )
  }

  GetBGColor()
  {
    return pumAPI.RGBtoBGR( this.bgcolor )
  }

  GetParent()
  {
    return this.owner.GetParent()
  }

  Free()
  {
    ;~ DeleteObject( this.hBrush )
    ;~ this.hBrush := ""
  }

  GetItems()
  {
    if !this.alive
      return 0
    return pumAPI._GetMenuItems( this.handle )
  }

  GetItemByPos( nPos )
  {
    return pumAPI._GetItem( this.handle, nPos, True )
  }

  Count()
  {
    if !this.alive
      return 0
    return pumAPI._GetMenuItemCount( this.handle )
  }

  Show( x = 0, y = 0, flags = "" )
  {
    if !this.alive
      return 0
    item := 0
    tpmflags := 0x100
    for i,v in pumAPI.StrSplit( flags, A_Space, A_Space A_Tab )
      if ( val := PUM_Menu._trackConsts[ v ] )
        tpmflags |= val
    isContext := tpmflags & 0x1
    if !isContext ;check if menu is not recursed menu ( has TPM_RECURSE flag )
    {
      if IsFunc( foo := this.objPum.onshow )
        ret := %foo%( "onshow", this )
      if ( ret = 0 )
        return
      Gui PUM_MENU_GUI:+LastFound +ToolWindow +HwndPUMhParent +AlwaysOnTop
      Gui, PUM_MENU_GUI:Show
      WinActivate,% "ahk_id " PUMhParent
      ControlFocus,,ahk_id %PUMhParent%
      pumAPI._msgMonitor( 1 )
      pumAPI.SetTimer( "PUM_MenuCheck", 100 )
    }
    else
    {
      Gui PUM_MENU_GUI: +LastFoundExist
      PUMhParent := WinExist()
    }
    this.objPUM.IsMenuShown := True
    itemID := pumAPI._TrackPopupMenuEx( this.handle, tpmflags, x, y, PUMhParent )
    this.objPUM.IsMenuShown := False
    if itemID
    {
      if ( item := this.objPUM._items[ itemID ] )
        if isFunc( foo := this.objPUM.onrun )
          %foo%( "onrun", item )
    }

    if !isContext
    {
      pumAPI._msgMonitor( 0 )
      pumAPI.DestroyWindow( PUMhParent )
      if IsFunc( foo := this.objPum.onclose )
        %foo%( "onclose", this )
    }
    return item
  }

  Add( params = "", pos = -1, fByPos = True )
  {
    if !this.alive
      return 0
    id := ++this.objPUM._itemsCount
    item := new PUM_Item( id, this )
    this.objPUM._items[ id ] := item
    item.setParams( params, pos, fByPos )
    return item
  }

  SetParams( params )
  {
    if !this.alive
      return 0
    if IsObject( params )
    {
      for name,val in params
        this[ name ] := val
      if !pumAPI.isEmpty( params["tcolor"] )
        this.tcolor := pumAPI.RGBtoBGR( this.tcolor )
      if !pumAPI.isEmpty( params["bgcolor"] )
        this.bgcolor := pumAPI.RGBtoBGR( this.bgcolor )
    }
    this._update()
  }

  _update()
  {
    this.Free()
    ;typedef struct MENUINFO {
    ;  DWORD   cbSize;				0
    ;  DWORD   fMask;				  4
    ;  DWORD   dwStyle;				8
    ;  UINT    cyMax;				  12
    ;  HBRUSH  hbrBack;				16
    ;  DWORD   dwContextHelpID;		16+ptr
    ;  ULONG_PTR  dwMenuData;		16+2ptr
    ;								16+3ptr

    if ( pumAPI.IsInteger( this.bgcolor ) && !this.nocolors )
      clr := this.bgcolor
    else
      clr := PUM_Menu._defaults[ "bgcolor" ]

    fMask := 0
    fMask |= pumAPI.MIM_BACKGROUND
    fMask |= pumAPI.MIM_MAXHEIGHT
    fMask |= pumAPI.MIM_MENUDATA

    cbSize := pumAPI.MENUINFOsize
    VarSetCapacity( struct, cbSize, 0 )
    NumPut( cbSize, struct, 0, "UInt")
    NumPut( fMask, struct, 4, "UInt")
    NumPut( this.maxHeight, struct, 12, "UInt")
    NumPut( this.objPum.GetBrush( clr ), struct, 16, "UPtr")
    NumPut( &this, struct, 16+2*A_PtrSize, "UPtr")
    pumAPI._SetMenuInfo( this.handle, &struct )
  }
}

PUM_MenuCheck( p* )
{
  Gui,PUM_MENU_GUI:+LastFoundExist
  IfWinNotActive
  {
    pumAPI._EndMenu()
    pumAPI.SetTimer( A_ThisFunc, "OFF" )
  }
  return
}

;handler of WM_ENTERMENULOOP message
PUM_OnEnterLoop()
{
  return 0
}

;handler of WM_EXITMENULOOP	message
PUM_OnExitLoop()
{
  return 0
}

;not currently used
PUM_OnMButtonDown( wParam, lParam, msg, hwnd )
{
  x := lParam & 0xFFFF
  y := lParam >> 16
  IsCtrl := wParam & 0x0008
  IsLMB := wParam & 0x0001
  IsMMB := wParam & 0x0010
  IsRMB := wParam & 0x0002
  IsShift := wParam & 0x0004
  IsXB1 := wParam & 0x0020
  IsXB2 := wParam & 0x0040
  tooltip % x " - " y "`nCtrl " IsCtrl "`nLMB " IsLMB "`nIsMMB " IsMMB "`nIsRMB " IsRMB "`nIsShift " IsShift "`nIsXB1 " IsXB1 "`nIsXB2 " IsXB2
}

;handler of WM_CONTEXTMENU message
PUM_OnRButtonUp( wParam, lParam, msg, hwnd )
{
  if ( item := pumAPI._GetItem( lParam, wParam ) )
  {
    if IsFunc( foo := item.menu.objPUM.onrbutton )
      %foo%( "onrbutton", item )
  }
  return 0
}

;handler of WM_INITMENUPOPUP message
PUM_OnInit( wParam, lParam, msg, hwnd )
{
  hMenu := wParam
  menu := pumAPI._GetMenuFromHandle( hMenu )
  if isFunc( foo := menu.objPUM.oninit )
    %foo%( "oninit", menu )
  return 0
}

;handler of WM_UNINITMENUPOPUP message
PUM_OnUninit( wParam, lParam, msg, hwnd )
{
  hMenu := wParam
  menu := pumAPI._GetMenuFromHandle( hMenu )
  if isFunc( foo := menu.objPUM.onuninit )
    %foo%( "onuninit", menu )
  return 0
}

;handler of WM_MENUCHAR message
PUM_OnMenuChar( wParam, lParam, msg, hwnd )
{
  charCode := wParam & 0xffff
  type := wParam >> 16
  hMenu := lParam
  itemsList := pumAPI._GetMenuItems( hMenu )
  itemPos := ""
  for i,item in itemsList
    if ( item.hotCharCode == charCode )
    {
      itemPos := i-1
      break
    }
  if( itemPos = "" )
    for i,item in itemsList
    {
      if pumAPI.isEmpty( hotChar := SubStr( item.name,1,1 ) )
        continue
      StringLower, hotChar, hotChar
      if ( asc( hotChar ) == charCode )
      {
        itemPos := i-1
        break
      }
    }

  if ( itemPos != "" )
  {
    mode := item.menu.objPUM.mnemonicCmd = "select" ? 3 : 2
    return ( mode << 16 ) | itemPos
  }
  return 0
}

;handler of WM_MENUSELECT, WM_MBUTTONDOWN messages
PUM_OnSelect( wParam, lParam, msg, hwnd )
{
  static hMenu, nItem, fByPosition
  if ( msg = 0x207 ) ;MBUTTON
  {
    if ( item := pumAPI._GetItem( hMenu, nItem, fByPosition ) )
      if isFunc( foo := item.menu.objPUM.onmbutton )
        %foo%( "onmbutton", item )
    return 0
  }
  nItem := wParam & 0xFFFF
  state := wParam >> 16
  isSubMenu := state & 0x10
  ;~ wm := state & 0x00008000
  ;~ ih := state & 0x00000080
  ;~ ig := state & 0x00000001
  ;~ id := state & 0x00000002
  ;~ tooltip % "wm : " wm "`nih : " ih "`nig : " ig "`nid : " id
  hMenu := lParam
  if isSubMenu
    fByPosition := True
  else
    fByPosition := False
  if ( item := pumAPI._GetItem( hMenu, nItem, fByPosition ) )
  {
    if isFunc( foo := item.menu.objPUM.onselect )
      %foo%( "onselect", item )
    return 0
  }
  return 0
}

;handler of WM_DRAWITEM message
PUM_OnDraw( wParam, lParam, msg, hwnd )
{
  critical
  ;~ typedef struct tagDRAWITEMSTRUCT {
  ;~ UINT      CtlType;		    0
  ;~ UINT      CtlID;			4
  ;~ UINT      itemID;			8
  ;~ UINT      itemAction;		12
  ;~ UINT      itemState;		16
  ;~ HWND      hwndItem;		16+ptr
  ;~ HDC       hDC;			    16+2ptr
  ;~ RECT      rcItem;
  ;~ left						16+3ptr
  ;~ top						20+3ptr
  ;~ right						24+3ptr
  ;~ bottom					    28+3ptr
  ;~ ULONG_PTR itemData;		32+3ptr
  ;~                            32+4ptr
  if ( wParam != 0 )    ;means the message not for menu
    return
  ;~ ctlType := NumGet( lParam + 0, 0, "UInt" )
  ;~ if ( ctlType != 1 )  ;ODT_MENU - again check this is menu
    ;~ return
  itemData := NumGet( lParam + 0, 32 + 3 * A_PtrSize, "UPtr" ) ;pointer on <item> object
  item := object( itemData )    ;getting object itself
  itemAction := NumGet( lParam + 0, 12, "UInt" )
  itemState := NumGet( lParam + 0, 16, "UInt" )
  hDC := NumGet( lParam + 0, 16 + 2 * A_PtrSize, "UPtr" )
  pRECT := lParam + 16 + 3 * A_PtrSize
  left := NumGet( pRECT + 0, 0, "UInt" )
  top := NumGet( pRECT + 0, 4, "UInt" )
  right := NumGet( pRECT + 0, 8, "UInt" )
  bottom := NumGet( pRECT + 0, 12, "UInt" )

  ;colors definition
  tcolor := item.menu.nocolors ? PUM_Menu._defaults[ "tcolor" ]
            : item.disabled ? pumAPI.GetSysColor( 17 )
            : ( !pumAPI.IsEmpty( item.tcolor ) ? item.tcolor : item.menu.tcolor )
  bgcolor := !item.menu.nocolors ? ( !pumAPI.IsEmpty( item.bgcolor ) ? item.bgcolor : item.menu.bgcolor )
            : PUM_Menu._defaults[ "bgcolor" ]
  selMethod := item.menu.objPUM.selMethod
  selBGColor := item.menu.objPUM.selBGColor
  selBGColor := selBGColor = -1 ? ~bgcolor & 0xFFFFFF : selBGColor
  selTColor := item.disabled ? pumAPI.GetSysColor( 17 )
              : item.menu.objPUM.selTColor
  selTColor := selTColor = -1 ? ~tcolor & 0xFFFFFF : selTColor
  isItemSelected := ( itemState & 1 )

  itemNoIcons := item.noicons = -1 ? item.menu.noicons : item.noicons
  itemNoText := item.notext = -1 ? item.menu.notext : item.notext

  if ( itemAction = pumAPI.ODA_FOCUS )
    return True
  else ;ODA_DRAWENTIRE | ODA_SELECT
  {
    if item.issep
    {
      pumAPI.SetRect( sepRect, left, top, right, bottom )
      NumPut( top+1, &sepRect, 4, "UInt" )
      pumAPI.DrawEdge( hDC, &sepRect )
    }
    else
    {
      ;filling item's background in case "fill" selection method
      if ( ( itemAction = pumAPI.ODA_SELECT && selMethod = "fill" ) || ( itemAction = pumAPI.ODA_DRAWENTIRE && !pumAPI.IsEmpty( item.bgcolor ) ) )
      {
        clr := isItemSelected ? selBGColor : bgcolor
        pumAPI.FillRect( hDC, pRect, clr )
      }

      ;filling rect with selection color
      if ( selMethod = "fill" && isItemSelected )
        pumAPI.FillRect( hDC, pRect, selBGColor )

      ;drawing frame selection
      if ( selMethod = "frame" && itemAction = PUM.ODA_SELECT )
      {
        clr := isItemSelected ? selBGColor : bgcolor
        loop, % item.menu.objPUM.frameWidth
        {
          pumAPI.SetRect( frameRect, left, top, right, bottom )
          infNum := -1 - ( A_Index - 1 )
          pumAPI.InflateRect( &frameRect, infNum, infNum )
          pumAPI.FrameRect( hDC, &frameRect, clr )
        }
      }
      ;drawing text
      if ( !itemNoText && ( ( itemAction = pumAPI.ODA_SELECT && selMethod = "fill" ) || itemAction = pumAPI.ODA_DRAWENTIRE ) )
      {
        tClr := isItemSelected ? selTColor : tcolor
        bClr := isItemSelected ? selBGColor : bgcolor
        pumAPI.SetBkColor( hDC, bClr )
        hfontOld := pumAPI.SelectObject( hDC, item.hfont )
        textFlags := 0x4 | 0x20 | 0x100 | ( item.noPrefix ? 0x800 : 0 ) ; DT_VCENTER | DT_SINGLELINE | DT_NOCLIP | DT_NOPREFIX(?)
        tleft := left
                  + ( itemNoIcons ? 0 : item.menu.iconssize + item.menu.textoffset )
                  + item.menu.xmargin
        tright := right - ( item.assocMenu ? 15 : 0 ) - item.menu.xmargin
        ttop := top + item.menu.ymargin
        tbot := bottom - item.menu.ymargin
        ;~ if ( item.disabled && !isItemSelected )
        ;~ {
          ;~ SetTextColor( hDC, 0xFFFFFF )
          ;~ SetRect( textRect, tleft + 1, ttop + 1, tright + 1, tbot + 1 )
          ;~ DrawText( hDC, item.name, &textRect, textFlags )
        ;~ }
        pumAPI.SetTextColor( hDC, tClr )
        pumAPI.SetRect( textRect, tleft, ttop, tright, tbot )
        pumAPI.DrawText( hDC, item.name, &textRect, textFlags )
        pumAPI.SelectObject( hDC, hfontOld )
      }
      ;drawing icon
      if ( !itemNoIcons && Item.GetIconHandle()
          && ( ( itemAction = pumAPI.ODA_SELECT && selMethod = "fill" ) || itemAction = pumAPI.ODA_DRAWENTIRE ) )
      {
        pumAPI.DrawIconEx( hDC
                    , left + item.menu.xmargin
                    , top + item._y_icon
                    , item.GetIconHandle() )
      }
      ;drawing submenu arrow
      if item.assocMenu
          && ( ( itemAction = pumAPI.ODA_SELECT && selMethod = "fill" ) || itemAction = pumAPI.ODA_DRAWENTIRE )
      {
        ;code took from here: http://www.codeguru.com/cpp/controls/menu/miscellaneous/article.php/c13017/Owner-Drawing-the-Submenu-Arrow.htm
        bmWidth := 25
        bmHeight := bottom - top
        ;calculating it's pos
        bmY := round( top - ( ( bottom - top ) - bmHeight )/2 )
        bmX := round( right - bmWidth / 1.2 )

        ;drawing arrow in the colors we need
        arrowDC := pumAPI.CreateCompatibleDC( hDC )
        fillDC := pumAPI.CreateCompatibleDC( hDC )
        arrowBM := pumAPI.CreateCompatibleBitmap( hDC, bmWidth, bmHeight )
        fillBM := pumAPI.CreateCompatibleBitmap( hDC, bmWidth, bmHeight )
        oldArrowBitmap := pumAPI.SelectObject( arrowDC, arrowBM )
        oldFillBitmap := pumAPI.SelectObject( fillDC, fillBM )
        ;Set the offscreen arrow rect
        pumAPI.SetRect( tmpArrowR, 0, 0, bmWidth, bmHeight )
        ;Draw the frame control arrow (The OS draws this as a black on
        ;                            white bitmap mask)
        pumAPI.DrawFrameControl( arrowDC, &tmpArrowR, 2, 0 )
        ;Fill the fill bitmap with the arrow color
        clr := isItemSelected ? selTColor : tcolor
        pumAPI.FillRect( fillDC, &tmpArrowR, clr )
        ;Blit the items in a masking fashion
        pumAPI.BitBlt( hDC, bmX, bmY, bmWidth, bmHeight, fillDC, 0, 0, 0x00660046 )
        pumAPI.BitBlt( hDC, bmX, bmY, bmWidth, bmHeight, arrowDC, 0, 0, 0x008800C6 )
        pumAPI.BitBlt( hDC, bmX, bmY, bmWidth, bmHeight, fillDC, 0, 0, 0x00660046 )

        pumAPI.SelectObject( arrowDC, oldArrowBitmap )
        pumAPI.SelectObject( fillDC, oldFillBitmap )
        pumAPI.DeleteObject( arrowBM )
        pumAPI.DeleteObject( fillBM )
        pumAPI.DeleteDC( arrowDC )
        pumAPI.DeleteDC( fillDC )
      }
    }
  }
  ;This call basically is what stops the OS from drawing the submenu arrow
  pumAPI.ExcludeClipRect( hDC, left, top, right, bottom )  ;avoid submenu arrow drawing
  return True
}

;handler of WM_MEASUREITEM message
PUM_OnMeasure( wParam, lParam, msg, hwnd )
{
  critical
  ;~ typedef struct MEASUREITEMSTRUCT {
  ;~ UINT      CtlType;         0
  ;~ UINT      CtlID;           4
  ;~ UINT      itemID;          8
  ;~ UINT      itemWidth;       12
  ;~ UINT      itemHeight;      16
  ;~ ULONG_PTR itemData;        16+ptr
  ;                             16+2ptr
  if ( wParam != 0 )    ;not a menu
    return
  ;~ CtlType := NumGet( lParam+0, 0, "UInt" )
  ;~ if ( CtlType != 1 ) ;not a menu
    ;~ return
  itemData := NumGet( lParam+0, 16+A_PtrSize, "UPtr" )  ;getting stored pointer to item object
  item := Object( itemData )
  if item.issep
    h := 4, w := 0
  else
  {
    itemNoIcons := item.noicons = -1 ? item.menu.noicons : item.noicons
    itemNoText := item.notext = -1 ? item.menu.notext : item.notext
    hDC := pumAPI.GetDC( hwnd )
    hOldFont := pumAPI.SelectObject( hDC, item.hfont )
    size := pumAPI.GetTextExtentPoint32( hDC, item.name )
    w := itemNoIcons ? size.cx
        : itemNoText ? item.menu.iconssize - 11   ;i don't know where this 11 pixels goes from
        : item.menu.iconssize + item.menu.textoffset + size.cx
    w += item.menu.xmargin*2
    if item.submenu
      w += 10 ;15
    else if !itemNoText
      w += item.menu.textMargin
    h := itemNoIcons ? size.cy
        : itemNoText ? item.menu.iconssize
        : pumAPI.max( item.menu.iconssize, size.cy )
    h += item.menu.ymargin*2
    item._y_icon := round( ( h - item.menu.iconssize )/2 )
    pumAPI.SelectObject( hDC, hOldFont )
    pumAPI.ReleaseDC( hDC, hWnd )
  }
  NumPut( w, lParam+0, 12, "UInt" )
  NumPut( h, lParam+0, 16, "UInt" )
  return True
}