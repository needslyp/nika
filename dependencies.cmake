set(CPR_FORCE_USE_SYSTEM_CURL ON)
set(CPR_BUILD_TESTS OFF)
set(CPR_BUILD_TESTS_SSL OFF)

include(FetchContent)
FetchContent_Declare(cpr GIT_REPOSITORY https://github.com/libcpr/cpr.git
        GIT_TAG db351ffbbadc6c4e9239daaa26e9aefa9f0ec82d)
FetchContent_MakeAvailable(cpr)

# Important flag for building, cpr change this to ON
set(BUILD_SHARED_LIBS OFF)

find_package(nlohmann_json 3.7.3 REQUIRED)
