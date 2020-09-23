from distutils.core import setup
from Cython.Compiler import Options
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

Options.embed = "main"

setup(
	name="layers",
	cmdclass={'build_ext': build_ext},
	ext_modules=cythonize(
		'src/main.py',
		include_path=["src/"],
		build_dir="build/",
		language_level = "3"
	),
)

