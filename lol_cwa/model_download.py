# SDK模型下载
from pathlib import Path
from modelscope import snapshot_download


def model_download(name: str):
    if name is not None or name != '':
        path = 'E:\\ai_models\\'
        for i in name.split('/'):
            path += f'{i}\\'
            Path(path).mkdir(exist_ok=True)
        model_dir = snapshot_download(
            model_id=name,
            local_dir=path
        )
        return model_dir


model_download('iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online')

