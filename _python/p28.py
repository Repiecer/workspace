import torch
import ChatTTS
import torchaudio

chat = ChatTTS.Chat()
chat.load(compile=False)

# 1. 固定低沉男声音色
AUDIO_SEED = 2424  # 或者试试 7869
torch.manual_seed(AUDIO_SEED)
rand_spk = chat.sample_random_speaker()

# 2. 设置推理参数，控制语速、音调
params_infer_code = {
    'spk_emb': rand_spk,            # 使用上面固定的音色
    'temperature': 0.2,             # 让发音更稳定
    'top_P': 0.7,                   # 控制生成多样性
    'top_K': 20,                    # 控制生成多样性
    # 这里无法直接设置 formant_shift，需要通过后续音频处理或更底层的接口
}

# 3. 准备文本
texts = ["你好，这是一个低沉而清晰的男声示例，语速特意放慢了。"]

# 4. 生成语音
wavs = chat.infer(texts, params_infer_code=params_infer_code)

# 5. 保存音频
torchaudio.save("deep_slow_voice.wav", torch.from_numpy(wavs[0]).unsqueeze(0), 24000)