file(GLOB_RECURSE SOURCES "*.cpp" "*.hpp")

add_library (TextToSpeechService SHARED ${SOURCES})

target_include_directories(TextToSpeechService PRIVATE ${SC_MEMORY_SRC})
target_link_libraries(TextToSpeechService sc-memory)

add_dependencies(TextToSpeechService sc-memory)

sc_codegen(TextToSpeechService ${CMAKE_CURRENT_LIST_DIR})
