### https://github.com/hooke007/MPV_lazy/wiki/3_K7sfunc
### CREDIT https://github.com/BlackMickey
### MEMC_SVP_PRO.vpy

import vapoursynth as vs
from vapoursynth import core
import k7sfunc as k7f

clip = video_in

#####################
# Opcje Użytkownika #
#####################

H_Pre = 1440
Fps_Num = 120000
Fps_Den = 1001
Abs = True
Nvof = False
Gpu = 0
Lk_Fmt = False
## Liczba całkowita, przewidywana wysokość docelowa (wypełnij wysokością swojego monitora)
## Liczba całkowita, wynik Fps_Num/Fps_Den to docelowa liczba klatek na sekundę lub mnożnik
## Liczba całkowita
## <True|False> Czy wyjście ma być w formacie FPS (True) czy mnożnika (False)
## <True|False> Czy używać Optical Flow (tylko dla kart graficznych Nvidia)
## <0|11|12|21> Numer używanej karty graficznej, 0 to pierwsza karta
## <True|False> Czy zablokować format pikseli na yuv420p8

ret = k7f.FPS_CTRL(clip, fps_in=container_fps, fps_ret=True)
clip = k7f.FMT_CTRL(clip, h_max=H_Pre, fmt_pix=1 if Lk_Fmt else 0)
clip = k7f.SVP_PRO(clip, fps_in=container_fps, fps_num=Fps_Num, fps_den=Fps_Den, abs=Abs, nvof=Nvof, gpu=0)

clip.set_output()
