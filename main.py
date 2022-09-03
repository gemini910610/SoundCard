import matplotlib.pyplot as pyplot
import soundcard
import numpy

class SoundCard:
    def __init__(self):
        self.__speaker = soundcard.default_speaker()
        self.__microphone = soundcard.default_microphone()
        self.__sample_rate = 44100
        self.__channels = 1
    
    def set_speaker(self, speaker_index: int):
        '''
        [parameter]
        speaker_index: index of speaker\n
        * `use all_speakers()` to check speakers
        '''
        self.__speaker = soundcard.all_speakers()[speaker_index]
    def set_microphone(self, microphone_index: int, include_loopback: bool = False):
        '''
        [parameter]
        microphone_index: index of microphone
        include_loopback: whether include loopback (virtual microphone which record output of speaker)\n
        * use `all_microphone(include_loopback)` to check microphones
        '''
        self.__microphone = soundcard.all_microphones(include_loopback)[microphone_index]
    
    def record_fft(self) -> numpy.ndarray:
        '''
        record and convert into 10 octave bands, and normalize to 0 ~ 100
        '''
        CHUNK = 1024
        data = self.record(CHUNK / self.sample_rate).reshape(CHUNK)
        fft_data = numpy.abs(numpy.fft.rfft(data)[:-1])
        
        # 1 octave band
        # fft_data[1] = 1 * sample_rate / CHUNK = 1 * 44100 / 1024 = 43 Hz
        # fft_data[511] = 511 * 44100 / 1024 = 22000 Hz
        bands = numpy.array([             #     range      central frequency
            fft_data[1],                  #    22 ~ 44     31.5
            fft_data[2],                  #    44 ~ 88     63
            numpy.sum(fft_data[3:5]),     #    88 ~ 177    125
            numpy.sum(fft_data[5:9]),     #   177 ~ 355    250
            numpy.sum(fft_data[9:18]),    #   355 ~ 710    500
            numpy.sum(fft_data[18:34]),   #   710 ~ 1420   1000
            numpy.sum(fft_data[34:67]),   #  1420 ~ 2840   2000
            numpy.sum(fft_data[67:133]),  #  2840 ~ 5680   4000
            numpy.sum(fft_data[133:265]), #  5680 ~ 11360  8000
            numpy.sum(fft_data[265:]),    # 11360 ~ 22050  16000
        ])
        return numpy.round(bands.clip(0, CHUNK / 2) / (CHUNK / 2) * 100).astype(int)
    @property
    def frequency_label(self) -> list[str]:
        '''
        get frequency of 10 octave bands
        '''
        return ['31.5', '63', '125', '250', '500', '1K', '2K', '4K', '8K', '16K']

    def prepare_plot(self):
        '''
        prepare to display frequency
        '''
        figure, self.__axes = pyplot.subplots()
        self.__canvas = figure.canvas
        self.__x = numpy.arange(len(self.frequency_label))
        pyplot.show(block=False)
    def display_frequency(self, data: numpy.ndarray):
        '''
        use matplotlib to display frequency
        * call `prepare_plot()` before this method
        '''
        self.__axes.cla()
        pyplot.xticks(self.__x, self.frequency_label)
        pyplot.ylim(0, 100)
        pyplot.bar(self.__x, data)
        self.__canvas.draw()
        self.__canvas.flush_events()
    
    def record(self, second: float) -> numpy.ndarray:
        '''
        record from microphone\n
        [parameter]
        second: record second
        '''
        frame_count = int(self.__sample_rate * second)
        with self.__microphone.recorder(self.__sample_rate, self.__channels) as microphone:
            return microphone.record(frame_count)
    
    def play(self, data: numpy.ndarray):
        '''
        use speaker to play\n
        [parameter]
        data: data to play
        '''
        with self.__speaker.player(self.__sample_rate) as speaker:
            speaker.play(data)

    def all_speakers(self) -> list[dict]:
        '''
        get info of speakers
        '''
        return [
            {
                'id': speaker.id,
                'name': speaker.name,
                'channels': speaker.channels
            } for speaker in soundcard.all_speakers()
        ]
    def all_microphones(self, include_loopback: bool = False) -> list[dict]:
        '''
        get info of microphones
        '''
        return [
            {
                'id': microphone.id,
                'name': microphone.name,
                'channels': microphone.channels
            } for microphone in soundcard.all_microphones(include_loopback)
        ]
    
    @property
    def sample_rate(self):
        return self.__sample_rate
    @property
    def channels(self):
        return self.__channels
    @property
    def speaker_info(self):
        '''
        get current speaker info
        '''
        return {
            'id': self.__speaker.id,
            'name': self.__speaker.name,
            'channels': self.__speaker.channels
        }
    @property
    def microphone_info(self):
        '''
        get current microphone info
        '''
        return {
            'id': self.__microphone.id,
            'name': self.__microphone.name,
            'channels': self.__microphone.channels
        }

if __name__ == '__main__':
    sound_card = SoundCard()

    microphones = sound_card.all_microphones(True)
    for i in range(len(microphones)):
        print(f'{i}: {microphones[i]["name"]}')
    id = int(input('microphone > '))
    sound_card.set_microphone(id, True)

    sound_card.prepare_plot()
    while True:
        data = sound_card.record_fft()
        # do something ...
        sound_card.display_frequency(data)
