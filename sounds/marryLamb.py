import math
import os


def round(n):
    if n > 255:
        n = 255
    elif n < 0:
        n = 0
    return n


# 这个函数是关键
def chord(c):
    # 采样率，即每秒钟采集样本的次数
    # 1分钟里采集44100个样本
    # 为什么要这样呢？ 因为至少需要大于 2 倍录制频率的采样率才能被确定波形
    # 人耳听到的最大频率是22050，所以它的2倍就是44100
    # 为什么要大于2倍呢 todo
    sample_frequency = 44100

    # 频率
    # 音符的频率, 如 A4 = 440 Hz, 意思是每秒钟该音符有440个完整的波
    frequency = c["m"]

    # 音量是50
    volume = 50

    # 样本长度
    # 五线谱的拍子是相对节奏，需要你自己定义一个节拍是多少的绝对时间
    # 样本长度 = 每分钟采样的量 / 每分钟打几个拍子
    # 生成 1 秒的音乐，需要 sample_frequency 个样本
    # sample_frequency / 4 个样本，就代表生成了 0.25 秒的音乐
    # （1秒 x 每秒需要采集的样本量）/ 1分钟打4个拍子 = 每个拍子需要的样本量（0.25秒的音乐）
    # 按照每个音符持续 0.25s, 即将 sample_frequency / 4, 得到 0.25s 内的样本数量samples_length
    untill = c["t"]
    # 1分钟采样sample_frequency次
    # 那么这个音符，我应该采样几次呢？ 就是 （1秒采样的次数 x 音符的持续秒数）
    # 音符的持续秒数就是（1 / 音符的拍子）。所以4拍的话，就是持续0.25秒
    # 一个音符要采样的次数 = int(每秒的采样次数 * 1 / 音符的拍子)
    samples_length = int(sample_frequency / untill)
    print("samples_length", samples_length,  "untill", untill)

    # 新建一个byte数列，长度就是一个音符要采样的次数
    # 这里面只能保存没有符号位的8位的数据
    data = bytearray(samples_length)

    # 算每一个样本所要用到的周期长度，单位是PI，也就是每一次采样，我要间隔几个PI
    # 1 秒有 sample_frequency 个样本 （1秒要采取44100个样本）
    # 1 秒有 frequency 个周期
    # 则 1 个周期里，我们采集 sample_frequency / frequency 次样本

    # 正弦波 1 个周期长度是 2 * pi
    # 那么我们现在要算出的就是 每一个样本所用到的单位周期数（ 2·π / 一个周期要采集的样本次数）

    # ω = 2·π / T, T 是最小正周期, 简单理解就是 x + T (x 走过 T 个长度) 之后重新开始一个新的正弦波
    # 用 sample_frequency / frequency 可以得到一个周期内的采样数量, 即是 T(单位周期的采样量）
    # 那么就可以得到 ω = (2·π) / (sample_frequency / frequency) => 2·π * frequency / sample_frequency
    # 就是 下面的 r (也就是一个采样需要多少PI，采一次样，我往前走了多少PI)
    # 那么第一个采样值我就走了r，第二采样值就走了2r
    r = 2.0 * math.pi * frequency / sample_frequency

    # 正弦函数的公式： y = A·sin(ω·x + φ)
    # A: 纵向的拉伸/收缩, 体现在代码中的 volume
    # ω: 周期的变化, 也就是r
    # φ: 横向的平移, 没有体现
    # x： 就是i
    for i, e in enumerate(data):
        # +128 是因为一个字节的数字范围是 - 128
        # 到127，但是这里只存正整。因为是unsigned int 8位的范围要变成0 - 255。
        # 而sin函数的范围是-1到1，-1要代表0，1要代表255，0要代表127

        # 为了从正弦波图形中取得第 i 个采样值
        # 需要用 采样序号 i 乘以 采样间隔长度 r
        # 得到从图像开始处（原点）到达第 i 个采样点的距离 i * r
        # 从而取得正弦波图形在第 i 个采样点处的值 sin(i * r)

        # 由于这里面的使用的是 无符号的 8 位数字表示, 最大值为 255
        # 那么这里的正弦函数的最低值就是0, 需要纵向平移正弦函数以在(0 - 255)之间表示, 因此需要加上 128
        # i 就是公式中的 x, volume 就是纵轴的缩放倍率
        # i * r 也就是当前位置上的PI的值，这样用sin可以求出sin值
        # 求出来的就是每一音符的每一次采样得到的v，把他们连起来就是音乐
        # todo 播放器又是如何去解释这些v的呢，它怎么就知道周期是啥了呢
        v = 128 + int(volume * math.sin(i * r))
        data[i] = v

    # 谐波 对声波进行傅里叶变换后的频率大于基波的波
    # 让声音的波形更丰富，更接近真实的乐器
    for i, e in enumerate(data):
        v = data[i] + int(volume/2 * math.sin(i * r * 2))
        data[i] = v
    for i, e in enumerate(data):
        v = data[i] + int(volume/3 * math.sin(i * r * 4))
        data[i] = v
    for i, e in enumerate(data):
        v = data[i] + int(volume/4 * math.sin(i * r * 8))
        # 将数值限定在 0 - 255 的范围内
        data[i] = round(v)
    return data


def main():

    # 音符的频率, 单位是HZ
    # 如 A4 = 440 Hz, 意思是每秒钟该音符有440个完整的波，一个波就是一次振动循环
    # 但是这个波的很多细节还没有（比如波有多宽，波有高）
    C4 = 261.63
    D4 = 293.66
    E4 = 329.63
    F4 = 349.23
    G4 = 392.00
    A4 = 440.00
    B4 = 493.88

    doremiMap = {
        "1": C4,
        "2": D4,
        "3": E4,
        "4": F4,
        "5": G4,
        "6": A4,
        "7": B4,
    }

    # melody = [E4, E4, F4, G4, G4, F4, E4, D4]
    # TODO 完全可以减少2这个重复
    mary = [
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["2"], "t": 2},
        {"m": doremiMap["1"], "t": 2},
        {"m": doremiMap["2"], "t": 2},
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["3"], "t": 1},
        {"m": doremiMap["2"], "t": 2},
        {"m": doremiMap["2"], "t": 2},
        {"m": doremiMap["2"], "t": 1},
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["5"], "t": 2},
        {"m": doremiMap["5"], "t": 1},
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["2"], "t": 2},
        {"m": doremiMap["1"], "t": 2},
        {"m": doremiMap["2"], "t": 2},
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["2"], "t": 2},
        {"m": doremiMap["2"], "t": 2},
        {"m": doremiMap["3"], "t": 2},
        {"m": doremiMap["2"], "t": 2},
        {"m": doremiMap["1"], "t": 1},
    ]

    # melody = [E4, D4, C4, D4, E4, E4, E4]
    # 把他们弄成曲子的过程，就是计算这个波的过程，然后把波的数据转换成音乐
    ds = [chord(c) for c in mary]
    data = b''.join(ds)
    # print("data", ds)

    open('sound.pcm', 'wb').write(data)
    # u8 表示 unsigned 8 bit
    # -ar 表示采样率
    cmd = '../ffmpeg -y -f u8 -ar 44100 -ac 1 -acodec pcm_u8 -i sound.pcm sound.wav'
    os.system(cmd)


if __name__ == '__main__':
    main()
