Is an agent that performs the message classification by topic with extracted arguments.

**Action class:**

`action_message_topic_classification`

**Parameters:**

1. `message node` - an element of `concept_message`;

**Libraries used:**

* [Wit.ai](https://wit.ai/) - to classify message and get entities;
* [pymorphy2](https://pymorphy2.readthedocs.io/en/stable/user/guide.html) - to get entity word normal form.

**Comment:**

* The input message must contain a text file with the text in Russian;
* The excluding entity should be formalized in knowledge base.

### Examples

Examples of an input structure:

<img src="../images/messageTopicClassificationAgentInput.png"></img>

Examples of an output structure:

<img src="../images/messageTopicClassificationAgentOutput.png"></img>

**Message classes:**

1. `concept_message_about_entity`
2. `concept_message_about_work`
3. `concept_message_about_process`
4. `concept_message_about_part`
5. `concept_message_about_process_order`
6. `concept_message_about_responsibility`
7. `concept_message_about_available_resource`
8. `concept_message_about_required_resource`
9. `concept_message_about_condition`
10. `concept_message_about_characteristic`
11. `concept_greeting_message`

**Argument:**

`rrel_entity` - Relation that connects an atomic message with the message entity

### Result

Possible result codes:

* `sc_result_ok` - the message is successfully classified or the action doesn't belong to the action_message_topic_classification.
* `sc_result_error`- internal error.
