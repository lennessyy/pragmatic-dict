#### Goal
- Provide comprehensive semantic, phonetic (through video) and pragmatic information on a searched word and visualize pragmatic data in a vertical column chart for viewing ease 
- Deployed at: [Words in the Wild](http://words-in-the-wild.herokuapp.com)

#### Site users
- Learners of English
- Linguistic researchers

#### Requirements
Python 3.7 or above 

#### Dev Quickstart
- Run `pip install -r requirements.txt` to install dependencies
- Run `flask run` to start the development server

#### Stacks and libraries
- Python/Flask
- PostgreSQL
- Bootstrap
- jQuery
- Axios

#### Data and API
	
- Semantic information from a dictionary API ([Merriam Webster](https://dictionaryapi.com/) or Oxford Dictionary of English API)
- pronunciation info from [Youglish](https://youglish.com/api/doc/js-api) API (videos of the term being said from videos on YouTube)
- pragmatic information from [Sketch Engine](https://www.sketchengine.eu/documentation/api-documentation/#toggle-id-2) API (the most frequently used subject, verb, adverb associated with the searched term by category


#### User Flow
- User enters a word to search and the corresponding part of speech
- Click search, or press the `enter` key to conduct search
- Search will return the definitions of the word, or an error message if the word is not found in the dictionary API
- App will visualize the pragmatic data returned from Sketch Engine, showing the frequency of the most common collocations of the searched word by grammatical relationship
- App will also start auto playing a list of YouTube videos whose caption includes the searched word at the mark of the word being uttered
- Users can sign up for the site to save their searches and make notes on their saved searches 

#### Grammatical Relation Labels
Sketch Engine groups collocations by their relationship to the searched word and has defined a set of short-hand labels for these relationships. Here is a list of the common relationships and their labels:

- modifies: A word that is modified by the searched word
- modifier: A word that modifies the searched word
- and/or: A word that appears in parallel with the searched word connected by conjunctions `and` and `or` 
- object_of: A predicate that has the searched word as its object
- subject_of: A predicate that has the searched word as its subject 
- object: A word that is the object of the searched word
- pp_in-p: A word that is modified by a prepositional phrase beginning with the word `in` and the searched word
	- Example:
		- Searched word: eat
		- pp_in-p: silence (eat in silence)
- pp_of-p: A word that is modified by a prepositional phrase beginning with the word `of` and the searched word 
- pp\_obj_of-p: A word that appears in a prepositional phrase beginning with the word `of` that has the searched word as its object
	- Example:
		- Searched word: beauty
		- pp\_obj_of-p: queen (queen of beauty)
- adj_subject: A word that is the subject of a searched adjective
		