class Time:
    def __init__(self, time):
        self.milliseconds = self._get_milliseconds(time)
        self.text = time

    def _get_milliseconds(self, time):
        total_milliseconds = 0

        hours = 0
        minutes = 0
        seconds = 0
        centiseconds = 0

        colon_temp = None
        dot_temp = None

        if time.find(":") != -1:
            colon_temp = time.split(":")
            if len(colon_temp) == 3:
                hours = int(colon_temp[0])
                minutes = int(colon_temp[1])
                dot_temp = colon_temp[-1].split(".")
            else:
                minutes = int(colon_temp[0])
                dot_temp = colon_temp[-1].split(".")

        if dot_temp is None:
            dot_temp = time.split(".")
            
        seconds = int(dot_temp[0])
        centiseconds = int(dot_temp[1])

        total_milliseconds = hours * 3600 * 1000 \
                + minutes * 60 * 1000 \
                + seconds * 1000 \
                + centiseconds * 10

        return total_milliseconds
