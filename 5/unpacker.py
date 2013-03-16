import datetime
import zipfile
from zipfile import ZipInfo


def print_info(archive_name):
    zf = zipfile.ZipFile(archive_name,compression=zipfile.ZIP_DEFLATED)
    for info in zf.infolist():
        x=[
            'orig_filename',
            'filename',
            'date_time',
            'compress_type',
            'comment',
            'extra',
            'create_system',
            'create_version',
            'extract_version',
            'reserved',
            'flag_bits',
            'volume',
            'internal_attr',
            'external_attr',
            'header_offset',
            'CRC',
            'compress_size',
            'file_size',
            '_raw_time',
        ]
        print '------------------------'
        for _x in x:
            print _x,'',getattr(info,_x)


def create():
    print 'creating archive'
    zf = zipfile.ZipFile(r'C:\Users\attila\Desktop\ring\5\hacked_011.FCStd', mode='w',
                    compression=zipfile.ZIP_DEFLATED

                         )
    try:
        files=[
            'Document.xml',
            'PartShape.brp',
            'PartShape1.brp',
            'PartShape2.brp',
            'GuiDocument.xml',
            'DiffuseColor',
            'DiffuseColor1',
        ]
        for f in files:
            fn = r'C:\Users\attila\Desktop\ring\5\x4\\' + f
            zf.write(fn,arcname=f)
    finally:
        print 'closing'
        zf.close()

create()

#print_info(r'C:\Users\attila\Desktop\ring\5\PR_014.FCStd')
#print_info(r'C:\Users\attila\Desktop\ring\5\zipfile_write.FCStd')

'''
orig_filename  Document.xml
filename  Document.xml
date_time  (2013, 3, 15, 15, 26, 24)
compress_type  8
comment
extra
create_system  0
create_version  20
extract_version  20
reserved  0
flag_bits  0
volume  0
internal_attr  0
external_attr  2176057344
header_offset  0
CRC  1962020135
compress_size  2044
file_size  12314
_raw_time  31564
'''


