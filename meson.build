project(
    'hipopybind',
    'cpp',
    version: '2.0.0',
    license: 'MIT',
    meson_version: '>= 1.2.0',
    default_options: [
        'cpp_std=c++17',
        'buildtype=release',
    ],
)

#---------- Find python ----------#
py = import('python').find_installation(pure: false)

#---------- Add CMake subprojects ----------#
# Setup a CMake dependency
cmake = import('cmake')
opt_var = cmake.subproject_options()

# Call CMake with `-DSOME_OTHER_VAR=ON`
opt_var.add_cmake_defines({'DOWNLOAD_CATCH': true})
opt_var.add_cmake_defines({'PYBIND11_INSTALL': false})
opt_var.add_cmake_defines({'PYBIND11_TEST': false})
opt_var.set_install(false)

# Configure the CMake project
pybind11_sub = cmake.subproject('pybind11', options : opt_var)

# Fetch the dependency object
pybind11_dep = pybind11_sub.dependency('pybind11_headers')

#---------- Add meson subprojects ----------#
hipo_dep = subproject('hipo4',
                    default_options : {
                        'build_examples' : false,
                        'dataframes'     : false,
                        'prefix'         : get_option('prefix'),
                    })
hipo_dep = dependency('hipo4')

#---------- Compile Pybind11 Module ----------#
py.extension_module('hipopybind',
    'src/main.cpp',
    install: true,
    dependencies : [pybind11_dep,hipo_dep],
)
