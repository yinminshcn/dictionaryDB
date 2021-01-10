import base64
import mimetypes
import re
import requests

def fetch(uri):
    if re.match("http.*", uri):
        dat = requests.get(uri).content
        bs64 = base64.b64encode(dat)
        return ''' src="data:{mime};base64,{dat}" '''.format(mime = mimetypes.guess_type(uri)[0], dat = bs64.decode('utf-8'))
        # return "data:" + mimetypes.guess_type(uri)[0] + ";base64," + bs64.decode('utf-8')
    else:
        with open(uri, "rb") as f:
            dat = f.read()
            bs64 = base64.b64encode(dat)
            return ''' src="data:{mime};base64,{dat}" '''.format(mime = mimetypes.guess_type(uri)[0], dat = bs64.decode('utf-8'))
            # return "data:" + mimetypes.guess_type(uri)[0] + ";base64," + bs64.decode('utf-8')
    return ""