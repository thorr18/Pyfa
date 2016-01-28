"""
Distribution builder for pyfa.
"""
import sys
import config
import requests.certs
import setuptools # already imported by Ruby installer
print "setup version: ", setuptools.__version__

APP = 'pyfa.py'
app_version = '{}'.format(config.version)
app_description = 'Python fitting assistant'

if 'darwin' in sys.platform:
    setuptools.setup(
            name=APP,
            version=app_version,
            description=app_description,
            url="https://github.com/pyfa-org/Pyfa",
            license="GNU",
            package_dir={'': '.'},
            packages=setuptools.find_packages(),
            package_data={'': ['imgs/gui/*.png','imgs/icons/*.png','imgs/renders/*.png']},
            py_modules=['config'],
            scripts=['pyfa.py'],
            #entry_points={'gui_scripts': ['pyfa = pyfa']},
            data_files=[('', ['eve.db', requests.certs.where()]),
                        ('icons', ['dist_assets/mac/pyfa.icns'])]
    )
else:
    # The modules that contain the bulk of teh source
    packages = ['eos', 'gui', 'service', 'utils']
    # Extra files that will be copied into the root directory
    include_files = ['eve.db', 'LICENSE', 'README.md', (requests.certs.where(),'cacert.pem')]
    # this is read by dist.py to package the icons
    icon_dirs = ['gui', 'icons', 'renders']

    includes = []
    #  collection.abc due to bug:
    #  https://bitbucket.org/anthony_tuininga/cx_freeze/issues/127/collectionssys-error
    # All the other stuff is crap that I have. VENV isn't working right for me for a few dependancies, so bleh
    excludes = ['Tkinter', 'collections.abc', 'IPython', 'PyQt4', 'PIL', 'nose', 'tornado', 'zmq', 'mysql', 'scipy']

    if __name__ == "__main__":
        from cx_Freeze import setup, Executable

        # Windows-specific options
        build_options_winexe = {
            'packages': packages,
            'include_files': include_files,
            'includes': includes,
            'excludes': excludes,
            'compressed': True,
            'optimize': 2,
            'include_msvcr': True,
        }

        build_options_winmsi = {
            'upgrade_code': '{E80885AC-31BA-4D9A-A04F-9E5915608A6C}',
            'add_to_path': False,
            'initial_target_dir': r'[ProgramFilesFolder]\{}'.format(app_name),
        }


        # Mac-specific options (untested)
        build_options_macapp = {
            'iconfile': 'dist_assets/mac/pyfa.icns',
            'bundle_name': app_name,
        }

        build_options_macdmg = {
            'volume_label': app_name,
            'applications-shortcut': True,
        }


        # Generic executable options
        executable_options = {
            'script': 'pyfa.py',
            # Following are windows-specific options, they are stored
            # on a per-executable basis
            'base': 'Win32GUI' if sys.platform=='win32' else None,
            'icon': 'dist_assets/win/pyfa.ico',
            'shortcutDir': 'DesktopFolder',
            'shortcutName': app_name,
        }

        setup(
            name=app_name,
            version=app_version,
            description=app_description,
            options={
                'build_exe': build_options_winexe,
                'bdist_msi': build_options_winmsi,
                'bdist_mac': build_options_macapp,
                'bdist_dmg': build_options_macdmg,
            },
            executables=[Executable(**executable_options)]
        )
