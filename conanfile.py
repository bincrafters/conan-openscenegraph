from conans import ConanFile, CMake, tools
import os


class OpenscenegraphConan(ConanFile):
    name = "openscenegraph"
    version = "3.6.3"
    description = "OpenSceneGraph is an open source high performance 3D graphics toolkit"
    topics = ("conan", "openscenegraph", "graphics")
    url = "https://github.com/bincrafters/conan-openscenegraph"
    homepage = "https://github.com/openscenegraph/OpenSceneGraph"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    short_paths = True
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_osg_applications": [True, False],
        "build_osg_plugins_by_default": [True, False],
        "build_osg_examples": [True, False],
        "dynamic_openthreads": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "build_osg_applications": False,
        "build_osg_plugins_by_default": False,
        "build_osg_examples": False,
        "dynamic_openthreads": True
    }
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = (
        "zlib/1.2.11",
        "freetype/2.9.0@bincrafters/stable",
        "libjpeg/9c",
        "libxml2/2.9.9",
        "libcurl/7.67.0",
        "libpng/1.6.37",
        "libtiff/4.0.9",
        "sdl2/2.0.9@bincrafters/stable",
        "jasper/2.0.14",
        "cairo/1.17.2@bincrafters/stable",
        # "openblas/0.2.20@conan/stable", Removed until openblas is in conan center
    )

    def requirements(self):
        if self.settings.os != "Windows":
            self.requires("asio/1.13.0")

    def system_requirements(self):
        if tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                if self.settings.arch == "x86" and tools.detected_architecture() == "x86_64":
                    installer.install("gcc-multilib")
                    installer.install("libx11-dev:i386")
                    installer.install("libgl1-mesa-dev:i386")
                    installer.install("libglu1-mesa-dev:i386")
                    installer.install("libegl1-mesa-dev:i386")
                    installer.install("libgtk2.0-dev:i386")
                    installer.install("libpoppler-glib-dev:i386")
                else:
                    installer.install("libx11-dev")
                    installer.install("libgl1-mesa-dev")
                    installer.install("libglu1-mesa-dev")
                    installer.install("libegl1-mesa-dev")
                    installer.install("libgtk2.0-dev")
                    installer.install("libpoppler-glib-dev")
            elif tools.os_info.with_yum:
                installer = tools.SystemPackageTool()
                if self.settings.arch == "x86" and tools.detected_architecture() == "x86_64":
                    installer.install("glibmm24.i686")
                    installer.install("glibc-devel.i686")
                    installer.install("libGLU-devel.i686")
                else:
                    installer.install("libGLU-devel")
            else:
                self.output.warn("Could not determine Linux package manager, skipping system requirements installation.")


    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        prefix = "OpenSceneGraph"
        sha256 = "51bbc79aa73ca602cd1518e4e25bd71d41a10abd296e18093a8acfebd3c62696"
        tools.get("{0}/archive/{1}-{2}.tar.gz".format(self.homepage, prefix,self.version), sha256=sha256)
        extracted_dir = "{}-{}-".format(prefix, prefix) + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_OSG_APPLICATIONS"] = self.options.build_osg_applications
        cmake.definitions["DYNAMIC_OPENSCENEGRAPH"] = self.options.shared
        cmake.definitions["BUILD_OSG_PLUGINS_BY_DEFAULT"] = self.options.build_osg_plugins_by_default
        cmake.definitions['BUILD_OSG_EXAMPLES'] = self.options.build_osg_examples
        cmake.definitions["DYNAMIC_OPENTHREADS"] = self.options.dynamic_openthreads

        if self.settings.compiler == "Visual Studio":
            cmake.definitions['BUILD_WITH_STATIC_CRT']= "MT" in str(self.settings.compiler.runtime)

        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("rt")
        if not self.options.shared:
            self.cpp_info.defines.append("OSG_LIBRARY_STATIC=1")
