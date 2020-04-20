# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Scripts\\MagPi-Fetch.py'],
             pathex=['H:\\Projects\\Python Related Stuff\\Pyzo Projects\\MagPi-Fetch'],
             binaries=[],
             datas=[],
             hiddenimports=['requests', 'requests_html', 'bs4', 're', 'os', 'time', 'sys', 'TextPrinter', 'ScrapperFunctions', 'SelectorFunctions', 'WriterFunction', 'pkg_resources.py2_warn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='MagPi-Fetch',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='Includes\\RaspberryPiIcon.ico')
