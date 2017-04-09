# Information Retrival Search Engine

## Quick-index to assignment questions
* [Why we chose to work on a movie database?](#overview)
* [Crawling the data](#1-crawling-the-data)
  * [Question 1](#question-1)
     * [How you crawled the corpus?](#question-11)
     * [what kind of information users would like to retreive?](#question-12)
     * [The numbers of records, words, and types (i.e., unique words) in the corpus](#question-13)
* [Indexing and Query analysis](#1-indexing)
  * [Standard indexing vs Stemming analysis vs Query variation](#2-indexing-and-querying)
  * [Modification on user query](#2-querying)
  * [Ranking](#3-ranking)
  * [Question 2](#question-2-perform-the-following-tasks)
     * [Build a simple web interface](#question-21)
     * [A simple UI for crawling and incremental indexing of new data](#question-22)
     * [Example of 5 queries](#question-23)
  * [Question 3](#question-3-explore-some-innovations-for-enhancing-the-indexing-and-ranking-explain-why-they-are-important-to-solve-specific-problems-illustrated-with-examples)
    * [Query variation](#enhancement-of-search-via-better-indexing)
    * [Recommendation system](#recommendation-system)
* [Classification](#3-classification)
  * [Question 4](#question-4)
    * [Motivate the choice of your classification approach in relation with the state of the art](#motivate-the-choice-of-your-classification-approach-in-relation-with-the-state-of-the-art)
    * [Discuss whether you had to pre-process data and why](#discuss-whether-you-had-to-pre-process-data-and-why)
    * [Build an evaluation dataset by manually labelling 10% of the collected data (at least 1,000 records) with an inter-annotator agreement of at least 80%](#build-an-evaluation-dataset-by-manually-labelling-10-of-the-collected-data-at-least-1000-records-with-an-inter-annotator-agreement-of-at-least-80)
    * [Provide evaluation metrics such as precision, recall, and F-measure and discuss results](#provide-evaluation-metrics-such-as-precision-recall-and-f-measure-and-discuss-results)
    * [Discuss performance metrics, e.g., records classified per second, and scalability of the system](#discuss-performance-metrics-eg-records-classified-per-second-and-scalability-of-the-system)
    * [A simple UI for visualizing classified data would be a bonus (but not compulsory)](#a-simple-ui-for-visualizing-classified-data-would-be-a-bonus-but-not-compulsory)
  * [Discussion of Results](#discussion-of-results)
    * [Evaluation Parameters](#evaluation-parameters)
    * [Observations and Inference](#observations-and-inference)
  * [Question 5](#question-5)
    * [Explore some innovations for enhancing classification](#explore-some-innovations-for-enhancing-classification)
   
  

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
The Movie Db (TMDB) api was used to extract the corpus and relevant information about the movies. The crawled and extracted corpus was stored in the formed of json-like text files. A single document consists of a text file with a single movie record containing the detailed plot information. During crawling, it was observed that ceratin records from the api call lacked plot information. We ignored such records during crawling as they were insignificant to the kind of information retreival system required. Each unique text fil.e is saved with a unique id from 1 to greater than 20,000. The unique identifier for each record is the 'imdb_id' as well as the text file number in our case. While the api returns a lot of information, we only store the following meta-data for each record:
 
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

The Movie Database(TMDb) API v3 was used to retrieve movie information in a systemic way via looping over TMDB ids in the following manner:
```python
import tmdbsimple as tmdb
tmdb.apikey=‘your API key’
movie=tmdb.Movies(1) #returns movie info of movie with tmdb id=1
```
Once an instance of an object type is created, we can call other methods on the instance to access its attributes.  
```python
#return movie’s title
movie.title
#get all info
response=movie.info()
```

We looped over 30,000 movie id’s however it was found that only 20390 of them were valid and only stored the information of these movies.
    

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

| Statistic                     | Count   |
|-------------------------------|---------|
| Number of documents           | 20390   |
| Total words                   | 1404539 |
| Average # words in a document | 68.8837 |
| Total unique words            | 177518  |



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

1. _Automatic spell-correction_: The user query undergoes automatic spell correction in case the query contains words not present in the reverse-index. The suggested spelling is presented to the user, where he can click t accept the suggestion and a new search takes place for the accepted suggestions.    
2. _Query by multiple fields_: Currently, in order to query by different fields such as 'Title' or 'Overview', different radio button is required to be selected in the UI since each field is indexed seperately.
3. _Simple boolean operation on user query_: The user can perform boolean queries such as 'eat - food' or 'sing + dance' to perform search on the data that contains eat but not food, and contains both sing and dance etc.
4. _Refining of queries_: Meta-data such as year of release and review are used as filter to provide user ease of narrowing down their results.
NOTE: The filtering is not done via javascript but refining search results through our index.
5. _Dynamic Crawling_: Covered under Question 2.2



### 3. Ranking

The ranking of the documents is based on the `TF_IDF` values of both the query and the document terms. The simple formula that has been used is:  

`TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).`

`IDF(t) = log_e(Total number of documents / Number of documents with term t in it)`  

The choice trade-off was made between `BM25` and `TF_IDF` methods of scoring document relevance. However, `TF_IDF` was used in the end because of its does not calculate score simply based on the probabilistic occurance of a term in a document but also considers the frequency of a word in the entire document.  

### Question 2: Perform the following tasks:  

#### Question 2.1  
#### Build a simple Web interface for the search engine 
The movie search engine allows users to select whether they want to search from movie titles, movie overviews or both. 
The time taken to find the best results, ranked according to the tf-idf score, and the number of results is displayed along with the top results. These can be further filtered by providing a range of release year and rating of the movie. All the results are paginated and displayed with their poster, overview and title and one page displays 5 movies. The effect of filtering using the release year and rating can be seen by checkng the number of results found. 
![Ui-image](https://drive.google.com/file/d/0BzkR3JVfK4-oQlpXS21MdHdxdEk)

#### Question 2.2
#### A simple UI for crawling and incremental indexing of new data would be a bonus (but not compulsory)  
Incremental crawling and indexing of data is possible on the basis of query and date. If a user search fails or is not found, new data is automatically crawled and if the search query exists in the results it is displayed. The crawling can be done by both query or date, but we chose crawl by date as the default implementation. The reason for this choice were:  
- The api used to retrieve data can only respond by querying of title with limited hits. In case the use makes a query for the overview, the api cannot return the data. Manual crawling of html pages was considered to eliminate this restriction, however the number of movie records were abudant and this was time consuming.
- Thus, the data is considered to be updated if all records from last fetch to the current date have been fetched. Thus we crawl dynamically by only considering the dates between previous crawl and current date. This considerably reduces the data to be crawled. We then fetch the records and add them to the current index. 
_(NOTE: Ideally all records should be added but sometimes, the records fetched fetched are >100K, hence, we only store a sample in our index and update it for demonstration purpose of this project)_

#### Question 2.3
#### Write five queries, get their results, and measure the speed of the querying  

| Query                           | Field searched | Total results | Total time | Top results                                                                                                                                    |
|---------------------------------|----------------|---------------|------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| A villager prays for his grandson              | overview       | 1             | 0.06s   | Promise me this                                                        |
| ghost haunting a house                     | overview, title       | 14           | 0.035s   | The Ghost of Angela Web, Thirteen Erotic Ghosts, Death of a ghost hunter                                     |
| boy + girl - love                           | overview, title        | 71            | 0.063s   | Puberty Blues, The Pirate Movie, Take a Chance, Summer Camp Nightmare                                                                           |
| serial killer and a detective                   | overview, title          | 31             | 0.034s   | Copy cat, Frankenstein, 10 to Midnight, Detective Story                                                             |
| the princess and prince | overview, title         | 25            | 0.04 sec  | Sinbad and the Eye of the Tiger, The Adventures of Prince Achmed, The Wild Swans |

### Question 3: Explore some innovations for enhancing the indexing and ranking. Explain why they are important to solve specific problems, illustrated with examples. 

#### Enhancement of search via better indexing
##### Query variation 
_Discussed under Indexing and Querying_   

##### N-grams

The stemming analysis was changed to N-grams, to test for more robust searches ad phrases. The previous queries show more results in almost the same time. After hit and trial, with minsize=2 and maxsize=4 was chosen.

| Query                             | Field searched  | Total results | Total time | Top results                                                                                                   |
|-----------------------------------|-----------------|---------------|------------|---------------------------------------------------------------------------------------------------------------|
| A villager prays for his grandson | overview        | 1             | 0.082s     | Promise me this                                                                                               |
| ghost haunting a house            | overview, title | 17            | 0.035s     | The Ghost of Angela Web, Thirteen Erotic Ghosts, Death of a ghost hunter                                      |
| boy + girl - love                 | overview, title | 97            | 0.063s     | Puberty Blues, The Pirate Movie, Take a Chance, Summer Camp Nightmare                                         |
| serial killer and a detective     | overview, title | 31            | 0.034s     | Frankenstein, 10 to Midnight, Detective Story                                                                 |
| the princess and prince           | overview, title | 141           | 0.04 sec   | Princess protection program, Sinbad and the Eye of the Tiger, The Adventures of Prince Achmed, The Wild Swans |

It is seen that in most cases a textual query longer than 5-6 words usually yields no results with our earlier analyzer. However, after implemntation of the N-grams analyzer the search becomes more responsive to longer user queries.

##### Taking a closer look 

- Example 1
`a ghost in the shell` returns 7 records with N-grams while previous analyser returns only 5. The two different records were: Frankenstein and Edison's Frankenstein where N-grams was catching the name of the author 'Shelley'. Needless to say, it was also the lowest ranked result. 
- Example 2
`Eat` returned 3797 records with N-grams. However, it included terms like 'Death, 'Kreator' etc. which were not the focus of the user's search. The normal indexer returned only 19 relevsnt records.

Thus, we conclude that N-grams is very powerful in detecting terms similar to user queries, particularly helpful in running longer queries.However it may return misleading results for short, one-word queries as can be seen the the above examples.

#### Recommendation system


We built a recommendation system based on the tf-idf matching values between a document and the others instead of user query to get a recommendation system. The recommendation system was explored in two parts: Raw recommendation system and through bag of words classification model in Whoosh.

We tried to build a recommendation system that would recommend movies similar to a given movie based on the similarity of movie plots.

We first pre-processed each movie plot by removing punctuation and stopwords, and then extracted the noun phrases from each document( to remove terms like according etc.). Each document was then converted to a tf-idf vector and stored in a dictionary along with the document id. 

The cosine similarity for each pair of document ids was then calculated and put into a new dictionary. We then implemented a function that went through each pair of id's for a given id to find the document with the most similar plot.

However, we noticed that the time for creating the cosine similarity matrix was extremely long and did not support our additional feature of incremental crawling, based on which we used the bag of words classification model in Whoosh.

![RecommendationSystem](https://drive.google.com/file/d/0BzkR3JVfK4-oTmY4WktFZmFiODQ)


## 3. Classification
Classification is the process of determining the sub-category to which a new record/observation belongs. In machine learning, classification comes under supervised learning, where a training set of records with correctly identified categories is available. The classification of a new record is done based on this training set.
Both probabilistic and non-probabilistic classifiers were tested. The simple classifiers used include SVM, the Naïve Bayes classifiers and Logistic Regression. Some ensemble classifiers such as Bagging, Voting and the Random Forrest classifiers, were also used.
Three genres (categories) – horror, romance and crime were chosen, and a training set of 1500 movie records (500 of each genre) was used as the basis for classification. Around thousand movie records which were manually labelled by the team members, were used to test each classifier.

### Question 4: Perform the following tasks:
#### Motivate the choice of your classification approach in relation with the state of the art

The classification approach chosen was the machine learning based approach. This approach was preferred over rule-based or knowledge based classification because, these approaches are usually adopted when there is scarcity of data, i.e., there isn't enough manually labelled or supervised data available to train a machine-learning based approach. Due to the availability of a large training set with enough labelled data, a statistical machine learning approach is expected to perform better.

From the results obtained, it was observed that the Logistic Regression and the Multinomial Naïve Bayes classifiers outperformed the others simple classifiers in terms of accuracy. The Voting ensemble classifier was the most accurate among all the classifiers.

The best performer was the Multinomial Naïve Bayes classifier. It was almost as accurate as the voting classifier, but much faster.

#### Discuss whether you had to pre-process data and why

The overviews of the movie records were used as the training data. The text in the overviews were pre-processed by converting them to lower case, lemmatizing them and removing the stop words. This was done to avoid the inclusion of irrelevant words in the training set and to increase the speed of training. It was observed that this also improved the accuracy of classification. 

#### Build an evaluation dataset by manually labelling 10% of the collected data (at least 1,000 records) with an inter-annotator agreement of at least 80%

A total of 1000 movie records were used to test the classifiers, and these records were manually labelled. Refer to the attached file test_data.csv.

#### Provide evaluation metrics such as precision, recall, and F-measure and discuss results
![ClassificationResults](https://drive.google.com/file/d/0BzkR3JVfK4-oQnNta0ZqNVBNNTQ)

#### Discuss performance metrics, e.g., records classified per second, and scalability of the system

The confusion matrix for the Multinomial Naïve Bayes classifier is shown below. The rows indicate the actual genre of the movie record and the columns are the genres into which they are classified.

| Confusion Matrix | Horror | Romance | Crime |
|------------------|--------|---------|-------|
| Horror	          |   280	 |    22	  |   31  |
| Romance          |   28	  |   276	  |   29  |
| Crime	           |   17	  |    16	  |  301  |

When it came to the number of records classified per second, the ensemble classifiers were much slower compared to the simple classifiers. Among the simple classifier, the non-probabilistic classifier – SVM was much slower compared to the probabilistic classifiers.
SVM averaged 19 records per second, while the probabilistic classifiers averaged around 1750 records per second. The voting ensemble classifier averaged around 15 records per second.

#### A simple UI for visualizing classified data would be a bonus (but not compulsory)

A UI was designed to enable the user to key-in a movie plot. The genre into which the movie is classified, is displayed on the web page.

![Horror](https://drive.google.com/file/d/0BzkR3JVfK4-oRkVwdkJsUFlUOGM)
                  Classification of the plot of the horror movie - The Ring


![Romance](https://drive.google.com/file/d/0BzkR3JVfK4-ocVFzS0QzUTRmdmc)
                      Classification of the plot of the crime movie – Se7en


![Crime](https://drive.google.com/file/d/0BzkR3JVfK4-oYXRGektNM1VLZVE)
                  Classification of the plot of the romance movie – The Notebook

### Discussion of Results

#### Evaluation Parameters

In order to evaluate the performance of the different Machine Learning Classifiers, the following scores were calculated:
1.	Precision: Ratio of true positives to all positive results (including true and false positives)
2.	Recall: Proportion of correctly identified positives 
3.	Accuracy: Ratio of true (positive and negative) to the whole test dataset
4.	F(1) Score: Harmonic Mean of precision and recall: 2*Precision*Recall/(Precision+Recall)
5.	F(W) Score: F(1) score with more weightage to Precision than Recall

#### Observations and Inference

Bayes Classifiers give moderate to good performance. This is due to the fact that Bayes Classifiers are based on the assumption that the documents in the datasets are independent. This assumption is satisfied to a large extend as movie overviews are generally independent of each other. Multinomial NB with tf-idf vectorization gives the best performance in terms of accuracy (Accuracy: 85.70%, F1: 85.84%, FW: 85.75%) compared to all other classifiers as it is based on multinomial distribution and works well for data which can be converted into frequencies or count, with the count of words in documents being the case for this evaluation. Bernoulli performs moderately as it only uses binary vectors representing occurrence of words. Gaussian NB tends to be least accurate as it is based on the premise that the underlying dataset has a continuous normal distribution, which is not the case for the words in documents

For SVM, the performance is reasonably good (Count Vectorizer: 83.7% accuracy and F1 Score, tfidf: 84.8% accuracy and F1 Score). As the documents are multiple dimensional, SVM is effective as SVM plots each document as a point in n-dimensional space as Support Vectors.

For Logistic Regression, as it is uses log functions on binary values to predict the probability of occurrence of words, it gives a good performance as the movie reviews are independent.

Random forest and Bagging also gave decent results, however Gradient performed poorly.

Most of the models tend to perform better with tf-idf vectorizers. Since tf-idf vectorization normalizes the results based of rarity or infrequency of the words, by giving such rare words more weightage, it is able to perform well as different movies overviews have specific key words which are quite specific to its genre

As expected, our enhanced of Ensemble (Voting) perform the best out of all the models. However, the performance improvement is only marginal based on f scores and accuracy which may be due to the averaging out effect. First the classifier with equal weights and then with varying weights. Equal weighted Voting with Count Vectorizer performed the best (Accuracy: 87.00%, F1: 87.03%, FW: 87.01%) out of the lot.

Even though Voting with Count Vectorizer performed the best, it takes significant time to classify (greater than 1s), which would not be appropriate for online real-time classification. Hence we decided to choose the Multinomial NB model as it gives the best individual model performance (second best overall) and significantly less execution time (~0.1 s)

### Question 5: Explore some innovations for enhancing classification. Explain why they are important to solvespecific problems, illustrated with examples.

To enhance classification, ensemble classifiers such as Random Forrest, Bagging, Gradient Boosting, and Voting classifiers were used. From the results, it was observed that the Random Forrest and the Bagging classifiers performed on par with the simple classifiers – Logistic Regression and Multinomial NB, in terms of accuracy. The voting classifier had the highest accuracy among all the classifiers. However, the ensemble classifiers were found to be much slower compared to the simple classifiers. This is because, ensemble classifiers combine the predictions of several base estimators built with a given learning algorithm in order to improve generalizability / robustness compared to a single estimator.




Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.

