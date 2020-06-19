#### The Goal of the website
- Provide comprehensive information in semantics, pronunciation, pragmatic use on a searched word and vividly visualize data returned from select API. 

#### Site users
- Learners of English (and other languages if more appropriate apis are found for other languages)
- English speakers who conduct linguistic research
your users?

#### Data and API
	
- Semantic information from a dictionary API (Merriam Webster or Oxford Dictionary of English API)
- pronunciation info from Youglish API (videos of the term being said from videos on Youtube)
- pragmatic information from Sketch Engine API (the most frequently used subject, verb, adverb associated with the searched term by category


#### Project outline

	
##### Database Schema: 
- This will be a simple database with a users table and a searches table with a one-to-many relationship. The users table will have username and password and the searches table will have all information that are used on the site for every search, so that the user can easily retrieve previous searches 

##### Possible difficulties
- Hard to decide exactly how to store searches
Visualization of the data that come back from the API
The Sketch Engine API is highly complicated with many options, but doesn't really have a library to help make these configurations easier, so working with Sketch might prove to be difficult
	
##### Information to secure:
- User passwords


##### User flow
- User enters a word to search, and the search button fires off three api calls, and have the results visualized in three columns, each per API. If the user wants to save a search, the site will prompt them to sign up for an account
		
##### Stretch Goals
- Allow user to choose different languages supported by Sketch Engine and Youglish, and make the site multilingual
