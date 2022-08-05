add_subdirectory(SpeechToTextAgent)
add_subdirectory(TextToSpeechAgent)
add_subdirectory(MessageClassificationModule)

if (${SC_BUILD_TESTS})
	add_subdirectory(CommonTestModule)
endif ()
