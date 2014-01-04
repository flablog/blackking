#!/usr/bin/python

import tornado.ioloop
import tornado.web
from tornado.escape import json_encode
import os
import sys
import random

sys.path.append('.')

import blackking.blackking as blackking

debug = True
port = 1985

        
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Which user are you ?<ul>")
        for i in range (1,5):
            self.write('<li><a href="/user/%s/dashboard/">User %s</a></li>' % (i,i))
        self.write("</ul>")

class NewGameHandler(tornado.web.RequestHandler):
    def get(self, playersNb):
        bk = blackking.Bk()
        bk.newGame(playersNb)
        self.write("New game created")

class UserDashboardHandler(tornado.web.RequestHandler):
    def get(self, playerId):
        self.render('dashboard.html', playerId=playerId)
        
        
        
class UserUpdateDashboard(tornado.web.RequestHandler):
    def get(self, playerId):
        
        obj = {}
        bk = blackking.Bk(player = playerId)
        
        currentTurn = bk.whichTurnIsIt()
        
        
        obj["CURRENTTURN"]=str(bk.currentPlay())
        
        
        if currentTurn == '0':
            # Verifier que tout le monde a pas une mission
            bk.canWeStartTheGame()
            currentTurn = bk.whichTurnIsIt()
            
        if currentTurn == playerId:
            obj["TURN"] = "<strong>It's your turn! </strong><button id='IAMDONE' class='btn btn-success btn-xs'>I'm done !</button>"
        elif currentTurn == '0':
            obj["TURN"] = "We are waiting everyone to get a mission to start"
            bk.canWeStartTheGame()
        else:
            obj["TURN"] = "It's player %s turn" % currentTurn
        
        # Current Mission
        missions = bk.getMissions()
        missions.reverse()
        
        hasMission = False
        for m in missions:
            obj["MISSION_MSG_%i" % m[0]] = m[1]
            obj["MISSION_STS_%i" % m[0]] = m[3]
            if m[3] != "SUCCESS":
                hasMission = True
        if not hasMission:
            obj["NEWMISSION"]= "YES"
        else:
            obj["NEWMISSION"] = "NO"
        
        #Last King Move
        lastKingMove = bk.getLastKingMove()
        print lastKingMove
        
        obj["KINGMOVE_MSG"] = lastKingMove[0]
        obj["KINGMOVE_IMGSRC"] = lastKingMove[1]
        obj["KINGMOVE_LASTMSG"] = lastKingMove[2]
        
        # random secret info
        # A chance out of 100
        """
        if (random.random() < .01):
            hint = bk.getHint()
            obj["INFO"] = "<strong>Secret information:</strong> %s" % hint
        """
        print obj
        self.write(json_encode(obj))

        
class UserTurnDoneHandler(tornado.web.RequestHandler):
    def get(self,playerId):
        bk = blackking.Bk(player = playerId)
        currentTurn = bk.whichTurnIsIt()
        if currentTurn == playerId:
            bk.nextTurn()
            self.write('OK')
        else:
            self.write('WRONG USER')
class UserGetMissionHandler(tornado.web.RequestHandler):
    def get(self,playerId):
        print 'NEW MISSION for PLAYER', playerId
        bk = blackking.Bk(player = playerId)
        bk.getNewMission()
        self.write('OK')
    
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/user/(.*)/dashboard/", UserDashboardHandler),
            (r"/user/(.*)/updateDashboard/", UserUpdateDashboard),
            (r"/user/(.*)/turnDone/", UserTurnDoneHandler),
            (r"/user/(.*)/getMission/", UserGetMissionHandler),
            
            (r"/new/(.*)/", NewGameHandler),
            
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
