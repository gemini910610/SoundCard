# SoundCard
## library need to install
```cmd
pip install matplotlib
pip install soundcard
```
## steps of converting signal into octave bands
referenced from [LINK](https://www.youtube.com/watch?v=4Otqdwql63c)
1. 1024 samples of signal
2. numpy.fft.rfft() to convert into 513 complex elements
3. remove last element
4. numpy.abs() to convert into 512 amplitudes
5. convert into 10 octave bands
## octave band
Octave-and-one-third-octave-bands.png is from [LINK](https://www.researchgate.net/figure/Octave-and-one-third-octave-bands_fig1_318659078)
![](Octave-and-one-third-octave-bands.png)
