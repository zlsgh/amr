Automatic Mail Reply (AMR)
=============
Responding to email is a time-consuming task that is a requirement for most professions. Many people find themselves answering the same questions over and over, repeatedly replying with answers they have written previously either in whole or in part. This tool, called Automatic Mail Reply (AMR), is implemented to help with repeated email response creation. The system uses past email interactions and, through unsupervised statistical learning, attempts to recover relevant information to give to the user to assist in writing their reply. The statistical learning models, term frequency - inverse document frequency (tf-idf), Latent Semantic Analysis (LSA), and Latent Dirichlet Allocation (LDA) are used for this email document retrieval and similarity matching.

Dependencies
=============
In order to use AMR, you will need the following Python libraries:

* NLTK
* GenSim
* SciKit-Learn
* Numpy
* Scipy

Instructions
=============
1. Run main.py to get started and set up the keywords text for the archive of emails. 
1. Once this is completed you can run ProcessEmail.py to have amr continuously check for a new email. When a new one comes in, it will send you the best possible match for that message!

Background and Further Reading
=============
This system was developed as my thesis for my master's degree in computer science from the University of Maine. If you would like to read my full thesis you will be able to find it on the [University of Maine's library page here](https://digitalcommons.library.umaine.edu/etd/2379/).

Disclaimer
=============
This project does not guarantee anything. Use at your own risk.
