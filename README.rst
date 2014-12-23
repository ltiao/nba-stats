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

Since the Heroku Postgres Hobby Dev plan has a row limit of 10,000, it
will not be useful for anything beside a basic remote development server.
On the other hand, Digital Ocean does not pose limitations of this kind,
so we can use it for our staging / demo environment. 

Before moving on, let's set up the local development environment.

+++++++++++++++++++++++
Development Environment
+++++++++++++++++++++++

Note: These steps were performed on Mac OS X 10.10.1 (Yosemite)

1.  First, ensure the latest version of Python is installed exactly
    according to this http://docs.python-guide.org/en/latest/starting/install/osx/ 
    so ``setuptools`` and ``pip`` are installed (you'll 
    need to install GCC, Homebrew). 
2.  Next, install ``virtualenv`` and ``virtualenvwrapper``::

      $ pip install virtualenv virtualenvwrapper

    You will need to add a few lines to the shell startup file to install
    and configure ``virtualenvwrapper``. Follow http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file 
    for more information.
3.  fef 

.. [1] "Premature optimization is the root of all evil" - Donald Knuth