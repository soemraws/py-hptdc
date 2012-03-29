all : hptdc_wrapper.dll

hptdc_wrapper.dll : hptdc_wrapper.cpp
  cl /I"C:\Program Files\HPTDC8-PCI\driver" /DWIN32 /DEXPORTING hptdc_wrapper.cpp /EHsc /LD /link "C:\Program Files\HPTDC8-PCI\driver\hptdc_driver.lib"

clean :
  del hptdc_wrapper.dll hptdc_wrapper.obj hptdc_wrapper.exp
