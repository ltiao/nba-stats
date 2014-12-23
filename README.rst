=========
nba-stats
=========

First we set up our local development environment, along with a remote 
development environment, as well as a staging environment which will
closely resemble the basic production environment once we're ready to 
deploy - we don't want to nor do we need to be bogged down by the 
intricacies of deploying our application at this stage [1]_.

Since this is a small side project, we can only afford either the free 
tier or the cheapest available alternative with popular Platform as a 
Service (PaaS) hosting providers. While affordable, this also comes with 
the risks and uncertainties of the changes that vendors can make, such 
as crippling price increases, performance degradation, unacceptable 
terms of service changes, untenable service license agreements, sudden 
decreases in availability, or simply going out of business.

To avoid being locked in to a single host provider, a philosophy espoused
by most seasoned developers, we use Heroku for our development environment
and Digital Ocean for our production environment to ensure mobility and 
versatility and to avoid being forced into architectural decisions based 
on the needs of the hosting provider. 



.. [1] "Premature optimization is the root of all evil" - Donald Knuth