import {
    ScAddr,
    ScConstruction,
    ScLinkContent,
    ScLinkContentType,
    ScNet,
    ScTemplate,
    ScTemplateResult,
    ScTemplateSearchResult,
    ScType,
} from '@ostis/sc-core';
import { ServerKeynodes } from './ServerKeynodes';
import { ServerBase } from './ServerBase';

export class ServerUtils extends ServerBase {
    constructor(client: ScNet, keynodes: ServerKeynodes) {
        super(client, keynodes);
    }

    public async DoSearch(scsTempl: string): Promise<ScTemplateSearchResult> {
        const searchResult: ScTemplateSearchResult = await this.client.TemplateSearch(scsTempl);

        return new Promise<ScTemplateSearchResult>(function (resolve) {
            resolve(searchResult);
        });
    }

    public async GenerateActionNode(actionClass: ScAddr, params: ScAddr[]): Promise<ScAddr> {
        const actionNodeAlias = '_action_node';
        const template: ScTemplate = new ScTemplate();
        template.Triple(actionClass, ScType.EdgeAccessVarPosPerm, [ScType.NodeVar, actionNodeAlias]);
        template.Triple(this.keynodes.kQuestion, ScType.EdgeAccessVarPosPerm, actionNodeAlias);
        template.TripleWithRelation(
            actionNodeAlias,
            ScType.EdgeDCommonVar,
            this.keynodes.kTestUser,
            ScType.EdgeAccessVarPosPerm,
            this.keynodes.kNrelAuthors,
        );
        params.forEach((param, index) => {
            if (index < 3) {
                template.TripleWithRelation(
                    actionNodeAlias,
                    ScType.EdgeAccessVarPosPerm,
                    params[index],
                    ScType.EdgeAccessVarPosPerm,
                    this.keynodes.kRrel1,
                );
            }
        });
        const generationResult: ScTemplateResult = await this.client.TemplateGenerate(template, {});
        let actionNode = new ScAddr();
        if (generationResult.size > 0) {
            actionNode = generationResult.Get(actionNodeAlias);
        }
        return Promise.resolve(actionNode);
    }

    public async GenerateMessageTextLink(linkContent: string): Promise<ScAddr> {
        const linkAlias = 'link';
        const construction: ScConstruction = new ScConstruction();
        construction.CreateLink(ScType.LinkConst, new ScLinkContent(linkContent, ScLinkContentType.String), linkAlias);
        construction.CreateEdge(ScType.EdgeAccessConstPosPerm, this.keynodes.kConceptTextFile, linkAlias);
        construction.CreateEdge(ScType.EdgeAccessConstPosPerm, this.keynodes.kLangRu, linkAlias);
        const result: ScAddr[] = await this.client.CreateElements(construction);
        return Promise.resolve(result[0]);
    }

    public async GenerateMessageSoundLink(linkContent: string): Promise<ScAddr> {
        const linkAlias = 'link';
        const construction: ScConstruction = new ScConstruction();
        construction.CreateLink(ScType.LinkConst, new ScLinkContent(linkContent, ScLinkContentType.String), linkAlias);
        construction.CreateEdge(ScType.EdgeAccessConstPosPerm, this.keynodes.kLangRu, linkAlias);
        construction.CreateEdge(ScType.EdgeAccessConstPosPerm, this.keynodes.kConceptSoundFile, linkAlias);
        construction.CreateEdge(ScType.EdgeAccessConstPosPerm, this.keynodes.kFormatWav, linkAlias);

        const result: ScAddr[] = await this.client.CreateElements(construction);
        return Promise.resolve(result[0]);
    }

    public async InitMessageReplyAction(text: string, isSound: boolean): Promise<ScAddr> {
        const linkAddr: ScAddr = await (isSound
            ? this.GenerateMessageSoundLink(text)
            : this.GenerateMessageTextLink(text));
        const actionNode = await this.GenerateActionNode(this.keynodes.kActionReplyToMessage, [linkAddr]);
        const construction: ScConstruction = new ScConstruction();
        construction.CreateEdge(ScType.EdgeAccessConstPosPerm, this.keynodes.kQuestionInitiated, actionNode);
        await this.client.CreateElements(construction);
        return Promise.resolve(actionNode);
    }
}
