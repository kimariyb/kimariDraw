set "multiwfn_path=d:\environment\Multiwfn\Multiwfn.exe"

for /f %%i in ('dir *.out /b') do (
    %multiwfn_path% %%i < commands.txt > NUL
    rename spectrum_curve.txt %%~ni.txt
)
del spectrum_line.txt
del spectrum_curve.txt