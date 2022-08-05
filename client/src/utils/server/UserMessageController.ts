import { ScAddr, ScNet, ScTemplate, ScTemplateSearchResult, ScType } from '@ostis/sc-core';
import { ServerKeynodes } from './ServerKeynodes';
import { ServerBase } from './ServerBase';

export class UserMessageController extends ServerBase {
    private readonly template_message_search_iterations_count: number =
        +process.env.TEMPLATE_MESSAGE_SEARCH_ITERATIONS_COUNT;
    private readonly template_message_search_max_iterations_count: number =
        +process.env.TEMPLATE_MESSAGE_SEARCH_MAX_ITERATIONS_COUNT;

    constructor(client: ScNet, keynodes: ServerKeynodes) {
        super(client, keynodes);
    }

    public async findUserMessageNode(actionNode: ScAddr): Promise<ScAddr> {
        let userMsgContent;
        const soundLinkAlias = 'sound_link';
        const template: ScTemplate = new ScTemplate();
        template.TripleWithRelation(
            actionNode,
            ScType.EdgeAccessVarPosPerm,
            [ScType.LinkVar, soundLinkAlias],
            ScType.EdgeAccessVarPosPerm,
            this.keynodes.kRrel1,
        );
        template.Triple([ScType.NodeVar, 'sound_node'], ScType.EdgeAccessVarPosPerm, soundLinkAlias);
        template.TripleWithRelation(
            'sound_node',
            ScType.EdgeDCommonVar,
            [ScType.NodeVar, 'message'],
            ScType.EdgeAccessVarPosPerm,
            this.keynodes.kNrelScTextTranslation,
        );
        const userMessage: ScTemplateSearchResult = await this.client.TemplateSearch(template);
        if (userMessage.length != 0) {
            userMsgContent = await userMessage[0].Get('message');
        }
        return new Promise((resolve) => {
            resolve(userMsgContent);
        });
    }

    public async findUserText(message: ScAddr): Promise<string> {
        let userMsgContent = '';
        let iterator = 0;
        let resolveFunction;
        const timerForFinishedArc = setInterval(async () => {
            const template: ScTemplate = new ScTemplate();
            template.TripleWithRelation(
                [ScType.NodeVar, 'text_node'],
                ScType.EdgeDCommonVar,
                message,
                ScType.EdgeAccessVarPosPerm,
                this.keynodes.kNrelScTextTranslation,
            );
            template.Triple('text_node', ScType.EdgeAccessVarPosPerm, [ScType.LinkVar, 'user_text']);
            template.Triple(this.keynodes.kConceptTextFile, ScType.EdgeAccessVarPosPerm, 'user_text');
            const userMessage: ScTemplateSearchResult = await this.client.TemplateSearch(template);
            if (userMessage.length != 0) {
                userMsgContent = await this.findLinkContent(userMessage[0].Get('user_text'));
                resolveFunction(userMsgContent);
            }
            iterator++;
            if (userMsgContent.length != 0 || iterator > this.template_message_search_iterations_count) {
                clearInterval(timerForFinishedArc);
                resolveFunction(userMsgContent);
            }
        }, this.template_search_waiting_ms_interval);

        return new Promise((resolve) => {
            resolveFunction = resolve;
        });
    }
}
