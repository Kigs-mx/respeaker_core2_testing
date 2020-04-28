#!/usr/bin/env python3
'''
Programa para grabar archivos de audio  v2
Al correr el script de pueden declarar 5 argumentos, que se utilizan en el programa.
Dichos argumentos son:
chunk channels rate duration file_record_name.wav
deden ir solo separados por espacios sin declarar el nombre de la variable
Consulta sobre conversion del objeto buffer a un array
https://stackoverflow.com/questions/24974032/reading-realtime-audio-data-into-numpy-array
'''

import pyaudio
import wave
import numpy as np
import sys

def main(argv):

    if len(sys.argv) <= 1:
      print("You have to declare the args: chunk channels rate duration file_record_name.wav")
      print("just write the four numbers. Load default values")
                #[scriptName,  buffer_size, channels, rate, record_seconds, file_record_name]
      sys.argv = ['recordFile.py', '2048', '6', '96000', '5', 'testRecMicsArray.wav']

    print("Reading arguments...")
    chunk = int( sys.argv[1] )
    chs = int( sys.argv[2] )
    rate = int( sys.argv[3] )
    record_seconds = int( sys.argv[4] )
    #wave_output_file = sys.argv[5]
    wave_output_file = str(chs)+'_ch_'+str(record_seconds)+'sec_'+str(rate)+'_fs.wav'

    print(record_seconds)

    #chunk = 2048
    #channels = 8
    #rate = 96000
    #record_seconds = 5
    #wave_output_file = "testRecPython.wav"
    Format = pyaudio.paInt16

    #create and configure the microphone
    mic = pyaudio.PyAudio()
    stream = mic.open(format = Format, channels = chs, rate = rate,
        input=True, frames_per_buffer=chunk)

    print("recording...")

    #read and store microphone data per frame read
    frames = []
    #define iterations of for and times that record buffer
    rec_time = int(rate/chunk*record_seconds)
    print("For cycle count: %d",rec_time)
    for i in range(0, rec_time):
        data = stream.read(chunk)
        #datas.append(np.frombuffer(data, dtype=np.int16))
        frames.append(data)

    print("done recording ...")

    # stop and close streaming and kill object
    stream.stop_stream()
    stream.close()
    mic.terminate()

    #convert obj buffer to array
    buffer = np.frombuffer(data, dtype=np.int16)
    bufCh = np.stack((buffer[::chs], buffer[0::chs]), axis=0)
    print("Lenght of buffer: ",bufCh.size)


    # combine & store all microphone data to output.wav file
    outputFile = wave.open(wave_output_file, 'wb')
    outputFile.setnchannels(chs)
    outputFile.setsampwidth(mic.get_sample_size(Format))
    outputFile.setframerate(rate)
    outputFile.writeframes(b''.join(frames))
    outputFile.close()


if __name__ == "__main__":
    main(sys.argv)
