file(GLOB_RECURSE SOURCES "*.cpp" "*.hpp")

add_library (MessageClassificationModule SHARED ${SOURCES})

target_include_directories(MessageClassificationModule PRIVATE ${SC_MEMORY_SRC})
target_link_libraries(MessageClassificationModule sc-memory)

add_dependencies(MessageClassificationModule sc-memory)

sc_codegen(MessageClassificationModule ${CMAKE_CURRENT_LIST_DIR})
