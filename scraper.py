import requests
import sys
import concurrent.futures
from lxml import etree
from ptime import Time
from cache import Cache
from functools import partial

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
        self._cache = Cache()
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

        wca_site_tree = self._cache.get_competitor_page_tree(wca_profile_id)

        if wca_site_tree is None:
            wca_scrape_result = self._htmlscraper.scrape(wca_site_str)
            wca_site_tree = etree.HTML(wca_scrape_result)
            self._cache.add_competitor_page_tree(wca_profile_id, wca_site_tree)

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
        

    def _get_data(self, competitor, event):
        competitor_time, use_single = self._get_time(competitor, event)
        if competitor_time is None:
            return None, None, None

        competitor_name = self._get_name(competitor)
        return competitor_name, competitor_time, use_single


    def scrape(self, event):
        site_str = "http://www.canadiancubing.com/Event/" + self.competition + "/Competitors/" + event.replace(" ", "%20")

        scrape_result = self._htmlscraper.scrape(site_str)
        site_tree = etree.HTML(scrape_result)

        with_results_competitors_trees = site_tree.xpath("//table[@class='table table-hover table-striped table-bordered']//a")
        competitors = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for competitor_name, competitor_time, use_single in executor.map(partial(self._get_data, event=event), with_results_competitors_trees, chunksize=10):
                if competitor_time is not None:
                    competitors.append({ 'name': competitor_name, 'time': competitor_time, 'use_single': use_single })
        
        competitors = sorted(competitors, key = lambda competitor: competitor["time"].milliseconds)

        return competitors


class ScheduleScraper:
    def __init__(self, competition):
        self.competition = competition
        self._htmlscraper = HTMLScraper()


    # return total_time in milliseconds followed by number of DNFs
    def _get_times_total(self, event_table):
        total_time = 0
        total_number_dnfs = 0
        max_solves_allowed_string = event_table.xpath("thead/tr/th[@class='solves']/@colspan")[0]
        max_solves_allowed = int(max_solves_allowed_string)

        for row in event_table.xpath("tbody/tr"):
            num_dnfs = 0
            total_row_time = 0
            columns = row.xpath("td")
            num_columns = len(columns)
            time_columns = [column.xpath("text()") for column in columns[-(max_solves_allowed + 1): -1]]

            for time in time_columns:
                if time is None or len(time) == 0:
                    continue
                time = time[0].strip()
                if time == "":
                    continue
                if time[0] == "(":
                    time = time[1:-1]
                if time != "DNF" and time != "DNS":
                    parsed_time = Time(time) 
                    total_row_time += parsed_time.milliseconds
                elif time == "DNF":
                    total_number_dnfs += 1

            total_time += total_row_time

        return (total_time, total_number_dnfs)


    def scrape(self):
        site_str = "http://www.worldcubeassociation.org/competitions/" + self.competition + "/results/all"

        scrape_result = self._htmlscraper.scrape(site_str)
        site_tree = etree.HTML(scrape_result)

        event_name_paths = site_tree.xpath("//h3/span")
        event_names = [x.xpath("text()")[0].strip() for x in event_name_paths]

        event_table_paths = site_tree.xpath("//div[@class='table-responsive']/table")

        event_name_time_pairs = []

        for name, event_table in zip(event_names, event_table_paths):
            estimated_total_time, number_DNFs = self._get_times_total(event_table)
            event_name_time_pairs.append({"event_name": name, "total_event_time": estimated_total_time, "num_DNFs": number_DNFs })
               
        return event_name_time_pairs


class EventScraper:
    def __init__(self, competition):
        self.competition = competition
        self._htmlscraper = HTMLScraper()


    def scrape(self):
        site_str = "http://www.canadiancubing.com/Event/" + self.competition

        scrape_result = self._htmlscraper.scrape(site_str)
        site_tree = etree.HTML(scrape_result)

        events_list = site_tree.xpath("//h2[@id='events']/following-sibling::div/ul/li")
        events = [x.xpath("text()")[0].strip() for x in events_list]
        return events



class ValidationScraper:
    def __init__(self, competition):
        self.competition = competition
        self._htmlscraper = HTMLScraper()


    def check_competition_valid(self):
        site_str = "http://www.canadiancubing.com/Event/" + self.competition

        try:
            scrape_result = self._htmlscraper.scrape(site_str)
            site_tree = etree.HTML(scrape_result)
            banner = site_tree.xpath("//div[@id='layout-banner']/h4")[0]
            return True
        except:
            return False

