### Rife v4, wypełnianie klatek, bardzo wysokie wymagania wydajnościowe

import vapoursynth as vs
from vapoursynth import core

input = video_in
colorlv = input.get_frame(0).props._ColorRange
fmt_in = input.format.id

#####################
# Opcje Użytkownika #
#####################

FPS_num = 2
FPS_den = 1
GPU = 0
GPU_t = 8

## Wartość FPS_num/FPS_den to wielokrotność częstotliwości klatek (licznik i mianownik muszą być liczbami całkowitymi, a wynik obliczeń może być liczbą zmiennoprzecinkową; obsługiwane tylko w modelu v4) 2/1 = fps x 2
## .
## Numer karty graficznej używanej do przetwarzania, z 0 oznaczającym pierwszą kartę w kolejności
## Liczba wątków procesora karty graficznej, która ma być używana do przetwarzania (orginalnie = 2)

if container_fps > 32 :
	raise Exception("Częstotliwość klatek źródłowych przekracza dopuszczalny zakres, tymczasowo wyłączono ten skrypt.")

cut0 = core.misc.SCDetect(clip=input, threshold=0.15)

cut1 = core.resize.Bilinear(clip=cut0, format=vs.RGBS, matrix_in_s="709")
cut2 = core.rife.RIFE(clip=cut1, model=9, factor_num=FPS_num, factor_den=FPS_den, gpu_id=GPU, gpu_thread=GPU_t, sc=True, skip=True, skip_threshold=60.0)

output = core.resize.Bilinear(clip=cut2, format=fmt_in, matrix_s="709", range=1 if colorlv==0 else None)

output.set_output()
