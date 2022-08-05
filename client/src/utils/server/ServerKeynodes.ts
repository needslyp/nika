import { ResolveIdtfMap, ScAddr, ScIdtfResolveParams, ScNet, ScType } from '@ostis/sc-core';

const sNrelSystemIdentifier = 'nrel_system_identifier';
const sQuestion = 'question';
const sQuestionInitiated = 'question_initiated';
const sActionReplyToMessage = 'action_reply_to_message';
const sFormatWav = 'format_wav';
const sFormatM4a = 'format_m4a';
const sLangEn = 'lang_en';
const sLangRu = 'lang_ru';
const sNrelAuthors = 'nrel_authors';
const sRrel1 = 'rrel_1';
const sRrel2 = 'rrel_2';
const sRrel3 = 'rrel_3';
const sConceptSoundFile = 'concept_sound_file';
const sConceptTextFile = 'concept_text_file';
const sQuestionFinished = 'question_finished';
const sQuestionFinishedSuccessfully = 'question_finished_successfully';
const sNrelAnswer = 'nrel_answer';
const sNrelReplyMessage = 'nrel_reply';
const sNrelScTextTranslation = 'nrel_sc_text_translation';

// Test
const sTestUser = 'test_user';

export class ServerKeynodes {
    private _client: ScNet = null;

    private _kNrelSystemIdentifier: ScAddr = null;
    private _kQuestion: ScAddr = null;
    private _kQuestionInitiated: ScAddr = null;
    private _kActionReplyToMessage: ScAddr = null;
    private _kFormatWav: ScAddr = null;
    private _kFormatM4a: ScAddr = null;
    private _kLangEn: ScAddr = null;
    private _kLangRu: ScAddr = null;
    private _kNrelAuthors: ScAddr = null;
    private _kRrel1: ScAddr = null;
    private _kRrel2: ScAddr = null;
    private _kRrel3: ScAddr = null;
    private _kConceptSoundFile: ScAddr = null;
    private _kConceptTextFile: ScAddr = null;
    private _kQuestionFinished: ScAddr = null;
    private _kQuestionFinishedSuccessfully: ScAddr = null;
    private _kNrelAnswers: ScAddr = null;
    private _kNrelReplyMessage: ScAddr = null;
    private _kNrelScTextTranslation: ScAddr = null;

    // test
    private _kTestUser: ScAddr = null;

    constructor(client: ScNet) {
        this._client = client;
    }

    public async Initialize(): Promise<boolean> {
        const self = this;
        return new Promise<boolean>(function (resolve) {
            const keynodesList: ScIdtfResolveParams[] = [
                { idtf: sNrelSystemIdentifier, type: ScType.Unknown },
                { idtf: sQuestion, type: ScType.Unknown },
                { idtf: sQuestionInitiated, type: ScType.Unknown },
                { idtf: sActionReplyToMessage, type: ScType.Unknown },
                { idtf: sFormatWav, type: ScType.Unknown },
                { idtf: sFormatM4a, type: ScType.Unknown },
                { idtf: sLangEn, type: ScType.Unknown },
                { idtf: sLangRu, type: ScType.Unknown },
                { idtf: sNrelAuthors, type: ScType.Unknown },
                { idtf: sRrel1, type: ScType.Unknown },
                { idtf: sRrel2, type: ScType.Unknown },
                { idtf: sRrel3, type: ScType.Unknown },
                { idtf: sConceptSoundFile, type: ScType.Unknown },
                { idtf: sConceptTextFile, type: ScType.Unknown },
                { idtf: sQuestionFinished, type: ScType.Unknown },
                { idtf: sQuestionFinishedSuccessfully, type: ScType.Unknown },
                { idtf: sNrelAnswer, type: ScType.Unknown },
                { idtf: sNrelReplyMessage, type: ScType.Unknown },
                { idtf: sNrelScTextTranslation, type: ScType.Unknown },

                { idtf: sTestUser, type: ScType.NodeConst },
            ];

            self._client.ResolveKeynodes(keynodesList).then(function (res: ResolveIdtfMap) {
                self._kNrelSystemIdentifier = res[sNrelSystemIdentifier];
                self._kQuestion = res[sQuestion];
                self._kQuestionInitiated = res[sQuestionInitiated];
                self._kActionReplyToMessage = res[sActionReplyToMessage];
                self._kFormatWav = res[sFormatWav];
                self._kFormatM4a = res[sFormatM4a];
                self._kLangEn = res[sLangEn];
                self._kLangRu = res[sLangRu];
                self._kNrelAuthors = res[sNrelAuthors];
                self._kRrel1 = res[sRrel1];
                self._kRrel2 = res[sRrel2];
                self._kRrel3 = res[sRrel3];
                self._kConceptSoundFile = res[sConceptSoundFile];
                self._kConceptTextFile = res[sConceptTextFile];
                self._kQuestionFinished = res[sQuestionFinished];
                self._kQuestionFinishedSuccessfully = res[sQuestionFinishedSuccessfully];
                self._kNrelAnswers = res[sNrelAnswer];
                self._kNrelReplyMessage = res[sNrelReplyMessage];
                self._kTestUser = res[sTestUser];
                self._kNrelScTextTranslation = res[sNrelScTextTranslation];

                let resValue = true;
                for (let i = 0; i < keynodesList.length; ++i) {
                    const idtf: string = keynodesList[i].idtf;
                    const addr: ScAddr = res[idtf];
                    console.log(`Resolve keynode ${idtf} = ${addr.value}`);

                    resValue = resValue && addr.isValid();
                }

                resolve(resValue);
            });
        });
    }

    get kNrelSystemIdentifier(): ScAddr {
        return this._kNrelSystemIdentifier;
    }

    public get kQuestion(): ScAddr {
        return this._kQuestion;
    }

    public get kQuestionInitiated(): ScAddr {
        return this._kQuestionInitiated;
    }

    public get kQuestionFinished(): ScAddr {
        return this._kQuestionFinished;
    }

    public get kNrelAnswer(): ScAddr {
        return this._kNrelAnswers;
    }

    public get kNrelScTextTranslation(): ScAddr {
        return this._kNrelScTextTranslation;
    }

    public get kNrelReplyMessage(): ScAddr {
        return this._kNrelReplyMessage;
    }

    public get kQuestionFinishedSuccessfully(): ScAddr {
        return this._kQuestionFinishedSuccessfully;
    }

    public get kActionReplyToMessage(): ScAddr {
        return this._kActionReplyToMessage;
    }

    public get kFormatWav(): ScAddr {
        return this._kFormatWav;
    }

    get kFormatM4a(): ScAddr {
        return this._kFormatM4a;
    }

    get kLangEn(): ScAddr {
        return this._kLangEn;
    }

    get kLangRu(): ScAddr {
        return this._kLangRu;
    }

    get kNrelAuthors(): ScAddr {
        return this._kNrelAuthors;
    }

    get kRrel1(): ScAddr {
        return this._kRrel1;
    }

    get kRrel2(): ScAddr {
        return this._kRrel2;
    }

    get kRrel3(): ScAddr {
        return this._kRrel3;
    }

    get kConceptSoundFile(): ScAddr {
        return this._kConceptSoundFile;
    }

    get kConceptTextFile(): ScAddr {
        return this._kConceptTextFile;
    }

    public get kTestUser(): ScAddr {
        return this._kTestUser;
    }
}
