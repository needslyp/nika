file(GLOB_RECURSE SOURCES "*.cpp" "*.hpp")

add_library (CommonTestModule SHARED ${SOURCES})

target_include_directories(CommonTestModule PRIVATE ${SC_MEMORY_SRC})
target_link_libraries(CommonTestModule sc-memory)

add_dependencies(CommonTestModule sc-memory)

sc_codegen(CommonTestModule ${CMAKE_CURRENT_LIST_DIR})
