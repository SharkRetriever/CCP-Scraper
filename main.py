from scraper import PsychScraper, EventScraper
from printer import PsychPrinter

def main():
    competition_name = "NMO2017"
    pscraper = PsychScraper(competition_name)
    escraper = EventScraper(competition_name)
    pprinter = PsychPrinter()

    competition_events = escraper.scrape()

    for event in competition_events:
        event_psych = pscraper.scrape(event)
        pprinter.print_psych(event, event_psych)


if __name__ == "__main__":
    main()
