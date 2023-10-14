### Strategia wypełniania klatek typu 'konserwatywna' w mvtools, o średnich kosztach obliczeniowych
### MOD of https://gist.github.com/KCCat/1b3a7b7f085a066af3719859f88ded02

import vapoursynth as vs
from vapoursynth import core

input = video_in
vs_api = vs.__api_version__.api_major

#####################
# Opcje Użytkownika #
#####################

FPS_target = 170 # Zmiana z mvtools_std.vpy

## Parametr docelowej częstotliwości klatek wyjściowych, na przykład 60 fps. Wartości specjalne to: 'display_fps/2' oznacza docelową częstotliwość równą połowie częstotliwości odświeżania ekranu, a 'container_fps*2' oznacza podwójną częstotliwość klatek źródłowych. Używanie bardzo wysokich częstotliwości klatek może prowadzić do zwiększenia zużycia energii i powstawania artefaktów. Dla wyświetlaczy o częstotliwości odświeżania 144 Hz zalecana jest docelowa częstotliwość klatek do 72 fps, a pozostałe klatki można wygenerować za pomocą opcji 'frame blending compensation' (--interpolation)

if container_fps > 32 :
	raise Exception("Częstotliwość klatek źródłowych przekracza dopuszczalny zakres, tymczasowo wyłączono ten skrypt.")

def ffps(fps) :
	rfps = int('%.0f' % fps)
	if ( abs(fps - (rfps/1.001)) < abs(fps - (rfps/1.000)) ) :
		vfps, vden = rfps*1000, 1001
	else :
		vfps, vden = rfps*1000, 1000
	return vfps, vden

vfps, vden = ffps(container_fps)
cut1 = core.std.AssumeFPS(input, fpsnum=int(vfps), fpsden=vden)
cut_s = core.mv.Super(clip=cut1, sharp=1, rfilter=4)

if vs_api >=4 :
	cut_b = core.mv.Analyse(super=cut_s, blksize=64, searchparam=0, pelsearch=3, isb=True, lambda_=0, lsad=10000, overlapv=16, badrange=0, search_coarse=4)
	cut_f = core.mv.Analyse(super=cut_s, blksize=64, searchparam=0, pelsearch=3, lambda_=0, lsad=10000, overlapv=16, badrange=0, search_coarse=4)
else :
	cut_b = core.mv.Analyse(super=cut_s, blksize=64, searchparam=0, pelsearch=3, isb=True, _lambda=0, lsad=10000, overlapv=16, badrange=0, search_coarse=4)
	cut_f = core.mv.Analyse(super=cut_s, blksize=64, searchparam=0, pelsearch=3, _lambda=0, lsad=10000, overlapv=16, badrange=0, search_coarse=4)

output = core.mv.BlockFPS(clip=cut1, super=cut_s, mvbw=cut_b, mvfw=cut_f, num=FPS_target * 1000, den=vden, mode=2, thscd1=970, thscd2=255, blend=False)

output.set_output()
