import pyaudio
import numpy as np


class SpeechModel:

    def __init__(self, model_dir):
        from funasr import AutoModel

        # 加载实时流式语音识别模型
        self.model = AutoModel(
            model=model_dir,
            model_revision="v2.0.4",
            disable_update=True,
        )

    def audio_listener(self, callback):
        # 配置音频流参数
        chunk_size = [0, 10, 5]  # 600ms
        encoder_chunk_look_back = 4
        decoder_chunk_look_back = 1
        cache = {}

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
                res = self.model.generate(input=speech_chunk, cache=cache, is_final=False,
                                          chunk_size=chunk_size,
                                          encoder_chunk_look_back=encoder_chunk_look_back,
                                          decoder_chunk_look_back=decoder_chunk_look_back)
                talk = res[0]['text']
                if talk == '':
                    count += 1
                    if count == 5:  # 5 * 600ms 设定3秒输出所说的话
                        if len(result) != 0:
                            callback(result)
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
