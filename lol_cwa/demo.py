import pyaudio
import numpy as np
from funasr import AutoModel

model_dir = 'E:\\ai_models\\iic\\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online'

# 加载实时流式语音识别模型
model = AutoModel(
    model=model_dir,
    model_revision="v2.0.4",
    disable_update=True,
)

# 配置音频流参数
chunk_size = [0, 10, 5]  # 600ms
encoder_chunk_look_back = 4
decoder_chunk_look_back = 1
cache = {}


def audio_listener(callback):
    # 初始化麦克风录音
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=9600)  # 600ms 的音频块
    try:
        result = ''
        count = 0
        while True:
            audio_chunk = stream.read(9600)  # 600ms
            speech_chunk = np.frombuffer(audio_chunk, dtype=np.int16)
            # 传递给模型进行实时识别
            res = model.generate(input=speech_chunk, cache=cache, is_final=False,
                                 chunk_size=chunk_size,
                                 encoder_chunk_look_back=encoder_chunk_look_back,
                                 decoder_chunk_look_back=decoder_chunk_look_back)
            talk = res[0]['text']
            if talk == '':
                count += 1
                if count == 5:  # 5 * 600ms 设定3秒输出所说的话
                    if len(result) != 0:
                        callback(result)
                        # trans(result, 'zh', 'en')
                        result = ''
                    count = 0
            else:
                result += talk
    except Exception as e:
        print(f"Error while reading audio: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == '__main__':
    pass

