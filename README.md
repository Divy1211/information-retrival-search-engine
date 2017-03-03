# Information Retrival Search Engine

## Quick-index to assignment questions
* [Question 1](#question-1)
  * [How you crawled the corpus?](#question-11)
  * [what kind of information users would like to retreive?](#question-12)
  * [The numbers of records, words, and types (i.e., unique words) in the corpus](#question-13)

## Overview

The information retrieval search engine built by our team is based on Movies, the data for which has been obtained by the TMDB api. Our motivation for picking the above in order to build an information retrieval system is influenced by two main factors: 
- **Real world application**  
A typical Movie data consists of title, plot description, poster, genre, date, language, runtime, actors, review etc. that provides realistic paramteres for the construction of a typical search engine in real world. As a result, although set on Movie data, the search engine helps us draw parallels to many other forms of real world data.
- **Opportunity to learn**  
The Movie data consists of numbers, dates, text, images, urls i.e. a great amalgamation of datafor trying different techniques taught in the information retreival course. Thus, we felt the dataset provided enough diversity to learn something new.


## 1 Crawling the data

### Question 1

#### Question 1.1   
#### How you crawled the corpus (e.g., source, keywords, API, library) and stored them (e.g., whether a record corresponds to a file or a line, meta information like publication date, author name, record ID)  
The Movie Db (TmDB) api was used to extract the corpus and relevant information about the movies. The crawled and extracted corpus was stored in the formed of json-like text files. A single document consists of a text file with a single movie record containing the detailed plot information. During crawling, it was observed that ceratin records from the api call lacked plot information. We ignored such records during crawling as they were insignificant to the kind of information retreival system required. Each unique text fil.e is saved with a unique id from 1 to greater than 20,000. The unique identifier for each record is the 'imdb_id' as well as the text file number in our case. While the api returns a lot of information, we only store the following meta-data for each record:
 
 - **Title**  
   The title of the film. The title will be indexed along with the plot.
 - **Overview**  
   The plot of the film. The main text of the document.
 - **tagline**   
   The film 'tagline' or a catchphrase or slogan, especially as used in advertising, or the punchline of the film.
 - **runtime**  
   The runtime of the film. This is an integer field which is not indexed. However, it is used as a stored field that is     displayed with the search results.
 - **poster_path**  
   The poster path of the link consists of the partial url to the film banner which can be NULL.
 - **genres**  
    The genre under which the image is categorised.  One film might be categorised under more than one genre.
 - **production_companies**  
    The names of all production companies releveant in the production of the film. One film might be categorised under several production houses.
 - **release_date**  
    The official release date of a film. This might contain information of several unreleased films. Such films do not have a released date.
 - **imdb_id**  
    The unique imdb id for each movie
 - **popularity**  
    The popularity is a numeric value between 0 to 1 which corresponds to the ranking of the film according to viewer ratings
 - **revenue**  
    The revenue of a film gives the total projected collections made by the film. It might not be available for all films.
 - **vote_average**  
    Gives the average vote count of the film
 - **adult**  
    A boolean value that categorizes the film's approved audience to be adult- True or False.
    

#### Question 1.2   
#### What kind of information users might like to retrieve from your crawled corpus (i.e., applications), with example queries  
Most frequenty users might want to search for a particular movie by its title and find out it's information such as rating, popularity, plot, genre by searching for the main title. The users may also like to recollect the title of some movie by typing in the plot or tagline. Thus, we would like to support both kinds of searches. Furthermore, users might want to search for a list of movies by one or more movie genre and decide to watch the most popular movie in that segment.  

We aim to archieve the basic Query functionalities, the implementation of advanced query features is subject to our progress.  

| Query type        | Example of basic Query         | Example of advanced Query                                                                                                  | Expected Result                                                 | Details                                                                                                                                                        |
|-------------------|--------------------------------|----------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Search by title   | fear of clowns (exact title)   | Frea of Clowns (Spell check)                                                                                               | Movies with similar title                                       | The result should be specific, not more than 3-5 films unless the title is a series                                                                            |
| Search by tagline | competitive gymnastics         | competition of gymnasts (Spell check)                                                                                      | Movie with similar tagline                                      | The result should be specific, not more than 3-5 films unless the title is a series                                                                            |
| Search by plot    | murderous clowns in circus     |                                                                                                                            | Movies with similar plot overview                               | The result can be little less specific and not limited to 3-5 films                                                                                            |
| Search by genre   | crime and thriller movies      | movies with suspense and murder (deciding which genre the user is looking for based on classification from previous data)  | Movies under the crime and thriller genre, sorted by popularity | A good example for boolean indexing by Genre                                                                                                                   |
| Search by review  | > 4.7 popularity, < 6.7 rating | Average popularity movies(with ambiguous popularity ratings)                                                               | Movies who are popular than 4.7 rating, less than 6.7 rating    | Try to convert user text search for a range of ratings, and display results likewise. The simple case could be to use filter, while the advanced would be NLP. |

#### Question 1.3  
#### The numbers of records, words, and types (i.e., unique words) in the corpus

## 2 Indexing and querying

The corpus was indexed using the python Whoosh library. There were two main reasons for chosing Whoosh over Solr+Lucene.  
- Firstly, Whoosh is a python library which is the same as the rest of our project environment. The crawling task was done in python, as well as the website was developed in Django.
- Secondly, it's simplicity and elegance at handling indexing, querying and ranking.

The trade-off with Whoosh vs. Solr+Lucene is the speed in case the number of documents are large. However, for around 20K records, the speed difference is insignificant. As a result, Whoosh was used for Indexing, Querying and Ranking of documents.

### 1. Indexing

- _Basic Indexing of both document and query_  
The initial indexing was done by simple tokenization of text followed by conversion to lowercase. However, this included indexing of every word as it is. This meant different variants of a word would be considered different tokens and indexed likewise. However, this was not effecient because when a user searched for the term 'murder' he or she maybe talking about 'murderous' or 'murderly' etc. The basic indexing method limited our text search.

- _Stemming Analysis of both document and query_
The search was able to improve with the help of Stemming Analysis. The text was first tokenised and converted to lowercase, also changing them to their root form. 

_Both the query and documents were stemmed_  

For example,
```python
from whoosh.analysis import RegexTokenizer
rext = RegexTokenizer()
indexed = rext(u"This text is beautifully indexed")
stemmer = StemFilter()
print ([token.text for token in stemmer(stream)])
['Thi', 'text', 'is', 'beautifulli', 'index']
```
Stemming provides the following benefits:  
- Reduced index size
- Increased Querying Speed
- Allows users to find documents without worrying about word forms

The following were the disadvantages of stemming:
- The stemming algorithm can sometimes incorrectly inflate words by removing suffixes
- Since the stemmed forms are often not proper words, so the index cannot be used as a dictionary    
  
The results of normal tokenization vs stemming analysis were calculated based on certain set queries. The table below shows that stemming greatly helps reduce the size of index. The runtime however, is faster for indexes that have not been stemmed particularly because not all versions of a words need to be searched. However, the trade off is not large and the efficiency of the former case is more desireable.  

**Table 2.1 Summary of stemming analysis**

| Index field          | Total index space with stemming | Total index space without stemming | Average query speed with stemming | Average query speed without stemming | Average number of query results with stemming | Average number of query results without stemming |
|----------------------|---------------------------------|------------------------------------|-----------------------------------|--------------------------------------|-----------------------------------------------|--------------------------------------------------|
| Overview             | 37683                           | 49938                              | 30.1025 ms                        | 22.5827 ms                           | 767                                           | 413                                              |
| Title                | 12585                           | 14401                              | 22.9966 ms                        | 19.0061 ms                           | 119                                           | 101                                              |
| Tagline              | 6288                            | 8122                               | 25.3580 ms                        | 24.0190 ms                           | 154                                           | 128                                              |
| Production companies | 9538                            | 10035                              | 28.4068 ms                        | 22.1769 ms                           | 722                                           | 718                                              |
| Genres               | 22                              | 22                                 | 44.924 ms                         | 50.3830 ms                           | 135                                           | 135                                              |

- _Basic indexing of document and variation of query_  
Since the timing for retrival of words from basic index is faster, another approach was tried that involved basic indexing of all the words but expansion of the user search query. This provided a middle path between index and user search in terms of timing. For example, 

| Query    | Type of indexing | Total results | Total time | Top results                                                                                                           |
|----------|------------------|---------------|------------|-----------------------------------------------------------------------------------------------------------------------|
| murdered | stemming         | 1235          | 39.20 ms   | The Mean Season   Strip Nude for Your Killer   Memories of Murder   Without Evidence   The Rockville Slayer           |
| murdered | variation        | 1154          | 79.90 ms   | The Mean Season,Strip Nude for Your Killer,Seven Murders for Scotland Yard,Memories of Murder,Murder in Coweta County |
| care     | stemming         | 214           | 41.31 ms   | Care Bears Movie II: A New Generation   The Other Day in Eden   America   Pauline & Paulette   RoboDoc                |
| care     | variation        | 229           | 55.07 ms   | Care Bears Movie II: A New Generation Pauline & Paulette   Anita   Bloody Reunion   Dr. Alemn                         |

After analysis, it was clear than the stemming analyser was faster for most query and gave nearly similar results. Thus, in the end the indexing was done with Stemming analysis.

### 2. Querying

The Querying is a simple user-input that returns the best matched results. To provide best user-experience, the following querying features were implemented:  

1. _Automatic spell-correction_: The user query undergoes automatic spell correction in case the query contains words not present in the reverse-index.  
[Future-Update-Under-Implementation] The query will also provide user interactivity to pick from a list of corrected spelling of misspelt words.  
2. _Query term highlighting_: [Under-construction] The returned result text contains the highlighted original query term(s) by making them bold to enhance user interaction.
3. _Query by different fields_: Currently, in order to query by different fields such as 'Title' or 'Overview', different radio button is required to be selected in the UI since each field is indexed seperately.
[Advanced] Improve the user search experience such that it is not required to chose the field. The following options are available in order to archieve this:-  
- Merge results from different searches of each field  
Pro's: Easy to implement  
Con's: Increases time, ranking on merging from different field difficult to pinpoint
- Make one index for all text fields instead of several
Pro's: Easy to implement
Con's: Possibly increase time due to increase in size of index


### 3. Ranking

The ranking of the documents is based on the `TF_IDF` values of both the query and the document terms. The simple formula that has been used is:  

`TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).`

`IDF(t) = log_e(Total number of documents / Number of documents with term t in it)`  

The choice trade-off was made between `BM25` and `TF_IDF` methods of scoring document relevance. However, `TF_IDF` was used in the end because of its does not calculate score simply based on the probabilistic occurance of a term in a document but also considers the frequency of a word in the entire document.  

### Question 2: Perform the following tasks:  

#### Build a simple Web interface for the search engine (e.g., Google)  
- [] To-be-filled by Noopur Jain   

#### A simple UI for crawling and incremental indexing of new data would be a bonus (but not compulsory)  
[To-do]  
#### Write five queries, get their results, and measure the speed of the querying  

| Query                           | Field searched | Total results | Total time | Top results                                                                                                                                    |
|---------------------------------|----------------|---------------|------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| murderous clowns                | overview       | 6             | 27.53 ms   | Fear of Clowns, Der Clown - Tag der Vergeltung, Clownhouse, Camp Blood 2, Satan's Storybook                                                        |
| love travel                     | overview       | 61            | 28.79 ms   | Kyun...! Ho Gaya Na, The Tiger and the Snow,  Ship of Fools, Transformations, Look at Me with Pornographic Eyes                                     |
| blood                           | tagline        | 53            | 30.93 ms   | Dillinger, Sleepers, Flaming Frontier, Straight to Hell, Bound by Honor                                                                            |
| when in Rome                    | title          | 5             | 23.08 ms   | Tony Rome, The Fall of Rome, The Hidden History of Rome, When in Rome Rome, Open City                                                             |
| criminal and horror and mystery | genres         | 40            | 344.47 ms  | `(Spell check)Did you mean: crime and horror and mystery` The Murders in the Rue, Morgue Blue Velvet, Close Your Eyes, Not Forgotten, The Seamstress |

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
