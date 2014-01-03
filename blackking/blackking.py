import sqlite3
import os
from random import shuffle

gameRoot = "/Users/flavioperez/Documents/projets/blackking/games/"


class Bk:
    def __init__(self, player=0):
        # INITIALIZE
        self.c = None
        self.con = None
        self.game = "67HT7HT"
        self.player = player
        
        self.connect()
        
        
    def closeCon(self):
        #CLOSECONNECTION
        self.con.close()    
        
    def connect(self):
        # CONNECT
        self.con = sqlite3.connect(gameRoot + self.game+'.db')
        self.c = self.con.cursor()    
    
    def newGame(self,users=4):
        # NEW GAME
        users = int(users)
        self.closeCon()
        
        if os.path.exists(gameRoot + self.game + '.db'):
            os.remove(gameRoot+ self.game + '.db')
            
        self.connect()
           
        self.c.execute('SELECT SQLITE_VERSION()')
        
        data = self.c.fetchone()
        
        print "SQLite version: %s" % data
        
        
        self.c.execute("CREATE TABLE Settings(meta_name TEXT, meta_value TEXT)")
        self.c.execute("INSERT INTO Settings VALUES('Players','4')")
        self.c.execute("INSERT INTO Settings VALUES('CurrentPlayer','1')")
        self.c.execute("INSERT INTO Settings VALUES('CurrentTurn','1')")
        self.c.execute("INSERT INTO Settings VALUES('CurrentPlay','1')")
        self.c.execute("INSERT INTO Settings VALUES('playLimit','0')")
        self.c.execute("INSERT INTO Settings VALUES('timeLimit','0')")
        
        
        
        self.c.execute("CREATE TABLE Objective(objective_player TEXT, objective_mission TEXT, objective_question TEXT, objective_status TEXT)")
        self.c.execute("CREATE TABLE ObjectiveHints(objective_id INT, objective_player TEXT, objective_hint TEXT)")
        
        """
        for i in range (1, users+1):
            missionOder, missionQuestion, missionHints = self.createMission(playerId=i)
            self.c.execute("INSERT INTO Objective VALUES('%s', '%s','%s', 'RUNNING')" % (i, missionOder, missionQuestion))
            lastMissionId = self.c.lastrowid
            
            for h in missionHints:
                self.c.execute("INSERT INTO ObjectiveHints VALUES(%i, '%s', '%s')" % (lastMissionId, i, h))
        """
        self.con.commit()
        
    def getMissions(self):
        self.c.execute("SELECT ROWID, objective_mission, objective_question, objective_status FROM Objective WHERE objective_player = '%s'" % self.player)
        return self.c.fetchall()
        
    def getHint(self):
        # GET HINT
        self.c.execute("SELECT objective_hint FROM ObjectiveHints WHERE objective_player != '%s' ORDER BY RANDOM() LIMIT 1" % self.player)
        return self.c.fetchone()[0]
    
    def createMission(self,missionType=None, playerId=0):
        # CREATE MISSION
        figures = ["White King","White Queen","White Fool","White Horse","White Tower","White Peon","Black King","Black Queen","Black Fool","Black Horse","Black Tower","Black Peon"]
        
        if not missionType:
            missionType = "meeting"
        
        if missionType =="meeting":
            shuffle(figures)
            missionOder = "Your mission is to have the <strong>%s</strong> met the <strong>%s</strong>" % (figures[0], figures[1])
            missionQuestion = "As the <strong>%s</strong> met the <strong>%s</strong> ?" % (figures[0], figures[1])
            missionHints = []
            missionHints.append("Someone as to met the %s" % figures[0])
            missionHints.append("The %s is having a secret meeting" % figures[1])
            missionHints.append("Player %s is in a meeting mission" % playerId)
        return (missionOder, missionQuestion, missionHints)
    
            
        
    
        
    def whichTurnIsIt(self):
        # WHICH TURN
        self.c.execute('SELECT meta_value from Settings WHERE meta_name = "CurrentPlayer"')
        data = self.c.fetchone()[0]
        return data
        con.close()
        
    def nextTurn(self):
        # NEXT TURN
        self.c.execute('SELECT meta_value from Settings WHERE meta_name = "Players"')
        players = int(self.c.fetchone()[0])
        self.c.execute('SELECT meta_value from Settings WHERE meta_name = "CurrentPlayer"')
        currentPlayer = int(self.c.fetchone()[0])
        currentPlayer += 1
        if currentPlayer > players:
            currentPlayer = 1
        self.c.execute('SELECT meta_value from Settings WHERE meta_name = "CurrentPlay"')
        currentPlay = int(self.c.fetchone()[0])
        currentPlay += 1
        self.c.execute('UPDATE Settings SET meta_value="%s" WHERE meta_name="CurrentPlayer"' % currentPlayer)
        self.c.execute('UPDATE Settings SET meta_value="%s" WHERE meta_name="CurrentPlayer"' % currentPlayer)
        self.c.execute('UPDATE Settings SET meta_value="%s" WHERE meta_name="CurrentPlay"' % currentPlay)
        self.con.commit()
        
        
    