
# -*- mode: python -*-

block_cipher = None
data_map =  [("dds_to_jpg","dds_to_jpg"),("model_state.pth","."),("data.json","."),("texconv.exe",".")]
a=Analysis(['main.py'],
            pathex=['E:\\Users\\shishaohua.SHISHAOHUA1\\PycharmProjects\\style_swaper_new'],
            binaries=[],
            datas=data_map,
            hiddenimports=[],
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
          [],
          exclude_binaries=True,
          name='Style_Swap',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Style_Swap')