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
  run_command('meson', 'install', '-C', libhipo_build_dir, check: true)

  # Assume libhipo_install_dir is a Meson File object or string path
  hipo_include_dir = 'include'
  hipo_lib_dir     = libhipo_install_dir / 'lib'
  hipo_lib_name    = 'hipo4'
  install_subdir(
    hipo_include_dir,
    install_dir: hb_pkg_dir
  )
  install_subdir(
    hipo_lib_dir,
    install_dir: hb_pkg_dir
  )
  if host_os != 'darwin'
    install_data(
      hipo_lib_dir / 'libhipo4.so',
      install_dir: hb_pkg_dir
    )
    run_command('ls', '-lrth', hipo_lib_dir, check: true)
    lz4_path = hipo_lib_dir / 'liblz4.so.1.9.4'
    if fs.is_file(lz4_path)
      install_data(
        lz4_path,
        install_dir: hb_pkg_dir,
        rename: 'liblz4.so'
      )
    endif
  endif
  libhipo_dep = declare_dependency(
    include_directories: include_directories(hipo_include_dir),
    link_args: ['-L' + hipo_lib_dir, '-l' + hipo_lib_name]
  )
endif

# ---- Build the Python extension ----

# Install the python init script so your python installation can find the package
install_data('src/__init__.py', install_dir: hb_pkg_dir)

# Set link args to include GNU libstdc++ and libgcc on linux
link_args = []
if host_os != 'darwin'
  link_args += ['-static-libstdc++', '-static-libgcc']
endif

# Compile the shared module
pybind_module = shared_module('_core',
  'src/hipopybind_module.cpp',
  dependencies: [pybind11_dep, libhipo_dep],
  cpp_args: ['-DVERSION_INFO="@0@"'.format(meson.project_version())],
  link_args: link_args,
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
