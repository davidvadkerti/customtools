"""Opens webapp for calculation of elevation of Topography points."""

from pyrevit import script

__context__ = 'zero-doc'


url = 'http://pxlsjpg.atwebpages.com/topography/topography_en.html'
script.open_url(url)
