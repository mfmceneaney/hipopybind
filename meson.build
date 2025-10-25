project(
    'hipopybind',
    'cpp',
    version: '2.0.0',
    license: 'MIT',
    meson_version: '>=1.2',
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
libhipo_dep = dependency('libhipo4', method: 'pkg-config', required: false)

# ---- Set python install directory ----
hb_pkg_dir = python.get_install_dir() / 'hipopybind'

# Set loader path
host_os = host_machine.system()
if host_os == 'darwin'
  pybind_rpath = '@loader_path/lib'
else
  # Linux and others
  pybind_rpath = '$ORIGIN/lib'
endif

# If no pkg-config is found
if not libhipo_dep.found()
  message('libhipo not found via pkg-config. Assuming ./install_hipo.sh has already been run...')

  # Assume hipo is already installed locally in the source project
  hipo_lib_name    = 'hipo4'
  hipo_include_dir = 'hipo' / hipo_lib_name
  hipo_lib_dir     = meson.project_source_root() / 'lib'

  libhipo_dep = declare_dependency(
    include_directories: include_directories(hipo_include_dir),
    link_args: ['-L' + hipo_lib_dir, '-l' + hipo_lib_name]
  )

  # Install arbitrary data directory into the Python package
  install_subdir(
    'lib',
    install_dir: hb_pkg_dir
  )
  install_subdir(
    'include',
    install_dir: hb_pkg_dir
  )

endif

# ---- Build the Python extension ----
install_data('src/__init__.py', install_dir: hb_pkg_dir)
pybind_module = python.extension_module('_core',
  'src/hipopybind_module.cpp',
  dependencies: [pybind11_dep, libhipo_dep],
  cpp_args: ['-DVERSION_INFO="@0@"'.format(meson.project_version())],
  install: true,
  install_dir: hb_pkg_dir,
  install_rpath: pybind_rpath,
)

# Export a dependency object for use as a subproject
hipopybind_dep = declare_dependency(
  link_with: pybind_module,
)

# Export the dependency so superprojects can access it
meson.override_dependency('hipopybind_dep', hipopybind_dep)
