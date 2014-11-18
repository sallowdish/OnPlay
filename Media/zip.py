import os
import zipfile
import datetime


def print_info(archive_name):
    zf = zipfile.ZipFile(archive_name)
    for info in zf.infolist():
        print info.filename
        print '\tComment:\t', info.comment
        date = datetime.datetime(*info.date_time)
        print '\tSystem:\t\t', info.create_system, '(0 = Windows, 3 = Unix)'
        print '\tZIP version:\t', info.create_version
        print '\tCompressed:\t', info.compress_size, 'bytes'
        print '\tUncompressed:\t', info.file_size, 'bytes'
	zf.extractall('..\Games\games')
	zf.close
    # date = datetime.datetime(*info.date_time)
# zipSize = info.compress_size, 'bytes'
# unzipSize = info.file_size, 'bytes'
		


if __name__ == '__main__':
    print_info('testGame.zip')
	
# with zipfile.ZipFile('testGame.zip', "r") as z:
    # z.extractall('..\Games\games')
# z.close
	
os.remove('testGame.zip')