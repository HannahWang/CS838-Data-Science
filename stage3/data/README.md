## Tables

	A: 3188 tuples (restaurants information from Yelp in Los Angeles)
	B: 3120 tuples (restaurants information from Tripadvisor in Los Angeles)
	C: 1745 tuples (entity pairs after blocking step)
	S: 500 tuples (sampled from C; labeled data in S_labeled)
	I: 250 tuples (training set)
	J: 250 tuples (testing set)

## Attributes

	### In A and B
	  * id [num]
	  * name [text]
	  * Category_1 [text]
	  * Category_2 [text]
	  * Address [text]
	  * City [text]
	  * Zipcode [5-digit]
	  * Phone [10-digit]
	  * Price [number of dollar signs]
	  * Rating [1 to 5, allow half]
	  * Review_count [number]
	  * A set of attributes for open hours
	  * hours_day_<open/close>: [HHMM] in 24 hour format
		  - Examples:
		    + hours_sun_open = 1100
		    + hours_sun_close = 200


