### Skrypt wbudowany w pewien odtwarzacz ma wysokie koszty obliczeniowe

import vapoursynth as vs
from vapoursynth import core

#####################
# Opcje Użytkownika #
#####################

## Całkowicie pomiń interpolację ruchu dla treści przekraczających poniższe limity
max_width  = 1920
max_height = 1200
max_fps    = 60 # Można zmienić na 120, oraz w mpv.conf odznacz display-fps=120
## używaj BlockFPS zamiast FlowFPS dla treści przekraczających poniższe limity
max_flow_width  = 1280
max_flow_height = 720
## blok jest uważany za zmieniony, gdy 8*8*x > th_block|flow_diff z 8*8
## to rozmiar bloku (przeskalowany wewnętrznie), a x różnica każdego
## piksela w tym bloku, domyślnie 400
th_block_diff = 8*8*7
th_flow_diff  = 8*8*7
# (threshold/255)% bloki muszą się zmienić, by uznać to za zmianę sceny
## (= brak kompensacji ruchu), domyślnie 130
th_block_changed = 14
th_flow_changed  = 14
## rozmiar bloków, na których wykonywany jest krok analizy
blocksize  = 2**4


# załóż, że display_fps jest fałszywe, gdy nie mieści się w określonym zakresie
target_num = 60 if display_fps < 23.9 or display_fps > 300 else display_fps
while (target_num > max_fps):
    target_num /= 2
target_num = int(target_num * 1e6)
target_den = int(1e6)
source_num = int(container_fps * 1e6)
source_den = int(1e6)

clip = video_in

if not (clip.width > max_width or clip.height > max_height or container_fps > max_fps):
    clip = core.std.AssumeFPS(clip, fpsnum=source_num, fpsden=source_den)
    sup  = core.mv.Super(clip, pel=2, hpad=blocksize, vpad=blocksize)
    bv   = core.mv.Analyse(sup, blksize=blocksize, isb=True , chroma=True, search=3, searchparam=2)
    fv   = core.mv.Analyse(sup, blksize=blocksize, isb=False, chroma=True, search=3, searchparam=2)

    use_block = clip.width > max_flow_width or clip.height > max_flow_height
    if use_block:
        clip = core.mv.BlockFPS(clip, sup, bv, fv, num=target_num, den=target_den,
                                mode=3, thscd1=th_block_diff, thscd2=th_block_changed)
    else:
        clip = core.mv.FlowFPS(clip, sup, bv, fv, num=target_num, den=target_den,
                               mask=0, thscd1=th_flow_diff, thscd2=th_flow_changed)
    print('motion-interpolation: {0} -> {1} FPS | {3} | {2} Hz'
          .format(source_num / source_den, target_num / target_den,
                  display_fps, use_block and "block" or "flow"))
else:
    print('motion-interpolation: skipping {0}x{1} {2} FPS video'
          .format(clip.width, clip.height, container_fps))

clip.set_output()
