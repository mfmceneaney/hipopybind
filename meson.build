project(
    'hipopybind',
    'cpp',
    version: '1.9.9',
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
fs = import('fs')

#---------- Find python ----------#
python = import('python').find_installation(pure: false)

# ---- Find Python and pybind11 ----
pybind11_dep = dependency('pybind11', required: true)

# ---- Try to find libhipo via pkg-config ----
libhipo_dep = dependency('libhipo4', method: 'pkg-config', required: false)

# ---- Set python install directory ----
hb_pkg_dir = python.get_install_dir() / meson.project_name()

# Set loader path
host_os = host_machine.system()
if host_os == 'darwin'
  pybind_rpath = '@loader_path/lib'
else
  # Linux and others
  pybind_rpath = '$ORIGIN'
endif

if not libhipo_dep.found()
  message('libhipo not found via pkg-config. Attempting to build from source...')

  libhipo_src_dir = meson.project_source_root() / 'hipo'
  libhipo_build_dir = meson.current_build_dir() / 'libhipo_build'
  libhipo_install_dir = meson.project_source_root()

  # Run meson setup with workaround for macos x86_64 architecture if you are building on arm64
  macos_arch = get_option('macos_arch')
  message('macos_arch = @0@'.format(macos_arch))
  if host_os == 'darwin' and macos_arch == 'x86_64'
    message('Building for macos_arch==x86_64')
    run_command('meson', 'setup', libhipo_build_dir, libhipo_src_dir,
                '--prefix=' + libhipo_install_dir,
                '--cross-file', 'cross_x86_64_macos.txt',
                env: environment(),
                check: true)
  else
    run_command('meson', 'setup', libhipo_build_dir, libhipo_src_dir,
                '--prefix=' + libhipo_install_dir,
                env: environment(),
                check: true)
  endif

  # Compile and install
  run_command('meson', 'compile', '-C', libhipo_build_dir, check: true)
  hipo_install_target = run_command('meson', 'install', '-C', libhipo_build_dir, check: true)

  # Assume libhipo_install_dir is a Meson File object or string path
  hipo_include_dir = 'include'
  lib_dir          = 'lib'
  hipo_lib_dir     = libhipo_install_dir / lib_dir
  hipo_lib_name    = 'hipo4'
  lz4_lib_name     = 'lz4'
  new_hipo_lib_name = hipo_lib_name + 'pybind11'

  # Install include directory
  install_subdir(
    hipo_include_dir,
    install_dir: hb_pkg_dir
  )
  install_subdir(
    hipo_lib_dir,
    install_dir: hb_pkg_dir
  )

  # Set file extension
  file_ext = '.dylib'
  if host_os != 'darwin'
    file_ext = '.so'
  endif

  # Copy hipo4 into main directory and rename to avoid loading conflicts
  # if another library loads libhipo4 from another place
  hipo4_path = join_paths(hipo_lib_dir, 'lib'+hipo_lib_name+file_ext)
  new_hipo_lib_fname = 'lib'+new_hipo_lib_name+file_ext
  new_hipo4_path = hipo_lib_dir / new_hipo_lib_fname
  rename_libhipo4 = custom_target(
    'rename_libhipo4',
    input : hipo4_path,   # the built library
    output: new_hipo_lib_fname,         # just a filename, no directories
    command: ['mv', '@INPUT@', '@OUTPUT@'],
    build_by_default: true,
    install_dir: host_os=='darwin' ? hb_pkg_dir / 'lib' : hb_pkg_dir ,
  )

  # Copy lz4 into main directory if it exists
  lz4_path = join_paths(hipo_lib_dir, 'lib'+lz4_lib_name+file_ext+'.1.9.4')
  if fs.is_file(lz4_path)
    install_data(
      lz4_path,
      install_dir: hb_pkg_dir
    )
  endif

  # Declare hipo dependency
  libhipo_dep = declare_dependency(
    include_directories: include_directories(hipo_include_dir),
    link_args: ['-L' + hipo_lib_dir, '-l'+new_hipo_lib_name, '-rpath', pybind_rpath],
  )
endif

# ---- Build the Python extension ----

# Install the python init script so your python installation can find the package
install_data('src/__init__.py', install_dir: hb_pkg_dir)

# Compile the shared module
pybind_module = shared_module('_core',
  'src/hipopybind_module.cpp',
  dependencies: [pybind11_dep, libhipo_dep],
  cpp_args: ['-DVERSION_INFO="@0@"'.format(meson.project_version())],
  install: true,
  install_dir: hb_pkg_dir,
  install_rpath: pybind_rpath,
  build_rpath: pybind_rpath,
  name_prefix: '',
  name_suffix: 'so',
)

# Export a dependency object for use as a subproject
hipopybind_dep = declare_dependency(
  link_with: pybind_module,
)

# Export the dependency so superprojects can access it
meson.override_dependency('hipopybind_dep', hipopybind_dep)
