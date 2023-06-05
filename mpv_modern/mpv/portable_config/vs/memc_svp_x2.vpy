### https://github.com/hooke007/MPV_lazy/wiki/3_K7sfunc
### svpflow - podwajanie klatek, średnie zużycie zasobów
### MEMC_SVP_LQ

import vapoursynth as vs
from vapoursynth import core
import k7sfunc as k7f

clip = video_in

############
# Opcje użytkownika #
############

H_Pre = 1440
Cpu = 0
Gpu = 0
Lk_Fmt = False
## Liczba całkowita, przewidywana wysokość docelowa (wypełnij wysokością swojego monitora)
## <0|1> Czy używać tylko CPU
## <0|11|12|21> Numer używanej karty graficznej, 0 to pierwsza karta
## <True|False> Czy zablokować format pikseli na yuv420p8

ret = k7f.FPS_CTRL(clip, fps_in=container_fps, fps_ret=True)
clip = k7f.FMT_CTRL(clip, h_max=H_Pre, fmt_pix=1 if Lk_Fmt else 0)
clip = k7f.SVP_LQ(clip, fps_in=container_fps, cpu=Cpu, gpu=Gpu)

clip.set_output()
