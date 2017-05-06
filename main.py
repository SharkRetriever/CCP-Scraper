from scraper import PsychScraper
from printer import PsychPrinter


def main():
    competition_name = "NCR2017"
    competition_events = ["2x2x2", "3x3x3", "3x3x3 One-Handed", 
            "3x3x3 Blindfolded", "4x4x4", 
            "Pyraminx", "Skewb"]

    pscraper = PsychScraper(competition_name)
    pprinter = PsychPrinter()
    for event in competition_events:
        event_psych = pscraper.scrape(event)
        pprinter.print_psych(event, event_psych)


if __name__ == "__main__":
    main()
