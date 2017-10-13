from scraper import PsychScraper, EventScraper, ValidationScraper, ScheduleScraper
from printer import PsychPrinter
import datetime

def run_psych():
    competition_name = input("Enter abbreviated competition name (e.g. NCR2017): ")

    start_time = datetime.datetime.now()
    done_str = "DONE"

    vscraper = ValidationScraper(competition_name)
    competition_valid = vscraper.check_competition_valid()
    if not competition_valid:
        print("ERROR: Competition specified either does not exist or is not listed on canadiancubing.com.")
        return

    # e.g. 2017-06-11-NCR2017-psych.txt
    now = datetime.datetime.now()
    file_name_segments = [str(now.year), str(now.month).zfill(2), str(now.day).zfill(2), 
            competition_name, "psych.txt"]
    output_file_name = "-".join(file_name_segments)

    print("Initializing scrapers and generator...", end="", flush=True)
    pscraper = PsychScraper(competition_name)
    escraper = EventScraper(competition_name)
    pprinter = PsychPrinter()
    print(done_str)

    print("Finding events for " + competition_name + "...", end="", flush=True)
    competition_events = escraper.scrape()
    print(done_str)

    for event in competition_events:
        print("Generating sheet for " + event + "...", end="", flush=True)
        event_psych = pscraper.scrape(event)
        pprinter.print_psych_to_file(event, event_psych, output_file_name)
        print(done_str)

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    minutes, seconds = divmod(duration.total_seconds(), 60)
    print("Psych sheet generated in " + str(round(minutes)) + " minutes and " + str(round(seconds)) + " seconds under name '" + output_file_name + "'.")


def run_scheda():
    competition_name = input("Enter a competition name in full (e.g. Newmarket Open 2017): ")
    competition_name = "".join(competition_name.split(" "))

    num_stations = int(input("Enter number of stations: "))

    start_time = datetime.datetime.now()
    done_str = "DONE"

    print("Initializing scrapers...", end="", flush=True)
    sscraper = ScheduleScraper(competition_name)
    print(done_str)

    print("Finding times for " + competition_name + "...", end="", flush=True)
    event_time_blocks = sscraper.scrape()
    print(done_str)

    for block in event_time_blocks:
        print(block["event_name"] + ": " + str(round(block["total_event_time"] / 1000 / 60 / num_stations)) + " minutes discarding " + str(block["num_DNFs"]) + " DNFs")

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    minutes, seconds = divmod(duration.total_seconds(), 60)
    print("Schedule analyzed in " + str(round(minutes)) + " minutes and " + str(round(seconds)) + " seconds")


def main():
    command = input("Enter a command [psych for psyche sheet/scheda for schedule analysis]: ")
    if command == "psych":
        run_psych()
    elif command == "scheda":
        run_scheda()
    else:
        print("Invalid command")
    

if __name__ == "__main__":
    main()
