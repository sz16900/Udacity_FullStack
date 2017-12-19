#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect("dbname=tournament")
    except:
        print "I am unable to connect to the 'tournament' database."
    return conn

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    try:
        c.execute('DELETE FROM match')
    except:
        print "I cannot clear the 'match' table."
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    try:
        c.execute('DELETE FROM player')
    except:
        print "I cannot clear the 'match' table."
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute('SELECT COUNT(*) FROM player')
    num_players = c.fetchone()
    db.close()
    return int(num_players[0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    try:
        c.execute('INSERT INTO player (name) VALUES (%s)', (name,))
    except:
        print "I cannot create new player."
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    try:
        c.execute("""select tb_1.id, tb_1.name, tb_1.wins, tb_2.matches from
        (select player.id, player.name, count(match) as matches from player left join match on player.id = match.winner or player.id = match.loser group by player.id) as tb_2
        join
        (select player.id, player.name, count(match.winner) as wins from player left join match on player.id = match.winner group by player.id order by wins desc) as tb_1
        on tb_1.id = tb_2.id order by tb_1.wins desc""")
    except:
        "I cannot fetch the players' standings."
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    try:
        c.execute('INSERT INTO match VALUES (%s, %s)', (winner, loser))
    except:
        print "I cannot create a new match."
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()
    pair_list = pairs = list()
    for i in range(0, len(standings), 2):
        pair_list.append((standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1]))
    return pair_list
