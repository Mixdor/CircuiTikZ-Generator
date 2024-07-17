from cx_Freeze import setup, Executable

includefiles = [('images', 'lib/images'), ('list_components.txt', 'lib/list_components.txt')]

setup(
    name="Circuitikz-Generator",
    version="0.7",
    description="Tool to design electronic circuits in LaTeX",
    executables=[Executable('main.py', base=None, target_name='Circuitikz-Generator')],
    options={
        'build_exe': {
            'include_files': includefiles
        }
    }
)
