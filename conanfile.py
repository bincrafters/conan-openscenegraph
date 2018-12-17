#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class OpenscenegraphConan(ConanFile):
    name = "openscenegraph"
    version = "3.6.3"
    description = "OpenSceneGraph is an open source high performance 3D graphics toolkit"
    topics = ("conan", "openscenegraph", "graphics")
    url = "https://github.com/bincrafters/conan-openscenegraph"
    homepage = "https://github.com/openscenegraph/OpenSceneGraph"
    author = "Bincrafters <bincrafters@gmail.com>"
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
        "build_osg_plugins": [True, False], 
        "build_osg_examples": [True, False], 
    }
    default_options = {
        "shared": False, 
        "fPIC": True,
        "build_osg_applications": False, 
        "build_osg_plugins_by_default": False, 
        "build_osg_examples": False, 
    }
    _sha256_checksum = "51bbc79aa73ca602cd1518e4e25bd71d41a10abd296e18093a8acfebd3c62696"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = (
        "zlib/1.2.11@conan/stable",
        "freetype/2.9.0@bincrafters/stable",
        "libjpeg/9c@bincrafters/stable",
        "libxml2/2.9.8@bincrafters/stable",
        "libcurl/7.61.1@bincrafters/stable",
        "libpng/1.6.34@bincrafters/stable",
        "libtiff/4.0.9@bincrafters/stable",
        "sdl2/2.0.9@bincrafters/stable",
        "jasper/2.0.14@conan/stable",
        # "openblas/0.2.20@conan/stable", Removed until openblas is in conan center
    )
    
    def requirements(self):
        if self.settings.os != "Windows":
            self.requires("asio/1.12.0@bincrafters/stable")

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.get(
            "{0}/archive/OpenSceneGraph-{1}.tar.gz".format(self.homepage, self.version), 
            sha256=self._sha256_checksum
        )
        extracted_dir = "OpenSceneGraph-OpenSceneGraph" "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_OSG_APPLICATIONS"] = "ON" if self.options.build_osg_applications else "OFF"
        cmake.definitions["DYNAMIC_OPENSCENEGRAPH"] = "ON" if self.options.shared else "OFF"
        cmake.definitions["BUILD_OSG_PLUGINS_BY_DEFAULT"] = "ON" if self.options.build_osg_plugins_by_default else "OFF"
        cmake.definitions['BUILD_OSG_EXAMPLES '] = "ON" if self.options.build_osg_examples else "OFF"
        
        if self.settings.compiler == "Visual Studio":
            cmake.definitions['BUILD_WITH_STATIC_CRT']= "ON" if "MT" in str(self.settings.compiler.runtime) else "OFF"
        
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
