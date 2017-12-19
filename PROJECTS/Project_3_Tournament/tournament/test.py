import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    conn = ""
    try:
        conn = psycopg2.connect("dbname=tournament")
    except:
        print "I am unable to connect to the 'tournament' database."
    return conn

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
    c.execute("""select tb_1.id, tb_1.name, tb_1.wins, tb_2.matches from
    (select player.id, count(*) as matches from player left join match on player.id = match.winner or player.id = match.loser group by player.id) as tb_2
    join
    (select player.id, player.name, count(match.winner) as wins from player left join match on player.id = match.winner group by player.id order by wins desc) as tb_1
    on tb_1.id = tb_2.id""")
    rows = c.fetchall()
    print len(rows)
    exit()
    db.close()
    exit()

playerStandings()
