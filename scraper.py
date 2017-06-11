import requests
import sys
from lxml import etree
from ptime import Time

class HTMLScraper:
    def __init__(self):
        pass


    def scrape(self, site):
        """
        Scrapes the requested site and returns its text

        site : string - must be valid site
        """
        site_resp = requests.get(site)
        return site_resp.text



class PsychScraper:
    def __init__(self, competition):
        self.competition = competition

        self._htmlscraper = HTMLScraper() 
        self._wca_event_dict = { "2x2x2": "222", "3x3x3": "333", 
                "3x3x3 One-Handed": "333oh", "3x3x3 Blindfolded": "333bf",
                "4x4x4 Blindfolded": "444bf", "5x5x5 Blindfolded": "555bf",
                "3x3x3 Fewest Moves": "333fm", "3x3x3 With Feet": "333wf", "3x3x3 Multi-Blind": "333mbd",
                "4x4x4": "444", "5x5x5": "555", "6x6x6": "666", "7x7x7": "777",
                "Pyraminx": "pyram", "Skewb": "skewb", "Megaminx": "minx", "Square-1": "sq1",
                "Clock": "clock" }


    def _get_name(self, competitor):
        name = competitor.xpath("text()")[0].strip()
        return name


    def _get_average_time(self, event_block):
        event_average_block = event_block.xpath("td")[5]

        event_average_text = event_average_block.xpath("a/text()")[0].strip()
        if event_average_text == "":
            return None
        else:
            time = Time(event_average_text)
            return time

    def _get_single_time(self, event_block):
        event_single_block = event_block.xpath("td")[4]

        event_single_text = event_single_block.xpath("a/text()")[0].strip()
        if event_single_text == "":
            return None
        else:
            time = Time(event_single_text)
            return time

    def _get_time(self, competitor, event):
        wca_profile_id = competitor.xpath("@href")[0].split("=")[-1]
        wca_site_str = "https://www.worldcubeassociation.org/persons/" + wca_profile_id
        wca_scrape_result = self._htmlscraper.scrape(wca_site_str)
        wca_site_tree = etree.HTML(wca_scrape_result)

        event_block = None
        try:
            records_table = wca_site_tree.xpath("//div[@class='personal-records']//table")[0]
            event_id = self._wca_event_dict[event]
            event_block = records_table.xpath("//td[@class='event' and @data-event='" + event_id + "']/..")[0]
        except:
            return None, None

        event_average_text = self._get_average_time(event_block);
        event_single_text = self._get_single_time(event_block);

        if event_average_text is not None and not event.endswith("Blindfolded") and not event.endswith("Blind"):
            return event_average_text, False
        elif event_single_text is not None:
            return event_single_text, True
        else:
            return None, None
        

    def scrape(self, event):
        site_str = "http://www.canadiancubing.com/Event/" + self.competition + "/Competitors/" + event.replace(" ", "%20")

        scrape_result = self._htmlscraper.scrape(site_str)
        site_tree = etree.HTML(scrape_result)

        with_results_competitors_trees = site_tree.xpath("//table[@class='table table-hover table-striped table-bordered']//a")
        competitors = []

        for competitor in with_results_competitors_trees:
            competitor_name = self._get_name(competitor)
            competitor_time, use_single = self._get_time(competitor, event)
            if competitor_time is not None:
                competitors.append({ 'name': competitor_name, 'time': competitor_time, 'use_single': use_single })
        
        competitors = sorted(competitors, key = lambda competitor: competitor["time"].milliseconds)

        return competitors
