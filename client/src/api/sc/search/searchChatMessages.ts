import { ScAddr, ScTemplate, ScType } from 'ts-sc-client';
import { client } from '../client';

const rrel1 = 'rrel_1';
const nrelAuth = 'nrel_authors';
const nrelScTextTranslation = 'nrel_sc_text_translation';
const conceptPatient = 'concept_patient';
const conceptAssistant = 'concept_assistant';
const nrelMessageSequence = 'nrel_message_sequence';
const rrelLast = 'rrel_last';
const exactValue = 'exact_value';
const begin = 'begin';
const nrelTimestampMeasurement = 'nrel_timestamp_measurement';
const attachment = 'nrel_attachments';

const baseKeynodes = [
    { id: rrel1, type: ScType.NodeConstRole },
    { id: nrelAuth, type: ScType.NodeConstNoRole },
    { id: nrelScTextTranslation, type: ScType.NodeConstNoRole },
    { id: conceptPatient, type: ScType.NodeConstClass },
    { id: conceptAssistant, type: ScType.NodeConstClass },
    { id: nrelMessageSequence, type: ScType.NodeConstNoRole },
    { id: rrelLast, type: ScType.NodeConstRole },
    { id: exactValue, type: ScType.NodeConstClass },
    { id: begin, type: ScType.NodeConstClass },
    { id: nrelTimestampMeasurement, type: ScType.NodeConstNoRole },
    { id: attachment, type: ScType.NodeConstNoRole },
];

interface IMessage {
    text: string | number;
    author: ScAddr;
    id: number;
    time: string | number;
    date: string;
    attachment?: string;
    addr: ScAddr;
}

const findLastMessageNode = async (chatNode: ScAddr, keynodes: Record<string, ScAddr>) => {
    const messagesClassNodeAlias = '_messages_node';
    const template = new ScTemplate();

    template.tripleWithRelation(
        chatNode,
        ScType.EdgeAccessVarPosPerm,
        [ScType.NodeVar, messagesClassNodeAlias],
        ScType.EdgeAccessVarPosPerm,
        keynodes[rrelLast],
    );
    const resultMessagesClassNode = await client.templateSearch(template);
    if (resultMessagesClassNode.length) {
        return resultMessagesClassNode[0].get(messagesClassNodeAlias);
    }
    return null;
};
const findCurrentEdge = async (chatNode: ScAddr, messageNode: ScAddr) => {
    const currentEdgeAlias = '_current_edge';

    const template = new ScTemplate();
    template.triple(chatNode, [ScType.EdgeAccessVarPosPerm, currentEdgeAlias], messageNode);
    const resultLastMessageEdge = await client.templateSearch(template);
    console.log({ resultLastMessageEdge });

    if (resultLastMessageEdge.length) {
        return resultLastMessageEdge[0].get(currentEdgeAlias);
    }
    return null;
};

const findPreviousMessageNode = async (chatNode: ScAddr, currentEdge: ScAddr) => {
    const previousMessageClassAlias = '_privious_message_class';

    const templatePreviousMessageClass = new ScTemplate();
    templatePreviousMessageClass.triple(chatNode, currentEdge, [ScType.NodeVar, previousMessageClassAlias]);

    const resultNextMessageClassEdge = await client.templateSearch(templatePreviousMessageClass);
    if (resultNextMessageClassEdge.length) {
        return resultNextMessageClassEdge[0].get(previousMessageClassAlias);
    }
    return null;
};
const findPreviousEdge = async (chatNode: ScAddr, keynodes: Record<string, ScAddr>, currrentMessageNode: ScAddr) => {
    const nextMessageEdgeAlias = '_previous_message_edge';
    const currentMessageEdgeAlias = '_previous_message_example_edge';

    const templateNextEdge = new ScTemplate();

    templateNextEdge.triple(chatNode, [ScType.EdgeAccessVarPosPerm, nextMessageEdgeAlias], ScType.NodeVar);
    templateNextEdge.triple(chatNode, [ScType.EdgeAccessVarPosPerm, currentMessageEdgeAlias], currrentMessageNode);
    templateNextEdge.tripleWithRelation(
        nextMessageEdgeAlias,
        ScType.EdgeDCommonVar,
        currentMessageEdgeAlias,
        ScType.EdgeAccessVarPosPerm,
        keynodes[nrelMessageSequence],
    );

    const resultNextMessageClassEdge = await client.templateSearch(templateNextEdge);
    if (resultNextMessageClassEdge.length) {
        return resultNextMessageClassEdge[0].get(nextMessageEdgeAlias);
    }
    return null;
};

export const getInfoMessage = async (messagesNode: ScAddr, keynodes: Record<string, ScAddr>, attachment?: string) => {
    const messageNodeAlias = '_message_node';
    const authorNodeAlias = '_author_node';
    const textNodeAlias = '_text_node';
    const timeNodeAlias = '_time_node';
    const timeAlias = '_time';

    const template = new ScTemplate();

    template.tripleWithRelation(
        [ScType.NodeVar, messageNodeAlias],
        ScType.EdgeDCommonVar,
        messagesNode,
        ScType.EdgeAccessVarPosPerm,
        keynodes[nrelScTextTranslation],
    );
    template.triple(messageNodeAlias, ScType.EdgeAccessVarPosPerm, [ScType.LinkVar, textNodeAlias]);

    template.tripleWithRelation(
        messagesNode,
        ScType.EdgeDCommonVar,
        [ScType.NodeVar, authorNodeAlias],
        ScType.EdgeAccessVarPosPerm,
        keynodes[nrelAuth],
    );

    template.triple([ScType.NodeVarClass, timeNodeAlias], ScType.EdgeAccessVarPosPerm, messagesNode);
    template.triple(keynodes[exactValue], ScType.EdgeAccessVarPosPerm, timeNodeAlias);
    template.triple(keynodes[begin], ScType.EdgeAccessVarPosPerm, timeNodeAlias);

    template.tripleWithRelation(
        timeNodeAlias,
        ScType.EdgeDCommonVar,
        [ScType.LinkVar, timeAlias],
        ScType.EdgeAccessVarPosPerm,
        keynodes[nrelTimestampMeasurement],
    );

    const result = await client.templateSearch(template);

    if (!result.length) return;

    const linkNode = result[0].get(textNodeAlias);

    const resultText = await client.getLinkContents([linkNode]);
    const text = resultText[0].data;

    const author = result[0].get(authorNodeAlias);

    const nodeTime = result[0].get(timeAlias);
    const infoTime = await client.getLinkContents([nodeTime]);

    const [, fullTime] = infoTime[0].data.toString().split(' ');
    const [hour, minute] = fullTime.split(':');
    const time = `${hour}:${minute}`;

    const [date] = infoTime[0].data.toString().split(' ');

    return { id: linkNode.value, text, author, time, date, attachment, addr: messagesNode };
};

export const getImage = async (messageNode: ScAddr, keynodes: Record<string, ScAddr>) => {
    const attachmentAlias = '_attachment';
    const attachmentLinkAlias = '_attachment_link';
    const template = new ScTemplate();
    template.tripleWithRelation(
        messageNode,
        ScType.EdgeDCommonVar,
        [ScType.NodeVar, attachmentAlias],
        ScType.EdgeAccessVarPosPerm,
        keynodes[attachment],
    );
    template.triple(attachmentAlias, ScType.EdgeAccessVarPosPerm, [ScType.LinkVar, attachmentLinkAlias]);

    const result = await client.templateSearch(template);

    if (result.length) {
        const attachmentLink = result[0].get(attachmentLinkAlias);
        const attachmentImg = await client.getLinkContents([attachmentLink]);
        const resultAttach = attachmentImg[0].data;

        return resultAttach ? String(resultAttach) : undefined;
    }
    return undefined;
};

const checkRrel1 = async (keynodes: Record<string, ScAddr>, chatNode: ScAddr, messageNode: ScAddr) => {
    const template = new ScTemplate();
    template.tripleWithRelation(
        chatNode,
        ScType.EdgeAccessVarPosPerm,
        messageNode,
        ScType.EdgeAccessVarPosPerm,
        keynodes[rrel1],
    );
    const result = await client.templateSearch(template);

    return !!result.length;
};

const getFirstMessages = async (
    chatNode: ScAddr,
    keynodes: Record<string, ScAddr>,
    amount: number,
    lastMessageScAddr?: ScAddr,
) => {
    const messages: IMessage[] = [];
    const defaultReturn = { messages: [], shouldEnd: false };
    let count = 0;
    let currentMessagesNode = lastMessageScAddr || (await findLastMessageNode(chatNode, keynodes));

    if (!currentMessagesNode) return defaultReturn;

    let currentEdge = await findCurrentEdge(chatNode, currentMessagesNode);

    if (!currentEdge) return defaultReturn;

    const lastAttachment = await getImage(currentMessagesNode, keynodes);
    const lastMessage = await getInfoMessage(currentMessagesNode, keynodes, lastAttachment);
    if (!lastMessage) return defaultReturn;
    if (!lastMessageScAddr) messages.push(lastMessage);

    while (count < amount) {
        count++;
        if (!currentMessagesNode) break;
        currentEdge = await findPreviousEdge(chatNode, keynodes, currentMessagesNode);

        if (!currentEdge) break;

        currentMessagesNode = await findPreviousMessageNode(chatNode, currentEdge);

        if (!currentMessagesNode) break;

        const attachment = await getImage(currentMessagesNode, keynodes);
        const message = await getInfoMessage(currentMessagesNode, keynodes, attachment);
        if (!message) break;
        messages.unshift(message);
    }
    const shouldEnd = messages[0] ? await checkRrel1(keynodes, chatNode, messages[0].addr) : true;

    return { messages, shouldEnd };
};

export const searchChatMessages = async (chatNode: ScAddr, ammount: number, lastMessageScAddr?: ScAddr) => {
    const keynodes = await client.resolveKeynodes(baseKeynodes);
    return await getFirstMessages(chatNode, keynodes, ammount, lastMessageScAddr);
};
