# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The program to use to edit the cache.
CMAKE_EDIT_COMMAND = /usr/bin/ccmake

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /ufs/dijkstra/Projects/somatic-mutation-caller

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /ufs/dijkstra/Projects/somatic-mutation-caller

# Include any dependencies generated for this target.
include CMakeFiles/sm_caller.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/sm_caller.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/sm_caller.dir/flags.make

CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o: CMakeFiles/sm_caller.dir/flags.make
CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o: src/smc_likelihood.c
	$(CMAKE_COMMAND) -E cmake_progress_report /ufs/dijkstra/Projects/somatic-mutation-caller/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o   -c /ufs/dijkstra/Projects/somatic-mutation-caller/src/smc_likelihood.c

CMakeFiles/sm_caller.dir/src/smc_likelihood.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/sm_caller.dir/src/smc_likelihood.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -E /ufs/dijkstra/Projects/somatic-mutation-caller/src/smc_likelihood.c > CMakeFiles/sm_caller.dir/src/smc_likelihood.c.i

CMakeFiles/sm_caller.dir/src/smc_likelihood.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/sm_caller.dir/src/smc_likelihood.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -S /ufs/dijkstra/Projects/somatic-mutation-caller/src/smc_likelihood.c -o CMakeFiles/sm_caller.dir/src/smc_likelihood.c.s

CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o.requires:
.PHONY : CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o.requires

CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o.provides: CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o.requires
	$(MAKE) -f CMakeFiles/sm_caller.dir/build.make CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o.provides.build
.PHONY : CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o.provides

CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o.provides.build: CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o

CMakeFiles/sm_caller.dir/src/smc_input.c.o: CMakeFiles/sm_caller.dir/flags.make
CMakeFiles/sm_caller.dir/src/smc_input.c.o: src/smc_input.c
	$(CMAKE_COMMAND) -E cmake_progress_report /ufs/dijkstra/Projects/somatic-mutation-caller/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object CMakeFiles/sm_caller.dir/src/smc_input.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/sm_caller.dir/src/smc_input.c.o   -c /ufs/dijkstra/Projects/somatic-mutation-caller/src/smc_input.c

CMakeFiles/sm_caller.dir/src/smc_input.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/sm_caller.dir/src/smc_input.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -E /ufs/dijkstra/Projects/somatic-mutation-caller/src/smc_input.c > CMakeFiles/sm_caller.dir/src/smc_input.c.i

CMakeFiles/sm_caller.dir/src/smc_input.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/sm_caller.dir/src/smc_input.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -S /ufs/dijkstra/Projects/somatic-mutation-caller/src/smc_input.c -o CMakeFiles/sm_caller.dir/src/smc_input.c.s

CMakeFiles/sm_caller.dir/src/smc_input.c.o.requires:
.PHONY : CMakeFiles/sm_caller.dir/src/smc_input.c.o.requires

CMakeFiles/sm_caller.dir/src/smc_input.c.o.provides: CMakeFiles/sm_caller.dir/src/smc_input.c.o.requires
	$(MAKE) -f CMakeFiles/sm_caller.dir/build.make CMakeFiles/sm_caller.dir/src/smc_input.c.o.provides.build
.PHONY : CMakeFiles/sm_caller.dir/src/smc_input.c.o.provides

CMakeFiles/sm_caller.dir/src/smc_input.c.o.provides.build: CMakeFiles/sm_caller.dir/src/smc_input.c.o

CMakeFiles/sm_caller.dir/src/smc_main.c.o: CMakeFiles/sm_caller.dir/flags.make
CMakeFiles/sm_caller.dir/src/smc_main.c.o: src/smc_main.c
	$(CMAKE_COMMAND) -E cmake_progress_report /ufs/dijkstra/Projects/somatic-mutation-caller/CMakeFiles $(CMAKE_PROGRESS_3)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object CMakeFiles/sm_caller.dir/src/smc_main.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/sm_caller.dir/src/smc_main.c.o   -c /ufs/dijkstra/Projects/somatic-mutation-caller/src/smc_main.c

CMakeFiles/sm_caller.dir/src/smc_main.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/sm_caller.dir/src/smc_main.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -E /ufs/dijkstra/Projects/somatic-mutation-caller/src/smc_main.c > CMakeFiles/sm_caller.dir/src/smc_main.c.i

CMakeFiles/sm_caller.dir/src/smc_main.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/sm_caller.dir/src/smc_main.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -S /ufs/dijkstra/Projects/somatic-mutation-caller/src/smc_main.c -o CMakeFiles/sm_caller.dir/src/smc_main.c.s

CMakeFiles/sm_caller.dir/src/smc_main.c.o.requires:
.PHONY : CMakeFiles/sm_caller.dir/src/smc_main.c.o.requires

CMakeFiles/sm_caller.dir/src/smc_main.c.o.provides: CMakeFiles/sm_caller.dir/src/smc_main.c.o.requires
	$(MAKE) -f CMakeFiles/sm_caller.dir/build.make CMakeFiles/sm_caller.dir/src/smc_main.c.o.provides.build
.PHONY : CMakeFiles/sm_caller.dir/src/smc_main.c.o.provides

CMakeFiles/sm_caller.dir/src/smc_main.c.o.provides.build: CMakeFiles/sm_caller.dir/src/smc_main.c.o

# Object files for target sm_caller
sm_caller_OBJECTS = \
"CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o" \
"CMakeFiles/sm_caller.dir/src/smc_input.c.o" \
"CMakeFiles/sm_caller.dir/src/smc_main.c.o"

# External object files for target sm_caller
sm_caller_EXTERNAL_OBJECTS =

bin/sm_caller: CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o
bin/sm_caller: CMakeFiles/sm_caller.dir/src/smc_input.c.o
bin/sm_caller: CMakeFiles/sm_caller.dir/src/smc_main.c.o
bin/sm_caller: CMakeFiles/sm_caller.dir/build.make
bin/sm_caller: /usr/lib64/libgmp.so
bin/sm_caller: CMakeFiles/sm_caller.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking C executable bin/sm_caller"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/sm_caller.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/sm_caller.dir/build: bin/sm_caller
.PHONY : CMakeFiles/sm_caller.dir/build

# Object files for target sm_caller
sm_caller_OBJECTS = \
"CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o" \
"CMakeFiles/sm_caller.dir/src/smc_input.c.o" \
"CMakeFiles/sm_caller.dir/src/smc_main.c.o"

# External object files for target sm_caller
sm_caller_EXTERNAL_OBJECTS =

CMakeFiles/CMakeRelink.dir/sm_caller: CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o
CMakeFiles/CMakeRelink.dir/sm_caller: CMakeFiles/sm_caller.dir/src/smc_input.c.o
CMakeFiles/CMakeRelink.dir/sm_caller: CMakeFiles/sm_caller.dir/src/smc_main.c.o
CMakeFiles/CMakeRelink.dir/sm_caller: CMakeFiles/sm_caller.dir/build.make
CMakeFiles/CMakeRelink.dir/sm_caller: /usr/lib64/libgmp.so
CMakeFiles/CMakeRelink.dir/sm_caller: CMakeFiles/sm_caller.dir/relink.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking C executable CMakeFiles/CMakeRelink.dir/sm_caller"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/sm_caller.dir/relink.txt --verbose=$(VERBOSE)

# Rule to relink during preinstall.
CMakeFiles/sm_caller.dir/preinstall: CMakeFiles/CMakeRelink.dir/sm_caller
.PHONY : CMakeFiles/sm_caller.dir/preinstall

CMakeFiles/sm_caller.dir/requires: CMakeFiles/sm_caller.dir/src/smc_likelihood.c.o.requires
CMakeFiles/sm_caller.dir/requires: CMakeFiles/sm_caller.dir/src/smc_input.c.o.requires
CMakeFiles/sm_caller.dir/requires: CMakeFiles/sm_caller.dir/src/smc_main.c.o.requires
.PHONY : CMakeFiles/sm_caller.dir/requires

CMakeFiles/sm_caller.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/sm_caller.dir/cmake_clean.cmake
.PHONY : CMakeFiles/sm_caller.dir/clean

CMakeFiles/sm_caller.dir/depend:
	cd /ufs/dijkstra/Projects/somatic-mutation-caller && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /ufs/dijkstra/Projects/somatic-mutation-caller /ufs/dijkstra/Projects/somatic-mutation-caller /ufs/dijkstra/Projects/somatic-mutation-caller /ufs/dijkstra/Projects/somatic-mutation-caller /ufs/dijkstra/Projects/somatic-mutation-caller/CMakeFiles/sm_caller.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/sm_caller.dir/depend

