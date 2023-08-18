for /f %%i in ('dir *.toml /b') do (
    kimaridraw %%i < draw.txt > NUL
)