from easy_gtfs.objects.agency import Agency
from easy_gtfs.managers.gtfsmanager import GTFSManager
from easy_gtfs.managers.agencymanager import Agencies

ag = GTFSManager()
ag.load_folder("easy_gtfs/sample-feed.zip")

#am = Agencies()
#am.load_file("easy_gtfs/agency.txt")

#a = Agency(
    #agency_id="1234",
    #agency_name="test",
    #agency_email="123@gmail.com",
    #agency_url="https://1123.google.com",
    #agency_timezone="Berlin/Europe"
##)

#print(a)