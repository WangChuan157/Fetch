import leancloud
from lolba.clim import Fetcher

fetcher = Fetcher()
fetcher.fetch_douyu()
for host in fetcher.hosts:
    host.save()