file(GLOB_RECURSE SOURCES "*.cpp" "*.hpp")

add_library (SpeechToTextService SHARED ${SOURCES})

target_include_directories(SpeechToTextService PRIVATE ${SC_MEMORY_SRC})
target_link_libraries(SpeechToTextService sc-memory)

add_dependencies(SpeechToTextService sc-memory)

sc_codegen(SpeechToTextService ${CMAKE_CURRENT_LIST_DIR})
