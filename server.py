from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse

HOST_NAME = '192.168.0.10'
PORT_NUMBER = 8080
baseurl = 'http://' + HOST_NAME + ':' + str(PORT_NUMBER)


class GetHandler(BaseHTTPRequestHandler):
    
  def printLocationQR(self, id):
    message_parts = [
    '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">',
    '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es" lang="es">',
    '<head>',
    '<title>nuevo sitio</title>',
    '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />',
    '<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no" />',
    '<script type="text/javascript" src="qrcodejs/jquery.min.js"></script>',
    '<script type="text/javascript" src="qrcodejs/qrcode.js"></script>',
    '</head>',
    '<body>',
    '<div id="inp" style="width:200px; height:200px; margin-top:15px;"></div> Entrada<p/>',
    '<div id="out" style="width:200px; height:200px; margin-top:15px;"></div> Salida<p/>',
    '<div id="query" style="width:200px; height:200px; margin-top:15px;"></div> Consulta<p/>',
    '<script type="text/javascript">',
    'var inp = new QRCode(document.getElementById("inp"), {width:200, height:200});',
    'var out = new QRCode(document.getElementById("out"), {width:200, height:200});',
    'var query = new QRCode(document.getElementById("query"), {width:200, height:200});',
    'inp.makeCode("'+baseurl+'/in?'+str(id)+'");',
    'out.makeCode("'+baseurl+'/out?'+str(id)+'");',
    'query.makeCode("'+baseurl+'/q?'+str(id)+'");',
    '</script>','</body>',''];
    return '\r\n'.join(message_parts)
  
  def printDocumentQR(self, id):
    message_parts = [
    '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">',
    '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es" lang="es">',
    '<head>',
    '<title>nuevo documento</title>',
    '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />',
    '<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no" />',
    '<script type="text/javascript" src="qrcodejs/jquery.min.js"></script>',
    '<script type="text/javascript" src="qrcodejs/qrcode.js"></script>',
    '</head>',
    '<body>',
    '<div id="doc" style="width:200px; height:200px; margin-top:15px;"></div>'+str(id)+'<p/>',
    '<script type="text/javascript">',
    'var doc = new QRCode(document.getElementById("doc"), {width:200, height:200});',
    'doc.makeCode("'+baseurl+'/doc?'+str(id)+'");',
    '</script>','</body>',''];
    return '\r\n'.join(message_parts)
  
  def defaultPage(self, parsed_path):
    message_parts = [
            'CLIENT VALUES:',
            'client_address=%s (%s)' % (self.client_address,
                                        self.address_string()),
            'command=%s' % self.command,
            'path=%s' % self.path,
            'real path=%s' % parsed_path.path,
            'query=%s' % parsed_path.query,
            'request_version=%s' % self.request_version,
            '',
            'SERVER VALUES:',
            'server_version=%s' % self.server_version,
            'sys_version=%s' % self.sys_version,
            'protocol_version=%s' % self.protocol_version,
            '',
            'HEADERS RECEIVED:',
            ]
    for name, value in sorted(self.headers.items()):
        message_parts.append('%s=%s' % (name, value.rstrip()))
    message_parts.append('')
    message = '\r\n'.join(message_parts)
    return(message)

  def siteIn(self, p):
    print self.client_address[0], "IN", p.query
    return "in" + str(p.query)

  def siteOut(self, p):
    print self.client_address[0], "OUT", p.query
    return "out" + str(p.query)

  def siteQuery(self, p):
    print self.client_address[0], "Q", p.query
    return "query" + str(p.query)

  def docCheckin(self, p):
    print self.client_address[0], "DOC", p.query
    return "doc" + str(p.query)



  def do_GET(self):
    parsed_path = urlparse.urlparse(self.path)
    if parsed_path.path == "/newSite":
      message = self.printLocationQR(parsed_path.query)
    elif parsed_path.path == "/newDoc":
      message = self.printDocumentQR(parsed_path.query)
    elif parsed_path.path == "/in":
      message = self.siteIn(parsed_path)
    elif parsed_path.path == "/out":
      message = self.siteOut(parsed_path)
    elif parsed_path.path == "/q":
      message = self.siteQuery(parsed_path)
    elif parsed_path.path == "/doc":
      message = self.docCheckin(parsed_path)
    elif parsed_path.path == "/qrcodejs/qrcode.js":
      message_parts = file('qrcodejs/qrcode.js','r').readlines()
      message_parts.append('')
      message = '\n'.join(message_parts)
    elif parsed_path.path == "/qrcodejs/jquery.min.js":
      message_parts = file('qrcodejs/jquery.min.js','r').readlines()
      message_parts.append('')
      message = '\r\n'.join(message_parts)
    else:
      message = self.defaultPage(parsed_path)
    self.send_response(200)
    self.end_headers()
    self.wfile.write(message)
    return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer((HOST_NAME, PORT_NUMBER), GetHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
