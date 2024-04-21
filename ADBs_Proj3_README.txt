NAME: Bevis Cheung (mc5312), Sebastian Hereu (smh2278)
________________


Files|
(1) README.txt - the current file


(2) main.py - contains the logic for generating association rules from INTREGRATED-DATASET.csv
(3) INTEGRATED-DATASET.csv - to be used with (2), the file from which association rules are mined
(4) example-run.txt - example run of main.py on INTEGRATED-DATASET.csv
________________


External Libraries|
(1) sys, csv, itertools - standard library
________________


How to Run Program|
python3 main.py INTEGRATED-DATASET.csv <min_sup> <min_conf>
Note that the parameters are given in the project 3 specification. <min_sup> and <min_conf> are both values between 0 and 1
For example, to run the Association Rule Mining Algorithm on INTEGRATED-DATASET.csv with minimum support 0.01 and minimum confidence 0.5, run:
python3 main.py INTEGRATED-DATASET.csv 0.01 0.5
________________


General Description|
For our project, we chose to use the NYPD Hate Crimes dataset, available at https://data.cityofnewyork.us/Public-Safety/NYPD-Hate-Crimes/bqiq-cu78/about_data. This dataset contains data about confirmed hate crime incidents in NYC. The original dataset has 2,725 rows and 14 columns. Each row represents a hate crime incident and contains such information as the area in which the crime occurred,  the group targeted, and the type of crime. 


To map the hate crime dataset to INTEGRATED-DATASET.csv, we first defined a notion of transactions and items. Using the Pandas library to manipulate the Hate Crime csv file, we defined a new column called ‘transaction_id’, which is the concatenation of the string representations for ‘Complaint Year Number’, ‘Month Number’, and ‘Complaint Precinct Code’. For the items, we used the columns ‘Offense Description’, which specifies the type of crime committed, and ‘Bias Motive Description’, which specifies the targeted group. We grouped this table by ‘transaction_id’ and defined the row corresponding to each transaction as all unique values for ‘Offense Description’ and ‘Bias Motive Description’. This final table is the INTEGRATED-DATASET.csv file included with the submission. 


Our choice of INTEGRATED-DATASET is compelling as it delves into what has unfortunately become a major issue, hate crimes in NYC. Bad actors, whether that be individuals or entities, target specific groups with violence and intimidation, looking to instill fear in that group and incite disorder. We hope that we can extract the types of crimes that tend to be perpetrated against certain groups so that law enforcement can better allocate resources for fighting such heinous acts.


All of the logic for parsing the INTEGRATED-DATASET.csv file and generating association rules is present in main.py. The main function calls three functions: load_dataset(), run_apriori(), and output_result(). 


load_dataset() parses in the INTEGRATED-DATASET.csv, reading it the global ‘transactions’ variable. 


run_apriori() is responsible for running the apriori algorithm. The function has a main outer loop that runs for as long as at least one item set was generated in the last iteration. In each iteration of the loop, apriori_gen() is called to obtain the candidate itemsets of size k. Like described in class, size k candidate sets are generated from the sets of size k-1. After these initial candidates are obtained, we run a pruning step in which we eliminate those itemsets containing subsets that are infrequent. This extra pruning step ensures that only potential candidates are retained.


Finally, main calls output_result(), which is responsible for outputting the itemsets meeting the minimum support threshold and the association rules that meet the minimum confidence. 


Now, we discuss a compelling sample run of our program. Consider the sample run,
‘python3 main.py INTEGRATED-DATASET.csv 0.01 0.5’ 

The output of that run is included in example-run.txt. As discussed earlier, hate crime in NYC is a large issue, and cases have been on rise in the past couple of years. For example, a rise in anti-Asian hate crime occurred during the  COVID 19 pandemic and there is currently a rise in anti-Jewish and anti-Muslim crime precipitated by the conflict in the Middle East. We believe that our program uncovered interesting and actionable association rules between certain groups and those crimes committed against them. For example, we uncovered the relation, [ANTI_CATHOLIC] => [CRIMINAL_MISCHIEF_RELATED_OF]. With this association rule, law enforcement may be able to find a connection between different criminal mischief offenses and anti-Catholic motivation. Often, it is difficult for law enforcement to relate isolated incidents to a larger trend of hate crime. This dataset may be an aid to find connections between crime and targeted-groups, so that resources may be allocated more efficiently to protect members of the affected group. Part of being a New Yorker is being a member of a diverse community of individuals from different backgrounds and creeds, and intimidation of any one group has no place in NYC!