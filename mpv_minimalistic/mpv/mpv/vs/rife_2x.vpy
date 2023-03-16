### Rife v4, podwajanie klatek (wymuszone wyjście 8 bitów), wysokie wymagania wydajnościowe

import vapoursynth as vs
from vapoursynth import core
import math

input = video_in
colorlv = input.get_frame(0).props._ColorRange
fmt_src = input.format

#####################
# Opcje Użytkownika #
#####################

Max_Leng = 720
GPU = 0
GPU_t = 8
Static_th = 60.0

## Jeśli krótszy bok wideo przekracza podaną długość, zostanie ono automatycznie zmniejszone w celu poprawy wydajności kosztem jakości obrazu
	## !!!
	## Rekomendowane	->	(1080p 24fps -> 1080p 48fps): 				RTX 3080 +		~ rife_1080p_x2.vpy = rife_std.vpy
	## Minimum dla		-> 	(1080p / 720p 24fps -> 720p 48fps): 		RTX 2080 Ti +	~ rife_720p_x2.vpy = rife_2x.vpy
	## OK				->	(1080p / 720p /480p 24fps -> 480p 48fps): 	? 				~ rife_480p_x2.vpy
## Numer karty graficznej używanej do przetwarzania, z 0 oznaczającym pierwszą kartę w kolejności
## Liczba wątków procesora karty graficznej, która ma być używana do przetwarzania (orginalnie = 2)
## Próg wykrywania nieruchomych klatek, na którym nie będą wykonywane obliczenia rekompensacyjne

if container_fps > 32 :
	raise Exception("Częstotliwość klatek źródłowych przekracza dopuszczalny zakres, tymczasowo wyłączono ten skrypt.")

if input.width >= input.height :
	short_edge = input.height
	max_Leng2 = input.width*(Max_Leng/input.height)
	w_ds = max_Leng2
	h_ds = Max_Leng
else :
	short_edge = input.width
	max_Leng2 = input.height*(Max_Leng/input.width)
	w_ds = Max_Leng
	h_ds = max_Leng2

if fmt_src.subsampling_w or fmt_src.subsampling_h :
	if not (w_ds % 2 == 0) :
		w_ds = math.floor(w_ds / 2) * 2
	if not (h_ds % 2 == 0) :
		h_ds = math.floor(h_ds / 2) * 2

cut0 = core.misc.SCDetect(clip=input, threshold=0.15)

if short_edge > Max_Leng :
	cut1 = core.resize.Bicubic(clip=cut0, width=w_ds, height=h_ds, format=vs.RGBS, matrix_in_s="709")
else :
	cut1 = core.resize.Bilinear(clip=cut0, format=vs.RGBS, matrix_in_s="709")
cut2 = core.rife.RIFE(clip=cut1, model=9, factor_num=2, factor_den=1, gpu_id=GPU, gpu_thread=GPU_t, sc=True, skip=True, skip_threshold=Static_th)

output = core.resize.Bilinear(clip=cut2, format=vs.YUV420P8, matrix_s="709", range=1 if colorlv==0 else None)

output.set_output()
