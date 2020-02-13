# Yak Shop
We want to develop a Yak online shop for a Yak shepherd living on the tundra herding a group of Yaks. we want to sell Yak wool and milk. 
We have to know some facts about Yak. Yaks like humans also age, and with age they give less milk until they finally die of old age. 
Contrary to humans, a standard Yak year consists of 100 days. The shepherd currently has Yaks who all stem from the “LabYaks” tribe. 
This tribe is known for its consistency in wool quality, milk taste and production rate of said goods. The shepherd gave us the
following facts about LabYaks:
*  Each day a LabYak produces 50-D*0.03 liters of milk (D =age in days).
*  At most every 8+D*0.01 days you can again shave a LabYak (D =age in days).
*  A yak can be first shaven when he is 1 year.
*  A LabYak dies the day he turns 10.

# Assumptions
*  The moment we open up the YakShop webshop will be day 0, and all yaks are eligible to be shaven, as the two of you spent quite 
a lot of time setting up this shop and the shepherd wasn’t able to attend much to his herd.
*  Each morning the shepherd milks and shaves his yaks. Yaks which aren’t eligible to be shaven on the exact day, cannot be shaved today. 
Example: a yak who started out on day 0 as 4 years, can be shaven again during day 13.
*  When querying your app and placing orders, the elapsed time in days (T) is used. A value of for instance 13 means that day 12 has elapsed 
and we’re at midnight day 13.

# User Stories
*   As a Yak Shepherd, I want to be able to read in a XML file that contains data about my herd so that I can query it.
*   As a Yak Shepherd I want to be able to load a new Herd into my webshop using an Http ReST service so that I can open my webshop
*   As a Yak Shepherd I want to be able to query my herd and my current stock using Http ReST services which output JSON data
*   As a Yak Shepherd I want my customers to be able to buy from my stock using my Http ReST services.
