Is an agent that translates the sound of a message into text, binds it to the message through the appropriate relation. If the text file associated with the message already exists, then the translation is not performed. The message has translation into a `sound file` that has a `language`.

**Action class:**

`action_recognize_text`
 
**Parameters:**

1. `message node` - an element of `concept_message`.

**Libraries used:**

* [Azure-cognitiveservices-speech](https://docs.microsoft.com/en-us/azure/?product=featured) version 1.13.0.

### Example

Example of an input structure:

<img src="../images/speechToTextAgentInput.png"></img>

Example of an output structure:

<img src="../images/speechToTextAgentOutput.png"></img>

### Result

Possible result codes:

* `sc_result_ok` - text message generated;
* `sc_result_error` - internal error.
