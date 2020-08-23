# tron-ranking
### A web-app that calculates and displays user ratings based on match results

## How to run this
The easiest way to get this running is using docker. There's data already committed to the repo which will be used for calculating and storing rankings in the database when you build the docker image. Once it's built, running it will start the python flask webapp and pull results from the database. 

To build the image, from the command line, simply run 
```
docker build --build-arg RATING_TYPE=trueskill -t ranking_app .
```

from within the base directory (where the Dockerfile lives). The rating type argument specifies whether to use an algorithm like TrueSkill or Elo for ratings. trueskill is preffered at this point, so let's stick with that. 

**Note:** The docker image build will try to read from a google sheet to get data pertaining to matches. If it fails to do that, it will only load existing data in the raw_data directory. If you need the functionality for pulling from the google sheet, you'll have to have a key file that's not checked into github. Please contact me if you need that.  

After it's built, we can run the docker container with
```
docker run -p 5000:5000 ranking_app
```

Now that the container is running, you should be able to see it in action by visiting http://localhost:5000 from your browser!

## Digging a little deeper

You might have some questions on what actually is happening with this. I'll try answering a few of those. If you look in the `raw_data` directory, there you'll find match results used for calculating rankings. Each file in there represents a different "match type". A player will have a different ranking for each match type. For example, if Foo has a bunch of wins recorded in FileXYZ_scorelog_parsed, and a bunch of loses in another, they will have separate rankings for each of those (one relatively high, another low). In the database, those are represented as 2 separate ranking entities, each with their own match type. Match type is interpreted from the filename containing the data. So Foo would have a high elorating with match type FileXYZ. 

With the data in the `raw_data` directory, `load_matches.py` will read through each file in there and calculate and store ratings for each of those match types. This script gets run when you build the docker image. 

Finally, after the script has run, we can start up our web app which will simply be reading those results. At this point, the app is only displaying elo rating for two matchtypes (`sbl_eu_scorelog` and `sbl_us_scorelog`), but it could easily display more if we populate the database with others (there's actually already data in the raw_data directory for over 1000 matches in casual sumoserver which gets stored as elo ratings with match type `scorelog`). 

