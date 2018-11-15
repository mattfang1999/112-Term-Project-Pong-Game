
import audioop
import pyaudio as pa

#######
#Much of the speech audio code was taken from this page:
#https://www.<the website>.com
#######

class Speech():
    def __init__(self):
        # soundtrack properties
        self.format = pa.paInt16
        self.rate = 16000
        self.channel = 1
        self.chunk = 1024
        self.threshold = 4000
        self.isLoudEnough = False 

        # intialise microphone stream
        self.audio = pa.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                  channels=self.channel,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)


    def record(self):
        
        #while True:
        data = self.stream.read(self.chunk)
        rms = audioop.rms(data,2) #get input volume
        if rms>self.threshold: #if input volume greater than threshold
            self.isLoudEnough = True
                
                
                
            
                