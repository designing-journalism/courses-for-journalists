# Designing Journalism

repo containing (for now) an rss file containing info about AI courses fit for journalists. 


# This branch will be about creating a conversational system (usin agents?) with (probably the GToolkit):


## Why Conversational? 

Simpler to create? (well, we also develop a 'traditional' website, so simpler does not mean 'less work' in this case, it's more like looking at what the alternatives are)

## Why Agents?

That's just a brainwave i had: experimented with it before, and suddenly thought it could be very nice to create a prototype for the RPO course RecSys that works with agents. 

## Why Glamorous Toolkit?

It's one of my favorite tools! Furthermore (for now) it would mean I can create the chat  system locally (hopefully simpler at first), while also experimenting with something that i can easily let other people test (locally at first). 



## Installation

```st
Metacello new
	repository: 'github://designing-journalism/courses-for-journalists:gt-conversationator/';
	baseline: 'GitCoursesForJournalists';
	load
```
