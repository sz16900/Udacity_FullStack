import media
import one_thousand_movies

le_voyage_dans_la_lune = media.Movie("Le Voyage dans la lune", 
	"A group of astronomers go on an expedition to the Moon.", 
	"https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Voyage_dans_la_Lune_affiche.jpg/800px-Voyage_dans_la_Lune_affiche.jpg", 
	"https://www.youtube.com/watch?v=_FrdVdKlxUk")

the_great_train_robbery = media.Movie("The Great Train Robery", 
	"A group of bandits stage a brazen train hold-up, only to find a determined posse hot on their heels.",
	"https://images-na.ssl-images-amazon.com/images/M/MV5BYzM5YTkzNzItYmQ4Ny00MWRjLWExMjYtMzNiYzYwY2RiMzJmXkEyXkFqcGdeQXVyMTYxNjkxOQ@@._V1_UY268_CR11,0,182,268_AL_.jpg",
	"https://www.youtube.com/watch?v=gwqC3WJYylA")

the_birth_of_a_nation = media.Movie("The Birth of a Nation",
	"The Stoneman family finds its friendship with the Camerons affected by the Civil War, both fighting in opposite armies. The development of the war in their" +
	"lives plays through to Lincoln's assassination and the birth of the Ku Klux Klan.",
	"https://images-na.ssl-images-amazon.com/images/M/MV5BYTM4ZDhiYTQtYzExNC00YjVlLTg2YWYtYTk3NTAzMzcwNTExXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SY1000_CR0,0,671,1000_AL_.jpg",
	"https://www.youtube.com/watch?v=a9UPOkIpR0A&t=2s")

# movies = [le_voyage_dans_la_lune, the_great_train_robbery, the_birth_of_a_nation]
# one_thousand_movies.open_movies_page(movies)
# print(media.Movie.VALID_RATINGS)

print(media.Movie.__doc__)
print(media.Movie.__name__)
print(media.Movie.__module__)


