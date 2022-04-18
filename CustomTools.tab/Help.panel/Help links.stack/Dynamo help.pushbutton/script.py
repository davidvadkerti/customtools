"""Opens the dynamo help web page."""
from pyrevit import script


__context__ = 'zero-doc'


url = 'http://dynamohelp.atwebpages.com'
script.open_url(url)
