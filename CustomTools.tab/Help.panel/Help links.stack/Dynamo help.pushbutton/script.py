"""Opens the GFI wiki dynamo help article."""
from pyrevit import script


__context__ = 'zero-doc'


url = 'http://dynamohelp.atwebpages.com'
script.open_url(url)
