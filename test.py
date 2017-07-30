import os,mimetypes
def debug(*args):
    print args

def walker(basepath):
    filesin = []
    filesout = []
    if basepath:
        debug('Scanning',basepath)

        try:
            os.path.walk(basepath,lambda tag,path,files: [filesin.append(os.path.join(path,x)) for x in files],None)
        except Exception as e:
            debug('Error scanning {}: {}'.format(basename,e))
            pass        
        for f in filesin:
            mtype = mimetypes.guess_type(f)
            if not mtype or not mtype[0]:
                debug('Cannot get mimetype for {}'.format(f))
                continue
            if 'image/' in mtype[0]:
                filesout.append((f,os.stat(f).st_mtime))
            else:
                debug('Warning, unknown mimetype({}) for {}'.format(mtype[0],f))
    debug('{} has {} files'.format(basepath,len(filesout)))
    return filesout
