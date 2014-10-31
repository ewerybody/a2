d = {
    'nfo':{
        'name': 'nameOfTheModule',
        'about': 'some text about the module',
        'author': 'Author Name',
        'version': 0.1
    },
    'cfg': {
        'hotkey':[{
            'label': 'Small Text of whats the Hotkey for',
            'key': '+WheelUp', # direct AHK style hotkey string
            'keyChange': False, # user can change the hotkey
            'scope': 'ahk_class SomeWindowClass123', # None = global hotkey
            'scopeChange': False, # User can change scope
            'send': '^v', # applies win version specific send method
            'code': 'MsgBox Hello!', # direct AHK code snippet
            'enabled': False, # if set, the hotkey is not enabled by default
            'multi': True, # can have multiple hotkeys with shared functionality and scope
            'include': 'nameOfTheModule.ahk' # when enabled this script file will be included on a2 start
        },
        {
            'label': 'Browse Back',
            'key': '+WheelDown',
            'scope': 'ahk_class Chrome_WidgetWin_1',
            'code': 'Send, {Browser_Back}'
        }]
    }
}