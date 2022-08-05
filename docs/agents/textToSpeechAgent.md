Is an agent that generates the voicing of the message text and associates it with the relation "nrel_sc_text_translation". The generated voicing represents sc-link with sound file `saved in Base64 encoding`.

**Action class:**

`action_synthesize_speech`

**Parameters:**

1. `message node` - an element of `concept_message`;

**Comment:**

* The message `language` class is optional because the text language is specified by the class to which the `text link` belongs; 
* There is no explicit answer, the agent completes the description of the message in the knowledge base with its voice acting.

**Libraries used:**

* [Azure-cognitiveservices-speech](https://docs.microsoft.com/en-us/azure/?product=featured) version 1.13.0;
* [AWS Polly](https://docs.aws.amazon.com/kindle/index.html).

### Example

**Example 1**

Example of an input structure when the argument is not dynamic:

<img src="../images/textToSpeechAgentInputArgumNotDynamic.png"></img>

Example of an output structure when the argument is not dynamic:

<img src="../images/textToSpeechAgentOutputArgumNotDynamic.png"></img>

**Example 2**

Example of an input structure when the argument is dynamic:

<img src="../images/textToSpeechAgentInputArgumDynamic.png"></img>

Example of an output structure when the argument is dynamic:

<img src="../images/textToSpeechAgentOutputArgumDynamic.png"></img>

### Result

Possible result codes:
 
* `sc_result_ok` sound response created;
* `sc_result_error`- internal error.
