import wave


def turn_pcm_to_wave(pcm_path):
    with open(pcm_path, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
    with wave.open(pcm_path + '.wav', 'wb') as wavfile:
        wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)