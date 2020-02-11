import librosa
import librosa.display
from IPython.display import Audio
import numpy as np
import matplotlib.pyplot as plt

# 1. 음성파일 load
audio_path = "../0. data/train/train_data/wav_001.wav"
y, sr = librosa.load(audio_path)  # sr=48000, mono=True, duration=1)
# sr = smaple rate [Hz]
# mono = 사운드 채널 수 (True:1, False:2)
# duration = 사운드 길이 [s]

ori_sent = "GO DO YOU HEAR"

Audio(data=y, rate=sr)   # 왜 이거 안뜨지?

# D = librosa.amplitude_to_db(librosa.stft(y[:1024]), ref=np.max)
# plt.plot(D.flatten())
# plt.show()

print("Done")

# 3. Mel-frequency cepstral coefficients (MFCC)
# Q. What is MFCC ? 멜-스펙트로그램 ?

S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
log_S = librosa.amplitude_to_db(S, ref=np.max)
# plt.figure(figsize=(12, 4))
# librosa.display.specshow(log_S, sr=sr, x_axis="time", y_axis="mel")
# plt.title("mel power spectrogram")
# plt.colorbar(format="%+02.0f dB")
# plt.tight_layout()
# plt.show()

# 4. Normalization
min_level_db = -100

def _normalize(S):
    return np.clip((S - min_level_db) / -min_level_db, 0, 1)

norm_S = _normalize(log_S)
plt.figure(figsize=(12, 4))
librosa.display.specshow(norm_S, sr=sr, x_axis="time", y_axis="mel")
plt.title("norm mel power spectrogram")
plt.colorbar(format="%+0.1f dB")
plt.tight_layout()
plt.show()
