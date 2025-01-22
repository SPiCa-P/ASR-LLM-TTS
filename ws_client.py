import asyncio
import websockets
import pyaudio


# 音频配置
CHUNK = 1024  # 每次读取的帧数
FORMAT = pyaudio.paInt16  # 音频格式
CHANNELS = 1  # 单声道
RATE = 16000  # 采样率

async def send_audio(uri):
    # 初始化音频流
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    async with websockets.connect(uri) as websocket:
        print("Connected to the server. Sending audio...")
        try:
            while True:
                data = stream.read(CHUNK)
                await websocket.send(data)
                
        except websockets.ConnectionClosed as e:
            print(f"Connection closed unexpectedly: {e}")
        except KeyboardInterrupt:
            print("Stopping audio stream...")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            

# 启动发送
asyncio.run(send_audio("ws://0.0.0.0:8765"))