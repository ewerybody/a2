# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\eric\\io\\code\\a2\\lib\\batches\\..\\..\\ui\\a2app.py'],
             pathex=['C:\\Users\\eric\\io\\code\\a2\\lib\\batches\\'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='a2app',
          debug=False,
          strip=False,
          upx=False,
          console=False , icon='C:\\Users\\eric\\io\\code\\a2\\ui\\res\\a2.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='a2app')
