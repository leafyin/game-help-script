# encoding=utf-8
"""
语音识别服务模块
加载 FunASR 实时语音识别模型，监听麦克风并输出识别文本
"""

import threading
import numpy as np
import pyaudio

from pathlib import Path
from modelscope import snapshot_download


def download_model(save_path: str):
    """
    下载语音识别模型到指定路径
    :param save_path: 模型保存目录
    """
    model_name = 'iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online'
    for part in model_name.split('/'):
        save_path = f'{save_path}/{part}'
        Path(save_path).mkdir(parents=True, exist_ok=True)
    snapshot_download(model_id=model_name, local_dir=save_path)
    print(f"[模型下载完成] {save_path}")


class SpeechRecognizer:
    """
    实时语音识别器
    使用 FunASR 模型流式识别麦克风输入
    """

    def __init__(self, model_dir: str):
        from funasr import AutoModel
        self.model = AutoModel(
            model=model_dir,
            model_revision="v2.0.4",
            disable_update=True,
        )

    def start_listening(self, stop_event: threading.Event, callback=None):
        """
        开始监听麦克风，实时识别语音
        :param stop_event: 线程停止事件
        :param callback:   识别到完整语句后的回调函数
        """
        chunk_size = [0, 10, 5]  # 600ms 音频块
        encoder_chunk_look_back = 4
        decoder_chunk_look_back = 1
        cache = {}

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=9600,  # 600ms
        )
        try:
            result = ''
            silence_count = 0
            while not stop_event.is_set():
                audio_chunk = stream.read(9600)
                speech_chunk = np.frombuffer(audio_chunk, dtype=np.int16)

                # 传递给模型进行实时识别
                res = self.model.generate(
                    input=speech_chunk,
                    cache=cache,
                    is_final=False,
                    chunk_size=chunk_size,
                    encoder_chunk_look_back=encoder_chunk_look_back,
                    decoder_chunk_look_back=decoder_chunk_look_back,
                )
                talk = res[0]['text']

                if talk == '':
                    silence_count += 1
                    # 连续静默约 3 秒（5 * 600ms）认为一句话结束
                    if silence_count == 5:
                        if len(result) != 0 and callback:
                            callback(result)
                            result = ''
                        silence_count = 0
                else:
                    result += talk
        except Exception as e:
            print(f"[音频监听错误] {e}")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
