import math
import os
import wave


def round(n):
    if n > 255:
        n = 255
    elif n < 0:
        n = 0
    return n


def chord(c):
    # 44100个样本
    sample_frequency = 44100

    # 频率
    # print("chord", c)
    frequency = c["m"]
    # print("chord", c, frequency)

    # 音量是50
    volume = 50

    # 样本长度
    untill = c["t"]
    # print("untill", untill)
    samples_length = int(sample_frequency / untill)

    # 弄样本长度个byte数列
    data = bytearray(samples_length)

    # 算一个周期是多少PI
    r = 2.0 * math.pi * frequency / sample_frequency

    # 然后取他们的sin值？
    for i, e in enumerate(data):
        v = 128 + int(volume * math.sin(i * r))
        # print("v", v)
        data[i] = v
    # for i, e in enumerate(data):
    #     v = data[i] + int(volume/2 * math.sin(i * r * 2))
    #     data[i] = v
    # for i, e in enumerate(data):
    #     v = data[i] + int(volume/3 * math.sin(i * r * 4))
    #     data[i] = v
    # for i, e in enumerate(data):
    #     v = data[i] + int(volume/4 * math.sin(i * r * 8))
    #     data[i] = round(v)
    data = envolope(data, 0.1, 0, 0, 0.9)
    return data

def pcm_2_wav(data):
    header_length = 44
    header = bytearray(header_length)

    # ChunkID
    chunk_id = 'RIFF'
    header[0:4] = chunk_id.encode('ascii')

    # ChunkSize
    chunk_size = len(data) + 36
    header[4:8] = chunk_size.to_bytes(4, byteorder='little')

    # Format
    format = 'WAVE'
    header[8:12] = format.encode('ascii')

    # Subchunk1ID
    subchunk1_id = 'fmt '
    header[12:16] = subchunk1_id.encode('ascii')

    # Subchunk1Size
    subchunk1_size = 16
    header[16:20] = subchunk1_size.to_bytes(4, byteorder='little')

    audio_format = 1
    header[20:22] = audio_format.to_bytes(2, byteorder='little')

    num_channels = 1
    header[22:24] = num_channels.to_bytes(2, byteorder='little')

    sample_rate = 44100
    header[24:28] = sample_rate.to_bytes(4, byteorder='little')

    bits_per_sample = 8
    byte_rate = int(sample_rate * num_channels * bits_per_sample / 8)
    block_align = int(num_channels * bits_per_sample / 8)
    header[28:32] = byte_rate.to_bytes(4, byteorder='little')
    header[32:34] = block_align.to_bytes(2, byteorder='little')
    header[34:36] = bits_per_sample.to_bytes(2, byteorder='little')

    subchunk2_id = 'data'
    header[36:40] = subchunk2_id.encode('ascii')

    subchunk2_size = len(data)
    header[40:44] = subchunk2_size.to_bytes(4, byteorder='little')

    # print('length of header: ', len(header))

    return header + data

def envolope(data, a, d, s, r):
    factor = 0.01       # 增强和衰弱系数
    l = len(data)       # 拿到音乐数据的长度
    a = int(l * a)      # 把l和a相乘，这是为什么
    d = a + int(l * d)
    s = d + int(l * s)
    r = s + int(l * r)
    # print(a, d, s, r)

    # attack
    for i in range(a):
        # print("data[i]", data[0])
        v = round(data[i] + int(i * factor))
        data[i] = v
    # decay
    for i in range(a, d):
        # print(i , a, d, len(data))
        v = round(data[i] - int(i * factor))
        data[i] = v
    # sustain
    for i in range(d, s):
        v = round(data[i] - int(i * factor))
        data[i] = v
    # release
    for i in range(s, r):
        v = round(data[i] - int(i * factor))
        data[i] = v
    return data

def main():
    # 每个音的振幅
    C4 = 261.63
    D4 = 293.66
    E4 = 329.63
    F4 = 349.23
    G4 = 392.00
    G3 = 196.00
    A4 = 440.00
    A3 = 220.00
    B4 = 493.88
    B3 = 246.94

    doremiMap = {
        "1": C4,
        "2": D4,
        "3": E4,
        "4": F4,
        "5": G4,
        "5.": G3,
        "6": A4,
        "6.": A3,
        "7": B4,
        "7.": B3,
        "0": 0,
    }

    # 把他们弄成曲子
    # melody = [E4, E4, F4, G4, G4, F4, E4, D4]
    mary = [
        # 1 - 1
        {"m": doremiMap["5."], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["2"], "t": 4},
        {"m": doremiMap["1"], "t": 4},
        {"m": doremiMap["5."], "t": 2},
        {"m": doremiMap["0"], "t": 4},
        {"m": doremiMap["5."], "t": 8},
        {"m": doremiMap["5."], "t": 8},
        # 1 - 2
        {"m": doremiMap["5."], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["2"], "t": 4},
        {"m": doremiMap["1"], "t": 4},
        {"m": doremiMap["6."], "t": 2},
        {"m": doremiMap["0"], "t": 2},

        # 2-1
        {"m": doremiMap["6."], "t": 4},
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["2"], "t": 4},
        {"m": doremiMap["7."], "t": 2},
        {"m": doremiMap["0"], "t": 2},

        # 2-2
        {"m": doremiMap["5"], "t": 4},
        {"m": doremiMap["5"], "t": 4},
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["2"], "t": 4},
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["1"], "t": 4},
        {"m": doremiMap["0"], "t": 4},
        # 3 - 1
        {"m": doremiMap["5."], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["2"], "t": 4},
        {"m": doremiMap["1"], "t": 4},
        {"m": doremiMap["5."], "t": 2},
        {"m": doremiMap["0"], "t": 2},
        # 3 - 2
        {"m": doremiMap["5."], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["2"], "t": 4},
        {"m": doremiMap["1"], "t": 4},
        {"m": doremiMap["6."], "t": 2},
        {"m": doremiMap["0"], "t": 4},
        {"m": doremiMap["6."], "t": 4},
        # 4 - 1
        {"m": doremiMap["6."], "t": 4},
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["2"], "t": 4},
        {"m": doremiMap["5"], "t": 4},
        {"m": doremiMap["5"], "t": 4},
        {"m": doremiMap["5"], "t": 4},
        {"m": doremiMap["5"], "t": 4},
        # 4-2
        {"m": doremiMap["6"], "t": 4},
        {"m": doremiMap["5"], "t": 4},
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["2"], "t": 4},
        {"m": doremiMap["1"], "t": 1 / (1/2 + 1/4)},
        {"m": doremiMap["0"], "t": 4},
        # 5-1
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["3"], "t": 2},
        # 5-2
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["5"], "t": 4},
        {"m": doremiMap["1"], "t": 4},
        {"m": doremiMap["2"], "t": 8},
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["0"], "t": 4},
        # 6-1
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["3"], "t": 8},
        {"m": doremiMap["3"], "t": 8},
        # 6-2
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["2"], "t": 4},
        {"m": doremiMap["2"], "t": 4},
        {"m": doremiMap["1"], "t": 4},
        {"m": doremiMap["2"], "t": 2},
        {"m": doremiMap["5"], "t": 2},
        # 7-1
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["3"], "t": 2},
        # 7-2
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["5"], "t": 4},
        {"m": doremiMap["1"], "t": 4},
        {"m": doremiMap["2"], "t": 8},
        {"m": doremiMap["3"], "t": 1 / (1/2 + 1/4)},
        {"m": doremiMap["0"], "t": 4},
        #8-1
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["3"], "t": 4},
        {"m": doremiMap["3"], "t": 8},
        {"m": doremiMap["3"], "t": 8},
        #8-2
        {"m": doremiMap["5"], "t": 4},
        {"m": doremiMap["5"], "t": 4},
        {"m": doremiMap["4"], "t": 4},
        {"m": doremiMap["2"], "t": 4},
        {"m": doremiMap["1"], "t": 2},
        {"m": doremiMap["0"], "t": 4},
    ]


    # melody = [E4, E4, F4, G4, G4, F4, E4, D4, C4, C4, D4, E4, E4, D4, D4]
    # melody = [E4, D4, C4, D4, E4, E4, E4]

    # 把他们弄成曲子
    ds = [chord(c) for c in mary]
    data = b''.join(ds)

    open('sound.pcm', 'wb').write(data)
    # u8 表示 unsigned 8 bit
    # -ar 表示采样率
    # cmd = '../ffmpeg -y -f u8 -ar 44100 -ac 1 -acodec pcm_u8 -i sound.pcm sound.wav'
    # os.system(cmd)
    wav_data = pcm_2_wav(data)
    open('sound.wav', 'wb').write(data)


def turn_pcm_to_wave(pcm_path):
    with open(pcm_path, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
    with wave.open(pcm_path + '.wav', 'wb') as wavfile:
        wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)


if __name__ == '__main__':
    main()
