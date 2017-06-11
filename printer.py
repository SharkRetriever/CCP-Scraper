from unicodedata import normalize

class PsychPrinter:
    def __init__(self):
        self._NUM_SPACES = 45
        pass


    def _get_spacing(self, rank, name, time):
        return " " * (self._NUM_SPACES \
                - len(rank) - len(normalize('NFC', name)) - len(time.text))


    def _generate_print(self, event, psych):
        generated = "EVENT: " + event + "\n"

        for i, competitor in enumerate(psych):
            rank = str(i + 1)
            name = competitor["name"]
            time = competitor["time"]
            use_single = competitor["use_single"]
            use_single_suffix = " (s)" if use_single else ""
            spacing = self._get_spacing(rank, name, time)
            generated += rank + ". " + name + spacing + time.text + use_single_suffix + "\n"

        generated += "\n"
        return generated


    def print_psych(self, event, psych):
        generated = self._generate_print(event, psych)
        print(generated)


    def print_psych_to_file(self, event, psych, file_name):
        generated = self._generate_print(event, psych)
        with open(file_name, "a") as f:
            f.write(generated)


