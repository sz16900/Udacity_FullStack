-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS player;

\c tournament;

CREATE TABLE player(
  id SERIAL PRIMARY KEY,
  name VARCHAR(80)
);

CREATE TABLE match(
  winner INT REFERENCES player(id),
  loser INT REFERENCES player(id),
  PRIMARY KEY (winner, loser)
);

insert into player (name) values ('seth');
insert into player (name) values ('zac');
insert into player (name) values ('sam');
insert into player (name) values ('nou');
insert into match values (1, 2);
insert into match values (3, 4);
-- insert into match values (1, 3);
-- insert into match values (2, 4);


select tb_1.id, tb_1.name, tb_1.wins, tb_2.matches from
(select player.id, player.name, count(match) as matches from player left join match on player.id = match.winner or player.id = match.loser group by player.id) as tb_2
join
(select player.id, player.name, count(match.winner) as wins from player left join match on player.id = match.winner group by player.id order by wins desc) as tb_1
on tb_1.id = tb_2.id order by tb_1.wins desc;
