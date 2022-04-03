import pygame as py
import librosa
import librosa.display
import matplotlib.pyplot as plt 
import numpy as np
import time
import ctypes

# SCREEN
# Get Size of the Screen 
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen_width = screensize[0]
screen_height = screensize[1]

# setup pygame 
py.init()
py.display.set_caption("AudioVisualizer")
window = py.display.set_mode(screensize)
clock = py.time.Clock()
running = True
hud = True
bars_width = True

# LIBROSA
# CHOOSE YOUT SONG
filename = 'music/music.wav'
data, sr = librosa.load(filename, sr=44100)

d = librosa.stft(data, hop_length=512, n_fft=2048*4)
d_harmonic, d_percussive = librosa.decompose.hpss(d)

# setup frequencies for harmonic with librosa
spectrogram_h = librosa.amplitude_to_db(d_harmonic, ref=np.max)
frequencies_h = librosa.core.fft_frequencies(sr=44100, n_fft = 2048)
time = librosa.core.frames_to_time(np.arange(spectrogram_h.shape[1]), sr=sr, 
                                   hop_length=512, n_fft = 2048)
time_index_ratio_h = len(time)/time[len(time)-1]
frequencies_index_ratio_h = len(frequencies_h)/frequencies_h[len(frequencies_h)-1]

def get_decibel_h(target_time, freq):
    return spectrogram_h[int(freq*frequencies_index_ratio_h)][int(target_time*time_index_ratio_h)]

# setup frequencies for percussive with librosa
spectrogram_p = librosa.amplitude_to_db(d_percussive, ref=np.max)
frequencies_p = librosa.core.fft_frequencies(sr=44100, n_fft = 2048)
time = librosa.core.frames_to_time(np.arange(spectrogram_p.shape[1]), sr=sr, 
                                   hop_length=512, n_fft = 2048)
time_index_ratio_p = len(time)/time[len(time)-1]
frequencies_index_ratio_p = len(frequencies_p)/frequencies_p[len(frequencies_p)-1]

def get_decibel_p(target_time, freq):
    return spectrogram_p[int(freq*frequencies_index_ratio_p)][int(target_time*time_index_ratio_p)]

### SHOW PERCUSSIVE AND HARMONICS PER PYPLOT #### ADITIONAL
# plt.style.use('dark_background')
# rp = np.max(np.abs(d))
# fig, ax = plt.subplots(nrows=3, sharex=True, sharey=True)
# img = librosa.display.specshow(librosa.amplitude_to_db(np.abs(d), ref=rp),
#                          y_axis='log', x_axis='time', ax=ax[0])
# ax[0].set(title='Full spectrogram')
# ax[0].label_outer()

# librosa.display.specshow(librosa.amplitude_to_db(np.abs(d_harmonic), ref=rp),
#                          y_axis='log', x_axis='time', ax=ax[1])
# ax[1].set(title='Harmonic spectrogram')
# ax[1].label_outer()

# librosa.display.specshow(librosa.amplitude_to_db(np.abs(d_percussive), ref=rp),
#                          y_axis='log', x_axis='time', ax=ax[2])
# ax[2].set(title='Percussive spectrogram')
# fig.colorbar(img, ax=ax)
# plt.show()
### SHOW PERCUSSIVE AND HARMONICS PER PYPLOT #### ADITIONAL

# define default for color_theme
color_theme = 0
# set color by color-index for harmonics
def set_color_p(segment):
    color = [[[121, 163, 146],[3, 116, 105],[1, 89, 86],[0, 53, 66],[0, 29, 41]], # colorScheme 2
            [[86, 166, 50],[242, 226, 5],[242, 203, 5],[242, 135, 5],[217, 4, 4]], # colorScheme 1
            [[143, 142, 191],[79, 77, 140],[71, 64, 115],[46, 65, 89],[38, 38, 38]], # colorScheme 4
            [[85, 89, 54,],[108, 115, 60],[191, 182, 48],[166, 159, 65],[242, 242, 242]], # colorScheme 5
            [[1, 38, 25],[1, 64, 41],[2, 115, 74],[59, 191, 143],[167, 242, 228]], # colorScheme 3
            [[1, 40, 64],[2, 94, 115],[4, 138, 191],[75, 195, 242,],[75, 226, 242]], # colorScheme 6
            [[114, 166, 3],[79, 115, 2],[39, 64, 1],[89, 85, 62],[242, 188, 27]], # colorScheme 8
            [[28, 56, 140],[48, 88, 140],[217, 102, 155],[217, 121, 201,],[242, 162, 92]], # colorScheme 9
            [[144, 46, 242],[132, 102, 242],[164, 128, 242],[206, 153, 242],[241, 194, 242]]] # colorScheme 12
             
    return color[color_theme][segment]

# set color by color-index for harmonics
def set_color_h(segment):
    color = [[[121, 163, 146],[3, 116, 105],[1, 89, 86],[0, 53, 66],[0, 29, 41]],# colorScheme 2
            [[86, 166, 50],[242, 226, 5],[242, 203, 5],[242, 135, 5],[217, 4, 4]], # colorScheme 1
            [[143, 142, 191],[79, 77, 140],[71, 64, 115],[46, 65, 89],[38, 38, 38]], # colorScheme 4
            [[85, 89, 54,],[108, 115, 60],[191, 182, 48],[166, 159, 65],[242, 242, 242]], # colorScheme 5
            [[0, 29, 41],[0, 53, 66],[1, 89, 86],[3, 116, 105],[121, 163, 146]], # colorScheme 2
            [[1, 38, 38],[1, 28, 38],[2, 64, 89],[2, 73, 89],[83, 151, 166,]], # colorScheme 7
            [[114, 166, 3],[79, 115, 2],[39, 64, 1],[89, 85, 62],[242, 188, 27]], # colorScheme 8
            [[18, 88, 153],[67, 145, 204],[91, 9, 255],[209, 101, 1],[255, 146, 71]], # colorScheme 10
            [[104, 5, 242],[98, 4, 191],[163, 18, 166],[191, 75, 75],[242, 159, 5]]] # colorScheme 11
            
    return color[color_theme][segment]

# define frequency bands and height
freq_bands = 31
freq_heights = 25

# HARMONIC
# create HARMONIC bands and start posistion
freq_harmonic = []
harmonic_pos = screen_width*0.015, screen_height*0.51
# total size of harmonic series in procent
harmonic_width = int(screen_width*0.98)
harmonic_height = int(screen_height*0.45)
# size of single point in the harmonic series
harmonic_size_widgth = ((harmonic_width/freq_bands))
harmonic_size_height = ((harmonic_height/freq_heights)*0.6)



# freq_harmonics[band][height]
for x in range(freq_bands):
    freq_band = []
    for y in range(freq_heights):
        a = [((harmonic_width/freq_bands)*x)+harmonic_pos[0],                    
             (harmonic_height-(y*(harmonic_height/freq_heights))+harmonic_pos[1])] 
        freq_band.append(a)
    # reverse the matrix
    freq_band.reverse()
    freq_harmonic.append(freq_band)
    
def draw_harmonics(freq_height, freq_band, bars_width_value):
    for height in range(freq_height):
        # define color-theme per height
        if height <= 2:
            color = set_color_h(0)
        elif height <= 5:
            color = set_color_h(1)
        elif height <= 13:
            color = set_color_h(2)
        elif height <= 18:
            color = set_color_h(3)
        elif height <= 23:
            color = set_color_h(4)
        # create rectangle matrix
        py.draw.rect(window, py.Color(*color), 
                    py.Rect(*freq_harmonic[freq_band][height], 
                            harmonic_size_widgth*bars_width_value, 
                            harmonic_size_height), 0, 2)
        
# PERCUSSIVE
# create percussive bands and start posistion
freq_percussive = []
percussive_pos = screen_width*0.015, screen_height*0.04
# total size of percussive series in procent
percussive_width = int(screen_width*0.98)
percussive_height = int(screen_height*0.45)
# size of single point in the percussive series
percussive_size_widgth = ((percussive_width/freq_bands))
percussive_size_height = ((percussive_height/freq_heights)*0.6)

# freq_percussive[band][height]
for x in range(freq_bands):
    freq_band = []
    for y in range(freq_heights):
        a = [((percussive_width/freq_bands)*x)+harmonic_pos[0],                    
             (percussive_height-(y*(percussive_height/freq_heights))+percussive_pos[1])] 
        freq_band.append(a)
    freq_percussive.append(freq_band)
        
def draw_percussive(freq_height, freq_band,bars_width_value):
    for height in range(freq_height):
        # define color-theme per height
        if height <= 2:
            color = set_color_p(0)
        elif height <= 5:
            color = set_color_p(1)
        elif height <= 13:
            color = set_color_p(2)
        elif height <= 18:
            color = set_color_p(3)
        elif height <= 23:
            color = set_color_p(4)
        # create rectangle matrix
        py.draw.rect(window, py.Color(color), 
                    py.Rect(*freq_percussive[freq_band][height], 
                            percussive_size_widgth*bars_width_value, 
                            percussive_size_height), 0, 2)
 

# define the frequencies bands
bars = [20, 25, 31,
        40, 50, 63,
        80, 100, 125,
        160, 200, 250,
        315, 400, 500,
        630, 800, 1000,
        1250, 1600, 2000,
        2500, 3150, 4000,
        5000, 6300, 8000,
        10000, 12500, 16000,
        20000]

def draw_hud():
    # render fonts
    default_font = py.font.SysFont("Arial Black", 18)
    head_font = py.font.SysFont("Arial Black", 60)
    
    # render percussive header    
    render_percussive = head_font.render("PERCUSSIVE", True, py.Color(200, 200, 200))
    rect_p = render_percussive.get_rect()
    rect_p.center = screen_width*0.5, screen_height*0.05
    window.blit(render_percussive, rect_p)
    
    # render harmonic header    
    render_harmonic = head_font.render("HARMONIC", True, py.Color(200, 200, 200))
    rect_h = render_harmonic.get_rect()
    rect_h.center = screen_width*0.5, screen_height*0.95
    window.blit(render_harmonic, rect_h)
    
    # render commands
    cmd_text = ["PRESS",
                "M: Menü on/off",
                "NUMBER 1-9: Color-Preset",
                "ESC: EXIT",
                "D: Change the bar-width"]
    
    for index in range(0, 5):
        line = cmd_text[index]
        render_cmd = default_font.render(line, True, py.Color(180, 180, 180))
        rect_cmd = render_cmd.get_rect()
        rect_cmd.topleft =  screen_width*0.02, (screen_height*0.8)+index*30
        window.blit(render_cmd, rect_cmd)
    
def handle_key():
    global color_theme
    global running 
    global hud
    global bars_width
    for event in [e for e in py.event.get() if e.type == py.KEYDOWN]:
        # exit programm
        if event.key == py.K_ESCAPE:
            running = False
        # change color-theme
        if event.key == py.K_1:
            color_theme = 0
        if event.key == py.K_2:
            color_theme = 1
        if event.key == py.K_3:
            color_theme = 2
        if event.key == py.K_4:
            color_theme = 3
        if event.key == py.K_5:
            color_theme = 4
        if event.key == py.K_6:
            color_theme = 5
        if event.key == py.K_7:
            color_theme = 6
        if event.key == py.K_8:
            color_theme = 7
        if event.key == py.K_9:
            color_theme = 8
        # change the width of the bars
        if event.key == py.K_d:
            bars_width = not bars_width 
        # show menü    
        if event.key == py.K_m:
            hud = not hud
            
def app():
    py.mixer.music.load(filename)
    py.mixer.music.play(0)

    while running:
        window.fill(py.Color(0,0,0)) 
        handle_key()
        
        if bars_width:
            bars_width_value = 0.8
        else:
            bars_width_value = 0.5
            
        # Harmonic
        for b in bars:
            decibel_scala_value = int(get_decibel_h(py.mixer.music.get_pos()/1000.0, b)*-1/3.2)
            decibel_reverse = freq_heights-decibel_scala_value 
            index = bars.index(b)
            draw_harmonics(decibel_reverse, index, bars_width_value)
        
        # Percussiv
        for b in bars:
            decibel_scala_value = int(get_decibel_p(py.mixer.music.get_pos()/1000.0, b)*-1/3.2)
            decibel_reverse = freq_heights-decibel_scala_value 
            index = bars.index(b)
            draw_percussive(decibel_reverse, index, bars_width_value)

        if hud:
            draw_hud()
            
        py.display.update()
        
app()
py.quit()