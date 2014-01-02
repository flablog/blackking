#!/usr/bin/python

import tornado.ioloop
import tornado.web
import os
import sys
sys.path.append('.')


debug = False
port = 1984

userCookieName = "intranetUser"

if "/u/R_D" in os.getcwd() or '/dev/' in os.getcwd():
    debug = True
    port = 1985

def getUser(tornadoSession):
    return tornadoSession.get_cookie(userCookieName)
    
class SignInHandler(tornado.web.RequestHandler):
    def get(self, user):
        if not user:
            self.render('signIn.html')
        else:
            self.write(user)
            self.set_cookie(userCookieName, user)
            self.redirect('/')
class SignOutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie(userCookieName)
        self.redirect('/')
        
        
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not getUser(self): self.redirect('/signIn/') # Check User
        user = getUser(self)
        
        # Trains
        import apps.trains
        nextTrains = apps.trains.nextTrains()
        print repr(self.request)
        print self.request.remote_ip 
        self.render('homepage.html', user=user, nextTrains= ", ".join(nextTrains))

class GifGiftHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('gifgift.html')

    
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/signIn/(.*)", SignInHandler),
            (r"/signOut/", SignOutHandler),
            (r"/gifgift/", GifGiftHandler),
        ]
                
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, debug=debug, **settings)


if __name__ == "__main__":
    print "\nStarting ", __file__
    print "serveur demarre sur port ", port 
    if debug:
        print "Debug Mode ON"
        import datetime
        print datetime.datetime.now()
    app = Application()
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()
