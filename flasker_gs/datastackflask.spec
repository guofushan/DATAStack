# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['yunwei.py','settings.py','add_instance.py','add_monitor.py','add_user.py','backup.py','binlog2sql.py','crontab.py','dbcreate.py','db_driver.py','inventory.py','mysql_adduser.py','mysql_backup.py','mysql_binlog2sql.py','mysql_crontab.py','mysql_dbcreate.py','mysql_detail.py','mysql_log.py','mysql.py','mysql_setmodify.py','mysql_topsql.py','rds_backup.py','rdsmysql.py','rds_table_size.py','scheduler.py','table_size.py','tools.py','user copy.py','user.py','yunweicenter.py','yunwei copy.py','redis_detail.py','add_redis.py','redis_adduser.py'],
    pathex=['/app/yandi/flasker_gs'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='datastackflask',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

