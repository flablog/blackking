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
        self.player = int(player)
        
        self.connect()
        
        
    def closeCon(self):
        #CLOSECONNECTION
        self.con.close()    
        
    def connect(self):
        # CONNECT
        self.con = sqlite3.connect(gameRoot + self.game+'.db')
        self.c = self.con.cursor()    
    
    def newGame(self,playersNb=4):
        # NEW GAME : create the database
        playersNb = int(playersNb)
        
        # Destroying db if it exists
        self.closeCon()
        if os.path.exists(gameRoot + self.game + '.db'):
            os.remove(gameRoot+ self.game + '.db')
        
        # New connection : creates a new Db
        self.connect()
        
        self.c.execute('SELECT SQLITE_VERSION()')
        data = self.c.fetchone()
        print "SQLite version: %s" % data
        
        # Settings 
        self.c.execute("CREATE TABLE Settings(meta_name TEXT, meta_value TEXT)")
        self.c.execute("INSERT INTO Settings VALUES('Players','%i')" % playersNb)
        self.c.execute("INSERT INTO Settings VALUES('CurrentPlayer','0')")
        self.c.execute("INSERT INTO Settings VALUES('CurrentTurn','0')")
        self.c.execute("INSERT INTO Settings VALUES('CurrentPlay','0')")
        self.c.execute("INSERT INTO Settings VALUES('playLimit','0')")
        self.c.execute("INSERT INTO Settings VALUES('timeLimit','0')")
        self.c.execute("INSERT INTO Settings VALUES('startedAd','0')")
        
        self.c.execute("INSERT INTO Settings VALUES('Player1Color','0')")
        self.c.execute("INSERT INTO Settings VALUES('Player2Color','0')")
        self.c.execute("INSERT INTO Settings VALUES('Player3Color','0')")
        self.c.execute("INSERT INTO Settings VALUES('Player4Color','0')")
        self.c.execute("INSERT INTO Settings VALUES('Player5Color','0')")
        
        
        # Create Missions
        self.c.execute("CREATE TABLE Missions(mission_name TEXT, p1 INT, p2 INT, p3 INT, p4 INT, p1Color INT, p2Color INT, p3Color INT, p4Color INT, mission_points INT, mission_level INT, assigned INT, status INT)")
        # Missions status 0 : not assigned, 1, running, 2 poll, 3 success
        self.populateMissions()
        #self.populateMissions()
        #self.populateMissions()
        
        # Mission Polls
        self.c.execute("CREATE TABLE MissionPoll(missionId INT, player INT, vote INT, result INT)")
        
        # King Moves
        self.c.execute("CREATE TABLE KingMoves(message TEXT, image_url TEXT, releaseTime INT)")
        self.c.execute("INSERT INTO KingMoves VALUES('The King is awaking and getting ready for a new day...','',%i)" % time.time())
        
        self.populateKingMoves()
        self.populateKingMoves()
        self.populateKingMoves()
        
        
        self.con.commit()
    def getScores(self):
        self.c.execute('SELECT meta_value from Settings WHERE meta_name = "Players"')
        players = int(self.c.fetchone()[0])
        scores = {}
        for p in range(1, players+1):
            scores[p] = 0
        
        self.c.execute('SELECT assigned, mission_points FROM Missions WHERE assigned != 0 and status == 3')
        for r in self.c.fetchall():
            scores[r[0]] += r[1]
            
        return scores
        
               
    def votePoll(self, missionId, vote):
        #CREATE TABLE MissionPoll(missionId INT, player INT, vote INT, result INT)
        self.c.execute('UPDATE MissionPoll SET vote = 1, result= %i WHERE missionId = %i and player= %i' %  (int(vote), int(missionId), self.player) )
        self.con.commit()
        
        # Check if mission is validated
        self.c.execute('SELECT vote, result from MissionPoll WHERE missionId = %i' % int(missionId))
        everyoneHasVote = True
        pollValidated = True
        print '\nchecking Vote'
        for r in self.c.fetchall():
            print r
            if r[0] == 0:
                everyoneHasVote = False
            else:
                if r[1] == 0:
                    pollValidated = False
        print "everyoneHasVote", everyoneHasVote, "pollValidated", pollValidated
        print ''
        if everyoneHasVote and pollValidated:
            print "MISSION VALIDATED :", missionId
            self.c.execute('UPDATE Missions SET status = 3 WHERE ROWID = %i' %  int(missionId) )
            self.c.execute('DELETE FROM MissionPoll WHERE  missionId = %i' %  int(missionId) )
            self.con.commit()
        if everyoneHasVote and not pollValidated:
            print "MISSION NOT VALIDATED :", missionId
            self.c.execute('UPDATE Missions SET status = 1 WHERE ROWID = %i' %  int(missionId) )
            self.c.execute('DELETE FROM MissionPoll WHERE  missionId = %i' %  int(missionId) )
            self.con.commit()
            
    
    def getMyPolls(self):
        self.c.execute('SELECT missionId from MissionPoll WHERE player = %i and vote =0' % self.player)
        missionsToCheck = []
        for r in self.c.fetchall():
            missionsToCheck.append(r[0])
        return missionsToCheck
        
    def callForPoll(self, missionId):
        self.c.execute('SELECT meta_value from Settings WHERE meta_name = "Players"')
        players = int(self.c.fetchone()[0])
        
        # Check IF poll is not running already
        
        self.c.execute('UPDATE Missions SET status = 2 WHERE ROWID = %i' %  int(missionId) )
        
        
        for i in range(1, players+1):
            if self.player == i: continue
            self.c.execute('INSERT INTO MissionPoll VALUES(%i, %i, 0, 0)' % (int(missionId), i))
        
        self.con.commit()
        #MissionPoll(missionId INT, player INT, vote INT, result INT)
    
    def assignNewMission(self, difficulty=1):
    
        # Get an available mission according to difficulty
        self.c.execute("SELECT ROWID FROM Missions WHERE assigned == 0 and mission_level == %i  ORDER BY RANDOM() LIMIT 1" % (difficulty))
        missionId =  self.c.fetchone()[0]
        
        self.c.execute('UPDATE Missions SET assigned = %i, status = 1 WHERE ROWID = %i' % ( self.player, missionId) )
        self.con.commit()
        return missionId
    def getMissions(self, missionId=None):
    
        if not missionId:
            self.c.execute("SELECT ROWID, mission_name, p1, p2, p3, p4, p1Color, p2Color, p3Color, p4Color, mission_points, mission_level, assigned, status FROM Missions WHERE assigned = %i" % self.player)
        else:
            self.c.execute("SELECT ROWID, mission_name, p1, p2, p3, p4, p1Color, p2Color, p3Color, p4Color, mission_points, mission_level, assigned, status FROM Missions WHERE ROWID = %i" % missionId)
        missions = []
        for r in self.c.fetchall():
            m = {}
            m['ROWID'] = r[0]
            m['name'] = r[1]
            m['p1'] = r[2]
            m['p2'] = r[3]
            m['p3'] = r[4]
            m['p4'] = r[5]
            m['p1Color'] = r[6]
            m['p2Color'] = r[7]
            m['p3Color'] = r[8]
            m['p4Color'] = r[9]
            m['mission_points'] = r[10]
            m['mission_level'] = r[11]
            m['assigned'] = r[12]
            m['status'] = r[13]
            missions.append(m)
            
        return missions
        
        
    def canWeStartTheGame(self):
        # Get the current Mission
        #print 'Checking if game can start'
        self.c.execute('SELECT meta_value from Settings WHERE meta_name = "Players"')
        players = int(self.c.fetchone()[0])
        playerAsMission = {}
        for i in range(1, players+1):
            playerAsMission[i] = False
            
            #self.c.execute("CREATE TABLE Missions(mission_name TEXT, p1 TEXT, p2 TEXT, p3 TEXT, p4 TEXT, p1Color INT, p2Color INT, p3Color INT, p4Color INT, mission_points INT, mission_level INT, assigned INT, status INT)")
        
        self.c.execute("SELECT ROWID, assigned, status FROM Missions")
        for r in self.c.fetchall():
            if int(r[1]) in playerAsMission.keys() and r[2] in [1, 2]:
                playerAsMission[int(r[1])] = True
        gameCanStart = True
        for k in playerAsMission.keys():
            if playerAsMission[k] == False:
                gameCanStart=False
        #print playerAsMission
        if gameCanStart:
            # Game can start
            #new turn !
            self.nextTurn()

            
    
    
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
            (1,     'trusts the bishops'),
            (1,     'trusts his queen'),
            (1,     'trusts the towers'),
            (1,     'trusts the horses'),
            (1,     'trusts everyone on black squares'),
            (1,     'trusts everyone on white squares'),
            (1,     'trusts everyone near the gates'),
            (1,     'trusts everyone around him'),
            
            # Distrusts
            (1,     'trusts no one in his perpendicular vision'),
            (1,     'distrusts his queen'),
            (1,     'distrusts the towers'),
            (1,     'distrusts the horses'),
            (1,     'distrusts the bishops'),
            (1,     'distrusts everyone on black squares'),
            (1,     'distrusts everyone on white squares'),
            (1,     'distrusts everyone near the gates'),
            (1,     'distrusts everyone around him'),
            
            
            #Collective Action
            (1,     'wants a bal! everyone move a piece in L'),
            (1,     'is tired of his court, everyone bring 1 new subject'),            
            (1,     'is agoraphobe, everyone take out 1 subject'),               
            
             
            #Chances
            (1,     'wants to see the queen'),
            (1,     'wants to see the bishops'),
            (1,     'wants to see the towers'),
            (1,     'wants to see the horses'),
            (1,     'exiles a figure'),
            (1,     'exiles 2 pawns'),
            (1,     'is sleeping, swap two figures'),
            (1,     'wants a private audience, bring 2 near him'),
            (1,     'feels generous, promote one pawn to a higher figure'),
            (1,     'is trustful, change one piece to black'),           
            (1,     'eared rumors, you change mission'),
            (1,     'is sleeping in, you can perform one more action'),
            (1,     'is drunk, a pawn uses the secret passageway under his throne '),
            
        
        
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
            
            
            self.c.execute("INSERT INTO Missions VALUES('%s', %i, %i, %i, %i, %i, %i, %i, %i, %i, %i, 0, 0)" % (m[0], p1, p2, p3, p4, colors[0], colors[1], colors[2], colors[3], m[5], m[6]))
        
    