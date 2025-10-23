project(
    'hipopybind',
    'cpp',
    version: '2.0.0',
    license: 'MIT',
    meson_version: '>= 1.2.0',
    default_options: [
        'cpp_std=c++17',
        'buildtype=release',
        'python.install_env=auto',
    ],
)

# meson modules
pkg = import('pkgconfig')

#---------- Find python ----------#
python = import('python').find_installation(pure: false)

# ---- Find Python and pybind11 ----
pybind11_dep = dependency('pybind11', required: true)

# ---- Try to find libhipo via pkg-config ----
libhipo_dep = dependency('libhipo', method: 'pkg-config', required: false)

# ---- Set python install directory ----
hb_pkg_dir = python.get_install_dir() / 'hipopybind'

if not libhipo_dep.found()
  message('libhipo not found via pkg-config. Attempting to build from source...')

  # Set paths for meson
  libhipo_src_dir     = meson.project_source_root() / 'hipo'
  libhipo_build_dir   = meson.current_build_dir() / 'libhipo_build'
  libhipo_install_dir = hb_pkg_dir

  # Run meson setup
  run_command('meson', 'setup', libhipo_build_dir, libhipo_src_dir,
              '--prefix=' + libhipo_install_dir,
              check: true)

  # Compile and install
  run_command('meson', 'compile', '-C', libhipo_build_dir, check: true)
  run_command('meson', 'install', '-C', libhipo_build_dir, check: true)

  # Assume libhipo_install_dir is a Meson File object or string path
  hipo_lib_name    = 'hipo4'
  hipo_include_dir = 'hipo' / hipo_lib_name
  hipo_lib_dir     = libhipo_install_dir / 'lib'

  libhipo_dep = declare_dependency(
    include_directories: include_directories(hipo_include_dir),
    link_args: ['-L' + hipo_lib_dir, '-l' + hipo_lib_name]
  )

endif

# ---- Build the Python extension ----
host_os = host_machine.system()
if host_os == 'darwin'
  pybind_rpath = '@loader_path/lib'
else
  # Linux and others
  pybind_rpath = '$ORIGIN/lib'
endif
install_data('src/__init__.py', install_dir: hb_pkg_dir)
pybind_module = python.extension_module('_core',
  'src/hipopybind_module.cpp',
  dependencies: [pybind11_dep, libhipo_dep],
  cpp_args: ['-DVERSION_INFO="@0@"'.format(meson.project_version())],
  install: true,
  install_dir: hb_pkg_dir,
  install_rpath: pybind_rpath,
)
