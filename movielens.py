# This program analyses MovieLens data based on gender
from articlelength import *

def main():
    # Getting data from files
    movieFile = open('movies.dat', mode='r', encoding='latin_1')
    ratingFile = open('ratings.dat', mode='r', encoding='latin_1')
    userFile = open('users.dat', mode='r', encoding='latin_1')
    # Getting dictionaries from files
    users = makeUserGender(userFile)
    movies = makeMoviesDictionary(movieFile)
    moviesByName = makeMoviesDictionaryByName(movieFile)
    addedRatingsAndUsersToDictionary(ratingFile, movies, users)

    # Counting the number of males and females who reviewed each movie
    ratingCount = countRatings(movies)

    # Finding top 20 movies for each gender
    topMale = sortTopMale(ratingCount)
    topMaleMovies = movieIDName(topMale,movies)
    topFemale = sortTopFemale(ratingCount)
    topFemaleMovies = movieIDName(topFemale,movies)

    # We directly edited the movies.dat file so that the names were the same as
    # Wikipedia
    print('These are the top 20 male movies along with the length of their Wikipedia articles: \n')
    print(articleLength(topMaleMovies), '\n')

    print('These are the top 20 female movies along with the length of their Wikipedia articles: \n')
    print(articleLength(topFemaleMovies), '\n')

    movieFile.close()
    ratingFile.close()
    userFile.close()

# Getting the name of a movie from an ID list
def movieIDName(top, movies):
    topMovies = []
    for ID in top:
        topMovies.append(movies[ID][0])
    return topMovies

# Making a dictionary where the name of the movie is the key
def makeMoviesDictionaryByName(movieFile):
    # Seek sets the pointer of the file back to the starting position
    movieFile.seek(0,0)
    moviesByName = {}
    for row in movieFile:
        row = row.rstrip()
        items = row.split('::')
        # We make the name the key and make a list of the MovieID and Genre associated with it
        moviesByName[items[1]] = [items[0],items[2]]
    return moviesByName

# Making the data from the movies.dat file into a dictionary
def makeMoviesDictionary(movieFile):
    movies = {}
    for row in movieFile:
        row = row.rstrip()
        items = row.split('::')
        # Making a dictionary with the MovieID as the key and a list with name and Genre
        movies[items[0]] = [items[1],items[2]]
    return movies

# Getting the top 20 movies rated by males
def sortTopMale(ratingCount):
    ratingToMovieDict = {}
    lowest = 0
    topTwenty = [0]
    for movie in ratingCount:
        # set the maleRaters to the corrosponding value in ratingCount of male - female raters
        maleRaters = ratingCount[movie][2]
        # If the number of male raters exceeds the previous lowest number remove the old lowest
        # only after there are already twenty values, then assign a new lowest
        if maleRaters >= lowest:
            if len(topTwenty) >= 20:
                topTwenty.remove(lowest)
            topTwenty.append(maleRaters)
            # Make a dictionary of the movies using the male raters as a key
            ratingToMovieDict[maleRaters] = movie
            lowest = sorted(topTwenty)[0]
    # Turn the ratings into the corrosponding movie names
    movieRated = []
    for rating in topTwenty:
        movieRated.append(ratingToMovieDict[rating])
    #Return the list of the top 20 male rated movies
    return movieRated

# Getting the top 20 movies rated by females, we required a new method
# since different movies had the same diferance in ratings
def sortTopFemale(ratingCount):

    #make a dictionsary of just the movieID and the (male raters- female raters)
    femaleRatingCount = {}
    for rating in ratingCount:
        femaleRatingCount[rating] = ratingCount[rating][3]


    counter = 0
    topTwenty = []
    # Sort the dictionary by its values, in desending order and take top 20
    for rating in reversed(sorted(femaleRatingCount.values())):
        if counter < 20:
            counter += 1
            topTwenty.append(rating)

    # Make list of MovieID corrosponding to top twenty ratings
    movieList = []
    for movie in femaleRatingCount:
        if femaleRatingCount[movie] in topTwenty:
            movieList.append(movie)
            if len(movieList) >= 20:
                break
    return movieList

# adding ratings and users to movie Dictionary
def addedRatingsAndUsersToDictionary(ratingFile, movies,users):

    for row in ratingFile:
        row = row.rstrip()
        items = row.split('::')
        # Adding UserID, ratings, gender, and age
        userInfo = [items[0],items[2]] + users[items[0]]
        movies[items[1]].append(tuple(userInfo))

# Make a dictionary from data from users.dat
def makeUserGender(userFile):
    users = {}
    for row in userFile:
        row = row.rstrip()
        items = row.split('::')
        users[items[0]] = [items[1],items[2]]
    return users

# Counts the number of male and female ratings, and the difference between them
def countRatings(movies):
    movieCount = {}
    # Go through all the movies in movies dictionary

    for movie in movies:
        males = 0
        females = 0
        # Go through the list associated with each movie
        for user in movies[movie]:
            # Don't try this on the name of the movie and the genre
            if isinstance(user,tuple):
                # Add 1 to the corrosponding gender
                if user[2] == "M":
                    males += 1
                if user[2] == "F":
                    females +=1

        movieCount[movie] = (males, females, males - females, females - males)
    return movieCount

if __name__ == '__main__':
    main()
