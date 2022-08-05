import { ChatController } from 'chat-ui-react';

export enum Mode {
    Initializing,
    MainUI,
}

export interface State {
    mode: Mode;
    initMessage: string;
    url: string;
    answerText: string;
    answerWaiting: boolean;
    chat: ChatController;
}

export const _initState: State = {
    mode: Mode.Initializing,
    initMessage: '',
    url: '',
    answerText: '',
    answerWaiting: false,
    chat: new ChatController(),
};
