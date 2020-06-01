@set DIR="%cd%"

@for /R %DIR% %%f in (*.tga) do ( 
@texconv.exe -dxt5 -file %%f
)

md dds
copy *.dds .\dds\