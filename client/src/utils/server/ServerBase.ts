import {
    ScAddr,
    ScEventParams,
    ScEventType,
    ScLinkContent,
    ScNet,
    ScTemplate,
    ScTemplateSearchResult,
    ScType,
} from '@ostis/sc-core';
import { ServerKeynodes } from './ServerKeynodes';

export class ServerBase {
    private readonly _client: ScNet = null;
    private readonly _keynodes: ServerKeynodes = null;
    protected readonly template_search_iterations_count: number = +process.env.TEMPLATE_SEARCH_ITERATIONS_COUNT;
    protected readonly template_search_waiting_ms_interval: number = +process.env.TEMPLATE_SEARCH_WAITING_MS_INTERVAL;

    constructor(client: ScNet, keynodes: ServerKeynodes) {
        this._client = client;
        this._keynodes = keynodes;
    }

    public get client(): ScNet {
        return this._client;
    }

    public get keynodes(): ServerKeynodes {
        return this._keynodes;
    }

    public get host(): string {
        return location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
    }

    public async findAnswerConstruction(actionNode: ScAddr): Promise<ScTemplateSearchResult> {
        const template: ScTemplate = new ScTemplate();
        template.TripleWithRelation(
            actionNode,
            ScType.EdgeDCommonVar,
            [ScType.NodeVarStruct, 'structure'],
            ScType.EdgeAccessVarPosPerm,
            this.keynodes.kNrelAnswer,
        );
        template.Triple('structure', ScType.EdgeAccessVarPosPerm, [ScType.NodeVar, 'answer_msg']);

        template.TripleWithRelation(
            [ScType.NodeVar, 'user_msg'],
            ScType.EdgeDCommonVar,
            'answer_msg',
            ScType.EdgeAccessVarPosPerm,
            this.keynodes.kNrelReplyMessage,
        );
        const resultAnswerMsg: ScTemplateSearchResult = await this.client.TemplateSearch(template);
        return new Promise((resolve) => {
            resolve(resultAnswerMsg);
        });
    }

    public async findAnswerLink(actionNode: ScAddr, linkClass: ScAddr): Promise<ScAddr> {
        const linkAlias = 'link';
        const template: ScTemplate = new ScTemplate();
        template.TripleWithRelation(
            [ScType.NodeVar, 'translation_node'],
            ScType.EdgeDCommonVar,
            actionNode,
            ScType.EdgeAccessVarPosPerm,
            this.keynodes.kNrelScTextTranslation,
        );
        template.Triple('translation_node', ScType.EdgeAccessVarPosPerm, [ScType.LinkVar, linkAlias]);
        template.Triple(linkClass, ScType.EdgeAccessVarPosPerm, [ScType.LinkVar, linkAlias]);
        const templateResult: ScTemplateSearchResult = await this.client.TemplateSearch(template);
        let linkAddr: ScAddr = null;
        if (templateResult.length != 0) {
            linkAddr = templateResult[0].Get(linkAlias);
        }

        return new Promise((resolve) => {
            resolve(linkAddr);
        });
    }

    public async findLinkContent(link: ScAddr): Promise<string> {
        const linkContent: ScLinkContent[] = await this.client.GetLinkContents([link]);
        const contentResult: string = linkContent[0].data.toString();
        return new Promise<string>((resolve) => {
            resolve(contentResult);
        });
    }

    public waitActionFinish(actionNode: ScAddr, callback: () => void): void {
        let actionIsFinished = false;
        const onActionFinished = (subscibedAddr: ScAddr, arc: ScAddr, anotherAddr: ScAddr) => {
            if (anotherAddr.isValid() && anotherAddr.equal(this.keynodes.kQuestionFinished)) {
                actionIsFinished = true;
                callback();
            }
        };
        const eventParams: ScEventParams = new ScEventParams(actionNode, ScEventType.AddIngoingEdge, onActionFinished);
        this.client.EventsCreate([eventParams]).then((scEvents) => {
            let iterator = 0;
            const interval = setInterval(() => {
                iterator++;
                if (actionIsFinished || iterator > this.template_search_iterations_count) {
                    this.client.EventsDestroy(scEvents);
                    clearInterval(interval);
                }
            }, this.template_search_waiting_ms_interval);
        });
    }

    public async findSystemReplyMessage(actionNode: ScAddr): Promise<ScAddr> {
        const answerMessageNodeConstruction: ScTemplateSearchResult = await this.findAnswerConstruction(actionNode);
        let answerNode: ScAddr;
        if (answerMessageNodeConstruction.length > 0) {
            answerNode = answerMessageNodeConstruction[0].Get('answer_msg');
        }
        return answerNode;
    }

    public async findMessageLinkContent(messageAddr: ScAddr, linkClass: ScAddr): Promise<string> {
        const linkNode: ScAddr = await this.findAnswerLink(messageAddr, linkClass);
        return linkNode != null ? this.findLinkContent(linkNode) : Promise.resolve('');
    }

    public blobToBase64(blob: Blob): Promise<string> {
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        return new Promise<string>((resolve) => {
            reader.onloadend = () => {
                if (typeof reader.result === 'string') {
                    resolve(reader.result.split(',')[1]);
                } else resolve('');
            };
        });
    }

    public downloadBase64File(base64File: string, fileName: string): void {
        const a = document.createElement('a');
        a.href = 'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,' + base64File;
        a.download = fileName;
        a.click();
    }
}
