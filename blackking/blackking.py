import sqlite3
import os
from random import shuffle
import random
import time

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
    
    def newGame(self,playersNb=4):
        # NEW GAME
        playersNb = int(playersNb)
        self.closeCon()
        
        if os.path.exists(gameRoot + self.game + '.db'):
            os.remove(gameRoot+ self.game + '.db')
            
        self.connect()
           
        self.c.execute('SELECT SQLITE_VERSION()')
        
        data = self.c.fetchone()
        
        print "SQLite version: %s" % data
        
        
        self.c.execute("CREATE TABLE Settings(meta_name TEXT, meta_value TEXT)")
        self.c.execute("INSERT INTO Settings VALUES('Players','%i')" % playersNb)
        self.c.execute("INSERT INTO Settings VALUES('CurrentPlayer','0')")
        self.c.execute("INSERT INTO Settings VALUES('CurrentTurn','0')")
        self.c.execute("INSERT INTO Settings VALUES('CurrentPlay','0')")
        self.c.execute("INSERT INTO Settings VALUES('playLimit','0')")
        self.c.execute("INSERT INTO Settings VALUES('timeLimit','0')")
        self.c.execute("INSERT INTO Settings VALUES('startedAd','0')")
        
        #self.c.execute("CREATE TABLE Players(player_name TEXT)")
        #for i in range(0,playersNb):
        #    self.c.execute("INSERT INTO Players VALUES('Player %d')" % str(i+1))
        
        #self.c.execute("CREATE TABLE Objective(objective_player TEXT, objective_mission TEXT, objective_question TEXT, objective_status TEXT)")
        #self.c.execute("CREATE TABLE ObjectiveHints(objective_id INT, objective_player TEXT, objective_hint TEXT)")
        
        self.c.execute("CREATE TABLE Missions(mission_name TEXT, p1 TEXT, p2 TEXT, p3 TEXT, p4 TEXT, p1Color INT, p2Color INT, p3Color INT, p4Color INT, mission_points INT, mission_level INT, assigned INT)")
        
        self.populateMissions()
        
        self.c.execute("CREATE TABLE KingMoves(message TEXT, image_url TEXT, releaseTime INT)")
        
        self.c.execute("INSERT INTO KingMoves VALUES('The King is going to walk on his castle','',%i)" % time.time())
        
        self.populateKingMoves()
        
        
        self.con.commit()
    def populateMissions(self):
        
           
        #      'mission Name'   , 'Piece1', 'Piece2', 'Piece3', 'Piece4', Points, difficulty
        
        missions = [
            #['',         '','','','',   1  , 1 ],
            ['',         'F','F','C','P',    5  , 4  ],
            ['',         'F','F','T','P',    5  , 4  ],
            ['',         'F','F','P','P',    5  , 4  ],
            ['',         'T','T','P','P',    5  , 4  ],
            ['',         'T','T','C','P',    5  , 4  ],
            ['',         'T','T','F','P',    5  , 4  ],
            ['',         'C','C','P','P',    5  , 4  ],
            ['',         'C','C','F','P',    5  , 4  ],
            ['',         'C','C','T','P',    5  , 4  ],
            ['',         'C','T','F','P',    3  , 3  ],
            ['',         'R','C','F','P',    3  , 3  ],
            ['',         'R','T','C','P',    3  , 3  ],
            ['',         'T','F','P','P',    3  , 3  ],
            ['',         'R','T','F','P',    3  , 3  ],
            ['',         'R','C','P','P',    2  , 2  ],
            ['',         'R','T','P','P',    2  , 2  ],
            ['',         'C','F','P','P',    2  , 2  ],
            ['',         'R','F','P','P',    2  , 2  ],
            ['',         'T','C','P','P',    2  , 2  ],
            ['',         'F','P','P','P',    1  , 1  ],
            ['',         'F','P','P','P',    1  , 1  ],
            ['',         'R','P','P','P',    1  , 1  ],
            ['',         'C','P','P','P',    1  , 1  ],
            ['',         'T','P','P','P',    1  , 1  ],
            ['',         'T','P','P','P',    1  , 1  ],
            ['',         'C','P','P','P',    1  , 1  ],
            ['',         'R','P','P','P',    1  , 1  ],

        ]
        
        for m in missions:
            # Couleur aleatoire sur une des pieces
            # 0 = black, 1= white, 2 = nocolor
            colors = [2,2,2,2]
            piecesToPick = [0,1,2,3]
            random.shuffle(piecesToPick)
            
            colors[piecesToPick[0]] = random.randint(0,1)
            
            # Pieces 
            pieces = {'P': 0,'T':1, 'C':2, 'F':3, 'R': 4}
            p1 = pieces[m[1]]
            p2 = pieces[m[2]]
            p3 = pieces[m[3]]
            p4 = pieces[m[4]]
            
            
            self.c.execute("INSERT INTO Missions VALUES('%s', %i, %i, %i, %i, %i, %i, %i, %i, %i, %i, 0)" % (m[0], p1, p2, p3, p4, colors[0], colors[1], colors[2], colors[3], m[5], m[6]))
        
            
    def canWeStartTheGame(self):
        # Get the current Mission
        print 'Checking if game can start'
        self.c.execute('SELECT meta_value from Settings WHERE meta_name = "Players"')
        players = int(self.c.fetchone()[0])
        playerAsMission = {}
        for i in range(1, players+1):
            playerAsMission[i] = False
        
        self.c.execute("SELECT ROWID, objective_player, objective_status FROM Objective")
        for r in self.c.fetchall():
            if int(r[1]) in playerAsMission.keys() and r[2] in ['RUNNING', 'POOL']:
                playerAsMission[int(r[1])] = True
        gameCanStart = True
        for k in playerAsMission.keys():
            if playerAsMission[k] == False:
                gameCanStart=False
        print playerAsMission
        if gameCanStart:
            # Game can start
            #new turn !
            self.nextTurn()
       
    def getMissions(self):
        
        self.c.execute("SELECT ROWID, objective_mission, objective_question, objective_status FROM Objective WHERE objective_player = '%s'" % self.player)
        return self.c.fetchall()
        
        
    def getHint(self):
        # GET HINT : ABANDON
        return ''
        self.c.execute("SELECT objective_hint FROM ObjectiveHints WHERE objective_player != '%s' ORDER BY RANDOM() LIMIT 1" % self.player)
        return self.c.fetchone()[0]
        
        
    
    def getNewMission(self, difficulty=1):
        missionOrder, missionQuestion, missionHints = self.createMission()
        print 'New Mission :', missionOrder
        self.c.execute("INSERT INTO Objective VALUES('%s', '%s','%s', 'RUNNING')" % (self.player, missionOrder, missionQuestion))
        self.con.commit()
        
    def createMission(self,missionType=None, playerId=0):
        # CREATE MISSION : ABANDON
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
    
            
    def populateKingMoves(self):
        cardsProbability=[
            # King useless
            (3,    'reflects on the meaning of life'),
            
            # king moves
            (1,     'the king moves to the closest corner'),
            (1,     'the king moves to the further corner'),
            (1,     'the king changes direction and moves'),
            (1,     'the king is impatient and moves three times'),
            
            # Trust
            (1,     'trusts everyone in his perpendicular vision'),
            (1,     'trusts everyone in his diagonal vision'),
            (1,     'trusts the bishops'),
            (1,     'trusts his queen'),
            (1,     'trusts the towers'),
            (1,     'trusts the horses'),
            (1,     'trusts everyone on black squares'),
            (1,     'trusts everyone on white squares'),
            (1,     'is trustful today, change one piece to black'),
            
            # Distrusts
            (1,     'trusts no one in his perpendicular vision'),
            (1,     'trusts no one in his diagonal vision'),
            (1,     'distrusts his queen'),
            (1,     'distrusts the towers'),
            (1,     'distrusts the horses'),
            (1,     'distrusts the bishops'),
            (1,     'distrusts everyone near a door'),
            (1,     'distrusts everyone on white squares'),
            (1,     'distrusts everyone around him, he needs some fresh air'),
            (1,     'distrusts everyone near the gates'),
        
            #Calls
            (1,     'wants to see the queen, privately'),
            (1,     'wants to confess. He call the bishops'),
            (1,     'wants his bodyguards, the towers'),
            (1,     'wants to hunt and need his horses'),
            (1,     'wants some company and call three different people from his court'),
            (1,     'is tired of his court, bring 2 new subjects into the palace'),
            
            #Exiles
            (1,     'exiles a figure'),
            (1,     'exiles 2 pawns'),
        
        
            # Specials
            (1,     'eared rumors, you change mission'),
            (1,     'wants a bal! everyone move a piece in L'),
            (1,     'is sleeping, exchange two figures'),
        
        
        
        ]
        
        cards = []
        for c in cardsProbability:
            for i in range(0,c[0]):
                
                #cards.append(c[1])
                #moves
                moves = True
                if random.random() > .8: moves = False
                
                sentance = ''
                if 'the king' in c[1]:
                    sentance = c[1]
                
                else:
                    if moves:
                        sentance = "the king moves and " + c[1] 
                    else:
                        sentance = "the king " + c[1]
                cards.append(sentance)
        
        random.shuffle(cards)
        
        for c in cards:
            #KingMoves(message TEXT, image_url TEXT)
            self.c.execute("INSERT INTO KingMoves VALUES('%s','',0)" % c)
        self.con.commit()
    
    def currentPlay(self):
        self.c.execute('SELECT meta_value from Settings WHERE meta_name = "CurrentPlay"')
        data = self.c.fetchone()[0]
        return data
    def whichTurnIsIt(self):
        # WHICH TURN
        self.c.execute('SELECT meta_value from Settings WHERE meta_name = "CurrentPlayer"')
        data = self.c.fetchone()[0]
        return data
        con.close()
    def getLastKingMove(self):
        self.c.execute('SELECT message, image_url, releaseTime from KingMoves ORDER BY releaseTime DESC LIMIT 1')
        return self.c.fetchone()
         
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
        
        # Verifier que j'ai assez de cartes rois
        
        # Nouveau move du roi
        self.c.execute('UPDATE KingMoves SET releaseTime="%i" WHERE ROWID=%i' % (time.time(), currentPlay))
        #KingMoves(message TEXT, image_url TEXT, releaseTime INT)
        
        self.con.commit()
        
        
    